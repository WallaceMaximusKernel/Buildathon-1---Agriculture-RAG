
from backend.embeddings import get_embedding_model

# Initialize embedding model
embeddings = get_embedding_model()

# Sample agricultural scheme text
text = "Government provides subsidies for agricultural machinery."

# Generate embedding
vector = embeddings.embed_query(text)

print("Embedding model loaded successfully!")
print("Vector dimensions:", len(vector))
print("First 5 values:", vector[:5])
