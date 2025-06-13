"""
Project Planner Agent for SkillMate platform.
Generates detailed project plans with tasks, timelines, and resources.
"""

from typing import Dict, Any, List, Optional
import logging
import json

# Set up logger
logger = logging.getLogger(__name__)

try:
    from ..config.settings import settings
    from ..prompts.planner_prompts import PlannerPrompts
    from ..schemas.project_schemas import ProjectPlan, Sprint, Task
    from ..config.model_provider import model_provider, with_api_key_rotation
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config.settings import settings
    from prompts.planner_prompts import PlannerPrompts
    from schemas.project_schemas import ProjectPlan, Sprint, Task
    from config.model_provider import model_provider, with_api_key_rotation


class ProjectPlannerAgent:
    """Project planner agent for generating comprehensive project plans."""
    
    def __init__(self):
        """Initialize the project planner agent."""
        # Create LLM using the model provider factory
        self.llm = model_provider.create_llm(
            model_type="planner",
            temperature=0.6
        )
    
    @with_api_key_rotation(max_retries=3, retry_delay=1.0)
    def _analyze_requirements(self, project_name: str, project_goal: str, team_size: int, duration: str) -> Dict[str, Any]:
        """Analyze project requirements and determine scope.
        
        Args:
            project_name: Name of the project
            project_goal: Goal of the project
            team_size: Size of the team
            duration: Project duration
            
        Returns:
            Dictionary with requirements analysis
        """
        prompt = f"""Analyze the project "{project_name}" with goal: "{project_goal}"

Team size: {team_size} members
Duration: {duration}

Break down the project into:
1. Core functional requirements (5-8 key features)
2. Technical requirements (APIs, databases, frameworks)
3. Non-functional requirements (performance, security, scalability)
4. Project complexity level (Low/Medium/High)

Format as:
**Core Features:**
- Feature 1: Description
- Feature 2: Description

**Technical Requirements:**
- Requirement 1
- Requirement 2

**Non-functional:**
- Performance targets
- Security considerations

**Complexity:** Low/Medium/High with justification"""
        
        try:
            response = self.llm.predict(prompt)
            
            # Parse requirements (simplified)
            requirements = {
                "core_features": [],
                "technical": [],
                "non_functional": [],
                "complexity": "medium"
            }
            
            lines = response.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if line.startswith('**Core Features:**'):
                    current_section = "core_features"
                elif line.startswith('**Technical Requirements:**'):
                    current_section = "technical"
                elif line.startswith('**Non-functional:**'):
                    current_section = "non_functional"
                elif line.startswith('**Complexity:**'):
                    if "low" in line.lower():
                        requirements["complexity"] = "low"
                    elif "high" in line.lower():
                        requirements["complexity"] = "high"
                    else:
                        requirements["complexity"] = "medium"
                elif line.startswith('-') and current_section:
                    req = line.lstrip('-').strip()
                    if req and current_section in requirements:
                        requirements[current_section].append(req)
            
            return requirements
            
        except Exception as e:
            logger.error(f"Error analyzing requirements: {e}")
            # Fallback requirements
            return {
                "core_features": [
                    f"Core functionality for {project_name}",
                    "User interface and experience",
                    "Data management",
                    "Core business logic"
                ],
                "technical": [
                    "API integration",
                    "Database storage",
                    "Authentication system"
                ],
                "non_functional": [
                    "Performance optimization",
                    "Security measures",
                    "Scalability considerations"
                ],
                "complexity": "medium"
            }
    
    @with_api_key_rotation(max_retries=3, retry_delay=1.0)
    def _design_architecture(self, project_name: str, project_goal: str, team_size: int, duration: str, complexity: str, tech_preferences: List[str] = None) -> Dict[str, Any]:
        """Design the technical architecture for the project.
        
        Args:
            project_name: Name of the project
            project_goal: Goal of the project
            team_size: Size of the team
            duration: Project duration
            complexity: Project complexity
            tech_preferences: Preferred technologies
            
        Returns:
            Dictionary with architecture design
        """
        tech_prefs = ", ".join(tech_preferences) if tech_preferences else "No specific preferences"
        
        prompt = f"""Design the technical architecture for "{project_name}":

Project Goal: {project_goal}
Team Size: {team_size}
Duration: {duration}
Complexity: {complexity}
Technology Preferences: {tech_prefs}

Provide:
1. Overall architecture pattern (MVC, Microservices, etc.)
2. Technology stack recommendations
3. Database design approach
4. API structure
5. Deployment strategy
6. Development workflow

Consider team size and timeline constraints. Recommend technologies suitable for a {duration} timeline with {team_size} developers."""
        
        try:
            response = self.llm.predict(prompt)
            
            # Parse architecture components
            architecture = {
                "pattern": "MVC",  # Default
                "frontend": [],
                "backend": [],
                "database": [],
                "deployment": [],
                "workflow": []
            }
            
            # Simple parsing to extract technology recommendations
            if "react" in response.lower():
                architecture["frontend"].append("React")
            if "vue" in response.lower():
                architecture["frontend"].append("Vue.js")
            if "angular" in response.lower():
                architecture["frontend"].append("Angular")
            if "node" in response.lower():
                architecture["backend"].append("Node.js")
            if "express" in response.lower():
                architecture["backend"].append("Express")
            if "python" in response.lower():
                architecture["backend"].append("Python")
            if "django" in response.lower():
                architecture["backend"].append("Django")
            if "flask" in response.lower():
                architecture["backend"].append("Flask")
            if "mongodb" in response.lower():
                architecture["database"].append("MongoDB")
            if "postgresql" in response.lower() or "postgres" in response.lower():
                architecture["database"].append("PostgreSQL")
            if "mysql" in response.lower():
                architecture["database"].append("MySQL")
            if "docker" in response.lower():
                architecture["deployment"].append("Docker")
            if "kubernetes" in response.lower() or "k8s" in response.lower():
                architecture["deployment"].append("Kubernetes")
            if "aws" in response.lower():
                architecture["deployment"].append("AWS")
            if "azure" in response.lower():
                architecture["deployment"].append("Azure")
            if "gcp" in response.lower() or "google cloud" in response.lower():
                architecture["deployment"].append("Google Cloud")
            if "agile" in response.lower():
                architecture["workflow"].append("Agile")
            if "scrum" in response.lower():
                architecture["workflow"].append("Scrum")
            if "kanban" in response.lower():
                architecture["workflow"].append("Kanban")
            if "ci/cd" in response.lower() or "continuous integration" in response.lower():
                architecture["workflow"].append("CI/CD")
                
            # Determine architecture pattern
            if "microservice" in response.lower():
                architecture["pattern"] = "Microservices"
            elif "serverless" in response.lower():
                architecture["pattern"] = "Serverless"
            elif "mvc" in response.lower():
                architecture["pattern"] = "MVC"
            elif "layered" in response.lower():
                architecture["pattern"] = "Layered Architecture"
            
            # Ensure we have at least some values
            if not architecture["frontend"]:
                architecture["frontend"] = ["React"]
            if not architecture["backend"]:
                architecture["backend"] = ["Node.js"]
            if not architecture["database"]:
                architecture["database"] = ["MongoDB"]
            if not architecture["deployment"]:
                architecture["deployment"] = ["Docker"]
            if not architecture["workflow"]:
                architecture["workflow"] = ["Agile"]
            
            return architecture
            
        except Exception as e:
            logger.error(f"Error designing architecture: {e}")
            # Fallback architecture
            return {
                "pattern": "MVC",
                "frontend": ["React"],
                "backend": ["Node.js"],
                "database": ["MongoDB"],
                "deployment": ["Docker"],
                "workflow": ["Agile"]
            }
    
    @with_api_key_rotation(max_retries=3, retry_delay=1.0)
    def _plan_sprints(self, project_name: str, project_goal: str, duration: str, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Plan the sprints for the project.
        
        Args:
            project_name: Name of the project
            project_goal: Goal of the project
            duration: Project duration
            requirements: Project requirements
            
        Returns:
            List of sprint plans
        """
        # Format requirements for prompt
        core_features = "\n".join([f"- {feature}" for feature in requirements.get("core_features", [])])
        
        prompt = f"""Create a sprint plan for the project "{project_name}" with goal: "{project_goal}"
Duration: {duration}

Core features to implement:
{core_features}

Break down the project into 2-4 sprints, each with:
1. Sprint name and duration
2. Sprint goals
3. Key deliverables
4. Main tasks to complete

Format as:
**Sprint 1: [Name] (X weeks)**
- Goals: goal1, goal2
- Deliverables: deliverable1, deliverable2
- Tasks:
  - Task 1: Description
  - Task 2: Description

**Sprint 2: [Name] (X weeks)**
...etc."""
        
        try:
            response = self.llm.predict(prompt)
            
            # Parse sprints
            sprints = []
            current_sprint = None
            current_section = None
            
            lines = response.split('\n')
            for line in lines:
                line = line.strip()
                
                if line.startswith('**Sprint'):
                    if current_sprint:
                        sprints.append(current_sprint)
                    
                    # Extract sprint name and duration
                    sprint_name = "Sprint"
                    duration = "2 weeks"
                    
                    if ":" in line:
                        sprint_name = line.split(':', 1)[1].split('(')[0].strip()
                    
                    if "(" in line and ")" in line:
                        duration = line.split('(')[1].split(')')[0].strip()
                    
                    current_sprint = {
                        "name": sprint_name,
                        "duration": duration,
                        "goals": [],
                        "deliverables": [],
                        "tasks": []
                    }
                    current_section = None
                    
                elif line.startswith('- Goals:'):
                    current_section = "goals"
                    goals = line.replace('- Goals:', '').strip()
                    current_sprint["goals"] = [g.strip() for g in goals.split(',') if g.strip()]
                    
                elif line.startswith('- Deliverables:'):
                    current_section = "deliverables"
                    deliverables = line.replace('- Deliverables:', '').strip()
                    current_sprint["deliverables"] = [d.strip() for d in deliverables.split(',') if d.strip()]
                    
                elif line.startswith('- Tasks:'):
                    current_section = "tasks"
                    
                elif line.startswith('  -') and current_section == "tasks" and current_sprint:
                    task = line.lstrip('- ').strip()
                    if task:
                        current_sprint["tasks"].append(task)
            
            # Add the last sprint
            if current_sprint:
                sprints.append(current_sprint)
            
            # Ensure we have at least one sprint
            if not sprints:
                sprints = [{
                    "name": "Sprint 1",
                    "duration": "2 weeks",
                    "goals": ["Initial implementation"],
                    "deliverables": ["Core functionality"],
                    "tasks": ["Set up project", "Implement basic features"]
                }]
            
            return sprints
            
        except Exception as e:
            logger.error(f"Error planning sprints: {e}")
            # Fallback sprint plan
            return [{
                "name": "Sprint 1: Setup",
                "duration": "2 weeks",
                "goals": ["Project setup", "Initial implementation"],
                "deliverables": ["Project structure", "Basic functionality"],
                "tasks": ["Set up development environment", "Implement core features"]
            }, {
                "name": "Sprint 2: Development",
                "duration": "2 weeks",
                "goals": ["Feature development"],
                "deliverables": ["Working prototype"],
                "tasks": ["Implement remaining features", "Testing"]
            }]
    
    @with_api_key_rotation(max_retries=3, retry_delay=1.0)
    def _assess_risks(self, project_name: str, project_goal: str, team_size: int, duration: str, complexity: str) -> List[Dict[str, Any]]:
        """Assess potential risks for the project.
        
        Args:
            project_name: Name of the project
            project_goal: Goal of the project
            team_size: Size of the team
            duration: Project duration
            complexity: Project complexity
            
        Returns:
            List of risk assessments
        """
        prompt = f"""Identify potential risks for the project "{project_name}" with goal: "{project_goal}"

Team size: {team_size} members
Duration: {duration}
Complexity: {complexity}

For each risk, provide:
1. Risk description
2. Impact level (Low/Medium/High)
3. Probability (Low/Medium/High)
4. Mitigation strategy

Format as:
**Risk 1: [Risk Name]**
- Description: Detailed description
- Impact: Low/Medium/High
- Probability: Low/Medium/High
- Mitigation: Strategy to mitigate

**Risk 2: [Risk Name]**
...etc."""
        
        try:
            response = self.llm.predict(prompt)
            
            # Parse risks
            risks = []
            current_risk = None
            
            lines = response.split('\n')
            for line in lines:
                line = line.strip()
                
                if line.startswith('**Risk'):
                    if current_risk:
                        risks.append(current_risk)
                    
                    risk_name = line.replace('**Risk', '').replace('**', '').strip()
                    if ":" in risk_name:
                        risk_name = risk_name.split(':', 1)[1].strip()
                    
                    current_risk = {
                        "name": risk_name,
                        "description": "",
                        "impact": "Medium",
                        "probability": "Medium",
                        "mitigation": ""
                    }
                    
                elif line.startswith('- Description:') and current_risk:
                    current_risk["description"] = line.replace('- Description:', '').strip()
                    
                elif line.startswith('- Impact:') and current_risk:
                    impact = line.replace('- Impact:', '').strip().lower()
                    if "high" in impact:
                        current_risk["impact"] = "High"
                    elif "low" in impact:
                        current_risk["impact"] = "Low"
                    else:
                        current_risk["impact"] = "Medium"
                        
                elif line.startswith('- Probability:') and current_risk:
                    probability = line.replace('- Probability:', '').strip().lower()
                    if "high" in probability:
                        current_risk["probability"] = "High"
                    elif "low" in probability:
                        current_risk["probability"] = "Low"
                    else:
                        current_risk["probability"] = "Medium"
                        
                elif line.startswith('- Mitigation:') and current_risk:
                    current_risk["mitigation"] = line.replace('- Mitigation:', '').strip()
            
            # Add the last risk
            if current_risk:
                risks.append(current_risk)
            
            return risks
            
        except Exception as e:
            logger.error(f"Error assessing risks: {e}")
            # Fallback risks
            return [{
                "name": "Timeline Risk",
                "description": "Project might take longer than expected",
                "impact": "High",
                "probability": "Medium",
                "mitigation": "Regular progress tracking and adjusting scope if necessary"
            }, {
                "name": "Technical Risk",
                "description": "Technical challenges might arise during development",
                "impact": "Medium",
                "probability": "Medium",
                "mitigation": "Research technical solutions early and have backup plans"
            }]
    
    @with_api_key_rotation(max_retries=3, retry_delay=1.0)
    def _allocate_resources(self, project_name: str, team_size: int, duration: str, architecture: Dict[str, Any]) -> Dict[str, Any]:
        """Allocate resources for the project.
        
        Args:
            project_name: Name of the project
            team_size: Size of the team
            duration: Project duration
            architecture: Project architecture
            
        Returns:
            Dictionary with resource allocation
        """
        # Format architecture for prompt
        frontend = ", ".join(architecture.get("frontend", []))
        backend = ", ".join(architecture.get("backend", []))
        database = ", ".join(architecture.get("database", []))
        
        prompt = f"""Allocate resources for the project "{project_name}"

Team size: {team_size} members
Duration: {duration}
Frontend technologies: {frontend}
Backend technologies: {backend}
Database: {database}

Provide:
1. Team roles and responsibilities
2. Development environment setup
3. Required tools and software
4. Timeline allocation
5. Budget considerations (if applicable)

Format as clear sections with bullet points."""
        
        try:
            response = self.llm.predict(prompt)
            
            # Parse resource allocation (simplified)
            resources = {
                "team_roles": [],
                "development_environment": [],
                "tools": [],
                "timeline": {},
                "budget": {}
            }
            
            # Simple extraction of roles based on team size
            if team_size >= 1:
                resources["team_roles"].append("Project Manager")
            if team_size >= 2:
                resources["team_roles"].append("Frontend Developer")
            if team_size >= 3:
                resources["team_roles"].append("Backend Developer")
            if team_size >= 4:
                resources["team_roles"].append("UI/UX Designer")
            if team_size >= 5:
                resources["team_roles"].append("QA Engineer")
            if team_size >= 6:
                resources["team_roles"].append("DevOps Engineer")
            
            # Extract development environment and tools from response
            if "vs code" in response.lower() or "vscode" in response.lower():
                resources["development_environment"].append("VS Code")
            if "intellij" in response.lower():
                resources["development_environment"].append("IntelliJ IDEA")
            if "git" in response.lower():
                resources["tools"].append("Git")
            if "github" in response.lower():
                resources["tools"].append("GitHub")
            if "gitlab" in response.lower():
                resources["tools"].append("GitLab")
            if "jira" in response.lower():
                resources["tools"].append("Jira")
            if "trello" in response.lower():
                resources["tools"].append("Trello")
            if "slack" in response.lower():
                resources["tools"].append("Slack")
            if "docker" in response.lower():
                resources["tools"].append("Docker")
            
            # Ensure we have at least some values
            if not resources["development_environment"]:
                resources["development_environment"] = ["VS Code", "Terminal"]
            if not resources["tools"]:
                resources["tools"] = ["Git", "GitHub", "Slack"]
            
            return resources
            
        except Exception as e:
            logger.error(f"Error allocating resources: {e}")
            # Fallback resources
            return {
                "team_roles": ["Project Manager", "Frontend Developer", "Backend Developer"],
                "development_environment": ["VS Code", "Terminal"],
                "tools": ["Git", "GitHub", "Slack"],
                "timeline": {"planning": "20%", "development": "60%", "testing": "20%"},
                "budget": {"development": "70%", "tools": "20%", "contingency": "10%"}
            }
    
    @with_api_key_rotation(max_retries=3, retry_delay=1.0)
    def _compose_final_plan(self, project_name: str, project_goal: str, team_size: int, duration: str,
                          requirements: Dict[str, Any], architecture: Dict[str, Any],
                          sprints: List[Dict[str, Any]], risks: List[Dict[str, Any]],
                          resources: Dict[str, Any]) -> str:
        """Compose the final project plan.
        
        Args:
            project_name: Name of the project
            project_goal: Goal of the project
            team_size: Size of the team
            duration: Project duration
            requirements: Project requirements
            architecture: Project architecture
            sprints: Sprint plans
            risks: Risk assessments
            resources: Resource allocation
            
        Returns:
            Final project plan as formatted text
        """
        prompt = PlannerPrompts.project_plan_prompt().format(
            project_name=project_name,
            project_goal=project_goal,
            team_size=team_size,
            duration=duration,
            core_features="\n".join([f"- {feature}" for feature in requirements.get("core_features", [])]),
            architecture_pattern=architecture.get("pattern", "MVC"),
            frontend=", ".join(architecture.get("frontend", [])),
            backend=", ".join(architecture.get("backend", [])),
            database=", ".join(architecture.get("database", [])),
            sprints="\n".join([f"- Sprint {i+1}: {sprint['name']} ({sprint['duration']})" for i, sprint in enumerate(sprints)]),
            risks="\n".join([f"- {risk['name']}: {risk['impact']} impact, {risk['probability']} probability" for risk in risks[:3]]),
            team_roles=", ".join(resources.get("team_roles", []))
        )
        
        try:
            final_plan = self.llm.predict(prompt)
            return final_plan
        except Exception as e:
            logger.error(f"Error composing final plan: {e}")
            # Fallback plan
            return f"""# Project Plan: {project_name}

## Project Overview
- Goal: {project_goal}
- Team Size: {team_size}
- Duration: {duration}

## Requirements
- Core Features: {', '.join(requirements.get('core_features', [])[:3])}
- Technical Requirements: {', '.join(requirements.get('technical', [])[:3])}

## Architecture
- Pattern: {architecture.get('pattern', 'MVC')}
- Frontend: {', '.join(architecture.get('frontend', []))}
- Backend: {', '.join(architecture.get('backend', []))}
- Database: {', '.join(architecture.get('database', []))}

## Sprint Plan
{chr(10).join([f"- Sprint {i+1}: {sprint['name']} ({sprint['duration']})" for i, sprint in enumerate(sprints)])}

## Risks and Mitigations
{chr(10).join([f"- {risk['name']}: {risk['impact']} impact, {risk['probability']} probability" for risk in risks[:3]])}

## Resource Allocation
- Team Roles: {', '.join(resources.get('team_roles', []))}
- Tools: {', '.join(resources.get('tools', []))}"""
    
    def create_project_plan(self, project_name: str, project_goal: str, 
                           team_size: int = 4, duration: str = "4 weeks",
                           tech_preferences: List[str] = None) -> Dict[str, Any]:
        """Create a comprehensive project plan.
        
        Args:
            project_name: Name of the project
            project_goal: Goal of the project
            team_size: Size of the team
            duration: Project duration
            tech_preferences: Preferred technologies
            
        Returns:
            Dictionary containing the project plan and its components
        """
        try:
            # Step 1: Analyze requirements
            requirements = self._analyze_requirements(project_name, project_goal, team_size, duration)
            
            # Step 2: Design architecture
            architecture = self._design_architecture(
                project_name, project_goal, team_size, duration,
                requirements.get("complexity", "medium"), tech_preferences
            )
            
            # Step 3: Plan sprints
            sprints = self._plan_sprints(project_name, project_goal, duration, requirements)
            
            # Step 4: Assess risks
            risks = self._assess_risks(
                project_name, project_goal, team_size, duration,
                requirements.get("complexity", "medium")
            )
            
            # Step 5: Allocate resources
            resources = self._allocate_resources(project_name, team_size, duration, architecture)
            
            # Step 6: Compose final plan
            final_plan = self._compose_final_plan(
                project_name, project_goal, team_size, duration,
                requirements, architecture, sprints, risks, resources
            )
            
            # Create project plan object
            project_plan = {
                "project_name": project_name,
                "project_goal": project_goal,
                "team_size": team_size,
                "duration": duration,
                "requirements": requirements,
                "architecture": architecture,
                "sprints": sprints,
                "risks": risks,
                "resources": resources,
                "final_plan": final_plan
            }
            
            return {
                "success": True,
                "project_plan": project_plan
            }
            
        except Exception as e:
            logger.error(f"Error creating project plan: {e}")
            return {
                "success": False,
                "error": str(e),
                "project_name": project_name,
                "project_goal": project_goal
            }
    
    def generate_daily_standup(self, team_id: str, project_name: str, 
                              recent_activity: str = "", current_blockers: str = "") -> Dict[str, Any]:
        """Generate a daily standup report.
        
        Args:
            team_id: ID of the team
            project_name: Name of the project
            recent_activity: Recent team activity
            current_blockers: Current blockers
            
        Returns:
            Dictionary with standup report
        """
        try:
            prompt = f"""Generate a daily standup report for the project "{project_name}".

Recent team activity:
{recent_activity}

Current blockers:
{current_blockers}

Include:
1. Summary of yesterday's progress
2. Today's plan
3. Blockers and how to address them
4. Any team coordination needed

Format as a clear, concise standup report."""
            
            standup_report = self.llm.predict(prompt)
            
            return {
                "success": True,
                "team_id": team_id,
                "project_name": project_name,
                "standup_report": standup_report
            }
            
        except Exception as e:
            logger.error(f"Error generating daily standup: {e}")
            return {
                "success": False,
                "error": str(e),
                "team_id": team_id,
                "project_name": project_name
            }
    
    def generate_project_plan(self, team_name: str, project_description: str, 
                             team_members: List[str], team_size: int, 
                             timeline: str) -> Dict[str, Any]:
        """Generate a project plan for a team.
        
        Args:
            team_name: Name of the team
            project_description: Description of the project
            team_members: List of team members
            team_size: Size of the team
            timeline: Project timeline
            
        Returns:
            Dictionary with project plan
        """
        # This is a wrapper around create_project_plan for compatibility
        return self.create_project_plan(
            project_name=team_name,
            project_goal=project_description,
            team_size=team_size,
            duration=timeline
        ) 