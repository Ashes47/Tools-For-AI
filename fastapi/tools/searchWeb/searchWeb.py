import requests
from requests.auth import HTTPBasicAuth
from tools.searchWeb.models import SearchParams, SearchResponse, SearchResult
import os


def search(params: SearchParams):
    base_url = os.getenv("SEARCH_ENGINE_URL")
    auth = HTTPBasicAuth(
        os.getenv("SEARCH_ENGINE_USERNAME"), os.getenv("SEARCH_ENGINE_PASSWORD")
    )
    query = params.to_search_query()

    search_params = {
        "q": query.query,
        "format": params.format,
        "categories": params.categories,
        "language": params.language,
        "safesearch": params.safesearch.value,
        "time_range": params.time_range,
        "engines": [engine.name for engine in params.engines],
        "pageno": params.pageno,
        "limit": params.limit,
        "timeout_limit": params.timeout_limit,
        "external_bang": params.external_bang,
        "redirect_to_first_result": params.redirect_to_first_result,
    }

    response = requests.get(base_url, params=search_params, auth=auth)

    if response.status_code == 200:
        data = response.json()

        # Filter results by requested engines
        requested_engines = set(engine.name for engine in params.engines)
        filtered_results = [
            result
            for result in data.get("results", [])
            if set(result.get("engines", [])) & requested_engines
        ]

        # Sort results by score in descending order
        sorted_results = sorted(
            filtered_results, key=lambda x: x.get("score", 0), reverse=True
        )

        # Limit results to specified limit
        limited_results = sorted_results[: params.limit]

        # Convert results to SearchResult models
        search_results = [
            SearchResult(
                url=res["url"],
                title=res["title"],
                content=res["content"],
                score=res.get("score"),
                category=res.get("category"),
            )
            for res in limited_results
        ]

        return SearchResponse(
            query=data["query"], answers=data.get("answers", []), results=search_results
        )
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")