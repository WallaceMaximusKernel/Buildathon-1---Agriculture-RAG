
from langchain_community.vectorstores import FAISS
from backend.embeddings import get_embedding_model


def load_vector_store():

    # Load embedding model
    embeddings = get_embedding_model()

    # Load existing FAISS database
    vector_store = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    print("FAISS database loaded successfully!")

    return vector_store


def search_documents(question, top_k=3):

    # Load FAISS database
    vector_store = load_vector_store()

    # Perform similarity search
    results = vector_store.similarity_search_with_score(
        question,
        k=top_k
    )

    return results
