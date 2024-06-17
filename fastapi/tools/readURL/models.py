from pydantic import BaseModel


class ContentURL(BaseModel):
    response: str

    class Config:
        json_schema_extra = {
            "example": {"response": "Adolf Hilter wiki page in Markdown format"}
        }
