
from backend.ingestion import load_pdf, split_documents
from backend.vector_store import create_vector_store

file_path = "sample_scheme.pdf"

# Load PDF
documents = load_pdf(file_path)

# Split documents
chunks = split_documents(documents)

# Create FAISS database
vector_store = create_vector_store(chunks)

print("Vector database creation completed!")
