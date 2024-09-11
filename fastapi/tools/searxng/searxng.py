import httpx
from redis.asyncio import Redis
from tools.readURL.models import ReadURL
from tools.readURL.generateMarkdown import generateMarkdownForPage
from tools.searxng.models.models import (
    SearXNGSearchResults,
    SearchResultItem,
    SearchResultVideo,
    SearchResultImage,
)
from typing import Optional
import os
from fastapi import APIRouter, Request, HTTPException

# Fetch environment variables
SEARXNG_API_URL = os.getenv("SEARXNG_API_URL", "http://searxng:8080")
SEARXNG_MAX_RESULTS = int(os.getenv("SEARXNG_MAX_RESULTS", "50"))
SEARXNG_CRAWL_MULTIPLIER = int(os.getenv("SEARXNG_CRAWL_MULTIPLIER", "4"))
SEARXNG_DEFAULT_DEPTH = os.getenv("SEARXNG_DEFAULT_DEPTH", "basic")
SEARXNG_ENGINES = os.getenv("SEARXNG_ENGINES", "google,bing,duckduckgo,wikipedia,brave")
SEARXNG_SAFESEARCH = int(os.getenv("SEARXNG_SAFESEARCH", "0"))
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
CACHE_TTL = 3600  # Cache time-to-live in seconds
PAGES_ADVANCED_RESULT = 2

searxngRouter = APIRouter(prefix="/tool")


# Redis configuration
redis_client = Redis.from_url(REDIS_URL)


# Updated fetch function to handle optional images and videos with correct categories
async def fetch_search_results(
    query: str,
    max_results: int,
    include_images: bool,
    include_videos: bool,
    advanced_query: bool,
) -> SearXNGSearchResults:
    url = f"{SEARXNG_API_URL}/search"
    results_per_page = 10
    pages_needed = (max_results + results_per_page - 1) // results_per_page

    # Dynamically set the categories based on user
    searchDepth = SEARXNG_DEFAULT_DEPTH
    categories = ["general"]
    if include_images:
        categories.append("images")
    if include_videos:
        categories.append("videos")
    if advanced_query:
        searchDepth = "advanced"

    async with httpx.AsyncClient() as client:
        params = {
            "q": query,
            "format": "json",
            "categories": ",".join(categories),
            "pageno": pages_needed,
            "safesearch": SEARXNG_SAFESEARCH,
            "engines": SEARXNG_ENGINES,
            "searchDepth": searchDepth,
        }
        response = await client.get(url, params=params)
        response.raise_for_status()
        return transform_to_search_results(
            response.json(), max_results, include_images, include_videos
        )


# Updated transformation function to include images and videos conditionally
def transform_to_search_results(
    response: dict, max_results: int, include_images: bool, include_videos: bool
) -> SearXNGSearchResults:
    results = [
        SearchResultItem(
            title=res["title"], url=res["url"], content=res.get("content", "")
        )
        for res in response.get("results", [])
        if "title" in res and "url" in res
    ][:max_results]

    images = []
    videos = []

    if include_images:
        images = [
            SearchResultImage(
                url=res["img_src"], description=res.get("description", "")
            )
            for res in response.get("results", [])
            if "img_src" in res and res["img_src"]
        ][:max_results]

    if include_videos:
        videos = [
            SearchResultVideo(
                url=res["url"], title=res["title"], duration=res.get("duration")
            )
            for res in response.get("results", [])
            if "category" in res and res["category"] == "videos"
        ][:max_results]

    return SearXNGSearchResults(
        query=response.get("query", ""),
        results=results,
        images=images if include_images else None,
        videos=videos if include_videos else None,
        number_of_results=len(results),
    )


async def get_cached_results(cache_key: str) -> Optional[SearXNGSearchResults]:
    result = await redis_client.get(cache_key)
    if result:
        return SearXNGSearchResults.parse_raw(result)
    return None


async def set_cached_results(cache_key: str, results: SearXNGSearchResults):
    await redis_client.set(cache_key, results.json(), ex=CACHE_TTL)


@searxngRouter.post("/search", response_model=SearXNGSearchResults)
async def search(request: Request):
    data = await request.json()
    query = data.get("query")
    max_results = min(
        int(data.get("maxResults", SEARXNG_MAX_RESULTS)), SEARXNG_MAX_RESULTS
    )
    include_images = data.get("includeImages", False)
    include_videos = data.get("includeVideos", False)
    advanced_query = data.get("advancedQuery", False)

    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")

    cache_key = f"search:{query}:{max_results}:{'images' if include_images else ''}:{'videos' if include_videos else ''}"
    cached_results = await get_cached_results(cache_key)
    if cached_results:

        if advanced_query:
            urls_to_crawl = [
                item.url for item in cached_results.results[:PAGES_ADVANCED_RESULT]
            ]
            advanced_results = generateMarkdownForPage(
                ReadURL(urls=urls_to_crawl, summarize=True)
            )
            cached_results.advanced_result = "\n".join(advanced_results.content)

        return cached_results

    results = await fetch_search_results(
        query, max_results, include_images, include_videos, advanced_query
    )
    if advanced_query:
        urls_to_crawl = [item.url for item in results.results[:PAGES_ADVANCED_RESULT]]
        advanced_results = generateMarkdownForPage(
            ReadURL(urls=urls_to_crawl, summarize=True)
        )
        results.advanced_result = "\n".join(advanced_results.content)

    await set_cached_results(cache_key, results)
    return results


# Define the cleanup function
async def cleanup_expired_cache():
    # Assuming we want to delete keys explicitly if they are found to be expired
    async for key in redis_client.scan_iter(match="search:*", count=100):
        ttl = await redis_client.ttl(key)
        if ttl <= 0:
            await redis_client.delete(key)
