"""
Roadmap Generator Agent for SkillMate platform.
Generates learning roadmaps for skills and technologies.
"""

from typing import Dict, Any, List, Optional
import logging
import json

# Set up logger
logger = logging.getLogger(__name__)

try:
    from ..config.settings import settings
    from ..prompts.roadmap_prompts import RoadmapPrompts
    from ..config.model_provider import model_provider, with_api_key_rotation
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config.settings import settings
    from prompts.roadmap_prompts import RoadmapPrompts
    from config.model_provider import model_provider, with_api_key_rotation


class RoadmapGeneratorAgent:
    """Roadmap generator agent for creating skill learning paths."""
    
    def __init__(self):
        """Initialize the roadmap generator agent."""
        # Create LLM using the model provider factory
        self.llm = model_provider.create_llm(
            model_type="planner",
            temperature=0.7
        )
    
    @with_api_key_rotation(max_retries=3, retry_delay=1.0)
    def _analyze_skill(self, skill: str) -> Dict[str, Any]:
        """Analyze the skill and determine its complexity and domain.
        
        Args:
            skill: The skill to analyze
            
        Returns:
            Dictionary with skill analysis
        """
        prompt = f"""Analyze the skill "{skill}" and provide:
1. Domain classification (e.g., Programming, Design, Data Science, etc.)
2. Complexity level (Beginner-friendly, Intermediate, Advanced)
3. Key sub-skills involved
4. Industry relevance and applications

Respond in JSON format:
{{
    "domain": "domain_name",
    "complexity": "level",
    "sub_skills": ["skill1", "skill2"],
    "applications": ["app1", "app2"]
}}"""
        
        try:
            response = self.llm.predict(prompt)
            # Try to parse JSON response
            try:
                return json.loads(response)
            except:
                # Return basic structure if parsing fails
                return {
                    "domain": "Technology",
                    "complexity": "Intermediate",
                    "sub_skills": [f"{skill} fundamentals"],
                    "applications": ["Various industries"]
                }
        except Exception as e:
            logger.error(f"Error analyzing skill: {e}")
            return {
                "domain": "Technology",
                "complexity": "Intermediate",
                "sub_skills": [f"{skill} fundamentals"],
                "applications": ["Various industries"]
            }
    
    @with_api_key_rotation(max_retries=3, retry_delay=1.0)
    def _find_prerequisites(self, skill: str) -> List[str]:
        """Find prerequisites for the skill.
        
        Args:
            skill: The skill to find prerequisites for
            
        Returns:
            List of prerequisites
        """
        prompt = f"""What are the essential prerequisites for learning "{skill}"?
List 3-5 foundational concepts or skills someone should know before starting.
Include both technical and general prerequisites.

Format as a simple list:
- Prerequisite 1
- Prerequisite 2
- etc."""
        
        try:
            response = self.llm.predict(prompt)
            # Extract prerequisites (simplified parsing)
            prerequisites = []
            lines = response.split('\n')
            for line in lines:
                if line.strip().startswith('-') or line.strip().startswith('•'):
                    prereq = line.strip().lstrip('-•').strip()
                    if prereq:
                        prerequisites.append(prereq)
            
            return prerequisites[:5]  # Limit to 5
        except Exception as e:
            logger.error(f"Error finding prerequisites: {e}")
            return [f"Basic understanding related to {skill}"]
    
    @with_api_key_rotation(max_retries=3, retry_delay=1.0)
    def _plan_learning_phases(self, skill: str, user_level: str) -> List[Dict[str, Any]]:
        """Plan the learning phases for the skill.
        
        Args:
            skill: The skill to plan phases for
            user_level: User's current level
            
        Returns:
            List of learning phases
        """
        prompt = f"""Create a structured learning plan for "{skill}" with 4 phases:
1. Foundation Phase (Beginner)
2. Building Phase (Intermediate)
3. Mastery Phase (Advanced)
4. Specialization Phase (Expert)

For each phase, specify:
- Duration estimate
- Key concepts to learn
- Skills to develop
- Success criteria

Format as:
Phase 1: Foundation (X weeks)
- Key concepts: concept1, concept2
- Skills: skill1, skill2
- Success: criteria

Phase 2: Building (X weeks)
...etc"""
        
        try:
            response = self.llm.predict(prompt)
            phases = []
            
            # Parse phases (simplified)
            current_phase = {}
            lines = response.split('\n')
            
            for line in lines:
                line = line.strip()
                if line.startswith('Phase'):
                    if current_phase:
                        phases.append(current_phase)
                    
                    # Extract phase name and duration
                    phase_info = line.split(':')
                    if len(phase_info) >= 2:
                        phase_name = phase_info[1].split('(')[0].strip()
                        duration = "4-6 weeks"  # Default
                        if '(' in line and ')' in line:
                            duration = line.split('(')[1].split(')')[0]
                        
                        current_phase = {
                            "name": phase_name,
                            "duration": duration,
                            "concepts": [],
                            "skills": [],
                            "success_criteria": ""
                        }
                elif line.startswith('- Key concepts:'):
                    concepts = line.replace('- Key concepts:', '').strip()
                    current_phase["concepts"] = [c.strip() for c in concepts.split(',')]
                elif line.startswith('- Skills:'):
                    skills = line.replace('- Skills:', '').strip()
                    current_phase["skills"] = [s.strip() for s in skills.split(',')]
                elif line.startswith('- Success:'):
                    current_phase["success_criteria"] = line.replace('- Success:', '').strip()
            
            if current_phase:
                phases.append(current_phase)
            
            return phases
            
        except Exception as e:
            logger.error(f"Error planning learning phases: {e}")
            # Fallback phases
            return [
                {"name": "Foundation", "duration": "4-6 weeks", "concepts": [f"Basic {skill}"], "skills": ["Fundamentals"], "success_criteria": "Complete basic exercises"},
                {"name": "Building", "duration": "6-8 weeks", "concepts": [f"Intermediate {skill}"], "skills": ["Practical application"], "success_criteria": "Build first project"},
                {"name": "Mastery", "duration": "8-12 weeks", "concepts": [f"Advanced {skill}"], "skills": ["Complex problem solving"], "success_criteria": "Complete advanced project"},
                {"name": "Specialization", "duration": "12+ weeks", "concepts": [f"Expert {skill}"], "skills": ["Teaching others"], "success_criteria": "Contribute to community"}
            ]
    
    @with_api_key_rotation(max_retries=3, retry_delay=1.0)
    def _curate_resources(self, skill: str) -> List[Dict[str, Any]]:
        """Curate learning resources for the skill.
        
        Args:
            skill: The skill to curate resources for
            
        Returns:
            List of resource categories
        """
        prompt = f"""Recommend specific learning resources for "{skill}":

1. Online Courses (2-3 recommendations)
2. Books (2-3 recommendations)
3. Tutorials/Websites (3-4 recommendations)
4. Practice Platforms (2-3 recommendations)
5. Communities/Forums (2-3 recommendations)

Include both free and paid options. Mention why each resource is valuable.

Format as:
**Online Courses:**
- Course Name (Platform) - Why it's good

**Books:**
- Book Title by Author - Why it's valuable

etc."""
        
        try:
            response = self.llm.predict(prompt)
            # Store as structured data (simplified)
            resources = [
                {"type": "courses", "items": []},
                {"type": "books", "items": []},
                {"type": "tutorials", "items": []},
                {"type": "practice", "items": []},
                {"type": "communities", "items": []}
            ]
            
            # Parse resources (simplified - in production would be more sophisticated)
            current_category = None
            lines = response.split('\n')
            
            for line in lines:
                line = line.strip()
                if line.startswith('**') and line.endswith(':**'):
                    category = line.replace('**', '').replace(':', '').lower()
                    if 'course' in category:
                        current_category = 0
                    elif 'book' in category:
                        current_category = 1
                    elif 'tutorial' in category or 'website' in category:
                        current_category = 2
                    elif 'practice' in category or 'platform' in category:
                        current_category = 3
                    elif 'communit' in category or 'forum' in category:
                        current_category = 4
                    else:
                        current_category = None
                elif line.startswith('-') and current_category is not None:
                    resource = line.lstrip('-').strip()
                    if resource:
                        resources[current_category]["items"].append(resource)
            
            return resources
            
        except Exception as e:
            logger.error(f"Error curating resources: {e}")
            return [
                {"type": "courses", "items": [f"{skill} courses on popular platforms"]},
                {"type": "books", "items": [f"Books about {skill}"]},
                {"type": "tutorials", "items": [f"Online tutorials for {skill}"]},
                {"type": "practice", "items": [f"Practice platforms for {skill}"]},
                {"type": "communities", "items": [f"Online communities for {skill}"]}
            ]
    
    @with_api_key_rotation(max_retries=3, retry_delay=1.0)
    def _suggest_projects(self, skill: str, user_level: str) -> List[Dict[str, Any]]:
        """Suggest practice projects for the skill.
        
        Args:
            skill: The skill to suggest projects for
            user_level: User's current level
            
        Returns:
            List of project suggestions
        """
        prompt = f"""Suggest practical projects for learning "{skill}" at different levels:

1. Beginner (2 projects)
2. Intermediate (2 projects)
3. Advanced (2 projects)

For each project, provide:
- Project name
- Brief description
- Key skills practiced
- Estimated time to complete
- Resources needed

Format as:
**Beginner Projects:**
1. Project Name
   - Description: Brief description
   - Skills: skill1, skill2
   - Time: X hours/days
   - Resources: resource1, resource2

**Intermediate Projects:**
...etc."""
        
        try:
            response = self.llm.predict(prompt)
            projects = []
            
            # Parse projects (simplified)
            current_level = None
            current_project = {}
            lines = response.split('\n')
            
            for line in lines:
                line = line.strip()
                if line.startswith('**') and line.endswith(':**'):
                    current_level = line.replace('**', '').replace(':', '').strip()
                elif line.startswith('1.') or line.startswith('2.') or line.startswith('3.') or line.startswith('4.'):
                    if current_project:
                        projects.append(current_project)
                    
                    project_name = line.split('.', 1)[1].strip()
                    current_project = {
                        "name": project_name,
                        "level": current_level,
                        "description": "",
                        "skills": [],
                        "time": "",
                        "resources": []
                    }
                elif line.startswith('- Description:'):
                    current_project["description"] = line.replace('- Description:', '').strip()
                elif line.startswith('- Skills:'):
                    skills = line.replace('- Skills:', '').strip()
                    current_project["skills"] = [s.strip() for s in skills.split(',')]
                elif line.startswith('- Time:'):
                    current_project["time"] = line.replace('- Time:', '').strip()
                elif line.startswith('- Resources:'):
                    resources = line.replace('- Resources:', '').strip()
                    current_project["resources"] = [r.strip() for r in resources.split(',')]
            
            if current_project:
                projects.append(current_project)
            
            return projects
            
        except Exception as e:
            logger.error(f"Error suggesting projects: {e}")
            return [
                {"name": f"Basic {skill} project", "level": "Beginner", "description": f"Simple project to practice {skill}", "skills": [f"{skill} basics"], "time": "1-2 weeks", "resources": ["Online tutorials"]},
                {"name": f"Intermediate {skill} project", "level": "Intermediate", "description": f"More complex project using {skill}", "skills": [f"{skill} intermediate concepts"], "time": "2-4 weeks", "resources": ["Documentation"]},
                {"name": f"Advanced {skill} project", "level": "Advanced", "description": f"Complex project showcasing {skill} mastery", "skills": [f"Advanced {skill}"], "time": "4-8 weeks", "resources": ["Advanced tutorials"]}
            ]
    
    @with_api_key_rotation(max_retries=3, retry_delay=1.0)
    def _compose_roadmap(self, skill: str, user_level: str, time_commitment: str, 
                        prerequisites: List[str], learning_phases: List[Dict[str, Any]], 
                        resources: List[Dict[str, Any]], projects: List[Dict[str, Any]]) -> str:
        """Compose the final roadmap.
        
        Args:
            skill: The skill for the roadmap
            user_level: User's current level
            time_commitment: User's time commitment
            prerequisites: List of prerequisites
            learning_phases: List of learning phases
            resources: List of resource categories
            projects: List of project suggestions
            
        Returns:
            Complete roadmap as formatted text
        """
        prompt = RoadmapPrompts.roadmap_composition_prompt().format(
            skill=skill,
            user_level=user_level,
            time_commitment=time_commitment,
            prerequisites="\n".join([f"- {p}" for p in prerequisites]),
            phases="\n".join([f"- {p['name']} ({p['duration']}): {', '.join(p['concepts'][:3])}" for p in learning_phases]),
            resources="\n".join([f"- {r['type'].capitalize()}: {', '.join(r['items'][:2])}" for r in resources]),
            projects="\n".join([f"- {p['name']} ({p['level']}): {p['description'][:50]}..." for p in projects[:3]])
        )
        
        try:
            roadmap = self.llm.predict(prompt)
            return roadmap
        except Exception as e:
            logger.error(f"Error composing roadmap: {e}")
            return f"# Learning Roadmap for {skill}\n\nThis roadmap will help you learn {skill} efficiently. Start with the prerequisites, then follow the learning phases."
    
    def generate_roadmap(self, skill: str, user_level: str = "beginner", 
                        time_commitment: str = "moderate") -> Dict[str, Any]:
        """Generate a comprehensive learning roadmap for a skill.
        
        Args:
            skill: The skill to generate a roadmap for
            user_level: User's current level (beginner, intermediate, advanced)
            time_commitment: User's time commitment (minimal, moderate, intensive)
            
        Returns:
            Dictionary containing the roadmap and its components
        """
        try:
            # Step 1: Analyze skill
            skill_analysis = self._analyze_skill(skill)
            
            # Step 2: Find prerequisites
            prerequisites = self._find_prerequisites(skill)
            
            # Step 3: Plan learning phases
            learning_phases = self._plan_learning_phases(skill, user_level)
            
            # Step 4: Curate resources
            resources = self._curate_resources(skill)
            
            # Step 5: Suggest projects
            projects = self._suggest_projects(skill, user_level)
            
            # Step 6: Compose roadmap
            roadmap = self._compose_roadmap(
                skill, user_level, time_commitment,
                prerequisites, learning_phases, resources, projects
            )
            
            # Return complete roadmap data
            return {
                "success": True,
                "skill": skill,
                "user_level": user_level,
                "time_commitment": time_commitment,
                "skill_analysis": skill_analysis,
                "prerequisites": prerequisites,
                "learning_phases": learning_phases,
                "resources": resources,
                "projects": projects,
                "roadmap": roadmap
            }
            
        except Exception as e:
            logger.error(f"Error generating roadmap: {e}")
            return {
                "success": False,
                "error": str(e),
                "skill": skill,
                "user_level": user_level,
                "time_commitment": time_commitment,
                "roadmap": f"Unable to generate roadmap for {skill} due to an error: {str(e)}"
            }
    
    def get_skill_assessment(self, skill: str, current_knowledge: str) -> Dict[str, Any]:
        """Assess current skill level and provide recommendations.
        
        Args:
            skill: The skill to assess
            current_knowledge: Description of current knowledge
            
        Returns:
            Dictionary with assessment and recommendations
        """
        try:
            prompt = f"""Assess the user's current level in {skill} based on this description:
"{current_knowledge}"

Provide:
1. Current skill level (Beginner/Intermediate/Advanced)
2. Strengths identified
3. Areas for improvement
4. Recommended next steps
5. Estimated time to reach next level

Format as a structured assessment with clear sections."""
            
            assessment = self.llm.predict(prompt)
            
            return {
                "success": True,
                "skill": skill,
                "current_knowledge": current_knowledge,
                "assessment": assessment
            }
            
        except Exception as e:
            logger.error(f"Error assessing skill: {e}")
            return {
                "success": False,
                "error": str(e),
                "skill": skill,
                "current_knowledge": current_knowledge,
                "assessment": f"Unable to assess skill level for {skill} due to an error: {str(e)}"
            } 