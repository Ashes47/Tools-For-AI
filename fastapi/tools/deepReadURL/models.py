from typing import List
from pydantic import BaseModel


class INFO(BaseModel):
    title: str
    body: str
    links: List[str]
    images: List[str]


class DeepResponse(BaseModel):
    urls: List[str]
    info: List[INFO]
