import os
from dotenv import load_dotenv
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

load_dotenv()

client = ImageAnalysisClient(
    endpoint=os.environ["CV_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["CV_KEY"])
)

with open("burger.jpg", "rb") as f:
    image_data = f.read()

result = client.analyze(
    image_data=image_data,
    visual_features=[VisualFeatures.READ],
)

# result = client.analyze_from_url(
#     image_url="https://learn.microsoft.com/azure/ai-services/computer-vision/media/quickstarts/presentation.png",
#     visual_features=[VisualFeatures.READ],
# )

if result.read is not None:
    for block in result.read.blocks:
        for line in block.lines:
            print(f"Line: '{line.text}'  BoundingBox: {line.bounding_polygon}")