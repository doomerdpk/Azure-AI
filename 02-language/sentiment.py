from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

client = TextAnalyticsClient(
    endpoint=os.environ["LANG_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["LANG_KEY"])
)

# documents = [
#     "I absolutely loved this product, it exceeded all my expectations!",
#     "The service was terrible and I want a refund.",
#     "It was okay, nothing special but not bad either."
# ]

# results = client.analyze_sentiment(documents)

# for doc in results:
#     print(f"Text: {doc.sentences[0].text if doc.sentences else ''}")
#     print(f"Overall sentiment: {doc.sentiment}")
#     print(f"Scores -> positive: {doc.confidence_scores.positive:.2f}, "
#           f"neutral: {doc.confidence_scores.neutral:.2f}, "
#           f"negative: {doc.confidence_scores.negative:.2f}")
#     print("---")


documents = [
    "The food was great but the service was painfully slow.",
]

results = client.analyze_sentiment(documents, show_opinion_mining=True)

for doc in results:
    for sentence in doc.sentences:
        print(f"Sentence: {sentence.text}")
        print(f"Overall sentence sentiment: {sentence.sentiment}")
        for opinion in sentence.mined_opinions:
            target = opinion.target
            print(f"  Target: '{target.text}' -> {target.sentiment} "
                  f"(positive: {target.confidence_scores.positive:.2f}, "
                  f"negative: {target.confidence_scores.negative:.2f})")
            for assessment in opinion.assessments:
                print(f"    Assessment: '{assessment.text}' -> {assessment.sentiment}")
        print("---")