"""
Main API functions for SkillMate AI system.
Flask-compatible functions for all AI features.
"""

import os
import logging
from typing import Dict, Any, List, Optional, BinaryIO
from datetime import datetime

# Set up logger
logger = logging.getLogger(__name__)

try:
    # Try relative imports first (for package usage)
    from .agents.general_assistant import GeneralAssistantAgent
    from .agents.team_assistant import TeamAssistantAgent
    from .agents.smart_matcher import SmartMatcherAgent
    from .agents.roadmap_generator import RoadmapGeneratorAgent
    from .agents.project_planner import ProjectPlannerAgent
    from .embeddings.embedding_service import EmbeddingService
    from .memory.conversation_memory import ConversationMemoryManager
    from .config.settings import settings
except ImportError:
    # Fall back to absolute imports (for direct execution)
    from agents.general_assistant import GeneralAssistantAgent
    from agents.team_assistant import TeamAssistantAgent
    from agents.smart_matcher import SmartMatcherAgent
    from agents.roadmap_generator import RoadmapGeneratorAgent
    from agents.project_planner import ProjectPlannerAgent
    from embeddings.embedding_service import EmbeddingService
    from memory.conversation_memory import ConversationMemoryManager
    from config.settings import settings


class SkillMateAI:
    """Main class for SkillMate AI functionality."""
    
    def __init__(self):
        """Initialize the SkillMate AI system."""
        self.memory_manager = ConversationMemoryManager()
        self.general_assistant = GeneralAssistantAgent(self.memory_manager)
        self.embedding_service = EmbeddingService()
        
    def general_ai_response(self, user_id: str, message: str) -> Dict[str, Any]:
        """Handle general AI chat requests.
        
        Args:
            user_id: User ID
            message: User's message
            
        Returns:
            Dict containing the AI response and metadata
        """
        try:
            # Validate input
            if not user_id or not user_id.strip():
                return {
                    "success": False,
                    "response": "⚠️ Please provide a valid user ID.",
                    "user_id": "unknown",
                    "timestamp": datetime.now().isoformat(),
                    "error_type": "invalid_user_id",
                    "error": "user_id cannot be empty"
                }
                
            if not message or not message.strip():
                return {
                    "success": False,
                    "response": "⚠️ Please provide a message for me to respond to.",
                    "user_id": user_id,
                    "timestamp": datetime.now().isoformat(),
                    "error_type": "invalid_input"
                }
            
            response = self.general_assistant.generate_response(user_id, message)
            
            # Check if the response indicates an error (like API quota)
            is_error = any(indicator in response for indicator in ["🚫", "🔑", "🤖", "⏱️", "⚠️", "⏰"]) or "Error code: 429" in response
            
            # Determine error type
            error_type = None
            if is_error:
                if "🚫" in response or "429" in response or "quota" in response.lower():
                    error_type = "api_quota"
                elif "🔑" in response or "authentication" in response.lower():
                    error_type = "authentication"
                elif "🤖" in response or "model" in response.lower():
                    error_type = "model_unavailable"
                elif "⏱️" in response or "rate_limit" in response.lower():
                    error_type = "rate_limit"
                elif "⏰" in response or "timeout" in response.lower():
                    error_type = "timeout"
                else:
                    error_type = "general_error"
            
            # Ensure we have a valid response
            if not response or not response.strip():
                response = "I apologize, but I wasn't able to generate a response. Please try again."
                is_error = True
                error_type = "empty_response"
            
            return {
                "success": not is_error,
                "response": response,
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "conversation_id": user_id,
                "message_count": len(self.memory_manager.get_messages(user_id)),
                "error_type": error_type
            }
            
        except Exception as e:
            # Provide user-friendly error messages
            error_str = str(e)
            if "429" in error_str or "quota" in error_str.lower():
                error_response = "🚫 I'm currently experiencing high demand due to API limits. Please try again in a few minutes."
                error_type = "api_quota"
            elif "timeout" in error_str.lower():
                error_response = "⏰ The request timed out. Please try again."
                error_type = "timeout"
            else:
                error_response = f"⚠️ I encountered a technical issue: {error_str[:100]}... Please try again in a moment."
                error_type = "general_error"
                
            return {
                "success": False,
                "error": error_str,
                "response": error_response,
                "user_id": user_id or "unknown",
                "timestamp": datetime.now().isoformat(),
                "error_type": error_type
            }
    
    def upload_and_query_resume(self, user_id: str, file_stream: BinaryIO, 
                               filename: str, query: str) -> Dict[str, Any]:
        """Upload and process a resume, then answer a query about it.
        
        Args:
            user_id: User ID
            file_stream: File stream of the resume
            filename: Original filename
            query: Question about the resume
            
        Returns:
            Dict containing the answer and metadata
        """
        try:
            # Validate inputs
            if not query or not query.strip():
                return {
                    "success": False,
                    "error": "Query cannot be empty",
                    "answer": "Please provide a question about the resume.",
                    "user_id": user_id,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Process the resume file
            doc_ids = self.embedding_service.process_file_stream(
                file_stream, filename, user_id, 
                metadata={"document_type": "resume"}
            )
            
            if not doc_ids:
                return {
                    "success": False,
                    "error": "Failed to process resume file",
                    "answer": "I couldn't process the resume file. Please check the file format and try again.",
                    "user_id": user_id,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Query the resume
            relevant_docs = self.embedding_service.query_resume(user_id, query, k=3)
            
            # Check if we found relevant documents
            if not relevant_docs:
                return {
                    "success": True,
                    "answer": "I processed your resume but couldn't find specific information related to your question. Could you try rephrasing your question or asking about different aspects of the resume?",
                    "user_id": user_id,
                    "filename": filename,
                    "document_ids": doc_ids,
                    "relevant_sections": 0,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Format context for the prompt
            context = "\n\n".join([doc.page_content for doc in relevant_docs])
            
            # Validate context
            if not context or not context.strip():
                return {
                    "success": True,
                    "answer": "I processed your resume but the content appears to be empty or unreadable. Please check the file format and try uploading again.",
                    "user_id": user_id,
                    "filename": filename,
                    "document_ids": doc_ids,
                    "relevant_sections": len(relevant_docs),
                    "timestamp": datetime.now().isoformat()
                }
            
            # Generate answer using general assistant
            try:
                from .prompts.assistant_prompts import AssistantPrompts
            except ImportError:
                from prompts.assistant_prompts import AssistantPrompts
            
            prompt_template = AssistantPrompts.resume_qa_prompt()
            formatted_prompt = prompt_template.format(query=query, context=context)
            
            # Use the LLM directly with error handling
            try:
                response = self.general_assistant.llm.predict(formatted_prompt)
            except Exception as llm_error:
                # If LLM fails, provide a fallback response
                if "429" in str(llm_error) or "quota" in str(llm_error).lower():
                    response = "🚫 I'm currently experiencing high demand due to API limits. I found relevant sections in your resume, but can't generate a detailed answer right now. Please try again in a few minutes."
                else:
                    response = f"I found relevant information in your resume but encountered an issue generating the response: {str(llm_error)[:100]}..."
            
            # Validate response
            if not response or not response.strip():
                response = "I found relevant sections in your resume but couldn't generate a proper response. Please try rephrasing your question."
            
            return {
                "success": True,
                "answer": response,
                "user_id": user_id,
                "filename": filename,
                "document_ids": doc_ids,
                "relevant_sections": len(relevant_docs),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            error_str = str(e)
            print(f"Error in upload_and_query_resume: {error_str}")
            
            # Provide specific error messages
            if "list index out of range" in error_str:
                error_message = "I encountered an issue with the document processing system. Please try again."
            elif "timeout" in error_str.lower():
                error_message = "The request timed out while processing your resume. Please try again."
            elif "429" in error_str or "quota" in error_str.lower():
                error_message = "I'm currently experiencing high demand due to API limits. Please try again in a few minutes."
            else:
                error_message = f"I encountered an error processing your resume: {error_str[:100]}... Please try again."
            
            return {
                "success": False,
                "error": error_str,
                "answer": error_message,
                "user_id": user_id,
                "timestamp": datetime.now().isoformat()
            }
    
    def get_roadmap(self, skill: str, user_level: str = "beginner", 
                   time_commitment: str = "moderate") -> Dict[str, Any]:
        """
        Generate comprehensive learning roadmap using LangGraph workflow.
        
        Args:
            skill: Skill to learn
            user_level: Current skill level
            time_commitment: Available time commitment
        
        Returns:
            Dict with comprehensive learning roadmap
        """
        try:
            # Validate inputs
            if not skill or not skill.strip():
                return {
                    "success": False,
                    "error": "skill cannot be empty",
                    "skill": "",
                    "roadmap": "Please provide a valid skill to generate a roadmap.",
                    "agent_type": "roadmap_generator"
                }
                
            if not user_level or not user_level.strip():
                user_level = "beginner"
                
            if not time_commitment or not time_commitment.strip():
                time_commitment = "moderate"
            
            # Generate roadmap using LangGraph workflow
            roadmap_result = roadmap_generator.generate_roadmap(
                skill=skill,
                user_level=user_level,
                time_commitment=time_commitment
            )
            
            if roadmap_result["success"]:
                logger.info(f"Generated roadmap for skill: {skill}")
                
                return {
                    "success": True,
                    "skill": skill,
                    "roadmap": roadmap_result["roadmap"],
                    "prerequisites": roadmap_result["prerequisites"],
                    "learning_phases": roadmap_result["learning_phases"],
                    "resources": roadmap_result["resources"],
                    "projects": roadmap_result["projects"],
                    "workflow_metadata": {
                        "agent_type": roadmap_result["agent_type"],
                        "workflow_complete": roadmap_result["workflow_complete"],
                        "roadmap_steps": 6  # Number of workflow nodes
                    }
                }
            else:
                logger.error(f"Failed to generate roadmap: {roadmap_result.get('error', 'Unknown error')}")
                return {
                    "success": False,
                    "error": roadmap_result.get("error", "Roadmap generation failed"),
                    "skill": skill,
                    "agent_type": "roadmap_generator"
                }
                
        except Exception as e:
            logger.error(f"Error in get_roadmap: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "skill": skill or "",
                "roadmap": f"Error generating roadmap for {skill}",
                "agent_type": "roadmap_generator"
            }
    
    def suggest_project_plan(self, team_id: str, goal: str, team_size: int = 4, 
                            duration: str = "4 weeks", tech_preferences: List[str] = None) -> Dict[str, Any]:
        """
        Generate comprehensive project plan using LangGraph workflow.
        
        Args:
            team_id: Team identifier
            goal: Project goal/description
            team_size: Number of team members
            duration: Project duration
            tech_preferences: Preferred technologies
        
        Returns:
            Dict with comprehensive project plan
        """
        try:
            # Validate inputs
            if not team_id or not team_id.strip():
                return {
                    "success": False,
                    "error": "team_id cannot be empty",
                    "team_id": "",
                    "project_plan": "Please provide a valid team ID.",
                    "agent_type": "project_planner"
                }
                
            if not goal or not goal.strip():
                return {
                    "success": False,
                    "error": "project_description cannot be empty",
                    "team_id": team_id,
                    "project_plan": "Please provide a valid project description.",
                    "agent_type": "project_planner"
                }
            
            # Create project name from goal
            project_name = goal.split('.')[0].strip()[:50]  # First 50 chars
            
            # Get team skills if available
            team_skills = tech_preferences or []
            
            # Generate comprehensive project plan using LangGraph workflow
            plan_result = project_planner.create_project_plan(
                project_name=project_name,
                project_goal=goal,
                team_size=team_size,
                duration=duration,
                team_skills=team_skills
            )
            
            if plan_result["success"]:
                logger.info(f"Generated project plan for team {team_id}: {project_name}")
                
                return {
                    "success": True,
                    "team_id": team_id,
                    "project_plan": plan_result["project_plan"],
                    "requirements": plan_result["requirements"],
                    "architecture": plan_result["architecture"],
                    "sprint_plan": plan_result["sprint_plan"],
                    "risks": plan_result["risks"],
                    "resources": plan_result["resources"],
                    "complexity": plan_result["complexity"],
                    "workflow_metadata": {
                        "agent_type": plan_result["agent_type"],
                        "workflow_complete": plan_result["workflow_complete"],
                        "planning_steps": 6  # Number of workflow nodes
                    }
                }
            else:
                logger.error(f"Failed to generate project plan: {plan_result.get('error', 'Unknown error')}")
                return {
                    "success": False,
                    "error": plan_result.get("error", "Planning workflow failed"),
                    "team_id": team_id,
                    "agent_type": "project_planner"
                }
                
        except Exception as e:
            logger.error(f"Error in suggest_project_plan: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "team_id": team_id or "",
                "project_plan": f"Error generating project plan for team {team_id}",
                "agent_type": "project_planner"
            }
    
    def suggest_matches(self, user_id: str, limit: int = 10) -> Dict[str, Any]:
        """
        Generate smart user matches using LangGraph workflow.
        
        Args:
            user_id: User ID to find matches for
            limit: Maximum number of matches to return
        
        Returns:
            Dict with ranked matches and compatibility scores
        """
        try:
            # Validate inputs
            if not user_id or not user_id.strip():
                return {
                    "success": False,
                    "error": "user_id cannot be empty",
                    "user_id": "",
                    "matches": [],
                    "agent_type": "smart_matcher"
                }
                
            # Get user profile (mock data for now)
            user_profile = {
                "skills": ["Python", "React", "Machine Learning"],
                "interests": ["Web Development", "AI", "Data Science"],
                "experience_level": "Intermediate",
                "collaboration_preference": "Remote",
                "project_types": ["Web Apps", "ML Projects"]
            }
            
            # Get all users for matching (mock data)
            all_users = [
                {
                    "user_id": "user_001",
                    "skills": ["JavaScript", "Node.js", "React"],
                    "interests": ["Frontend", "Full Stack"],
                    "experience_level": "Intermediate"
                },
                {
                    "user_id": "user_002", 
                    "skills": ["Python", "Django", "PostgreSQL"],
                    "interests": ["Backend", "Databases"],
                    "experience_level": "Advanced"
                },
                {
                    "user_id": "user_003",
                    "skills": ["Python", "TensorFlow", "Data Science"],
                    "interests": ["Machine Learning", "AI"],
                    "experience_level": "Intermediate"
                }
            ]
            
            # Generate matches using LangGraph workflow
            matching_result = smart_matcher.find_matches(
                target_user=user_profile,
                candidate_users=all_users,
                project_context={"limit": limit}
            )
            
            if matching_result["success"]:
                matches = matching_result.get("recommendations", [])
                logger.info(f"Generated {len(matches)} matches for user {user_id}")
                
                return {
                    "success": True,
                    "user_id": user_id,
                    "matches": matches,
                    "match_summary": matching_result.get("analysis", "Match analysis completed"),
                    "workflow_metadata": {
                        "agent_type": matching_result["agent_type"],
                        "workflow_complete": matching_result["workflow_complete"],
                        "matching_steps": 4  # Number of workflow nodes
                    }
                }
            else:
                logger.error(f"Failed to generate matches: {matching_result.get('error', 'Unknown error')}")
                return {
                    "success": False,
                    "error": matching_result.get("error", "Matching workflow failed"),
                    "user_id": user_id,
                    "agent_type": "smart_matcher"
                }
                
        except Exception as e:
            logger.error(f"Error in suggest_matches: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "user_id": user_id or "",
                "matches": [],
                "agent_type": "smart_matcher"
            }
    
    def team_chat_ai(self, team_id: str, message: str, user_id: str = None, 
                    context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Handle team chat AI assistance using LangGraph workflow.
        
        Args:
            team_id: Team identifier
            message: User message
            user_id: User sending the message
            context: Additional context (project info, team members, etc.)
        
        Returns:
            Dict with AI response and workflow metadata
        """
        try:
            # Prepare team context
            team_context = context or {}
            team_context.update({
                "team_id": team_id,
                "user_id": user_id,
                "message": message
            })
            
            # Handle team chat using LangGraph workflow
            chat_result = team_assistant.process_team_message(
                team_id=team_id,
                message=message,
                team_info=team_context
            )
            
            if chat_result["success"]:
                logger.info(f"Team AI responded to team {team_id}")
                
                return {
                    "success": True,
                    "team_id": team_id,
                    "ai_response": chat_result["response"],
                    "message_type": chat_result["message_type"],
                    "suggestions": chat_result.get("suggestions", []),
                    "workflow_metadata": {
                        "agent_type": chat_result["agent_type"],
                        "workflow_complete": chat_result["workflow_complete"],
                        "processing_node": chat_result.get("processing_node", "responder")
                    }
                }
            else:
                logger.error(f"Team AI failed: {chat_result.get('error', 'Unknown error')}")
                return {
                    "success": False,
                    "error": chat_result.get("error", "Team AI workflow failed"),
                    "team_id": team_id
                }
                
        except Exception as e:
            logger.error(f"Error in team_chat_ai: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "team_id": team_id,
                "ai_response": "Sorry, I'm having trouble processing your request right now."
            }


# Initialize the SkillMate AI system
skillmate_ai = SkillMateAI()

# Initialize all agents
general_assistant = GeneralAssistantAgent()
team_assistant = TeamAssistantAgent()
smart_matcher = SmartMatcherAgent()
roadmap_generator = RoadmapGeneratorAgent()
project_planner = ProjectPlannerAgent()


# Flask-compatible API functions
def general_ai_response(user_id: str, message: str) -> Dict[str, Any]:
    """Flask-compatible function for general AI responses."""
    return skillmate_ai.general_ai_response(user_id, message)


def upload_and_query_resume(user_id: str, file_stream: BinaryIO, 
                           filename: str, query: str) -> Dict[str, Any]:
    """Flask-compatible function for resume upload and query."""
    return skillmate_ai.upload_and_query_resume(user_id, file_stream, filename, query)


def get_roadmap(skill: str, user_level: str = "beginner", 
               time_commitment: str = "moderate") -> Dict[str, Any]:
    """Flask-compatible function for roadmap generation."""
    return skillmate_ai.get_roadmap(skill, user_level, time_commitment)


def suggest_project_plan(team_id: str, goal: str, team_size: int = 4, 
                        duration: str = "4 weeks", tech_preferences: List[str] = None) -> Dict[str, Any]:
    """Flask-compatible function for project planning."""
    return skillmate_ai.suggest_project_plan(team_id, goal, team_size, duration, tech_preferences)


def suggest_matches(user_id: str, limit: int = 10) -> Dict[str, Any]:
    """Flask-compatible function for match suggestions."""
    return skillmate_ai.suggest_matches(user_id, limit)


def team_chat_ai(team_id: str, message: str, user_id: str = None, 
                context: Dict[str, Any] = None) -> Dict[str, Any]:
    """Flask-compatible function for team chat AI."""
    return skillmate_ai.team_chat_ai(team_id, message, user_id, context) 