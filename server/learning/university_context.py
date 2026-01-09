"""
University Context Module

Handles university-specific learning contexts including:
- Subjects with exams
- Syllabus management
- Academic schedules
- Different learning contexts (university, research, certification, etc.)
"""

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from enum import Enum
from pathlib import Path
from typing import Optional
import json


class LearningContext(Enum):
    """Types of learning contexts supported."""
    UNIVERSITY = "university"
    RESEARCH = "research"
    CERTIFICATION = "certification"
    COURSE_ONLINE = "course_online"
    SELF_TAUGHT = "self_taught"
    PROFESSIONAL = "professional"
    LANGUAGE = "language"
    EXAM_PREP = "exam_prep"  # Oposiciones, selectividad


class LearningStyle(Enum):
    """Learning style preferences."""
    VISUAL = "visual"
    PRACTICAL = "practical"
    THEORETICAL = "theoretical"
    MIXED = "mixed"
    AUTO_DETECT = "auto_detect"


class StudyPace(Enum):
    """Study intensity levels."""
    CASUAL = "casual"          # 3-5 h/week
    REGULAR = "regular"        # 6-10 h/week
    INTENSIVE = "intensive"    # 10+ h/week
    EMERGENCY = "emergency"    # As much as possible


class TopicStatus(Enum):
    """Status of a topic in the learning journey."""
    NEW = "new"                    # Never seen
    IN_PROGRESS = "in_progress"   # Currently learning
    LEARNED = "learned"           # Completed first pass
    REINFORCING = "reinforcing"   # Reviewing/practicing
    MASTERED = "mastered"         # High confidence
    RUSTY = "rusty"               # Needs review (SRS flagged)
    EXTENDING = "extending"       # Going deeper


@dataclass
class Subject:
    """Represents a university subject or course."""
    name: str
    code: Optional[str] = None
    professor: Optional[str] = None
    semester: Optional[str] = None
    credits: Optional[int] = None
    description: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "code": self.code,
            "professor": self.professor,
            "semester": self.semester,
            "credits": self.credits,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Subject":
        return cls(**data)


