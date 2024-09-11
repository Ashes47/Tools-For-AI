from pydantic import BaseModel, Field
from typing import Optional, Union, List


class SearchResultImage(BaseModel):
    url: str
    description: Optional[str] = None


class SearchResultItem(BaseModel):
    title: str
    url: str
    content: str


class SearchResultVideo(BaseModel):
    url: str
    title: str
    duration: Optional[str] = None


class SearXNGResult(BaseModel):
    title: str
    url: str
    content: str
    img_src: Optional[str] = None
    publishedDate: Optional[str] = None
    score: Optional[int] = None


class SearXNGSearchResults(BaseModel):
    images: Optional[List[SearchResultImage]] = None
    videos: Optional[List[SearchResultVideo]] = None
    results: List[SearchResultItem]
    advanced_result: Optional[str] = None
    number_of_results: int
    query: str
