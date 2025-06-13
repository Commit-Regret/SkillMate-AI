"""
User schemas for SkillMate AI system.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class Skill:
    """Schema for user skills."""
    
    name: str
    level: int = 1  # 1-5 scale
    years_experience: float = 0.0
    description: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert skill to dictionary format."""
        return {
            "name": self.name,
            "level": self.level,
            "years_experience": self.years_experience,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Skill":
        """Create a Skill instance from dictionary."""
        return cls(
            name=data["name"],
            level=data.get("level", 1),
            years_experience=data.get("years_experience", 0.0),
            description=data.get("description")
        )


@dataclass
class UserSchema:
    """Schema for user data."""
    
    user_id: str
    name: str
    skills: List[Skill] = field(default_factory=list)
    interests: List[str] = field(default_factory=list)
    bio: Optional[str] = None
    resume_vector: Optional[List[float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_skill(self, skill: Skill) -> None:
        """Add a new skill to the user."""
        self.skills.append(skill)
    
    def add_interest(self, interest: str) -> None:
        """Add a new interest to the user."""
        if interest not in self.interests:
            self.interests.append(interest)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary format."""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "skills": [skill.to_dict() for skill in self.skills],
            "interests": self.interests,
            "bio": self.bio,
            "resume_vector": self.resume_vector,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserSchema":
        """Create a UserSchema instance from dictionary."""
        skills = [Skill.from_dict(skill) for skill in data.get("skills", [])]
        
        return cls(
            user_id=data["user_id"],
            name=data["name"],
            skills=skills,
            interests=data.get("interests", []),
            bio=data.get("bio"),
            resume_vector=data.get("resume_vector"),
            metadata=data.get("metadata", {})
        ) 