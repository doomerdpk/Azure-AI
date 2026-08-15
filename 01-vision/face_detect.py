import os
from dotenv import load_dotenv
from azure.ai.vision.face import FaceClient
from azure.ai.vision.face.models import FaceDetectionModel, FaceRecognitionModel, FaceAttributeTypeDetection01
from azure.core.credentials import AzureKeyCredential

load_dotenv()

client = FaceClient(
    endpoint=os.environ["FACE_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["FACE_KEY"])
)

with open("Photo.jpg", "rb") as f:
    result = client.detect(
        f.read(),
        detection_model=FaceDetectionModel.DETECTION01,
        recognition_model=FaceRecognitionModel.RECOGNITION01,
        return_face_id=False,
        return_face_attributes=[FaceAttributeTypeDetection01.HEAD_POSE, FaceAttributeTypeDetection01.OCCLUSION],
    )

for face in result:
    print("Bounding box:", face.face_rectangle)
    print("Attributes:", face.face_attributes)