"""
Team AI Assistant with LangGraph workflow for SkillMate platform.
"""

from typing import Dict, Any, Optional, List
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from pydantic import BaseModel
import logging
import json

try:
    from langchain_core.chains import ConversationChain
    from langchain_core.memory import ConversationBufferMemory
except ImportError:
    from langchain.chains import ConversationChain
    from langchain.memory import ConversationBufferMemory

# Set up logger
logger = logging.getLogger(__name__)

try:
    from ..config.settings import settings
    from ..memory.conversation_memory import ConversationMemoryManager
    from ..prompts.team_prompts import TeamPrompts
    from ..schemas.message_schemas import MessageSchema
    from ..schemas.team_schemas import TeamSchema
    from ..config.model_provider import model_provider, with_api_key_rotation
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config.settings import settings
    from memory.conversation_memory import ConversationMemoryManager
    from prompts.team_prompts import TeamPrompts
    from schemas.message_schemas import MessageSchema
    from schemas.team_schemas import TeamSchema
    from config.model_provider import model_provider, with_api_key_rotation


class TeamState(BaseModel):
    """State for team assistant workflow."""
    team_id: str
    message: str
    team_info: Dict[str, Any]
    conversation_history: List[Dict[str, str]]
    current_context: str = ""
    response: str = ""
    needs_planning: bool = False
    needs_technical_help: bool = False
    needs_coordination: bool = False
    action_items: List[str] = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary for LangGraph compatibility."""
        return {
            "team_id": self.team_id,
            "message": self.message,
            "team_info": self.team_info,
            "conversation_history": self.conversation_history,
            "current_context": self.current_context,
            "response": self.response,
            "needs_planning": self.needs_planning,
            "needs_technical_help": self.needs_technical_help,
            "needs_coordination": self.needs_coordination,
            "action_items": self.action_items
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TeamState":
        """Create state from dictionary for LangGraph compatibility."""
        return cls(
            team_id=data.get("team_id", ""),
            message=data.get("message", ""),
            team_info=data.get("team_info", {}),
            conversation_history=data.get("conversation_history", []),
            current_context=data.get("current_context", ""),
            response=data.get("response", ""),
            needs_planning=data.get("needs_planning", False),
            needs_technical_help=data.get("needs_technical_help", False),
            needs_coordination=data.get("needs_coordination", False),
            action_items=data.get("action_items", [])
        )


class TeamAssistantAgent:
    """Team AI assistant with multi-agent workflow using LangGraph."""
    
    def __init__(self, memory_manager: Optional[ConversationMemoryManager] = None):
        """Initialize the team assistant agent.
        
        Args:
            memory_manager: Optional memory manager instance
        """
        # Create LLM using the model provider factory
        self.llm = model_provider.create_llm(
            model_type="team_assistant",
            temperature=0.7
        )
        
        self.memory_manager = memory_manager or ConversationMemoryManager()
        self.workflow = self._create_workflow()
    
    def _create_workflow(self) -> StateGraph:
        """Create the LangGraph workflow for team assistance.
        
        Returns:
            StateGraph workflow
        """
        # Use dict-based workflow instead of Pydantic model
        workflow = StateGraph(Dict)
        
        # Add nodes for different agent roles
        workflow.add_node("analyzer", self._analyze_message)
        workflow.add_node("planner", self._handle_planning)
        workflow.add_node("technical_advisor", self._handle_technical)
        workflow.add_node("coordinator", self._handle_coordination)
        workflow.add_node("responder", self._generate_response)
        
        # Define the workflow edges
        workflow.set_entry_point("analyzer")
        
        # Conditional routing based on analysis
        workflow.add_conditional_edges(
            "analyzer",
            self._route_message,
            {
                "planning": "planner",
                "technical": "technical_advisor", 
                "coordination": "coordinator",
                "general": "responder"
            }
        )
        
        # All specialized nodes lead to responder
        workflow.add_edge("planner", "responder")
        workflow.add_edge("technical_advisor", "responder")
        workflow.add_edge("coordinator", "responder")
        workflow.add_edge("responder", END)
        
        # Compile the workflow without checkpointer (not needed for this use case)
        return workflow.compile()
    
    def _analyze_message(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the incoming message to determine intent.
        
        Args:
            state: Current team state dictionary
            
        Returns:
            Updated state dictionary with analysis
        """
        message_lower = state["message"].lower()
        
        # Analyze intent with expanded keywords
        planning_keywords = ["plan", "sprint", "roadmap", "timeline", "schedule", "milestone", "project management"]
        
        # Expanded technical keywords for better detection
        technical_keywords = [
            "bug", "error", "implement", "code", "debug", "api", "database", "sync", "socket", 
            "real-time", "socket.io", "websocket", "conflict resolution", "technical", "implementation",
            "architecture", "design pattern", "algorithm", "data structure", "programming"
        ]
        
        coordination_keywords = ["assign", "delegate", "task", "who", "responsible", "deadline", "coordinate", "team"]
        
        # Check for keywords in the message
        state["needs_planning"] = any(keyword in message_lower for keyword in planning_keywords)
        state["needs_technical_help"] = any(keyword in message_lower for keyword in technical_keywords)
        state["needs_coordination"] = any(keyword in message_lower for keyword in coordination_keywords)
        
        # Also check conversation history for context
        if "conversation_history" in state and state["conversation_history"]:
            # Look at recent messages to detect ongoing technical discussion
            recent_messages = state["conversation_history"][-5:] if len(state["conversation_history"]) > 5 else state["conversation_history"]
            for msg in recent_messages:
                if msg.get("role") == "user":
                    msg_content = msg.get("content", "").lower()
                    # If previous messages contained technical keywords, this is likely a technical conversation
                    if any(keyword in msg_content for keyword in technical_keywords):
                        state["needs_technical_help"] = True
                        break
        
        return state
    
    def _route_message(self, state: Dict[str, Any]) -> str:
        """Route message to appropriate handler based on analysis.
        
        Args:
            state: Current team state dictionary
            
        Returns:
            Next node to process
        """
        if state["needs_planning"]:
            return "planning"
        elif state["needs_technical_help"]:
            return "technical"
        elif state["needs_coordination"]:
            return "coordination"
        else:
            return "general"
    
    @with_api_key_rotation(max_retries=3, retry_delay=1.0)
    def _handle_planning(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Handle planning-related requests.
        
        Args:
            state: Current team state dictionary
            
        Returns:
            Updated state dictionary
        """
        team_info = state["team_info"]
        prompt = f"""You are a project planning specialist for Team {team_info.get('name', 'Unknown')}.
        
        Team Project: {team_info.get('project_goal', 'Not specified')}
        Team Members: {', '.join(team_info.get('members', []))}
        
        The team asked: {state["message"]}
        
        Provide specific planning guidance, suggest concrete next steps, and help with project organization.
        Focus on actionable advice that moves the project forward.
        """
        
        planning_response = self.llm.predict(prompt)
        state["current_context"] = f"Planning Context: {planning_response}"
        
        # Extract action items (simplified)
        if "action" in planning_response.lower():
            if "action_items" not in state or not isinstance(state["action_items"], list):
                state["action_items"] = []
            state["action_items"].append("Review and implement suggested planning steps")
        
        return state
    
    @with_api_key_rotation(max_retries=3, retry_delay=1.0)
    def _handle_technical(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Handle technical requests.
        
        Args:
            state: Current team state dictionary
            
        Returns:
            Updated state dictionary
        """
        team_info = state["team_info"]
        prompt = f"""You are a technical advisor for Team {team_info.get('name', 'Unknown')}.
        
        Team Project: {team_info.get('project_goal', 'Not specified')}
        Tech Stack: {team_info.get('tech_stack', 'Not specified')}
        
        The team asked: {state["message"]}
        
        Provide technical guidance, debugging help, implementation suggestions, or architectural advice.
        Be specific and include code examples or technical steps where helpful.
        """
        
        technical_response = self.llm.predict(prompt)
        state["current_context"] = f"Technical Context: {technical_response}"
        
        return state
    
    @with_api_key_rotation(max_retries=3, retry_delay=1.0)
    def _handle_coordination(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Handle team coordination requests.
        
        Args:
            state: Current team state dictionary
            
        Returns:
            Updated state dictionary
        """
        team_info = state["team_info"]
        prompt = f"""You are a team coordination specialist for Team {team_info.get('name', 'Unknown')}.
        
        Team Members: {', '.join(team_info.get('members', []))}
        Project: {team_info.get('project_goal', 'Not specified')}
        
        The team asked: {state["message"]}
        
        Help with task assignment, team coordination, role clarification, and workflow organization.
        Suggest specific assignments and coordination strategies.
        """
        
        coordination_response = self.llm.predict(prompt)
        state["current_context"] = f"Coordination Context: {coordination_response}"
        
        # Extract action items
        if "assign" in coordination_response.lower():
            if "action_items" not in state or not isinstance(state["action_items"], list):
                state["action_items"] = []
            state["action_items"].append("Follow suggested task assignments")
        
        return state
    
    @with_api_key_rotation(max_retries=3, retry_delay=1.0)
    def _generate_response(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the final response.
        
        Args:
            state: Current team state dictionary
            
        Returns:
            Updated state dictionary with final response
        """
        # Get conversation history
        conversation_id = f"team_{state['team_id']}"
        history = self.memory_manager.get_chat_history(conversation_id)
        
        # Format chat history for context
        # Limit to last 10 messages for better context
        recent_history = history[-10:] if len(history) > 10 else history
        history_text = "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in recent_history])
        
        # Get prompt template
        prompt_template = TeamPrompts.team_assistant_prompt()
        
        team_info = state["team_info"]
        final_prompt = prompt_template.format(
            team_name=team_info.get('name', 'Your Team'),
            team_description=team_info.get('description', 'No description'),
            project_goal=team_info.get('project_goal', 'Not specified'),
            team_members=', '.join(team_info.get('members', [])),
            current_sprint=team_info.get('current_sprint', 'Not specified'),
            chat_history=history_text,
            input=state["message"]
        )
        
        # Include specialized context if available
        if "current_context" in state and state["current_context"]:
            final_prompt += f"\n\nSpecialized Analysis: {state['current_context']}"
        
        # Add explicit instruction to use conversation history
        final_prompt += "\n\nIMPORTANT: Use the chat history to maintain context and provide a coherent response that builds on previous interactions."
        
        response = self.llm.predict(final_prompt)
        
        # Add action items if any
        if "action_items" in state and state["action_items"]:
            response += f"\n\n📋 **Action Items:**\n" + "\n".join(f"• {item}" for item in state["action_items"])
        
        # Set the response in the state
        state["response"] = response
        return state
    
    def process_team_message(self, team_id: str, message: str, team_info: Dict[str, Any]) -> Dict[str, Any]:
        """Process a team message using the LangGraph workflow.
        
        Args:
            team_id: Team ID
            message: Message from team
            team_info: Team information
            
        Returns:
            Response with workflow results
        """
        try:
            # Validate inputs
            if not team_id or not team_id.strip():
                return {
                    "success": False,
                    "error": "Team ID cannot be empty",
                    "response": "Please provide a valid team ID.",
                    "team_id": team_id
                }
            
            if not message or not message.strip():
                return {
                    "success": False,
                    "error": "Message cannot be empty",
                    "response": "Please provide a message for the team assistant to process.",
                    "team_id": team_id
                }
            
            if not isinstance(team_info, dict):
                team_info = {"name": "Unknown Team"}
            
            # Create conversation ID for memory storage
            conversation_id = f"team_{team_id}"
            
            # Save user message to memory BEFORE processing
            user_message = MessageSchema(
                content=message,
                sender_id=team_id,
                role="user"
            )
            self.memory_manager.add_message(conversation_id, user_message)
            
            # Get updated history after adding the user message
            history = self.memory_manager.get_chat_history(conversation_id)
            
            # Create initial state as dictionary
            initial_state = {
                "team_id": team_id.strip(),
                "message": message.strip(),
                "team_info": team_info,
                "conversation_history": history,
                "current_context": "",
                "response": "",
                "needs_planning": False,
                "needs_technical_help": False,
                "needs_coordination": False,
                "action_items": []
            }
            
            # Run the workflow
            final_state = self.workflow.invoke(initial_state)
            
            # Validate response
            response = final_state.get("response", "")
            if not response or not response.strip():
                response = "I processed your message but couldn't generate a proper response. Could you please rephrase your request?"
            
            # Save assistant response to memory
            assistant_message = MessageSchema(
                content=response,
                sender_id="team_assistant",
                role="assistant"
            )
            self.memory_manager.add_message(conversation_id, assistant_message)
            
            # Determine message type based on analysis
            message_type = "general"
            if final_state.get("needs_planning", False):
                message_type = "planning"
            elif final_state.get("needs_technical_help", False):
                message_type = "technical"
            elif final_state.get("needs_coordination", False):
                message_type = "coordination"
            
            # Create suggestions based on message type and content
            suggestions = []
            if message_type == "planning":
                suggestions = [
                    "Create sprint timeline", 
                    "Set up project milestones",
                    "Schedule planning meeting"
                ]
            elif message_type == "technical":
                suggestions = [
                    "Review technical architecture",
                    "Set up development environment",
                    "Create technical documentation"
                ]
            elif message_type == "coordination":
                suggestions = [
                    "Assign tasks to team members",
                    "Schedule team sync meeting",
                    "Update project board"
                ]
            
            return {
                "success": True,
                "response": response,
                "team_id": team_id,
                "message_type": message_type,
                "workflow_complete": True,
                "suggestions": suggestions,
                "workflow_analysis": {
                    "needs_planning": final_state.get("needs_planning", False),
                    "needs_technical_help": final_state.get("needs_technical_help", False),
                    "needs_coordination": final_state.get("needs_coordination", False),
                    "action_items": final_state.get("action_items", [])
                },
                "agent_type": "team_assistant_workflow",
                "processing_node": "responder"
            }
            
        except Exception as e:
            error_str = str(e)
            print(f"Error in process_team_message: {error_str}")
            
            # Provide user-friendly error messages
            if "429" in error_str or "quota" in error_str.lower():
                error_response = "🚫 I'm currently experiencing high demand due to API limits. Please try again in a few minutes."
            elif "timeout" in error_str.lower():
                error_response = "⏰ The request timed out while processing your team message. Please try again."
            else:
                error_response = f"I encountered an issue processing your team message: {error_str[:100]}... Please try again."
            
            return {
                "success": False,
                "error": error_str,
                "response": error_response,
                "team_id": team_id or "Unknown",
                "message_type": "error",
                "workflow_complete": False
            }
    
    def get_team_status(self, team_id: str) -> Dict[str, Any]:
        """Get team conversation status and insights.
        
        Args:
            team_id: Team ID
            
        Returns:
            Team status information
        """
        conversation_id = f"team_{team_id}"
        messages = self.memory_manager.get_messages(conversation_id)
        
        # Analyze recent activity
        recent_messages = messages[-10:] if len(messages) > 10 else messages
        
        return {
            "team_id": team_id,
            "total_messages": len(messages),
            "recent_activity": len(recent_messages),
            "conversation_active": len(messages) > 0,
            "last_interaction": messages[-1].timestamp.isoformat() if messages else None
        } 