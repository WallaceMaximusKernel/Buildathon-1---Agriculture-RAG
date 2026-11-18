
import os
import uuid

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from backend.generation import generate_answer


from backend.ingestion import load_pdf, split_documents
from backend.vector_store import create_vector_store
from backend.retrieval import search_documents


app = FastAPI(
    title="Agriculture RAG API",
    description="Agricultural Government Schemes RAG Application",
    version="1.0.0"
)


UPLOAD_PATH = "uploads"

os.makedirs(UPLOAD_PATH, exist_ok=True)


# Request model for question
class QueryRequest(BaseModel):

    question: str
    top_k: int = 3


# API 1: Upload PDF and create embeddings
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Generate unique filename
    filename = f"{uuid.uuid4().hex}_{os.path.basename(file.filename)}"

    file_path = os.path.join(UPLOAD_PATH, filename)

    try:

        # Save uploaded PDF
        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded PDF is empty"
            )

        with open(file_path, "wb") as f:
            f.write(content)

        # Pipeline 1: Load PDF
        documents = load_pdf(file_path)

        if not documents or not any(
            document.page_content.strip() for document in documents
        ):
            raise HTTPException(
                status_code=400,
                detail="No extractable text found in PDF"
            )

        # Pipeline 2: Split documents
        chunks = split_documents(documents)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No text chunks generated"
            )

        # Pipeline 3: Generate embeddings and store in FAISS
        create_vector_store(chunks)

        return {
            "status": "success",
            "message": "PDF processed and stored in FAISS",
            "filename": filename,
            "total_pages": len(documents),
            "total_chunks": len(chunks)
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        await file.close()


# API 2: Retrieve relevant documents
@app.post("/query")
def query_documents(request: QueryRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    if not os.path.exists("faiss_index/index.faiss"):
        raise HTTPException(
            status_code=404,
            detail="No documents found. Please upload a PDF first."
        )

    results = search_documents(question, top_k=request.top_k)

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No relevant information found."
        )

    context = "\n\n".join([
        f"[Source: {os.path.basename(doc.metadata.get('source', 'Unknown'))}, "
        f"Page: {doc.metadata.get('page', 0) + 1}]\n"
        f"{doc.page_content}"
        for doc, score in results
    ])

    answer = generate_answer(question, context)

    sources = [
        {
            "source": os.path.basename(
                doc.metadata.get("source", "Unknown")
            ),
            "page": doc.metadata.get("page", 0) + 1,
            "score": float(score)
        }
        for doc, score in results
    ]

    return {
        "question": question,
        "answer": answer,
        "sources": sources
    }

# API 3: Backend and FAISS status
@app.get("/status")
def get_status():

    faiss_exists = os.path.exists(
        os.path.join("faiss_index", "index.faiss")
    )

    return {
        "backend": "running",
        "faiss_database": (
            "available" if faiss_exists else "not available"
        )
    }


@app.get("/")
def home():

    return {
        "message": "Welcome to Agriculture RAG API"
    }
