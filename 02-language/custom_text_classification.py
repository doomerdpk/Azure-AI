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

# response = requests.post(url, headers=headers, json=body)
# print("Status code:", response.status_code)
# print("Operation-Location header:", response.headers.get("operation-location"))
# print(response.text)

# import_job_url = response.headers.get("operation-location")

# while True:
#     status_response = requests.get(import_job_url, headers=headers)
#     status_data = status_response.json()
#     print("Status:", status_data["status"])
#     if status_data["status"] in ("succeeded", "failed", "partiallyCompleted"):
#         break
#     time.sleep(5)

# print(status_data)

# train_url = f"{endpoint}/language/authoring/analyze-text/projects/{project_name}/:train?api-version={api_version}"

# train_body = {
#     "modelLabel": "movie-genre-model",
#     "trainingConfigVersion": api_version,
#     "evaluationOptions": {
#         "kind": "percentage",
#         "trainingSplitPercentage": 80,
#         "testingSplitPercentage": 20
#     }
# }

# train_response = requests.post(train_url, headers=headers, json=train_body)
# print("Status code:", train_response.status_code)
# train_job_url = train_response.headers.get("operation-location")
# print("Training job URL:", train_job_url)

# while True:
#     status_response = requests.get(train_job_url, headers=headers)
#     status_data = status_response.json()
#     print("Status:", status_data["status"])
#     if status_data["status"] in ("succeeded", "failed", "partiallyCompleted"):
#         break
#     time.sleep(15)

# print(status_data)


# model_eval_url = f"{endpoint}/language/authoring/analyze-text/projects/{project_name}/models/movie-genre-model/evaluation/summary-result?api-version={api_version}"

# eval_response = requests.get(model_eval_url, headers=headers)
# print(json.dumps(eval_response.json(), indent=2))


deploy_name = "staging"
deploy_url = f"{endpoint}/language/authoring/analyze-text/projects/{project_name}/deployments/{deploy_name}?api-version={api_version}"

deploy_body = {"trainedModelLabel": "movie-genre-model"}

deploy_response = requests.put(deploy_url, headers=headers, json=deploy_body)
print("Status code:", deploy_response.status_code)
deploy_job_url = deploy_response.headers.get("operation-location")
print("Deploy job URL:", deploy_job_url)

while True:
    status_response = requests.get(deploy_job_url, headers=headers)
    status_data = status_response.json()
    print("Status:", status_data["status"])
    if status_data["status"] in ("succeeded", "failed"):
        break
    time.sleep(10)

print(status_data)