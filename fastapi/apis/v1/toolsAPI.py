from fastapi import APIRouter, Request
from auth import validateToken
from tools.deepReadURL.models import DeepBrowsingResult
from tools.deepReadURL.generateMarkdown import deepSearchForPage
from tools.searchYoutube.models import YoutubeSearchRequest, YoutubeSearchResult
from tools.searchYoutube.youtubeSearch import youtubeSearch
from tools.braveSearch.models import BraveSearchRequest, BraveSearchResult
from tools.braveSearch.braveSearch import braveSearh
from tools.readURL.generateMarkdown import generateMarkdownForPage
from tools.readURL.models import BrowsingResult
from tools.youtube.models import Transcription, TranscriptionResponse
from tools.youtube.getTranscript import getTranscription
from tools.mermaid.models import Mermaid
from tools.mermaid.createImage import createMermaidDiagram
from tools.plantuml.models import PlantUML
from tools.plantuml.createImage import createPlantUML
from tools.pythonShell.models import CommandRequest
from tools.models import CommandResponse, BrowsingRequest
from tools.pythonShell.createImage import execute_command
from tools.wordcloud.models import WordCloudRequest, create_word_cloud
from tools.wordcloud.createImage import createWordCloud
from tools.apexgraphs.createImage import createApexCharts
from tools.apexgraphs.models import ApexChartRequest
from tools.graphviz.models import GraphvizRequest
from tools.graphviz.createImage import createGraphViz
from tools.quickchart.createImage import createQuickCharts
from tools.quickchart.models import QuickChartRequest
from store.saveCode import storeCodeAsFile
from tools.threadingUtils import run_in_threadpool

toolsRouter = APIRouter(prefix="/tool")


# Fetch Transcription from a youtube link
@toolsRouter.post("/getTranscript")
async def getTranscript(data: Transcription, request: Request) -> TranscriptionResponse:
    """Get Youtube Transcription
    This function takes in the URL for a YouTube video and the language code for transcription and returns it's transcription with start time and duration in seconds
    """
    if not validateToken(request.headers["Authorization"]):
        raise Exception("Invalid Token")

    print(f"URL: {data.url}\nFetching transcription")

    transcript = await run_in_threadpool(getTranscription, data)
    return TranscriptionResponse(transcript=transcript)


# Create a Mermaid Diagram from text
@toolsRouter.post("/createMermaid")
async def createMermaid(data: Mermaid, request: Request) -> CommandResponse:
    """Get Mermaid Image
    This functions takes in code for the mindmap diagram in Markmap language for Mermaid and returns Mermaid Image
    """
    token = request.headers["Authorization"]
    if not validateToken(token):
        raise Exception("Invalid Token")

    print(f"Mermaid Diagram Recieved : {data.mermaidText}")
    print(f"Mermaid Text Recieved : {data.diagram}")
    storeCodeAsFile(data.mermaidText, f"mermaid/{data.diagram.value}")

    return await run_in_threadpool(createMermaidDiagram, data.mermaidText, data.diagram)


# Create a Plantuml Diagram from text
@toolsRouter.post("/createPlantuml")
async def createPlantuml(data: PlantUML, request: Request) -> CommandResponse:
    """Get Plantuml Image
    This functions takes in code for the Plantuml diagram in Markmap language for Plantuml and returns Plantuml Image
    """
    token = request.headers["Authorization"]
    if not validateToken(token):
        raise Exception("Invalid Token")

    print(f"Plantuml Diagram Recieved : {data.plantumlText}")
    print(f"Plantuml Text Recieved : {data.diagram}")
    storeCodeAsFile(data.plantumlText, f"plantuml/{data.diagram.value}")

    return await run_in_threadpool(createPlantUML, data.plantumlText, data.diagram)


# Create a Matplotlib Diagram from text
@toolsRouter.post("/createMatplotlib")
async def createMatplotlib(data: CommandRequest, request: Request) -> CommandResponse:
    """Get Matplotlib Image
    This functions takes in code in python language to create matplotlib diagram and returns the matplotlib diagram generated
    """
    token = request.headers["Authorization"]
    if not validateToken(token):
        raise Exception("Invalid Token")

    print(f"Python Code Recieved:\n{data.code}")

    return await run_in_threadpool(execute_command, data)


