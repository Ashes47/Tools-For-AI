from PIL import Image
import base64
import os
import io
import requests
import uuid
from constants import MERMAID_IMAGE_DIR, IMAGE_DIR
from tools.mermaid.models import Diagrams
from tools.models import CommandResponse
from tools.urlBuilder import urlFor, staticURL


def createMermaidDiagram(mermaidGraph, diagram):
    try:
        graphbytes = mermaidGraph.encode("ascii")

        base64_bytes = base64.b64encode(graphbytes)
        base64_string = base64_bytes.decode("ascii")

        rawImage = requests.get("https://mermaid.ink/img/" + base64_string).content
        imageFile = Image.open(io.BytesIO(rawImage))

        print("Saving Image")

        id = str(uuid.uuid4())
        diagramDirectory = getDirectory(diagram)
        path = os.getcwd() + f"/{IMAGE_DIR}/{MERMAID_IMAGE_DIR}/{diagramDirectory}"

        if not os.path.exists(path):
            os.makedirs(path)

        imageFile.save(f"{path}/{id}.png")
        return CommandResponse(
            output="Image Generated",
            imageURL=urlFor(f"{MERMAID_IMAGE_DIR}/{diagramDirectory}/{id}.png"),
        )

    except:
        return CommandResponse(
            output=f"error: fix the code and try again",
            imageURL=staticURL("invalid.png"),
        )


def getDirectory(diagram: Diagrams) -> str:
    match diagram:
        case Diagrams.FLOWCHART:
            return "flowchart"
        case Diagrams.SEQUENCE:
            return "sequence"
        case Diagrams.CLASS:
            return "class"
        case Diagrams.STATE:
            return "state"
        case Diagrams.ENTITY_RELATIONSHIP:
            return "erdiagram"
        case Diagrams.USER_JOURNEY:
            return "journey"
        case Diagrams.GANTT:
            return "gantt"
        case Diagrams.PIE:
            return "pie"
        case Diagrams.QUADRANT:
            return "quadrant"
        case Diagrams.REQUIREMENT:
            return "requirement"
        case Diagrams.GITGRAPH:
            return "gitgraph"
        case Diagrams.C4:
            return "c4"
        case Diagrams.MINDMAP:
            return "mindmap"
        case Diagrams.TIMELINE:
            return "timeline"
        case Diagrams.SANKEY:
            return "sankey"
        case Diagrams.XYCHART:
            return "xychart"
        case _:
            raise ValueError("Invalid Diagram Type")
