"""
Prompt templates for the Roadmap Generator agent.
"""

from langchain.prompts import PromptTemplate

class RoadmapPrompts:
    """Prompt templates for the Roadmap Generator agent."""
    
    @staticmethod
    def roadmap_generator_prompt() -> PromptTemplate:
        """Get the roadmap generator prompt template."""
        template = """You are a Learning Path Expert specializing in creating comprehensive roadmaps for skill development.

Create a detailed learning roadmap for: {skill}

Your roadmap should include:
1. Prerequisites and foundational knowledge
2. Learning phases from beginner to advanced
3. Recommended resources (courses, books, tutorials)
4. Practice projects for each phase
5. Estimated time commitment
6. Success metrics for each phase

Format the roadmap in a clear, structured way using Markdown.
"""
        return PromptTemplate(template=template, input_variables=["skill"])

    @staticmethod
    def roadmap_composition_prompt() -> PromptTemplate:
        """Get the roadmap composition prompt template."""
        template = """You are a Learning Path Expert specializing in creating comprehensive roadmaps for skill development.

Create a detailed learning roadmap for: {skill}

User's current level: {user_level}
Time commitment: {time_commitment}

Use the following information to create a comprehensive, well-structured roadmap:

PREREQUISITES:
{prerequisites}

LEARNING PHASES:
{phases}

RESOURCES:
{resources}

PROJECTS:
{projects}

Format the roadmap in a clear, structured way using Markdown. Include:
1. An introduction explaining the roadmap's purpose
2. Prerequisites section
3. Learning path with clear phases
4. Recommended resources organized by type
5. Practice projects with difficulty levels
6. Estimated timelines based on the user's time commitment
7. Success metrics for each phase

Make the roadmap visually organized, easy to follow, and motivating.
"""
        return PromptTemplate(
            template=template, 
            input_variables=["skill", "user_level", "time_commitment", "prerequisites", "phases", "resources", "projects"]
        )
    
    @staticmethod
    def skill_analysis_prompt():
        """Get the prompt template for analyzing a skill."""
        return """
        You are a SkillMate AI Learning Advisor, an expert in analyzing learning requirements.
        
        Analyze the following skill: {skill}
        
        Consider:
        - What domain does this skill belong to?
        - What are the core components of this skill?
        - What related skills might complement this?
        - What are common misconceptions about learning this skill?
        - What makes this skill challenging for beginners?
        
        Provide a concise analysis that helps understand the nature and scope of this skill.
        """
    
    @staticmethod
    def prerequisite_finder_prompt():
        """Get the prompt template for finding prerequisites for a skill."""
        return """
        You are a SkillMate AI Learning Advisor, an expert in identifying prerequisite knowledge.
        
        Identify the essential prerequisites for learning: {skill}
        
        For a {user_level} with {time_commitment} time commitment.
        
        List 3-7 specific prerequisites that are truly necessary before starting to learn this skill.
        For each prerequisite, briefly explain why it's important and how it relates to {skill}.
        
        Format as a bulleted list.
        """
    
    @staticmethod
    def learning_phases_prompt():
        """Get the prompt template for planning learning phases."""
        return """
        You are a SkillMate AI Learning Advisor, an expert in structuring learning journeys.
        
        Create a phase-by-phase learning plan for: {skill}
        
        For a {user_level} with {time_commitment} time commitment.
        
        Break the learning journey into 4-6 distinct phases, from fundamentals to mastery.
        For each phase:
        - Give it a clear name
        - Describe what will be learned
        - List specific topics to cover
        - Explain how to know when to move to the next phase
        
        Format each phase with a clear header and structured content.
        """
    
    @staticmethod
    def resource_curator_prompt():
        """Get the prompt template for curating learning resources."""
        return """
        You are a SkillMate AI Resource Curator, an expert in finding the best learning materials.
        
        Recommend high-quality learning resources for: {skill}
        
        For a {user_level} with {time_commitment} time commitment.
        
        Include a diverse mix of:
        - Books (2-3 essential ones)
        - Online courses (2-3 options, including free and paid)
        - Tutorials and documentation
        - Communities and forums
        - YouTube channels or specific videos
        - Blogs and websites
        
        For each resource, briefly explain why it's valuable and what makes it suitable for the user's level.
        Organize resources by category with clear headers.
        """
    
    @staticmethod
    def project_suggester_prompt():
        """Get the prompt template for suggesting practice projects."""
        return """
        You are a SkillMate AI Project Advisor, an expert in designing practical learning experiences.
        
        Suggest progressive practice projects for learning: {skill}
        
        For a {user_level} with {time_commitment} time commitment.
        
        Create 5-7 project ideas that:
        - Start simple and gradually increase in complexity
        - Apply key concepts from different learning phases
        - Are engaging and practical
        - Can be completed within a reasonable timeframe
        
        For each project:
        - Give it a specific, descriptive name
        - Explain the project goal
        - List key skills practiced
        - Suggest extensions or variations
        
        Format each project with a clear header and structured content.
        """ 