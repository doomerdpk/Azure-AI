import os
from dotenv import load_dotenv
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

load_dotenv()
from azure.ai.vision.imageanalysis.models import VisualFeatures

client = ImageAnalysisClient(
    endpoint=os.environ["CV_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["CV_KEY"])
)

result = client.analyze_from_url(
    image_url="https://learn.microsoft.com/azure/ai-services/computer-vision/media/quickstarts/presentation.png",
    visual_features=[VisualFeatures.SMART_CROPS],
)

if result.smart_crops is not None:
    for crop in result.smart_crops.list:
        print(f"Aspect ratio: {crop.aspect_ratio}  BoundingBox: {crop.bounding_box}")