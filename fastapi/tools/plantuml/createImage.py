import io
import os
from PIL import Image
from plantuml import PlantUML
import uuid
from constants import PLANTUML_IMAGE_DIR, IMAGE_DIR
from tools.plantuml.models import Diagrams
from tools.models import ImageURL
from tools.urlBuilder import urlFor


async def createPlantUML(plantumlText, diagram):
    try:
        # create a server object to call for your computations
        print("Calling PlantUML Server")
        server = PlantUML(
            url="https://www.plantuml.com/plantuml/img/",
            basic_auth={},
            form_auth={},
            http_opts={},
            request_opts={},
        )

        # Send and compile your diagram files to/with the PlantUML server
        rawImage = server.processes(plantumlText)
        imageStream = io.BytesIO(rawImage)
        imageFile = Image.open(imageStream)

        print("Saving Image")
        id = str(uuid.uuid4())
        diagramDirectory = getDirectory(diagram)
        path = os.getcwd() + f"/{IMAGE_DIR}/{PLANTUML_IMAGE_DIR}/{diagramDirectory}"

        if not os.path.exists(path):
            os.makedirs(path)

        imageFile.save(f"{path}/{id}.png")
        return ImageURL(
            imageURL=urlFor(f"{PLANTUML_IMAGE_DIR}/{diagramDirectory}/{id}.png")
        )
    except:
        return "Incorrect Plantuml Code, fix the code and try again"


def getDirectory(diagram):
    match diagram:
        case Diagrams.UML_ACTIVITY:
            return "uml_activity"
        case Diagrams.ARCHIMATE:
            return "archimate"
        case Diagrams.ASCIIMATH:
            return "asciimath"
        case Diagrams.UML_CLASS:
            return "uml_class"
        case Diagrams.UML_COMPONENT:
            return "uml_component"
        case Diagrams.DEPLOYMENT:
            return "deployment"
        case Diagrams.DITAA:
            return "ditaa"
        case Diagrams.GANTT:
            return "gantt"
        case Diagrams.GRAPHVIZ_DOT:
            return "graphviz_dot"
        case Diagrams.JLATEXMATH:
            return "jlatexmath"
        case Diagrams.GLOBAL_KEYWORDS_OPTIONS:
            return "global_keywords_options"
        case Diagrams.UML_OBJECT:
            return "uml_object"
        case Diagrams.UML_SEQUENCE:
            return "uml_sequence"
        case Diagrams.UML_STATE:
            return "uml_state"
        case Diagrams.TIMING:
            return "timing"
        case Diagrams.UML_USE_CASE:
            return "uml_use_case"
        case Diagrams.WIRE_FRAME:
            return "wire_frame"
        case _:
            raise ValueError("Invalid Diagram Type")
