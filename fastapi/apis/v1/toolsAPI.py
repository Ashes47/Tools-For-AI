from fastapi import APIRouter, Request
from auth import validateToken
from tools.youtube.models import Transcription, TranscriptionResponse
from tools.youtube.getTranscript import getTranscription
from tools.mermaid.models import Mermaid
from tools.mermaid.createImage import createMermaidDiagram
from tools.plantuml.models import PlantUML
from tools.plantuml.createImage import createPlantUML
from tools.pythonShell.models import CommandRequest
from tools.models import CommandResponse
from tools.pythonShell.createImage import execute_command
from tools.wordcloud.models import WordCloudRequest, create_word_cloud
from tools.wordcloud.createImage import createWordCloud
from store.saveCode import storeCodeAsFile

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

    transcript = await getTranscription(data)
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

    return await createMermaidDiagram(data.mermaidText, data.diagram)


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

    return await createPlantUML(data.plantumlText, data.diagram)


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

    return await execute_command(data)


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

    return await execute_command(data, seaborn_config)


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

    return await createWordCloud(create_word_cloud(data))
