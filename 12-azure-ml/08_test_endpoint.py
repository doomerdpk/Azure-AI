import json
import os

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

with open("endpoint_name.txt") as f:
    endpoint_name = f.read().strip()

# scikit-learn diabetes dataset has 10 features, pre-standardized
sample = {"input_data": [[0.038, 0.05, 0.061, 0.021, -0.044, -0.035, -0.043, -0.003, 0.02, -0.017]]}

request_file = "sample_request.json"
with open(request_file, "w") as f:
    json.dump(sample, f)

result = ml_client.online_endpoints.invoke(
    endpoint_name=endpoint_name,
    deployment_name="blue",
    request_file=request_file,
)
print(f"Prediction: {result}")