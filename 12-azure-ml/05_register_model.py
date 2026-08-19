import os

from dotenv import find_dotenv, load_dotenv

from azure.ai.ml import MLClient
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml.entities import Model
from azure.identity import AzureCliCredential

load_dotenv(find_dotenv())

ml_client = MLClient(
    credential=AzureCliCredential(),
    subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"],
    resource_group_name=os.environ["AML_RESOURCE_GROUP"],
    workspace_name=os.environ["AML_WORKSPACE_NAME"],
)

job_name = "good_king_sjr7ygvcgm"

model = Model(
    path=f"azureml://jobs/{job_name}/outputs/model_output",
    name="diabetes-linreg",
    description="Linear regression on sklearn diabetes toy dataset (Step 14 sanity check)",
    type=AssetTypes.MLFLOW_MODEL, 
)

registered_model = ml_client.models.create_or_update(model)
print(f"Registered: {registered_model.name} v{registered_model.version}")
print(f"Path: {registered_model.path}")