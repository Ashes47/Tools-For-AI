import g4f
from retry import retry
from constants import MAX_CONTEXT_WINDOW
import os
from openai import OpenAI


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


@retry(tries=3, delay=2, backoff=2)
def summurize(query, text):

    if query:
        content = f"You are a helpful assistant that summarizes the following text in English. The summary should be concise and accurate. Do not include any information that is not relevant to the text. If the text is not relevant to the query, return an empty string. The query is: {query}. The text is: {text}"
    else:
        content = f"You are a helpful assistant. Write a concise summary of the following text in English: {text}"
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_35_turbo_16k_0613,
        messages=[{"role": "user", "content": content}],
        temperature=0.7,
    )

    return response


def summarizeOpenAI(query, text):
    if query:
        content = f"You are a helpful assistant that summarizes the following text in English. The summary should be concise and accurate. Do not include any information that is not relevant to the text. If the text is not relevant to the query, return an empty string. The query is: {query}. The text is: {text}"
    else:
        content = f"You are a helpful assistant. Write a concise summary of the following text in English: {text}"
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": content}],
        model="gpt-3.5-turbo",
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


def process_search_results(query, parsed_content, useOpenAI=False):
    text_chunks = split_text_into_chunks(parsed_content)
    summarized_content = ""
    for chunk in text_chunks:
        if useOpenAI:
            summary = summarizeOpenAI(query, chunk)
        else:
            summary = summurize(query, chunk)
        summarized_content += summary + " "
    return summarized_content.strip()
