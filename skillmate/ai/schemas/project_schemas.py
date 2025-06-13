"""
Schema definitions for project planning.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class Task(BaseModel):
    """Schema for a task in a sprint."""
    
    name: str
    description: str
    assignee: Optional[str] = None
    status: str = "todo"  # todo, in_progress, done
    priority: str = "medium"  # low, medium, high
    estimated_hours: Optional[int] = None
    dependencies: List[str] = []
    tags: List[str] = []


class Sprint(BaseModel):
    """Schema for a sprint in a project plan."""
    
    name: str
    start_date: str
    end_date: str
    goals: List[str] = []
    tasks: List[Task] = []
    deliverables: List[str] = []
    status: str = "planned"  # planned, in_progress, completed
    notes: Optional[str] = None


class ProjectPlan(BaseModel):
    """Schema for a complete project plan."""
    
    project_name: str
    project_description: str
    team_size: int
    duration: str
    tech_stack: List[str] = []
    team_members: List[str] = []
    requirements: Dict[str, Any] = {}
    architecture: Dict[str, Any] = {}
    sprints: List[Sprint] = []
    risks: List[Dict[str, Any]] = []
    resources: Dict[str, Any] = {}
    timeline: Dict[str, Any] = {}
    milestones: List[Dict[str, Any]] = []
    status: str = "planning"  # planning, in_progress, completed


class ProjectSchema(BaseModel):
    """Schema for project data."""
    
    team_name: str
    project_description: str
    team_size: int
    timeline: str
    team_members: List[str] = []
    tech_stack: Optional[List[str]] = None
    requirements: Optional[Dict[str, Any]] = None
    architecture: Optional[Dict[str, Any]] = None
    sprints: Optional[List[Dict[str, Any]]] = None
    risks: Optional[List[Dict[str, Any]]] = None
    resources: Optional[Dict[str, Any]] = None
    final_plan: Optional[str] = None


class PlanningState(BaseModel):
    """State for project planning workflow."""
    
    team_name: str
    project_description: str
    team_size: int
    timeline: str
    team_members: List[str] = []
    requirements: Dict[str, Any] = {}
    architecture: Dict[str, Any] = {}
    sprint_plan: List[Dict[str, Any]] = []
    risks: List[Dict[str, Any]] = []
    resources: Dict[str, Any] = {}
    final_plan: str = "" 