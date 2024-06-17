from tools.readURL.models import BrowsingResult
from tools.models import BrowsingRequest
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import MarkdownifyTransformer
import requests


def generateMarkdownForPage(data: BrowsingRequest) -> BrowsingResult:
    try:
        loader = AsyncHtmlLoader([data.url])
        docs = loader.load()

        md = MarkdownifyTransformer()
        converted_docs = md.transform_documents(docs)

        return BrowsingResult(response=converted_docs[0].page_content)
    except Exception as e:
        return BrowsingResult(response=f"Error reading Webpage: {e}")