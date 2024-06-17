import json
from tools.urlBuilder import staticURL
from tools.models import CommandResponse
from tools.mermaid.prompts import *
from tools.mermaid.models import SmartMermaid, LLMResult
from tools.mermaid.createImage import createMermaidDiagram
import g4f
from retry import retry

def generateMermaidCode(data: SmartMermaid):
    try:
        match (data.diagram):
            case "Flowchart":
                return getCode(data.text, FLOWCHART, data.diagram, data.mermaidCode)
            case "Sequence Diagram":
                return getCode(data.text, SEQUENCE, data.diagram, data.mermaidCode)
            case "Class Diagram":
                return getCode(data.text, CLASS, data.diagram, data.mermaidCode)
            case "State Diagram":
                return getCode(data.text, STATE, data.diagram, data.mermaidCode)
            case "Entity Relationship Diagram":
                return getCode(data.text, ERDIAGRAM, data.diagram, data.mermaidCode)
            case "User Journey":
                return getCode(data.text, JOURNEY, data.diagram, data.mermaidCode)
            case "Gantt":
                return getCode(data.text, GANTT, data.diagram, data.mermaidCode)
            case "Pie Chart":
                return getCode(data.text, PIE, data.diagram, data.mermaidCode)
            case "Quadrant Chart":
                return getCode(data.text, QUADRANT, data.diagram, data.mermaidCode)
            case "Requirement Diagram":
                return getCode(data.text, REQUIREMENT, data.diagram, data.mermaidCode)
            case "Gitgraph (Git) Diagram":
                return getCode(data.text, GITGRAPH, data.diagram, data.mermaidCode)
            case "C4 Diagram":
                return getCode(data.text, C4DIAGRAM, data.diagram, data.mermaidCode)
            case "Mindmap":
                return getCode(data.text, MINDMAP, data.diagram, data.mermaidCode)
            case "Timeline":
                return getCode(data.text, TIMELINE, data.diagram, data.mermaidCode)
            case "Sankey":
                return getCode(data.text, SANKEY, data.diagram, data.mermaidCode)
            case "XYChart":
                return getCode(data.text, XYCHART, data.diagram, data.mermaidCode)
            case _:
                raise Exception("Invalid Diagram Type")
    except Exception as e:
        return CommandResponse(
            output=f"Please retry, could not generate code: {e}",
            imageURL=staticURL("invalid.png"),
        )


@retry(tries=5, delay=2, backoff=2)
def getCode(text: str, prompt: str, diagram_type: str, existing_code: str = None):
    userPrompt = f"create mermaid code for: {text}."
    if existing_code:
        userPrompt = (
            userPrompt + f" existing code for mermaid diagrams: {existing_code}"
        )

    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_35_turbo_16k_0613,
        temperature=0.24,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": userPrompt + f" pydantic response schema: {LLMResult.model_json_schema()}"},
        ],
        response_format={"type": "json_object"},
    )
    response = remove_json_indentation(response)

    code = json.loads(response)
    print(f"For {diagram_type} diagram, code: {code['code']}")
    return createMermaidDiagram(code["code"], diagram_type)

def remove_json_indentation(json_string):
  """
  Removes indentation and extra spaces from a JSON string.

  Args:
      json_string: The string containing the potentially indented JSON data.

  Returns:
      A string with indentation and extra spaces removed, suitable for JSON parsing.
  """
  lines = json_string.splitlines()  # Split into lines
  filtered_lines = [line.strip() for line in lines]  # Remove leading/trailing whitespace
  filtered_json = ''.join(filtered_lines)  # Join lines back into a single string
  return filtered_json
    
