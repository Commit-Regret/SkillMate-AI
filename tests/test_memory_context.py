#!/usr/bin/env python3
"""
Test script for memory and context functionality in SkillMate AI agents.
Focuses on verifying that agents maintain conversation history and context.
"""

import os
import sys
import json
import logging
from datetime import datetime

# Add parent directory to path to import skillmate modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def test_general_assistant_memory():
    """Test the General Assistant agent's memory functionality."""
    try:
        from skillmate.ai.agents.general_assistant import GeneralAssistantAgent
        
        logger.info("\n=== Testing General Assistant Memory ===\n")
        agent = GeneralAssistantAgent()
        
        # Create a conversation with multiple turns
        user_id = "test_user_memory"
        
        # First message - introduction
        logger.info("Turn 1: Introduction")
        response1 = agent.generate_response(user_id, "Hi, my name is Alex.")
        logger.info(f"Response: {response1[:100]}...")
        
        # Second message - follow-up question that requires memory of the name
        logger.info("\nTurn 2: Follow-up requiring memory")
        response2 = agent.generate_response(user_id, "What's my name?")
        logger.info(f"Response: {response2[:100]}...")
        
        # Third message - technical question
        logger.info("\nTurn 3: Technical question")
        response3 = agent.generate_response(user_id, "Can you explain what a binary search tree is?")
        logger.info(f"Response: {response3[:100]}...")
        
        # Fourth message - reference to previous explanation
        logger.info("\nTurn 4: Reference to previous explanation")
        response4 = agent.generate_response(user_id, "Can you give me an example of when I would use the data structure you just explained?")
        logger.info(f"Response: {response4[:100]}...")
        
        # Check if memory is working by looking for references to previous information
        memory_working = False
        if "Alex" in response2.lower() or "alex" in response2.lower():
            logger.info("PASS: Memory test - Agent remembered user's name")
            memory_working = True
        else:
            logger.info("FAIL: Memory test - Agent did not remember user's name")
        
        context_working = False
        if "binary" in response4.lower() or "tree" in response4.lower() or "search" in response4.lower():
            logger.info("PASS: Context test - Agent remembered previous technical discussion")
            context_working = True
        else:
            logger.info("FAIL: Context test - Agent did not reference previous technical discussion")
        
        return {
            "success": memory_working and context_working,
            "memory_working": memory_working,
            "context_working": context_working,
            "responses": [response1, response2, response3, response4]
        }
        
    except Exception as e:
        logger.error(f"Error testing General Assistant memory: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

def test_team_assistant_memory():
    """Test the Team Assistant agent's memory and context functionality."""
    try:
        from skillmate.ai.agents.team_assistant import TeamAssistantAgent
        
        logger.info("\n=== Testing Team Assistant Memory ===\n")
        agent = TeamAssistantAgent()
        
        # Create team context
        team_id = "test_team_memory"
        team_info = {
            "name": "Project Phoenix",
            "project_goal": "Build a real-time collaborative code editor with AI assistance",
            "members": ["Alex", "Jamie", "Taylor", "Morgan"],
            "tech_stack": ["React", "Node.js", "Socket.io", "MongoDB"],
            "current_sprint": "Sprint 2: Core Functionality"
        }
        
        # First message - task assignment
        logger.info("Turn 1: Task assignment")
        message1 = "We need to assign tasks for implementing the real-time collaboration feature. Who should work on what?"
        response1 = agent.process_team_message(team_id, message1, team_info)
        logger.info(f"Response: {response1.get('response', '')[:100]}...")
        
        # Second message - technical question about implementation
        logger.info("\nTurn 2: Technical question")
        message2 = "What's the best way to implement the real-time sync between users using Socket.io?"
        response2 = agent.process_team_message(team_id, message2, team_info)
        logger.info(f"Response: {response2.get('response', '')[:100]}...")
        
        # Third message - follow-up referencing previous discussion
        logger.info("\nTurn 3: Follow-up referencing previous discussion")
        message3 = "For the real-time sync we discussed, how should we handle conflict resolution when multiple users edit the same line?"
        response3 = agent.process_team_message(team_id, message3, team_info)
        logger.info(f"Response: {response3.get('response', '')[:100]}...")
        
        # Check if memory is working by looking for references to previous information
        context_working = False
        if ("socket" in response3.get('response', '').lower() or 
            "sync" in response3.get('response', '').lower() or 
            "real-time" in response3.get('response', '').lower()):
            logger.info("PASS: Context test - Agent remembered previous technical discussion")
            context_working = True
        else:
            logger.info("FAIL: Context test - Agent did not reference previous technical discussion")
        
        # Check workflow analysis for context awareness
        workflow_awareness = False
        if response3.get('workflow_analysis', {}).get('needs_technical_help', False):
            logger.info("PASS: Workflow analysis - Agent correctly identified technical context")
            workflow_awareness = True
        else:
            logger.info("FAIL: Workflow analysis - Agent did not identify technical context")
        
        return {
            "success": context_working and workflow_awareness,
            "context_working": context_working,
            "workflow_awareness": workflow_awareness,
            "responses": [
                response1.get('response', ''),
                response2.get('response', ''),
                response3.get('response', '')
            ],
            "workflow_analysis": [
                response1.get('workflow_analysis', {}),
                response2.get('workflow_analysis', {}),
                response3.get('workflow_analysis', {})
            ]
        }
        
    except Exception as e:
        logger.error(f"Error testing Team Assistant memory: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

def test_conversation_memory_manager():
    """Test the ConversationMemoryManager directly."""
    try:
        from skillmate.ai.memory.conversation_memory import ConversationMemoryManager
        from skillmate.ai.schemas.message_schemas import MessageSchema
        
        logger.info("\n=== Testing Conversation Memory Manager ===\n")
        
        memory_manager = ConversationMemoryManager()
        conversation_id = "test_conversation"
        
        # Add messages
        logger.info("Adding messages to memory")
        messages = [
            MessageSchema(content="Hello", sender_id="user1", role="user"),
            MessageSchema(content="Hi there! How can I help you?", sender_id="assistant", role="assistant"),
            MessageSchema(content="I need help with a project", sender_id="user1", role="user"),
            MessageSchema(content="Sure, what kind of project?", sender_id="assistant", role="assistant")
        ]
        
        for msg in messages:
            memory_manager.add_message(conversation_id, msg)
        
        # Retrieve messages
        logger.info("Retrieving conversation history")
        history = memory_manager.get_chat_history(conversation_id)
        retrieved_messages = memory_manager.get_messages(conversation_id)
        
        # Verify memory
        if len(history) == len(messages):
            logger.info(f"PASS: Memory test - Retrieved {len(history)} messages as expected")
            memory_working = True
        else:
            logger.info(f"FAIL: Memory test - Retrieved {len(history)} messages, expected {len(messages)}")
            memory_working = False
        
        # Verify message order
        order_correct = True
        for i, (orig, retrieved) in enumerate(zip(messages, retrieved_messages)):
            if orig.content != retrieved.content:
                logger.info(f"FAIL: Message order test at position {i}")
                order_correct = False
                break
        
        if order_correct:
            logger.info("PASS: Message order test - Messages retrieved in correct order")
        
        return {
            "success": memory_working and order_correct,
            "memory_working": memory_working,
            "order_correct": order_correct,
            "message_count": len(history)
        }
        
    except Exception as e:
        logger.error(f"Error testing Conversation Memory Manager: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

def main():
    """Main entry point."""
    # Set provider
    os.environ["MODEL_PROVIDER"] = "gemini"
    logger.info(f"Using {os.environ['MODEL_PROVIDER'].upper()} provider")
    
    # Create results directory
    results_dir = f"memory_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(results_dir, exist_ok=True)
    os.chdir(results_dir)
    
    # Run memory tests
    logger.info("Testing memory and context functionality...")
    
    results = {}
    
    # Test ConversationMemoryManager
    memory_manager_results = test_conversation_memory_manager()
    results["conversation_memory_manager"] = memory_manager_results
    
    # Test General Assistant memory
    general_assistant_results = test_general_assistant_memory()
    results["general_assistant"] = general_assistant_results
    
    # Test Team Assistant memory
    team_assistant_results = test_team_assistant_memory()
    results["team_assistant"] = team_assistant_results
    
    # Save results to file
    with open("memory_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Generate summary report
    with open("MEMORY_TEST_REPORT.md", "w") as f:
        f.write("# SkillMate AI Memory and Context Test Report\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Model Provider:** {os.environ['MODEL_PROVIDER'].upper()}\n\n")
        
        f.write("## Test Results Summary\n\n")
        f.write("| Component | Memory Working | Context Working |\n")
        f.write("|-----------|---------------|----------------|\n")
        
        general_memory = general_assistant_results.get("memory_working", False)
        general_context = general_assistant_results.get("context_working", False)
        f.write(f"| General Assistant | {'PASS' if general_memory else 'FAIL'} | {'PASS' if general_context else 'FAIL'} |\n")
        
        team_context = team_assistant_results.get("context_working", False)
        team_workflow = team_assistant_results.get("workflow_awareness", False)
        f.write(f"| Team Assistant | {'PASS' if team_context else 'FAIL'} | {'PASS' if team_workflow else 'FAIL'} |\n")
        
        memory_working = memory_manager_results.get("memory_working", False)
        order_correct = memory_manager_results.get("order_correct", False)
        f.write(f"| Memory Manager | {'PASS' if memory_working else 'FAIL'} | {'PASS' if order_correct else 'FAIL'} |\n\n")
        
        f.write("## Conclusion\n\n")
        all_passed = general_memory and general_context and team_context and team_workflow and memory_working and order_correct
        if all_passed:
            f.write("All memory and context tests passed successfully. The agents correctly maintain conversation history and context awareness.\n")
        else:
            f.write("Some memory and context tests failed. Please check the detailed results for more information.\n")
    
    logger.info(f"Memory tests completed. Results saved to {results_dir}/")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 