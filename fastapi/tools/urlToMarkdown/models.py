from pydantic import BaseModel


# Define the BrowsingRequest model
class BrowsingRequest(BaseModel):
    url: str

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://en.wikipedia.org/wiki/Adolf_Hitler"
                }
        }


class BrowsingResult(BaseModel):
    response: str

    class Config:
        json_schema_extra = {
            "example": {
                "response": ""
                }
        }