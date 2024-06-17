from tools.readURL.models import ContentURL
from tools.models import ReadURL
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import MarkdownifyTransformer
import requests


def generateMarkdownForPage(data: ReadURL) -> ContentURL:
    try:
        loader = AsyncHtmlLoader([data.url])
        docs = loader.load()

        md = MarkdownifyTransformer()
        converted_docs = md.transform_documents(docs)

        return ContentURL(response=converted_docs[0].page_content)
    except Exception as e:
        return ContentURL(response=f"Error reading Webpage: {e}")
