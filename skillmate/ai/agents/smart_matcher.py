"""
Smart Matcher Agent for SkillMate platform.
Matches users based on complementary skills and interests.
"""

from typing import Dict, Any, List, Optional
import logging
import numpy as np

# Set up logger
logger = logging.getLogger(__name__)

try:
    from ..config.settings import settings
    from ..embeddings.embedding_service import EmbeddingService
    from ..prompts.matcher_prompts import MatcherPrompts
    from ..config.model_provider import model_provider, with_api_key_rotation
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config.settings import settings
    from embeddings.embedding_service import EmbeddingService
    from prompts.matcher_prompts import MatcherPrompts
    from config.model_provider import model_provider, with_api_key_rotation


class SmartMatcherAgent:
    """Smart matching agent for finding compatible users."""
    
    def __init__(self, embedding_service: Optional[EmbeddingService] = None):
        """Initialize the smart matcher agent.
        
        Args:
            embedding_service: Optional embedding service instance
        """
        # Create LLM using the model provider factory
        self.llm = model_provider.create_llm(
            model_type="matcher",
            temperature=0.3  # Lower temperature for more consistent matching
        )
        
        self.embedding_service = embedding_service or EmbeddingService()
    
    def _analyze_skills(self, user_profile: Dict[str, Any], candidates: List[Dict[str, Any]]) -> Dict[str, float]:
        """Analyze skill compatibility between target user and candidates.
        
        Args:
            user_profile: Target user profile
            candidates: List of candidate profiles
            
        Returns:
            Dictionary mapping candidate IDs to skill scores
        """
        skill_scores = {}
        target_skills = set(user_profile.get('skills', []))
        
        for candidate in candidates:
            candidate_id = candidate.get('user_id', candidate.get('name', 'unknown'))
            candidate_skills = set(candidate.get('skills', []))
            
            # Calculate skill overlap and complementarity
            overlap = len(target_skills.intersection(candidate_skills))
            complement = len(candidate_skills - target_skills)
            total_skills = len(target_skills.union(candidate_skills))
            
            # Weighted score: overlap for collaboration + complement for learning
            if total_skills > 0:
                overlap_score = overlap / len(target_skills) if target_skills else 0
                complement_score = complement / max(len(candidate_skills), 1) if candidate_skills else 0
                skill_score = (overlap_score * 0.6) + (complement_score * 0.4)
            else:
                skill_score = 0.0
            
            skill_scores[candidate_id] = skill_score
        
        return skill_scores
    
    def _match_interests(self, user_profile: Dict[str, Any], candidates: List[Dict[str, Any]]) -> Dict[str, float]:
        """Match interests between target user and candidates.
        
        Args:
            user_profile: Target user profile
            candidates: List of candidate profiles
            
        Returns:
            Dictionary mapping candidate IDs to interest scores
        """
        interest_scores = {}
        target_interests = set(interest.lower() for interest in user_profile.get('interests', []))
        
        for candidate in candidates:
            candidate_id = candidate.get('user_id', candidate.get('name', 'unknown'))
            candidate_interests = set(interest.lower() for interest in candidate.get('interests', []))
            
            # Calculate interest overlap
            if target_interests and candidate_interests:
                overlap = len(target_interests.intersection(candidate_interests))
                interest_score = overlap / len(target_interests.union(candidate_interests))
            else:
                interest_score = 0.0
            
            interest_scores[candidate_id] = interest_score
        
        return interest_scores
    
    def _calculate_embeddings(self, user_profile: Dict[str, Any], candidates: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate embedding-based similarity scores.
        
        Args:
            user_profile: Target user profile
            candidates: List of candidate profiles
            
        Returns:
            Dictionary mapping candidate IDs to embedding scores
        """
        embedding_scores = {}
        
        try:
            # Create text representation of target user
            target_text = self._user_to_text(user_profile)
            target_embedding = self.embedding_service.create_user_embedding(
                user_profile.get('user_id', 'target'), target_text
            )
            
            for candidate in candidates:
                candidate_id = candidate.get('user_id', candidate.get('name', 'unknown'))
                
                # Create text representation of candidate
                candidate_text = self._user_to_text(candidate)
                candidate_embedding = self.embedding_service.create_user_embedding(
                    candidate_id, candidate_text
                )
                
                # Calculate cosine similarity
                similarity = self._cosine_similarity(target_embedding, candidate_embedding)
                embedding_scores[candidate_id] = float(similarity)
                
        except Exception as e:
            logger.error(f"Error calculating embeddings: {e}")
            # Fallback: set all embedding scores to 0
            for candidate in candidates:
                candidate_id = candidate.get('user_id', candidate.get('name', 'unknown'))
                embedding_scores[candidate_id] = 0.0
        
        return embedding_scores
    
    def _cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity score
        """
        if not isinstance(vec1, np.ndarray):
            vec1 = np.array(vec1)
        if not isinstance(vec2, np.ndarray):
            vec2 = np.array(vec2)
            
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return dot_product / (norm1 * norm2)
    
    @with_api_key_rotation(max_retries=3, retry_delay=1.0)
    def _assess_compatibility(self, user_profile: Dict[str, Any], candidate: Dict[str, Any]) -> float:
        """Assess overall compatibility using AI analysis.
        
        Args:
            user_profile: Target user profile
            candidate: Candidate profile
            
        Returns:
            Compatibility score
        """
        try:
            # Use AI to assess compatibility
            prompt = f"""Analyze the compatibility between these two users for collaboration:

User 1:
- Skills: {', '.join(user_profile.get('skills', []))}
- Interests: {', '.join(user_profile.get('interests', []))}
- Experience: {user_profile.get('experience', 'Not specified')}

User 2:
- Skills: {', '.join(candidate.get('skills', []))}
- Interests: {', '.join(candidate.get('interests', []))}
- Experience: {candidate.get('experience', 'Not specified')}

Rate their compatibility on a scale from 0.0 to 1.0, where 1.0 is perfect compatibility.
Consider skill complementarity, shared interests, and potential for successful collaboration.
Provide only the numeric score as a float between 0.0 and 1.0.
"""
            
            response = self.llm.predict(prompt)
            
            # Extract numeric score
            try:
                score = float(response.strip())
                # Ensure score is in valid range
                score = max(0.0, min(score, 1.0))
                return score
            except:
                # Fallback if parsing fails
                return 0.5
                
        except Exception as e:
            logger.error(f"Error assessing compatibility: {e}")
            return 0.5
    
    def _rank_candidates(self, skill_scores: Dict[str, float], interest_scores: Dict[str, float], 
                       embedding_scores: Dict[str, float], compatibility_scores: Dict[str, float]) -> Dict[str, float]:
        """Rank candidates based on combined scores.
        
        Args:
            skill_scores: Dictionary mapping candidate IDs to skill scores
            interest_scores: Dictionary mapping candidate IDs to interest scores
            embedding_scores: Dictionary mapping candidate IDs to embedding scores
            compatibility_scores: Dictionary mapping candidate IDs to compatibility scores
            
        Returns:
            Dictionary mapping candidate IDs to final scores
        """
        final_scores = {}
        
        # Weights for different score components
        weights = {
            "skills": 0.3,
            "interests": 0.2,
            "embeddings": 0.2,
            "compatibility": 0.3
        }
        
        # Combine scores with weights
        for candidate_id in skill_scores.keys():
            skill_score = skill_scores.get(candidate_id, 0.0)
            interest_score = interest_scores.get(candidate_id, 0.0)
            embedding_score = embedding_scores.get(candidate_id, 0.0)
            compatibility_score = compatibility_scores.get(candidate_id, 0.0)
            
            final_score = (
                skill_score * weights["skills"] +
                interest_score * weights["interests"] +
                embedding_score * weights["embeddings"] +
                compatibility_score * weights["compatibility"]
            )
            
            final_scores[candidate_id] = final_score
        
        return final_scores
    
    def _user_to_text(self, user: Dict[str, Any]) -> str:
        """Convert user profile to text representation for embedding.
        
        Args:
            user: User profile
            
        Returns:
            Text representation of user
        """
        parts = []
        
        if user.get('name'):
            parts.append(f"Name: {user['name']}")
        
        if user.get('skills'):
            parts.append(f"Skills: {', '.join(user['skills'])}")
        
        if user.get('interests'):
            parts.append(f"Interests: {', '.join(user['interests'])}")
        
        if user.get('experience'):
            parts.append(f"Experience: {user['experience']}")
        
        if user.get('bio'):
            parts.append(f"Bio: {user['bio']}")
        
        return "\n".join(parts)
    
    def find_matches(self, target_user: Dict[str, Any], candidate_users: List[Dict[str, Any]], 
                    project_context: Dict[str, Any] = None, limit: int = 5) -> Dict[str, Any]:
        """Find matches for a target user from a list of candidates.
        
        Args:
            target_user: Target user profile
            candidate_users: List of candidate profiles
            project_context: Optional project context
            limit: Maximum number of matches to return
            
        Returns:
            Dictionary with match results
        """
        try:
            # Step 1: Analyze skills
            skill_scores = self._analyze_skills(target_user, candidate_users)
            
            # Step 2: Match interests
            interest_scores = self._match_interests(target_user, candidate_users)
            
            # Step 3: Calculate embeddings
            embedding_scores = self._calculate_embeddings(target_user, candidate_users)
            
            # Step 4: Assess compatibility
            compatibility_scores = {}
            for candidate in candidate_users:
                candidate_id = candidate.get('user_id', candidate.get('name', 'unknown'))
                compatibility_scores[candidate_id] = self._assess_compatibility(target_user, candidate)
            
            # Step 5: Rank candidates
            final_scores = self._rank_candidates(skill_scores, interest_scores, embedding_scores, compatibility_scores)
            
            # Sort candidates by final score
            ranked_candidates = sorted(
                [(cid, score) for cid, score in final_scores.items()],
                key=lambda x: x[1],
                reverse=True
            )
            
            # Prepare match results
            matches = []
            for candidate_id, score in ranked_candidates[:limit]:
                # Find the candidate profile
                candidate = next((c for c in candidate_users if c.get('user_id', c.get('name', 'unknown')) == candidate_id), None)
                if candidate:
                    match_explanation = self._generate_match_explanation(
                        target_user, candidate,
                        skill_scores[candidate_id],
                        interest_scores[candidate_id],
                        compatibility_scores[candidate_id]
                    )
                    
                    matches.append({
                        "user_id": candidate_id,
                        "name": candidate.get('name', candidate_id),
                        "match_score": round(score * 100),  # Convert to percentage
                        "skills": candidate.get('skills', []),
                        "interests": candidate.get('interests', []),
                        "explanation": match_explanation
                    })
            
            return {
                "success": True,
                "target_user": target_user.get('user_id', target_user.get('name', 'target')),
                "matches": matches,
                "match_count": len(matches)
            }
            
        except Exception as e:
            logger.error(f"Error finding matches: {e}")
            return {
                "success": False,
                "error": str(e),
                "target_user": target_user.get('user_id', target_user.get('name', 'target')),
                "matches": []
            }
    
    def _generate_match_explanation(self, target_user: Dict[str, Any], candidate: Dict[str, Any],
                                  skill_score: float, interest_score: float, compatibility_score: float) -> str:
        """Generate an explanation for why users match.
        
        Args:
            target_user: Target user profile
            candidate: Candidate profile
            skill_score: Skill compatibility score
            interest_score: Interest similarity score
            compatibility_score: Overall compatibility score
            
        Returns:
            Match explanation text
        """
        try:
            prompt = f"""Explain why these two users would be good matches for collaboration:

User 1:
- Skills: {', '.join(target_user.get('skills', []))}
- Interests: {', '.join(target_user.get('interests', []))}

User 2:
- Skills: {', '.join(candidate.get('skills', []))}
- Interests: {', '.join(candidate.get('interests', []))}

Skill Compatibility: {skill_score:.2f}
Interest Similarity: {interest_score:.2f}
Overall Compatibility: {compatibility_score:.2f}

Write a brief, personalized explanation (2-3 sentences) of why these users would work well together.
Focus on complementary skills, shared interests, and potential for successful collaboration.
"""
            
            explanation = self.llm.predict(prompt)
            return explanation.strip()
            
        except Exception as e:
            logger.error(f"Error generating match explanation: {e}")
            return "These users have complementary skills and shared interests that would make them good collaborators." 