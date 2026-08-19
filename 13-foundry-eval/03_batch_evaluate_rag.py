from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
import sys
import json

sys.path.insert(0, os.path.expanduser("~/Projects/azure-ai-learning/06-rag"))
from rag import retrieve, generate

from azure.ai.evaluation import evaluate, RelevanceEvaluator, CoherenceEvaluator, GroundednessEvaluator

judge_model_config = {
    "azure_endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
    "api_key": os.environ["AZURE_OPENAI_KEY"],
    "azure_deployment": "gpt-chat-latest-judge",
}

queries = [
    "How does Azure DevOps Pipelines support CI/CD?",
    "What search capabilities does Azure AI Search provide?",
    "What is the price of Azure Virtual Machines?",
]

# Generate RAG outputs once, write to JSONL eval dataset
data_path = "eval_data.jsonl"
with open(data_path, "w") as f:
    for query in queries:
        docs = retrieve(query)
        answer = generate(query, docs)
        context = "\n\n".join([f"Document: {d['title']}\n{d['content']}" for d in docs])
        row = {"query": query, "response": answer, "context": context}
        f.write(json.dumps(row) + "\n")
        print(f"Generated: {query} -> {answer[:80]}...")

print("\nRunning batch evaluation...")

result = evaluate(
    data=data_path,
    evaluators={
        "relevance": RelevanceEvaluator(judge_model_config, is_reasoning_model=True),
        "coherence": CoherenceEvaluator(judge_model_config, is_reasoning_model=True),
        "groundedness": GroundednessEvaluator(judge_model_config, is_reasoning_model=True),
    },
)

print("\n--- Metrics summary ---")
print(json.dumps(result["metrics"], indent=2))