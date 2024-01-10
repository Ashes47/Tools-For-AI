from pydantic import BaseModel


class ImageURL(BaseModel):
    imageURL: str

    class Config:
        json_schema_extra = {"example": {"imageURL": "https://example.com/image.png"}}
