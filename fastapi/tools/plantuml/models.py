from pydantic import BaseModel
from enum import Enum


class Diagrams(str, Enum):
    UML_ACTIVITY = "UML Activity Diagram"
    ARCHIMATE = "Archimate Diagram"
    ASCIIMATH = "AsciiMath Diagram"
    UML_CLASS = "UML Class Diagram"
    UML_COMPONENT = "UML Component Diagram"
    DEPLOYMENT = "Deployment Diagram"
    DITAA = "DITAA Diagram"
    GANTT = "Gantt Diagram"
    GRAPHVIZ_DOT = "GraphViz DOT Diagram"
    JLATEXMATH = "JLatexMath Diagram"
    GLOBAL_KEYWORDS_OPTIONS = "Global Keywords and Options"
    UML_OBJECT = "UML Object Diagram"
    UML_SEQUENCE = "UML Sequence Diagram"
    UML_STATE = "UML State Diagram"
    TIMING = "Timing Diagram"
    UML_USE_CASE = "UML Use Case Diagram"
    WIRE_FRAME = "Wire Frame Diagram"


class PlantUML(BaseModel):
    plantumlText: str
    diagram: Diagrams

    class Config:
        json_schema_extra = {
            "example": {
                "plantumlText": "@startmindmap\n* GPT Opportunities\n** Building GPTs for GPT Store\n*** Focus on unique GPTs\n**** Use private data sets\n**** Integrate unique APIs\n*** Be aware of competition\n*** Potential OpenAI integration\n** Custom GPTs for Businesses\n*** Start an AI agency\n**** Specialize in GPT solutions\n**** Plan, create, sell tailored GPTs\n*** Consistent revenue stream\n*** Adapt to OpenAI updates\n** Specializing in GPT Strategy and Development as a Freelancer\n*** Growing demand for skilled freelancers\n**** Learn Python and JavaScript\n**** Build GPTs using assistant API\n**** Join communities for clients\n**** Build a personal brand\n*** Importance of Hands-on Experience\n**** Build GPTs\n**** Understand assistant API\n**** Stay updated with AI and GPT tech\n**** Leverage private data and unique applications\n@endmindmap",
                "diagram": "UML Activity Diagram",
            }
        }
