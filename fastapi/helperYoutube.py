from youtube_transcript_api import YouTubeTranscriptApi
import urllib.parse as urlparse
import os
from models import TranscriptionResponse, Transcriptslot
from typing import List

def getVideoId(URL):
  """
  Examples:
  - http://youtu.be/SA2iWivDJiE
  - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
  - http://www.youtube.com/embed/SA2iWivDJiE
  - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
  """
  query = urlparse.urlparse(URL)
  if query.hostname == 'youtu.be':
    return query.path[1:]
  if query.hostname in ('www.youtube.com', 'youtube.com'):
    if query.path == '/watch':
      p = urlparse.parse_qs(query.query)
      return p['v'][0]
    if query.path[:7] == '/embed/':
      return query.path.split('/')[2]
    if query.path[:3] == '/v/':
      return query.path.split('/')[2]
  # fail?
  return None


def makeSlots(transcription) -> List[Transcriptslot]:
  result: List[Transcriptslot] = []

  text = ""
  dur = 0
  start = 0
  for obj in transcription:
    text += " " + obj['text']
    dur += obj['duration']
    start = min(start, obj['start'])

    if dur > 30:
      result.append(Transcriptslot(text=text, start=start, duration=dur))
      text = ""
      start = start + dur
      dur = 0

  result.append(Transcriptslot(text=text, start=start, duration=dur))
  return result


def getTranscription(URL) -> List[Transcriptslot]:
  videoId = getVideoId(URL)
  transcription = YouTubeTranscriptApi.get_transcript(videoId)

  return makeSlots(transcription)


def validateToken(token):
  if token == os.environ['token']:
    return True

  return False
