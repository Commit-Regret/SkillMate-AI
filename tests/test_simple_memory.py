#!/usr/bin/env python3
"""
Simple test script for memory functionality in SkillMate AI.
Uses direct LLM calls instead of complex workflows to verify memory works.
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, Any, List

# Add parent directory to path to import skillmate modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Import required modules
from skillmate.ai.memory.conversation_memory import ConversationMemoryManager
from skillmate.ai.schemas.message_schemas import MessageSchema
from skillmate.ai.config.model_provider import ModelProvider

class SimpleMemoryTest:
    """Simple class to test memory functionality."""
    
    def __init__(self):
        """Initialize the test class."""
        # Create model provider and LLM
        self.model_provider = ModelProvider()
        self.llm = self.model_provider.create_llm(
            model_type="general_assistant",
            temperature=0.7
        )
        
        # Create memory manager
        self.memory_manager = ConversationMemoryManager()
    
    def chat_with_memory(self, conversation_id: str, message: str) -> str:
        """Chat with memory functionality.
        
        Args:
            conversation_id: ID for the conversation
            message: User message
            
        Returns:
            Assistant response
        """
        # Get conversation history
        history = self.memory_manager.get_chat_history(conversation_id)
        history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history[-5:]])
        
        # Create prompt with history
        prompt = f"""You are a helpful AI assistant.

Conversation history:
{history_text}

User: {message}

Respond to the user's message, taking into account the conversation history.
"""
        
        # Get response
        response = self.llm.predict(prompt)
        
        # Save to memory
        user_message = MessageSchema(
            content=message,
            sender_id=conversation_id,
            role="user"
        )
        self.memory_manager.add_message(conversation_id, user_message)
        
        assistant_message = MessageSchema(
            content=response,
            sender_id="assistant",
            role="assistant"
        )
        self.memory_manager.add_message(conversation_id, assistant_message)
        
        return response
    
    def get_memory_status(self, conversation_id: str) -> Dict[str, Any]:
        """Get memory status.
        
        Args:
            conversation_id: ID for the conversation
            
        Returns:
            Memory status
        """
        messages = self.memory_manager.get_messages(conversation_id)
        
        return {
            "conversation_id": conversation_id,
            "total_messages": len(messages),
            "conversation_active": len(messages) > 0,
            "last_message": messages[-1].content if messages else None
        }

def test_simple_memory():
    """Test simple memory functionality."""
    try:
        logger.info("\n=== Testing Simple Memory ===\n")
        
        # Create test instance
        test = SimpleMemoryTest()
        
        # Create conversation
        conversation_id = "test_simple_memory"
        
        # First message - introduction
        logger.info("Turn 1: Introduction")
        message1 = "Hi, my name is Alex and I'm working on a project called SkillMate."
        response1 = test.chat_with_memory(conversation_id, message1)
        logger.info(f"Response: {response1[:100]}...")
        
        # Check memory status
        status1 = test.get_memory_status(conversation_id)
        logger.info(f"Memory status after turn 1: {status1}")
        
        # Second message - follow-up question that requires memory of the name and project
        logger.info("\nTurn 2: Follow-up requiring memory")
        message2 = "What's my name and what project am I working on?"
        response2 = test.chat_with_memory(conversation_id, message2)
        logger.info(f"Response: {response2[:100]}...")
        
        # Check memory status
        status2 = test.get_memory_status(conversation_id)
        logger.info(f"Memory status after turn 2: {status2}")
        
        # Third message - technical question
        logger.info("\nTurn 3: Technical question")
        message3 = "Can you explain what a memory manager is in the context of AI assistants?"
        response3 = test.chat_with_memory(conversation_id, message3)
        logger.info(f"Response: {response3[:100]}...")
        
        # Check memory status
        status3 = test.get_memory_status(conversation_id)
        logger.info(f"Memory status after turn 3: {status3}")
        
        # Fourth message - reference to previous explanation
        logger.info("\nTurn 4: Reference to previous explanation")
        message4 = "Based on what you just explained, how does that help maintain context in conversations?"
        response4 = test.chat_with_memory(conversation_id, message4)
        logger.info(f"Response: {response4[:100]}...")
        
        # Check memory status
        status4 = test.get_memory_status(conversation_id)
        logger.info(f"Memory status after turn 4: {status4}")
        
        # Check if memory is working by looking for references to previous information
        memory_working = False
        if ("Alex" in response2.lower() or "alex" in response2.lower()) and "skillmate" in response2.lower():
            logger.info("PASS: Memory test - Agent remembered user's name and project")
            memory_working = True
        else:
            logger.info("FAIL: Memory test - Agent did not remember user's name and project")
        
        context_working = False
        if "memory" in response4.lower() and "context" in response4.lower():
            logger.info("PASS: Context test - Agent remembered previous technical discussion")
            context_working = True
        else:
            logger.info("FAIL: Context test - Agent did not reference previous technical discussion")
        
        # Final memory status
        final_status = test.get_memory_status(conversation_id)
        logger.info(f"\nFinal memory status: {final_status}")
        
        return {
            "success": memory_working and context_working,
            "memory_working": memory_working,
            "context_working": context_working,
            "total_messages": final_status.get("total_messages", 0),
            "responses": [response1, response2, response3, response4]
        }
        
    except Exception as e:
        logger.error(f"Error testing simple memory: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

def main():
    """Main entry point."""
    # Set provider
    os.environ["MODEL_PROVIDER"] = "gemini"
    logger.info(f"Using {os.environ.get('MODEL_PROVIDER', 'default').upper()} provider")
    
    # Run memory test
    logger.info("Testing simple memory functionality...")
    
    results = test_simple_memory()
    
    # Save results to file
    with open("simple_memory_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    # Generate summary report
    with open("SIMPLE_MEMORY_REPORT.md", "w") as f:
        f.write("# SkillMate AI Simple Memory Test Report\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Model Provider:** {os.environ.get('MODEL_PROVIDER', 'default').upper()}\n\n")
        
        f.write("## Test Results Summary\n\n")
        f.write("| Test | Result |\n")
        f.write("|------|--------|\n")
        
        memory_working = results.get("memory_working", False)
        context_working = results.get("context_working", False)
        
        memory_status = "PASS" if memory_working else "FAIL"
        context_status = "PASS" if context_working else "FAIL"
        
        f.write(f"| Memory Test | {memory_status} |\n")
        f.write(f"| Context Test | {context_status} |\n\n")
        
        f.write("## Details\n\n")
        f.write(f"- Total messages stored: {results.get('total_messages', 0)}\n")
        f.write(f"- Overall success: {results.get('success', False)}\n\n")
        
        f.write("## Conclusion\n\n")
        if results.get("success", False):
            f.write("The memory system successfully maintains conversation history and context awareness. ")
            f.write("It correctly remembers previous interactions and uses that context to provide relevant responses.\n")
        else:
            f.write("Some memory and context tests failed. The memory system may not be properly maintaining ")
            f.write("conversation history or using context effectively. Please check the detailed results for more information.\n")
    
    logger.info(f"Simple memory test completed. Results saved to current directory.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 