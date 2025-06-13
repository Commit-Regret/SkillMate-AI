#!/usr/bin/env python3
"""
Comprehensive test suite for the SkillMate AI system.
"""

import os
import sys
import json
import logging
import time
from typing import Dict, Any, List, Optional
from datetime import datetime

# Add parent directory to path to import skillmate modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from skillmate.ai.main import SkillMateAI
    print("✅ Successfully imported main functions")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Available files in directory:")
    for file in os.listdir():
        if file.endswith('.py'):
            print(f"  - {file}")
    sys.exit(1)

# Configure logging for testing
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_results.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class SkillMateAITester:
    """Comprehensive testing suite for SkillMate AI system."""
    
    def __init__(self):
        """Initialize the tester with dummy data."""
        self.test_results = []
        self.start_time = datetime.now()
        self.dummy_data = self._generate_dummy_data()
        self.provider = os.getenv("MODEL_PROVIDER", "openai")
        self.results = {
            "general_assistant": {"success": 0, "failure": 0},
            "roadmap_generator": {"success": 0, "failure": 0},
            "project_planner": {"success": 0, "failure": 0},
            "smart_matcher": {"success": 0, "failure": 0}
        }
        
        logger.info(f"Initializing SkillMate AI Tester with provider: {self.provider}")
        
    def _generate_dummy_data(self) -> Dict[str, Any]:
        """Generate comprehensive dummy data for testing."""
        return {
            "users": [
                {
                    "user_id": "test_user_001",
                    "name": "Alice Johnson",
                    "skills": ["Python", "React", "Machine Learning", "Data Science"],
                    "interests": ["Web Development", "AI", "Startups"],
                    "experience": "3 years in software development",
                    "bio": "Full-stack developer passionate about AI and machine learning applications",
                    "looking_for": "Co-founder for AI startup",
                    "experience_level": "Intermediate",
                    "collaboration_preference": "Remote",
                    "project_types": ["Web Apps", "ML Projects", "APIs"]
                },
                {
                    "user_id": "test_user_002", 
                    "name": "Bob Smith",
                    "skills": ["JavaScript", "Node.js", "MongoDB", "React Native"],
                    "interests": ["Mobile Development", "Backend Systems", "DevOps"],
                    "experience": "5 years in mobile and web development",
                    "bio": "Mobile-first developer with backend expertise",
                    "looking_for": "Technical co-founder",
                    "experience_level": "Advanced",
                    "collaboration_preference": "Hybrid",
                    "project_types": ["Mobile Apps", "Web Services"]
                },
                {
                    "user_id": "test_user_003",
                    "name": "Carol Davis",
                    "skills": ["UI/UX Design", "Figma", "Adobe Creative Suite", "Frontend"],
                    "interests": ["Design Systems", "User Research", "Product Design"],
                    "experience": "4 years in product design",
                    "bio": "Product designer focused on user-centered design",
                    "looking_for": "Development partner",
                    "experience_level": "Intermediate",
                    "collaboration_preference": "In-person",
                    "project_types": ["Design Systems", "Web Apps"]
                }
            ],
            "teams": [
                {
                    "team_id": "team_alpha",
                    "name": "Team Alpha",
                    "project_goal": "Build a real-time collaboration platform for remote teams",
                    "members": ["Alice Johnson", "Bob Smith", "Carol Davis"],
                    "tech_stack": ["React", "Node.js", "WebSocket", "MongoDB"],
                    "duration": "6 weeks"
                },
                {
                    "team_id": "team_beta",
                    "name": "Team Beta", 
                    "project_goal": "Develop an AI-powered learning management system",
                    "members": ["Alice Johnson", "Bob Smith"],
                    "tech_stack": ["Python", "TensorFlow", "React", "PostgreSQL"],
                    "duration": "8 weeks"
                }
            ],
            "skills_to_test": [
                "Python Programming",
                "React Development", 
                "Machine Learning",
                "UI/UX Design",
                "DevOps Engineering",
                "Mobile Development",
                "Data Science",
                "Blockchain Development"
            ],
            "resume_content": """John Doe
Software Engineer

EXPERIENCE:
• 3+ years developing web applications using React, Node.js, and Python
• Built machine learning models for predictive analytics
• Led a team of 4 developers on e-commerce platform
• Expertise in cloud deployment with AWS and Docker

SKILLS:
• Programming: Python, JavaScript, TypeScript, Java
• Web Technologies: React, Node.js, Express, HTML/CSS
• Databases: PostgreSQL, MongoDB, Redis
• Machine Learning: TensorFlow, scikit-learn, pandas
• Cloud: AWS, Docker, Kubernetes
• Tools: Git, Jenkins, JIRA

EDUCATION:
• B.S. Computer Science, University of Technology
• Machine Learning Specialization, Coursera

PROJECTS:
• E-commerce Platform: Built scalable online marketplace
• ML Recommendation System: Developed product recommendation engine
• Real-time Chat App: Created WebSocket-based communication platform""",
            "test_messages": [
                "How should we structure our sprint for the next 2 weeks?",
                "What's the best architecture for a real-time chat application?",
                "Can you help us identify potential risks in our project timeline?",
                "We need to allocate tasks among team members effectively",
                "What are the latest best practices for React development?",
                "How do we handle user authentication in our web app?",
                "Can you suggest a deployment strategy for our application?",
                "What testing frameworks should we use for our project?"
            ]
        }
    
    def log_test_result(self, test_name: str, success: bool, details: str, 
                       duration: float = 0, metadata: Dict[str, Any] = None):
        """Log a test result.
        
        Args:
            test_name: Name of the test
            success: Whether the test passed
            details: Test details
            duration: Test duration in seconds
            metadata: Optional metadata
        """
        status = "PASS" if success else "FAIL"
        
        # Remove emoji characters for Windows compatibility
        clean_details = details.replace("🚫", "").replace("🔑", "").replace("🤖", "").replace("⏱️", "").replace("⚠️", "").replace("⏰", "").replace("✅", "").replace("❌", "")
        
        logger.info(f"{status} - {test_name}: {clean_details}")
        logger.info(f"   Duration: {duration:.2f}s")
        
        self.test_results.append({
            "test_name": test_name,
            "success": success,
            "details": details,
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        })
    
    def _log_test_result(self, component: str, test_name: str, success: bool, details: Optional[str] = None):
        """Log test result.
        
        Args:
            component: Component being tested
            test_name: Name of the test
            success: Whether the test passed
            details: Optional details about the test
        """
        if success:
            logger.info(f"✅ {component} - {test_name}")
            self.results[component]["success"] += 1
        else:
            logger.error(f"❌ {component} - {test_name}")
            if details:
                logger.error(f"   Details: {details}")
            self.results[component]["failure"] += 1
    
    def test_general_ai_response(self):
        """Test the general assistant agent."""
        logger.info("Testing General Assistant Agent...")
        
        try:
            # Initialize agent
            agent = GeneralAssistantAgent()
            
            # Test basic question
            response = agent.generate_response("test_user", "What is SkillMate AI?")
            success = len(response) > 50  # Simple check for non-empty response
            self._log_test_result("general_assistant", "Basic Question", success)
            
            # Test code explanation
            code_snippet = """
            def factorial(n):
                if n == 0:
                    return 1
                else:
                    return n * factorial(n-1)
            """
            response = agent.generate_response("test_user", f"Explain this code: {code_snippet}")
            success = len(response) > 100  # Simple check for detailed response
            self._log_test_result("general_assistant", "Code Explanation", success)
            
            return True
        except Exception as e:
            logger.error(f"Error testing general assistant: {e}")
            traceback.print_exc()
            return False
    
    def test_resume_upload_and_query(self):
        """Test resume upload and query functionality."""
        logger.info("📄 Testing Resume Upload and Query...")
        
        resume_content = self.dummy_data["resume_content"]
        file_stream = BytesIO(resume_content.encode('utf-8'))
        
        test_queries = [
            "What are the candidate's main programming skills?",
            "How many years of experience does this person have?",
            "What projects has the candidate worked on?",
            "What technologies is the candidate familiar with?",
            "What is the candidate's educational background?"
        ]
        
        for i, query in enumerate(test_queries):
            start_time = time.time()
            try:
                file_stream.seek(0)
                
                response = upload_and_query_resume(
                    "test_user_001", 
                    file_stream, 
                    "test_resume.txt", 
                    query
                )
                duration = time.time() - start_time
                
                if response["success"] and response["answer"]:
                    self.log_test_result(
                        f"Resume Query Test {i+1}",
                        True,
                        f"Query: '{query}' | Answer: {response['answer'][:100]}...",
                        duration,
                        {"query": query, "filename": "test_resume.txt"}
                    )
                else:
                    self.log_test_result(
                        f"Resume Query Test {i+1}",
                        False,
                        f"Failed: {response.get('error', 'No answer generated')}",
                        duration
                    )
            except Exception as e:
                self.log_test_result(
                    f"Resume Query Test {i+1}",
                    False,
                    f"Exception: {str(e)}",
                    time.time() - start_time
                )
    
    def test_roadmap_generation(self):
        """Test the roadmap generator agent."""
        logger.info("Testing Roadmap Generator Agent...")
        
        try:
            # Initialize agent
            agent = RoadmapGeneratorAgent()
            
            # Test roadmap generation
            result = agent.generate_roadmap("Python", "beginner", "moderate")
            success = result.get("success", False) and len(result.get("roadmap", "")) > 200
            self._log_test_result("roadmap_generator", "Generate Roadmap", success)
            
            return True
        except Exception as e:
            logger.error(f"Error testing roadmap generator: {e}")
            traceback.print_exc()
            return False
    
    def test_project_planning(self):
        """Test the project planner agent."""
        logger.info("Testing Project Planner Agent...")
        
        try:
            # Initialize agent
            agent = ProjectPlannerAgent()
            
            # Test project plan creation
            result = agent.create_project_plan(
                "E-commerce Website",
                "Create a modern e-commerce platform",
                team_size=4,
                duration="4 weeks"
            )
            success = result.get("success", False) and "project_plan" in result
            self._log_test_result("project_planner", "Create Project Plan", success)
            
            return True
        except Exception as e:
            logger.error(f"Error testing project planner: {e}")
            traceback.print_exc()
            return False
    
    def test_smart_matching(self):
        """Test the smart matcher agent."""
        logger.info("Testing Smart Matcher Agent...")
        
        try:
            # Initialize agent
            agent = SmartMatcherAgent()
            
            # Test user matching
            target_user = {
                "user_id": "user1",
                "name": "Alice",
                "skills": ["Python", "React", "UI Design"],
                "interests": ["Web Development", "AI", "Mobile Apps"]
            }
            
            candidate_users = [
                {
                    "user_id": "user2",
                    "name": "Bob",
                    "skills": ["JavaScript", "Node.js", "MongoDB"],
                    "interests": ["Web Development", "Backend", "Databases"]
                },
                {
                    "user_id": "user3",
                    "name": "Charlie",
                    "skills": ["Python", "Django", "PostgreSQL"],
                    "interests": ["AI", "Machine Learning", "Data Science"]
                }
            ]
            
            result = agent.find_matches(target_user, candidate_users)
            success = result.get("success", False) and "matches" in result
            self._log_test_result("smart_matcher", "Find Matches", success)
            
            return True
        except Exception as e:
            logger.error(f"Error testing smart matcher: {e}")
            traceback.print_exc()
            return False
    
    def test_team_chat_ai(self):
        """Test team chat AI functionality."""
        logger.info("💬 Testing Team Chat AI...")
        
        teams = self.dummy_data["teams"]
        messages = self.dummy_data["test_messages"]
        
        for team in teams:
            for i, message in enumerate(messages[:4]):
                start_time = time.time()
                try:
                    context = {
                        "team_name": team["name"],
                        "project_goal": team["project_goal"],
                        "members": team["members"],
                        "tech_stack": team["tech_stack"]
                    }
                    
                    response = team_chat_ai(
                        team["team_id"],
                        message,
                        "test_user_001",
                        context
                    )
                    duration = time.time() - start_time
                    
                    if response["success"] and response["ai_response"]:
                        has_workflow_metadata = "workflow_metadata" in response
                        message_type = response.get("message_type", "unknown")
                        has_suggestions = "suggestions" in response and len(response.get("suggestions", [])) > 0
                        
                        self.log_test_result(
                            f"Team Chat - {team['name']} (Message {i+1})",
                            True,
                            f"Response type: {message_type} | Response: {response['ai_response'][:50]}...",
                            duration,
                            {
                                "team_id": team["team_id"],
                                "message": message,
                                "message_type": message_type,
                                "has_workflow_metadata": has_workflow_metadata,
                                "has_suggestions": has_suggestions,
                                "response_length": len(response["ai_response"])
                            }
                        )
                    else:
                        self.log_test_result(
                            f"Team Chat - {team['name']} (Message {i+1})",
                            False,
                            f"Failed: {response.get('error', 'No response generated')}",
                            duration
                        )
                except Exception as e:
                    self.log_test_result(
                        f"Team Chat - {team['name']} (Message {i+1})",
                        False,
                        f"Exception: {str(e)}",
                        time.time() - start_time
                    )
    
    def test_error_handling(self):
        """Test error handling functionality."""
        logger.info("🛑 Testing Error Handling...")
        
        # Test invalid inputs
        test_cases = [
            {"func": "general_ai_response", "args": ["", "Hello"], "expected_error": "user_id"},
            {"func": "get_roadmap", "args": ["", "beginner", "moderate"], "expected_error": "skill"},
            {"func": "suggest_project_plan", "args": ["team1", "", 4, "4 weeks", []], "expected_error": "project_description"},
            {"func": "suggest_matches", "args": ["", 5], "expected_error": "user_id"}
        ]
        
        for test_case in test_cases:
            start_time = time.time()
            func_name = test_case["func"]
            args = test_case["args"]
            expected_error = test_case["expected_error"]
            
            try:
                # Get the function dynamically
                func = globals()[func_name]
                response = func(*args)
                duration = time.time() - start_time
                
                # Check if the error was handled correctly
                if not response.get("success", True) and expected_error.lower() in str(response.get("error", "")).lower():
                    self.log_test_result(
                        f"Error Handling - {func_name}",
                        True,
                        f"Correctly handled invalid {expected_error}",
                        duration
                    )
                else:
                    self.log_test_result(
                        f"Error Handling - {func_name}",
                        False,
                        f"Failed to handle invalid {expected_error}",
                        duration
                    )
            except Exception as e:
                self.log_test_result(
                    f"Error Handling - {func_name}",
                    False,
                    f"Unexpected exception: {str(e)}",
                    time.time() - start_time
                )
    
    # Aliases for compatibility with run_tests.py
    test_general_assistant = test_general_ai_response
    test_roadmap_generator = test_roadmap_generation
    test_project_planner = test_project_planning
    test_smart_matcher = test_smart_matching
    
    def run_all_tests(self):
        """Run all tests."""
        logger.info("🚀 Running all tests...")
        
        self.test_general_ai_response()
        self.test_resume_upload_and_query()
        self.test_roadmap_generation()
        self.test_project_planning()
        self.test_smart_matching()
        self.test_team_chat_ai()
        self.test_error_handling()
        
        self.generate_test_report()
    
    def generate_test_report(self):
        """Generate a comprehensive test report."""
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = len(self.test_results) - passed_tests
        success_rate = (passed_tests / len(self.test_results)) * 100 if self.test_results else 0
        total_duration = sum(result["duration"] for result in self.test_results)
        
        logger.info("\n" + "=" * 60)
        logger.info("TEST SUMMARY REPORT")
        logger.info("=" * 60)
        logger.info(f"Total Tests: {len(self.test_results)}")
        logger.info(f"Passed: {passed_tests}")
        logger.info(f"Failed: {failed_tests}")
        logger.info(f"Success Rate: {success_rate:.1f}%")
        logger.info(f"Total Duration: {total_duration:.2f}s")
        
        if failed_tests > 0:
            logger.info("\nFAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    # Remove emoji characters for Windows compatibility
                    clean_details = result["details"].replace("🚫", "").replace("🔑", "").replace("🤖", "").replace("⏱️", "").replace("⚠️", "").replace("⏰", "").replace("✅", "").replace("❌", "")
                    logger.info(f"   • {result['test_name']}: {clean_details}")
        
        # Save detailed report to JSON
        report_data = {
            "test_summary": {
                "total_tests": len(self.test_results),
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": f"{success_rate:.1f}%",
                "total_duration": f"{total_duration:.2f}s",
                "timestamp": datetime.now().isoformat()
            },
            "test_results": self.test_results
        }
        
        with open("test_report.json", "w") as f:
            json.dump(report_data, f, indent=2)
        
        logger.info(f"\nDetailed report saved to: test_report.json")
        logger.info(f"Test logs saved to: test_results.log")
        
        # Provide recommendations based on results
        if success_rate < 50:
            logger.info("\nCRITICAL! Major issues need immediate attention.")
        elif success_rate < 80:
            logger.info("\nWARNING! Several issues need attention.")
        else:
            logger.info("\nGOOD! Most tests are passing.")
        
        return report_data

    def get_test_summary(self):
        """Get summary of test results.
        
        Returns:
            Dictionary with test summary
        """
        total_success = sum(component["success"] for component in self.results.values())
        total_failure = sum(component["failure"] for component in self.results.values())
        total_tests = total_success + total_failure
        
        return {
            "total_tests": total_tests,
            "total_success": total_success,
            "total_failure": total_failure,
            "success_rate": f"{(total_success / total_tests) * 100:.1f}%" if total_tests > 0 else "N/A",
            "component_results": self.results,
            "provider": self.provider
        }
    
    def print_test_summary(self):
        """Print summary of test results."""
        summary = self.get_test_summary()
        
        logger.info("\n" + "=" * 60)
        logger.info(f"Test Summary (Provider: {summary['provider']})")
        logger.info("=" * 60)
        logger.info(f"Total Tests: {summary['total_tests']}")
        logger.info(f"Passed: {summary['total_success']}")
        logger.info(f"Failed: {summary['total_failure']}")
        logger.info(f"Success Rate: {summary['success_rate']}")
        logger.info("=" * 60)
        
        for component, results in summary["component_results"].items():
            component_total = results["success"] + results["failure"]
            if component_total > 0:
                success_rate = f"{(results['success'] / component_total) * 100:.1f}%"
            else:
                success_rate = "N/A"
            
            logger.info(f"{component}: {results['success']}/{component_total} ({success_rate})")
        
        logger.info("=" * 60)


def main():
    """Main function to run the test suite."""
    if not os.getenv("OPENAI_API_KEY"):
        logger.warning("⚠️ OPENAI_API_KEY not found in environment variables!")
        logger.warning("Please set your OpenAI API key for full testing.")
        logger.warning("Some tests may fail without a valid API key.")
        os.environ["OPENAI_API_KEY"] = "sk-dummy-key-for-testing"
    
    tester = SkillMateAITester()
    tester.run_all_tests()


if __name__ == "__main__":
    main() 