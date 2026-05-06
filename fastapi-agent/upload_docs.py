"""
One-time script: upload your documents to Pinecone.
Run:  python upload_docs.py
"""
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

# ── 1. Connect to Pinecone ─────────────────────────────────────────────────────
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index_name = os.environ["PINECONE_INDEX_NAME"]

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,             # text-embedding-3-small output size
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    print(f"Created Pinecone index: {index_name}")
else:
    print(f"Using existing Pinecone index: {index_name}")

# ── 2. Load your documents (put .txt files in ./docs/) ────────────────────────
loader = DirectoryLoader("./docs", glob="**/*.pdf", loader_cls=PyPDFLoader)
raw_docs = loader.load()
print(f"Loaded {len(raw_docs)} document(s).")

# ── 3. Split into chunks ───────────────────────────────────────────────────────
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(raw_docs)
print(f"Split into {len(chunks)} chunk(s).")

# ── 4. Embed & upsert ─────────────────────────────────────────────────────────
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
index = pc.Index(index_name)
vectorstore = PineconeVectorStore(index=index, embedding=embeddings)
vectorstore.add_documents(chunks)
print("Upload complete!")
