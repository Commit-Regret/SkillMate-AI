#!/usr/bin/env python3
"""
SkillMate AI Demo - Demonstrates all system features in one script.
"""

import os
import sys
import json
import logging
from datetime import datetime
import time

# Add parent directory to path to import skillmate modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def setup_environment():
    """Set up the environment for the demo."""
    # Default to Gemini provider
    os.environ["MODEL_PROVIDER"] = "gemini"
    logger.info(f"Using model provider: {os.environ.get('MODEL_PROVIDER', 'gemini').upper()}")
    
    # Create results directory
    results_dir = f"demo_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(results_dir, exist_ok=True)
    os.chdir(results_dir)
    logger.info(f"Results will be saved to {results_dir}/")
    
    return results_dir

def demo_general_assistant():
    """Demonstrate the General Assistant agent."""
    try:
        from agents.general_assistant import GeneralAssistantAgent
        
        logger.info("\n=== DEMO: General Assistant ===\n")
        agent = GeneralAssistantAgent()
        
        # Demo questions
        questions = [
            "What is SkillMate AI?",
            "How can I prepare for a technical interview?",
            "What are some trending technologies in 2025?"
        ]
        
        results = []
        for question in questions:
            logger.info(f"Question: {question}")
            start_time = time.time()
            response = agent.generate_response("demo_user", question)
            end_time = time.time()
            
            results.append({
                "question": question,
                "response": response,
                "time_taken": f"{end_time - start_time:.2f} seconds"
            })
            
            logger.info(f"Response: {response[:100]}...")
            logger.info(f"Time taken: {end_time - start_time:.2f} seconds")
            logger.info("---")
        
        # Save results to file
        with open("general_assistant_demo.json", "w") as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"General Assistant results saved to general_assistant_demo.json")
        return results
        
    except Exception as e:
        logger.error(f"Error demonstrating General Assistant: {e}")
        import traceback
        traceback.print_exc()
        return None

def demo_roadmap_generator():
    """Demonstrate the Roadmap Generator agent."""
    try:
        from agents.roadmap_generator import RoadmapGeneratorAgent
        
        logger.info("\n=== DEMO: Roadmap Generator ===\n")
        agent = RoadmapGeneratorAgent()
        
        # Demo skills
        skills = [
            {"skill": "Data Science", "level": "beginner", "commitment": "moderate"},
            {"skill": "DevOps", "level": "intermediate", "commitment": "high"}
        ]
        
        results = []
        for skill_info in skills:
            logger.info(f"Generating roadmap for {skill_info['skill']} ({skill_info['level']})...")
            start_time = time.time()
            result = agent.generate_roadmap(
                skill_info["skill"], 
                skill_info["level"], 
                skill_info["commitment"]
            )
            end_time = time.time()
            
            if result.get("success", False):
                roadmap = result.get("roadmap", "")
                results.append({
                    "skill": skill_info["skill"],
                    "level": skill_info["level"],
                    "commitment": skill_info["commitment"],
                    "roadmap": roadmap,
                    "time_taken": f"{end_time - start_time:.2f} seconds"
                })
                
                logger.info(f"Roadmap generated successfully ({len(roadmap)} characters)")
                logger.info(f"Time taken: {end_time - start_time:.2f} seconds")
                logger.info(f"First 100 characters: {roadmap[:100]}...")
            else:
                logger.error(f"Failed to generate roadmap: {result.get('error', 'Unknown error')}")
                
            logger.info("---")
        
        # Save results to file
        with open("roadmap_generator_demo.json", "w") as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Roadmap Generator results saved to roadmap_generator_demo.json")
        return results
        
    except Exception as e:
        logger.error(f"Error demonstrating Roadmap Generator: {e}")
        import traceback
        traceback.print_exc()
        return None

