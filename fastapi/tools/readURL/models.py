from pydantic import BaseModel


class BrowsingResult(BaseModel):
    response: str

    class Config:
        json_schema_extra = {
            "example": {"response": "Adolf Hilter wiki page in Markdown format"}
        }
