from azure.ai.ml import MLClient
from azure.identity import AzureCliCredential

ml_client = MLClient(
    credential=AzureCliCredential(),
    subscription_id="7939cc19-6638-45a9-b3ad-a87050a55491",
    resource_group_name="rg-ai-learning",
    workspace_name="aml-learning-01",
)

ws = ml_client.workspaces.get("aml-learning-01")
print(f"Connected: {ws.name} | location: {ws.location} | id: {ws.id}")