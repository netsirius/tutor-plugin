"""
Learning Style Analyzer

Detects and adapts to different learning styles:
- Visual learners
- Reading/Writing learners
- Kinesthetic (hands-on) learners
- Auditory learners (limited support in text-based tutoring)

Also tracks learning patterns and preferences.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
from enum import Enum
import json
from pathlib import Path


class LearningStyle(Enum):
    """Primary learning style categories (VARK model)."""
    VISUAL = "visual"  # Prefer diagrams, charts, images
    READING = "reading"  # Prefer text, documentation
    KINESTHETIC = "kinesthetic"  # Prefer hands-on, exercises
    MULTIMODAL = "multimodal"  # Mix of styles


class PacingPreference(Enum):
    """How fast the student prefers to learn."""
    SLOW = "slow"  # Thorough, detailed explanations
    MODERATE = "moderate"  # Balanced approach
    FAST = "fast"  # Quick overview, jump to practice


class FeedbackPreference(Enum):
    """How the student prefers to receive feedback."""
    DETAILED = "detailed"  # Long explanations of what went wrong
    CONCISE = "concise"  # Brief, actionable feedback
    SOCRATIC = "socratic"  # Questions that lead to discovery


@dataclass
class LearningProfile:
    """A student's learning profile based on observed behavior."""
    primary_style: LearningStyle = LearningStyle.MULTIMODAL
    style_scores: dict[str, float] = field(default_factory=dict)  # style -> score

    pacing: PacingPreference = PacingPreference.MODERATE
    feedback_preference: FeedbackPreference = FeedbackPreference.DETAILED

    # Time patterns
    preferred_session_length_minutes: int = 45
    best_time_of_day: Optional[str] = None  # morning, afternoon, evening, night

    # Engagement patterns
    exercises_before_theory_ratio: float = 0.5  # 0=all theory first, 1=all exercises first
    hint_usage_rate: float = 0.5  # How often they use hints
    retry_persistence: float = 0.5  # How many times they retry before giving up

    # Content preferences
    prefers_examples: bool = True
    prefers_analogies: bool = True
    prefers_diagrams: bool = True
    code_comment_density: str = "medium"  # sparse, medium, verbose

    # Performance patterns
    morning_performance: float = 0.5
    afternoon_performance: float = 0.5
    evening_performance: float = 0.5

    # Metadata
    observations_count: int = 0
    last_updated: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "primary_style": self.primary_style.value,
            "style_scores": self.style_scores,
            "pacing": self.pacing.value,
            "feedback_preference": self.feedback_preference.value,
            "preferred_session_length_minutes": self.preferred_session_length_minutes,
            "best_time_of_day": self.best_time_of_day,
            "exercises_before_theory_ratio": self.exercises_before_theory_ratio,
            "hint_usage_rate": self.hint_usage_rate,
            "retry_persistence": self.retry_persistence,
            "prefers_examples": self.prefers_examples,
            "prefers_analogies": self.prefers_analogies,
            "prefers_diagrams": self.prefers_diagrams,
            "code_comment_density": self.code_comment_density,
            "morning_performance": self.morning_performance,
            "afternoon_performance": self.afternoon_performance,
            "evening_performance": self.evening_performance,
            "observations_count": self.observations_count,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "LearningProfile":
        return cls(
            primary_style=LearningStyle(data.get("primary_style", "multimodal")),
            style_scores=data.get("style_scores", {}),
            pacing=PacingPreference(data.get("pacing", "moderate")),
            feedback_preference=FeedbackPreference(data.get("feedback_preference", "detailed")),
            preferred_session_length_minutes=data.get("preferred_session_length_minutes", 45),
            best_time_of_day=data.get("best_time_of_day"),
            exercises_before_theory_ratio=data.get("exercises_before_theory_ratio", 0.5),
            hint_usage_rate=data.get("hint_usage_rate", 0.5),
            retry_persistence=data.get("retry_persistence", 0.5),
            prefers_examples=data.get("prefers_examples", True),
            prefers_analogies=data.get("prefers_analogies", True),
            prefers_diagrams=data.get("prefers_diagrams", True),
            code_comment_density=data.get("code_comment_density", "medium"),
            morning_performance=data.get("morning_performance", 0.5),
            afternoon_performance=data.get("afternoon_performance", 0.5),
            evening_performance=data.get("evening_performance", 0.5),
            observations_count=data.get("observations_count", 0),
            last_updated=datetime.fromisoformat(data["last_updated"]) if data.get("last_updated") else None,
        )


@dataclass
class LearningObservation:
    """A single observation of student behavior."""
    timestamp: datetime
    observation_type: str  # session, exercise, hint, feedback
    data: dict = field(default_factory=dict)


