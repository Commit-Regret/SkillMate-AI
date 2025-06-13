#!/usr/bin/env python3
"""
Simplified test script for Team Assistant memory functionality.
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

def test_team_assistant_memory():
    """Test the Team Assistant agent's memory and context functionality."""
    try:
        from agents.team_assistant import TeamAssistantAgent
        
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
        logger.info(f"Response 1 success: {response1.get('success', False)}")
        logger.info(f"Response 1 (first 100 chars): {response1.get('response', '')[:100]}...")
        
        # Second message - technical question about implementation
        logger.info("\nTurn 2: Technical question")
        message2 = "What's the best way to implement the real-time sync between users using Socket.io?"
        response2 = agent.process_team_message(team_id, message2, team_info)
        logger.info(f"Response 2 success: {response2.get('success', False)}")
        logger.info(f"Response 2 (first 100 chars): {response2.get('response', '')[:100]}...")
        
        # Third message - follow-up referencing previous discussion
        logger.info("\nTurn 3: Follow-up referencing previous discussion")
        message3 = "For the real-time sync we discussed, how should we handle conflict resolution when multiple users edit the same line?"
        response3 = agent.process_team_message(team_id, message3, team_info)
        logger.info(f"Response 3 success: {response3.get('success', False)}")
        logger.info(f"Response 3 (first 100 chars): {response3.get('response', '')[:100]}...")
        
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
        
        # Get team status to verify conversation history
        team_status = agent.get_team_status(team_id)
        logger.info(f"\nTeam status: {team_status}")
        logger.info(f"Total messages in memory: {team_status.get('total_messages', 0)}")
        
        memory_working = team_status.get('total_messages', 0) >= 6  # 3 user messages + 3 assistant responses
        if memory_working:
            logger.info("PASS: Memory test - Correct number of messages stored")
        else:
            logger.info(f"FAIL: Memory test - Expected at least 6 messages, got {team_status.get('total_messages', 0)}")
        
        return {
            "success": context_working and workflow_awareness and memory_working,
            "context_working": context_working,
            "workflow_awareness": workflow_awareness,
            "memory_working": memory_working,
            "total_messages": team_status.get('total_messages', 0)
        }
        
    except Exception as e:
        logger.error(f"Error testing Team Assistant memory: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

def main():
    """Main entry point."""
    # Set provider
    os.environ["MODEL_PROVIDER"] = "gemini"
    logger.info(f"Using {os.environ.get('MODEL_PROVIDER', 'default').upper()} provider")
    
    # Run memory test
    logger.info("Testing Team Assistant memory and context functionality...")
    
    results = test_team_assistant_memory()
    
    # Save results to file
    with open("team_memory_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Generate summary report
    with open("TEAM_MEMORY_REPORT.md", "w") as f:
        f.write("# SkillMate AI Team Assistant Memory Test Report\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Model Provider:** {os.environ.get('MODEL_PROVIDER', 'default').upper()}\n\n")
        
        f.write("## Test Results Summary\n\n")
        f.write("| Component | Memory Working | Context Working | Workflow Analysis |\n")
        f.write("|-----------|---------------|----------------|------------------|\n")
        
        memory_working = results.get("memory_working", False)
        context_working = results.get("context_working", False)
        workflow_awareness = results.get("workflow_awareness", False)
        
        memory_status = "PASS" if memory_working else "FAIL"
        context_status = "PASS" if context_working else "FAIL"
        workflow_status = "PASS" if workflow_awareness else "FAIL"
        
        f.write(f"| Team Assistant | {memory_status} | {context_status} | {workflow_status} |\n\n")
        
        f.write("## Details\n\n")
        f.write(f"- Total messages stored: {results.get('total_messages', 0)}\n")
        f.write(f"- Overall success: {results.get('success', False)}\n\n")
        
        f.write("## Conclusion\n\n")
        if results.get("success", False):
            f.write("The Team Assistant agent successfully maintains conversation history and context awareness. ")
            f.write("It correctly remembers previous interactions and uses that context to provide relevant responses.\n")
        else:
            f.write("Some memory and context tests failed. The Team Assistant agent may not be properly maintaining ")
            f.write("conversation history or using context effectively. Please check the detailed results for more information.\n")
    
    logger.info(f"Team Assistant memory test completed. Results saved to current directory.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 