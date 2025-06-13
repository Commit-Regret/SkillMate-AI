"""
Unified model provider and API key management for SkillMate AI.

This module provides a factory for creating LLM instances based on the configured provider
and handles API key rotation for both OpenAI and Gemini.
"""

import os
import json
import time
import random
import logging
import functools
from typing import Dict, Any, Optional, List, Callable, TypeVar, cast
from langchain.chat_models import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Set up logger
logger = logging.getLogger(__name__)

# Type variable for decorator
F = TypeVar('F', bound=Callable[..., Any])

class APIKeyManager:
    """Manages API keys for different providers and handles rotation."""
    
    def __init__(self, keys_file: str = "api_keys.json"):
        """Initialize the API key manager.
        
        Args:
            keys_file: Path to the JSON file containing API keys
        """
        self.keys_file = keys_file
        self.openai_keys: List[str] = []
        self.gemini_keys: List[str] = []
        self.current_openai_key_index = 0
        self.current_gemini_key_index = 0
        self.load_keys()
    
    def load_keys(self) -> None:
        """Load API keys from file and environment variables."""
        # Load from file if it exists
        if os.path.exists(self.keys_file):
            try:
                with open(self.keys_file, 'r') as f:
                    data = json.load(f)
                    self.openai_keys = data.get('openai_keys', [])
                    self.gemini_keys = data.get('gemini_keys', [])
                logger.info(f"Loaded {len(self.openai_keys)} OpenAI keys and {len(self.gemini_keys)} Gemini keys from {self.keys_file}")
            except Exception as e:
                logger.error(f"Error loading API keys from file: {e}")
        
        # Add environment variable keys if they exist and are not already in the lists
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and openai_key not in self.openai_keys:
            self.openai_keys.append(openai_key)
            logger.info("Added OpenAI API key from environment variable")
        
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key and gemini_key not in self.gemini_keys:
            self.gemini_keys.append(gemini_key)
            logger.info("Added Gemini API key from environment variable")
        
        # Initialize default Gemini keys if none exist
        if not self.gemini_keys:
            self._initialize_default_gemini_keys()
    
    def _initialize_default_gemini_keys(self) -> None:
        """Initialize default Gemini API keys."""
        # Default Gemini API keys
        default_gemini_keys = [
            "AIzaSyBQWxhgoL4h_zYDraa8YJ9qiKBFDOxJW0U",
            "AIzaSyC74TJjAZbPCON0bpctKb-_SUlhMOgI3HA",
            "AIzaSyBIQmQY8MRBek3PgRit0fPc_JoxvjXI2ME",
            "AIzaSyD5G5jKp1IYrT2pXypyI2biXR1P4CIFXaM",
            "AIzaSyB5lS_jcK2ZRpYzqYSo7FdJzNdwQcGb8BE"
        ]
        
        for key in default_gemini_keys:
            if key not in self.gemini_keys:
                self.gemini_keys.append(key)
        
        if self.gemini_keys:
            logger.info(f"Initialized {len(self.gemini_keys)} default Gemini API keys")
            self.save_keys()
    
    def save_keys(self) -> None:
        """Save API keys to file."""
        try:
            with open(self.keys_file, 'w') as f:
                json.dump({
                    'openai_keys': self.openai_keys,
                    'gemini_keys': self.gemini_keys
                }, f, indent=2)
            logger.info(f"Saved API keys to {self.keys_file}")
        except Exception as e:
            logger.error(f"Error saving API keys to file: {e}")
    
    def get_openai_key(self) -> Optional[str]:
        """Get the current OpenAI API key.
        
        Returns:
            Current OpenAI API key or None if no keys are available
        """
        if not self.openai_keys:
            return None
        
        return self.openai_keys[self.current_openai_key_index]
    
    def get_gemini_key(self) -> Optional[str]:
        """Get the current Gemini API key.
        
        Returns:
            Current Gemini API key or None if no keys are available
        """
        if not self.gemini_keys:
            return None
        
        return self.gemini_keys[self.current_gemini_key_index]
    
    def rotate_openai_key(self) -> Optional[str]:
        """Rotate to the next OpenAI API key.
        
        Returns:
            Next OpenAI API key or None if no keys are available
        """
        if not self.openai_keys:
            return None
        
        self.current_openai_key_index = (self.current_openai_key_index + 1) % len(self.openai_keys)
        logger.info(f"Rotated to OpenAI API key {self.current_openai_key_index + 1}/{len(self.openai_keys)}")
        return self.openai_keys[self.current_openai_key_index]
    
    def rotate_gemini_key(self) -> Optional[str]:
        """Rotate to the next Gemini API key.
        
        Returns:
            Next Gemini API key or None if no keys are available
        """
        if not self.gemini_keys:
            return None
        
        self.current_gemini_key_index = (self.current_gemini_key_index + 1) % len(self.gemini_keys)
        logger.info(f"Rotated to Gemini API key {self.current_gemini_key_index + 1}/{len(self.gemini_keys)}")
        return self.gemini_keys[self.current_gemini_key_index]
    
    def add_openai_key(self, key: str) -> bool:
        """Add an OpenAI API key.
        
        Args:
            key: OpenAI API key to add
            
        Returns:
            True if key was added, False if it already exists
        """
        if key in self.openai_keys:
            return False
        
        self.openai_keys.append(key)
        self.save_keys()
        return True
    
    def add_gemini_key(self, key: str) -> bool:
        """Add a Gemini API key.
        
        Args:
            key: Gemini API key to add
            
        Returns:
            True if key was added, False if it already exists
        """
        if key in self.gemini_keys:
            return False
        
        self.gemini_keys.append(key)
        self.save_keys()
        return True
    
    def remove_openai_key(self, key: str) -> bool:
        """Remove an OpenAI API key.
        
        Args:
            key: OpenAI API key to remove
            
        Returns:
            True if key was removed, False if it doesn't exist
        """
        if key not in self.openai_keys:
            return False
        
        self.openai_keys.remove(key)
        self.save_keys()
        return True
    
    def remove_gemini_key(self, key: str) -> bool:
        """Remove a Gemini API key.
        
        Args:
            key: Gemini API key to remove
            
        Returns:
            True if key was removed, False if it doesn't exist
        """
        if key not in self.gemini_keys:
            return False
        
        self.gemini_keys.remove(key)
        self.save_keys()
        return True


