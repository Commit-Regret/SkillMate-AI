"""
Prompt templates for project planning functionality.
"""

from langchain.prompts import PromptTemplate


class PlanningPrompts:
    """Prompt templates for project planning functionality."""
    
    @staticmethod
    def project_roadmap_prompt() -> PromptTemplate:
        """Generate the project roadmap prompt template.
        
        Returns:
            Prompt template for generating project roadmaps
        """
        template = """You are a project planning expert for the SkillMate platform. Create a comprehensive project roadmap for the following project:

PROJECT DETAILS:
Name: {project_name}
Description: {project_description}
Technology Stack: {tech_stack}
Team Size: {team_size}
Duration: {project_duration}
Complexity Level: {complexity_level}
Target Audience: {target_audience}

Create a detailed roadmap that includes:
1. Project phases with clear milestones
2. Technical architecture and setup requirements
3. Development tasks broken down by priority
4. Risk assessment and mitigation strategies
5. Resource allocation and team coordination
6. Quality assurance and testing phases
7. Deployment and launch considerations

Your roadmap should be realistic, accounting for the team size and duration constraints. Prioritize features that deliver maximum value with available resources.

FORMAT YOUR RESPONSE AS FOLLOWS:

# Project Roadmap: {project_name}

## Project Overview
- **Objective**: [Clear project goal]
- **Duration**: {project_duration}
- **Team**: {team_size} members
- **Tech Stack**: {tech_stack}
- **Complexity**: {complexity_level}

## Phase 1: Project Setup & Planning (Week 1)
**Goals**: [Phase objectives]

**Technical Setup**:
- [Setup task 1]
- [Setup task 2]
- [Setup task 3]

**Planning Tasks**:
- [Planning task 1]
- [Planning task 2]

**Deliverables**:
- [Deliverable 1]
- [Deliverable 2]

**Success Criteria**:
- [Criteria 1]
- [Criteria 2]

## Phase 2: Core Development (Week 2-3)
**Goals**: [Phase objectives]

**Development Tasks**:
- [High Priority]: [Task description] - [Team member role]
- [High Priority]: [Task description] - [Team member role]
- [Medium Priority]: [Task description] - [Team member role]

**Deliverables**:
- [Deliverable 1]
- [Deliverable 2]

**Success Criteria**:
- [Criteria 1]
- [Criteria 2]

## Phase 3: Feature Enhancement & Integration (Week 4)
**Goals**: [Phase objectives]

**Tasks**:
- [Task 1]
- [Task 2]
- [Task 3]

**Integration Points**:
- [Integration 1]
- [Integration 2]

## Phase 4: Testing & Optimization (Week 5)
**Goals**: [Phase objectives]

**Testing Strategy**:
- [Testing approach 1]
- [Testing approach 2]

**Optimization Tasks**:
- [Optimization 1]
- [Optimization 2]

## Phase 5: Deployment & Launch (Week 6)
**Goals**: [Phase objectives]

**Deployment Tasks**:
- [Deployment task 1]
- [Deployment task 2]

**Launch Checklist**:
- [Launch item 1]
- [Launch item 2]

## Risk Assessment & Mitigation

### High Risk Items
- **Risk**: [Risk description]
  - **Impact**: [Impact level]
  - **Mitigation**: [How to address]

### Medium Risk Items
- **Risk**: [Risk description]
  - **Mitigation**: [How to address]

## Resource Allocation
- **Frontend Development**: [Percentage]% - [Team members]
- **Backend Development**: [Percentage]% - [Team members]
- **Design/UX**: [Percentage]% - [Team members]
- **Testing/QA**: [Percentage]% - [Team members]

## Success Metrics
- [Metric 1]: [Target]
- [Metric 2]: [Target]
- [Metric 3]: [Target]
"""
        
        return PromptTemplate(
            template=template,
            input_variables=[
                "project_name", "project_description", "tech_stack", "team_size",
                "project_duration", "complexity_level", "target_audience"
            ]
        )
    
    @staticmethod
    def daily_standup_prompt() -> PromptTemplate:
        """Generate the daily standup facilitation prompt template.
        
        Returns:
            Prompt template for facilitating daily standups
        """
        template = """You are a standup facilitator for the SkillMate platform. Based on the team's current status and project information, generate structured standup discussion points.

TEAM INFORMATION:
Team Name: {team_name}
Project: {project_name}
Current Sprint: {current_sprint}
Sprint Goal: {sprint_goal}
Days Remaining in Sprint: {days_remaining}

RECENT ACTIVITY:
{recent_activity}

CURRENT BLOCKERS:
{current_blockers}

Generate a structured standup agenda that helps the team:
1. Share progress effectively
2. Identify and address blockers
3. Coordinate upcoming work
4. Stay aligned with sprint goals
5. Maintain team momentum

Focus on actionable discussions and concrete next steps.

FORMAT YOUR RESPONSE AS FOLLOWS:

# Daily Standup - {team_name}
**Date**: [Current date]
**Sprint**: {current_sprint}
**Goal**: {sprint_goal}
**Days Remaining**: {days_remaining}

## Progress Check-in
### What was accomplished yesterday?
- [Key accomplishments to discuss]
- [Team coordination points]

### What's planned for today?
- [Priority tasks for today]
- [Coordination needed]

### Are there any blockers?
- [Known blockers to address]
- [Potential issues to watch]

## Sprint Progress Review
- **Overall Progress**: [Assessment based on recent activity]
- **Sprint Goal Status**: [On track/At risk/Behind]
- **Key Metrics**: [Relevant progress indicators]

## Action Items
1. [Action item 1] - [Owner] - [Due date]
2. [Action item 2] - [Owner] - [Due date]
3. [Action item 3] - [Owner] - [Due date]

## Discussion Points
- [Important topic 1 for team discussion]
- [Important topic 2 for team discussion]

## Next Standup Focus
- [What to pay attention to tomorrow]
"""
        
        return PromptTemplate(
            template=template,
            input_variables=[
                "team_name", "project_name", "current_sprint", "sprint_goal",
                "days_remaining", "recent_activity", "current_blockers"
            ]
        )
    
    @staticmethod
    def retrospective_prompt() -> PromptTemplate:
        """Generate the sprint retrospective prompt template.
        
        Returns:
            Prompt template for facilitating sprint retrospectives
        """
        template = """You are a retrospective facilitator for the SkillMate platform. Help the team reflect on their sprint and identify improvements for future work.

SPRINT INFORMATION:
Team: {team_name}
Sprint: {sprint_name}
Duration: {sprint_duration}
Sprint Goal: {sprint_goal}
Goal Achievement: {goal_achievement}

SPRINT METRICS:
Completed Tasks: {completed_tasks}
Incomplete Tasks: {incomplete_tasks}
Blockers Encountered: {blockers_encountered}
Team Feedback: {team_feedback}

Generate a structured retrospective that helps the team:
1. Celebrate successes and wins
2. Identify what worked well
3. Discuss challenges and obstacles
4. Create actionable improvement plans
5. Strengthen team collaboration

Focus on constructive feedback and concrete action items.

FORMAT YOUR RESPONSE AS FOLLOWS:

# Sprint Retrospective - {sprint_name}
**Team**: {team_name}
**Sprint Goal**: {sprint_goal}
**Achievement**: {goal_achievement}

## Sprint Summary
- **Duration**: {sprint_duration}
- **Completed**: {completed_tasks} tasks
- **Remaining**: {incomplete_tasks} tasks
- **Goal Status**: [Assessment of goal achievement]

## What Went Well 🎉
### Team Strengths
- [Strength 1]: [Specific example]
- [Strength 2]: [Specific example]
- [Strength 3]: [Specific example]

### Process Wins
- [Process win 1]: [Impact]
- [Process win 2]: [Impact]

### Technical Successes
- [Technical success 1]: [Benefit]
- [Technical success 2]: [Benefit]

## What Could Be Improved 🔧
### Challenges Faced
- [Challenge 1]: [Impact and suggested improvement]
- [Challenge 2]: [Impact and suggested improvement]
- [Challenge 3]: [Impact and suggested improvement]

### Process Issues
- [Process issue 1]: [Suggested solution]
- [Process issue 2]: [Suggested solution]

### Technical Obstacles
- [Technical obstacle 1]: [How to address]
- [Technical obstacle 2]: [How to address]

## Key Learnings 📚
- [Learning 1]: [How to apply this knowledge]
- [Learning 2]: [How to apply this knowledge]
- [Learning 3]: [How to apply this knowledge]

## Action Items for Next Sprint
### High Priority
1. [Action item 1] - [Owner] - [Expected impact]
2. [Action item 2] - [Owner] - [Expected impact]

### Medium Priority
1. [Action item 3] - [Owner] - [Expected impact]
2. [Action item 4] - [Owner] - [Expected impact]

### Process Improvements
- [Process improvement 1]: [Implementation plan]
- [Process improvement 2]: [Implementation plan]

## Team Health Check
- **Communication**: [Assessment and recommendations]
- **Collaboration**: [Assessment and recommendations]
- **Workload Balance**: [Assessment and recommendations]
- **Technical Growth**: [Assessment and recommendations]

## Appreciation Corner 💙
[Recognize team members' contributions and effort]

## Next Sprint Focus
[Key areas to prioritize in the upcoming sprint]
"""
        
        return PromptTemplate(
            template=template,
            input_variables=[
                "team_name", "sprint_name", "sprint_duration", "sprint_goal",
                "goal_achievement", "completed_tasks", "incomplete_tasks",
                "blockers_encountered", "team_feedback"
            ]
        ) 