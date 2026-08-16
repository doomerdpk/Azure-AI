from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI

client = SearchClient(
    endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
    index_name=os.environ["AZURE_SEARCH_INDEX"],
    credential=AzureKeyCredential(os.environ["AZURE_SEARCH_KEY"])
)

# Basic keyword search
# print("=== Keyword Search: 'kubernetes containers' ===")
# results = client.search(search_text="kubernetes containers")
# for r in results:
#     print(f"  [{r['category']}] {r['title']}")
#     print(f"  {r['content'][:100]}...")

# Filter by category
# print("\n=== Filtered Search: category = AI ===")
# results = client.search(search_text="*", filter="category eq 'AI'")
# for r in results:
#     print(f"  {r['title']}")



# from azure.search.documents.models import QueryType

# print("\n=== Semantic Search: 'AI APIs without ML expertise' ===")
# results = client.search(
#     search_text="AI APIs without ML expertise",
#     query_type=QueryType.SEMANTIC,
#     semantic_configuration_name="default",
#     top=3
# )
# for r in results:
#     print(f"  [{r['category']}] {r['title']}")
#     print(f"  {r['content'][:100]}...")


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


# from azure.search.documents.models import VectorizedQuery

# print("\n=== Vector Search: 'CI/CD automation' ===")

# query_vector = openai_client.embeddings.create(
#     input="CI/CD automation",
#     model=os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT"]
# ).data[0].embedding

# results = search_client.search(
#     search_text=None,
#     vector_queries=[
#         VectorizedQuery(
#             vector=query_vector,
#             k_nearest_neighbors=3,
#             fields="content_vector"
#         )
#     ]
# )

# for r in results:
#     print(f"  [{r['category']}] {r['title']}")
#     print(f"  Score: {r['@search.score']:.4f}")
#     print(f"  {r['content'][:100]}...")




print("\n=== Hybrid Search: 'CI/CD automation' ===")

query_vector = openai_client.embeddings.create(
    input="CI/CD automation",
    model=os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT"]
).data[0].embedding

results = search_client.search(
    search_text="CI/CD automation",
    vector_queries=[
        VectorizedQuery(
            vector=query_vector,
            k_nearest_neighbors=3,
            fields="content_vector"
        )
    ],
    top=3
)

for r in results:
    print(f"  [{r['category']}] {r['title']}")
    print(f"  Score: {r['@search.score']:.4f}")
    print(f"  {r['content'][:100]}...")