from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

client = DocumentAnalysisClient(
    endpoint=os.environ["DOC_INTELLIGENCE_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["DOC_INTELLIGENCE_KEY"])
)

invoice_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/invoice.pdf"

poller = client.begin_analyze_document_from_url("prebuilt-invoice", invoice_url)
result = poller.result()

for invoice in result.documents:
    fields = invoice.fields
    print(f"Vendor: {fields.get('VendorName', {}).value if fields.get('VendorName') else 'N/A'}")
    print(f"Customer: {fields.get('CustomerName', {}).value if fields.get('CustomerName') else 'N/A'}")
    print(f"Invoice ID: {fields.get('InvoiceId', {}).value if fields.get('InvoiceId') else 'N/A'}")
    print(f"Due Date: {fields.get('DueDate', {}).value if fields.get('DueDate') else 'N/A'}")
    print(f"Amount Due: {fields.get('AmountDue', {}).value if fields.get('AmountDue') else 'N/A'}")
    if "Items" in fields:
        print("Line items:")
        for item in fields["Items"].value:
            desc = item.value.get("Description")
            amount = item.value.get("Amount")
            if desc and amount:
                print(f"  - {desc.value}: {amount.value}")