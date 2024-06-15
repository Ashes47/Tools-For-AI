from tools.braveSearch.models import BraveSearchRequest, BraveSearchResult
from langchain_community.tools import BraveSearch
import ast
import os


async def braveSearh(data: BraveSearchRequest) -> BraveSearchResult:
    try:
        tool = BraveSearch.from_api_key(
            api_key=os.environ["BraveAPIKEY"], search_kwargs={"count": 4}
        )
        response = tool.run(data.topic)
        result = ast.literal_eval(response)
        return BraveSearchResult(
            titles=[x["title"] for x in result],
            links=[x["link"] for x in result],
            descriptions=[x["snippet"] for x in result],
        )

    except Exception as e:
        return BraveSearchResult(
            titles=["Exception"], links=[], descriptions=[f"Error: {e}"]
        )
