from tools.deepReadURL.models import DeepResponse
from tools.models import ReadURL
import requests
from tools.deepReadURL.crawler import cleanup_html
import concurrent.futures


def deepSearchForPage(data: ReadURL) -> DeepResponse:
    try:
        urls = []
        information = []
        source = data.url
        response = requests.get(source)
        title, minimized_body, link_urls, image_urls = cleanup_html(
            response.text, source
        )
        limit_pages = data.limit - 1
        link_urls = list(set(link_urls))
        if len(link_urls) > limit_pages:
            link_urls = link_urls[:limit_pages]
        content = f"Title: {title}, Body: {minimized_body}, Links: {link_urls}, Images: {image_urls}"

        urls.append(source)
        information.append(content)

        def fetch_and_process(link):
            try:
                print(f"Fetching {link}")
                response = requests.get(link)
                title, minimized_body, link_urls, image_urls = cleanup_html(
                    response.text, link
                )
                content = f"Title: {title}, Body: {minimized_body}, Links: {link_urls}, Images: {image_urls}"
                return (link, content)
            except Exception as e:
                print(f"Exception on reading {link}: {e}")
                return None

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(fetch_and_process, link) for link in link_urls]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    link, content = result
                    urls.append(link)
                    information.append(content)

        return DeepResponse(urls=urls, info=information)
    except Exception as e:
        print(f"Exception on reading {source}: {e}")
        return DeepResponse(urls=[], info=["Could not read the page"])
