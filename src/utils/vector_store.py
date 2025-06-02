from typing import List, Optional, Dict, Any, Tuple
from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
import json
from datetime import datetime
import numpy as np

class VectorStore:
    def __init__(self, openai_api_key: str):
        """Initialize the vector store with OpenAI embeddings.
        
        Args:
            openai_api_key (str): OpenAI API key for embeddings
        """
        self.embeddings = OpenAIEmbeddings(api_key=openai_api_key)
        self.vector_store = None
        self.metadata_file = "vector_store_metadata.json"

    def create_vector_store(self, documents: List[Document], directory: str = "vector_store", batch_size: int = 100) -> None:
        """Create and save a vector store from documents.
        
        Args:
            documents (List[Document]): List of documents to create vector store from
            directory (str): Directory to save vector store in
            batch_size (int): Number of documents to process at once
        """
        if not documents:
            raise ValueError("No documents provided to create vector store")
        
        # Process documents in batches
        total_docs = len(documents)
        print(f"Processing {total_docs} documents in batches of {batch_size}...")
        
        for i in range(0, total_docs, batch_size):
            batch = documents[i:i + batch_size]
            if i == 0:
                # Create new vector store for first batch
                self.vector_store = FAISS.from_documents(batch, self.embeddings)
            else:
                # Add to existing vector store for subsequent batches
                self.vector_store.add_documents(batch)
            print(f"Processed {min(i + batch_size, total_docs)}/{total_docs} documents")
        
        # Save vector store
        save_path = os.path.join(os.getcwd(), directory)
        os.makedirs(save_path, exist_ok=True)
        self.vector_store.save_local(save_path)
        
        # Save metadata
        metadata = {
            "created_at": datetime.now().isoformat(),
            "document_count": len(documents),
            "sources": list(set(doc.metadata.get("source", "unknown") for doc in documents)),
            "categories": list(set(doc.metadata.get("category", "unknown") for doc in documents)),
            "batch_size": batch_size
        }
        self._save_metadata(directory, metadata)
        
        print(f"✅ Saved vector store to {directory}")
        print(f"📊 Statistics:")
        print(f"   - Documents: {metadata['document_count']}")
        print(f"   - Sources: {', '.join(metadata['sources'])}")
        print(f"   - Categories: {', '.join(metadata['categories'])}")

    def load_vector_store(self, directory: str = "vector_store") -> None:
        """Load an existing vector store from directory.
        
        Args:
            directory (str): Directory containing the vector store
        """
        load_path = os.path.join(os.getcwd(), directory)
        if not os.path.exists(load_path):
            raise ValueError(f"Vector store directory {directory} does not exist")
        
        self.vector_store = FAISS.load_local(str(load_path), self.embeddings)
        
        # Load and display metadata
        metadata = self._load_metadata(directory)
        if metadata:
            print(f"✅ Loaded vector store from {directory}")
            print(f"📊 Statistics:")
            print(f"   - Documents: {metadata.get('document_count', 'unknown')}")
            print(f"   - Created: {metadata.get('created_at', 'unknown')}")
            print(f"   - Sources: {', '.join(metadata.get('sources', ['unknown']))}")
            print(f"   - Categories: {', '.join(metadata.get('categories', ['unknown']))}")

    def similarity_search(self, query: str, k: int = 4, score_threshold: float = 0.7) -> List[Tuple[Document, float]]:
        """Search for similar documents with similarity scores.
        
        Args:
            query (str): Query string to search for
            k (int): Number of results to return
            score_threshold (float): Minimum similarity score (0-1)
            
        Returns:
            List[Tuple[Document, float]]: List of (document, score) tuples
        """
        if not self.vector_store:
            raise ValueError("No vector store available for search")
        
        # Get documents and scores
        docs_and_scores = self.vector_store.similarity_search_with_score(query, k=k)
        
        # Filter by score threshold and sort by score
        filtered_results = [(doc, score) for doc, score in docs_and_scores if score >= score_threshold]
        filtered_results.sort(key=lambda x: x[1], reverse=True)
        
        return filtered_results

    def _save_metadata(self, directory: str, metadata: Dict[str, Any]) -> None:
        """Save metadata about the vector store.
        
        Args:
            directory (str): Directory to save metadata in
            metadata (Dict[str, Any]): Metadata to save
        """
        metadata_path = os.path.join(os.getcwd(), directory, self.metadata_file)
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

    def _load_metadata(self, directory: str) -> Optional[Dict[str, Any]]:
        """Load metadata about the vector store.
        
        Args:
            directory (str): Directory containing metadata
            
        Returns:
            Optional[Dict[str, Any]]: Loaded metadata or None if not found
        """
        metadata_path = os.path.join(os.getcwd(), directory, self.metadata_file)
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                return json.load(f)
        return None 