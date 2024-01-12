import os
import requests
import uuid
from constants import APEXCHARTS_IMAGE_DIR, IMAGE_DIR
from tools.apexgraphs.models import ApexChartRequest
from tools.models import CommandResponse
from tools.urlBuilder import urlFor, staticURL

async def createApexCharts(data: ApexChartRequest) -> CommandResponse:
    try:
        response = requests.get(
            "https://quickchart.io/apex-charts/render", params=data.dict()
        )
        if response.status_code == 200:
            print("Saving Image")

            id = str(uuid.uuid4())
            path = os.getcwd() + f"/{IMAGE_DIR}/{APEXCHARTS_IMAGE_DIR}/{data.chartType}"

            if not os.path.exists(path):
                os.makedirs(path)

            with open(f"{path}/{id}.png", "wb") as f:
                f.write(response.content)

            return CommandResponse(
                output="Image Generated",
                imageURL=urlFor(f"{APEXCHARTS_IMAGE_DIR}/{data.chartType}/{id}.png"),
            )
    except:
        return CommandResponse(
            output=f"Error generating wordcloud",
            imageURL=staticURL("invalid.png"),
        )