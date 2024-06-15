from pydantic import BaseModel


# Define the BrowsingRequest model
class YoutubeSearchRequest(BaseModel):
    topic: str

    class Config:
        json_schema_extra = {
            "example": {
                "topic": "Quantum Computing"
                }
        }


class YoutubeSearchResult(BaseModel):
    links: list[str]

    class Config:
        json_schema_extra = {
            "example": {
                "links": ['https://www.youtube.com/watch?v=g_IaVepNDT4&pp=ygURUXVhbnR1bSBDb21wdXRpbmc%3D', 'https://www.youtube.com/watch?v=QuR969uMICM&pp=ygURUXVhbnR1bSBDb21wdXRpbmc%3D']
                }
        }