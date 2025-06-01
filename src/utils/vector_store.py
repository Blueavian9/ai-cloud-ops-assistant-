from typing import List
from pathlib import Path
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

class VectorStore:
    def __init__(self, openai_api_key: str):
        """Initialize the vector store with OpenAI embeddings."""
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=openai_api_key,
            model="text-embedding-ada-002"
        )
        self.vector_store = None

    def create_vector_store(self, documents: List[Document]) -> None:
        """Create a FAISS vector store from documents."""
        if not documents:
            raise ValueError("No documents provided to create vector store")
        
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
        print(f"✅ Created vector store with {len(documents)} documents")

    def save_vector_store(self, directory: str) -> None:
        """Save the vector store to disk."""
        if not self.vector_store:
            raise ValueError("No vector store to save")
        
        save_path = Path(directory)
        save_path.mkdir(parents=True, exist_ok=True)
        self.vector_store.save_local(str(save_path))
        print(f"✅ Saved vector store to {directory}")

    def load_vector_store(self, directory: str) -> None:
        """Load a vector store from disk."""
        load_path = Path(directory)
        if not load_path.exists():
            raise ValueError(f"Vector store directory {directory} does not exist")
        
        self.vector_store = FAISS.load_local(str(load_path), self.embeddings)
        print(f"✅ Loaded vector store from {directory}")

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Search for similar documents."""
        if not self.vector_store:
            raise ValueError("No vector store available for search")
        
        return self.vector_store.similarity_search(query, k=k) 