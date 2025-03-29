from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import subprocess

# Load & split PDF
docs = PyPDFLoader("BUILDINGLLMS.pdf").load()
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# Use new embeddings wrapper (with GPU + batching)
embedder = HuggingFaceEmbeddings(
    model_name='sentence-transformers/all-MiniLM-L6-v2',
    model_kwargs={'device': 'cuda'},
    encode_kwargs={'batch_size': 32}
)

# Vector store
db = Chroma.from_documents(chunks, embedding=embedder)

# RAG prompt
question = "What are the main risks mentioned in the document?"
results = db.similarity_search(question, k=3)
context = "\n\n".join([doc.page_content for doc in results])

rag_prompt = f"""Answer based on the context below.

Context:
{context}

Question:
{question}
"""

response = subprocess.run(["ollama", "run", "mistral"], input=rag_prompt.encode(), capture_output=True)
print(response.stdout.decode())
