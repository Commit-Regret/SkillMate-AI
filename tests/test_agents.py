#!/usr/bin/env python3
"""
Test script for SkillMate AI agents.
Generates sample outputs from all agents for demonstration purposes.
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

def test_general_assistant():
    """Test the General Assistant agent."""
    try:
        from agents.general_assistant import GeneralAssistantAgent
        
        logger.info("Testing General Assistant Agent...")
        agent = GeneralAssistantAgent()
        
        # Test questions
        questions = [
            "What is SkillMate AI?",
            "How can I improve my Python programming skills?",
            "What are some good project ideas for a web developer?"
        ]
        
        results = []
        for question in questions:
            logger.info(f"Question: {question}")
            response = agent.generate_response("test_user", question)
            results.append({
                "question": question,
                "response": response
            })
            logger.info(f"Response length: {len(response)} characters")
        
        # Save results to file
        with open("general_assistant_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"General Assistant results saved to general_assistant_results.json")
        return results
        
    except Exception as e:
        logger.error(f"Error testing General Assistant: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_roadmap_generator():
    """Test the Roadmap Generator agent."""
    try:
        from agents.roadmap_generator import RoadmapGeneratorAgent
        
        logger.info("Testing Roadmap Generator Agent...")
        agent = RoadmapGeneratorAgent()
        
        # Test skills
        skills = [
            {"skill": "Python", "level": "beginner", "commitment": "moderate"},
            {"skill": "React", "level": "intermediate", "commitment": "high"},
            {"skill": "Machine Learning", "level": "beginner", "commitment": "low"}
        ]
        
        results = []
        for skill_info in skills:
            logger.info(f"Generating roadmap for {skill_info['skill']} ({skill_info['level']})...")
            result = agent.generate_roadmap(
                skill_info["skill"], 
                skill_info["level"], 
                skill_info["commitment"]
            )
            
            if result.get("success", False):
                results.append({
                    "skill": skill_info["skill"],
                    "level": skill_info["level"],
                    "commitment": skill_info["commitment"],
                    "roadmap": result.get("roadmap", "")
                })
                logger.info(f"Roadmap generated successfully ({len(result.get('roadmap', ''))} characters)")
            else:
                logger.error(f"Failed to generate roadmap: {result.get('error', 'Unknown error')}")
        
        # Save results to file
        with open("roadmap_generator_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Roadmap Generator results saved to roadmap_generator_results.json")
        return results
        
    except Exception as e:
        logger.error(f"Error testing Roadmap Generator: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_project_planner():
    """Test the Project Planner agent."""
    try:
        from agents.project_planner import ProjectPlannerAgent
        
        logger.info("Testing Project Planner Agent...")
        agent = ProjectPlannerAgent()
        
        # Test projects
        projects = [
            {
                "name": "E-commerce Website",
                "description": "Create a modern e-commerce platform with product listings, shopping cart, and checkout",
                "team_size": 4,
                "duration": "4 weeks"
            },
            {
                "name": "AI Chatbot",
                "description": "Build a chatbot using LangChain and OpenAI for customer support",
                "team_size": 2,
                "duration": "2 weeks"
            }
        ]
        
        results = []
        for project in projects:
            logger.info(f"Generating project plan for {project['name']}...")
            result = agent.create_project_plan(
                project["name"],
                project["description"],
                team_size=project["team_size"],
                duration=project["duration"]
            )
            
            if result.get("success", False):
                results.append({
                    "project_name": project["name"],
                    "description": project["description"],
                    "team_size": project["team_size"],
                    "duration": project["duration"],
                    "project_plan": result.get("project_plan", "")
                })
                logger.info(f"Project plan generated successfully ({len(result.get('project_plan', ''))} characters)")
            else:
                logger.error(f"Failed to generate project plan: {result.get('error', 'Unknown error')}")
        
        # Save results to file
        with open("project_planner_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Project Planner results saved to project_planner_results.json")
        return results
        
    except Exception as e:
        logger.error(f"Error testing Project Planner: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_smart_matcher():
    """Test the Smart Matcher agent."""
    try:
        from agents.smart_matcher import SmartMatcherAgent
        
        logger.info("Testing Smart Matcher Agent...")
        agent = SmartMatcherAgent()
        
        # Test user profiles
        target_user = {
            "user_id": "user1",
            "name": "Alice",
            "skills": ["Python", "React", "UI Design"],
            "interests": ["Web Development", "AI", "Mobile Apps"],
            "bio": "Full-stack developer interested in AI applications"
        }
        
        candidate_users = [
            {
                "user_id": "user2",
                "name": "Bob",
                "skills": ["JavaScript", "Node.js", "MongoDB"],
                "interests": ["Web Development", "Backend", "Databases"],
                "bio": "Backend specialist with 3 years experience"
            },
            {
                "user_id": "user3",
                "name": "Charlie",
                "skills": ["Python", "Django", "PostgreSQL"],
                "interests": ["AI", "Machine Learning", "Data Science"],
                "bio": "AI enthusiast with Python background"
            },
            {
                "user_id": "user4",
                "name": "Diana",
                "skills": ["UI/UX Design", "Figma", "HTML/CSS"],
                "interests": ["Design Systems", "User Research", "Mobile Apps"],
                "bio": "UI/UX designer focused on user-centered design"
            }
        ]
        
        logger.info(f"Finding matches for {target_user['name']}...")
        result = agent.find_matches(target_user, candidate_users)
        
        if result.get("success", False):
            matches = result.get("matches", [])
            logger.info(f"Found {len(matches)} matches")
            
            # Save results to file
            with open("smart_matcher_results.json", "w") as f:
                json.dump({
                    "target_user": target_user,
                    "candidate_users": candidate_users,
                    "matches": matches
                }, f, indent=2)
            
            logger.info(f"Smart Matcher results saved to smart_matcher_results.json")
            return matches
        else:
            logger.error(f"Failed to find matches: {result.get('error', 'Unknown error')}")
            return None
        
    except Exception as e:
        logger.error(f"Error testing Smart Matcher: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_team_assistant():
    """Test the Team Assistant agent."""
    try:
        from agents.team_assistant import TeamAssistantAgent
        
        logger.info("Testing Team Assistant Agent...")
        agent = TeamAssistantAgent()
        
        # Test team context
        team_context = {
            "team_id": "team123",
            "name": "Project Alpha",
            "project_goal": "Build a real-time collaboration platform for remote teams",
            "members": ["Alice", "Bob", "Charlie"],
            "tech_stack": ["React", "Node.js", "WebSocket", "MongoDB"]
        }
        
        # Test questions
        questions = [
            "How should we structure our sprint for the next 2 weeks?",
            "What's the best architecture for our real-time collaboration features?",
            "Can you help us identify potential risks in our project timeline?"
        ]
        
        results = []
        for question in questions:
            logger.info(f"Question: {question}")
            response = agent.process_team_message(
                team_id="team123",
                message=question,
                team_info=team_context
            )
            
            results.append({
                "question": question,
                "response": response
            })
            
            if response.get("success", False):
                ai_response = response.get("ai_response", "")
                logger.info(f"Response length: {len(ai_response)} characters")
            else:
                logger.error(f"Failed to generate response: {response.get('error', 'Unknown error')}")
        
        # Save results to file
        with open("team_assistant_results.json", "w") as f:
            json.dump({
                "team_context": team_context,
                "results": results
            }, f, indent=2)
        
        logger.info(f"Team Assistant results saved to team_assistant_results.json")
        return results
        
    except Exception as e:
        logger.error(f"Error testing Team Assistant: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main entry point."""
    # Set provider
    provider = os.getenv("MODEL_PROVIDER", "gemini")
    logger.info(f"Using {provider.upper()} provider")
    
    # Create results directory
    results_dir = f"agent_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(results_dir, exist_ok=True)
    os.chdir(results_dir)
    
    # Test all agents
    logger.info("Testing all agents...")
    
    test_general_assistant()
    test_roadmap_generator()
    test_project_planner()
    test_smart_matcher()
    test_team_assistant()
    
    logger.info(f"All agent tests completed. Results saved to {results_dir}/")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 