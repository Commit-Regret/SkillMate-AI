"""
Vector store management for SkillMate AI.

This module provides functionality for creating and managing vector stores.
"""

import os
import logging
from typing import List, Dict, Any, Optional, Union
import numpy as np

from langchain.vectorstores import FAISS, Chroma
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Set up logger
logger = logging.getLogger(__name__)

try:
    from ..config.settings import settings
    from ..config.model_provider import model_provider
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config.settings import settings
    from config.model_provider import model_provider


class VectorStoreManager:
    """Manager for vector stores."""
    
    def __init__(self):
        """Initialize the vector store manager."""
        self.provider = os.getenv("MODEL_PROVIDER", "openai").lower()
        self.embeddings = model_provider.create_embeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
        
        # Create store directories
        os.makedirs(settings.vector_db_path, exist_ok=True)
        
        # Store collections
        self.stores: Dict[str, Union[FAISS, Chroma]] = {}
    
    def create_faiss_store(self, texts, metadatas=None):
        """Create a FAISS vector store.
        
        Args:
            texts: List of texts to embed
            metadatas: Optional metadata for each text
            
        Returns:
            FAISS vector store
        """
        try:
            return FAISS.from_texts(texts, self.embeddings, metadatas=metadatas)
        except Exception as e:
            logger.error(f"Error creating FAISS store: {e}")
            return None
    
    def create_chroma_store(self, texts, metadatas=None, collection_name="skillmate"):
        """Create a Chroma vector store.
        
        Args:
            texts: List of texts to embed
            metadatas: Optional metadata for each text
            collection_name: Name of the collection
            
        Returns:
            Chroma vector store
        """
        try:
            return Chroma.from_texts(
                texts, 
                self.embeddings, 
                metadatas=metadatas, 
                collection_name=collection_name
            )
        except Exception as e:
            logger.error(f"Error creating Chroma store: {e}")
            return None
    
    def get_store(self, collection_name: str) -> Union[FAISS, Chroma]:
        """Get a vector store by collection name.
        
        Args:
            collection_name: Name of the vector store collection
            
        Returns:
            FAISS or Chroma vector store
        """
        if collection_name not in self.stores:
            persist_path = os.path.join(settings.vector_db_path, collection_name)
            
            if self.provider == "chroma":
                if os.path.exists(persist_path):
                    self.stores[collection_name] = Chroma(
                        persist_directory=persist_path,
                        embedding_function=self.embeddings
                    )
                else:
                    self.stores[collection_name] = Chroma(
                        persist_directory=persist_path,
                        embedding_function=self.embeddings
                    )
            else:  # Default to FAISS
                index_path = os.path.join(persist_path, "index.faiss")
                if os.path.exists(index_path):
                    try:
                        self.stores[collection_name] = FAISS.load_local(
                            persist_path,
                            self.embeddings,
                            allow_dangerous_deserialization=True
                        )
                    except Exception as e:
                        print(f"Error loading FAISS index for {collection_name}: {e}")
                        # Create new empty store if loading fails
                        os.makedirs(persist_path, exist_ok=True)
                        # Create with a dummy document to avoid empty index issues
                        dummy_doc = Document(
                            page_content="This is a placeholder document to initialize the vector store.",
                            metadata={"type": "placeholder", "collection": collection_name}
                        )
                        self.stores[collection_name] = FAISS.from_documents(
                            documents=[dummy_doc],
                            embedding=self.embeddings
                        )
                        self._save_store(collection_name)
                else:
                    os.makedirs(persist_path, exist_ok=True)
                    # Create with a dummy document to avoid empty index issues
                    dummy_doc = Document(
                        page_content="This is a placeholder document to initialize the vector store.",
                        metadata={"type": "placeholder", "collection": collection_name}
                    )
                    self.stores[collection_name] = FAISS.from_documents(
                        documents=[dummy_doc],
                        embedding=self.embeddings
                    )
                    self._save_store(collection_name)
        
        return self.stores[collection_name]
    
    def add_texts(self, collection_name: str, texts: List[str], metadatas: List[Dict[str, Any]] = None) -> List[str]:
        """Add texts to a vector store.
        
        Args:
            collection_name: Name of the vector store collection
            texts: List of text strings to add
            metadatas: Optional metadata for each text
            
        Returns:
            List of IDs for the added texts
        """
        store = self.get_store(collection_name)
        
        # Split texts into chunks if needed
        if len(texts) == 1 and len(texts[0]) > settings.chunk_size:
            documents = self.text_splitter.create_documents([texts[0]], [metadatas[0]] if metadatas else None)
            chunked_texts = [doc.page_content for doc in documents]
            chunked_metadatas = [doc.metadata for doc in documents] if metadatas else None
            
            ids = store.add_texts(chunked_texts, chunked_metadatas)
        else:
            ids = store.add_texts(texts, metadatas)
        
        self._save_store(collection_name)
        return ids
    
    def add_documents(self, collection_name: str, documents: List[Document]) -> List[str]:
        """Add documents to a vector store.
        
        Args:
            collection_name: Name of the vector store collection
            documents: List of Document objects to add
            
        Returns:
            List of IDs for the added documents
        """
        store = self.get_store(collection_name)
        
        # Split documents into chunks if needed
        chunked_documents = self.text_splitter.split_documents(documents)
        
        if self.provider == "chroma":
            ids = store.add_documents(chunked_documents)
        else:  # FAISS
            texts = [doc.page_content for doc in chunked_documents]
            metadatas = [doc.metadata for doc in chunked_documents]
            ids = store.add_texts(texts, metadatas)
        
        self._save_store(collection_name)
        return ids
    
    def similarity_search(self, collection_name: str, query: str, k: int = 4) -> List[Document]:
        """Search for similar documents in a vector store.
        
        Args:
            collection_name: Name of the vector store collection
            query: Query string
            k: Number of results to return
            
        Returns:
            List of Document objects
        """
        try:
            store = self.get_store(collection_name)
            results = store.similarity_search(query, k=k+5)  # Get extra to filter placeholders
            
            # Filter out placeholder documents
            filtered_results = [
                doc for doc in results 
                if doc.metadata.get("type") != "placeholder"
            ]
            
            # If no real documents found, return empty list
            if not filtered_results:
                return []
            
            return filtered_results[:k]
            
        except Exception as e:
            print(f"Error in similarity search for {collection_name}: {e}")
            return []
    
    def similarity_search_with_score(self, collection_name: str, query: str, k: int = 4) -> List[tuple]:
        """Search for similar documents in a vector store and return scores.
        
        Args:
            collection_name: Name of the vector store collection
            query: Query string
            k: Number of results to return
            
        Returns:
            List of tuples (Document, score)
        """
        store = self.get_store(collection_name)
        return store.similarity_search_with_score(query, k=k)
    
    def delete_collection(self, collection_name: str) -> bool:
        """Delete a vector store collection.
        
        Args:
            collection_name: Name of the vector store collection
            
        Returns:
            True if the collection was deleted, False otherwise
        """
        if collection_name in self.stores:
            del self.stores[collection_name]
            
        persist_path = os.path.join(settings.vector_db_path, collection_name)
        if os.path.exists(persist_path):
            import shutil
            shutil.rmtree(persist_path)
            return True
        
        return False
    
    def _save_store(self, collection_name: str) -> None:
        """Save a vector store to disk.
        
        Args:
            collection_name: Name of the vector store collection
        """
        if collection_name not in self.stores:
            return
        
        store = self.stores[collection_name]
        persist_path = os.path.join(settings.vector_db_path, collection_name)
        
        if self.provider == "chroma":
            if hasattr(store, "persist"):
                store.persist()
        else:  # FAISS
            os.makedirs(persist_path, exist_ok=True)
            store.save_local(persist_path) 