def with_api_key_rotation(func: Optional[F] = None, *, max_retries: int = 3, retry_delay: float = 1.0) -> Callable:
    """Decorator to handle API key rotation on quota errors.
    
    Args:
        func: Function to decorate
        max_retries: Maximum number of retries
        retry_delay: Delay between retries in seconds
        
    Returns:
        Decorated function
    """
    def decorator(f: F) -> F:
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            retries = 0
            last_error = None
            
            while retries <= max_retries:
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    error_str = str(e).lower()
                    last_error = e
                    
                    # Check if this is a quota error
                    if any(err in error_str for err in ["quota", "rate_limit", "429", "limit exceeded"]):
                        retries += 1
                        
                        if retries <= max_retries:
                            # Rotate API key based on provider
                            provider = os.getenv("MODEL_PROVIDER", "openai").lower()
                            
                            if provider == "openai":
                                new_key = key_manager.rotate_openai_key()
                                if new_key:
                                    os.environ["OPENAI_API_KEY"] = new_key
                                    logger.info(f"Rotated to new OpenAI API key (retry {retries}/{max_retries})")
                                else:
                                    logger.warning("No more OpenAI API keys available for rotation")
                            elif provider == "gemini":
                                new_key = key_manager.rotate_gemini_key()
                                if new_key:
                                    os.environ["GEMINI_API_KEY"] = new_key
                                    logger.info(f"Rotated to new Gemini API key (retry {retries}/{max_retries})")
                                else:
                                    logger.warning("No more Gemini API keys available for rotation")
                            
                            # Add jitter to retry delay
                            jitter = random.uniform(0.1, 0.5)
                            time.sleep(retry_delay + jitter)
                            continue
                    
                    # If not a quota error or max retries reached, re-raise
                    raise
            
            # If we get here, we've exhausted all retries
            if last_error:
                raise last_error
            else:
                raise RuntimeError("Failed after multiple retries")
        
        return cast(F, wrapper)
    
    if func is None:
        return decorator
    else:
        return decorator(func)


class DummyEmbeddings:
    """Dummy embeddings class for when no API keys are available."""
    
    def embed_documents(self, texts):
        """Return dummy embeddings for documents.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of dummy embeddings
        """
        # Return a list of 1536-dimensional embeddings (same as OpenAI)
        return [[0.0] * 1536 for _ in texts]
    
    def embed_query(self, text):
        """Return dummy embedding for query.
        
        Args:
            text: Text to embed
            
        Returns:
            Dummy embedding
        """
        # Return a 1536-dimensional embedding (same as OpenAI)
        return [0.0] * 1536


