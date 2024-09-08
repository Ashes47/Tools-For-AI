import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


def make_request():
    url = "https://mewow.dev/api/v1/tool/getTranscript"
    headers = {"Authorization": "Basic plswork", "Content-Type": "application/json"}
    data = {"urls": ["https://www.youtube.com/watch?v=1bm8FTM12kw"], "language": "en"}
    response = requests.post(url, headers=headers, json=data)
    return response.text


def main():
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(2)]
        for future in as_completed(futures):
            results.append(future.result())
    return results


if __name__ == "__main__":
    responses = main()
    # Optionally print or process the responses here
    print(responses)  # Print the first five responses for review
