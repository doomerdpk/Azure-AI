from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
from azure.search.documents.indexes import SearchIndexClient
# from azure.search.documents.indexes.models import (
#     SearchIndex, SimpleField, SearchableField,
#     SearchFieldDataType, SearchField
# )
from azure.core.credentials import AzureKeyCredential

client = SearchIndexClient(
    endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AZURE_SEARCH_KEY"])
)

# index = SearchIndex(
#     name=os.environ["AZURE_SEARCH_INDEX"],
#     fields=[
#         SimpleField(name="id", type=SearchFieldDataType.String, key=True),
#         SearchableField(name="title", type=SearchFieldDataType.String),
#         SearchableField(name="content", type=SearchFieldDataType.String),
#         SimpleField(name="category", type=SearchFieldDataType.String, filterable=True, facetable=True),
#     ]
# )

# result = client.create_or_update_index(index)
# print(f"Index '{result.name}' created with {len(result.fields)} fields")





# from azure.search.documents.indexes.models import (
#     SearchIndex, SimpleField, SearchableField,
#     SearchFieldDataType, SemanticConfiguration,
#     SemanticSearch, SemanticPrioritizedFields,
#     SemanticField
# )

# index = SearchIndex(
#     name=os.environ["AZURE_SEARCH_INDEX"],
#     fields=[
#         SimpleField(name="id", type=SearchFieldDataType.String, key=True),
#         SearchableField(name="title", type=SearchFieldDataType.String),
#         SearchableField(name="content", type=SearchFieldDataType.String),
#         SimpleField(name="category", type=SearchFieldDataType.String, filterable=True, facetable=True),
#     ],
#     semantic_search=SemanticSearch(
#         configurations=[
#             SemanticConfiguration(
#                 name="default",
#                 prioritized_fields=SemanticPrioritizedFields(
#                     title_field=SemanticField(field_name="title"),
#                     content_fields=[SemanticField(field_name="content")]
#                 )
#             )
#         ]
#     )
# )

# result = client.create_or_update_index(index)
# print(f"Index updated with semantic configuration")





from azure.search.documents.indexes.models import (
    SearchIndex, SimpleField, SearchableField,
    SearchFieldDataType, SemanticConfiguration,
    SemanticSearch, SemanticPrioritizedFields,
    SemanticField, SearchField, VectorSearch,
    HnswAlgorithmConfiguration, VectorSearchProfile
)

index = SearchIndex(
    name=os.environ["AZURE_SEARCH_INDEX"],
    fields=[
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="title", type=SearchFieldDataType.String),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SimpleField(name="category", type=SearchFieldDataType.String, filterable=True, facetable=True),
        SearchField(
            name="content_vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=1536,
            vector_search_profile_name="default-profile"
        )
    ],
    vector_search=VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="default-algo")],
        profiles=[VectorSearchProfile(name="default-profile", algorithm_configuration_name="default-algo")]
    ),
    semantic_search=SemanticSearch(
        configurations=[
            SemanticConfiguration(
                name="default",
                prioritized_fields=SemanticPrioritizedFields(
                    title_field=SemanticField(field_name="title"),
                    content_fields=[SemanticField(field_name="content")]
                )
            )
        ]
    )
)

result = client.create_or_update_index(index)
print("Index updated with vector search support")