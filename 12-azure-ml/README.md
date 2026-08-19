# Azure ML Fundamentals: Diabetes Regression

This folder is a small, script-based Azure Machine Learning walkthrough. It trains a scikit-learn linear regression model on the built-in diabetes dataset, registers the resulting MLflow model, deploys it to a managed online endpoint, and invokes the endpoint with a sample request.

The example is intentionally compact. Its purpose is to demonstrate Azure ML asset and job mechanics rather than to produce a clinically useful model.

## What This Example Builds

- A versioned `diabetes-toy` URI file data asset containing 442 rows and 10 standardized features plus `target`.
- A reusable Azure ML environment named `aml-learning-env` for training.
- A serverless command job named `diabetes-linreg-train`.
- A registered MLflow model named `diabetes-linreg`.
- A key-authenticated managed online endpoint with a generated name.
- A `blue` managed online deployment with 100% of endpoint traffic.
- A scoring service that accepts JSON and returns linear regression predictions.

## Folder Contents

| Path                         | Purpose                                                                                                                                                |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | --- |
| `00_connectivity_check.py`   | Connects to the configured workspace and prints its location and resource ID. This script uses literal workspace values as a quick connectivity check. |
| `01_register_data_asset.py`  | Creates `data/diabetes.csv` from `sklearn.datasets.load_diabetes` and registers it as `diabetes-toy:1`.                                                |
| `02_register_environment.py` | Registers the training environment from `environment/conda.yml`.                                                                                       |
| `03_submit_training_job.py`  | Submits the training command using serverless compute and the registered data asset.                                                                   |
| `04_stream_job_logs.py`      | Streams a submitted job by job name and prints its final status.                                                                                       |
| `05_register_model.py`       | Registers the training output as the latest version of the `diabetes-linreg` MLflow model.                                                             |
| `06_create_endpoint.py`      | Creates a uniquely named managed online endpoint and writes its name to `endpoint_name.txt`.                                                           |
| `07_create_deployment.py`    | Original deployment attempt using the latest registered model.                                                                                         |     |
| `08_test_endpoint.py`        | Sends a ten-feature sample to the `blue` deployment and prints the prediction.                                                                         |
| `src/train.py`               | Reads the CSV, trains `LinearRegression`, prints RMSE, and saves an MLflow-compatible scikit-learn model.                                              |     |
| `environment/conda.yml`      | Conda specification for the training environment.                                                                                                      |
| `data/diabetes.csv`          | Materialized copy of the scikit-learn diabetes dataset.                                                                                                |
| `endpoint_name.txt`          | Generated endpoint name used by the deployment and test scripts.                                                                                       |

## Prerequisites

1. An Azure subscription with an Azure ML workspace.
2. Azure CLI installed and authenticated:

   ```bash
   az login
   ```

3. Python 3.10 or a compatible Python environment.
4. Azure ML SDK and local packages installed. A typical setup is:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   python -m pip install azure-ai-ml azure-identity python-dotenv pandas scikit-learn mlflow
   ```

5. Environment variables available to `python-dotenv`. The scripts call `find_dotenv()`, so a `.env` file in this repository or a parent directory can provide:

   ```dotenv
   AZURE_SUBSCRIPTION_ID=<subscription-id>
   AML_RESOURCE_GROUP=<resource-group>
   AML_WORKSPACE_NAME=<workspace-name>
   ```

The Azure CLI credential uses the signed-in identity. That identity needs permission to read and create workspace assets, submit jobs, and manage online endpoints and deployments.

## Run the Workflow

Run these commands from this directory, not from the repository root. Several scripts use relative paths such as `environment/conda.yml`, `endpoint_name.txt`, and `./src`.

```bash
cd 12-azure-ml
python 00_connectivity_check.py
python 01_register_data_asset.py
python 02_register_environment.py
python 03_submit_training_job.py
```

The training script prints a job name, status, and Studio URL. Save the job name. The job may initially be `NotStarted` or `Running`.

Stream the job after submission:

```bash
python 04_stream_job_logs.py <job-name>
```

When the job completes successfully, update `job_name` in `05_register_model.py` to the successful job name, then register the model:

```bash
python 05_register_model.py
```

Create the endpoint:

```bash
python 06_create_endpoint.py
```

This writes the generated endpoint name to `endpoint_name.txt`. Deploy the latest model:

```bash
python 07_create_deployment.py
```

The original deployment script is retained as part of the learning sequence. For the working deployment, run the repair script:

```bash
python 08_test_endpoint.py
```

The expected response is a serialized prediction from the linear regression model. The exact value depends on the registered model version.

## Training Flow

`01_register_data_asset.py` regenerates the CSV from `load_diabetes(as_frame=True)`. The dataset has these feature columns:

```text
age, sex, bmi, bp, s1, s2, s3, s4, s5, s6
```

`src/train.py` removes `target`, uses an 80/20 `train_test_split` with `random_state=42`, trains `sklearn.linear_model.LinearRegression`, and prints root mean squared error on the test split. MLflow scikit-learn autologging is enabled, while `mlflow.sklearn.save_model` writes the model to the command output directory.

`03_submit_training_job.py` passes the registered data asset through the `data` input and writes the model to the `model_output` URI-folder output. Because no `compute` argument is supplied, Azure ML selects serverless compute.

## Deployment and Request Contract

The inference environment uses Python 3.10 and includes:

- `mlflow==3.15.1`
- `scikit-learn==1.7.2`
- `pandas==2.3.3`
- `azureml-inference-server-http==1.4.1`
- `azureml-ai-monitoring`

`src/score.py` follows the Azure ML inference server contract:

- `init()` loads the model from the `AZUREML_MODEL_DIR` environment variable.
- `run(raw_data)` accepts either a JSON string or an already parsed object.
- The request must contain `input_data` with rows containing exactly 10 feature values.
- The response is shaped as `{"predictions": [...]}`.

Example request:

```json
{
  "input_data": [
    [0.038, 0.05, 0.061, 0.021, -0.044, -0.035, -0.043, -0.003, 0.02, -0.017]
  ]
}
```

It also registers a dedicated inference environment and assigns all endpoint traffic to the repaired `blue` deployment. The server log may still show a harmless `conda --root` compatibility message; the actionable failure is a missing scoring entry script or a failed worker boot.

## Cleanup

Managed online endpoints incur cost while provisioned. Delete the endpoint when finished using the Azure CLI or Azure ML Studio. Deleting the endpoint also removes its deployments.

```bash
az ml online-endpoint delete \
  --name "$(cat endpoint_name.txt)" \
  --resource-group "$AML_RESOURCE_GROUP" \
  --workspace-name "$AML_WORKSPACE_NAME" \
  --yes
```

Registered data, environments, models, and completed jobs are separate workspace assets and may require separate cleanup according to the retention needs of the workspace.

## Notes for Reproducibility

- Asset and environment versions are created by Azure ML; `diabetes-toy` is explicitly registered as version `1`.
- The endpoint name is generated with an 8-character UUID suffix, so it changes when the endpoint is recreated.
- The model-registration script currently uses a manually supplied training job name. This is deliberate for the lesson but must be updated for each new training run.
- `00_connectivity_check.py` contains workspace identifiers directly, while the other workflow scripts read identifiers from environment variables. Keep credentials and secrets out of source files.
