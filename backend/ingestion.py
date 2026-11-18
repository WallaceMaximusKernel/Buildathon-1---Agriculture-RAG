
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_pdf(file_path):

    # Load PDF document
    loader = PyPDFLoader(file_path)

    documents = loader.load()

    print(f"Total pages loaded: {len(documents)}")

    return documents


def split_documents(documents):

    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    # Split documents into chunks
    chunks = text_splitter.split_documents(documents)

    print(f"Total chunks generated: {len(chunks)}")

    return chunks
