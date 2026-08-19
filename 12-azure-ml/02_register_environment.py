import os

from dotenv import find_dotenv, load_dotenv

from azure.ai.ml import MLClient
from azure.ai.ml.entities import Environment
from azure.identity import AzureCliCredential

load_dotenv(find_dotenv())

ml_client = MLClient(
    credential=AzureCliCredential(),
    subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"],
    resource_group_name=os.environ["AML_RESOURCE_GROUP"],
    workspace_name=os.environ["AML_WORKSPACE_NAME"],
)

env = Environment(
    name="aml-learning-env",
    description="sklearn + mlflow env for AML fundamentals learning (Step 14)",
    conda_file="environment/conda.yml",
    image="mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu22.04",
)

registered_env = ml_client.environments.create_or_update(env)
print(f"Registered: {registered_env.name} v{registered_env.version}")