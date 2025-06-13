"""
Prompt templates for user matching functionality.
"""

from langchain.prompts import PromptTemplate


class MatchingPrompts:
    """Prompt templates for user matching functionality."""
    
    @staticmethod
    def skill_compatibility_prompt() -> PromptTemplate:
        """Generate the skill compatibility analysis prompt template.
        
        Returns:
            Prompt template for analyzing skill compatibility
        """
        template = """You are a skill compatibility analyzer for the SkillMate platform. Your task is to analyze the compatibility between two users based on their skills, experience, and interests.

USER 1 PROFILE:
Name: {user1_name}
Skills: {user1_skills}
Experience Levels: {user1_experience}
Interests: {user1_interests}
Bio: {user1_bio}

USER 2 PROFILE:
Name: {user2_name}
Skills: {user2_skills}
Experience Levels: {user2_experience}
Interests: {user2_interests}
Bio: {user2_bio}

COLLABORATION CONTEXT:
Project Type: {project_type}
Team Size: {team_size}
Duration: {project_duration}

Analyze the compatibility between these two users and provide:

1. COMPATIBILITY SCORE (0-100): Overall compatibility rating
2. COMPLEMENTARY STRENGTHS: Areas where the users complement each other
3. OVERLAPPING EXPERTISE: Skills and interests they share
4. POTENTIAL SYNERGIES: How they could work well together
5. POSSIBLE CHALLENGES: Potential areas of conflict or challenge
6. ROLE DISTRIBUTION: Suggested role allocation if they work together
7. COLLABORATION RECOMMENDATION: Overall recommendation (Highly Compatible/Compatible/Somewhat Compatible/Not Compatible)

Be objective and consider both technical skills and soft skills. Focus on how their combined expertise could benefit a project.

FORMAT YOUR RESPONSE AS FOLLOWS:

# Compatibility Analysis: {user1_name} & {user2_name}

## Compatibility Score: [0-100]/100

## Complementary Strengths
- [Strength 1]: How User 1's skills complement User 2's gaps
- [Strength 2]: How User 2's skills complement User 1's gaps

## Overlapping Expertise
- [Shared skill/interest 1]: Level of overlap and benefit
- [Shared skill/interest 2]: Level of overlap and benefit

## Potential Synergies
- [Synergy 1]: How they could amplify each other's capabilities
- [Synergy 2]: Collaborative opportunities

## Possible Challenges
- [Challenge 1]: Potential conflict or difficulty
- [Challenge 2]: Areas requiring attention

## Suggested Role Distribution
- {user1_name}: [Primary role and responsibilities]
- {user2_name}: [Primary role and responsibilities]

## Overall Recommendation: [Compatibility Level]
[Brief explanation of the recommendation]
"""
        
        return PromptTemplate(
            template=template,
            input_variables=[
                "user1_name", "user1_skills", "user1_experience", "user1_interests", "user1_bio",
                "user2_name", "user2_skills", "user2_experience", "user2_interests", "user2_bio",
                "project_type", "team_size", "project_duration"
            ]
        )
    
    @staticmethod
    def team_matching_prompt() -> PromptTemplate:
        """Generate the team matching prompt template.
        
        Returns:
            Prompt template for suggesting team matches
        """
        template = """You are a team formation expert for the SkillMate platform. You need to recommend the best potential teammates for a user based on their profile and requirements.

TARGET USER PROFILE:
Name: {target_user_name}
Skills: {target_user_skills}
Experience: {target_user_experience}
Interests: {target_user_interests}
Bio: {target_user_bio}
Looking for: {looking_for}

CANDIDATE USERS:
{candidate_users}

PROJECT CONTEXT:
Type: {project_type}
Duration: {project_duration}
Team Size Needed: {team_size}

For each candidate, evaluate:
1. Skill complementarity with the target user
2. Shared interests and values
3. Experience level compatibility
4. Potential for effective collaboration
5. Likelihood of successful project completion

Rank the candidates from best to worst match and provide detailed reasoning for each recommendation.

FORMAT YOUR RESPONSE AS FOLLOWS:

# Team Recommendations for {target_user_name}

## Top Matches

### 1. [Candidate Name] - [Match Score]/100
**Why this is a great match:**
- [Reason 1]
- [Reason 2]
- [Reason 3]

**Complementary Skills:**
- Target user brings: [Skills]
- Candidate brings: [Skills]

**Potential Collaboration:**
- [How they could work together effectively]

**Recommendation:** [Highly Recommended/Recommended/Consider]

### 2. [Candidate Name] - [Match Score]/100
...

### 3. [Candidate Name] - [Match Score]/100
...

## Overall Team Formation Advice
[General advice about forming an effective team with these candidates]
"""
        
        return PromptTemplate(
            template=template,
            input_variables=[
                "target_user_name", "target_user_skills", "target_user_experience",
                "target_user_interests", "target_user_bio", "looking_for",
                "candidate_users", "project_type", "project_duration", "team_size"
            ]
        )
    
    @staticmethod
    def smart_connect_prompt() -> PromptTemplate:
        """Generate the smart connect suggestion prompt template.
        
        Returns:
            Prompt template for AI-enhanced connection suggestions
        """
        template = """You are an intelligent connection facilitator for the SkillMate platform. Your role is to create personalized connection suggestions that help users discover potential collaborators they might not have considered.

USER PROFILE:
Name: {user_name}
Skills: {user_skills}
Interests: {user_interests}
Recent Activity: {recent_activity}
Connection History: {connection_history}

PLATFORM INSIGHTS:
Trending Skills: {trending_skills}
Popular Project Types: {popular_projects}
Successful Team Patterns: {successful_patterns}

Based on this information, generate smart connection suggestions that:
1. Expand the user's network beyond their obvious skill matches
2. Introduce them to complementary skillsets they might benefit from
3. Consider emerging trends and opportunities
4. Account for their past connection patterns and preferences

Provide 3-5 smart connection suggestions with compelling reasons why each connection could be valuable.

FORMAT YOUR RESPONSE AS FOLLOWS:

# Smart Connection Suggestions for {user_name}

## Suggestion 1: Connect with [Skill/Role] Experts
**Why this connection makes sense:**
[Explanation of the strategic value]

**Specific benefits:**
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

**Potential collaboration opportunities:**
- [Opportunity 1]
- [Opportunity 2]

## Suggestion 2: Explore [Domain/Technology] Community
**Why this connection makes sense:**
[Explanation of the strategic value]

**Specific benefits:**
- [Benefit 1]
- [Benefit 2]

**Potential collaboration opportunities:**
- [Opportunity 1]
- [Opportunity 2]

## Suggestion 3: [Creative/Unique Suggestion]
...

## Suggestion 4: [Growth-Oriented Suggestion]
...

## Suggestion 5: [Trend-Based Suggestion]
...

## Connection Strategy
[Overall advice on how to approach these connections and maximize networking effectiveness]
"""
        
        return PromptTemplate(
            template=template,
            input_variables=[
                "user_name", "user_skills", "user_interests", "recent_activity",
                "connection_history", "trending_skills", "popular_projects", "successful_patterns"
            ]
        ) 