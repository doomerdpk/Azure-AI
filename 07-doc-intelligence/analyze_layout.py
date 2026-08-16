from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

client = DocumentAnalysisClient(
    endpoint=os.environ["DOC_INTELLIGENCE_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["DOC_INTELLIGENCE_KEY"])
)


doc_url = "https://raw.githubusercontent.com/Azure/azure-sdk-for-python/main/sdk/formrecognizer/azure-ai-formrecognizer/samples/sample_forms/forms/Invoice_1.pdf"

poller = client.begin_analyze_document_from_url("prebuilt-layout", doc_url)
result = poller.result()

print("=== Pages ===")
for page in result.pages:
    print(f"Page {page.page_number}: {len(page.lines)} lines, {len(page.words)} words")

# Extract tables
print("\n=== Tables ===")
for i, table in enumerate(result.tables):
    print(f"Table {i+1}: {table.row_count} rows x {table.column_count} columns")
    for cell in table.cells:
        if cell.row_index == 0:
            print(f"  Header col {cell.column_index}: {cell.content}")