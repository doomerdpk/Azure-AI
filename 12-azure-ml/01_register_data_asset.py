import os
from pathlib import Path

import pandas as pd
from dotenv import find_dotenv, load_dotenv
from sklearn.datasets import load_diabetes

from azure.ai.ml import MLClient
from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes
from azure.identity import AzureCliCredential

load_dotenv(find_dotenv())

ml_client = MLClient(
    credential=AzureCliCredential(),
    subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"],
    resource_group_name=os.environ["AML_RESOURCE_GROUP"],
    workspace_name=os.environ["AML_WORKSPACE_NAME"],
)

# Materialize the toy dataset to a local CSV
data = load_diabetes(as_frame=True)
df = data.frame  # features + target column "target"
local_path = Path(__file__).parent / "data" / "diabetes.csv"
local_path.parent.mkdir(exist_ok=True)
df.to_csv(local_path, index=False)
print(f"Wrote {len(df)} rows to {local_path}")

# Register as a versioned Data asset in the workspace
data_asset = Data(
    name="diabetes-toy",
    version="1",
    path=str(local_path),
    type=AssetTypes.URI_FILE,
    description="sklearn diabetes toy dataset, for AML mechanics sanity check",
)

registered = ml_client.data.create_or_update(data_asset)
print(f"Registered: {registered.name} v{registered.version} | path: {registered.path}")