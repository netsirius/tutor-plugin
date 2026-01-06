"""
Recommendation Engine

Generates personalized recommendations for:
- Next topics to learn
- Exercises to practice
- Review sessions
- Study schedule optimization
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


class RecommendationType(Enum):
    """Types of recommendations."""
    NEXT_TOPIC = "next_topic"
    EXERCISE = "exercise"
    REVIEW = "review"
    BREAK = "break"
    CHALLENGE = "challenge"
    PROJECT = "project"


@dataclass
class Recommendation:
    """A single recommendation for the student."""
    recommendation_type: RecommendationType
    title: str
    description: str
    priority: float  # 0.0 to 1.0
    reason: str  # Why this is recommended
    action: str  # What to do
    estimated_minutes: int = 30
    difficulty: int = 2  # 1-5
    related_topics: list[str] = field(default_factory=list)
    prerequisites: list[str] = field(default_factory=list)
    resource_path: Optional[str] = None  # Path to lesson/exercise

    def to_dict(self) -> dict:
        return {
            "type": self.recommendation_type.value,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "reason": self.reason,
            "action": self.action,
            "estimated_minutes": self.estimated_minutes,
            "difficulty": self.difficulty,
            "related_topics": self.related_topics,
            "prerequisites": self.prerequisites,
            "resource_path": self.resource_path,
        }


class RecommendationEngine:
    """
    Generates personalized learning recommendations.

    Uses:
    - Current progress
    - Skill gaps
    - Learning style
    - Spaced repetition data
    - Time of day / available time
    """

    def __init__(
        self,
        progress: dict,
        curriculum: dict,
        skill_gaps: Optional[list] = None,
        learning_profile: Optional[dict] = None,
        srs_due_items: Optional[list] = None,
    ):
        """
        Initialize the recommendation engine.

        Args:
            progress: Student's progress data
            curriculum: Course curriculum
            skill_gaps: List of identified skill gaps
            learning_profile: Learning style profile
            srs_due_items: Items due for spaced repetition review
        """
        self.progress = progress
        self.curriculum = curriculum
        self.skill_gaps = skill_gaps or []
        self.learning_profile = learning_profile or {}
        self.srs_due_items = srs_due_items or []

    def get_recommendations(
        self,
        available_minutes: int = 60,
        context: str = "general",  # general, quick_practice, deep_learning, review
    ) -> list[Recommendation]:
        """
        Get personalized recommendations.

        Args:
            available_minutes: Time available for study
            context: Study context/goal

        Returns:
            List of recommendations sorted by priority
        """
        recommendations = []

        # Always check for due reviews first
        recommendations.extend(self._get_review_recommendations())

        # Add context-specific recommendations
        if context == "quick_practice":
            recommendations.extend(self._get_quick_practice_recommendations(available_minutes))
        elif context == "deep_learning":
            recommendations.extend(self._get_deep_learning_recommendations(available_minutes))
        elif context == "review":
            recommendations.extend(self._get_comprehensive_review_recommendations())
        else:
            # General recommendations
            recommendations.extend(self._get_next_topic_recommendations())
            recommendations.extend(self._get_exercise_recommendations())
            recommendations.extend(self._get_skill_gap_recommendations())

        # Add break recommendation if studying for a while
        session_stats = self.progress.get("current_session", {})
        if session_stats.get("duration_minutes", 0) > 45:
            recommendations.append(self._get_break_recommendation())

        # Filter by available time
        recommendations = [
            r for r in recommendations
            if r.estimated_minutes <= available_minutes
        ]

        # Sort by priority
        recommendations.sort(key=lambda r: r.priority, reverse=True)

        return recommendations[:10]  # Return top 10

    def get_next_action(self) -> Recommendation:
        """
        Get the single best next action.

        Returns:
            The highest priority recommendation
        """
        recommendations = self.get_recommendations()
        if recommendations:
            return recommendations[0]

        # Default recommendation
        return Recommendation(
            recommendation_type=RecommendationType.NEXT_TOPIC,
            title="Continue Learning",
            description="Continue with your curriculum",
            priority=0.5,
            reason="Keep making progress",
            action="Open the next lesson",
        )

    def _get_review_recommendations(self) -> list[Recommendation]:
        """Get recommendations for spaced repetition reviews."""
        recommendations = []

        if self.srs_due_items:
            # Group by type
            due_count = len(self.srs_due_items)

            recommendations.append(Recommendation(
                recommendation_type=RecommendationType.REVIEW,
                title=f"Review Due ({due_count} items)",
                description=f"You have {due_count} items ready for review",
                priority=0.9,  # High priority for due reviews
                reason="Spaced repetition keeps knowledge fresh",
                action="Start review session",
                estimated_minutes=min(30, due_count * 3),
            ))

        return recommendations

    def _get_next_topic_recommendations(self) -> list[Recommendation]:
        """Get recommendations for next topics to learn."""
        recommendations = []

        # Find the next topic in curriculum
        current_module = self.progress.get("current_module")
        modules = self.curriculum.get("modules", [])

        for module in modules:
            module_id = module.get("id")
            module_progress = self.progress.get("modules", {}).get(module_id, {})

            if module_progress.get("status") == "completed":
                continue

            # Check prerequisites
            prereqs = module.get("prerequisites", [])
            prereqs_met = all(
                self.progress.get("modules", {}).get(p, {}).get("status") == "completed"
                for p in prereqs
            )

            if not prereqs_met:
                continue

            # Find first incomplete topic
            topics = module.get("topics", [])
            for topic in topics:
                topic_id = topic.get("id") if isinstance(topic, dict) else topic

                recommendations.append(Recommendation(
                    recommendation_type=RecommendationType.NEXT_TOPIC,
                    title=f"Learn: {module.get('title', module_id)}",
                    description=topic.get("title", topic_id) if isinstance(topic, dict) else topic_id,
                    priority=0.7,
                    reason="Next topic in your curriculum",
                    action=f"Open lessons/{module_id}/",
                    estimated_minutes=topic.get("estimated_minutes", 30) if isinstance(topic, dict) else 30,
                    difficulty=module.get("difficulty", 2),
                    resource_path=f"lessons/{module_id}/",
                ))
                break

            break  # Only recommend from first available module

        return recommendations

    def _get_exercise_recommendations(self) -> list[Recommendation]:
        """Get recommendations for exercises."""
        recommendations = []

        current_module = self.progress.get("current_module")
        if not current_module:
            return recommendations

        # Get current module from curriculum
        module_data = None
        for module in self.curriculum.get("modules", []):
            if module.get("id") == current_module:
                module_data = module
                break

        if not module_data:
            return recommendations

        exercises = module_data.get("exercises", [])
        module_progress = self.progress.get("modules", {}).get(current_module, {})
        exercise_progress = module_progress.get("exercises", {})

        for exercise in exercises:
            if isinstance(exercise, dict):
                ex_id = exercise.get("id")
                ex_title = exercise.get("title", ex_id)
                difficulty = exercise.get("difficulty", "intermediate")
            else:
                ex_id = exercise
                ex_title = exercise
                difficulty = "intermediate"

            # Skip completed
            if exercise_progress.get(ex_id, {}).get("status") == "completed":
                continue

            difficulty_map = {"basic": 1, "intermediate": 2, "advanced": 3, "challenge": 4}
            diff_value = difficulty_map.get(difficulty, 2)

            recommendations.append(Recommendation(
                recommendation_type=RecommendationType.EXERCISE,
                title=f"Exercise: {ex_title}",
                description=f"{difficulty.title()} difficulty exercise",
                priority=0.6,
                reason="Practice reinforces learning",
                action=f"Open lessons/{current_module}/exercises/{ex_id}/",
                estimated_minutes=diff_value * 15,
                difficulty=diff_value,
                resource_path=f"lessons/{current_module}/exercises/{ex_id}/",
            ))
            break  # Only recommend one exercise

        return recommendations

    def _get_skill_gap_recommendations(self) -> list[Recommendation]:
        """Get recommendations based on skill gaps."""
        recommendations = []

        for gap in self.skill_gaps[:3]:  # Top 3 gaps
            recommendations.append(Recommendation(
                recommendation_type=RecommendationType.NEXT_TOPIC,
                title=f"Strengthen: {gap.skill_name}",
                description=f"Fill gap: {gap.current_level.name} → {gap.target_level.name}",
                priority=gap.priority * 0.8,
                reason=f"Prerequisite for {len(gap.blocking_skills)} other skills",
                action="Review related topics",
                estimated_minutes=gap.estimated_time_minutes,
                difficulty=gap.gap_size + 1,
                related_topics=gap.related_topics,
            ))

        return recommendations

    def _get_quick_practice_recommendations(self, available_minutes: int) -> list[Recommendation]:
        """Get recommendations for quick practice sessions."""
        recommendations = []

        # Recommend short exercises
        recommendations.append(Recommendation(
            recommendation_type=RecommendationType.EXERCISE,
            title="Quick Practice",
            description="Short exercise to maintain momentum",
            priority=0.8,
            reason="Perfect for limited time",
            action="Start a basic exercise",
            estimated_minutes=min(15, available_minutes),
            difficulty=1,
        ))

        # Recommend flashcard review
        if self.srs_due_items:
            review_count = min(10, len(self.srs_due_items))
            recommendations.append(Recommendation(
                recommendation_type=RecommendationType.REVIEW,
                title=f"Quick Review ({review_count} items)",
                description="Review key concepts",
                priority=0.85,
                reason="Maintain knowledge retention",
                action="Start quick review",
                estimated_minutes=review_count * 2,
            ))

        return recommendations

    def _get_deep_learning_recommendations(self, available_minutes: int) -> list[Recommendation]:
        """Get recommendations for deep learning sessions."""
        recommendations = []

        # Recommend comprehensive topic study
        recommendations.append(Recommendation(
            recommendation_type=RecommendationType.NEXT_TOPIC,
            title="Deep Dive Session",
            description="Comprehensive study of next topic with exercises",
            priority=0.8,
            reason="Extended time allows for deeper understanding",
            action="Start comprehensive lesson",
            estimated_minutes=min(60, available_minutes),
            difficulty=3,
        ))

        # Recommend challenging exercise
        recommendations.append(Recommendation(
            recommendation_type=RecommendationType.CHALLENGE,
            title="Challenge Exercise",
            description="Test your skills with a challenging problem",
            priority=0.7,
            reason="Challenges accelerate growth",
            action="Attempt advanced exercise",
            estimated_minutes=min(45, available_minutes),
            difficulty=4,
        ))

        return recommendations

    def _get_comprehensive_review_recommendations(self) -> list[Recommendation]:
        """Get recommendations for review sessions."""
        recommendations = []

        # All due SRS items
        if self.srs_due_items:
            recommendations.append(Recommendation(
                recommendation_type=RecommendationType.REVIEW,
                title="Complete Review Session",
                description=f"Review all {len(self.srs_due_items)} due items",
                priority=0.95,
                reason="Comprehensive review for retention",
                action="Start full review",
                estimated_minutes=len(self.srs_due_items) * 3,
            ))

        # Weak topic review
        if self.skill_gaps:
            weakest = self.skill_gaps[0]
            recommendations.append(Recommendation(
                recommendation_type=RecommendationType.REVIEW,
                title=f"Review: {weakest.skill_name}",
                description="Strengthen your weakest area",
                priority=0.8,
                reason="Targeted improvement",
                action="Review topic materials",
                estimated_minutes=30,
                difficulty=2,
            ))

        return recommendations

    def _get_break_recommendation(self) -> Recommendation:
        """Get break recommendation for long sessions."""
        return Recommendation(
            recommendation_type=RecommendationType.BREAK,
            title="Take a Break",
            description="You've been studying for a while. A short break helps retention!",
            priority=0.6,
            reason="Breaks improve focus and memory consolidation",
            action="Rest for 10-15 minutes",
            estimated_minutes=10,
            difficulty=0,
        )
