"""
Exam Preparation Module

Handles exam-specific preparation including:
- Exam simulations
- Performance analysis by topic
- Time management strategies
- Adaptive preparation based on time remaining
"""

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from enum import Enum
from pathlib import Path
from typing import Optional
import json
import random


class ExamPrepMode(Enum):
    """Exam preparation modes based on time available."""
    FULL = "full"                 # > 2 weeks
    STANDARD = "standard"         # 1-2 weeks
    INTENSIVE = "intensive"       # 3-7 days
    EMERGENCY = "emergency"       # 1-2 days
    LAST_MINUTE = "last_minute"   # Hours


class QuestionType(Enum):
    """Types of exam questions."""
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    LONG_ANSWER = "long_answer"
    CODING = "coding"
    PROBLEM_SOLVING = "problem_solving"
    FILL_BLANK = "fill_blank"
    MATCHING = "matching"


@dataclass
class ExamQuestion:
    """A question in an exam simulation."""
    id: str
    topic_id: str
    topic_name: str
    question_type: QuestionType
    question_text: str
    points: float = 1.0
    estimated_minutes: int = 2
    difficulty: int = 2  # 1-5

    # After answering
    student_answer: Optional[str] = None
    is_correct: Optional[bool] = None
    score_earned: float = 0.0
    time_spent_seconds: Optional[int] = None
    feedback: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "topic_id": self.topic_id,
            "topic_name": self.topic_name,
            "question_type": self.question_type.value,
            "question_text": self.question_text,
            "points": self.points,
            "estimated_minutes": self.estimated_minutes,
            "difficulty": self.difficulty,
            "student_answer": self.student_answer,
            "is_correct": self.is_correct,
            "score_earned": self.score_earned,
            "time_spent_seconds": self.time_spent_seconds,
            "feedback": self.feedback,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ExamQuestion":
        data = data.copy()
        data["question_type"] = QuestionType(data["question_type"])
        return cls(**data)


@dataclass
class ExamSimulation:
    """An exam simulation session."""
    id: str
    name: str
    created_at: datetime
    duration_minutes: int
    questions: list[ExamQuestion] = field(default_factory=list)

    # Status
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    is_completed: bool = False

    # Results
    total_points: float = 0.0
    points_earned: float = 0.0
    percentage_score: float = 0.0
    time_used_minutes: int = 0

    # Analysis
    topics_performance: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "duration_minutes": self.duration_minutes,
            "questions": [q.to_dict() for q in self.questions],
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "is_completed": self.is_completed,
            "total_points": self.total_points,
            "points_earned": self.points_earned,
            "percentage_score": self.percentage_score,
            "time_used_minutes": self.time_used_minutes,
            "topics_performance": self.topics_performance,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ExamSimulation":
        sim = cls(
            id=data["id"],
            name=data["name"],
            created_at=datetime.fromisoformat(data["created_at"]),
            duration_minutes=data["duration_minutes"],
            questions=[ExamQuestion.from_dict(q) for q in data.get("questions", [])],
            is_completed=data.get("is_completed", False),
            total_points=data.get("total_points", 0),
            points_earned=data.get("points_earned", 0),
            percentage_score=data.get("percentage_score", 0),
            time_used_minutes=data.get("time_used_minutes", 0),
            topics_performance=data.get("topics_performance", {}),
        )
        if data.get("started_at"):
            sim.started_at = datetime.fromisoformat(data["started_at"])
        if data.get("completed_at"):
            sim.completed_at = datetime.fromisoformat(data["completed_at"])
        return sim

    @property
    def time_remaining_minutes(self) -> int:
        """Get remaining time if simulation is active."""
        if not self.started_at or self.is_completed:
            return self.duration_minutes

        elapsed = (datetime.now() - self.started_at).total_seconds() / 60
        return max(0, int(self.duration_minutes - elapsed))


