
from backend.retrieval import search_documents

question = "What subsidies are available for agricultural machinery?"

results = search_documents(question, top_k=3)

print("\nRetrieved Results:")

for i, (document, score) in enumerate(results, start=1):

    print(f"\nResult {i}")
    print("-" * 50)

    print("Content:", document.page_content)

    print("Source:", document.metadata.get("source"))

    print("Page:", document.metadata.get("page"))

    print("Similarity Distance:", score)
