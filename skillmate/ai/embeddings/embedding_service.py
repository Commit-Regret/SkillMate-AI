"""
Embedding service for document processing and vector storage.
"""

import os
import tempfile
from typing import List, Dict, Any, Optional, BinaryIO, Union
import uuid

from langchain.docstore.document import Document
from langchain.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
    CSVLoader,
    UnstructuredHTMLLoader
)

from .vector_store import VectorStoreManager


class EmbeddingService:
    """Service for embedding documents and handling document operations."""
    
    def __init__(self, vector_store_manager: Optional[VectorStoreManager] = None):
        """Initialize the embedding service.
        
        Args:
            vector_store_manager: Optional VectorStoreManager instance
        """
        self.vector_store = vector_store_manager or VectorStoreManager()
    
    def process_file(self, file_path: str, user_id: str, metadata: Dict[str, Any] = None) -> List[str]:
        """Process a file and add it to the vector store.
        
        Args:
            file_path: Path to the file
            user_id: User ID
            metadata: Optional metadata
            
        Returns:
            List of document IDs
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Determine file type and load document
        ext = os.path.splitext(file_path)[1].lower()
        documents = self._load_documents(file_path, ext)
        
        # Add metadata
        base_metadata = metadata or {}
        base_metadata["user_id"] = user_id
        base_metadata["file_path"] = file_path
        base_metadata["file_type"] = ext
        
        for doc in documents:
            doc.metadata.update(base_metadata)
        
        # Add documents to vector store
        collection_name = f"users_{user_id}"
        return self.vector_store.add_documents(collection_name, documents)
    
    def process_file_stream(self, file_stream: BinaryIO, filename: str, user_id: str, 
                           metadata: Dict[str, Any] = None) -> List[str]:
        """Process a file stream and add it to the vector store.
        
        Args:
            file_stream: File-like object
            filename: Original filename
            user_id: User ID
            metadata: Optional metadata
            
        Returns:
            List of document IDs
        """
        # Create temporary file
        ext = os.path.splitext(filename)[1].lower()
        with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as temp_file:
            temp_path = temp_file.name
            file_stream.seek(0)
            temp_file.write(file_stream.read())
        
        try:
            # Process the temporary file
            return self.process_file(temp_path, user_id, metadata)
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def process_resume(self, file_path: str, user_id: str) -> List[str]:
        """Process a resume file and add it to the vector store.
        
        Args:
            file_path: Path to the resume file
            user_id: User ID
            
        Returns:
            List of document IDs
        """
        metadata = {
            "document_type": "resume",
            "user_id": user_id
        }
        
        collection_name = f"resumes_{user_id}"
        documents = self._load_documents(file_path, os.path.splitext(file_path)[1].lower())
        
        for doc in documents:
            doc.metadata.update(metadata)
        
        return self.vector_store.add_documents(collection_name, documents)
    
    def query_user_documents(self, user_id: str, query: str, k: int = 4) -> List[Document]:
        """Query documents for a user.
        
        Args:
            user_id: User ID
            query: Query string
            k: Number of results to return
            
        Returns:
            List of matching documents
        """
        collection_name = f"users_{user_id}"
        return self.vector_store.similarity_search(collection_name, query, k=k)
    
    def query_resume(self, user_id: str, query: str, k: int = 4) -> List[Document]:
        """Query a user's resume.
        
        Args:
            user_id: User ID
            query: Query string
            k: Number of results to return
            
        Returns:
            List of matching document sections
        """
        collection_name = f"resumes_{user_id}"
        return self.vector_store.similarity_search(collection_name, query, k=k)
    
    def create_user_embedding(self, user_id: str, text: str) -> List[float]:
        """Create an embedding for a user's text.
        
        Args:
            user_id: User ID
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        # Get embedding directly from the embedding model
        return self.vector_store.embeddings.embed_query(text)
    
    def find_similar_users(self, user_id: str, embedding: List[float], k: int = 5) -> List[Dict[str, Any]]:
        """Find users with similar embeddings.
        
        Args:
            user_id: Reference user ID
            embedding: Embedding vector
            k: Number of results to return
            
        Returns:
            List of similar users with scores
        """
        # This would require a special collection for user embeddings
        collection_name = "user_embeddings"
        
        # Convert embedding to Document format for FAISS
        query_embedding = embedding
        
        # This is a custom implementation as similarity_search expects a string query
        # For an actual implementation, you might use cosine similarity directly or 
        # store the embeddings in a database with vector search capabilities
        store = self.vector_store.get_store(collection_name)
        
        if hasattr(store, "index") and hasattr(store, "docstore"):  # FAISS
            # FAISS implementation
            scores, indices = store.index.search(
                self.vector_store.embeddings._normalize([query_embedding]), k + 1
            )
            
            results = []
            for i, idx in enumerate(indices[0]):
                if idx != -1:  # Valid index
                    doc_id = store.index_to_docstore_id[idx]
                    doc = store.docstore.search(doc_id)
                    
                    # Skip if this is the same user
                    if doc.metadata.get("user_id") == user_id:
                        continue
                    
                    results.append({
                        "user_id": doc.metadata.get("user_id"),
                        "score": float(scores[0][i]),
                        "metadata": doc.metadata
                    })
            
            return results[:k]  # Ensure we return at most k results
        
        # Fallback for other vector stores or when direct search isn't possible
        return []
    
    def _load_documents(self, file_path: str, ext: str) -> List[Document]:
        """Load documents from a file.
        
        Args:
            file_path: Path to the file
            ext: File extension
            
        Returns:
            List of documents
        """
        if ext in [".pdf"]:
            loader = PyPDFLoader(file_path)
        elif ext in [".docx", ".doc"]:
            loader = UnstructuredWordDocumentLoader(file_path)
        elif ext in [".txt", ".md"]:
            loader = TextLoader(file_path)
        elif ext in [".csv"]:
            loader = CSVLoader(file_path)
        elif ext in [".html", ".htm"]:
            loader = UnstructuredHTMLLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        
        return loader.load() 