"""
Dynamic Study Planner

Intelligent planning engine that:
- Creates study schedules based on available time and exam dates
- Reorganizes dynamically when circumstances change
- Prioritizes by exam weight and knowledge gaps
- Adapts to learning style and pace
"""

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from enum import Enum
from pathlib import Path
from typing import Optional
import json
import math

from .university_context import (
    UniversityConfig,
    SyllabusUnit,
    ExamInfo,
    TopicStatus,
    LearnerProfile,
    StudyPace,
)


class SessionType(Enum):
    """Types of study sessions."""
    LEARN_NEW = "learn_new"           # Learn new content
    REINFORCE = "reinforce"           # Practice and reinforce
    EXTEND = "extend"                 # Go deeper
    REVIEW_SRS = "review_srs"         # Spaced repetition review
    EXAM_PREP = "exam_prep"           # Exam preparation
    SIMULATE = "simulate"             # Exam simulation
    REST = "rest"                     # Suggested break


class PlanAdjustmentType(Enum):
    """Types of plan adjustments."""
    TIME_ADDED = "time_added"         # User has more time
    TIME_REDUCED = "time_reduced"     # User has less time
    TOPIC_ADDED = "topic_added"       # New topic in syllabus
    TOPIC_REMOVED = "topic_removed"   # Topic removed
    EXAM_DATE_CHANGED = "exam_date_changed"
    PROGRESS_FASTER = "progress_faster"   # Ahead of schedule
    PROGRESS_SLOWER = "progress_slower"   # Behind schedule
    TOPIC_DIFFICULTY = "topic_difficulty"  # Topic harder than expected


@dataclass
class StudySession:
    """A planned study session."""
    id: str
    date: date
    start_time: Optional[str] = None  # "18:00"
    duration_minutes: int = 60
    session_type: SessionType = SessionType.LEARN_NEW
    topic_id: Optional[str] = None
    topic_name: Optional[str] = None
    description: str = ""
    priority: int = 1  # 1 = highest
    is_completed: bool = False
    actual_duration: Optional[int] = None
    notes: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "start_time": self.start_time,
            "duration_minutes": self.duration_minutes,
            "session_type": self.session_type.value,
            "topic_id": self.topic_id,
            "topic_name": self.topic_name,
            "description": self.description,
            "priority": self.priority,
            "is_completed": self.is_completed,
            "actual_duration": self.actual_duration,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "StudySession":
        data = data.copy()
        data["date"] = date.fromisoformat(data["date"])
        data["session_type"] = SessionType(data["session_type"])
        return cls(**data)


