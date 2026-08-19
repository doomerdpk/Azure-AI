from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())

from azure.ai.evaluation import RelevanceEvaluator, CoherenceEvaluator

judge_model_config = {
    "azure_endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
    "api_key": os.environ["AZURE_OPENAI_KEY"],
    "azure_deployment": "gpt-chat-latest-judge",
}

relevance_eval = RelevanceEvaluator(judge_model_config, is_reasoning_model=True)
coherence_eval = CoherenceEvaluator(judge_model_config, is_reasoning_model=True)

query = "What is the capital of France?"
response = "Paris is the capital of France."

relevance_result = relevance_eval(query=query, response=response)
coherence_result = coherence_eval(query=query, response=response)

print("Relevance:", relevance_result)
print()
print("Coherence:", coherence_result)