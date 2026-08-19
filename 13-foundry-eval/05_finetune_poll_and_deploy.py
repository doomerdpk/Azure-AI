import time
from openai import AzureOpenAI
from dotenv import load_dotenv, find_dotenv
import os, sys

load_dotenv(find_dotenv())
client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_KEY"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version="2024-10-21",
)

job_id = sys.argv[1]  # pass the job id printed by 04_finetune_job.py

while True:
    job = client.fine_tuning.jobs.retrieve(job_id)
    print(f"status: {job.status}")
    if job.status in ("succeeded", "failed", "cancelled"):
        break
    time.sleep(30)

if job.status == "succeeded":
    print(f"\nFine-tuned model: {job.fine_tuned_model}")
    print("Deploy it with:")
    print(f"""
az cognitiveservices account deployment create \\
  --name aoai-learning-01 \\
  --resource-group rg-ai-learning \\
  --deployment-name gpt-4.1-mini-ft-sanity \\
  --model-name {job.fine_tuned_model} \\
  --model-version 1 \\
  --model-format OpenAI \\
  --sku-name Standard \\
  --sku-capacity 10
""")
else:
    print(job.error)