# Create a Seaborn Diagram from text
@toolsRouter.post("/createSeaborn")
async def createSeaborn(data: CommandRequest, request: Request) -> CommandResponse:
    """Get Seaborn Image
    This functions takes in code in python language to create stunning seaborn diagram and returns the seaborn diagram generated
    """
    token = request.headers["Authorization"]
    if not validateToken(token):
        raise Exception("Invalid Token")

    seaborn_config = {
        "style": "whitegrid",  # A clean background with gridlines
        "palette": "bright",  # A bright and vibrant color palette
        "context": "paper",  # Medium elements, suitable for presentations
        "font_scale": 1.25,  # Slightly larger font size for readability
    }

    print(f"Python Code Recieved:\n{data.code}")

    return await run_in_threadpool(execute_command, data, seaborn_config)


@toolsRouter.post("/createWordcloud")
async def createWordcloud(data: WordCloudRequest, request: Request) -> CommandResponse:
    """
    Create WordCloud
    This function takes in text with optional other parameters and creates a wordcloud.
    text: keywords with count. ex: "hello:10,world:5,testing:5,123"
    """
    token = request.headers["Authorization"]
    if not validateToken(token):
        raise Exception("Invalid Token")

    print(f"Wordcloud request received:\n{data.text}")

    return await run_in_threadpool(createWordCloud, create_word_cloud(data))


@toolsRouter.post("/createApexcharts")
async def createApexcharts(data: ApexChartRequest, request: Request) -> CommandResponse:
    """
    Create Apexcharts
    This function takes in config with optional width and height and creates an Apexcharts.
    """
    token = request.headers["Authorization"]
    if not validateToken(token):
        raise Exception("Invalid Token")

    print(f"Apexcharts request received:\n{data.config}")
    storeCodeAsFile(data.config, f"apexcharts")

    return await run_in_threadpool(createApexCharts, data)


@toolsRouter.post("/createGraphviz")
async def createGraphviz(data: GraphvizRequest, request: Request) -> CommandResponse:
    """Get Graphviz Image
    This functions takes in code for the Graphviz diagram in Markmap language with layout and returns Graphviz Image
    """
    token = request.headers["Authorization"]
    if not validateToken(token):
        raise Exception("Invalid Token")

    print(f"Graphviz request received:\n{data.graph}")
    storeCodeAsFile(data.graph, f"graphviz")

    return await run_in_threadpool(createGraphViz, data)


@toolsRouter.post("/createQuickChart")
async def createQuickChart(
    data: QuickChartRequest, request: Request
) -> CommandResponse:
    """
    Create QuickChart
    This function takes in parameters: text with width and height and background color and creates a QuickChart.
    """
    token = request.headers["Authorization"]
    if not validateToken(token):
        raise Exception("Invalid Token")

    print(f"QuickChart request received:\n{data.chart}")
    storeCodeAsFile(data.chart, f"quickcharts")

    return await run_in_threadpool(createQuickCharts, data)


@toolsRouter.post("/readWebpage")
async def readWebPage(data: BrowsingRequest, request: Request) -> BrowsingResult:
    """
    Read Webpages
    This function allows to convert a webpage to Markdown by sharing it's URL
    """
    token = request.headers["Authorization"]
    if not validateToken(token):
        raise Exception("Invalid Token")

    print(f"readWebpage request received:\n{data.url}")

    return await run_in_threadpool(generateMarkdownForPage, data)

@toolsRouter.post("/deepReadWebpage")
def deepReadWebPage(data: BrowsingRequest, request: Request) -> DeepBrowsingResult:
    """
    Deep Read Webpages
    This function allows you to navigate to the links within the input webpage and return information from all the links found + the original webpage.
    """
    token = request.headers["Authorization"]
    if not validateToken(token):
        raise Exception("Invalid Token")
    
    print(f"deepReadWebpage request received:\n{data.url}")

    return deepSearchForPage(data)


@toolsRouter.post("/searchBrave")
async def searchBrave(data: BraveSearchRequest, request: Request) -> BraveSearchResult:
    """
    Search Brave
    This function allows to search for a topic on Web via Brave Search
    """
    token = request.headers["Authorization"]
    if not validateToken(token):
        raise Exception("Invalid Token")

    print(f"searchBrave request received:\n{data.topic}")

    return await run_in_threadpool(braveSearh, data)


@toolsRouter.post("/searchYoutube")
async def searchYoutube(
    data: YoutubeSearchRequest, request: Request
) -> YoutubeSearchResult:
    """
    Search Youtube
    This function allows to search for a topic on Youtube
    """
    token = request.headers["Authorization"]
    if not validateToken(token):
        raise Exception("Invalid Token")

    print(f"searchYoutube request received:\n{data.topic}")

    return await run_in_threadpool(youtubeSearch, data)
