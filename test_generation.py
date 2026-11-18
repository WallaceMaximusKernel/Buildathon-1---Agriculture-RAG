
from backend.retrieval import search_documents
from backend.generation import generate_answer

# User question
question = "What subsidy is available for agricultural machinery?"

# Step 1: Retrieve relevant chunks from FAISS
results = search_documents(question, top_k=3)

# Step 2: Prepare retrieved context
context = "\n\n".join([
    document.page_content
    for document, score in results
])

# Step 3: Generate answer using OpenAI
answer = generate_answer(question, context)

# Step 4: Display answer
print("\nQUESTION:")
print(question)

print("\nGENERATED ANSWER:")
print(answer)
