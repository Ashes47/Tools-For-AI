import os
import requests
import uuid
from constants import GRAPHVIZ_IMAGE_DIR, IMAGE_DIR
from tools.graphviz.models import GraphvizRequest
from tools.models import CommandResponse
from tools.urlBuilder import urlFor, staticURL


async def createGraphViz(data: GraphvizRequest) -> CommandResponse:
    try:
        response = requests.post(
            "https://quickchart.io/graphviz",
            json={"graph": data.graph, "layout": data.layout.value, "format": "png"},
        )

        if response.status_code == 200:
            print("Saving Image")

            id = str(uuid.uuid4())
            path = os.getcwd() + f"/{IMAGE_DIR}/{GRAPHVIZ_IMAGE_DIR}"

            if not os.path.exists(path):
                os.makedirs(path)

            with open(f"{path}/{id}.png", "wb") as f:
                f.write(response.content)

            return CommandResponse(
                output="Image Generated",
                imageURL=urlFor(f"{GRAPHVIZ_IMAGE_DIR}/{id}.png"),
            )

    except:
        return CommandResponse(
            output=f"Error generating wordcloud",
            imageURL=staticURL("invalid.png"),
        )
