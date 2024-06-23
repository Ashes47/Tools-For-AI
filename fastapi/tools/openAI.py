from retry import retry
from constants import MAX_CONTEXT_WINDOW, SUMMARIZE_MODEL, JSON_MODEL
import os
from openai import OpenAI
import re
from html import unescape
import json
from fastapi import HTTPException

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def summarizeOpenAI(query, text, stringifiedJson):
    if query:
        content = f"You are a helpful assistant that summarizes the following text in English. The summary should be concise and accurate. Do not include any information that is not relevant to the text. If the text is not relevant to the query, return an empty string. The query is: {query}. The text is: {text}."
    else:
        content = f"You are a helpful assistant. Write a concise summary of the following text in English: {text}."

    if stringifiedJson and stringifiedJson != "":
        content = (
            content
            + f" Please try to have all these features {stringifiedJson} in your response."
        )
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": content}],
        model=SUMMARIZE_MODEL,
        temperature=0.7,
        max_tokens=500,
    )
    return response.choices[0].message.content


def split_text_into_chunks(text):
    # Split the text into manageable chunks without breaking sentences
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(" ".join(current_chunk + [word])) <= MAX_CONTEXT_WINDOW:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def clean_text(text, remove_images=True):
    # Strip HTML tags
    try:
        text = re.sub(r"<[^>]+>", "", text)
        # Convert HTML entities to their corresponding characters
        text = unescape(text)
        # Remove image URLs
        if remove_images:
            text = re.sub(
                r"https?://[\w\.-]+/\S+\.(jpg|jpeg|png|gif|bmp)(\?\S*)?", "", text
            )
        # Replace multiple spaces with a single space and trim leading/trailing spaces
    except Exception as e:
        print(f"Error cleaning text: {e}")
        return text
    return re.sub(r"\s+", " ", text).strip()


def process_search_results(query, parsed_content, stringifiedJson=None):
    text_chunks = split_text_into_chunks(clean_text(parsed_content, True))
    summarized_content = ""
    for chunk in text_chunks:
        summary = summarizeOpenAI(query, chunk, stringifiedJson)
        summarized_content += summary + " "
    if stringifiedJson and stringifiedJson != "":
        try:
            return jsonOpenAI(summarized_content, stringifiedJson)
        except Exception as e:
            print(f"Error creating JSON: {e}")
            return HTTPException(status_code=500, detail="Error creating JSON")
    return summarized_content.strip()


@retry(tries=3, delay=2, backoff=2)
def jsonOpenAI(response, stringifiedJson):
    print("Json OpenAI")
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"You are a JSON generator. You must only output valid JSON. User will now share a summarised content. You must generate a JSON Object as per this Example: {stringifiedJson}. Do not answer in Markdown.",
            },
            {"role": "user", "content": response},
        ],
        model=JSON_MODEL,
        temperature=0.7,
        max_tokens=500,
    )
    print("Json Response")
    print(response.choices[0].message.content)
    return str(json.loads(response.choices[0].message.content))
