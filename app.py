import streamlit as st

from src.config import get_settings
from src.document_loader import load_uploaded_file
from src.rag_service import RAGService

st.set_page_config(
    page_title="DocMind — RAG Document Intelligence",
    page_icon="🧠",
    layout="wide",
)

settings = get_settings()


@st.cache_resource
def get_service():
    return RAGService(settings)


service = get_service()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "indexed_docs" not in st.session_state:
    st.session_state.indexed_docs = []

with st.sidebar:
    st.title("🧠 DocMind")
    st.caption("RAG-Based Document Intelligence")
    st.divider()

    uploaded_files = st.file_uploader(
        "Upload PDF, DOCX or TXT files",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        max_upload_size=settings.max_file_size_mb,
    )

    if uploaded_files and st.button(
        "📥 Index documents", type="primary", use_container_width=True
    ):
        progress = st.progress(0)
        status = st.empty()

        for i, uploaded in enumerate(uploaded_files):
            try:
                status.info(f"Processing {uploaded.name}...")
                chunks = load_uploaded_file(uploaded)
                result = service.index_document(chunks)
                st.session_state.indexed_docs.append(result)
            except Exception as exc:
                st.error(f"{uploaded.name}: {exc}")
            progress.progress((i + 1) / len(uploaded_files))

        status.success("Indexing complete.")

    st.divider()
    service.top_k = st.slider("Retrieved chunks", 2, 10, settings.top_k)

    st.subheader("Indexed documents")
    for doc in st.session_state.indexed_docs[-10:]:
        st.write(f"📄 {doc['file']} — {doc['chunks']} chunks")

    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.title("RAG-Based Document Intelligence System")
st.caption("Upload documents → retrieve relevant context → generate grounded answers.")

chat_tab, insights_tab, about_tab = st.tabs(
    ["💬 Chat", "📑 Document Insights", "ℹ️ About"]
)

with chat_tab:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("sources"):
                with st.expander("Sources"):
                    for source in message["sources"]:
                        st.markdown(
                            f"**[{source['index']}] {source['file']}** "
                            f"({source['location']}) · similarity `{source['similarity']:.3f}`"
                        )
                        st.caption(source["preview"])

    question = st.chat_input("Ask a question about your indexed documents...")

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            try:
                with st.spinner("Retrieving context and generating answer..."):
                    result = service.answer(question)
                st.markdown(result["answer"])

                with st.expander("Sources", expanded=True):
                    for source in result["sources"]:
                        st.markdown(
                            f"**[{source['index']}] {source['file']}** "
                            f"({source['location']}) · similarity `{source['similarity']:.3f}`"
                        )
                        st.caption(source["preview"])

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["answer"],
                    "sources": result["sources"],
                })
            except Exception as exc:
                st.error(str(exc))

with insights_tab:
    st.subheader("Document Insights")
    stats = service.collection_stats()
    c1, c2 = st.columns(2)
    c1.metric("Indexed chunks", stats["chunks"])
    c2.metric("Collection", stats["collection"])

    if stats["chunks"] == 0:
        st.info("Index a document first.")
    elif st.button("✨ Generate collection summary", type="primary"):
        try:
            with st.spinner("Generating summary..."):
                result = service.summarize()
            st.markdown(result["summary"])
            if result["key_points"]:
                st.subheader("Key points")
                for point in result["key_points"]:
                    st.markdown(f"- {point}")
        except Exception as exc:
            st.error(str(exc))

with about_tab:
    st.subheader("What this demonstrates")
    st.markdown("""
    - **RAG architecture:** retrieval before generation
    - **Embeddings:** semantic representation of document chunks
    - **Vector search:** persistent ChromaDB retrieval
    - **Grounding:** answers constrained to retrieved context
    - **Source attribution:** file/page citations
    - **Document engineering:** PDF, DOCX and TXT parsing
    - **GenAI engineering:** configuration, persistence, testing and Docker
    """)
