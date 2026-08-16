from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

client = DocumentAnalysisClient(
    endpoint=os.environ["DOC_INTELLIGENCE_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["DOC_INTELLIGENCE_KEY"])
)

receipt_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/receipt.png"

poller = client.begin_analyze_document_from_url("prebuilt-receipt", receipt_url)
result = poller.result()

for receipt in result.documents:
    print(f"Receipt type: {receipt.doc_type}")
    fields = receipt.fields

    if "MerchantName" in fields:
        print(f"Merchant: {fields['MerchantName'].value} (confidence: {fields['MerchantName'].confidence:.2f})")
    if "TransactionDate" in fields:
        print(f"Date: {fields['TransactionDate'].value} (confidence: {fields['TransactionDate'].confidence:.2f})")
    if "Total" in fields:
        print(f"Total: {fields['Total'].value} (confidence: {fields['Total'].confidence:.2f})")
    if "Items" in fields:
        print("Items:")
        for item in fields["Items"].value:
            name = item.value.get("Description")
            price = item.value.get("TotalPrice")
            if name and price:
                print(f"  - {name.value}: {price.value}")