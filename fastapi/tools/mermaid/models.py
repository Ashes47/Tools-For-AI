from typing import Optional
from pydantic import BaseModel
from enum import Enum


class Diagrams(str, Enum):
    FLOWCHART = "Flowchart"
    SEQUENCE = "Sequence Diagram"
    CLASS = "Class Diagram"
    STATE = "State Diagram"
    ENTITY_RELATIONSHIP = "Entity Relationship Diagram"
    USER_JOURNEY = "User Journey"
    GANTT = "Gantt"
    PIE = "Pie Chart"
    QUADRANT = "Quadrant Chart"
    REQUIREMENT = "Requirement Diagram"
    GITGRAPH = "Gitgraph (Git) Diagram"
    C4 = "C4 Diagram"
    MINDMAP = "Mindmap"
    TIMELINE = "Timeline"
    SANKEY = "Sankey"
    XYCHART = "XYChart"


class Mermaid(BaseModel):
    mermaidText: str
    diagram: Diagrams

    class Config:
        json_schema_extra = {
            "example": {
                "mermaidText": "flowchart TD\n    A[Christmas] -->|Get money| B(Go shopping)\n    B --> C{Let me think}\n    C -->|One| D[Laptop]\n    C -->|Two| E[iPhone]\n    C -->|Three| F[fa:fa-car Car]",
                "diagram": "Flowchart",
            }
        }


class SmartMermaid(BaseModel):
    text: str
    diagram: Diagrams
    mermaidCode: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Change Christmas to New Year",
                "diagram": "Flowchart",
                "mermaidCode": "flowchart TD\n    A[Christmas] -->|Get money| B(Go shopping)\n    B --> C{Let me think}\n    C -->|One| D[Laptop]\n    C -->|Two| E[iPhone]\n    C -->|Three| F[fa:fa-car Car]",
            }
        }


class LLMResult(BaseModel):
    code: str
