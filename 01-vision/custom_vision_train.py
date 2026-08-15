import os
import time
from dotenv import load_dotenv
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry
from msrest.authentication import ApiKeyCredentials

load_dotenv()

credentials = ApiKeyCredentials(in_headers={"Training-key": os.environ["CV_TRAINING_KEY"]})
trainer = CustomVisionTrainingClient(os.environ["CV_TRAINING_ENDPOINT"], credentials)

# project = trainer.create_project("Tree Classifier - Hemlock vs Cherry")
# print("Project created:", project.id, project.name)

# hemlock_tag = trainer.create_tag(project.id, "Hemlock")
# cherry_tag = trainer.create_tag(project.id, "Japanese_Cherry")
# print("Tags created:", hemlock_tag.id, cherry_tag.id)

project_id = os.environ["CV_PROJECT_ID"]
iteration_id = os.environ["CV_ITERATION_ID"]

tags = trainer.get_tags(project_id)
hemlock_tag = next(t for t in tags if t.name == "Hemlock")
cherry_tag = next(t for t in tags if t.name == "Japanese_Cherry")

# base_path = "custom-vision-data/"

# def upload_images(folder, tag):
#     folder_path = os.path.join(base_path, folder)
#     image_list = []
#     for filename in os.listdir(folder_path):
#         with open(os.path.join(folder_path, filename), "rb") as f:
#             image_list.append(ImageFileCreateEntry(name=filename, contents=f.read(), tag_ids=[tag.id]))
#     upload_result = trainer.create_images_from_files(project_id, ImageFileCreateBatch(images=image_list))
#     if not upload_result.is_batch_successful:
#         for image in upload_result.images:
#             print("Image status:", image.status)
#     else:
#         print(f"Uploaded {len(image_list)} images tagged '{tag.name}'")

# upload_images("Hemlock", hemlock_tag)
# upload_images("Japanese_Cherry", cherry_tag)



# print("Training...")
# iteration = trainer.train_project(project_id)
# while iteration.status != "Completed":
#     iteration = trainer.get_iteration(project_id, iteration.id)
#     print("Training status:", iteration.status)
#     time.sleep(5)

# print("Training completed. Iteration ID:", iteration.id)

publish_name = "hemlock-cherry-model"
prediction_resource_id = os.environ["CV_PREDICTION_RESOURCE_ID"]

trainer.publish_iteration(project_id, iteration_id, publish_name, prediction_resource_id)
print(f"Published iteration as '{publish_name}'")