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


class ReadURL(BaseModel):
    url: str
    limit: int = 10
    summarize: bool = False
    use_openAI: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://en.wikipedia.org/wiki/Adolf_Hitler",
                "limit": 10,
            }
        }
