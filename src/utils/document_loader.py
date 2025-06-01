from typing import List
from pathlib import Path
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

class DocumentLoader:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """Initialize the document loader with chunking parameters."""
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )

    def load_pdfs(self, directory: str) -> List[Document]:
        """Load all PDFs from a directory and split them into chunks."""
        docs = []
        pdf_dir = Path(directory)
        
        # Load each PDF file
        for pdf_file in pdf_dir.glob("*.pdf"):
            try:
                loader = PyPDFLoader(str(pdf_file))
                docs.extend(loader.load())
                print(f"✅ Loaded {pdf_file.name}")
            except Exception as e:
                print(f"❌ Error loading {pdf_file.name}: {str(e)}")
        
        # Split documents into chunks
        if docs:
            chunks = self.text_splitter.split_documents(docs)
            print(f"📄 Split {len(docs)} documents into {len(chunks)} chunks")
            return chunks
        return [] 