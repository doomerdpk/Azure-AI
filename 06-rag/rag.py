from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions

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

content_safety_client = ContentSafetyClient(
    endpoint=os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AZURE_CONTENT_SAFETY_KEY"])
)

# Severity is 0-6 per category; 2 is a reasonable default block threshold for a learning setup
SEVERITY_THRESHOLD = 2


def check_content_safety(text):
    result = content_safety_client.analyze_text(AnalyzeTextOptions(text=text))
    flagged = [
        cat.category for cat in result.categories_analysis
        if cat.severity is not None and cat.severity >= SEVERITY_THRESHOLD
    ]
    return flagged  # empty list = safe


def retrieve(query, top=3):
    query_vector = openai_client.embeddings.create(
        input=query,
        model=os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT"]
    ).data[0].embedding

    results = search_client.search(
        search_text=query,
        vector_queries=[
            VectorizedQuery(
                vector=query_vector,
                k_nearest_neighbors=top,
                fields="content_vector"
            )
        ],
        top=top
    )
    return [{"title": r["title"], "content": r["content"]} for r in results]


def generate(query, context_docs):
    context = "\n\n".join([
        f"Document: {doc['title']}\n{doc['content']}"
        for doc in context_docs
    ])

    response = openai_client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        messages=[
            {
                "role": "system",
                "content": f"""You are a helpful assistant. Answer the user's question
based ONLY on the provided context documents. If the answer is not in the context,
say 'I don't have information about that in my knowledge base.'

Context: {context}"""
            },
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content


def rag(query):
    print(f"\nQuery: {query}")

    flagged = check_content_safety(query)
    if flagged:
        print(f"  Blocked by Content Safety: {flagged}")
        return "I can't process that request."

    print("Retrieving relevant documents...")
    docs = retrieve(query)
    for doc in docs:
        print(f"  - {doc['title']}")
    print("Generating answer...")
    answer = generate(query, docs)
    print(f"\nAnswer: {answer}")
    return answer


if __name__ == "__main__":
    rag("How does Azure DevOps Pipelines support CI/CD?")
    rag("What search capabilities does Azure AI Search provide?")
    rag("What is the price of Azure Virtual Machines?")
    rag("I want to kill everyone at my office tomorrow")