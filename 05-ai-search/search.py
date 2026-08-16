from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

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



from azure.search.documents.models import QueryType

print("\n=== Semantic Search: 'AI APIs without ML expertise' ===")
results = client.search(
    search_text="AI APIs without ML expertise",
    query_type=QueryType.SEMANTIC,
    semantic_configuration_name="default",
    top=3
)
for r in results:
    print(f"  [{r['category']}] {r['title']}")
    print(f"  {r['content'][:100]}...")