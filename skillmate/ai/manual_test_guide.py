"""
Manual Testing Guide for SkillMate AI System
Interactive testing for specific features and scenarios
"""

import os
import sys
import json
from io import BytesIO
from datetime import datetime

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

class ManualTester:
    """Interactive manual testing for SkillMate AI features."""
    
    def __init__(self):
        """Initialize the manual tester."""
        print("🧪 SkillMate AI Manual Testing Guide")
        print("=" * 50)
        
        # Check API key
        if not os.getenv("OPENAI_API_KEY"):
            print("⚠️ WARNING: Set OPENAI_API_KEY for full functionality!")
            os.environ["OPENAI_API_KEY"] = "sk-dummy-key-for-testing"
    
    def test_general_ai(self):
        """Test general AI conversation."""
        print("\n🤖 Testing General AI Assistant")
        print("-" * 30)
        
        print("Sample questions you can ask:")
        print("1. How do I get started with React?")
        print("2. What's the difference between Python and JavaScript?")
        print("3. Explain machine learning in simple terms")
        print("4. What are some good coding practices?")
        
        while True:
            message = input("\nEnter your message (or 'quit' to exit): ")
            if message.lower() == 'quit':
                break
                
            response = general_ai_response("manual_test_user", message)
            
            print(f"\n✅ Success: {response['success']}")
            if response['success']:
                print(f"🤖 AI Response: {response['response']}")
            else:
                print(f"❌ Error: {response.get('error', 'Unknown error')}")
    
    def test_resume_analysis(self):
        """Test resume upload and analysis."""
        print("\n📄 Testing Resume Analysis")
        print("-" * 30)
        
        sample_resume = """John Smith
Senior Software Engineer

EXPERIENCE:
• 5+ years developing web applications with React, Node.js, and Python
• Led development of microservices architecture serving 1M+ users
• Experience with cloud platforms (AWS, Azure) and DevOps practices
• Built machine learning models for recommendation systems

SKILLS:
• Languages: Python, JavaScript, TypeScript, Java, Go
• Frontend: React, Vue.js, Angular, HTML/CSS
• Backend: Node.js, Django, Flask, Express
• Databases: PostgreSQL, MongoDB, Redis
• Cloud: AWS, Docker, Kubernetes
• ML: TensorFlow, PyTorch, scikit-learn

EDUCATION:
• M.S. Computer Science, Stanford University
• B.S. Software Engineering, UC Berkeley

PROJECTS:
• E-commerce Platform: Built scalable marketplace with 500K+ users
• AI Chatbot: Developed NLP-powered customer service bot
• Real-time Analytics: Created data processing pipeline with Apache Kafka"""
        
        print("Sample resume loaded. You can query it with questions like:")
        print("1. What programming languages does this candidate know?")
        print("2. How many years of experience do they have?")
        print("3. What projects have they worked on?")
        print("4. What's their educational background?")
        
        while True:
            query = input("\nEnter your query about the resume (or 'quit' to exit): ")
            if query.lower() == 'quit':
                break
            
            # Create file stream
            file_stream = BytesIO(sample_resume.encode('utf-8'))
            
            response = upload_and_query_resume(
                "manual_test_user",
                file_stream,
                "sample_resume.txt",
                query
            )
            
            print(f"\n✅ Success: {response['success']}")
            if response['success']:
                print(f"📋 Answer: {response['answer']}")
            else:
                print(f"❌ Error: {response.get('error', 'Unknown error')}")
    
    def test_roadmap_generation(self):
        """Test learning roadmap generation."""
        print("\n🗺️ Testing Roadmap Generation")
        print("-" * 30)
        
        popular_skills = [
            "Python Programming", "React Development", "Machine Learning",
            "UI/UX Design", "DevOps", "Data Science", "Mobile Development",
            "Blockchain", "Cybersecurity", "Cloud Computing"
        ]
        
        print("Popular skills for roadmap generation:")
        for i, skill in enumerate(popular_skills, 1):
            print(f"{i:2d}. {skill}")
        
        while True:
            skill = input("\nEnter a skill for roadmap generation (or 'quit' to exit): ")
            if skill.lower() == 'quit':
                break
            
            level = input("Enter your current level (beginner/intermediate/advanced): ") or "beginner"
            time_commitment = input("Enter time commitment (light/moderate/intensive): ") or "moderate"
            
            response = get_roadmap(skill, level, time_commitment)
            
            print(f"\n✅ Success: {response['success']}")
            if response['success']:
                print(f"🗺️ Roadmap for {skill}:")
                print(response['roadmap'])
                
                if 'learning_phases' in response:
                    print(f"\n📚 Learning phases: {len(response['learning_phases'])}")
                if 'resources' in response:
                    print(f"📖 Resources provided: {len(response['resources'])}")
            else:
                print(f"❌ Error: {response.get('error', 'Unknown error')}")
    
    def test_project_planning(self):
        """Test project planning functionality."""
        print("\n📋 Testing Project Planning")
        print("-" * 30)
        
        sample_projects = [
            "Build a social media platform for developers",
            "Create an AI-powered chatbot for customer service", 
            "Develop a mobile app for expense tracking",
            "Build a real-time collaboration tool",
            "Create an e-learning platform with video streaming"
        ]
        
        print("Sample project ideas:")
        for i, project in enumerate(sample_projects, 1):
            print(f"{i}. {project}")
        
        while True:
            goal = input("\nEnter project goal (or 'quit' to exit): ")
            if goal.lower() == 'quit':
                break
            
            try:
                team_size = int(input("Enter team size (2-8): ") or "4")
                duration = input("Enter project duration (e.g., '6 weeks'): ") or "6 weeks"
                tech_prefs = input("Enter tech preferences (comma-separated): ").split(',')
                tech_prefs = [tech.strip() for tech in tech_prefs if tech.strip()]
                
                response = suggest_project_plan(
                    f"manual_test_team_{datetime.now().timestamp()}",
                    goal,
                    team_size,
                    duration,
                    tech_prefs
                )
                
                print(f"\n✅ Success: {response['success']}")
                if response['success']:
                    print(f"📋 Project Plan:")
                    print(response['project_plan'])
                    
                    if 'requirements' in response:
                        print(f"\n📝 Requirements: {len(response['requirements'])}")
                    if 'risks' in response:
                        print(f"⚠️ Risks identified: {len(response['risks'])}")
                    if 'complexity' in response:
                        print(f"🎯 Complexity: {response['complexity']}")
                else:
                    print(f"❌ Error: {response.get('error', 'Unknown error')}")
                    
            except ValueError:
                print("❌ Invalid team size. Please enter a number.")
    
    def test_smart_matching(self):
        """Test smart user matching."""
        print("\n🎯 Testing Smart Matching")
        print("-" * 30)
        
        sample_users = [
            "test_user_python_dev", "test_user_react_designer",
            "test_user_mobile_dev", "test_user_data_scientist",
            "test_user_fullstack", "test_user_devops_eng"
        ]
        
        print("Sample user IDs for matching:")
        for user in sample_users:
            print(f"• {user}")
        
        while True:
            user_id = input("\nEnter user ID for matching (or 'quit' to exit): ")
            if user_id.lower() == 'quit':
                break
            
            try:
                limit = int(input("Enter number of matches to find (1-10): ") or "5")
                
                response = suggest_matches(user_id, limit)
                
                print(f"\n✅ Success: {response['success']}")
                if response['success']:
                    print(f"🎯 Found {len(response['matches'])} matches for {user_id}")
                    
                    for i, match in enumerate(response['matches'], 1):
                        print(f"{i}. User: {match.get('user_id', 'Unknown')}")
                        print(f"   Score: {match.get('compatibility_score', 'N/A')}")
                        print(f"   Reason: {match.get('match_reason', 'No reason provided')[:100]}...")
                        print()
                else:
                    print(f"❌ Error: {response.get('error', 'Unknown error')}")
                    
            except ValueError:
                print("❌ Invalid limit. Please enter a number.")
    
    def test_team_chat(self):
        """Test team chat AI functionality."""
        print("\n💬 Testing Team Chat AI")
        print("-" * 30)
        
        sample_teams = [
            ("team_web_dev", "Web Development Team"),
            ("team_mobile", "Mobile App Team"),
            ("team_ai_research", "AI Research Team"),
            ("team_startup", "Startup Development Team")
        ]
        
        print("Sample teams:")
        for team_id, team_name in sample_teams:
            print(f"• {team_id}: {team_name}")
        
        print("\nSample messages to try:")
        print("1. How should we structure our sprint for the next 2 weeks?")
        print("2. What's the best architecture for our web application?")
        print("3. Can you help us identify potential risks in our timeline?")
        print("4. We need to allocate tasks among team members")
        
        team_id = input("\nEnter team ID: ") or "team_web_dev"
        
        context = {
            "team_name": f"Team {team_id}",
            "project_goal": "Build an innovative web application",
            "members": ["Alice (Frontend)", "Bob (Backend)", "Carol (Design)"],
            "tech_stack": ["React", "Node.js", "PostgreSQL"]
        }
        
        while True:
            message = input(f"\n[{team_id}] Enter team message (or 'quit' to exit): ")
            if message.lower() == 'quit':
                break
            
            response = team_chat_ai(team_id, message, "manual_test_user", context)
            
            print(f"\n✅ Success: {response['success']}")
            if response['success']:
                print(f"🤖 Team AI: {response['ai_response']}")
                
                if 'message_type' in response:
                    print(f"📝 Message type: {response['message_type']}")
                if response.get('suggestions'):
                    print(f"💡 Suggestions: {len(response['suggestions'])}")
            else:
                print(f"❌ Error: {response.get('error', 'Unknown error')}")
    
    def run_interactive_menu(self):
        """Run the interactive testing menu."""
        while True:
            print("\n" + "=" * 50)
            print("🧪 SkillMate AI Manual Testing Menu")
            print("=" * 50)
            print("1. 🤖 Test General AI Assistant")
            print("2. 📄 Test Resume Analysis")
            print("3. 🗺️ Test Roadmap Generation")
            print("4. 📋 Test Project Planning")
            print("5. 🎯 Test Smart Matching")
            print("6. 💬 Test Team Chat AI")
            print("7. 🚪 Exit")
            
            choice = input("\nSelect an option (1-7): ")
            
            if choice == '1':
                self.test_general_ai()
            elif choice == '2':
                self.test_resume_analysis()
            elif choice == '3':
                self.test_roadmap_generation()
            elif choice == '4':
                self.test_project_planning()
            elif choice == '5':
                self.test_smart_matching()
            elif choice == '6':
                self.test_team_chat()
            elif choice == '7':
                print("\n👋 Thanks for testing SkillMate AI!")
                break
            else:
                print("❌ Invalid choice. Please select 1-7.")

def main():
    """Main function for manual testing."""
    tester = ManualTester()
    tester.run_interactive_menu()

if __name__ == "__main__":
    main() 