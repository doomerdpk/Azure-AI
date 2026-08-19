from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())

from azure.ai.evaluation import RelevanceEvaluator

judge_model_config = {
    "azure_endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
    "api_key": os.environ["AZURE_OPENAI_KEY"],
    "azure_deployment": os.environ["AZURE_OPENAI_DEPLOYMENT"],
}

relevance_eval = RelevanceEvaluator(judge_model_config, is_reasoning_model=True)

result = relevance_eval(
    query="What is the capital of France?",
    response="Paris is the capital of France."
)
print(result)