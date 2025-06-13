"""
Message schemas for SkillMate AI system.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any, Literal


@dataclass
class MessageSchema:
    """Schema for chat messages in the system."""
    
    content: str
    sender_id: str
    timestamp: datetime = None
    role: Literal["user", "assistant", "system"] = "user"
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Set default values for optional fields."""
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary format."""
        return {
            "content": self.content,
            "sender_id": self.sender_id,
            "timestamp": self.timestamp.isoformat(),
            "role": self.role,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MessageSchema":
        """Create a MessageSchema instance from dictionary."""
        timestamp = data.get("timestamp")
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        
        return cls(
            content=data["content"],
            sender_id=data["sender_id"],
            timestamp=timestamp,
            role=data.get("role", "user"),
            metadata=data.get("metadata", {})
        )


@dataclass
class ConversationSchema:
    """Schema for storing conversation history."""
    
    conversation_id: str
    messages: List[MessageSchema]
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Set default values for optional fields."""
        if self.metadata is None:
            self.metadata = {}
    
    def add_message(self, message: MessageSchema) -> None:
        """Add a new message to the conversation."""
        self.messages.append(message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert conversation to dictionary format."""
        return {
            "conversation_id": self.conversation_id,
            "messages": [msg.to_dict() for msg in self.messages],
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConversationSchema":
        """Create a ConversationSchema instance from dictionary."""
        messages = [MessageSchema.from_dict(msg) for msg in data.get("messages", [])]
        
        return cls(
            conversation_id=data["conversation_id"],
            messages=messages,
            metadata=data.get("metadata", {})
        ) 