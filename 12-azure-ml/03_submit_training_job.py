import os

from dotenv import find_dotenv, load_dotenv

from azure.ai.ml import MLClient, Input, Output, command
from azure.identity import AzureCliCredential

load_dotenv(find_dotenv())

ml_client = MLClient(
    credential=AzureCliCredential(),
    subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"],
    resource_group_name=os.environ["AML_RESOURCE_GROUP"],
    workspace_name=os.environ["AML_WORKSPACE_NAME"],
)

job = command(
    code="./src",
    command="python train.py --data ${{inputs.data}} --model_output ${{outputs.model_output}}",
    inputs={"data": Input(type="uri_file", path="azureml:diabetes-toy:1")},
    outputs={"model_output": Output(type="uri_folder")},
    environment="aml-learning-env@latest",
    display_name="diabetes-linreg-train",
    experiment_name="12-azure-ml-fundamentals",
    # no compute= param -> runs on serverless compute
)

returned_job = ml_client.jobs.create_or_update(job)
print(f"Submitted job: {returned_job.name}")
print(f"Status: {returned_job.status}")
print(f"Studio URL: {returned_job.studio_url}")