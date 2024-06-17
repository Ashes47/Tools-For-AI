from youtube_transcript_api import YouTubeTranscriptApi
import urllib.parse as urlparse
from tools.youtube.models import (
    Transcription,
    TranscriptionResponse,
    TranscriptionObject,
)
from typing import List


def getVideoId(URL):
    """
    Extract the YouTube video ID from various URL formats, including YouTube Shorts.

    Examples:
    - https://www.youtube.com/shorts/Fwy4_Q4lTZE
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse.urlparse(URL)
    if query.hostname == "youtu.be":
        return query.path[1:]
    if query.hostname in ("www.youtube.com", "youtube.com"):
        if query.path.startswith("/shorts/"):
            return query.path.split("/")[2]
        if query.path == "/watch":
            p = urlparse.parse_qs(query.query)
            return p["v"][0]
        if query.path.startswith("/embed/"):
            return query.path.split("/")[2]
        if query.path.startswith("/v/"):
            return query.path.split("/")[2]
    return None


def makeSlots(transcription) -> TranscriptionResponse:
    result: List[TranscriptionObject] = []

    text = ""
    dur = 0
    start = 0
    for obj in transcription:
        text += " " + obj["text"]
        dur += obj["duration"]
        start = min(start, obj["start"])

        if dur > 30:
            result.append(TranscriptionObject(text=text, start=start, duration=dur))
            text = ""
            start = start + dur
            dur = 0

    result.append(TranscriptionObject(text=text, start=start, duration=dur))
    return result


def getTranscription(transcription: Transcription) -> TranscriptionResponse:
    videoId = getVideoId(transcription.url)
    transcription = YouTubeTranscriptApi.get_transcript(
        video_id=videoId, languages=[transcription.language.value]
    )
    return makeSlots(transcription)
