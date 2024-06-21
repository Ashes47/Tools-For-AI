from tools.readURL.models import ContentURL, ReadURL
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import MarkdownifyTransformer
from tools.searchWeb.utils import process_search_results


def generateMarkdownForPage(data: ReadURL) -> ContentURL:
    try:
        loader = AsyncHtmlLoader(data.urls)
        docs = loader.load()

        md = MarkdownifyTransformer()
        converted_docs = md.transform_documents(docs)

        content = []

        if not data.summarize:
            for doc in converted_docs:
                content.append(doc.page_content)
            return ContentURL(urls=data.urls, content=content)

        for converted_doc in converted_docs:
            data = process_search_results(
                None, converted_doc.page_content, data.use_openAI
            )
            content.append(data)

        return ContentURL(urls=data.urls, content=content)
    except Exception as e:
        return ContentURL(urls=[], content=["Error reading Webpage: {e}"])
