"""
Skill Analyzer

Analyzes student performance to identify skill gaps and strengths.
Provides targeted recommendations for improvement.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


class SkillLevel(Enum):
    """Proficiency levels for skills."""
    NOVICE = 1
    BEGINNER = 2
    INTERMEDIATE = 3
    ADVANCED = 4
    EXPERT = 5


@dataclass
class SkillGap:
    """Represents a gap in student's knowledge."""
    skill_id: str
    skill_name: str
    current_level: SkillLevel
    target_level: SkillLevel
    priority: float  # 0.0 to 1.0, higher = more urgent
    related_topics: list[str] = field(default_factory=list)
    recommended_exercises: list[str] = field(default_factory=list)
    estimated_time_minutes: int = 0
    blocking_skills: list[str] = field(default_factory=list)  # Skills that need this as prerequisite

    @property
    def gap_size(self) -> int:
        """Size of the gap in levels."""
        return self.target_level.value - self.current_level.value

    def to_dict(self) -> dict:
        return {
            "skill_id": self.skill_id,
            "skill_name": self.skill_name,
            "current_level": self.current_level.name,
            "target_level": self.target_level.name,
            "gap_size": self.gap_size,
            "priority": self.priority,
            "related_topics": self.related_topics,
            "recommended_exercises": self.recommended_exercises,
            "estimated_time_minutes": self.estimated_time_minutes,
            "blocking_skills": self.blocking_skills,
        }


@dataclass
class SkillAssessment:
    """Assessment result for a single skill."""
    skill_id: str
    skill_name: str
    level: SkillLevel
    confidence: float  # 0.0 to 1.0, how confident we are in this assessment
    evidence: list[str] = field(default_factory=list)  # Exercise IDs that contributed
    last_assessed: Optional[datetime] = None
    trend: str = "stable"  # "improving", "declining", "stable"

    def to_dict(self) -> dict:
        return {
            "skill_id": self.skill_id,
            "skill_name": self.skill_name,
            "level": self.level.name,
            "level_value": self.level.value,
            "confidence": self.confidence,
            "evidence_count": len(self.evidence),
            "last_assessed": self.last_assessed.isoformat() if self.last_assessed else None,
            "trend": self.trend,
        }


