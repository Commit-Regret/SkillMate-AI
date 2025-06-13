#!/usr/bin/env python3
"""
Demo script for the SkillMate AI model provider system.
Shows how to use both OpenAI and Gemini models interchangeably.
"""

import os
import sys
import argparse
import logging
from typing import List

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Demo for SkillMate AI model provider system")
    parser.add_argument(
        "--provider", 
        choices=["openai", "gemini", "both"], 
        default="openai",
        help="Model provider to use (openai, gemini, or both)"
    )
    parser.add_argument(
        "--query",
        type=str,
        default="What is SkillMate AI?",
        help="Query to send to the model"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser.parse_args()

def test_llm(provider: str, query: str):
    """Test LLM with the specified provider.
    
    Args:
        provider: Model provider to use
        query: Query to send to the model
    """
    from config.model_provider import model_provider
    
    # Set provider
    model_provider.set_provider(provider)
    logger.info(f"Using {provider.upper()} provider")
    
    # Create LLM
    llm = model_provider.create_llm("general_assistant")
    logger.info(f"Created LLM with model: {model_provider.get_model_name('general_assistant')}")
    
    # Generate response
    logger.info(f"Query: {query}")
    response = llm.predict(query)
    
    # Print response
    print(f"\n=== {provider.upper()} RESPONSE ===\n")
    print(response)
    print("\n" + "=" * 50 + "\n")
    
    return response

def test_embeddings(provider: str, texts: List[str]):
    """Test embeddings with the specified provider.
    
    Args:
        provider: Model provider to use
        texts: List of texts to embed
    """
    from config.model_provider import model_provider, DummyEmbeddings
    
    # Set provider
    model_provider.set_provider(provider)
    logger.info(f"Using {provider.upper()} provider for embeddings")
    
    # Create embeddings
    embeddings = model_provider.create_embeddings()
    
    # Check if using dummy embeddings
    if isinstance(embeddings, DummyEmbeddings):
        logger.warning("Using DummyEmbeddings (no API keys available)")
    
    # Generate embeddings
    logger.info(f"Generating embeddings for {len(texts)} texts")
    vectors = embeddings.embed_documents(texts)
    
    # Print embedding info
    logger.info(f"Generated {len(vectors)} embeddings with dimension {len(vectors[0])}")
    
    return vectors

def main():
    """Main entry point."""
    args = parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Test texts for embeddings
    test_texts = [
        "SkillMate AI is a comprehensive AI-powered system for team formation.",
        "It provides intelligent features for team collaboration and project management.",
        "The system supports both OpenAI and Gemini models through a unified provider system."
    ]
    
    try:
        if args.provider == "both":
            # Test both providers
            openai_response = test_llm("openai", args.query)
            gemini_response = test_llm("gemini", args.query)
            
            # Compare responses
            print("\n=== RESPONSE COMPARISON ===\n")
            print(f"OpenAI length: {len(openai_response)} chars")
            print(f"Gemini length: {len(gemini_response)} chars")
            
            # Test embeddings with both providers
            logger.info("\nTesting embeddings...")
            openai_vectors = test_embeddings("openai", test_texts)
            gemini_vectors = test_embeddings("gemini", test_texts)
            
        else:
            # Test single provider
            test_llm(args.provider, args.query)
            
            # Test embeddings
            logger.info("\nTesting embeddings...")
            test_embeddings(args.provider, test_texts)
        
        return 0
        
    except Exception as e:
        logger.error(f"Error in demo: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main()) 