class LearningStyleAnalyzer:
    """
    Analyzes student behavior to determine learning style preferences.

    Tracks patterns over time and adapts recommendations accordingly.
    """

    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize the learning style analyzer.

        Args:
            storage_path: Path to store profile data
        """
        self.storage_path = storage_path or Path.cwd() / ".tutor" / "learning_profile.json"
        self.profile = LearningProfile()
        self.observations: list[LearningObservation] = []
        self._load()

    def record_session(
        self,
        duration_minutes: int,
        exercises_completed: int,
        topics_read: int,
        hints_used: int,
        total_hints_available: int,
    ) -> None:
        """
        Record a study session.

        Args:
            duration_minutes: How long the session lasted
            exercises_completed: Number of exercises done
            topics_read: Number of topics/lessons read
            hints_used: How many hints were accessed
            total_hints_available: Total hints that could have been used
        """
        now = datetime.now()

        # Determine time of day
        hour = now.hour
        if 5 <= hour < 12:
            time_of_day = "morning"
        elif 12 <= hour < 17:
            time_of_day = "afternoon"
        elif 17 <= hour < 21:
            time_of_day = "evening"
        else:
            time_of_day = "night"

        observation = LearningObservation(
            timestamp=now,
            observation_type="session",
            data={
                "duration_minutes": duration_minutes,
                "exercises_completed": exercises_completed,
                "topics_read": topics_read,
                "hints_used": hints_used,
                "total_hints_available": total_hints_available,
                "time_of_day": time_of_day,
            }
        )
        self.observations.append(observation)

        # Update profile
        self._update_session_preferences(observation)
        self._save()

    def record_exercise_attempt(
        self,
        exercise_id: str,
        attempt_number: int,
        score: int,
        time_spent_minutes: int,
        used_hints: bool,
    ) -> None:
        """
        Record an exercise attempt.

        Args:
            exercise_id: ID of the exercise
            attempt_number: Which attempt this is
            score: Score achieved
            time_spent_minutes: Time spent on this attempt
            used_hints: Whether hints were accessed
        """
        now = datetime.now()
        hour = now.hour

        observation = LearningObservation(
            timestamp=now,
            observation_type="exercise",
            data={
                "exercise_id": exercise_id,
                "attempt_number": attempt_number,
                "score": score,
                "time_spent_minutes": time_spent_minutes,
                "used_hints": used_hints,
                "hour": hour,
            }
        )
        self.observations.append(observation)

        # Update profile
        self._update_exercise_patterns(observation)
        self._save()

    def record_content_interaction(
        self,
        content_type: str,  # text, diagram, example, exercise
        engagement_seconds: int,
    ) -> None:
        """
        Record interaction with content.

        Args:
            content_type: Type of content engaged with
            engagement_seconds: How long they engaged
        """
        observation = LearningObservation(
            timestamp=datetime.now(),
            observation_type="content",
            data={
                "content_type": content_type,
                "engagement_seconds": engagement_seconds,
            }
        )
        self.observations.append(observation)

        # Update style scores
        self._update_style_scores(observation)
        self._save()

    def get_content_recommendations(self) -> dict:
        """
        Get recommendations for content generation based on profile.

        Returns:
            Dictionary with content generation parameters
        """
        profile = self.profile

        return {
            # How to structure explanations
            "explanation_style": {
                "include_diagrams": profile.prefers_diagrams,
                "include_examples": profile.prefers_examples,
                "include_analogies": profile.prefers_analogies,
                "detail_level": "high" if profile.pacing == PacingPreference.SLOW else (
                    "low" if profile.pacing == PacingPreference.FAST else "medium"
                ),
            },

            # Code examples
            "code_style": {
                "comment_density": profile.code_comment_density,
                "example_complexity": "simple" if profile.pacing == PacingPreference.SLOW else "moderate",
            },

            # Exercise generation
            "exercise_style": {
                "provide_hints": profile.hint_usage_rate > 0.3,
                "hint_levels": 3 if profile.hint_usage_rate > 0.5 else 2,
                "scaffold_difficulty": profile.retry_persistence < 0.5,
            },

            # Feedback style
            "feedback_style": profile.feedback_preference.value,

            # Session recommendations
            "session": {
                "recommended_length_minutes": profile.preferred_session_length_minutes,
                "theory_exercise_ratio": 1 - profile.exercises_before_theory_ratio,
                "best_time": profile.best_time_of_day,
            },
        }

    def get_optimal_study_time(self) -> str:
        """
        Determine the best time for the student to study.

        Returns:
            Time of day recommendation
        """
        profile = self.profile

        performances = {
            "morning": profile.morning_performance,
            "afternoon": profile.afternoon_performance,
            "evening": profile.evening_performance,
        }

        return max(performances, key=performances.get)

    def get_style_summary(self) -> dict:
        """
        Get a summary of the detected learning style.

        Returns:
            Dictionary with style analysis
        """
        profile = self.profile

        return {
            "primary_style": profile.primary_style.value,
            "style_breakdown": profile.style_scores,
            "pacing": profile.pacing.value,
            "feedback_preference": profile.feedback_preference.value,
            "strengths": self._identify_strengths(),
            "suggestions": self._generate_suggestions(),
            "confidence": min(1.0, profile.observations_count / 20),  # Full confidence after 20 observations
        }

    def _update_session_preferences(self, observation: LearningObservation) -> None:
        """Update profile based on session data."""
        data = observation.data
        profile = self.profile

        # Update preferred session length (weighted average)
        weight = 0.3
        profile.preferred_session_length_minutes = int(
            profile.preferred_session_length_minutes * (1 - weight) +
            data["duration_minutes"] * weight
        )

        # Update hint usage rate
        if data["total_hints_available"] > 0:
            session_hint_rate = data["hints_used"] / data["total_hints_available"]
            profile.hint_usage_rate = (
                profile.hint_usage_rate * 0.7 +
                session_hint_rate * 0.3
            )

        # Update exercise/theory preference
        total_activities = data["exercises_completed"] + data["topics_read"]
        if total_activities > 0:
            exercise_ratio = data["exercises_completed"] / total_activities
            profile.exercises_before_theory_ratio = (
                profile.exercises_before_theory_ratio * 0.7 +
                exercise_ratio * 0.3
            )

        profile.observations_count += 1
        profile.last_updated = datetime.now()

    def _update_exercise_patterns(self, observation: LearningObservation) -> None:
        """Update profile based on exercise attempt."""
        data = observation.data
        profile = self.profile

        # Update retry persistence based on attempt number and score
        if data["attempt_number"] > 1:
            # They retried - update persistence
            profile.retry_persistence = min(1.0, profile.retry_persistence * 1.1)
        elif data["score"] < 70:
            # They didn't retry despite low score
            profile.retry_persistence = max(0.1, profile.retry_persistence * 0.9)

        # Update time-of-day performance
        hour = data["hour"]
        score_normalized = data["score"] / 100

        if 5 <= hour < 12:
            profile.morning_performance = (
                profile.morning_performance * 0.8 +
                score_normalized * 0.2
            )
        elif 12 <= hour < 17:
            profile.afternoon_performance = (
                profile.afternoon_performance * 0.8 +
                score_normalized * 0.2
            )
        else:
            profile.evening_performance = (
                profile.evening_performance * 0.8 +
                score_normalized * 0.2
            )

        # Determine best time
        performances = {
            "morning": profile.morning_performance,
            "afternoon": profile.afternoon_performance,
            "evening": profile.evening_performance,
        }
        profile.best_time_of_day = max(performances, key=performances.get)

        profile.observations_count += 1
        profile.last_updated = datetime.now()

    def _update_style_scores(self, observation: LearningObservation) -> None:
        """Update learning style scores based on content interaction."""
        data = observation.data
        profile = self.profile

        content_type = data["content_type"]
        engagement = data["engagement_seconds"]

        # Map content types to styles
        style_mapping = {
            "diagram": "visual",
            "chart": "visual",
            "image": "visual",
            "text": "reading",
            "documentation": "reading",
            "example": "reading",
            "exercise": "kinesthetic",
            "practice": "kinesthetic",
            "coding": "kinesthetic",
        }

        style = style_mapping.get(content_type, "reading")

        # Update style score
        if style not in profile.style_scores:
            profile.style_scores[style] = 0.0

        # Normalize engagement to a score
        engagement_score = min(1.0, engagement / 300)  # 5 minutes = full score
        profile.style_scores[style] = (
            profile.style_scores[style] * 0.9 +
            engagement_score * 0.1
        )

        # Determine primary style
        if profile.style_scores:
            max_style = max(profile.style_scores, key=profile.style_scores.get)
            max_score = profile.style_scores[max_style]

            # Check if multimodal (no clear dominant style)
            scores = list(profile.style_scores.values())
            if len(scores) >= 2 and max_score - min(scores) < 0.2:
                profile.primary_style = LearningStyle.MULTIMODAL
            else:
                profile.primary_style = LearningStyle(max_style)

        profile.observations_count += 1
        profile.last_updated = datetime.now()

    def _identify_strengths(self) -> list[str]:
        """Identify learning strengths."""
        strengths = []
        profile = self.profile

        if profile.retry_persistence > 0.7:
            strengths.append("High persistence - keeps trying until success")

        if profile.hint_usage_rate < 0.3:
            strengths.append("Independent learner - solves problems without much help")

        if profile.preferred_session_length_minutes > 60:
            strengths.append("Good focus - can maintain long study sessions")

        best_time = self.get_optimal_study_time()
        strengths.append(f"Most productive during {best_time}")

        return strengths

    def _generate_suggestions(self) -> list[str]:
        """Generate personalized suggestions."""
        suggestions = []
        profile = self.profile

        if profile.retry_persistence < 0.3:
            suggestions.append("Try to persist through challenges - struggle is part of learning")

        if profile.hint_usage_rate > 0.7:
            suggestions.append("Try solving problems without hints first to strengthen problem-solving skills")

        if profile.preferred_session_length_minutes < 20:
            suggestions.append("Consider longer study sessions for deeper learning")

        if profile.exercises_before_theory_ratio < 0.3:
            suggestions.append("Try more hands-on practice to reinforce concepts")

        return suggestions

    def _load(self):
        """Load profile from storage."""
        if not self.storage_path.exists():
            return

        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.profile = LearningProfile.from_dict(data.get("profile", {}))

        except (json.JSONDecodeError, KeyError):
            pass

    def _save(self):
        """Save profile to storage."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "version": 1,
            "profile": self.profile.to_dict(),
        }

        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