class ModelProvider:
    """Factory for creating LLM instances based on the configured provider."""
    
    def __init__(self):
        """Initialize the model provider."""
        self.provider = os.getenv("MODEL_PROVIDER", "openai").lower()
        
        # Model mappings
        self.openai_models = {
            "general_assistant": os.getenv("GENERAL_ASSISTANT_MODEL", "gpt-3.5-turbo"),
            "team_assistant": os.getenv("TEAM_ASSISTANT_MODEL", "gpt-3.5-turbo"),
            "planner": os.getenv("PLANNER_MODEL", "gpt-3.5-turbo"),
            "matcher": os.getenv("MATCHER_MODEL", "gpt-3.5-turbo")
        }
        
        self.gemini_models = {
            "general_assistant": os.getenv("GEMINI_GENERAL_MODEL", "gemini-1.5-flash"),
            "team_assistant": os.getenv("GEMINI_TEAM_MODEL", "gemini-1.5-flash"),
            "planner": os.getenv("GEMINI_PLANNER_MODEL", "gemini-1.5-flash"),
            "matcher": os.getenv("GEMINI_MATCHER_MODEL", "gemini-1.5-flash")
        }
    
    def create_llm(self, model_type: str, temperature: float = 0.7) -> Any:
        """Create an LLM instance based on the configured provider.
        
        Args:
            model_type: Type of model to create (general_assistant, team_assistant, etc.)
            temperature: Temperature parameter for the model
            
        Returns:
            LLM instance
        """
        if self.provider == "gemini":
            return self._create_gemini_llm(model_type, temperature)
        else:
            return self._create_openai_llm(model_type, temperature)
    
    def _create_openai_llm(self, model_type: str, temperature: float) -> ChatOpenAI:
        """Create an OpenAI LLM instance.
        
        Args:
            model_type: Type of model to create
            temperature: Temperature parameter for the model
            
        Returns:
            ChatOpenAI instance
        """
        api_key = key_manager.get_openai_key()
        if not api_key:
            # If no OpenAI key is available, fall back to Gemini
            logger.warning("No OpenAI API key available, falling back to Gemini")
            self.provider = "gemini"
            return self._create_gemini_llm(model_type, temperature)
        
        model_name = self.openai_models.get(model_type, "gpt-3.5-turbo")
        
        return ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            openai_api_key=api_key
        )
    
    def _create_gemini_llm(self, model_type: str, temperature: float) -> ChatGoogleGenerativeAI:
        """Create a Gemini LLM instance.
        
        Args:
            model_type: Type of model to create
            temperature: Temperature parameter for the model
            
        Returns:
            ChatGoogleGenerativeAI instance
        """
        api_key = key_manager.get_gemini_key()
        if not api_key:
            # If no Gemini key is available, try to initialize default keys
            key_manager._initialize_default_gemini_keys()
            api_key = key_manager.get_gemini_key()
            
            if not api_key:
                raise ValueError("No Gemini API key available")
        
        model_name = self.gemini_models.get(model_type, "gemini-1.5-flash")
        
        return ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            google_api_key=api_key
        )
    
    def create_embeddings(self):
        """Create an embeddings model based on the configured provider.
        
        Returns:
            Embeddings model (OpenAIEmbeddings, GoogleGenerativeAIEmbeddings, or DummyEmbeddings)
        """
        if self.provider == "gemini":
            try:
                api_key = key_manager.get_gemini_key()
                if not api_key:
                    # If no Gemini key is available, try to initialize default keys
                    key_manager._initialize_default_gemini_keys()
                    api_key = key_manager.get_gemini_key()
                
                if api_key:
                    logger.info("Using Gemini embeddings")
                    return GoogleGenerativeAIEmbeddings(
                        model="models/embedding-001",
                        google_api_key=api_key
                    )
                else:
                    logger.warning("No Gemini API key available for embeddings, falling back to OpenAI")
            except Exception as e:
                logger.error(f"Error creating Gemini embeddings: {e}")
                logger.warning("Falling back to OpenAI embeddings")
        
        # Default to OpenAI
        try:
            api_key = key_manager.get_openai_key()
            if api_key:
                embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
                logger.info(f"Using OpenAI embeddings model: {embedding_model}")
                return OpenAIEmbeddings(
                    model=embedding_model,
                    openai_api_key=api_key
                )
            else:
                # Use a dummy embeddings model if no API keys are available
                logger.warning("No API keys available for embeddings, using dummy embeddings")
                return DummyEmbeddings()
        except Exception as e:
            logger.error(f"Error creating OpenAI embeddings: {e}")
            logger.warning("Using dummy embeddings")
            return DummyEmbeddings()
    
    def get_provider(self) -> str:
        """Get the current provider.
        
        Returns:
            Current provider name
        """
        return self.provider
    
    def set_provider(self, provider: str) -> None:
        """Set the provider.
        
        Args:
            provider: Provider name (openai or gemini)
        """
        if provider.lower() not in ["openai", "gemini"]:
            raise ValueError("Invalid provider. Must be 'openai' or 'gemini'")
        
        self.provider = provider.lower()
        os.environ["MODEL_PROVIDER"] = self.provider
    
    def get_model_name(self, model_type: str) -> str:
        """Get the model name for the current provider and model type.
        
        Args:
            model_type: Type of model
            
        Returns:
            Model name
        """
        if self.provider == "gemini":
            return self.gemini_models.get(model_type, "gemini-1.5-flash")
        else:
            return self.openai_models.get(model_type, "gpt-3.5-turbo")


# Create global instances
key_manager = APIKeyManager()
model_provider = ModelProvider() 