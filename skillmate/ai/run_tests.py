#!/usr/bin/env python3
"""
Unified test script for SkillMate AI system.
Tests the system with either OpenAI or Gemini models.
"""

import os
import sys
import time
import json
import argparse
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("test_results.log")
    ]
)
logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run tests for SkillMate AI system")
    parser.add_argument(
        "--provider", 
        choices=["openai", "gemini", "both"], 
        default="openai",
        help="Model provider to use (openai, gemini, or both)"
    )
    parser.add_argument(
        "--tests", 
        choices=["general", "roadmap", "planner", "matcher", "provider", "all"], 
        default="all",
        help="Tests to run (provider tests the model provider system specifically)"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--api-key", 
        type=str,
        help="API key to use (will be set as environment variable)"
    )
    parser.add_argument(
        "--keys-file",
        type=str,
        default="api_keys.json",
        help="Path to API keys JSON file"
    )
    
    return parser.parse_args()

def setup_environment(args):
    """Set up the environment for testing.
    
    Args:
        args: Command line arguments
    """
    # Set model provider
    if args.provider != "both":
        os.environ["MODEL_PROVIDER"] = args.provider
        logger.info(f"Using model provider: {args.provider}")
    else:
        logger.info("Testing with both OpenAI and Gemini providers")
    
    # Set API key if provided
    if args.api_key:
        if args.provider == "openai":
            os.environ["OPENAI_API_KEY"] = args.api_key
            logger.info("Using provided OpenAI API key")
        elif args.provider == "gemini":
            os.environ["GEMINI_API_KEY"] = args.api_key
            logger.info("Using provided Gemini API key")
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.info("Verbose logging enabled")

def test_model_provider():
    """Test the model provider system."""
    try:
        from skillmate.ai.config.model_provider import model_provider, key_manager, DummyEmbeddings
        
        logger.info("Testing model provider system...")
        
        # Test provider switching
        original_provider = model_provider.get_provider()
        logger.info(f"Current provider: {original_provider}")
        
        # Test switching to the other provider
        new_provider = "gemini" if original_provider == "openai" else "openai"
        model_provider.set_provider(new_provider)
        current_provider = model_provider.get_provider()
        
        if current_provider == new_provider:
            logger.info(f"✅ Successfully switched provider to {new_provider}")
        else:
            logger.error(f"❌ Failed to switch provider to {new_provider}")
        
        # Test LLM creation
        try:
            llm = model_provider.create_llm("general_assistant")
            logger.info(f"✅ Successfully created LLM with {current_provider} provider")
            
            # Test simple prediction
            response = llm.predict("Hello, what is SkillMate AI?")
            if response and len(response) > 20:
                logger.info("✅ LLM prediction successful")
            else:
                logger.error("❌ LLM prediction failed or returned short response")
                
        except Exception as e:
            logger.error(f"❌ Failed to create LLM: {e}")
        
        # Test embeddings creation
        try:
            embeddings = model_provider.create_embeddings()
            
            if isinstance(embeddings, DummyEmbeddings):
                logger.warning("⚠️ Using DummyEmbeddings (no API keys available)")
            else:
                logger.info(f"✅ Successfully created embeddings with {current_provider} provider")
            
            # Test embedding functionality
            test_text = "This is a test document for embedding."
            embedding = embeddings.embed_query(test_text)
            
            if embedding and len(embedding) > 0:
                logger.info(f"✅ Embedding generation successful (dimension: {len(embedding)})")
            else:
                logger.error("❌ Embedding generation failed")
                
        except Exception as e:
            logger.error(f"❌ Failed to create embeddings: {e}")
        
        # Test API key management
        try:
            # Get current key counts
            openai_key_count = len(key_manager.openai_keys)
            gemini_key_count = len(key_manager.gemini_keys)
            
            logger.info(f"Current API keys: OpenAI ({openai_key_count}), Gemini ({gemini_key_count})")
            
            # Test key rotation
            if openai_key_count > 1:
                original_key = key_manager.get_openai_key()
                rotated_key = key_manager.rotate_openai_key()
                
                if original_key != rotated_key:
                    logger.info("✅ OpenAI key rotation successful")
                else:
                    logger.error("❌ OpenAI key rotation failed")
            
            if gemini_key_count > 1:
                original_key = key_manager.get_gemini_key()
                rotated_key = key_manager.rotate_gemini_key()
                
                if original_key != rotated_key:
                    logger.info("✅ Gemini key rotation successful")
                else:
                    logger.error("❌ Gemini key rotation failed")
                
        except Exception as e:
            logger.error(f"❌ Failed to test API key management: {e}")
        
        # Restore original provider
        model_provider.set_provider(original_provider)
        logger.info(f"Restored original provider: {original_provider}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error testing model provider: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_tests(args):
    """Run the specified tests.
    
    Args:
        args: Command line arguments
    """
    try:
        # Import the test module after setting environment variables
        from skillmate.ai.test_skillmate_system import SkillMateAITester
        
        # If testing both providers, run tests for each
        providers = ["openai", "gemini"] if args.provider == "both" else [args.provider]
        
        for provider in providers:
            if args.provider == "both":
                os.environ["MODEL_PROVIDER"] = provider
                logger.info(f"\n=== Running tests with {provider.upper()} provider ===\n")
            
            # Test model provider system specifically
            if args.tests == "provider" or args.tests == "all":
                logger.info(f"Testing model provider system with {provider} provider")
                test_model_provider()
            
            # Create tester instance
            tester = SkillMateAITester()
            
            if args.tests == "general" or args.tests == "all":
                logger.info(f"Running general assistant tests with {provider} provider")
                tester.test_general_assistant()
            
            if args.tests == "roadmap" or args.tests == "all":
                logger.info(f"Running roadmap generator tests with {provider} provider")
                tester.test_roadmap_generator()
            
            if args.tests == "planner" or args.tests == "all":
                logger.info(f"Running project planner tests with {provider} provider")
                tester.test_project_planner()
            
            if args.tests == "matcher" or args.tests == "all":
                logger.info(f"Running smart matcher tests with {provider} provider")
                tester.test_smart_matcher()
            
        logger.info("All tests completed")
        return True
        
    except Exception as e:
        logger.error(f"Error running tests: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main entry point."""
    args = parse_args()
    setup_environment(args)
    
    start_time = time.time()
    success = run_tests(args)
    end_time = time.time()
    
    duration = end_time - start_time
    logger.info(f"Test run completed in {duration:.2f} seconds")
    
    if success:
        logger.info("All tests passed")
        return 0
    else:
        logger.error("Tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 