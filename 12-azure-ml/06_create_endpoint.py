import os
import uuid

from dotenv import find_dotenv, load_dotenv

from azure.ai.ml import MLClient
from azure.ai.ml.entities import ManagedOnlineEndpoint
from azure.identity import AzureCliCredential

load_dotenv(find_dotenv())

ml_client = MLClient(
    credential=AzureCliCredential(),
    subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"],
    resource_group_name=os.environ["AML_RESOURCE_GROUP"],
    workspace_name=os.environ["AML_WORKSPACE_NAME"],
)

endpoint_name = f"diabetes-linreg-{uuid.uuid4().hex[:8]}"

endpoint = ManagedOnlineEndpoint(
    name=endpoint_name,
    description="linear regression on diabetes toy dataset",
    auth_mode="key",
)

result = ml_client.online_endpoints.begin_create_or_update(endpoint).result()
print(f"Endpoint created: {result.name}")
print(f"Scoring URI (not live until a deployment exists): {result.scoring_uri}")

with open("endpoint_name.txt", "w") as f:
    f.write(result.name)