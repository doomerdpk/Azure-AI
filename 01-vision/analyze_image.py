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

result = client.analyze_from_url(
    image_url="https://learn.microsoft.com/azure/ai-services/computer-vision/media/quickstarts/presentation.png",
    visual_features=[VisualFeatures.CAPTION, VisualFeatures.TAGS, VisualFeatures.OBJECTS],
)

print("Caption:", result.caption.text, result.caption.confidence)
print("Tags:", [t.name for t in result.tags.list])
print("Objects:", [o.tags[0].name for o in result.objects.list])