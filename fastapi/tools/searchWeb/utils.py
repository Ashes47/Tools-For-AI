import g4f
from retry import retry
from constants import MAX_CONTEXT_WINDOW

@retry(tries=3, delay=2, backoff=2)
def summarize(query, text):
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_35_turbo_16k_0613,
        messages=[
            {
                "role": "user",
                "content": f"You are a helpful assistant that summarizes the following text. The summary should be concise and accurate. Do not include any information that is not relevant to the text. If the text is not relevant to the query, return an empty string. The query is: {query}. The text is: {text}"
            }
        ]
    )

    return response

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

def process_search_results(query, parsed_content):
    text_chunks = split_text_into_chunks(parsed_content)
    summarized_content = ""
    for chunk in text_chunks:
        summary = summarize(query, chunk)
        summarized_content += summary + " "
    return summarized_content.strip()