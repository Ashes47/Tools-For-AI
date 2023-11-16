from pydantic import BaseModel
from typing import List

class Transcription(BaseModel):
  url: str

  class Config:
    json_schema_extra = {
        "example": {
            "url":
            "https://www.youtube.com/watch?v=Uk5f3ajkfSs&ab_channel=LiamOttley"
        }
    }


class Mermaid(BaseModel):
  mermaidText: str

  class Config:
    json_schema_extra = {
        "example": {
            "mermaidText":
            "graph TD\n    GPT_Opportunities[\"GPT Opportunities\"]\n\n    GPT_Store_Building[\"Building GPTs for GPT Store\"]\n    GPT_Opportunities --> GPT_Store_Building\n\n    Focus_Unique_GPTs[\"Focus on unique GPTs\"]\n    GPT_Store_Building --> Focus_Unique_GPTs\n    Focus_Unique_GPTs --> Use_Private_Data_Sets[\"Use private data sets\"]\n    Focus_Unique_GPTs --> Integrate_Unique_APIs[\"Integrate unique APIs\"]\n\n    GPT_Store_Building --> Be_Aware_of_Competition[\"Be aware of competition\"]\n    GPT_Store_Building --> Potential_OpenAI_Integration[\"Potential OpenAI integration\"]\n\n    Custom_GPTs_Businesses[\"Custom GPTs for Businesses\"]\n    GPT_Opportunities --> Custom_GPTs_Businesses\n\n    Start_AI_Agency[\"Start an AI agency\"]\n    Custom_GPTs_Businesses --> Start_AI_Agency\n    Start_AI_Agency --> Specialize_GPT_Solutions[\"Specialize in GPT solutions\"]\n    Start_AI_Agency --> Plan_Create_Sell_Tailored_GPTs[\"Plan, create, sell tailored GPTs\"]\n\n    Custom_GPTs_Businesses --> Consistent_Revenue_Stream[\"Consistent revenue stream\"]\n    Custom_GPTs_Businesses --> Adapt_To_OpenAI_Updates[\"Adapt to OpenAI updates\"]\n\n    GPT_Strategy_Development_Freelancer[\"Specializing in GPT Strategy and Development as a Freelancer\"]\n    GPT_Opportunities --> GPT_Strategy_Development_Freelancer\n\n    Growing_Demand_Freelancers[\"Growing demand for skilled freelancers\"]\n    GPT_Strategy_Development_Freelancer --> Growing_Demand_Freelancers\n    Growing_Demand_Freelancers --> Learn_Python_JavaScript[\"Learn Python and JavaScript\"]\n    Growing_Demand_Freelancers --> Build_GPTs_Using_Assistant_API[\"Build GPTs using assistant API\"]\n    Growing_Demand_Freelancers --> Join_Communities_For_Clients[\"Join communities for clients\"]\n    Growing_Demand_Freelancers --> Build_Personal_Brand[\"Build a personal brand\"]\n\n    Hands_On_Experience[\"Importance of Hands-on Experience\"]\n    GPT_Opportunities --> Hands_On_Experience\n\n    Hands_On_Experience --> Build_GPTs[\"Build GPTs\"]\n    Hands_On_Experience --> Understand_Assistant_API[\"Understand assistant API\"]\n    Hands_On_Experience --> Stay_Updated_With_AI_Tech[\"Stay updated with AI and GPT tech\"]\n    Hands_On_Experience --> Leverage_Private_Data_Unique_Applications[\"Leverage private data and unique applications\"]\n\n"
        }
    }


class PlantUML(BaseModel):
  plantumlText: str

  class Config:
    json_schema_extra = {
        "example": {
            "plantumlText":
            "@startmindmap\n* GPT Opportunities\n** Building GPTs for GPT Store\n*** Focus on unique GPTs\n**** Use private data sets\n**** Integrate unique APIs\n*** Be aware of competition\n*** Potential OpenAI integration\n** Custom GPTs for Businesses\n*** Start an AI agency\n**** Specialize in GPT solutions\n**** Plan, create, sell tailored GPTs\n*** Consistent revenue stream\n*** Adapt to OpenAI updates\n** Specializing in GPT Strategy and Development as a Freelancer\n*** Growing demand for skilled freelancers\n**** Learn Python and JavaScript\n**** Build GPTs using assistant API\n**** Join communities for clients\n**** Build a personal brand\n*** Importance of Hands-on Experience\n**** Build GPTs\n**** Understand assistant API\n**** Stay updated with AI and GPT tech\n**** Leverage private data and unique applications\n@endmindmap"
        }
    }


class Transcriptslot(BaseModel):
  text: str
  start: float
  duration: float

  class Config:
    json_schema_extra = {
        "example": {
            "text": "hey",
            "start": 0.00,
            "duration": 3.00
        }
    }

class TranscriptionResponse(BaseModel):
  transcript: List[Transcriptslot]

  class Config:
    json_schema_extra = {
        "example": {
          "transcript" : [{
            "text": "hey",
            "start": 0.00,
            "duration": 3.00
        }]
      }
    }


class ImageURL(BaseModel):
  imageURL: str

  class Config:
    json_schema_extra = {
        "example": {
            "imageURL": "https://example.com/image.png"
        }
    }
