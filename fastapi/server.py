# fastapi library imports
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
# Local imports
from constants import URL, IMAGE_DIR

# Import Routes
from apis.base import api_router

# FastAPI Config
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## Include routes
app.include_router(api_router)

## Mount static directories
app.mount("/" + IMAGE_DIR, StaticFiles(directory="images"), name="images")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/privacy", response_class=HTMLResponse)
async def privacy(request: Request):
  return templates.TemplateResponse("privacy.html",
                                    context={"request": request})
# Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Youtube to Mindmap",
        version="1.0.0",
        description="API for converting youtube videos to transcript and creating mindmaps",
        routes=app.routes,
        servers=[{"url": URL, "description": "Youtube to Mindmap"}],
    )
    openapi_schema["info"]["x-logo"] = {"url": URL + "/static/logo.png"}
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
