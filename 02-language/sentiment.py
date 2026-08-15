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


# documents = [
#     "The food was great but the service was painfully slow.",
# ]

# results = client.analyze_sentiment(documents, show_opinion_mining=True)

# for doc in results:
#     for sentence in doc.sentences:
#         print(f"Sentence: {sentence.text}")
#         print(f"Overall sentence sentiment: {sentence.sentiment}")
#         for opinion in sentence.mined_opinions:
#             target = opinion.target
#             print(f"  Target: '{target.text}' -> {target.sentiment} "
#                   f"(positive: {target.confidence_scores.positive:.2f}, "
#                   f"negative: {target.confidence_scores.negative:.2f})")
#             for assessment in opinion.assessments:
#                 print(f"    Assessment: '{assessment.text}' -> {assessment.sentiment}")
#         print("---")

# documents = [
#     "Microsoft was founded by Bill Gates and Paul Allen in Albuquerque, New Mexico. The company is now headquartered in Redmond, Washington."
# ]

# results = client.extract_key_phrases(documents)

# for doc in results:
#     print("Key phrases:", doc.key_phrases)


# documents = [
#     "Microsoft was founded by Bill Gates and Paul Allen in Albuquerque, New Mexico. The company is now headquartered in Redmond, Washington."
# ]

# results = client.recognize_entities(documents)

# for doc in results:
#     for entity in doc.entities:
#         print(f"Text: {entity.text}  Category: {entity.category}  Subcategory: {entity.subcategory}  Confidence: {entity.confidence_score:.2f}")

# documents = [
#     "My name is John Smith, my SSN is 859-98-0987, and you can reach me at john.smith@email.com or call 425-555-0123."
# ]

# results = client.recognize_pii_entities(documents)

# for doc in results:
#     print("Redacted text:", doc.redacted_text)
#     for entity in doc.entities:
#         print(f"  Entity: {entity.text}  Category: {entity.category}  Confidence: {entity.confidence_score:.2f}")


# documents = [
#     "This is written in English.",
#     "Ceci est écrit en français.",
#     "यह हिंदी में लिखा गया है।",
# ]

# results = client.detect_language(documents)

# for doc in results:
#     print(f"Language: {doc.primary_language.name}  ISO code: {doc.primary_language.iso6391_name}  Confidence: {doc.primary_language.confidence_score:.2f}")


raw_text = """Azure AI Language is a cloud-based service that provides natural language processing 
    features for understanding and analyzing text. It includes capabilities such as sentiment 
    analysis, key phrase extraction, named entity recognition, and language detection. Developers 
    can use this service to build applications that understand human language, extract insights 
    from unstructured text, and automate tasks like content moderation and customer feedback analysis. 
    The service supports multiple languages and can be accessed through REST APIs or client SDKs 
    in various programming languages. It is part of the broader Azure AI Services portfolio, which 
    also includes vision, speech, and decision-making capabilities."""

document = [" ".join(raw_text.split())]

poller = client.begin_extract_summary(document)
results = poller.result()

for result in results:
    if result.kind == "ExtractiveSummarization":
        print("Extractive summary sentences:")
        for sentence in result.sentences:
            print(f"  - {sentence.text} (rank: {sentence.rank_score:.2f})")