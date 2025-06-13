"""
Prompt templates for the Project Planner agent.
"""

from langchain.prompts import PromptTemplate

class PlannerPrompts:
    """Prompt templates for the Project Planner agent."""
    
    @staticmethod
    def requirements_analysis_prompt():
        """Get the prompt template for analyzing project requirements."""
        return """
        You are a SkillMate AI Project Planner, an expert in analyzing project requirements.
        
        Analyze the requirements for the following project:
        
        Team: {team_name}
        Project: {project_description}
        Team Size: {team_size}
        Timeline: {timeline}
        Team Members: {team_members}
        
        Provide a comprehensive analysis of:
        1. Core project requirements
        2. Technical requirements
        3. Resource requirements
        4. Potential challenges
        5. Key success factors
        
        Format your response in a clear, structured way with sections and bullet points.
        """
    
    @staticmethod
    def architecture_design_prompt():
        """Get the prompt template for designing project architecture."""
        return """
        You are a SkillMate AI Architecture Designer, an expert in designing technical architectures.
        
        Design a high-level architecture for the following project:
        
        Project: {project_description}
        Requirements: {requirements}
        Team Size: {team_size}
        Timeline: {timeline}
        
        Provide:
        1. System components and their interactions
        2. Technology stack recommendations
        3. Data flow diagram (in text form)
        4. API endpoints (if applicable)
        5. Deployment considerations
        
        Format your response in a clear, structured way with sections and bullet points.
        """
    
    @staticmethod
    def project_plan_prompt() -> PromptTemplate:
        """Get the project plan prompt template."""
        template = """You are a Project Planning Expert for SkillMate AI.

Create a comprehensive project plan for:

PROJECT: {project_name}
GOAL: {project_goal}
TEAM SIZE: {team_size} members
DURATION: {duration}

Use the following information to create a detailed, well-structured project plan:

CORE FEATURES:
{core_features}

ARCHITECTURE:
- Pattern: {architecture_pattern}
- Frontend: {frontend}
- Backend: {backend}
- Database: {database}

SPRINT PLAN:
{sprints}

RISKS:
{risks}

TEAM ROLES:
{team_roles}

Format the project plan in a clear, structured way using Markdown. Include:
1. Project overview and goals
2. Technical architecture diagram (described in text)
3. Sprint plan with timeline
4. Detailed tasks for each sprint
5. Risk assessment and mitigation strategies
6. Resource allocation and team structure
7. Success criteria and deliverables

Make the plan comprehensive yet practical for the team size and duration.
"""
        return PromptTemplate(
            template=template,
            input_variables=[
                "project_name", "project_goal", "team_size", "duration",
                "core_features", "architecture_pattern", "frontend", "backend", "database",
                "sprints", "risks", "team_roles"
            ]
        )
    
    @staticmethod
    def daily_standup_prompt() -> PromptTemplate:
        """Get the daily standup prompt template."""
        template = """You are a Scrum Master facilitating a daily standup for {team_name} working on {project_name}.

Current Sprint: {current_sprint}
Sprint Goal: {sprint_goal}
Days Remaining: {days_remaining}

Recent Activity:
{recent_activity}

Current Blockers:
{current_blockers}

Create a structured daily standup agenda with:
1. Brief summary of yesterday's progress
2. Today's focus areas and priorities
3. Identified blockers and proposed solutions
4. Any team coordination needs
5. Quick reminders about sprint goals and timeline

Keep it concise, actionable, and focused on moving the project forward.
"""
        return PromptTemplate(
            template=template,
            input_variables=[
                "team_name", "project_name", "current_sprint", "sprint_goal",
                "days_remaining", "recent_activity", "current_blockers"
            ]
        )
    
    @staticmethod
    def sprint_planning_prompt() -> PromptTemplate:
        """Get the sprint planning prompt template."""
        template = """You are a Project Manager planning sprints for {team_name} working on {project_name}.

Project Goal: {project_goal}
Team Size: {team_size}
Team Members: {team_members}
Project Duration: {project_duration}
Number of Sprints: {num_sprints}

Create a detailed sprint plan that includes:
1. Sprint breakdown with clear goals for each sprint
2. Key deliverables for each sprint
3. Task allocation considering team skills
4. Time estimates for major tasks
5. Dependencies between tasks
6. Testing and review processes

Format the sprint plan in a clear, structured way using Markdown.
"""
        return PromptTemplate(
            template=template,
            input_variables=[
                "team_name", "project_name", "project_goal", "team_size",
                "team_members", "project_duration", "num_sprints"
            ]
        )
    
    @staticmethod
    def risk_assessment_prompt() -> PromptTemplate:
        """Get the risk assessment prompt template."""
        template = """You are a Risk Management Expert assessing risks for {project_name}.

Project Goal: {project_goal}
Team Size: {team_size}
Duration: {duration}
Complexity: {complexity}

Identify and analyze potential risks for this project, including:
1. Technical risks
2. Schedule risks
3. Resource risks
4. External dependencies
5. Quality risks

For each risk, provide:
- Risk description
- Impact level (High/Medium/Low)
- Probability (High/Medium/Low)
- Mitigation strategy
- Contingency plan

Format the risk assessment in a clear, structured way using Markdown.
"""
        return PromptTemplate(
            template=template,
            input_variables=[
                "project_name", "project_goal", "team_size", "duration", "complexity"
            ]
        )
    
    @staticmethod
    def resource_allocation_prompt():
        """Get the prompt template for resource allocation."""
        return """
        You are a SkillMate AI Resource Allocator, an expert in optimizing project resources.
        
        Allocate resources for the following project:
        
        Project: {project_description}
        Sprint Plan: {sprint_plan}
        Team Size: {team_size}
        Timeline: {timeline}
        Team Members: {team_members}
        
        Provide a resource allocation plan including:
        1. Team member role assignments
        2. Time allocation per sprint
        3. Tool and technology requirements
        4. External resources needed
        5. Budget considerations (if applicable)
        
        Format your response in a clear, structured way with sections for different resource types.
        """
    
    @staticmethod
    def final_plan_prompt():
        """Get the prompt template for the final project plan."""
        return """
        You are a SkillMate AI Project Planner, an expert in creating comprehensive project plans.
        
        Create a final project plan for:
        
        Team: {team_name}
        Project: {project_description}
        Team Size: {team_size}
        Timeline: {timeline}
        Team Members: {team_members}
        
        Include:
        1. Executive Summary
        2. Project Scope
        3. Architecture Overview
        4. Sprint Plan
        5. Risk Management
        6. Resource Allocation
        7. Success Metrics
        8. Communication Plan
        
        Format your response as a professional project plan document with clear sections and subsections.
        """ 