import os

from dotenv import find_dotenv, load_dotenv

from azure.ai.ml import MLClient
from azure.ai.ml.entities import ManagedOnlineDeployment, Model
from azure.identity import AzureCliCredential

load_dotenv(find_dotenv())

ml_client = MLClient(
    credential=AzureCliCredential(),
    subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"],
    resource_group_name=os.environ["AML_RESOURCE_GROUP"],
    workspace_name=os.environ["AML_WORKSPACE_NAME"],
)

with open("endpoint_name.txt") as f:
    endpoint_name = f.read().strip()

# latest registered version of diabetes-linreg
model = ml_client.models.get(name="diabetes-linreg", label="latest")

deployment = ManagedOnlineDeployment(
    name="blue",
    endpoint_name=endpoint_name,
    model=model,
    instance_type="Standard_DS2_v2",  
    instance_count=1,
)

ml_client.online_deployments.begin_create_or_update(deployment).result()

# no traffic flows until you explicitly allocate it
endpoint = ml_client.online_endpoints.get(endpoint_name)
endpoint.traffic = {"blue": 100}
ml_client.online_endpoints.begin_create_or_update(endpoint).result()

print(f"Deployment 'blue' live on {endpoint_name}, traffic set to 100%")