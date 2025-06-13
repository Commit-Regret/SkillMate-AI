"""
Team schemas for SkillMate AI system.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class TeamMember:
    """Schema for team members."""
    
    user_id: str
    role: str = "member"  # "leader" or "member"
    joined_at: datetime = None
    
    def __post_init__(self):
        """Set default values for optional fields."""
        if self.joined_at is None:
            self.joined_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert team member to dictionary format."""
        return {
            "user_id": self.user_id,
            "role": self.role,
            "joined_at": self.joined_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TeamMember":
        """Create a TeamMember instance from dictionary."""
        joined_at = data.get("joined_at")
        if isinstance(joined_at, str):
            joined_at = datetime.fromisoformat(joined_at)
        
        return cls(
            user_id=data["user_id"],
            role=data.get("role", "member"),
            joined_at=joined_at
        )


@dataclass
class Sprint:
    """Schema for project sprints."""
    
    name: str
    start_date: datetime
    end_date: datetime
    goals: List[str] = field(default_factory=list)
    tasks: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert sprint to dictionary format."""
        return {
            "name": self.name,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "goals": self.goals,
            "tasks": self.tasks
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Sprint":
        """Create a Sprint instance from dictionary."""
        return cls(
            name=data["name"],
            start_date=datetime.fromisoformat(data["start_date"]),
            end_date=datetime.fromisoformat(data["end_date"]),
            goals=data.get("goals", []),
            tasks=data.get("tasks", [])
        )


@dataclass
class TeamSchema:
    """Schema for team data."""
    
    team_id: str
    name: str
    description: Optional[str] = None
    members: List[TeamMember] = field(default_factory=list)
    created_at: datetime = None
    project_goal: Optional[str] = None
    sprints: List[Sprint] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Set default values for optional fields."""
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def add_member(self, member: TeamMember) -> None:
        """Add a new member to the team."""
        self.members.append(member)
    
    def add_sprint(self, sprint: Sprint) -> None:
        """Add a new sprint to the team project."""
        self.sprints.append(sprint)
    
    def get_leader(self) -> Optional[TeamMember]:
        """Get the team leader."""
        for member in self.members:
            if member.role == "leader":
                return member
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert team to dictionary format."""
        return {
            "team_id": self.team_id,
            "name": self.name,
            "description": self.description,
            "members": [member.to_dict() for member in self.members],
            "created_at": self.created_at.isoformat(),
            "project_goal": self.project_goal,
            "sprints": [sprint.to_dict() for sprint in self.sprints],
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TeamSchema":
        """Create a TeamSchema instance from dictionary."""
        members = [TeamMember.from_dict(member) for member in data.get("members", [])]
        sprints = [Sprint.from_dict(sprint) for sprint in data.get("sprints", [])]
        created_at = data.get("created_at")
        
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        
        return cls(
            team_id=data["team_id"],
            name=data["name"],
            description=data.get("description"),
            members=members,
            created_at=created_at,
            project_goal=data.get("project_goal"),
            sprints=sprints,
            metadata=data.get("metadata", {})
        ) 