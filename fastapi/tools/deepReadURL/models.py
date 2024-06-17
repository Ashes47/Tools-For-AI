from typing import List
from pydantic import BaseModel


class DeepResponse(BaseModel):
    urls: List[str]
    info: List[str]

    class Config:
        json_schema_extra = {"example": {}}
