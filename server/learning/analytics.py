"""
Learning Analytics

Provides insights into learning progress, performance trends,
and actionable recommendations for improvement.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
import json
from pathlib import Path


@dataclass
class PerformanceMetrics:
    """Aggregated performance metrics."""
    # Overall metrics
    total_exercises_completed: int = 0
    total_exercises_attempted: int = 0
    average_score: float = 0.0
    total_time_minutes: int = 0

    # Trend metrics
    score_trend: str = "stable"  # improving, declining, stable
    speed_trend: str = "stable"  # faster, slower, stable
    consistency_score: float = 0.0  # 0-1, how consistent performance is

    # Time metrics
    average_session_minutes: int = 0
    total_sessions: int = 0
    study_streak_days: int = 0
    longest_streak_days: int = 0

    # Efficiency metrics
    first_attempt_success_rate: float = 0.0
    average_attempts_per_exercise: float = 1.0
    hint_dependency_score: float = 0.0  # 0=never uses, 1=always uses

    # Topic-specific
    strongest_topics: list[str] = field(default_factory=list)
    weakest_topics: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "overall": {
                "exercises_completed": self.total_exercises_completed,
                "exercises_attempted": self.total_exercises_attempted,
                "completion_rate": (
                    self.total_exercises_completed / self.total_exercises_attempted
                    if self.total_exercises_attempted > 0 else 0
                ),
                "average_score": round(self.average_score, 1),
                "total_time_hours": round(self.total_time_minutes / 60, 1),
            },
            "trends": {
                "score_trend": self.score_trend,
                "speed_trend": self.speed_trend,
                "consistency": round(self.consistency_score * 100, 1),
            },
            "sessions": {
                "total_sessions": self.total_sessions,
                "average_minutes": self.average_session_minutes,
                "current_streak": self.study_streak_days,
                "longest_streak": self.longest_streak_days,
            },
            "efficiency": {
                "first_attempt_success_rate": round(self.first_attempt_success_rate * 100, 1),
                "average_attempts": round(self.average_attempts_per_exercise, 1),
                "hint_dependency": round(self.hint_dependency_score * 100, 1),
            },
            "topics": {
                "strongest": self.strongest_topics[:5],
                "weakest": self.weakest_topics[:5],
            },
        }


@dataclass
class ProgressInsight:
    """An insight about the student's progress."""
    category: str  # achievement, concern, suggestion, milestone
    title: str
    description: str
    priority: int = 1  # 1=high, 2=medium, 3=low
    action: Optional[str] = None  # Recommended action
    data: dict = field(default_factory=dict)  # Supporting data

    def to_dict(self) -> dict:
        return {
            "category": self.category,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "action": self.action,
            "data": self.data,
        }


