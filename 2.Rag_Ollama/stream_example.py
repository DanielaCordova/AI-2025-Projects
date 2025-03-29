import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import subprocess
import tempfile
import os
#THE SAME AS set STREAMLIT_WATCH_DISABLE=true AT COMMAND LINE TO : Streamlit's file watcher tries to inspect all modules to reload them on code change,
#  PyTorch's internal module torch.classes has a non-standard structure that confuses Streamlit's watcher
#Result: You see an exception from torch._classes.py, but your app still runs fine
import sys
import types

# Fake the torch.classes module path to avoid Streamlit crash
import torch
torch.classes.__path__ = types.SimpleNamespace(_path=[])


st.set_page_config(page_title="Local RAG with Ollama", layout="centered")
st.title("📄🔍 RAG App with Local Ollama")

uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])
question = st.text_input("Ask a question about the document:")

if uploaded_file and question:
    with st.spinner("Processing document and searching for answers..."):
        # Save PDF temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        # Load and split PDF
        loader = PyPDFLoader(tmp_path)
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)

        # Embed and store in Chroma
        embedder = HuggingFaceEmbeddings(
            model_name='sentence-transformers/all-MiniLM-L6-v2',
            model_kwargs={'device': 'cuda'},
            encode_kwargs={'batch_size': 32}
        )
        db = Chroma.from_documents(chunks, embedding=embedder)

        # Search similar chunks
        results = db.similarity_search(question, k=3)
        context = "\n\n".join([doc.page_content for doc in results])

        # Build prompt
        rag_prompt = f"""Answer the question based on the context below.

Context:
{context}

Question:
{question}
"""

        # Run Ollama model locally
        try:
            response = subprocess.run(
                ["ollama", "run", "mistral"],
                input=rag_prompt.encode(),
                capture_output=True,
                timeout=60
            )
            answer = response.stdout.decode()
        except Exception as e:
            answer = f"Error calling Ollama: {e}"

        # Clean up temp file
        os.remove(tmp_path)

        st.subheader("📌 Answer:")
        st.write(answer)

        st.subheader("🔎 Retrieved Context:")
        st.text(context)
