#!/usr/bin/env python3
"""
Test runner for SkillMate AI system.
"""

import os
import sys
import importlib
import time
import logging
from datetime import datetime

# Add parent directory to path to import skillmate modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('test_results.log')
    ]
)
logger = logging.getLogger(__name__)

def run_tests():
    """Run all tests for the SkillMate AI system."""
    start_time = time.time()
    
    logger.info("🚀 Running all tests...")
    
    # Test modules to run
    test_modules = [
        "tests.test_skillmate_system",
        "tests.test_memory_context",
        "tests.test_team_memory",
        "tests.test_simple_memory"
    ]
    
    success_count = 0
    failure_count = 0
    
    for module_name in test_modules:
        try:
            logger.info(f"Running {module_name}...")
            module = importlib.import_module(module_name)
            if hasattr(module, "main"):
                module.main()
                success_count += 1
            else:
                logger.warning(f"No main() function found in {module_name}")
                failure_count += 1
        except Exception as e:
            logger.error(f"Error running {module_name}: {str(e)}")
            failure_count += 1
    
    end_time = time.time()
    duration = end_time - start_time
    
    logger.info("\n============================================================")
    logger.info("TEST SUMMARY REPORT")
    logger.info("============================================================")
    logger.info(f"Total Tests: {success_count + failure_count}")
    logger.info(f"Passed: {success_count}")
    logger.info(f"Failed: {failure_count}")
    
    if success_count + failure_count > 0:
        success_rate = (success_count / (success_count + failure_count)) * 100
        logger.info(f"Success Rate: {success_rate:.1f}%")
    
    logger.info(f"Total Duration: {duration:.2f}s")
    
    return success_count, failure_count

if __name__ == "__main__":
    run_tests() 