class LearningAnalytics:
    """
    Analyzes learning data to provide insights and recommendations.

    Tracks:
    - Performance over time
    - Learning velocity
    - Topic strengths/weaknesses
    - Study patterns
    - Engagement metrics
    """

    def __init__(self, progress: dict, sessions_path: Optional[Path] = None):
        """
        Initialize analytics.

        Args:
            progress: Student's progress data
            sessions_path: Path to session files
        """
        self.progress = progress
        self.sessions_path = sessions_path or Path.cwd() / ".tutor" / "sessions"

    def calculate_metrics(self) -> PerformanceMetrics:
        """
        Calculate comprehensive performance metrics.

        Returns:
            PerformanceMetrics with all calculated values
        """
        metrics = PerformanceMetrics()

        # Get all exercise data
        exercises = self._get_all_exercises()
        sessions = self._get_all_sessions()

        if not exercises:
            return metrics

        # Overall metrics
        metrics.total_exercises_attempted = len(exercises)
        metrics.total_exercises_completed = sum(
            1 for e in exercises if e.get("status") == "completed"
        )

        scores = [e.get("score", 0) for e in exercises if e.get("score")]
        if scores:
            metrics.average_score = sum(scores) / len(scores)

        # Time metrics
        if sessions:
            durations = [s.get("duration_minutes", 0) for s in sessions]
            metrics.total_time_minutes = sum(durations)
            metrics.total_sessions = len(sessions)
            metrics.average_session_minutes = (
                sum(durations) // len(durations) if durations else 0
            )

        # Calculate streaks
        stats = self.progress.get("statistics", {})
        metrics.study_streak_days = stats.get("streak_days", 0)
        metrics.longest_streak_days = max(
            metrics.study_streak_days,
            stats.get("longest_streak", 0)
        )

        # Efficiency metrics
        first_attempt_successes = sum(
            1 for e in exercises
            if e.get("status") == "completed" and e.get("attempts", 1) == 1
        )
        if exercises:
            metrics.first_attempt_success_rate = first_attempt_successes / len(exercises)

        attempts = [e.get("attempts", 1) for e in exercises]
        metrics.average_attempts_per_exercise = sum(attempts) / len(attempts) if attempts else 1

        # Calculate trends
        metrics.score_trend = self._calculate_score_trend(exercises)
        metrics.consistency_score = self._calculate_consistency(scores)

        # Topic analysis
        topic_scores = self._calculate_topic_scores(exercises)
        sorted_topics = sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)

        metrics.strongest_topics = [t for t, _ in sorted_topics[:5] if topic_scores[t] >= 70]
        metrics.weakest_topics = [t for t, _ in sorted_topics[-5:] if topic_scores[t] < 70]

        return metrics

    def generate_insights(self) -> list[ProgressInsight]:
        """
        Generate insights based on performance analysis.

        Returns:
            List of ProgressInsight objects
        """
        insights = []
        metrics = self.calculate_metrics()

        # Achievement insights
        insights.extend(self._check_achievements(metrics))

        # Concern insights
        insights.extend(self._check_concerns(metrics))

        # Suggestion insights
        insights.extend(self._generate_suggestions(metrics))

        # Milestone insights
        insights.extend(self._check_milestones(metrics))

        # Sort by priority
        insights.sort(key=lambda i: i.priority)

        return insights

    def get_weekly_report(self) -> dict:
        """
        Generate a weekly progress report.

        Returns:
            Dictionary with weekly summary
        """
        now = datetime.now()
        week_ago = now - timedelta(days=7)

        # Get this week's data
        sessions = self._get_all_sessions()
        week_sessions = [
            s for s in sessions
            if self._parse_date(s.get("date", "")) >= week_ago
        ]

        exercises = self._get_all_exercises()
        week_exercises = [
            e for e in exercises
            if self._parse_date(e.get("updated_at", "")) >= week_ago
        ]

        # Calculate weekly metrics
        week_time = sum(s.get("duration_minutes", 0) for s in week_sessions)
        week_completed = sum(1 for e in week_exercises if e.get("status") == "completed")
        week_scores = [e.get("score", 0) for e in week_exercises if e.get("score")]
        week_avg = sum(week_scores) / len(week_scores) if week_scores else 0

        # Compare to previous week
        two_weeks_ago = week_ago - timedelta(days=7)
        prev_sessions = [
            s for s in sessions
            if two_weeks_ago <= self._parse_date(s.get("date", "")) < week_ago
        ]
        prev_time = sum(s.get("duration_minutes", 0) for s in prev_sessions)

        time_change = week_time - prev_time
        time_change_pct = (time_change / prev_time * 100) if prev_time > 0 else 0

        return {
            "period": {
                "start": week_ago.isoformat(),
                "end": now.isoformat(),
            },
            "summary": {
                "study_time_minutes": week_time,
                "study_time_hours": round(week_time / 60, 1),
                "sessions_count": len(week_sessions),
                "exercises_completed": week_completed,
                "average_score": round(week_avg, 1),
            },
            "comparison": {
                "time_change_minutes": time_change,
                "time_change_percent": round(time_change_pct, 1),
                "trend": "up" if time_change > 0 else ("down" if time_change < 0 else "stable"),
            },
            "insights": [i.to_dict() for i in self.generate_insights()[:3]],
        }

    def get_improvement_plan(self) -> dict:
        """
        Generate a personalized improvement plan.

        Returns:
            Dictionary with improvement recommendations
        """
        metrics = self.calculate_metrics()
        insights = self.generate_insights()

        # Identify areas for improvement
        improvement_areas = []

        if metrics.first_attempt_success_rate < 0.5:
            improvement_areas.append({
                "area": "First-attempt success",
                "current": f"{metrics.first_attempt_success_rate * 100:.0f}%",
                "target": "70%",
                "action": "Review concepts before attempting exercises",
            })

        if metrics.average_attempts_per_exercise > 2:
            improvement_areas.append({
                "area": "Exercise efficiency",
                "current": f"{metrics.average_attempts_per_exercise:.1f} attempts/exercise",
                "target": "1.5 attempts/exercise",
                "action": "Take more time to understand requirements before coding",
            })

        if metrics.study_streak_days < 3:
            improvement_areas.append({
                "area": "Study consistency",
                "current": f"{metrics.study_streak_days} day streak",
                "target": "7+ day streak",
                "action": "Schedule regular study time each day",
            })

        # Generate weekly goals
        weekly_goals = self._generate_weekly_goals(metrics)

        return {
            "improvement_areas": improvement_areas,
            "weekly_goals": weekly_goals,
            "focus_topics": metrics.weakest_topics[:3],
            "estimated_time_hours": sum(g.get("time_minutes", 30) for g in weekly_goals) / 60,
        }

    def _get_all_exercises(self) -> list[dict]:
        """Get all exercise data flattened."""
        exercises = []
        for module_data in self.progress.get("modules", {}).values():
            for ex_id, ex_data in module_data.get("exercises", {}).items():
                exercises.append({
                    "id": ex_id,
                    **ex_data,
                })
        return exercises

    def _get_all_sessions(self) -> list[dict]:
        """Load all session files."""
        sessions = []
        if self.sessions_path.exists():
            for session_file in self.sessions_path.glob("*.json"):
                try:
                    with open(session_file, 'r', encoding='utf-8') as f:
                        sessions.append(json.load(f))
                except (json.JSONDecodeError, IOError):
                    pass
        return sessions

    def _calculate_score_trend(self, exercises: list[dict]) -> str:
        """Calculate if scores are trending up or down."""
        if len(exercises) < 5:
            return "stable"

        # Get scores in chronological order
        dated_scores = [
            (e.get("updated_at", ""), e.get("score", 0))
            for e in exercises
            if e.get("score")
        ]
        dated_scores.sort(key=lambda x: x[0])
        scores = [s for _, s in dated_scores]

        if len(scores) < 5:
            return "stable"

        # Compare first half to second half
        mid = len(scores) // 2
        first_half_avg = sum(scores[:mid]) / mid
        second_half_avg = sum(scores[mid:]) / (len(scores) - mid)

        diff = second_half_avg - first_half_avg

        if diff > 5:
            return "improving"
        elif diff < -5:
            return "declining"
        return "stable"

    def _calculate_consistency(self, scores: list[float]) -> float:
        """Calculate score consistency (inverse of variance)."""
        if len(scores) < 2:
            return 1.0

        mean = sum(scores) / len(scores)
        variance = sum((s - mean) ** 2 for s in scores) / len(scores)
        std_dev = variance ** 0.5

        # Normalize: lower std_dev = higher consistency
        # 0 std_dev = 1.0 consistency, 50 std_dev = 0.0 consistency
        return max(0, 1 - (std_dev / 50))

    def _calculate_topic_scores(self, exercises: list[dict]) -> dict[str, float]:
        """Calculate average score per topic."""
        topic_scores: dict[str, list[float]] = {}

        for ex in exercises:
            # Extract topic from exercise ID (assumes format like ex01_topic)
            ex_id = ex.get("id", "")
            parts = ex_id.split("_")
            if len(parts) > 1:
                topic = "_".join(parts[1:])
                score = ex.get("score", 0)

                if topic not in topic_scores:
                    topic_scores[topic] = []
                topic_scores[topic].append(score)

        return {
            topic: sum(scores) / len(scores)
            for topic, scores in topic_scores.items()
            if scores
        }

    def _check_achievements(self, metrics: PerformanceMetrics) -> list[ProgressInsight]:
        """Check for achievements to celebrate."""
        achievements = []

        if metrics.study_streak_days >= 7:
            achievements.append(ProgressInsight(
                category="achievement",
                title="🔥 Week Streak!",
                description=f"You've studied for {metrics.study_streak_days} days in a row!",
                priority=2,
            ))

        if metrics.first_attempt_success_rate >= 0.8:
            achievements.append(ProgressInsight(
                category="achievement",
                title="🎯 Sharp Shooter",
                description="80%+ first-attempt success rate - excellent preparation!",
                priority=2,
            ))

        if metrics.total_exercises_completed >= 50:
            achievements.append(ProgressInsight(
                category="achievement",
                title="📚 Dedicated Learner",
                description=f"{metrics.total_exercises_completed} exercises completed!",
                priority=2,
            ))

        return achievements

    def _check_concerns(self, metrics: PerformanceMetrics) -> list[ProgressInsight]:
        """Check for concerning patterns."""
        concerns = []

        if metrics.score_trend == "declining":
            concerns.append(ProgressInsight(
                category="concern",
                title="📉 Score Trend",
                description="Your scores have been declining. Consider reviewing fundamentals.",
                priority=1,
                action="Review weakest topics",
            ))

        if metrics.average_attempts_per_exercise > 3:
            concerns.append(ProgressInsight(
                category="concern",
                title="🔄 Many Retries",
                description="Averaging 3+ attempts per exercise. Try reviewing concepts first.",
                priority=1,
                action="Read theory before exercises",
            ))

        return concerns

    def _generate_suggestions(self, metrics: PerformanceMetrics) -> list[ProgressInsight]:
        """Generate improvement suggestions."""
        suggestions = []

        if metrics.weakest_topics:
            suggestions.append(ProgressInsight(
                category="suggestion",
                title="📖 Focus Area",
                description=f"Consider focusing on: {', '.join(metrics.weakest_topics[:3])}",
                priority=2,
                action="Practice weak topics",
            ))

        if metrics.average_session_minutes < 20:
            suggestions.append(ProgressInsight(
                category="suggestion",
                title="⏰ Longer Sessions",
                description="Try 30-45 minute sessions for deeper learning",
                priority=3,
            ))

        return suggestions

    def _check_milestones(self, metrics: PerformanceMetrics) -> list[ProgressInsight]:
        """Check for upcoming or reached milestones."""
        milestones = []

        # Check exercise milestones
        exercise_milestones = [10, 25, 50, 100, 250]
        for milestone in exercise_milestones:
            if metrics.total_exercises_completed >= milestone:
                milestones.append(ProgressInsight(
                    category="milestone",
                    title=f"🏆 {milestone} Exercises",
                    description=f"Completed {milestone} exercises!",
                    priority=3,
                ))
                break

        return milestones

    def _generate_weekly_goals(self, metrics: PerformanceMetrics) -> list[dict]:
        """Generate weekly learning goals."""
        goals = []

        # Study time goal
        target_time = max(180, metrics.total_time_minutes // 4)  # 3 hours minimum
        goals.append({
            "goal": "Study time",
            "target": f"{target_time // 60} hours",
            "time_minutes": target_time,
        })

        # Exercise goal
        target_exercises = max(5, metrics.total_exercises_completed // 4)
        goals.append({
            "goal": "Complete exercises",
            "target": f"{target_exercises} exercises",
            "time_minutes": target_exercises * 20,
        })

        # Topic review goal
        if metrics.weakest_topics:
            goals.append({
                "goal": "Review weak topic",
                "target": metrics.weakest_topics[0],
                "time_minutes": 60,
            })

        return goals

    def _parse_date(self, date_str: str) -> datetime:
        """Parse a date string to datetime."""
        if not date_str:
            return datetime.min

        try:
            # Try ISO format
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except ValueError:
            try:
                # Try date only
                return datetime.strptime(date_str[:10], "%Y-%m-%d")
            except ValueError:
                return datetime.min
