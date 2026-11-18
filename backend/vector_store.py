
import os

from langchain_community.vectorstores import FAISS
from backend.embeddings import get_embedding_model


FAISS_PATH = "faiss_index"


def create_vector_store(chunks):

    embeddings = get_embedding_model()

    if os.path.exists(os.path.join(FAISS_PATH, "index.faiss")):

        vector_store = FAISS.load_local(
            FAISS_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

        vector_store.add_documents(chunks)

        print("New documents added to existing FAISS database!")

    else:

        vector_store = FAISS.from_documents(
            documents=chunks,
            embedding=embeddings
        )

        print("New FAISS database created!")

    vector_store.save_local(FAISS_PATH)

    print("FAISS database saved successfully!")

    return vector_store
