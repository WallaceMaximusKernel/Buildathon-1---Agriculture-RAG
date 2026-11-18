
from backend.ingestion import load_pdf, split_documents

# Provide your PDF file path
file_path = "sample_scheme.pdf"

# Step 1: Load PDF
documents = load_pdf(file_path)

# Step 2: Split documents
chunks = split_documents(documents)

# Display first chunk
print("\nFirst Chunk:")
print(chunks[0].page_content)

# Display metadata
print("\nMetadata:")
print(chunks[0].metadata)

