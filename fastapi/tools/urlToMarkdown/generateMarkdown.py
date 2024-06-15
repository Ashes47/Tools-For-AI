from tools.urlToMarkdown.models import BrowsingRequest, BrowsingResult
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import MarkdownifyTransformer

async def generateMarkdownForPage(data: BrowsingRequest) -> BrowsingResult:
    try:
        # Fetch the webpage content
        loader = AsyncHtmlLoader([data.url])
        docs = loader.load()

        md = MarkdownifyTransformer()
        converted_docs = md.transform_documents(docs)
        
        return BrowsingResult(response=converted_docs[0].page_content)
    except Exception as e:
        return BrowsingResult(response=f"Error reading Webpage: {e}")