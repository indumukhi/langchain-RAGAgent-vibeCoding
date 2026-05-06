from langchain.tools import tool
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
import os


def build_retriever():
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    index = pc.Index(os.environ["PINECONE_INDEX_NAME"])
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = PineconeVectorStore(index=index, embedding=embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 4})


# Built once and reused across all agent calls
_retriever = None


def get_retriever():
    global _retriever
    if _retriever is None:
        _retriever = build_retriever()
    return _retriever


@tool
def internal_document_search(query: str) -> str:
    """Search internal company documents for relevant information.
    Use this for questions about policies, procedures, products, or any company-specific topic.
    Input should be a natural language search query.
    """
    retriever = get_retriever()
    docs = retriever.invoke(query)
    if not docs:
        return "No relevant documents found in the knowledge base."
    parts = [f"[Document {i + 1}]:\n{doc.page_content}" for i, doc in enumerate(docs)]
    return "\n\n---\n\n".join(parts)
