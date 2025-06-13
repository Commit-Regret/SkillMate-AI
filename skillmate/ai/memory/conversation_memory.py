"""
Conversation memory management for SkillMate AI.
"""

import json
import os
from typing import Dict, List, Optional, Any
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.schema import HumanMessage, AIMessage, SystemMessage

try:
    from ..config.settings import settings
    from ..schemas.message_schemas import MessageSchema, ConversationSchema
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config.settings import settings
    from schemas.message_schemas import MessageSchema, ConversationSchema


class ConversationMemoryManager:
    """Manages conversation memory for AI assistants."""
    
    def __init__(self, memory_type: str = None, token_limit: int = None):
        """Initialize the conversation memory manager.
        
        Args:
            memory_type: Type of memory to use ("buffer" or "summary")
            token_limit: Maximum number of tokens to store in memory
        """
        self.memory_type = memory_type or settings.memory_type
        self.token_limit = token_limit or settings.memory_token_limit
        self.conversations: Dict[str, ConversationSchema] = {}
        
        # Directory to store conversation history
        # Use an absolute path to ensure directory is accessible
        self.storage_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../conversation_storage"))
        
        # Ensure the storage directory exists
        try:
            os.makedirs(self.storage_dir, exist_ok=True)
            print(f"Conversation storage directory created at: {self.storage_dir}")
        except Exception as e:
            print(f"Error creating conversation storage directory: {e}")
            # Fallback to a different location if the primary location fails
            self.storage_dir = os.path.abspath("./conversation_storage")
            os.makedirs(self.storage_dir, exist_ok=True)
    
    def _get_memory_for_conversation(self, conversation_id: str) -> ConversationBufferMemory:
        """Get or create a LangChain memory object for a conversation.
        
        Args:
            conversation_id: Unique identifier for the conversation
            
        Returns:
            A ConversationBufferMemory or ConversationSummaryMemory instance
        """
        if self.memory_type == "summary":
            return ConversationSummaryMemory(
                llm=settings.llm,
                max_token_limit=self.token_limit,
                memory_key="chat_history",
                input_key="input",
            )
        else:  # Default to buffer memory
            return ConversationBufferMemory(
                memory_key="chat_history",
                input_key="input",
                return_messages=True,
                max_len=self.token_limit,
            )
    
    def get_conversation(self, conversation_id: str) -> ConversationSchema:
        """Get a conversation by ID, loading from disk if necessary.
        
        Args:
            conversation_id: Unique identifier for the conversation
            
        Returns:
            A ConversationSchema instance
        """
        if conversation_id not in self.conversations:
            # Try to load from disk
            conversation_path = os.path.join(self.storage_dir, f"{conversation_id}.json")
            if os.path.exists(conversation_path):
                with open(conversation_path, "r") as f:
                    data = json.load(f)
                    self.conversations[conversation_id] = ConversationSchema.from_dict(data)
            else:
                # Create new conversation
                self.conversations[conversation_id] = ConversationSchema(
                    conversation_id=conversation_id,
                    messages=[]
                )
        
        return self.conversations[conversation_id]
    
    def add_message(self, conversation_id: str, message: MessageSchema) -> None:
        """Add a new message to a conversation.
        
        Args:
            conversation_id: Unique identifier for the conversation
            message: Message to add to the conversation
        """
        conversation = self.get_conversation(conversation_id)
        conversation.add_message(message)
        self._save_conversation(conversation_id)
    
    def get_messages(self, conversation_id: str) -> List[MessageSchema]:
        """Get all messages in a conversation.
        
        Args:
            conversation_id: Unique identifier for the conversation
            
        Returns:
            List of messages in the conversation
        """
        conversation = self.get_conversation(conversation_id)
        return conversation.messages
    
    def get_chat_history(self, conversation_id: str) -> List[Dict[str, str]]:
        """Get chat history in a format suitable for LLM context.
        
        Args:
            conversation_id: Unique identifier for the conversation
            
        Returns:
            List of message dictionaries with role and content
        """
        conversation = self.get_conversation(conversation_id)
        return [{"role": msg.role, "content": msg.content} for msg in conversation.messages]
    
    def get_langchain_messages(self, conversation_id: str) -> List[Any]:
        """Get conversation messages in LangChain format.
        
        Args:
            conversation_id: Unique identifier for the conversation
            
        Returns:
            List of LangChain message objects
        """
        conversation = self.get_conversation(conversation_id)
        messages = []
        
        for msg in conversation.messages:
            if msg.role == "user":
                messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                messages.append(AIMessage(content=msg.content))
            elif msg.role == "system":
                messages.append(SystemMessage(content=msg.content))
        
        return messages
    
    def clear_conversation(self, conversation_id: str) -> None:
        """Clear a conversation's messages.
        
        Args:
            conversation_id: Unique identifier for the conversation
        """
        if conversation_id in self.conversations:
            self.conversations[conversation_id].messages = []
            self._save_conversation(conversation_id)
    
    def _save_conversation(self, conversation_id: str) -> None:
        """Save a conversation to disk.
        
        Args:
            conversation_id: Unique identifier for the conversation
        """
        if conversation_id in self.conversations:
            conversation_path = os.path.join(self.storage_dir, f"{conversation_id}.json")
            with open(conversation_path, "w") as f:
                json.dump(self.conversations[conversation_id].to_dict(), f, indent=2)
    
    def load_all_conversations(self) -> None:
        """Load all conversations from disk."""
        if not os.path.exists(self.storage_dir):
            return
        
        for filename in os.listdir(self.storage_dir):
            if filename.endswith(".json"):
                conversation_id = filename.replace(".json", "")
                conversation_path = os.path.join(self.storage_dir, filename)
                try:
                    with open(conversation_path, "r") as f:
                        data = json.load(f)
                        self.conversations[conversation_id] = ConversationSchema.from_dict(data)
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"Error loading conversation {conversation_id}: {e}")
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation.
        
        Args:
            conversation_id: Unique identifier for the conversation
            
        Returns:
            True if the conversation was deleted, False otherwise
        """
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            
            conversation_path = os.path.join(self.storage_dir, f"{conversation_id}.json")
            if os.path.exists(conversation_path):
                os.remove(conversation_path)
                return True
        
        return False 