# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv())

# import os
# from azure.search.documents import SearchClient
# from azure.core.credentials import AzureKeyCredential

# client = SearchClient(
#     endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
#     index_name=os.environ["AZURE_SEARCH_INDEX"],
#     credential=AzureKeyCredential(os.environ["AZURE_SEARCH_KEY"])
# )

# documents = [
#     {
#         "id": "1",
#         "title": "Azure OpenAI Service Overview",
#         "content": "Azure OpenAI Service provides access to OpenAI's GPT models including GPT-4 and GPT-3.5. It enables natural language processing, code generation, and text summarization at enterprise scale with Azure security.",
#         "category": "AI"
#     },
#     {
#         "id": "2",
#         "title": "Azure Kubernetes Service",
#         "content": "Azure Kubernetes Service (AKS) is a managed container orchestration service. It simplifies deploying, managing, and scaling containerized applications using Kubernetes on Azure.",
#         "category": "DevOps"
#     },
#     {
#         "id": "3",
#         "title": "Azure AI Search",
#         "content": "Azure AI Search is a cloud search service with built-in AI capabilities. It supports full-text search, semantic search, and vector search for building intelligent search experiences.",
#         "category": "AI"
#     },
#     {
#         "id": "4",
#         "title": "Azure DevOps Pipelines",
#         "content": "Azure DevOps Pipelines automates build, test, and deployment workflows. It supports CI/CD for any language, platform, and cloud with YAML-based pipeline definitions.",
#         "category": "DevOps"
#     },
#     {
#         "id": "5",
#         "title": "Azure Cognitive Services",
#         "content": "Azure Cognitive Services are prebuilt AI APIs for vision, speech, language and decision making. Developers can add AI capabilities to apps without machine learning expertise.",
#         "category": "AI"
#     }
# ]

# result = client.upload_documents(documents)
# print(f"Uploaded {len(documents)} documents")
# for r in result:
#     print(f"  id: {r.key} succeeded: {r.succeeded}")





from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI

search_client = SearchClient(
    endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
    index_name=os.environ["AZURE_SEARCH_INDEX"],
    credential=AzureKeyCredential(os.environ["AZURE_SEARCH_KEY"])
)

openai_client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_KEY"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version="2024-12-01-preview"
)

def get_embedding(text):
    response = openai_client.embeddings.create(
        input=text,
        model=os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT"]
    )
    return response.data[0].embedding

documents = [
    {"id": "1", "title": "Azure OpenAI Service Overview", "content": "Azure OpenAI Service provides access to OpenAI's GPT models including GPT-4 and GPT-3.5. It enables natural language processing, code generation, and text summarization at enterprise scale with Azure security.", "category": "AI"},
    {"id": "2", "title": "Azure Kubernetes Service", "content": "Azure Kubernetes Service (AKS) is a managed container orchestration service. It simplifies deploying, managing, and scaling containerized applications using Kubernetes on Azure.", "category": "DevOps"},
    {"id": "3", "title": "Azure AI Search", "content": "Azure AI Search is a cloud search service with built-in AI capabilities. It supports full-text search, semantic search, and vector search for building intelligent search experiences.", "category": "AI"},
    {"id": "4", "title": "Azure DevOps Pipelines", "content": "Azure DevOps Pipelines automates build, test, and deployment workflows. It supports CI/CD for any language, platform, and cloud with YAML-based pipeline definitions.", "category": "DevOps"},
    {"id": "5", "title": "Azure Cognitive Services", "content": "Azure Cognitive Services are prebuilt AI APIs for vision, speech, language and decision making. Developers can add AI capabilities to apps without machine learning expertise.", "category": "AI"}
]

print("Generating embeddings and uploading...")
for doc in documents:
    doc["content_vector"] = get_embedding(doc["content"])
    print(f"  Embedded: {doc['title']} ({len(doc['content_vector'])} dimensions)")

result = search_client.upload_documents(documents)
for r in result:
    print(f"  Uploaded id:{r.key} succeeded:{r.succeeded}")