# Standard library imports
import os
from threading import Thread
# Third-party library imports
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
import uvicorn
# Local imports
from models import Transcription, PlantUML, Mermaid, TranscriptionResponse, ImageURL
from helperPlantUML import createPlantUML
from helperYoutube import getTranscription, validateToken
from helperMermaid import createMermaid

############## FastAPI Config #######################################################
app = FastAPI(
    title="Youtube to Mindmap",
    description=
    """API for converting youtube videos to transcript and creating mindmaps""",
    version="1.0.0",
    servers=[
            {
                "url": "https://mewow.dev",
                "description": "Youtube to Mindmap"
            }
        ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
#####################################################################################


############## HealthCheck ##########################################################
@app.get("/ping")
async def ping():
  return {"ping": "pong"}


######################################################################################


@app.post("/getTranscript")
async def getTranscript(data: Transcription,
                  request: Request) -> TranscriptionResponse:
  """Get Youtube Transcription
  This function takes in the URL for a YouTube video and returns it's transcription with start time and duration"""
  url = data.url
  token = request.headers["Authorization"]
  if not validateToken(token):
    raise Exception("Invalid Token")
  print(f"URL: {url}")
  print("Fetching transcription")
  transcript = await getTranscription(url)
  return TranscriptionResponse(transcript=transcript)


@app.post('/getPlantUML')
async def getPlantUML(data: PlantUML, request: Request) -> ImageURL:
  """Get PlantUML Image
  This functions takes in code for the mindmap diagram in Markmap language for plantUML and returns plantUML Image
  """
  token = request.headers["Authorization"]
  if not validateToken(token):
    raise Exception("Invalid Token")
  plantumlText = data.plantumlText
  print(f"PlantUML Text Recieved: {plantumlText}")

  fileName = await createPlantUML(plantumlText)
  img_url = request.url_for('static', path=fileName)
  return ImageURL(imageURL=img_url._url)

  # image_bytes: bytes = createPlantUML(plantumlText)
  # return Response(content=image_bytes, media_type="image/png")


@app.post('/getMermaid')
async def getMermaid(data: Mermaid, request: Request) -> ImageURL:
  """Get Mermaid Image
  This functions takes in code for the mindmap diagram in Markmap language for Mermaid and returns Mermaid Image
  """
  token = request.headers["Authorization"]
  if not validateToken(token):
    raise Exception("Invalid Token")
  mermaidText = data.mermaidText
  print(f"Mermaid Text Recieved : {mermaidText}")

  fileName = await createMermaid(mermaidText)
  img_url = request.url_for('static', path=fileName)
  return ImageURL(imageURL=img_url._url)

  # image_bytes: bytes = createMermaid(mermaidText)
  # return Response(content=image_bytes, media_type="image/png")


@app.get('/clean')
async def clean(request: Request):
  token = request.headers["Authorization"]
  folder = './static'
  for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
      os.remove(file_path)
    except Exception as e:
      print('Failed to delete %s. Reason: %s' % (file_path, e))

  return {"message": "Temp Folder Cleaned"}


templates = Jinja2Templates(directory="templates")


@app.get("/privacy", response_class=HTMLResponse)
async def privacy(request: Request):
  return templates.TemplateResponse("privacy.html",
                                    context={"request": request})


############## Documentation #########################################################
def custom_openapi():
  if app.openapi_schema:
    return app.openapi_schema
  openapi_schema = get_openapi(
      title="Youtube to Mindmap",
      version="1.0.0",
      description=
      "API for converting youtube videos to transcript and creating mindmaps",
      routes=app.routes,
  )
  openapi_schema["info"]["x-logo"] = {
      "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
  }
  app.openapi_schema = openapi_schema
  return app.openapi_schema


app.openapi = custom_openapi
######################################################################################