def demo_project_planner():
    """Demonstrate the Project Planner agent."""
    try:
        from agents.project_planner import ProjectPlannerAgent
        
        logger.info("\n=== DEMO: Project Planner ===\n")
        agent = ProjectPlannerAgent()
        
        # Demo projects
        projects = [
            {
                "name": "Mobile Health App",
                "description": "Create a mobile application for health tracking, including exercise monitoring, nutrition logging, and wellness tips",
                "team_size": 3,
                "duration": "3 weeks"
            }
        ]
        
        results = []
        for project in projects:
            logger.info(f"Generating project plan for {project['name']}...")
            start_time = time.time()
            result = agent.create_project_plan(
                project["name"],
                project["description"],
                team_size=project["team_size"],
                duration=project["duration"]
            )
            end_time = time.time()
            
            if result.get("success", False):
                plan = result.get("project_plan", "")
                results.append({
                    "project_name": project["name"],
                    "description": project["description"],
                    "team_size": project["team_size"],
                    "duration": project["duration"],
                    "project_plan": plan,
                    "time_taken": f"{end_time - start_time:.2f} seconds"
                })
                
                logger.info(f"Project plan generated successfully ({len(plan)} characters)")
                logger.info(f"Time taken: {end_time - start_time:.2f} seconds")
                
                # Extract and display key sections
                if isinstance(plan, dict):
                    logger.info(f"Plan includes {len(plan.get('sprints', []))} sprints")
                    logger.info(f"Plan includes {len(plan.get('risks', []))} identified risks")
                else:
                    logger.info(f"First 100 characters: {plan[:100]}...")
            else:
                logger.error(f"Failed to generate project plan: {result.get('error', 'Unknown error')}")
                
            logger.info("---")
        
        # Save results to file
        with open("project_planner_demo.json", "w") as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Project Planner results saved to project_planner_demo.json")
        return results
        
    except Exception as e:
        logger.error(f"Error demonstrating Project Planner: {e}")
        import traceback
        traceback.print_exc()
        return None

def demo_smart_matcher():
    """Demonstrate the Smart Matcher agent."""
    try:
        from agents.smart_matcher import SmartMatcherAgent
        
        logger.info("\n=== DEMO: Smart Matcher ===\n")
        agent = SmartMatcherAgent()
        
        # Demo user profiles
        target_user = {
            "user_id": "user1",
            "name": "Jordan",
            "skills": ["JavaScript", "React", "Node.js"],
            "interests": ["Web Development", "UI/UX", "Open Source"],
            "bio": "Full-stack developer with 3 years of experience"
        }
        
        candidate_users = [
            {
                "user_id": "user2",
                "name": "Taylor",
                "skills": ["Python", "Django", "PostgreSQL"],
                "interests": ["Backend Development", "API Design", "DevOps"],
                "bio": "Backend developer specializing in Python"
            },
            {
                "user_id": "user3",
                "name": "Alex",
                "skills": ["UI/UX Design", "Figma", "CSS"],
                "interests": ["Web Design", "User Research", "Accessibility"],
                "bio": "UI/UX designer with focus on accessible interfaces"
            },
            {
                "user_id": "user4",
                "name": "Casey",
                "skills": ["JavaScript", "Vue.js", "Firebase"],
                "interests": ["Web Development", "Mobile Apps", "Real-time Applications"],
                "bio": "Frontend developer with interest in real-time applications"
            }
        ]
        
        logger.info(f"Finding matches for {target_user['name']}...")
        start_time = time.time()
        result = agent.find_matches(target_user, candidate_users)
        end_time = time.time()
        
        if result.get("success", False):
            matches = result.get("matches", [])
            logger.info(f"Found {len(matches)} matches")
            logger.info(f"Time taken: {end_time - start_time:.2f} seconds")
            
            # Display match information
            for i, match in enumerate(matches):
                logger.info(f"Match {i+1}: {match.get('name')} (Score: {match.get('match_score')})")
                logger.info(f"Explanation: {match.get('explanation')[:100]}...")
            
            # Save results to file
            with open("smart_matcher_demo.json", "w") as f:
                json.dump({
                    "target_user": target_user,
                    "candidate_users": candidate_users,
                    "matches": matches,
                    "time_taken": f"{end_time - start_time:.2f} seconds"
                }, f, indent=2)
            
            logger.info(f"Smart Matcher results saved to smart_matcher_demo.json")
            return matches
        else:
            logger.error(f"Failed to find matches: {result.get('error', 'Unknown error')}")
            return None
        
    except Exception as e:
        logger.error(f"Error demonstrating Smart Matcher: {e}")
        import traceback
        traceback.print_exc()
        return None

