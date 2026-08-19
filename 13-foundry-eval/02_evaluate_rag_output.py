from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
import sys

sys.path.insert(0, os.path.expanduser("~/Projects/azure-ai-learning/06-rag"))
from rag import retrieve, generate

from azure.ai.evaluation import RelevanceEvaluator, CoherenceEvaluator, GroundednessEvaluator

judge_model_config = {
    "azure_endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
    "api_key": os.environ["AZURE_OPENAI_KEY"],
    "azure_deployment": "gpt-chat-latest-judge",
}

relevance_eval = RelevanceEvaluator(judge_model_config, is_reasoning_model=True)
coherence_eval = CoherenceEvaluator(judge_model_config, is_reasoning_model=True)
groundedness_eval = GroundednessEvaluator(judge_model_config, is_reasoning_model=True)

query = "What search capabilities does Azure AI Search provide?"

docs = retrieve(query)
answer = generate(query, docs)
context = "\n\n".join([f"Document: {d['title']}\n{d['content']}" for d in docs])

print(f"Query: {query}")
print(f"Answer: {answer}\n")

print("Relevance:", relevance_eval(query=query, response=answer))
print()
print("Coherence:", coherence_eval(query=query, response=answer))
print()
print("Groundedness:", groundedness_eval(query=query, response=answer, context=context))