from tools.searchYoutube.models import YoutubeSearchRequest, YoutubeSearchResult
from langchain_community.tools import YouTubeSearchTool
import ast
import os


async def youtubeSearch(data: YoutubeSearchRequest) -> YoutubeSearchResult:
    try:
        tool = YouTubeSearchTool()
        response = tool.run(data.topic)
        result = ast.literal_eval(response)
        return YoutubeSearchResult(links=result)
    except Exception as e:
        return YoutubeSearchResult(links=[f"Exception: {e}"])
