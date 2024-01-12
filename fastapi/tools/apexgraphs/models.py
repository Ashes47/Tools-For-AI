from enum import Enum
from pydantic import BaseModel


# Define the enumeration for chart types
class ChartType(Enum):
    LINE = "line"
    AREA = "area"
    BAR = "bar"
    PIE = "pie"
    DONUT = "donut"
    RADIALBAR = "radialBar"
    SCATTER = "scatter"
    BUBBLE = "bubble"
    HEATMAP = "heatmap"
    CANDLESTICK = "candlestick"
    BOXPLOT = "boxPlot"
    RADAR = "radar"
    POLARAREA = "polarArea"
    RANGEBAR = "rangeBar"
    RANGEAREA = "rangeArea"
    TREEMAP = "treemap"
    OTHER = "other"


class ApexChartRequest(BaseModel):
    config: str
    width: int = 600
    height: int = 300
    chartType: ChartType

    class Config:
        json_schema_extra = {
            "example": {
                "config": "{'chart': {'type': 'area'}, 'series': [{'name': 'Minimum Temperature', 'data': [20, 22, 23, 22, 21, 24, 26, 28, 25]}, {'name': 'Maximum Temperature', 'data': [25, 28, 29, 30, 31, 32, 33, 34, 35]}], 'xaxis': {'categories': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']}, 'fill': {'type': 'gradient', 'gradient': {'shadeIntensity': 1, 'opacityFrom': 0.7, 'opacityTo': 0.9, 'stops': [0, 100]}}}",
                "width": 600,
                "height": 300,
                "chartType": "Line_Chart",
            }
        }
