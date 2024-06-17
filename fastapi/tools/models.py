from pydantic import BaseModel


class CommandResponse(BaseModel):
    output: str
    imageURL: str

    class Config:
        json_schema_extra = {
            "example": {
                "imageURL": "https://example.com/image.png",
                "output": "Image Generated",
            }
        }

class BrowsingRequest(BaseModel):
    url: str

    class Config:
        json_schema_extra = {
            "example": {"url": "https://en.wikipedia.org/wiki/Adolf_Hitler"}
        }