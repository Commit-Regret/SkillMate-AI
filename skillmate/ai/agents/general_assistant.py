"""
General AI Assistant for SkillMate platform.
"""

from typing import Dict, Any, Optional
import logging
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
    from ..prompts.assistant_prompts import AssistantPrompts
    from ..schemas.message_schemas import MessageSchema
    from ..config.model_provider import model_provider, with_api_key_rotation
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config.settings import settings
    from memory.conversation_memory import ConversationMemoryManager
    from prompts.assistant_prompts import AssistantPrompts
    from schemas.message_schemas import MessageSchema
    from config.model_provider import model_provider, with_api_key_rotation


class GeneralAssistantAgent:
    """General AI assistant for the SkillMate platform."""
    
    def __init__(self, memory_manager: Optional[ConversationMemoryManager] = None):
        """Initialize the general assistant agent.
        
        Args:
            memory_manager: Optional memory manager instance
        """
        # Create LLM using the model provider factory
        self.llm = model_provider.create_llm(
            model_type="general_assistant",
            temperature=0.7
        )
        
        self.memory_manager = memory_manager or ConversationMemoryManager()
        self.prompt_template = AssistantPrompts.general_assistant_prompt()
        
        # Cache for conversation chains to avoid recreating them
        self._conversation_chains: Dict[str, ConversationChain] = {}
    
    def _get_conversation_chain(self, user_id: str) -> ConversationChain:
        """Get or create a conversation chain for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            ConversationChain instance
        """
        if user_id not in self._conversation_chains:
            # Get chat history from memory manager
            chat_history = self.memory_manager.get_chat_history(user_id)
            
            # Create memory with existing history
            memory = ConversationBufferMemory(
                memory_key="chat_history",
                input_key="input",
                return_messages=True
            )
            
            # Add existing messages to memory
            for msg in chat_history:
                if msg["role"] == "user":
                    memory.chat_memory.add_user_message(msg["content"])
                elif msg["role"] == "assistant":
                    memory.chat_memory.add_ai_message(msg["content"])
            
            # Create conversation chain
            self._conversation_chains[user_id] = ConversationChain(
                llm=self.llm,
                prompt=self.prompt_template,
                memory=memory,
                verbose=False
            )
        
        return self._conversation_chains[user_id]
    
    @with_api_key_rotation(max_retries=3, retry_delay=1.0)
    def generate_response(self, user_id: str, message: str) -> str:
        """Generate a response to a user's message.
        
        This method is decorated with @with_api_key_rotation to automatically
        handle API quota errors by rotating to a different API key.
        
        Args:
            user_id: User ID
            message: User's message
            
        Returns:
            AI assistant's response
        """
        try:
            # Validate input
            if not message or not message.strip():
                return "⚠️ Please provide a message for me to respond to."
            
            # Add user message to memory
            user_message = MessageSchema(
                content=message,
                sender_id=user_id,
                role="user"
            )
            self.memory_manager.add_message(user_id, user_message)
            
            # Get conversation chain and generate response
            chain = self._get_conversation_chain(user_id)
            response = chain.predict(input=message)
            
            # Validate response
            if not response or not response.strip():
                response = "I apologize, but I wasn't able to generate a proper response. Could you please rephrase your question?"
            
            # Add assistant response to memory
            assistant_message = MessageSchema(
                content=response,
                sender_id="assistant",
                role="assistant"
            )
            self.memory_manager.add_message(user_id, assistant_message)
            
            return response
            
        except Exception as e:
            error_str = str(e)
            print(f"Error in GeneralAssistantAgent.generate_response: {error_str}")
            
            # Provide user-friendly error messages based on error type
            if "429" in error_str or "quota" in error_str.lower() or "insufficient_quota" in error_str.lower():
                error_message = "🚫 I'm currently experiencing high demand due to API limits. Please try again in a few minutes."
            elif "401" in error_str or "authentication" in error_str.lower():
                error_message = "🔑 There's an authentication issue with the API. Please check your API key configuration."
            elif "404" in error_str or "model" in error_str.lower():
                error_message = "🤖 The requested AI model is not available. Please contact support."
            elif "rate_limit" in error_str.lower():
                error_message = "⏱️ I'm processing requests too quickly. Please wait a moment and try again."
            elif "timeout" in error_str.lower():
                error_message = "⏰ The request timed out. Please try again."
            else:
                error_message = f"⚠️ I encountered a technical issue while processing your request: {error_str[:100]}... Please try again in a moment."
            
            return error_message
    
    def get_conversation_history(self, user_id: str, limit: Optional[int] = None) -> list:
        """Get conversation history for a user.
        
        Args:
            user_id: User ID
            limit: Optional limit on number of messages to return
            
        Returns:
            List of conversation messages
        """
        messages = self.memory_manager.get_messages(user_id)
        
        if limit:
            messages = messages[-limit:]
        
        return [msg.to_dict() for msg in messages]
    
    def clear_conversation(self, user_id: str) -> bool:
        """Clear conversation history for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            True if conversation was cleared successfully
        """
        try:
            self.memory_manager.clear_conversation(user_id)
            
            # Remove cached conversation chain
            if user_id in self._conversation_chains:
                del self._conversation_chains[user_id]
            
            return True
            
        except Exception as e:
            print(f"Error clearing conversation for user {user_id}: {e}")
            return False
    
    def get_assistant_info(self) -> Dict[str, Any]:
        """Get information about the assistant.
        
        Returns:
            Dictionary with assistant information
        """
        return {
            "name": "SkillMate AI Assistant",
            "description": "A helpful AI assistant for the SkillMate platform",
            "capabilities": [
                "General conversation and assistance",
                "Technical guidance and questions",
                "Project idea suggestions",
                "Career and skill development advice",
                "Resume improvement suggestions",
                "Team collaboration support"
            ],
            "provider": model_provider.get_provider(),
            "model": model_provider.get_model_name("general_assistant"),
            "memory_type": "conversation_buffer"
        }
    
    def suggest_project_ideas(self, skills: list, interests: list, team_size: int = 4, 
                             time_constraint: str = "1 week", domain: str = "hackathon",
                             num_ideas: int = 3) -> str:
        """Generate project ideas based on skills and interests.
        
        Args:
            skills: List of skills
            interests: List of interests
            team_size: Size of the team
            time_constraint: Time available for the project
            domain: Domain or context for the project
            num_ideas: Number of ideas to generate
            
        Returns:
            Generated project ideas
        """
        try:
            prompt = AssistantPrompts.project_idea_prompt()
            
            formatted_prompt = prompt.format(
                skills=", ".join(skills),
                interests=", ".join(interests),
                team_size=team_size,
                time_constraint=time_constraint,
                domain=domain,
                num_ideas=num_ideas
            )
            
            # Use the LLM directly for this one-off interaction
            response = self.llm.predict(formatted_prompt)
            return response
            
        except Exception as e:
            error_str = str(e)
            print(f"Error in GeneralAssistantAgent.suggest_project_ideas: {error_str}")
            return f"⚠️ I encountered an issue while generating project ideas: {error_str[:100]}... Please try again in a moment." 