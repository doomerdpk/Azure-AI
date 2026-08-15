import os
from dotenv import load_dotenv
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

load_dotenv()

prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": os.environ["CV_PREDICTION_KEY"]})
predictor = CustomVisionPredictionClient(os.environ["CV_PREDICTION_ENDPOINT"], prediction_credentials)

project_id = os.environ["CV_PROJECT_ID"]
publish_name = "hemlock-cherry-model"

test_image_path = "custom-vision-data/Test/test_image.jpg"

with open(test_image_path, "rb") as f:
    results = predictor.classify_image(project_id, publish_name, f.read())

for prediction in results.predictions:
    print(f"{prediction.tag_name}: {prediction.probability * 100:.2f}%")