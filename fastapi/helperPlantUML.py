import io
from PIL import Image
from plantuml import PlantUML
import uuid


def createPlantUML(plantumlText):

  # create a server object to call for your computations
  print("Calling PlantUML Server")
  server = PlantUML(url='https://www.plantuml.com/plantuml/img/',
                    basic_auth={},
                    form_auth={},
                    http_opts={},
                    request_opts={})

  # Send and compile your diagram files to/with the PlantUML server
  rawImage = server.processes(plantumlText)
  imageStream = io.BytesIO(rawImage)
  imageFile = Image.open(imageStream)

  print("Saving Image")
  id = str(uuid.uuid4())
  imageFile.save(f"./static/{id}.png")
  return id + '.png'
