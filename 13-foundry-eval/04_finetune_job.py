import time
from openai import AzureOpenAI
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_KEY"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version="2025-04-01-preview",
)

with open("finetune_data.jsonl", "rb") as f:
    training_file = client.files.create(file=f, purpose="fine-tune")
print(f"Uploaded file: {training_file.id}, status: {training_file.status}")

while client.files.retrieve(training_file.id).status != "processed":
    print("waiting for file processing...")
    time.sleep(5)

job = client.fine_tuning.jobs.create(
    training_file=training_file.id,
    model="gpt-4.1-mini-2025-04-14",
    extra_body={"trainingType": "GlobalStandard"},
)
print(f"Job created: {job.id}, status: {job.status}")