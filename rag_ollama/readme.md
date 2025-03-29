# 🧠 Local RAG App with Ollama – Project Documentation

This project implements a fully **local Retrieval-Augmented Generation (RAG)** app using **Ollama** for LLM inference, **ChromaDB** for vector storage, and **HuggingFace embeddings** for semantic search – all wrapped in a **Streamlit** interface.

---

## 🚀 What This App Does

1. Upload a **PDF document**
2. Split it into **overlapping chunks**
3. Convert chunks to **embeddings** (vectors)
4. Store in a **vector database** (Chroma)
5. Answer user questions using:
   - Vector search to retrieve relevant chunks
   - A local **LLM (via Ollama)** for answer generation

---

## 🧰 Tools & Libraries Used

### 📝 1. `PyPDFLoader` (from `langchain_community.document_loaders`)
- Loads PDF pages as `Document` objects
- One object per page with `page_content`

### ✂️ 2. `RecursiveCharacterTextSplitter`
- Splits long documents into chunks (e.g., 500 characters)
- Tries to break first by paragraphs, then sentences, then words
- Allows **overlap** to preserve context between chunks

### 🔍 3. `HuggingFaceEmbeddings` (from `langchain_huggingface`)
- Converts text chunks into **dense vector embeddings**
- Uses `sentence-transformers/all-MiniLM-L6-v2`
- Supports **GPU acceleration** (`device='cuda'`)
- `encode_kwargs={'batch_size': 32}` for faster embedding

### 🧠 4. `Chroma` (from `langchain_community.vectorstores`)
- Lightweight, local **vector database**
- Stores text chunks + embeddings
- Allows fast **similarity search** for semantic retrieval

### 🦙 5. `Ollama`
- Runs **local LLMs** (e.g., Mistral, LLaMA2, Gemma)
- Used to generate answers to questions with retrieved context
- CLI-based: called via `subprocess.run(...)`

### 🌐 6. `Streamlit`
- Provides the **user interface**:
  - Upload PDF
  - Ask a question
  - View answer + retrieved context

---

## 💡 Why Use This Setup?

- ✅ 100% **local + private**
- ✅ No API keys or internet required
- ✅ Fast semantic search (via Chroma)
- ✅ GPU acceleration (embeddings + Ollama)
- ✅ Extendable: Chat memory, multiple docs, export, etc.

---

## 📄 Example Workflow

1. Upload `report.pdf`
2. Split into ~30 chunks of 500 characters each
3. Embed using HuggingFace model (GPU)
4. Store in Chroma
5. Ask: “What are the risks?”
6. Retrieve top 3 chunks from vector search
7. Pass chunks + question to `ollama run mistral`
8. Display answer and context

---

## ✅ Next Steps You Can Add

- 🔁 Multi-turn chat with memory
- 📁 Support for Notion, Markdown, etc.
- 💾 Persistent vector storage
- 🧠 Agent-based tools (e.g., summarizer, tagger)

---

## 🔗 Dependencies Summary

```bash
pip install streamlit langchain langchain-community langchain-huggingface chromadb sentence-transformers pypdf
