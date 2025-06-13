"""
Comprehensive Testing Suite for SkillMate AI System
Tests all agents, workflows, and API functions with dummy data
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from typing import Dict, Any, List
from io import BytesIO, StringIO

# Add the ai module to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all the main functions
from main import (
    general_ai_response,
    upload_and_query_resume,
    get_roadmap,
    suggest_project_plan,
    suggest_matches,
    team_chat_ai
)

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
            "resume_content": """
            John Doe
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
            • Real-time Chat App: Created WebSocket-based communication platform
            """,
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
        """Log a test result."""
        result = {
            "test_name": test_name,
            "success": success,
            "details": details,
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"{status} - {test_name}: {details}")
        if duration > 0:
            logger.info(f"   Duration: {duration:.2f}s")
    
    def test_general_ai_response(self):
        """Test the general AI response functionality."""
        logger.info("🤖 Testing General AI Response...")
        
        test_cases = [
            "Hello, I'm new to programming. Can you help me get started?",
            "What's the difference between Python and JavaScript?",
            "Can you explain what machine learning is in simple terms?",
            "I'm working on a web project. Any suggestions for the tech stack?",
            "How do I improve my coding skills as a beginner?"
        ]
        
        for i, message in enumerate(test_cases):
            start_time = time.time()
            try:
                response = general_ai_response("test_user_001", message)
                duration = time.time() - start_time
                
                if response["success"] and response["response"]:
                    self.log_test_result(
                        f"General AI Test {i+1}",
                        True,
                        f"Got response: {response['response'][:100]}...",
                        duration,
                        {"message": message, "conversation_id": response.get("conversation_id")}
                    )
                else:
                    self.log_test_result(
                        f"General AI Test {i+1}",
                        False,
                        f"Failed: {response.get('error', 'No response generated')}",
                        duration
                    )
            except Exception as e:
                self.log_test_result(
                    f"General AI Test {i+1}",
                    False,
                    f"Exception: {str(e)}",
                    time.time() - start_time
                )
    
    def test_resume_upload_and_query(self):
        """Test resume upload and query functionality."""
        logger.info("📄 Testing Resume Upload and Query...")
        
        # Create a mock file stream
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
                # Reset file stream position
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
        """Test learning roadmap generation."""
        logger.info("🗺️ Testing Roadmap Generation...")
        
        skills = self.dummy_data["skills_to_test"]
        user_levels = ["beginner", "intermediate", "advanced"]
        time_commitments = ["light", "moderate", "intensive"]
        
        for i, skill in enumerate(skills[:4]):  # Test first 4 skills
            for level in user_levels[:2]:  # Test first 2 levels
                start_time = time.time()
                try:
                    response = get_roadmap(skill, level, "moderate")
                    duration = time.time() - start_time
                    
                    if response["success"] and response["roadmap"]:
                        # Check if workflow metadata is present
                        has_workflow_metadata = "workflow_metadata" in response
                        has_phases = "learning_phases" in response and len(response["learning_phases"]) > 0
                        has_resources = "resources" in response and len(response["resources"]) > 0
                        
                        self.log_test_result(
                            f"Roadmap Generation - {skill} ({level})",
                            True,
                            f"Generated roadmap with {len(response.get('learning_phases', []))} phases",
                            duration,
                            {
                                "skill": skill,
                                "level": level,
                                "has_workflow_metadata": has_workflow_metadata,
                                "has_phases": has_phases,
                                "has_resources": has_resources,
                                "roadmap_length": len(response["roadmap"])
                            }
                        )
                    else:
                        self.log_test_result(
                            f"Roadmap Generation - {skill} ({level})",
                            False,
                            f"Failed: {response.get('error', 'No roadmap generated')}",
                            duration
                        )
                except Exception as e:
                    self.log_test_result(
                        f"Roadmap Generation - {skill} ({level})",
                        False,
                        f"Exception: {str(e)}",
                        time.time() - start_time
                    )
    
    def test_project_planning(self):
        """Test project planning functionality."""
        logger.info("📋 Testing Project Planning...")
        
        test_projects = [
            {
                "goal": "Build a social media platform for developers",
                "team_size": 4,
                "duration": "8 weeks",
                "tech_preferences": ["React", "Node.js", "MongoDB"]
            },
            {
                "goal": "Create an AI-powered chatbot for customer service",
                "team_size": 3,
                "duration": "6 weeks", 
                "tech_preferences": ["Python", "TensorFlow", "Flask"]
            },
            {
                "goal": "Develop a mobile app for expense tracking",
                "team_size": 2,
                "duration": "4 weeks",
                "tech_preferences": ["React Native", "Firebase"]
            }
        ]
        
        for i, project in enumerate(test_projects):
            start_time = time.time()
            try:
                response = suggest_project_plan(
                    f"team_test_{i+1}",
                    project["goal"],
                    project["team_size"],
                    project["duration"],
                    project["tech_preferences"]
                )
                duration = time.time() - start_time
                
                if response["success"] and response["project_plan"]:
                    # Check workflow completeness
                    has_requirements = "requirements" in response and len(response["requirements"]) > 0
                    has_architecture = "architecture" in response
                    has_sprint_plan = "sprint_plan" in response
                    has_risks = "risks" in response and len(response["risks"]) > 0
                    has_resources = "resources" in response
                    
                    self.log_test_result(
                        f"Project Planning - {project['goal'][:30]}...",
                        True,
                        f"Generated plan with {len(response.get('requirements', []))} requirements",
                        duration,
                        {
                            "goal": project["goal"],
                            "team_size": project["team_size"],
                            "has_requirements": has_requirements,
                            "has_architecture": has_architecture,
                            "has_sprint_plan": has_sprint_plan,
                            "has_risks": has_risks,
                            "has_resources": has_resources,
                            "complexity": response.get("complexity", "unknown")
                        }
                    )
                else:
                    self.log_test_result(
                        f"Project Planning - {project['goal'][:30]}...",
                        False,
                        f"Failed: {response.get('error', 'No plan generated')}",
                        duration
                    )
            except Exception as e:
                self.log_test_result(
                    f"Project Planning - {project['goal'][:30]}...",
                    False,
                    f"Exception: {str(e)}",
                    time.time() - start_time
                )
    
    def test_smart_matching(self):
        """Test smart user matching functionality."""
        logger.info("🎯 Testing Smart Matching...")
        
        test_users = self.dummy_data["users"]
        
        for user in test_users:
            start_time = time.time()
            try:
                response = suggest_matches(user["user_id"], limit=5)
                duration = time.time() - start_time
                
                if response["success"] and "matches" in response:
                    num_matches = len(response["matches"])
                    has_workflow_metadata = "workflow_metadata" in response
                    has_match_summary = "match_summary" in response
                    
                    self.log_test_result(
                        f"Smart Matching - {user['name']}",
                        True,
                        f"Found {num_matches} matches",
                        duration,
                        {
                            "user_id": user["user_id"],
                            "num_matches": num_matches,
                            "has_workflow_metadata": has_workflow_metadata,
                            "has_match_summary": has_match_summary,
                            "user_skills": user["skills"]
                        }
                    )
                else:
                    self.log_test_result(
                        f"Smart Matching - {user['name']}",
                        False,
                        f"Failed: {response.get('error', 'No matches found')}",
                        duration
                    )
            except Exception as e:
                self.log_test_result(
                    f"Smart Matching - {user['name']}",
                    False,
                    f"Exception: {str(e)}",
                    time.time() - start_time
                )
    
    def test_team_chat_ai(self):
        """Test team chat AI functionality."""
        logger.info("💬 Testing Team Chat AI...")
        
        teams = self.dummy_data["teams"]
        messages = self.dummy_data["test_messages"]
        
        for team in teams:
            for i, message in enumerate(messages[:4]):  # Test first 4 messages per team
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
        """Test error handling and edge cases."""
        logger.info("⚠️ Testing Error Handling...")
        
        # Test with invalid inputs
        error_test_cases = [
            {
                "name": "Empty message to general AI",
                "func": lambda: general_ai_response("test_user", ""),
                "expected": "should handle empty message gracefully"
            },
            {
                "name": "Invalid skill for roadmap",
                "func": lambda: get_roadmap("", "beginner", "moderate"),
                "expected": "should handle empty skill gracefully"
            },
            {
                "name": "Invalid team size for project planning",
                "func": lambda: suggest_project_plan("test_team", "Build an app", 0, "4 weeks"),
                "expected": "should handle invalid team size"
            },
            {
                "name": "Empty team message",
                "func": lambda: team_chat_ai("test_team", "", "test_user"),
                "expected": "should handle empty team message"
            }
        ]
        
        for test_case in error_test_cases:
            start_time = time.time()
            try:
                response = test_case["func"]()
                duration = time.time() - start_time
                
                # Check if the function handled the error gracefully
                if isinstance(response, dict) and "error" in response:
                    self.log_test_result(
                        f"Error Handling - {test_case['name']}",
                        True,
                        f"Handled gracefully: {response.get('error', 'Unknown error')[:50]}...",
                        duration,
                        {"expected": test_case["expected"]}
                    )
                else:
                    self.log_test_result(
                        f"Error Handling - {test_case['name']}",
                        False,
                        "Did not handle error gracefully",
                        duration
                    )
            except Exception as e:
                self.log_test_result(
                    f"Error Handling - {test_case['name']}",
                    False,
                    f"Unhandled exception: {str(e)}",
                    time.time() - start_time
                )
    
    def run_all_tests(self):
        """Run all tests in the suite."""
        logger.info("🚀 Starting SkillMate AI System Comprehensive Testing...")
        logger.info("=" * 60)
        
        # Run all test categories
        test_categories = [
            ("General AI Response", self.test_general_ai_response),
            ("Resume Upload & Query", self.test_resume_upload_and_query),
            ("Roadmap Generation", self.test_roadmap_generation),
            ("Project Planning", self.test_project_planning),
            ("Smart Matching", self.test_smart_matching),
            ("Team Chat AI", self.test_team_chat_ai),
            ("Error Handling", self.test_error_handling)
        ]
        
        for category_name, test_func in test_categories:
            logger.info(f"\n🔍 Running {category_name} Tests...")
            try:
                test_func()
            except Exception as e:
                logger.error(f"❌ Test category {category_name} failed with exception: {str(e)}")
                self.log_test_result(
                    f"{category_name} - Category Error",
                    False,
                    f"Test category failed: {str(e)}"
                )
        
        # Generate final report
        self.generate_test_report()
    
    def generate_test_report(self):
        """Generate a comprehensive test report."""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        total_duration = (datetime.now() - self.start_time).total_seconds()
        
        # Calculate success rate
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Generate report
        report = {
            "test_summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests, 
                "failed_tests": failed_tests,
                "success_rate": f"{success_rate:.1f}%",
                "total_duration": f"{total_duration:.2f}s",
                "timestamp": datetime.now().isoformat()
            },
            "test_results": self.test_results,
            "system_info": {
                "python_version": sys.version,
                "test_environment": "Local Development"
            }
        }
        
        # Save detailed report to JSON
        with open("test_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        logger.info("\n" + "=" * 60)
        logger.info("📊 TEST SUMMARY REPORT")
        logger.info("=" * 60)
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"✅ Passed: {passed_tests}")
        logger.info(f"❌ Failed: {failed_tests}")
        logger.info(f"🎯 Success Rate: {success_rate:.1f}%")
        logger.info(f"⏱️ Total Duration: {total_duration:.2f}s")
        
        if failed_tests > 0:
            logger.info("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    logger.info(f"   • {result['test_name']}: {result['details']}")
        
        logger.info(f"\n📁 Detailed report saved to: test_report.json")
        logger.info(f"📁 Test logs saved to: test_results.log")
        
        # Final verdict
        if success_rate >= 90:
            logger.info("\n🎉 EXCELLENT! System is ready for production!")
        elif success_rate >= 75:
            logger.info("\n✅ GOOD! Minor issues to address before production.")
        elif success_rate >= 50:
            logger.info("\n⚠️ NEEDS WORK! Several issues need to be fixed.")
        else:
            logger.info("\n🚨 CRITICAL! Major issues need immediate attention.")
        
        return report


def main():
    """Main function to run the test suite."""
    # Set up environment variables if not already set
    if not os.getenv("OPENAI_API_KEY"):
        logger.warning("⚠️ OPENAI_API_KEY not found in environment variables!")
        logger.warning("Please set your OpenAI API key for full testing.")
        logger.warning("Some tests may fail without a valid API key.")
        
        # You can set a dummy key for testing structure (will fail API calls)
        os.environ["OPENAI_API_KEY"] = "sk-dummy-key-for-testing"
    
    # Initialize and run tests
    tester = SkillMateAITester()
    tester.run_all_tests()


if __name__ == "__main__":
    main() 