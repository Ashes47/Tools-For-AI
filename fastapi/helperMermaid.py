from PIL import Image
import base64
import io
import requests
import uuid


def createMermaid(mermaidGraph):

  graphbytes = mermaidGraph.encode("ascii")

  base64_bytes = base64.b64encode(graphbytes)
  base64_string = base64_bytes.decode("ascii")

  rawImage = requests.get('https://mermaid.ink/img/' + base64_string).content
  imageFile = Image.open(io.BytesIO(rawImage))

  print("Saving Image")
  id = str(uuid.uuid4())
  imageFile.save(f"./static/{id}.png")
  return id + '.png'
