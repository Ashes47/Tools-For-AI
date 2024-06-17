from bs4 import BeautifulSoup
from minify_html import minify
from urllib.parse import urljoin
import tempfile
from langchain_community.document_transformers import MarkdownifyTransformer
from langchain_community.document_loaders import UnstructuredHTMLLoader


def html_to_markdown(minimized_body: str) -> str:
    # Create a temporary file to store the HTML content
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp_file:
        tmp_file.write(minimized_body.encode('utf-8'))
        tmp_file_path = tmp_file.name

    # Load the HTML content
    loader = UnstructuredHTMLLoader(tmp_file_path)
    docs = loader.load()

    # Transform the loaded HTML content to Markdown
    md = MarkdownifyTransformer()
    converted_docs = md.transform_documents(docs)

    # Return the Markdown content
    return converted_docs[0].page_content

def cleanup_html(html_content: str, base_url: str) -> str:
    """
    Processes HTML content by removing unnecessary tags, minifying the HTML, and extracting the title and body content.

    Args:
        html_content (str): The HTML content to be processed.

    Returns:
        str: A string combining the parsed title and the minified body content. If no body content is found, it indicates so.

    Example:
        >>> html_content = "<html><head><title>Example</title></head><body><p>Hello World!</p></body></html>"
        >>> remover(html_content)
        'Title: Example, Body: <body><p>Hello World!</p></body>'

    This function is particularly useful for preparing HTML content for environments where bandwidth usage needs to be minimized.
    """

    soup = BeautifulSoup(html_content, 'html.parser')

    # Title Extraction
    title_tag = soup.find('title')
    title = title_tag.get_text() if title_tag else ""

    # Script and Style Tag Removal
    for tag in soup.find_all(['script', 'style']):
        tag.extract()

    # Links extraction
    links = soup.find_all('a')
    link_urls = []
    for link in links:
        if 'href' in link.attrs:
            link_urls.append(urljoin(base_url, link['href']))

    # Images extraction
    images = soup.find_all('img')
    image_urls = []
    for image in images:
        if 'src' in image.attrs:
            # if http or https is not present in the image url, join it with the base url
            if 'http' not in image['src']:
                image_urls.append(urljoin(base_url, image['src']))
            else:
                image_urls.append(image['src'])

    # Body Extraction (if it exists)
    body_content = soup.find('body')
    if body_content:
        # Minify the HTML within the body tag
        minimized_body = minify(str(body_content))

        return title, html_to_markdown(minimized_body), link_urls, image_urls
        # return "Title: " + title + ", Body: " + minimized_body + ", Links: " + str(link_urls) + ", Images: " + str(image_urls)

    # throw an error if no body content is found
    return title, "No Body Content Found", link_urls, image_urls