from pydantic import BaseModel, constr
from typing import List, Optional
from enum import Enum

class ScaleType(str, Enum):
    linear = 'linear'
    sqrt = 'sqrt'
    log = 'log'

class Case(str, Enum):
    upper = 'upper'
    lower = 'lower'
    none = 'none'

class LanguageCode(str, Enum):
    English = "en"
    Afrikaans = "af"
    Arabic = "ar"
    Armenian = "hy"
    Basque = "eu"
    Bengali = "be"
    Breton = "br"
    Bulgarian = "bu"
    Catalan = "ca"
    Chinese = "zh"
    Croatian = "hr"
    Czech = "ce"
    Danish = "da"
    Dutch = "nl"
    Esperanto = "ep"
    Estonian = "es"
    Finnish = "fi"
    French = "fr"
    Galician = "gl"
    German = "de"
    Greek = "el"
    Gujarati = "gu"
    Hausa = "ha"
    Hebrew = "he"
    Hindi = "hi"
    Hungarian = "hu"
    Indonesian = "in"
    Irish = "ir"
    Italian = "it"
    Japanese = "ja"
    Korean = "ko"
    Kurdish = "ku"
    Latin = "la"
    Latvian = "lv"
    Lithuanian = "li"
    Lugbara = "lg"
    Malay = "ms"
    Marathi = "ma"
    Burmese = "my"
    Norwegian = "no"
    Persian = "fa"
    Polish = "po"
    Portuguese = "pt"
    Punjabi = "pa"
    Romanian = "ro"
    Russian = "ru"
    Slovak = "sk"
    Slovenian = "sl"
    Somali = "so"
    Sotho = "st"
    Spanish = "sp"
    Swahili = "sw"
    Swedish = "sv"
    Tagalog = "ta"
    Thai = "th"
    Turkish = "tu"
    Ukrainian = "uk"
    Urdu = "ur"
    Vietnamese = "vi"
    Yoruba = "yo"
    Zulu = "zu"

class WordCloud(BaseModel):
    text: str
    format: str = 'png'
    width: int = 1000
    height: int = 1000
    backgroundColor: str = 'transparent'
    fontFamily: str = 'serif'
    fontWeight: str = 'normal'
    fontScale: int = 15
    scale: ScaleType = ScaleType.linear
    padding: int = 1
    rotation: int = 20
    maxNumWords: int = 200
    minWordLength: int = 4
    case: Case = Case.none
    colors: Optional[List[str]] = None
    removeStopwords: bool = True
    cleanWords: bool = True
    language: LanguageCode = LanguageCode.English
    useWordList: bool = False

class WordCloudRequest(BaseModel):
    text: str
    width: Optional[int]
    height: Optional[int]
    backgroundColor: Optional[str]
    fontFamily: Optional[str]
    fontWeight: Optional[str]
    fontScale:  Optional[int]
    padding: Optional[int]
    rotation: Optional[int]
    maxNumWords: Optional[int]
    minWordLength: Optional[int]
    scale: Optional[ScaleType]
    case: Optional[Case]
    colors: Optional[List[str]]
    removeStopwords: Optional[bool]
    cleanWords: Optional[bool]
    language: Optional[LanguageCode]

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Example word cloud text",
                "width": 800,
                "height": 600,
                "backgroundColor": "#ffffff",
                "fontFamily": "Arial",
                "fontWeight": "bold",
                "fontScale": 10,
                "padding": 2,
                "rotation": 45,
                "maxNumWords": 150,
                "minWordLength": 3,
                "scale": ScaleType.linear,
                "case": Case.upper,
                "colors": ["#FF5733", "#33FF57", "#3357FF"],
                "removeStopwords": False,
                "cleanWords": True,
                "language": LanguageCode.English
            }
        }


def create_word_cloud(request: WordCloudRequest) -> WordCloud:
    # Create a WordCloud object using the data from WordCloudRequest
    return WordCloud(
        text=request.text,
        format='png',
        width=request.width or WordCloud.width,
        height=request.height or WordCloud.height,
        backgroundColor=request.backgroundColor or WordCloud.backgroundColor,
        fontFamily=request.fontFamily or WordCloud.fontFamily,
        fontWeight=request.fontWeight or WordCloud.fontWeight,
        fontScale=request.fontScale or WordCloud.fontScale,
        scale=request.scale or WordCloud.scale,
        padding=request.padding or WordCloud.padding,
        rotation=request.rotation or WordCloud.rotation,
        maxNumWords=request.maxNumWords or WordCloud.maxNumWords,
        minWordLength=request.minWordLength or WordCloud.minWordLength,
        case=request.case or WordCloud.case,
        colors=request.colors,
        removeStopwords=request.removeStopwords if request.removeStopwords is not None else WordCloud.removeStopwords,
        cleanWords=request.cleanWords if request.cleanWords is not None else WordCloud.cleanWords,
        language=request.language or WordCloud.language,
        useWordList=False
    )