@dataclass
class ExamInfo:
    """Information about an exam."""
    date: date
    name: str = "Examen"
    type: str = "final"  # final, partial, quiz
    weight: float = 100.0  # Percentage of final grade
    duration_minutes: int = 120
    location: Optional[str] = None
    topics_included: list[str] = field(default_factory=list)

    @property
    def days_until(self) -> int:
        """Days until the exam."""
        return (self.date - date.today()).days

    @property
    def is_urgent(self) -> bool:
        """Check if exam is within 7 days."""
        return self.days_until <= 7

    @property
    def is_emergency(self) -> bool:
        """Check if exam is within 3 days."""
        return self.days_until <= 3

    def to_dict(self) -> dict:
        return {
            "date": self.date.isoformat(),
            "name": self.name,
            "type": self.type,
            "weight": self.weight,
            "duration_minutes": self.duration_minutes,
            "location": self.location,
            "topics_included": self.topics_included,
            "days_until": self.days_until,
            "is_urgent": self.is_urgent,
            "is_emergency": self.is_emergency,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ExamInfo":
        data = data.copy()
        data["date"] = date.fromisoformat(data["date"])
        # Remove computed properties
        data.pop("days_until", None)
        data.pop("is_urgent", None)
        data.pop("is_emergency", None)
        return cls(**data)


@dataclass
class SyllabusUnit:
    """A unit/topic in the syllabus."""
    id: str
    name: str
    description: Optional[str] = None
    weight: float = 0.0  # Weight in exam (percentage)
    estimated_hours: float = 2.0
    order: int = 0
    prerequisites: list[str] = field(default_factory=list)
    topics: list[str] = field(default_factory=list)
    resources: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "weight": self.weight,
            "estimated_hours": self.estimated_hours,
            "order": self.order,
            "prerequisites": self.prerequisites,
            "topics": self.topics,
            "resources": self.resources,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SyllabusUnit":
        return cls(**data)


@dataclass
class LearnerProfile:
    """Profile of the learner's preferences and style."""
    style: LearningStyle = LearningStyle.AUTO_DETECT
    detected_style: Optional[LearningStyle] = None
    pace: StudyPace = StudyPace.REGULAR
    hours_per_week: float = 8.0
    preferred_session_minutes: int = 45
    study_days: list[str] = field(default_factory=lambda: ["mon", "tue", "wed", "thu", "fri"])
    preferred_time: str = "evening"  # morning, afternoon, evening, night

    # Detected preferences (updated automatically)
    prefers_examples_first: bool = False
    prefers_theory_first: bool = False
    prefers_short_sessions: bool = False
    challenge_preference: str = "balanced"  # easy, balanced, challenging

    def to_dict(self) -> dict:
        return {
            "style": self.style.value,
            "detected_style": self.detected_style.value if self.detected_style else None,
            "pace": self.pace.value,
            "hours_per_week": self.hours_per_week,
            "preferred_session_minutes": self.preferred_session_minutes,
            "study_days": self.study_days,
            "preferred_time": self.preferred_time,
            "prefers_examples_first": self.prefers_examples_first,
            "prefers_theory_first": self.prefers_theory_first,
            "prefers_short_sessions": self.prefers_short_sessions,
            "challenge_preference": self.challenge_preference,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "LearnerProfile":
        data = data.copy()
        if "style" in data:
            data["style"] = LearningStyle(data["style"])
        if "detected_style" in data and data["detected_style"]:
            data["detected_style"] = LearningStyle(data["detected_style"])
        if "pace" in data:
            data["pace"] = StudyPace(data["pace"])
        return cls(**data)


@dataclass
class UniversityConfig:
    """Complete configuration for university context."""
    context: LearningContext
    subject: Subject
    exams: list[ExamInfo] = field(default_factory=list)
    syllabus_units: list[SyllabusUnit] = field(default_factory=list)
    learner_profile: LearnerProfile = field(default_factory=LearnerProfile)

    # Additional settings
    learning_language: str = "es"
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)

    @property
    def next_exam(self) -> Optional[ExamInfo]:
        """Get the next upcoming exam."""
        future_exams = [e for e in self.exams if e.days_until >= 0]
        if not future_exams:
            return None
        return min(future_exams, key=lambda e: e.days_until)

    @property
    def total_syllabus_hours(self) -> float:
        """Total estimated hours for all syllabus units."""
        return sum(u.estimated_hours for u in self.syllabus_units)

    def to_dict(self) -> dict:
        return {
            "context": self.context.value,
            "subject": self.subject.to_dict(),
            "exams": [e.to_dict() for e in self.exams],
            "syllabus_units": [u.to_dict() for u in self.syllabus_units],
            "learner_profile": self.learner_profile.to_dict(),
            "learning_language": self.learning_language,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "UniversityConfig":
        return cls(
            context=LearningContext(data["context"]),
            subject=Subject.from_dict(data["subject"]),
            exams=[ExamInfo.from_dict(e) for e in data.get("exams", [])],
            syllabus_units=[SyllabusUnit.from_dict(u) for u in data.get("syllabus_units", [])],
            learner_profile=LearnerProfile.from_dict(data.get("learner_profile", {})),
            learning_language=data.get("learning_language", "es"),
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.now(),
            last_updated=datetime.fromisoformat(data["last_updated"]) if "last_updated" in data else datetime.now(),
        )


class UniversityContextManager:
    """
    Manager for university learning context.

    Handles:
    - Configuration management
    - Syllabus operations
    - Topic status tracking
    - Exam countdown
    """

    def __init__(self, tutor_path: Path):
        self.tutor_path = tutor_path
        self.config_file = tutor_path / "university_config.json"
        self.topic_status_file = tutor_path / "topic_status.json"

        self._config: Optional[UniversityConfig] = None
        self._topic_status: dict[str, TopicStatus] = {}

        self._load()

    def _load(self) -> None:
        """Load configuration and topic status."""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._config = UniversityConfig.from_dict(data)

        if self.topic_status_file.exists():
            with open(self.topic_status_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._topic_status = {
                    k: TopicStatus(v) for k, v in data.items()
                }

    def _save(self) -> None:
        """Save configuration and topic status."""
        self.tutor_path.mkdir(parents=True, exist_ok=True)

        if self._config:
            self._config.last_updated = datetime.now()
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config.to_dict(), f, indent=2, ensure_ascii=False)

        with open(self.topic_status_file, 'w', encoding='utf-8') as f:
            json.dump(
                {k: v.value for k, v in self._topic_status.items()},
                f, indent=2
            )

    @property
    def config(self) -> Optional[UniversityConfig]:
        return self._config

    @property
    def is_configured(self) -> bool:
        return self._config is not None

    def initialize(
        self,
        context: LearningContext,
        subject: Subject,
        learner_profile: Optional[LearnerProfile] = None,
        learning_language: str = "es",
    ) -> UniversityConfig:
        """
        Initialize a new university context.

        Args:
            context: Type of learning context
            subject: Subject information
            learner_profile: Optional learner preferences
            learning_language: Language for content

        Returns:
            Created configuration
        """
        self._config = UniversityConfig(
            context=context,
            subject=subject,
            learner_profile=learner_profile or LearnerProfile(),
            learning_language=learning_language,
        )
        self._save()
        return self._config

    def add_exam(self, exam: ExamInfo) -> None:
        """Add an exam to the configuration."""
        if not self._config:
            raise ValueError("Context not initialized")

        self._config.exams.append(exam)
        self._config.exams.sort(key=lambda e: e.date)
        self._save()

    def add_syllabus_unit(self, unit: SyllabusUnit) -> None:
        """Add a syllabus unit."""
        if not self._config:
            raise ValueError("Context not initialized")

        self._config.syllabus_units.append(unit)
        self._config.syllabus_units.sort(key=lambda u: u.order)
        self._topic_status[unit.id] = TopicStatus.NEW
        self._save()

    def import_syllabus(self, units: list[SyllabusUnit]) -> int:
        """
        Import multiple syllabus units.

        Args:
            units: List of units to import

        Returns:
            Number of units imported
        """
        if not self._config:
            raise ValueError("Context not initialized")

        for unit in units:
            if unit.id not in [u.id for u in self._config.syllabus_units]:
                self._config.syllabus_units.append(unit)
                self._topic_status[unit.id] = TopicStatus.NEW

        self._config.syllabus_units.sort(key=lambda u: u.order)
        self._save()
        return len(units)

    def update_topic_status(self, topic_id: str, status: TopicStatus) -> None:
        """Update the status of a topic."""
        self._topic_status[topic_id] = status
        self._save()

    def get_topic_status(self, topic_id: str) -> TopicStatus:
        """Get the status of a topic."""
        return self._topic_status.get(topic_id, TopicStatus.NEW)

    def get_topics_by_status(self, status: TopicStatus) -> list[SyllabusUnit]:
        """Get all topics with a given status."""
        if not self._config:
            return []

        return [
            u for u in self._config.syllabus_units
            if self._topic_status.get(u.id) == status
        ]

    def get_study_summary(self) -> dict:
        """
        Get a summary of the current study state.

        Returns:
            Summary with progress, exam info, recommendations
        """
        if not self._config:
            return {"error": "Not configured"}

        # Count topics by status
        status_counts = {}
        for status in TopicStatus:
            status_counts[status.value] = len(self.get_topics_by_status(status))

        total_topics = len(self._config.syllabus_units)
        completed = status_counts.get("mastered", 0) + status_counts.get("learned", 0)

        # Calculate progress
        progress_pct = (completed / total_topics * 100) if total_topics > 0 else 0

        # Get exam info
        next_exam = self._config.next_exam
        exam_info = None
        if next_exam:
            exam_info = {
                "name": next_exam.name,
                "days_until": next_exam.days_until,
                "is_urgent": next_exam.is_urgent,
                "is_emergency": next_exam.is_emergency,
            }

        # Determine what needs attention
        needs_attention = []

        rusty_topics = self.get_topics_by_status(TopicStatus.RUSTY)
        if rusty_topics:
            needs_attention.append({
                "type": "rusty",
                "count": len(rusty_topics),
                "message": f"{len(rusty_topics)} topics need review",
            })

        if next_exam and next_exam.is_urgent:
            new_topics = self.get_topics_by_status(TopicStatus.NEW)
            if new_topics:
                needs_attention.append({
                    "type": "exam_urgent",
                    "count": len(new_topics),
                    "message": f"Exam in {next_exam.days_until} days, {len(new_topics)} topics not started",
                })

        return {
            "subject": self._config.subject.name,
            "context": self._config.context.value,
            "progress_percentage": round(progress_pct, 1),
            "topics": {
                "total": total_topics,
                "by_status": status_counts,
            },
            "next_exam": exam_info,
            "needs_attention": needs_attention,
            "hours_remaining": sum(
                u.estimated_hours for u in self._config.syllabus_units
                if self._topic_status.get(u.id) in [TopicStatus.NEW, TopicStatus.IN_PROGRESS]
            ),
        }

    def get_recommended_action(self) -> dict:
        """
        Get the recommended next action based on current state.

        Returns:
            Recommendation with action type and details
        """
        if not self._config:
            return {"action": "initialize", "message": "Please initialize your study plan first"}

        next_exam = self._config.next_exam

        # Check for rusty topics first (SRS priority)
        rusty = self.get_topics_by_status(TopicStatus.RUSTY)
        if rusty:
            return {
                "action": "review",
                "type": "srs_due",
                "topics": [u.name for u in rusty[:3]],
                "message": f"You have {len(rusty)} concepts to review",
                "estimated_minutes": min(len(rusty) * 5, 30),
            }

        # If exam is emergency mode
        if next_exam and next_exam.is_emergency:
            new_topics = self.get_topics_by_status(TopicStatus.NEW)
            if new_topics:
                # Focus on highest weight topics
                sorted_topics = sorted(new_topics, key=lambda t: t.weight, reverse=True)
                return {
                    "action": "emergency_learn",
                    "type": "exam_emergency",
                    "topic": sorted_topics[0].to_dict(),
                    "message": f"EXAM IN {next_exam.days_until} DAYS - Focus on high-weight topics",
                    "estimated_minutes": 60,
                }
            else:
                return {
                    "action": "exam_prep",
                    "type": "simulate",
                    "message": "All topics covered. Time for exam simulation!",
                    "estimated_minutes": next_exam.duration_minutes,
                }

        # If exam is urgent but not emergency
        if next_exam and next_exam.is_urgent:
            in_progress = self.get_topics_by_status(TopicStatus.IN_PROGRESS)
            if in_progress:
                return {
                    "action": "continue",
                    "type": "finish_topic",
                    "topic": in_progress[0].to_dict(),
                    "message": f"Exam in {next_exam.days_until} days - finish current topic",
                    "estimated_minutes": 45,
                }

        # Normal flow: continue in progress or start new
        in_progress = self.get_topics_by_status(TopicStatus.IN_PROGRESS)
        if in_progress:
            return {
                "action": "continue",
                "type": "in_progress",
                "topic": in_progress[0].to_dict(),
                "message": "Continue where you left off",
                "estimated_minutes": 45,
            }

        # Start new topic
        new_topics = self.get_topics_by_status(TopicStatus.NEW)
        if new_topics:
            # Respect prerequisites
            available = []
            for topic in new_topics:
                prereqs_met = all(
                    self._topic_status.get(p) in [TopicStatus.LEARNED, TopicStatus.MASTERED]
                    for p in topic.prerequisites
                )
                if prereqs_met:
                    available.append(topic)

            if available:
                return {
                    "action": "learn",
                    "type": "new_topic",
                    "topic": available[0].to_dict(),
                    "message": "Start a new topic",
                    "estimated_minutes": int(available[0].estimated_hours * 60),
                }

        # Everything learned, suggest reinforcement or extension
        learned = self.get_topics_by_status(TopicStatus.LEARNED)
        if learned:
            return {
                "action": "reinforce",
                "type": "practice",
                "topic": learned[0].to_dict(),
                "message": "Reinforce your knowledge with practice",
                "estimated_minutes": 30,
            }

        # All mastered
        return {
            "action": "extend",
            "type": "deepen",
            "message": "Excellent! Consider extending your knowledge or preparing for exams",
            "estimated_minutes": 60,
        }