class SkillAnalyzer:
    """
    Analyzes student performance to assess skill levels and identify gaps.

    Uses exercise results, attempt patterns, and time spent to evaluate
    proficiency in different skill areas.
    """

    # Skill taxonomy with prerequisites
    SKILL_PREREQUISITES = {
        # Programming fundamentals
        "variables": [],
        "types": ["variables"],
        "operators": ["variables", "types"],
        "control_flow": ["variables", "operators"],
        "functions": ["variables", "control_flow"],
        "data_structures": ["variables", "types"],
        "algorithms": ["data_structures", "control_flow", "functions"],

        # Rust-specific
        "ownership": ["variables", "types", "functions"],
        "borrowing": ["ownership"],
        "lifetimes": ["borrowing", "functions"],
        "traits": ["functions", "types"],
        "generics": ["traits", "types"],
        "error_handling": ["control_flow", "types"],
        "pattern_matching": ["control_flow", "types"],
        "concurrency": ["ownership", "lifetimes"],

        # Python-specific
        "list_comprehensions": ["data_structures", "control_flow"],
        "decorators": ["functions"],
        "generators": ["functions", "control_flow"],
        "async_await": ["functions", "generators"],
        "classes": ["functions", "types"],
        "metaclasses": ["classes", "decorators"],

        # General CS concepts
        "testing": ["functions"],
        "debugging": ["control_flow"],
        "refactoring": ["functions", "data_structures"],
        "performance": ["algorithms", "data_structures"],
        "design_patterns": ["classes", "functions"],
    }

    def __init__(self, progress: dict, curriculum: dict):
        """
        Initialize the skill analyzer.

        Args:
            progress: Student's progress data
            curriculum: Course curriculum data
        """
        self.progress = progress
        self.curriculum = curriculum
        self._skill_cache: dict[str, SkillAssessment] = {}

    def analyze_all_skills(self) -> dict[str, SkillAssessment]:
        """
        Analyze all skills based on completed exercises.

        Returns:
            Dictionary mapping skill IDs to assessments
        """
        skills = {}
        modules = self.progress.get("modules", {})

        # Collect all exercise results
        exercise_results = []
        for module_id, module_data in modules.items():
            for exercise_id, ex_data in module_data.get("exercises", {}).items():
                exercise_results.append({
                    "module_id": module_id,
                    "exercise_id": exercise_id,
                    "status": ex_data.get("status"),
                    "score": ex_data.get("score", 0),
                    "attempts": ex_data.get("attempts", 1),
                    "topics": self._get_exercise_topics(module_id, exercise_id),
                })

        # Map topics to skills and aggregate scores
        skill_scores: dict[str, list[tuple[float, int]]] = {}  # skill -> [(score, attempts)]

        for result in exercise_results:
            if result["status"] != "completed":
                continue

            for topic in result["topics"]:
                skill_id = self._topic_to_skill(topic)
                if skill_id:
                    if skill_id not in skill_scores:
                        skill_scores[skill_id] = []
                    skill_scores[skill_id].append((
                        result["score"],
                        result["attempts"],
                    ))

        # Calculate skill levels
        for skill_id, scores in skill_scores.items():
            level, confidence = self._calculate_skill_level(scores)
            trend = self._calculate_trend(skill_id, scores)

            skills[skill_id] = SkillAssessment(
                skill_id=skill_id,
                skill_name=self._skill_name(skill_id),
                level=level,
                confidence=confidence,
                evidence=[f"ex_{i}" for i in range(len(scores))],
                last_assessed=datetime.now(),
                trend=trend,
            )

        self._skill_cache = skills
        return skills

    def identify_gaps(
        self,
        target_skills: Optional[list[str]] = None,
        target_level: SkillLevel = SkillLevel.INTERMEDIATE
    ) -> list[SkillGap]:
        """
        Identify skill gaps based on current assessments.

        Args:
            target_skills: Specific skills to check (None = all)
            target_level: Desired proficiency level

        Returns:
            List of skill gaps sorted by priority
        """
        if not self._skill_cache:
            self.analyze_all_skills()

        gaps = []

        # Determine which skills to check
        skills_to_check = target_skills or list(self.SKILL_PREREQUISITES.keys())

        for skill_id in skills_to_check:
            current = self._skill_cache.get(skill_id)
            current_level = current.level if current else SkillLevel.NOVICE

            if current_level.value < target_level.value:
                # Calculate priority based on:
                # 1. How many other skills depend on this
                # 2. How big the gap is
                # 3. How recently we assessed it

                blocking_skills = self._get_blocking_skills(skill_id)
                gap_size = target_level.value - current_level.value

                priority = min(1.0, (
                    0.3 * (len(blocking_skills) / 5) +  # Dependency factor
                    0.4 * (gap_size / 4) +  # Gap size factor
                    0.3 * (1.0 if not current else 0.5)  # Novelty factor
                ))

                gaps.append(SkillGap(
                    skill_id=skill_id,
                    skill_name=self._skill_name(skill_id),
                    current_level=current_level,
                    target_level=target_level,
                    priority=priority,
                    related_topics=self._get_related_topics(skill_id),
                    recommended_exercises=self._get_recommended_exercises(skill_id, gap_size),
                    estimated_time_minutes=gap_size * 30,  # Rough estimate
                    blocking_skills=blocking_skills,
                ))

        # Sort by priority (highest first)
        gaps.sort(key=lambda g: g.priority, reverse=True)
        return gaps

    def get_strengths(self, min_level: SkillLevel = SkillLevel.INTERMEDIATE) -> list[SkillAssessment]:
        """
        Get skills where the student is strong.

        Args:
            min_level: Minimum level to consider a strength

        Returns:
            List of strong skills
        """
        if not self._skill_cache:
            self.analyze_all_skills()

        strengths = [
            skill for skill in self._skill_cache.values()
            if skill.level.value >= min_level.value
        ]
        strengths.sort(key=lambda s: s.level.value, reverse=True)
        return strengths

    def get_learning_path(self, target_skill: str) -> list[str]:
        """
        Get the optimal learning path to acquire a skill.

        Returns skills in order they should be learned,
        based on prerequisites.

        Args:
            target_skill: The skill to learn

        Returns:
            Ordered list of skill IDs
        """
        if not self._skill_cache:
            self.analyze_all_skills()

        # BFS to find all prerequisites
        path = []
        visited = set()
        queue = [target_skill]

        while queue:
            skill = queue.pop(0)
            if skill in visited:
                continue
            visited.add(skill)

            # Check if already proficient
            current = self._skill_cache.get(skill)
            if current and current.level.value >= SkillLevel.INTERMEDIATE.value:
                continue

            path.append(skill)

            # Add prerequisites to queue
            prereqs = self.SKILL_PREREQUISITES.get(skill, [])
            for prereq in prereqs:
                if prereq not in visited:
                    queue.append(prereq)

        # Reverse to get correct order (prerequisites first)
        path.reverse()
        return path

    def _calculate_skill_level(self, scores: list[tuple[float, int]]) -> tuple[SkillLevel, float]:
        """Calculate skill level from exercise scores."""
        if not scores:
            return SkillLevel.NOVICE, 0.0

        # Weight recent scores more heavily
        weighted_sum = 0
        weight_total = 0

        for i, (score, attempts) in enumerate(scores):
            # More recent = higher weight
            recency_weight = 1 + (i / len(scores))

            # Fewer attempts = higher weight
            attempt_weight = 1 / attempts

            weight = recency_weight * attempt_weight
            weighted_sum += score * weight
            weight_total += weight

        avg_score = weighted_sum / weight_total if weight_total > 0 else 0

        # Map score to level
        if avg_score >= 90:
            level = SkillLevel.EXPERT
        elif avg_score >= 75:
            level = SkillLevel.ADVANCED
        elif avg_score >= 60:
            level = SkillLevel.INTERMEDIATE
        elif avg_score >= 40:
            level = SkillLevel.BEGINNER
        else:
            level = SkillLevel.NOVICE

        # Confidence based on number of data points
        confidence = min(1.0, len(scores) / 5)

        return level, confidence

    def _calculate_trend(self, skill_id: str, scores: list[tuple[float, int]]) -> str:
        """Calculate if skill is improving, declining, or stable."""
        if len(scores) < 3:
            return "stable"

        # Compare first half to second half
        mid = len(scores) // 2
        first_half = sum(s for s, _ in scores[:mid]) / mid
        second_half = sum(s for s, _ in scores[mid:]) / (len(scores) - mid)

        diff = second_half - first_half

        if diff > 10:
            return "improving"
        elif diff < -10:
            return "declining"
        return "stable"

    def _get_blocking_skills(self, skill_id: str) -> list[str]:
        """Get skills that have this skill as a prerequisite."""
        blocking = []
        for skill, prereqs in self.SKILL_PREREQUISITES.items():
            if skill_id in prereqs:
                blocking.append(skill)
        return blocking

    def _get_exercise_topics(self, module_id: str, exercise_id: str) -> list[str]:
        """Get topics covered by an exercise."""
        for module in self.curriculum.get("modules", []):
            if module.get("id") == module_id:
                for exercise in module.get("exercises", []):
                    if isinstance(exercise, dict) and exercise.get("id") == exercise_id:
                        return exercise.get("topics", [])
        return []

    def _topic_to_skill(self, topic: str) -> Optional[str]:
        """Map a topic name to a skill ID."""
        # Simple mapping - in production this would be more sophisticated
        topic_lower = topic.lower().replace("-", "_").replace(" ", "_")
        if topic_lower in self.SKILL_PREREQUISITES:
            return topic_lower
        return None

    def _skill_name(self, skill_id: str) -> str:
        """Get human-readable name for a skill."""
        return skill_id.replace("_", " ").title()

    def _get_related_topics(self, skill_id: str) -> list[str]:
        """Get topics related to a skill."""
        # In production, this would query the curriculum
        return [skill_id]

    def _get_recommended_exercises(self, skill_id: str, gap_size: int) -> list[str]:
        """Get recommended exercises for a skill."""
        # In production, this would search the exercise database
        difficulties = {
            1: ["basic"],
            2: ["basic", "intermediate"],
            3: ["intermediate", "advanced"],
            4: ["advanced", "challenge"],
        }
        return difficulties.get(gap_size, ["intermediate"])