@dataclass
class TopicAnalysis:
    """Analysis of performance on a specific topic."""
    topic_id: str
    topic_name: str
    questions_count: int
    correct_count: int
    total_points: float
    points_earned: float
    average_time_seconds: float
    percentage: float
    trend: str  # improving, stable, declining
    weakness_areas: list[str] = field(default_factory=list)
    strength_areas: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "topic_id": self.topic_id,
            "topic_name": self.topic_name,
            "questions_count": self.questions_count,
            "correct_count": self.correct_count,
            "total_points": self.total_points,
            "points_earned": self.points_earned,
            "average_time_seconds": self.average_time_seconds,
            "percentage": self.percentage,
            "trend": self.trend,
            "weakness_areas": self.weakness_areas,
            "strength_areas": self.strength_areas,
        }


@dataclass
class ExamPrepPlan:
    """A preparation plan for an exam."""
    exam_date: date
    days_remaining: int
    mode: ExamPrepMode
    daily_plan: list[dict]
    focus_topics: list[str]
    simulations_planned: int
    estimated_readiness: float  # 0-100

    def to_dict(self) -> dict:
        return {
            "exam_date": self.exam_date.isoformat(),
            "days_remaining": self.days_remaining,
            "mode": self.mode.value,
            "daily_plan": self.daily_plan,
            "focus_topics": self.focus_topics,
            "simulations_planned": self.simulations_planned,
            "estimated_readiness": self.estimated_readiness,
        }


