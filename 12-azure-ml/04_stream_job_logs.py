import os
import sys

from dotenv import find_dotenv, load_dotenv

from azure.ai.ml import MLClient
from azure.identity import AzureCliCredential

load_dotenv(find_dotenv())

ml_client = MLClient(
    credential=AzureCliCredential(),
    subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"],
    resource_group_name=os.environ["AML_RESOURCE_GROUP"],
    workspace_name=os.environ["AML_WORKSPACE_NAME"],
)

job_name = sys.argv[1]
ml_client.jobs.stream(job_name)

final = ml_client.jobs.get(job_name)
print(f"\nFinal status: {final.status}")