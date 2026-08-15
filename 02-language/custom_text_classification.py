import os, json, requests, time
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

endpoint = os.environ["LANG_ENDPOINT"].rstrip("/")
key = os.environ["LANG_KEY"]
project_name = "movie-classifier"
api_version = "2022-05-01"

# Load the sample labels file
with open("custom-text-classification-data/Custom multi classification - movies summary/movieLabels.json") as f:
    body = json.load(f)

# Fix the container name to match yours
body["metadata"]["storageInputContainerName"] = "text-classification-data"
body["metadata"]["projectName"] = project_name
body["metadata"]["language"] = "en-us"

url = f"{endpoint}/language/authoring/analyze-text/projects/{project_name}/:import?api-version={api_version}"
headers = {
    "Ocp-Apim-Subscription-Key": key,
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, json=body)
print("Status code:", response.status_code)
print("Operation-Location header:", response.headers.get("operation-location"))
print(response.text)

import_job_url = response.headers.get("operation-location")

while True:
    status_response = requests.get(import_job_url, headers=headers)
    status_data = status_response.json()
    print("Status:", status_data["status"])
    if status_data["status"] in ("succeeded", "failed", "partiallyCompleted"):
        break
    time.sleep(5)

print(status_data)