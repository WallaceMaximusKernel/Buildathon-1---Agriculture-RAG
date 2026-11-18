
import os
import requests
import streamlit as st

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Agricultural Schemes Assistant",
    page_icon="🌾",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background-color: #f5f8f4;
    }

    section[data-testid="stSidebar"] {
        background-color: #173f2b;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    .main-title {
        color: #174c30;
        font-size: 32px;
        font-weight: 700;
    }

    .sub-title {
        color: #47704f;
        font-size: 17px;
    }

    .answer-box {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2e7d32;
        color: #202820;
    }

    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #dce8dc;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("🌾 Agriculture RAG")
st.sidebar.caption("Tamil Nadu Government Schemes")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Upload Documents",
        "Ask Agricultural Schemes"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Agricultural Schemes Knowledge Assistant")


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def get_backend_status():
    try:
        response = requests.get(
            f"{API_URL}/status",
            timeout=5
        )

        if response.status_code == 200:
            return response.json()

        return None

    except requests.exceptions.RequestException:
        return None


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    st.markdown(
        '<p class="main-title">Agricultural Schemes Dashboard</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="sub-title">Tamil Nadu Government Agricultural Engineering Schemes</p>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    status = get_backend_status()

    uploaded_files = []

    if os.path.exists(UPLOAD_DIR):
        uploaded_files = [
            file for file in os.listdir(UPLOAD_DIR)
            if file.lower().endswith(".pdf")
        ]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Uploaded PDF Documents",
            len(uploaded_files)
        )

    with col2:
        if status:
            st.metric("Backend Status", "Connected")
        else:
            st.metric("Backend Status", "Disconnected")

    st.markdown("### About this Application")

    st.write("""
    This application helps users explore Tamil Nadu Government
    agricultural engineering schemes using Retrieval-Augmented
    Generation (RAG).

    **Key capabilities:**

    - Upload agricultural scheme PDF documents.
    - Extract and process PDF content.
    - Generate embeddings and store them in FAISS.
    - Retrieve relevant information using semantic search.
    - Generate AI-powered answers using OpenAI.
    """)

    st.info(
        "Start by uploading a PDF document, then ask questions "
        "about the available agricultural schemes."
    )


# --------------------------------------------------
# UPLOAD DOCUMENTS
# --------------------------------------------------

elif page == "Upload Documents":

    st.markdown(
        '<p class="main-title">Upload Documents</p>',
        unsafe_allow_html=True
    )

    st.write(
        "Upload PDF documents containing agricultural scheme information."
    )

    uploaded_files = st.file_uploader(
        "Choose PDF documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:

        st.write(f"Selected documents: {len(uploaded_files)}")

        if st.button("Upload and Process Documents"):

            for uploaded_file in uploaded_files:

                st.write(f"Processing: {uploaded_file.name}")

                try:
                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf"
                        )
                    }

                    response = requests.post(
                        f"{API_URL}/upload",
                        files=files,
                        timeout=300
                    )

                    if response.status_code == 200:

                        result = response.json()

                        st.success(
                            f"Successfully processed: {uploaded_file.name}"
                        )

                        col1, col2 = st.columns(2)

                        col1.metric(
                            "Pages Loaded",
                            result.get("pages", 0)
                        )

                        col2.metric(
                            "Chunks Generated",
                            result.get("chunks", 0)
                        )

                    else:
                        try:
                            error = response.json().get(
                                "detail",
                                "Upload failed."
                            )
                        except ValueError:
                            error = response.text

                        st.error(
                            f"{uploaded_file.name}: {error}"
                        )

                except requests.exceptions.RequestException as e:
                    st.error(f"Backend connection error: {e}")


# --------------------------------------------------
# ASK AGRICULTURAL SCHEMES
# --------------------------------------------------

elif page == "Ask Agricultural Schemes":

    st.markdown(
        '<p class="main-title">Ask Agricultural Schemes</p>',
        unsafe_allow_html=True
    )

    st.write(
        "Ask questions about Tamil Nadu Government agricultural schemes."
    )

    question = st.text_area(
        "Enter your question",
        placeholder=(
            "Example: What are the benefits provided under "
            "agricultural mechanisation schemes?"
        ),
        height=120
    )

    top_k = st.selectbox(
        "Number of relevant document sections",
        options=[1, 2, 3, 4, 5],
        index=2
    )

    if st.button("Get Answer", type="primary"):

        if not question.strip():

            st.warning("Please enter a question.")

        else:

            with st.spinner(
                "Searching documents and generating your answer..."
            ):

                try:

                    response = requests.post(
                        f"{API_URL}/query",
                        json={
                            "question": question,
                            "top_k": top_k
                        },
                        timeout=180
                    )

                    if response.status_code == 200:

                        data = response.json()

                        st.markdown("---")
                        st.subheader("🤖 AI Generated Answer")

                        st.markdown(
                            f'<div class="answer-box">{data["answer"]}</div>',
                            unsafe_allow_html=True
                        )

                        st.markdown("### 📚 Source Documents")

                        for source in data.get("sources", []):

                            st.write(
                                f"📄 **{source['source']}** "
                                f"| Page: {source['page']}"
                            )

                    else:

                        try:
                            error = response.json().get(
                                "detail",
                                "Unable to generate answer."
                            )
                        except ValueError:
                            error = response.text

                        st.error(error)

                except requests.exceptions.Timeout:

                    st.error(
                        "The request timed out. Please try again."
                    )

                except requests.exceptions.RequestException as e:

                    st.error(
                        f"Could not connect to the backend: {e}"
                    )