def demo_model_provider():
    """Demonstrate the Model Provider functionality."""
    try:
        from config.model_provider import model_provider, key_manager, DummyEmbeddings
        
        logger.info("\n=== DEMO: Model Provider System ===\n")
        
        # Get current provider
        current_provider = model_provider.get_provider()
        logger.info(f"Current provider: {current_provider}")
        
        # Test switching providers
        alternate_provider = "openai" if current_provider == "gemini" else "gemini"
        model_provider.set_provider(alternate_provider)
        logger.info(f"Switched to provider: {model_provider.get_provider()}")
        
        # Test LLM creation
        llm = model_provider.create_llm("general_assistant")
        logger.info(f"Created LLM with provider: {model_provider.get_provider()}")
        
        # Test embedding creation
        embeddings = model_provider.create_embeddings()
        embedding_type = type(embeddings).__name__
        logger.info(f"Created embeddings of type: {embedding_type}")
        
        # Test embedding functionality
        test_text = "This is a test document for embedding with SkillMate AI."
        embedding = embeddings.embed_query(test_text)
        logger.info(f"Generated embedding with dimension: {len(embedding)}")
        
        # Test API key management
        openai_key_count = len(key_manager.openai_keys)
        gemini_key_count = len(key_manager.gemini_keys)
        logger.info(f"API keys available: OpenAI ({openai_key_count}), Gemini ({gemini_key_count})")
        
        # Restore original provider
        model_provider.set_provider(current_provider)
        logger.info(f"Restored original provider: {current_provider}")
        
        # Save results to file
        with open("model_provider_demo.json", "w") as f:
            json.dump({
                "initial_provider": current_provider,
                "switched_provider": alternate_provider,
                "embedding_type": embedding_type,
                "embedding_dimension": len(embedding),
                "openai_key_count": openai_key_count,
                "gemini_key_count": gemini_key_count
            }, f, indent=2)
        
        logger.info(f"Model Provider results saved to model_provider_demo.json")
        return True
        
    except Exception as e:
        logger.error(f"Error demonstrating Model Provider: {e}")
        import traceback
        traceback.print_exc()
        return False

def generate_summary_report(results_dir):
    """Generate a summary report of all demos."""
    try:
        logger.info("\n=== Generating Summary Report ===\n")
        
        summary = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "model_provider": os.environ.get("MODEL_PROVIDER", "gemini"),
            "results_directory": results_dir,
            "demos_run": [
                "General Assistant",
                "Roadmap Generator",
                "Project Planner",
                "Smart Matcher",
                "Model Provider"
            ],
            "system_info": {
                "python_version": sys.version,
                "platform": sys.platform
            }
        }
        
        # Save summary to file
        with open("demo_summary.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        # Generate markdown report
        with open("DEMO_REPORT.md", "w") as f:
            f.write("# SkillMate AI System Demo Report\n\n")
            f.write(f"**Date:** {summary['timestamp']}\n")
            f.write(f"**Model Provider:** {summary['model_provider'].upper()}\n")
            f.write(f"**Results Directory:** {summary['results_directory']}\n\n")
            
            f.write("## Demos Executed\n\n")
            for demo in summary['demos_run']:
                f.write(f"- {demo}\n")
            
            f.write("\n## System Information\n\n")
            f.write(f"- Python Version: {summary['system_info']['python_version']}\n")
            f.write(f"- Platform: {summary['system_info']['platform']}\n\n")
            
            f.write("## Summary of Results\n\n")
            f.write("All demo results have been saved as JSON files in this directory.\n")
            f.write("Each file contains the detailed outputs from the corresponding agent.\n\n")
            
            f.write("## Next Steps\n\n")
            f.write("1. Review the JSON output files for detailed results\n")
            f.write("2. Explore the agent implementations in the `skillmate/ai/agents` directory\n")
            f.write("3. Try the model provider with different configurations\n")
            f.write("4. Integrate the agents into your own applications\n")
        
        logger.info(f"Summary report generated: DEMO_REPORT.md")
        return True
        
    except Exception as e:
        logger.error(f"Error generating summary report: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main entry point."""
    results_dir = setup_environment()
    
    # Run all demos
    demo_model_provider()
    demo_general_assistant()
    demo_roadmap_generator()
    demo_project_planner()
    demo_smart_matcher()
    
    # Generate summary report
    generate_summary_report(results_dir)
    
    logger.info("\n=== Demo Complete ===\n")
    logger.info(f"All results saved to {results_dir}/")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 