class ExamPreparationEngine:
    """
    Engine for exam preparation.

    Provides:
    - Adaptive preparation strategies
    - Exam simulations
    - Performance analysis
    - Weakness identification
    """

    def __init__(self, tutor_path: Path):
        self.tutor_path = tutor_path
        self.simulations_file = tutor_path / "exam_simulations.json"
        self.history_file = tutor_path / "exam_history.json"

        self._simulations: list[ExamSimulation] = []
        self._history: list[dict] = []
        self._load()

    def _load(self) -> None:
        """Load simulations and history."""
        if self.simulations_file.exists():
            with open(self.simulations_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._simulations = [ExamSimulation.from_dict(s) for s in data]

        if self.history_file.exists():
            with open(self.history_file, 'r', encoding='utf-8') as f:
                self._history = json.load(f)

    def _save(self) -> None:
        """Save simulations and history."""
        self.tutor_path.mkdir(parents=True, exist_ok=True)

        with open(self.simulations_file, 'w', encoding='utf-8') as f:
            json.dump([s.to_dict() for s in self._simulations], f, indent=2, ensure_ascii=False)

        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self._history, f, indent=2, ensure_ascii=False)

    def get_prep_mode(self, days_until_exam: int) -> ExamPrepMode:
        """Determine preparation mode based on time available."""
        if days_until_exam > 14:
            return ExamPrepMode.FULL
        elif days_until_exam > 7:
            return ExamPrepMode.STANDARD
        elif days_until_exam > 2:
            return ExamPrepMode.INTENSIVE
        elif days_until_exam > 0:
            return ExamPrepMode.EMERGENCY
        else:
            return ExamPrepMode.LAST_MINUTE

    def create_prep_plan(
        self,
        exam_date: date,
        topics: list[dict],
        topic_mastery: dict[str, float],
        hours_per_day: float = 2.0,
    ) -> ExamPrepPlan:
        """
        Create an exam preparation plan.

        Args:
            exam_date: Date of the exam
            topics: List of topics with weights
            topic_mastery: Current mastery level per topic (0-100)
            hours_per_day: Available study hours per day

        Returns:
            ExamPrepPlan with daily activities
        """
        days_remaining = (exam_date - date.today()).days
        mode = self.get_prep_mode(days_remaining)

        # Identify focus topics (lowest mastery, highest weight)
        focus_topics = self._identify_focus_topics(topics, topic_mastery)

        # Generate daily plan
        daily_plan = self._generate_daily_plan(
            days_remaining=days_remaining,
            mode=mode,
            focus_topics=focus_topics,
            hours_per_day=hours_per_day,
        )

        # Calculate readiness estimate
        avg_mastery = sum(topic_mastery.values()) / len(topic_mastery) if topic_mastery else 0
        readiness = min(100, avg_mastery * 1.1)  # Slight boost for preparation

        # Determine simulations
        if mode == ExamPrepMode.FULL:
            simulations = min(4, days_remaining // 4)
        elif mode == ExamPrepMode.STANDARD:
            simulations = min(3, days_remaining // 3)
        elif mode == ExamPrepMode.INTENSIVE:
            simulations = min(2, days_remaining // 2)
        else:
            simulations = 1

        return ExamPrepPlan(
            exam_date=exam_date,
            days_remaining=days_remaining,
            mode=mode,
            daily_plan=daily_plan,
            focus_topics=focus_topics,
            simulations_planned=simulations,
            estimated_readiness=readiness,
        )

    def _identify_focus_topics(
        self,
        topics: list[dict],
        topic_mastery: dict[str, float],
    ) -> list[str]:
        """Identify topics that need the most attention."""
        scored_topics = []

        for topic in topics:
            topic_id = topic.get("id", topic.get("name", ""))
            weight = topic.get("weight", 10)
            mastery = topic_mastery.get(topic_id, 0)

            # Priority = high weight + low mastery
            priority = (weight / 100) * (100 - mastery)
            scored_topics.append((topic_id, priority))

        scored_topics.sort(key=lambda x: x[1], reverse=True)
        return [t[0] for t in scored_topics[:5]]

    def _generate_daily_plan(
        self,
        days_remaining: int,
        mode: ExamPrepMode,
        focus_topics: list[str],
        hours_per_day: float,
    ) -> list[dict]:
        """Generate a daily plan for exam preparation."""
        daily_plan = []

        for day in range(min(days_remaining, 14)):  # Max 2 weeks plan
            day_date = date.today() + timedelta(days=day)

            if mode == ExamPrepMode.EMERGENCY or days_remaining - day <= 2:
                # Last days: only review and simulation
                activities = [
                    {"type": "review", "duration": 30, "description": "Quick review of key concepts"},
                    {"type": "flashcards", "duration": 20, "description": "Flashcard review"},
                ]
                if day == days_remaining - 1:
                    activities.append({
                        "type": "rest",
                        "duration": 0,
                        "description": "Light review only - rest before exam"
                    })
            elif mode == ExamPrepMode.INTENSIVE:
                # Intensive: heavy practice
                minutes = int(hours_per_day * 60)
                activities = [
                    {"type": "review_srs", "duration": 15, "description": "SRS review"},
                    {"type": "practice", "duration": minutes - 45, "description": f"Practice weak topics: {', '.join(focus_topics[:2])}"},
                    {"type": "simulation", "duration": 30, "description": "Mini exam simulation"},
                ]
            else:
                # Standard/Full: balanced approach
                minutes = int(hours_per_day * 60)
                activities = [
                    {"type": "review_srs", "duration": 10, "description": "SRS review"},
                    {"type": "learn", "duration": minutes // 3, "description": "Learn or deepen topic"},
                    {"type": "practice", "duration": minutes // 3, "description": "Practice exercises"},
                    {"type": "review", "duration": minutes // 3, "description": "Review and consolidate"},
                ]

            daily_plan.append({
                "date": day_date.isoformat(),
                "day_number": day + 1,
                "activities": activities,
                "total_minutes": sum(a["duration"] for a in activities),
            })

        return daily_plan

    def create_simulation(
        self,
        name: str,
        duration_minutes: int,
        topics: list[dict],
        question_distribution: Optional[dict] = None,
    ) -> ExamSimulation:
        """
        Create a new exam simulation.

        Args:
            name: Name of the simulation
            duration_minutes: Duration in minutes
            topics: Topics to include
            question_distribution: Optional distribution of question types

        Returns:
            Created ExamSimulation
        """
        # Default distribution
        if not question_distribution:
            question_distribution = {
                QuestionType.MULTIPLE_CHOICE: 0.4,
                QuestionType.SHORT_ANSWER: 0.3,
                QuestionType.PROBLEM_SOLVING: 0.2,
                QuestionType.TRUE_FALSE: 0.1,
            }

        # Calculate number of questions based on time
        # Assume average 3 minutes per question
        num_questions = duration_minutes // 3

        questions = []
        total_points = 0

        for i in range(num_questions):
            # Select random topic weighted by exam weight
            topic = random.choices(
                topics,
                weights=[t.get("weight", 10) for t in topics]
            )[0]

            # Select question type
            q_type = random.choices(
                list(question_distribution.keys()),
                weights=list(question_distribution.values())
            )[0]

            # Determine points and time
            points = 1.0 if q_type == QuestionType.MULTIPLE_CHOICE else 2.0
            est_minutes = 2 if q_type == QuestionType.MULTIPLE_CHOICE else 4

            questions.append(ExamQuestion(
                id=f"q_{i+1}",
                topic_id=topic.get("id", str(i)),
                topic_name=topic.get("name", f"Topic {i}"),
                question_type=q_type,
                question_text=f"[Question about {topic.get('name', 'topic')}]",
                points=points,
                estimated_minutes=est_minutes,
                difficulty=random.randint(1, 5),
            ))
            total_points += points

        simulation = ExamSimulation(
            id=f"sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            name=name,
            created_at=datetime.now(),
            duration_minutes=duration_minutes,
            questions=questions,
            total_points=total_points,
        )

        self._simulations.append(simulation)
        self._save()

        return simulation

    def start_simulation(self, simulation_id: str) -> Optional[ExamSimulation]:
        """Start a simulation."""
        for sim in self._simulations:
            if sim.id == simulation_id:
                sim.started_at = datetime.now()
                self._save()
                return sim
        return None

    def submit_answer(
        self,
        simulation_id: str,
        question_id: str,
        answer: str,
        is_correct: bool,
        score: float,
        time_seconds: int,
        feedback: str = "",
    ) -> bool:
        """Submit an answer for a question."""
        for sim in self._simulations:
            if sim.id == simulation_id:
                for q in sim.questions:
                    if q.id == question_id:
                        q.student_answer = answer
                        q.is_correct = is_correct
                        q.score_earned = score
                        q.time_spent_seconds = time_seconds
                        q.feedback = feedback
                        self._save()
                        return True
        return False

    def complete_simulation(self, simulation_id: str) -> Optional[dict]:
        """
        Complete a simulation and calculate results.

        Returns:
            Results summary
        """
        for sim in self._simulations:
            if sim.id == simulation_id:
                sim.completed_at = datetime.now()
                sim.is_completed = True

                # Calculate scores
                sim.points_earned = sum(q.score_earned for q in sim.questions)
                if sim.total_points > 0:
                    sim.percentage_score = (sim.points_earned / sim.total_points) * 100

                # Calculate time used
                if sim.started_at:
                    sim.time_used_minutes = int(
                        (sim.completed_at - sim.started_at).total_seconds() / 60
                    )

                # Analyze by topic
                sim.topics_performance = self._analyze_topics(sim.questions)

                # Add to history
                self._history.append({
                    "simulation_id": sim.id,
                    "date": sim.completed_at.isoformat(),
                    "score": sim.percentage_score,
                    "topics_performance": sim.topics_performance,
                })

                self._save()

                return self._generate_results_summary(sim)

        return None

    def _analyze_topics(self, questions: list[ExamQuestion]) -> dict:
        """Analyze performance by topic."""
        by_topic = {}

        for q in questions:
            if q.topic_id not in by_topic:
                by_topic[q.topic_id] = {
                    "name": q.topic_name,
                    "total": 0,
                    "correct": 0,
                    "points_total": 0,
                    "points_earned": 0,
                    "time_total": 0,
                }

            by_topic[q.topic_id]["total"] += 1
            by_topic[q.topic_id]["points_total"] += q.points
            by_topic[q.topic_id]["points_earned"] += q.score_earned
            if q.is_correct:
                by_topic[q.topic_id]["correct"] += 1
            if q.time_spent_seconds:
                by_topic[q.topic_id]["time_total"] += q.time_spent_seconds

        # Calculate percentages
        for topic_id, data in by_topic.items():
            if data["points_total"] > 0:
                data["percentage"] = (data["points_earned"] / data["points_total"]) * 100
            else:
                data["percentage"] = 0

            if data["total"] > 0:
                data["avg_time_seconds"] = data["time_total"] / data["total"]
            else:
                data["avg_time_seconds"] = 0

        return by_topic

    def _generate_results_summary(self, sim: ExamSimulation) -> dict:
        """Generate a results summary for a completed simulation."""
        # Identify strengths and weaknesses
        topics = list(sim.topics_performance.items())
        sorted_topics = sorted(topics, key=lambda x: x[1]["percentage"])

        weakest = sorted_topics[:3] if len(sorted_topics) >= 3 else sorted_topics
        strongest = sorted_topics[-3:] if len(sorted_topics) >= 3 else sorted_topics

        # Determine pass/fail (assuming 60% pass)
        passed = sim.percentage_score >= 60

        # Calculate grade
        if sim.percentage_score >= 90:
            grade = "A"
        elif sim.percentage_score >= 80:
            grade = "B"
        elif sim.percentage_score >= 70:
            grade = "C"
        elif sim.percentage_score >= 60:
            grade = "D"
        else:
            grade = "F"

        return {
            "simulation_id": sim.id,
            "name": sim.name,
            "score": round(sim.percentage_score, 1),
            "grade": grade,
            "passed": passed,
            "points": f"{sim.points_earned}/{sim.total_points}",
            "time_used": f"{sim.time_used_minutes}/{sim.duration_minutes} min",
            "questions_correct": sum(1 for q in sim.questions if q.is_correct),
            "questions_total": len(sim.questions),
            "weakest_topics": [
                {"topic": t[0], "name": t[1]["name"], "score": round(t[1]["percentage"], 1)}
                for t in weakest
            ],
            "strongest_topics": [
                {"topic": t[0], "name": t[1]["name"], "score": round(t[1]["percentage"], 1)}
                for t in reversed(strongest)
            ],
            "recommendations": self._generate_recommendations(sim),
        }

    def _generate_recommendations(self, sim: ExamSimulation) -> list[str]:
        """Generate recommendations based on simulation results."""
        recommendations = []

        # Score-based recommendations
        if sim.percentage_score < 50:
            recommendations.append("Focus on fundamental concepts before attempting more simulations")
        elif sim.percentage_score < 70:
            recommendations.append("Review weak topics identified and practice more exercises")
        elif sim.percentage_score < 85:
            recommendations.append("Good progress! Focus on edge cases and advanced concepts")
        else:
            recommendations.append("Excellent! Maintain your knowledge with regular review")

        # Time-based recommendations
        if sim.time_used_minutes > sim.duration_minutes * 0.9:
            recommendations.append("Practice time management - you used most of the available time")

        # Topic-based recommendations
        weak_topics = [
            t for t, data in sim.topics_performance.items()
            if data["percentage"] < 60
        ]
        if weak_topics:
            recommendations.append(f"Priority review needed for: {', '.join(weak_topics[:3])}")

        return recommendations

    def get_simulation_history(self) -> list[dict]:
        """Get history of all simulations."""
        return sorted(self._history, key=lambda x: x["date"], reverse=True)

    def get_progress_trend(self) -> dict:
        """Analyze progress trend across simulations."""
        if len(self._history) < 2:
            return {"trend": "insufficient_data", "message": "Need at least 2 simulations for trend analysis"}

        scores = [h["score"] for h in self._history]

        # Simple linear trend
        recent_avg = sum(scores[-3:]) / min(3, len(scores[-3:]))
        older_avg = sum(scores[:-3]) / max(1, len(scores[:-3])) if len(scores) > 3 else scores[0]

        if recent_avg > older_avg + 5:
            trend = "improving"
            message = f"Your scores are improving! Recent average: {recent_avg:.1f}%"
        elif recent_avg < older_avg - 5:
            trend = "declining"
            message = f"Scores declining. Recent average: {recent_avg:.1f}%. Review your study strategy."
        else:
            trend = "stable"
            message = f"Scores stable around {recent_avg:.1f}%"

        return {
            "trend": trend,
            "message": message,
            "recent_average": recent_avg,
            "overall_average": sum(scores) / len(scores),
            "best_score": max(scores),
            "total_simulations": len(scores),
        }
