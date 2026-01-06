"""
Adaptive Learning Engine

The main orchestrator that combines all learning components:
- Skill analysis
- Knowledge graph
- Spaced repetition
- Learning styles
- Analytics
- Recommendations

Provides a unified interface for intelligent tutoring.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional
import json

from .skill_analyzer import SkillAnalyzer, SkillLevel
from .knowledge_graph import KnowledgeGraph, Topic, Prerequisite
from .spaced_repetition import SpacedRepetitionSystem, quality_from_exercise_result
from .learning_styles import LearningStyleAnalyzer
from .analytics import LearningAnalytics, PerformanceMetrics
from .recommendations import RecommendationEngine, Recommendation


@dataclass
class LearningState:
    """Current state of the student's learning."""
    current_module: Optional[str]
    current_topic: Optional[str]
    skill_level: SkillLevel
    session_active: bool
    session_duration_minutes: int
    items_due_for_review: int
    next_recommendation: Optional[Recommendation]


class AdaptiveLearningEngine:
    """
    Main orchestrator for adaptive learning.

    Combines all learning components to provide:
    - Intelligent curriculum adaptation
    - Personalized recommendations
    - Skill-based progression
    - Spaced repetition integration
    - Learning analytics
    """

    def __init__(self, tutor_path: Optional[Path] = None):
        """
        Initialize the adaptive learning engine.

        Args:
            tutor_path: Path to .tutor directory
        """
        self.tutor_path = tutor_path or Path.cwd() / ".tutor"

        # Load data
        self.config = self._load_json("config.json")
        self.progress = self._load_json("progress.json")
        self.curriculum = self._load_json("curriculum.json")

        # Initialize components
        self.skill_analyzer = SkillAnalyzer(self.progress, self.curriculum)
        self.knowledge_graph = KnowledgeGraph(self.tutor_path / "knowledge_graph.json")
        self.srs = SpacedRepetitionSystem(self.tutor_path / "srs.json")
        self.style_analyzer = LearningStyleAnalyzer(self.tutor_path / "learning_profile.json")
        self.analytics = LearningAnalytics(self.progress, self.tutor_path / "sessions")

    def get_current_state(self) -> LearningState:
        """
        Get the current learning state.

        Returns:
            LearningState with current progress info
        """
        # Analyze skills
        skills = self.skill_analyzer.analyze_all_skills()

        # Calculate overall skill level
        if skills:
            avg_level = sum(s.level.value for s in skills.values()) / len(skills)
            if avg_level >= 4:
                skill_level = SkillLevel.ADVANCED
            elif avg_level >= 3:
                skill_level = SkillLevel.INTERMEDIATE
            elif avg_level >= 2:
                skill_level = SkillLevel.BEGINNER
            else:
                skill_level = SkillLevel.NOVICE
        else:
            skill_level = SkillLevel.NOVICE

        # Get due reviews
        due_items = self.srs.get_due_items()

        # Get next recommendation
        recommendation = self.get_next_recommendation()

        # Check session status
        stats = self.progress.get("statistics", {})
        last_session = stats.get("last_session")
        today = datetime.now().strftime("%Y-%m-%d")
        session_active = last_session == today

        return LearningState(
            current_module=self.progress.get("current_module"),
            current_topic=self.progress.get("current_topic"),
            skill_level=skill_level,
            session_active=session_active,
            session_duration_minutes=stats.get("current_session_minutes", 0),
            items_due_for_review=len(due_items),
            next_recommendation=recommendation,
        )

    def get_next_recommendation(
        self,
        available_minutes: int = 60,
        context: str = "general"
    ) -> Recommendation:
        """
        Get the next recommended action.

        Args:
            available_minutes: Time available
            context: Study context

        Returns:
            Best recommendation
        """
        # Get skill gaps
        skill_gaps = self.skill_analyzer.identify_gaps()

        # Get learning profile
        profile = self.style_analyzer.profile.to_dict()

        # Get due SRS items
        due_items = self.srs.get_due_items()

        # Create recommendation engine
        engine = RecommendationEngine(
            progress=self.progress,
            curriculum=self.curriculum,
            skill_gaps=skill_gaps,
            learning_profile=profile,
            srs_due_items=due_items,
        )

        return engine.get_next_action()

    def get_personalized_curriculum(self) -> dict:
        """
        Generate a personalized curriculum based on the student's progress.

        Returns:
            Adapted curriculum with priorities and estimates
        """
        # Get skill gaps
        gaps = self.skill_analyzer.identify_gaps()
        gap_skills = {g.skill_id for g in gaps}

        # Get completed topics
        completed = self._get_completed_topics()

        # Adapt curriculum
        adapted_modules = []

        for module in self.curriculum.get("modules", []):
            module_id = module.get("id")
            module_progress = self.progress.get("modules", {}).get(module_id, {})

            # Calculate priority based on gaps
            module_topics = [t.get("id") if isinstance(t, dict) else t for t in module.get("topics", [])]
            relevant_gaps = [g for g in gaps if any(t in g.related_topics for t in module_topics)]

            priority = "normal"
            if module_progress.get("status") == "completed":
                priority = "completed"
            elif relevant_gaps:
                priority = "high" if max(g.priority for g in relevant_gaps) > 0.7 else "medium"

            adapted_modules.append({
                **module,
                "priority": priority,
                "progress_percentage": self._calculate_module_progress(module_id),
                "estimated_time_remaining": self._estimate_remaining_time(module),
                "skill_gaps_addressed": [g.skill_name for g in relevant_gaps[:3]],
            })

        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "normal": 2, "completed": 3}
        adapted_modules.sort(key=lambda m: priority_order.get(m["priority"], 2))

        return {
            **self.curriculum,
            "modules": adapted_modules,
            "personalized_at": datetime.now().isoformat(),
            "total_gaps": len(gaps),
        }

    def record_exercise_completion(
        self,
        module_id: str,
        exercise_id: str,
        score: int,
        attempts: int,
        time_spent_minutes: int,
    ) -> dict:
        """
        Record exercise completion and update all systems.

        Args:
            module_id: Module containing the exercise
            exercise_id: Exercise ID
            score: Score achieved (0-100)
            attempts: Number of attempts
            time_spent_minutes: Time spent

        Returns:
            Summary of updates
        """
        # Update progress
        self._update_exercise_progress(module_id, exercise_id, score, attempts)

        # Update SRS
        item_id = f"exercise:{module_id}:{exercise_id}"
        if item_id not in self.srs.items:
            self.srs.add_item(
                item_id=item_id,
                item_type="exercise",
                content_ref=f"lessons/{module_id}/exercises/{exercise_id}",
                title=exercise_id,
            )

        quality = quality_from_exercise_result(score, attempts)
        self.srs.record_review(item_id, quality)

        # Update learning style analyzer
        self.style_analyzer.record_exercise_attempt(
            exercise_id=exercise_id,
            attempt_number=attempts,
            score=score,
            time_spent_minutes=time_spent_minutes,
            used_hints=False,  # Would need to track this
        )

        # Re-analyze skills
        skills = self.skill_analyzer.analyze_all_skills()

        # Calculate new metrics
        metrics = self.analytics.calculate_metrics()

        return {
            "exercise_recorded": True,
            "score": score,
            "srs_next_review": self.srs.items[item_id].next_review.isoformat(),
            "new_average_score": metrics.average_score,
            "skill_updates": {
                s.skill_id: s.level.name
                for s in skills.values()
            },
        }

    def start_session(self) -> dict:
        """
        Start a new study session.

        Returns:
            Session info and recommendations
        """
        # Start session in analytics
        self._start_session_tracking()

        # Get state
        state = self.get_current_state()

        # Get content recommendations
        content_recs = self.style_analyzer.get_content_recommendations()

        # Get top recommendations
        engine = RecommendationEngine(
            progress=self.progress,
            curriculum=self.curriculum,
            skill_gaps=self.skill_analyzer.identify_gaps(),
            learning_profile=self.style_analyzer.profile.to_dict(),
            srs_due_items=self.srs.get_due_items(),
        )

        recommendations = engine.get_recommendations(available_minutes=60)

        return {
            "session_started": True,
            "current_state": {
                "module": state.current_module,
                "topic": state.current_topic,
                "skill_level": state.skill_level.name,
            },
            "items_due_for_review": state.items_due_for_review,
            "content_preferences": content_recs,
            "recommendations": [r.to_dict() for r in recommendations[:5]],
            "optimal_study_time": self.style_analyzer.get_optimal_study_time(),
        }

    def end_session(
        self,
        topics_covered: list[str],
        exercises_completed: list[str],
    ) -> dict:
        """
        End the current study session.

        Args:
            topics_covered: Topics studied
            exercises_completed: Exercises done

        Returns:
            Session summary
        """
        # Record session end
        self.style_analyzer.record_session(
            duration_minutes=self.progress.get("statistics", {}).get("current_session_minutes", 30),
            exercises_completed=len(exercises_completed),
            topics_read=len(topics_covered),
            hints_used=0,  # Would need to track
            total_hints_available=len(exercises_completed) * 3,  # Estimate
        )

        # Get weekly report
        weekly = self.analytics.get_weekly_report()

        # Get insights
        insights = self.analytics.generate_insights()

        return {
            "session_ended": True,
            "topics_covered": topics_covered,
            "exercises_completed": exercises_completed,
            "weekly_summary": weekly["summary"],
            "insights": [i.to_dict() for i in insights[:3]],
            "streak_days": self.progress.get("statistics", {}).get("streak_days", 0),
        }

    def get_comprehensive_report(self) -> dict:
        """
        Generate a comprehensive learning report.

        Returns:
            Full report with all analytics
        """
        # Performance metrics
        metrics = self.analytics.calculate_metrics()

        # Skill assessment
        skills = self.skill_analyzer.analyze_all_skills()

        # Skill gaps
        gaps = self.skill_analyzer.identify_gaps()

        # SRS stats
        srs_stats = self.srs.get_statistics()

        # Learning style
        style = self.style_analyzer.get_style_summary()

        # Improvement plan
        improvement = self.analytics.get_improvement_plan()

        # Weekly report
        weekly = self.analytics.get_weekly_report()

        return {
            "generated_at": datetime.now().isoformat(),
            "performance": metrics.to_dict(),
            "skills": {
                "assessments": {s.skill_id: s.to_dict() for s in skills.values()},
                "strengths": [s.to_dict() for s in self.skill_analyzer.get_strengths()],
                "gaps": [g.to_dict() for g in gaps],
            },
            "retention": srs_stats,
            "learning_style": style,
            "weekly_summary": weekly,
            "improvement_plan": improvement,
        }

    def _load_json(self, filename: str) -> dict:
        """Load a JSON file from tutor path."""
        filepath = self.tutor_path / filename
        if not filepath.exists():
            return {}
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def _save_json(self, filename: str, data: dict) -> None:
        """Save data to a JSON file."""
        filepath = self.tutor_path / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _get_completed_topics(self) -> set[str]:
        """Get set of completed topic IDs."""
        completed = set()
        for module_id, module_data in self.progress.get("modules", {}).items():
            if module_data.get("status") == "completed":
                completed.add(module_id)
            for ex_id, ex_data in module_data.get("exercises", {}).items():
                if ex_data.get("status") == "completed":
                    completed.add(f"{module_id}:{ex_id}")
        return completed

    def _calculate_module_progress(self, module_id: str) -> float:
        """Calculate progress percentage for a module."""
        module_data = None
        for m in self.curriculum.get("modules", []):
            if m.get("id") == module_id:
                module_data = m
                break

        if not module_data:
            return 0.0

        exercises = module_data.get("exercises", [])
        if not exercises:
            return 0.0

        total = len(exercises) if isinstance(exercises, list) else exercises
        if isinstance(exercises, int):
            # Count completed exercises in progress
            module_progress = self.progress.get("modules", {}).get(module_id, {})
            completed = sum(
                1 for ex in module_progress.get("exercises", {}).values()
                if ex.get("status") == "completed"
            )
        else:
            module_progress = self.progress.get("modules", {}).get(module_id, {})
            completed = sum(
                1 for ex in exercises
                if module_progress.get("exercises", {}).get(
                    ex.get("id") if isinstance(ex, dict) else ex, {}
                ).get("status") == "completed"
            )

        return (completed / total * 100) if total > 0 else 0.0

    def _estimate_remaining_time(self, module: dict) -> int:
        """Estimate remaining time for a module in minutes."""
        module_id = module.get("id")
        progress_pct = self._calculate_module_progress(module_id)

        total_time = module.get("estimated_hours", 4) * 60
        remaining = total_time * (1 - progress_pct / 100)

        return int(remaining)

    def _update_exercise_progress(
        self,
        module_id: str,
        exercise_id: str,
        score: int,
        attempts: int
    ) -> None:
        """Update exercise progress in storage."""
        if "modules" not in self.progress:
            self.progress["modules"] = {}

        if module_id not in self.progress["modules"]:
            self.progress["modules"][module_id] = {
                "status": "in_progress",
                "started_at": datetime.now().isoformat(),
                "exercises": {},
            }

        self.progress["modules"][module_id]["exercises"][exercise_id] = {
            "status": "completed" if score >= 60 else "in_progress",
            "score": score,
            "attempts": attempts,
            "updated_at": datetime.now().isoformat(),
        }

        self._save_json("progress.json", self.progress)

    def _start_session_tracking(self) -> None:
        """Start tracking a new session."""
        stats = self.progress.get("statistics", {})
        today = datetime.now().strftime("%Y-%m-%d")

        # Update streak
        last_session = stats.get("last_session")
        if last_session:
            last_date = datetime.strptime(last_session, "%Y-%m-%d")
            today_date = datetime.strptime(today, "%Y-%m-%d")
            diff = (today_date - last_date).days

            if diff == 1:
                stats["streak_days"] = stats.get("streak_days", 0) + 1
            elif diff > 1:
                stats["streak_days"] = 1
        else:
            stats["streak_days"] = 1

        stats["last_session"] = today
        self.progress["statistics"] = stats
        self._save_json("progress.json", self.progress)
