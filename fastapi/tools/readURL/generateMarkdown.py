from tools.readURL.models import ContentURL
from tools.models import ReadURL
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import MarkdownifyTransformer
from tools.searchWeb.utils import process_search_results


def generateMarkdownForPage(data: ReadURL) -> ContentURL:
    try:
        loader = AsyncHtmlLoader([data.url])
        docs = loader.load()

        md = MarkdownifyTransformer()
        converted_docs = md.transform_documents(docs)[0].page_content

        if data.summarize:
            converted_docs = process_search_results(
                None, converted_docs, data.use_openAI
            )

        return ContentURL(response=converted_docs)
    except Exception as e:
        return ContentURL(response=f"Error reading Webpage: {e}")
