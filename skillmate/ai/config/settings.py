"""
Configuration settings for the SkillMate AI system.
"""

import os
import logging
from dataclasses import dataclass
from typing import Optional, Literal
from pathlib import Path

# Set up logger
logger = logging.getLogger(__name__)

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv
    env_path = Path(".env")
    if env_path.exists():
        try:
            load_dotenv(env_path)
            logger.info(f"Loaded environment variables from {env_path}")
        except Exception as e:
            logger.warning(f"Error loading .env file: {e}")
            logger.warning("Using environment variables directly")
except ImportError:
    logger.warning("python-dotenv not installed, using environment variables directly")

# Define model provider types
ModelProvider = Literal["openai", "gemini"]

@dataclass
class Settings:
    """Configuration settings for the SkillMate AI system."""
    
    # Model provider settings
    model_provider: ModelProvider = os.getenv("MODEL_PROVIDER", "openai")
    
    # Vector database settings
    vector_db_type: str = os.getenv("VECTOR_DB_TYPE", "faiss")  # "faiss" or "chroma"
    vector_db_path: str = os.getenv("VECTOR_DB_PATH", "./vector_db")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    
    # Memory settings
    memory_type: str = os.getenv("MEMORY_TYPE", "conversation_buffer")
    memory_token_limit: int = int(os.getenv("MEMORY_TOKEN_LIMIT", "4000"))
    
    # Document processing settings
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1000"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    # Path settings
    resume_storage_path: str = os.getenv("RESUME_STORAGE_PATH", "./resume_storage")
    
    # Feature flags
    enable_roadmap_generator: bool = os.getenv("ENABLE_ROADMAP_GENERATOR", "True").lower() == "true"
    enable_project_planner: bool = os.getenv("ENABLE_PROJECT_PLANNER", "True").lower() == "true"
    enable_resume_qa: bool = os.getenv("ENABLE_RESUME_QA", "True").lower() == "true"
    enable_smart_matching: bool = os.getenv("ENABLE_SMART_MATCHING", "True").lower() == "true"
    
    def __post_init__(self):
        """Validate settings."""
        # Create directories if they don't exist
        os.makedirs(self.vector_db_path, exist_ok=True)
        os.makedirs(self.resume_storage_path, exist_ok=True)


# Create settings instance
settings = Settings() 