@dataclass
class StudyPlan:
    """A complete study plan."""
    id: str
    created_at: datetime
    updated_at: datetime
    target_exam: Optional[ExamInfo] = None
    sessions: list[StudySession] = field(default_factory=list)
    total_hours_planned: float = 0.0
    hours_completed: float = 0.0

    # Plan metadata
    strategy: str = "balanced"  # balanced, intensive, exam_focused
    confidence_score: float = 0.0  # How confident we are the plan is achievable

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "target_exam": self.target_exam.to_dict() if self.target_exam else None,
            "sessions": [s.to_dict() for s in self.sessions],
            "total_hours_planned": self.total_hours_planned,
            "hours_completed": self.hours_completed,
            "strategy": self.strategy,
            "confidence_score": self.confidence_score,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "StudyPlan":
        return cls(
            id=data["id"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            target_exam=ExamInfo.from_dict(data["target_exam"]) if data.get("target_exam") else None,
            sessions=[StudySession.from_dict(s) for s in data.get("sessions", [])],
            total_hours_planned=data.get("total_hours_planned", 0),
            hours_completed=data.get("hours_completed", 0),
            strategy=data.get("strategy", "balanced"),
            confidence_score=data.get("confidence_score", 0),
        )

    def get_sessions_for_date(self, target_date: date) -> list[StudySession]:
        """Get all sessions for a specific date."""
        return [s for s in self.sessions if s.date == target_date]

    def get_upcoming_sessions(self, days: int = 7) -> list[StudySession]:
        """Get sessions for the next N days."""
        today = date.today()
        end_date = today + timedelta(days=days)
        return [
            s for s in self.sessions
            if today <= s.date <= end_date and not s.is_completed
        ]

    @property
    def progress_percentage(self) -> float:
        """Calculate overall plan progress."""
        if self.total_hours_planned == 0:
            return 0.0
        return min(100.0, (self.hours_completed / self.total_hours_planned) * 100)


@dataclass
class DailyPlan:
    """Summary of what to do today."""
    date: date
    sessions: list[StudySession]
    total_minutes: int
    has_exam_urgency: bool
    srs_items_due: int
    main_focus: str
    motivational_message: str

    def to_dict(self) -> dict:
        return {
            "date": self.date.isoformat(),
            "sessions": [s.to_dict() for s in self.sessions],
            "total_minutes": self.total_minutes,
            "has_exam_urgency": self.has_exam_urgency,
            "srs_items_due": self.srs_items_due,
            "main_focus": self.main_focus,
            "motivational_message": self.motivational_message,
        }


class StudyPlanner:
    """
    Intelligent study planner.

    Creates and manages study plans that:
    - Adapt to available time and exam dates
    - Prioritize by importance and knowledge gaps
    - Reorganize automatically when needed
    - Consider learning style preferences
    """

    def __init__(
        self,
        config: UniversityConfig,
        topic_status: dict[str, TopicStatus],
        tutor_path: Path,
    ):
        self.config = config
        self.topic_status = topic_status
        self.tutor_path = tutor_path
        self.plan_file = tutor_path / "study_plan.json"

        self._current_plan: Optional[StudyPlan] = None
        self._load_plan()

    def _load_plan(self) -> None:
        """Load existing plan if available."""
        if self.plan_file.exists():
            with open(self.plan_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._current_plan = StudyPlan.from_dict(data)

    def _save_plan(self) -> None:
        """Save current plan."""
        if self._current_plan:
            self._current_plan.updated_at = datetime.now()
            self.tutor_path.mkdir(parents=True, exist_ok=True)
            with open(self.plan_file, 'w', encoding='utf-8') as f:
                json.dump(self._current_plan.to_dict(), f, indent=2, ensure_ascii=False)

    @property
    def current_plan(self) -> Optional[StudyPlan]:
        return self._current_plan

    def generate_plan(
        self,
        target_exam: Optional[ExamInfo] = None,
        hours_per_week: Optional[float] = None,
        strategy: str = "balanced",
    ) -> StudyPlan:
        """
        Generate a new study plan.

        Args:
            target_exam: Exam to prepare for (or next exam if None)
            hours_per_week: Available study hours (or from profile)
            strategy: Planning strategy (balanced, intensive, exam_focused)

        Returns:
            Generated study plan
        """
        # Use defaults from config
        if target_exam is None:
            target_exam = self.config.next_exam

        if hours_per_week is None:
            hours_per_week = self.config.learner_profile.hours_per_week

        # Calculate available time
        if target_exam:
            days_available = max(1, target_exam.days_until)
            total_hours_available = (days_available / 7) * hours_per_week
        else:
            days_available = 90  # Default 3 months
            total_hours_available = (days_available / 7) * hours_per_week

        # Get topics to cover
        topics_to_cover = self._get_topics_to_cover()

        # Calculate total hours needed
        total_hours_needed = sum(t.estimated_hours for t in topics_to_cover)

        # Determine strategy based on time constraint
        if total_hours_needed > total_hours_available * 1.5:
            strategy = "intensive"
        elif total_hours_needed > total_hours_available:
            strategy = "exam_focused"

        # Generate sessions
        sessions = self._generate_sessions(
            topics=topics_to_cover,
            days_available=days_available,
            hours_per_week=hours_per_week,
            strategy=strategy,
            exam=target_exam,
        )

        # Calculate confidence score
        confidence = self._calculate_confidence(
            total_hours_needed,
            total_hours_available,
            strategy,
        )

        # Create plan
        plan = StudyPlan(
            id=f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            target_exam=target_exam,
            sessions=sessions,
            total_hours_planned=sum(s.duration_minutes for s in sessions) / 60,
            strategy=strategy,
            confidence_score=confidence,
        )

        self._current_plan = plan
        self._save_plan()

        return plan

    def _get_topics_to_cover(self) -> list[SyllabusUnit]:
        """Get topics that need to be covered."""
        topics = []
        for unit in self.config.syllabus_units:
            status = self.topic_status.get(unit.id, TopicStatus.NEW)
            if status in [TopicStatus.NEW, TopicStatus.IN_PROGRESS, TopicStatus.RUSTY]:
                topics.append(unit)
        return topics

    def _generate_sessions(
        self,
        topics: list[SyllabusUnit],
        days_available: int,
        hours_per_week: float,
        strategy: str,
        exam: Optional[ExamInfo],
    ) -> list[StudySession]:
        """Generate study sessions."""
        sessions = []

        # Calculate daily hours
        study_days = self.config.learner_profile.study_days
        study_days_per_week = len(study_days)
        hours_per_day = hours_per_week / study_days_per_week
        session_duration = self.config.learner_profile.preferred_session_minutes

        # Sort topics by priority
        sorted_topics = self._prioritize_topics(topics, exam)

        # Generate dates
        today = date.today()
        day_map = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6}
        study_day_nums = [day_map[d] for d in study_days]

        session_id = 0
        current_topic_idx = 0
        topic_hours_remaining = {}

        for topic in sorted_topics:
            topic_hours_remaining[topic.id] = topic.estimated_hours

        for day_offset in range(days_available):
            current_date = today + timedelta(days=day_offset)
            weekday = current_date.weekday()

            if weekday not in study_day_nums:
                continue

            # Plan sessions for this day
            daily_minutes = int(hours_per_day * 60)
            minutes_planned = 0

            while minutes_planned < daily_minutes and current_topic_idx < len(sorted_topics):
                topic = sorted_topics[current_topic_idx]

                # Calculate session duration
                remaining_topic_minutes = topic_hours_remaining[topic.id] * 60
                available_minutes = min(
                    session_duration,
                    daily_minutes - minutes_planned,
                    remaining_topic_minutes
                )

                if available_minutes < 15:  # Skip tiny sessions
                    current_topic_idx += 1
                    continue

                # Determine session type
                status = self.topic_status.get(topic.id, TopicStatus.NEW)
                if status == TopicStatus.NEW:
                    session_type = SessionType.LEARN_NEW
                elif status == TopicStatus.RUSTY:
                    session_type = SessionType.REVIEW_SRS
                elif status == TopicStatus.LEARNED:
                    session_type = SessionType.REINFORCE
                else:
                    session_type = SessionType.LEARN_NEW

                sessions.append(StudySession(
                    id=f"session_{session_id}",
                    date=current_date,
                    start_time=self.config.learner_profile.preferred_time,
                    duration_minutes=int(available_minutes),
                    session_type=session_type,
                    topic_id=topic.id,
                    topic_name=topic.name,
                    description=f"{session_type.value.replace('_', ' ').title()}: {topic.name}",
                    priority=current_topic_idx + 1,
                ))

                session_id += 1
                minutes_planned += available_minutes
                topic_hours_remaining[topic.id] -= available_minutes / 60

                if topic_hours_remaining[topic.id] <= 0:
                    current_topic_idx += 1

        # Add exam simulation sessions if there's an exam
        if exam and exam.days_until > 3:
            # Add simulation 3 days before, 1 week before, and 2 weeks before
            simulation_offsets = [3, 7, 14]
            for offset in simulation_offsets:
                if exam.days_until >= offset:
                    sim_date = exam.date - timedelta(days=offset)
                    sessions.append(StudySession(
                        id=f"session_sim_{offset}",
                        date=sim_date,
                        duration_minutes=exam.duration_minutes,
                        session_type=SessionType.SIMULATE,
                        description=f"Exam Simulation #{simulation_offsets.index(offset) + 1}",
                        priority=0,  # High priority
                    ))

        # Sort by date
        sessions.sort(key=lambda s: (s.date, s.priority))

        return sessions

    def _prioritize_topics(
        self,
        topics: list[SyllabusUnit],
        exam: Optional[ExamInfo],
    ) -> list[SyllabusUnit]:
        """Prioritize topics based on multiple factors."""

        def calculate_priority(topic: SyllabusUnit) -> float:
            priority = 0.0

            # Weight factor (higher weight = higher priority)
            priority += topic.weight * 2

            # Status factor
            status = self.topic_status.get(topic.id, TopicStatus.NEW)
            status_priority = {
                TopicStatus.RUSTY: 50,      # High priority - needs review
                TopicStatus.IN_PROGRESS: 40,  # Continue what's started
                TopicStatus.NEW: 30,
                TopicStatus.LEARNED: 10,
                TopicStatus.MASTERED: 0,
            }
            priority += status_priority.get(status, 0)

            # Order factor (earlier topics first, but less important)
            priority -= topic.order * 0.5

            # Exam inclusion factor
            if exam and topic.id in exam.topics_included:
                priority += 30

            return priority

        return sorted(topics, key=calculate_priority, reverse=True)

    def _calculate_confidence(
        self,
        hours_needed: float,
        hours_available: float,
        strategy: str,
    ) -> float:
        """Calculate confidence score for the plan."""
        if hours_available == 0:
            return 0.0

        ratio = hours_available / hours_needed

        if ratio >= 1.5:
            return 95.0  # Plenty of time
        elif ratio >= 1.2:
            return 85.0  # Comfortable
        elif ratio >= 1.0:
            return 70.0  # Tight but doable
        elif ratio >= 0.8:
            return 50.0  # Need to prioritize
        elif ratio >= 0.6:
            return 30.0  # Very tight
        else:
            return 10.0  # Emergency mode

    def get_today_plan(self, srs_items_due: int = 0) -> DailyPlan:
        """
        Get the plan for today.

        Args:
            srs_items_due: Number of SRS items due for review

        Returns:
            DailyPlan with today's sessions and recommendations
        """
        today = date.today()
        sessions = []

        if self._current_plan:
            sessions = self._current_plan.get_sessions_for_date(today)

        # Check exam urgency
        has_urgency = False
        if self.config.next_exam:
            has_urgency = self.config.next_exam.is_urgent

        # Determine main focus
        if srs_items_due > 0:
            main_focus = f"Start with {srs_items_due} review items, then continue with planned sessions"
        elif sessions:
            first_session = sessions[0]
            main_focus = first_session.description
        else:
            main_focus = "No sessions planned for today - consider a quick review"

        # Generate motivational message
        if has_urgency:
            days = self.config.next_exam.days_until
            message = f"Exam in {days} days! Stay focused and you've got this!"
        elif sessions:
            message = "Let's make progress today. Every session counts!"
        else:
            message = "Rest day? Consider a quick review to maintain momentum."

        return DailyPlan(
            date=today,
            sessions=sessions,
            total_minutes=sum(s.duration_minutes for s in sessions),
            has_exam_urgency=has_urgency,
            srs_items_due=srs_items_due,
            main_focus=main_focus,
            motivational_message=message,
        )

    def adjust_plan(
        self,
        adjustment_type: PlanAdjustmentType,
        **kwargs,
    ) -> StudyPlan:
        """
        Adjust the current plan based on changes.

        Args:
            adjustment_type: Type of adjustment needed
            **kwargs: Additional parameters for the adjustment

        Returns:
            Adjusted study plan
        """
        if not self._current_plan:
            return self.generate_plan()

        if adjustment_type == PlanAdjustmentType.TIME_REDUCED:
            return self._handle_time_reduced(kwargs.get("new_hours_per_week", 4))

        elif adjustment_type == PlanAdjustmentType.TIME_ADDED:
            return self._handle_time_added(kwargs.get("new_hours_per_week", 12))

        elif adjustment_type == PlanAdjustmentType.TOPIC_ADDED:
            return self._handle_topic_added(kwargs.get("topic"))

        elif adjustment_type == PlanAdjustmentType.EXAM_DATE_CHANGED:
            return self._handle_exam_date_changed(kwargs.get("new_date"))

        elif adjustment_type == PlanAdjustmentType.PROGRESS_SLOWER:
            return self._handle_progress_slower()

        elif adjustment_type == PlanAdjustmentType.PROGRESS_FASTER:
            return self._handle_progress_faster()

        return self._current_plan

    def _handle_time_reduced(self, new_hours: float) -> StudyPlan:
        """Handle reduction in available time."""
        # Regenerate with new hours and prioritized topics
        return self.generate_plan(
            hours_per_week=new_hours,
            strategy="exam_focused",
        )

    def _handle_time_added(self, new_hours: float) -> StudyPlan:
        """Handle increase in available time."""
        return self.generate_plan(
            hours_per_week=new_hours,
            strategy="balanced",
        )

    def _handle_topic_added(self, topic: SyllabusUnit) -> StudyPlan:
        """Handle addition of a new topic."""
        # Add topic and regenerate
        return self.generate_plan()

    def _handle_exam_date_changed(self, new_date: date) -> StudyPlan:
        """Handle exam date change."""
        if self.config.next_exam:
            self.config.exams[0].date = new_date
        return self.generate_plan()

    def _handle_progress_slower(self) -> StudyPlan:
        """Handle slower than expected progress."""
        # Increase intensity
        return self.generate_plan(strategy="intensive")

    def _handle_progress_faster(self) -> StudyPlan:
        """Handle faster than expected progress."""
        # Can add more depth or extension
        return self.generate_plan(strategy="balanced")

    def mark_session_complete(
        self,
        session_id: str,
        actual_duration: int,
        notes: Optional[str] = None,
    ) -> bool:
        """Mark a session as completed."""
        if not self._current_plan:
            return False

        for session in self._current_plan.sessions:
            if session.id == session_id:
                session.is_completed = True
                session.actual_duration = actual_duration
                session.notes = notes
                self._current_plan.hours_completed += actual_duration / 60
                self._save_plan()
                return True

        return False

    def get_week_overview(self) -> dict:
        """Get an overview of the upcoming week."""
        if not self._current_plan:
            return {"error": "No plan available"}

        today = date.today()
        sessions = self._current_plan.get_upcoming_sessions(7)

        # Group by day
        by_day = {}
        for i in range(7):
            day = today + timedelta(days=i)
            day_sessions = [s for s in sessions if s.date == day]
            by_day[day.isoformat()] = {
                "date": day.strftime("%A, %B %d"),
                "sessions": [s.to_dict() for s in day_sessions],
                "total_minutes": sum(s.duration_minutes for s in day_sessions),
            }

        return {
            "week_start": today.isoformat(),
            "total_sessions": len(sessions),
            "total_hours": sum(s.duration_minutes for s in sessions) / 60,
            "by_day": by_day,
            "exam_days_remaining": self.config.next_exam.days_until if self.config.next_exam else None,
        }
