"""
Misconception Analysis System

Tracks and analyzes common errors and misconceptions to:
- Identify patterns in student mistakes
- Generate targeted remedial exercises
- Provide proactive warnings when approaching problem areas
- Track misconception resolution over time
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
import json
from pathlib import Path
from collections import defaultdict


class MisconceptionSeverity(Enum):
    """Severity levels for misconceptions."""
    LOW = "low"  # Minor misunderstanding, easily corrected
    MEDIUM = "medium"  # Significant gap, needs focused practice
    HIGH = "high"  # Fundamental misunderstanding, blocks progress
    CRITICAL = "critical"  # Prevents learning of dependent concepts


class MisconceptionStatus(Enum):
    """Status of a misconception."""
    ACTIVE = "active"  # Currently affecting performance
    IMPROVING = "improving"  # Being addressed, showing progress
    RESOLVED = "resolved"  # No longer appears in errors
    RECURRING = "recurring"  # Was resolved but reappeared


@dataclass
class MisconceptionInstance:
    """A single instance where a misconception appeared."""
    exercise_id: str
    exercise_type: str
    topic: str
    error_description: str
    student_response: str
    correct_response: str
    occurred_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "exercise_id": self.exercise_id,
            "exercise_type": self.exercise_type,
            "topic": self.topic,
            "error_description": self.error_description,
            "student_response": self.student_response,
            "correct_response": self.correct_response,
            "occurred_at": self.occurred_at.isoformat(),
        }


@dataclass
class Misconception:
    """A tracked misconception."""
    misconception_id: str
    name: str
    description: str
    category: str  # e.g., "syntax", "concept", "logic", "vocabulary"
    related_topics: list[str]
    severity: MisconceptionSeverity
    status: MisconceptionStatus
    instances: list[MisconceptionInstance]
    first_seen: datetime
    last_seen: datetime
    times_occurred: int
    times_corrected: int
    remediation_exercises: list[str]  # Exercise IDs that address this
    notes: str = ""

    def to_dict(self) -> dict:
        return {
            "misconception_id": self.misconception_id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "related_topics": self.related_topics,
            "severity": self.severity.value,
            "status": self.status.value,
            "instances": [i.to_dict() for i in self.instances[-10:]],  # Last 10
            "first_seen": self.first_seen.isoformat(),
            "last_seen": self.last_seen.isoformat(),
            "times_occurred": self.times_occurred,
            "times_corrected": self.times_corrected,
            "remediation_exercises": self.remediation_exercises,
            "notes": self.notes,
        }

    @property
    def correction_rate(self) -> float:
        """Calculate how often this misconception is being corrected."""
        if self.times_occurred == 0:
            return 0.0
        return self.times_corrected / self.times_occurred

    @property
    def is_improving(self) -> bool:
        """Check if misconception is improving based on recent instances."""
        if len(self.instances) < 3:
            return False

        recent = self.instances[-5:]
        older = self.instances[-10:-5] if len(self.instances) >= 10 else self.instances[:-5]

        if not older:
            return False

        # Compare frequency in recent vs older
        recent_days = (datetime.now() - recent[0].occurred_at).days or 1
        older_days = (recent[0].occurred_at - older[0].occurred_at).days or 1

        recent_rate = len(recent) / recent_days
        older_rate = len(older) / older_days

        return recent_rate < older_rate * 0.7  # 30% improvement


@dataclass
class RemediationSuggestion:
    """A suggestion for addressing a misconception."""
    misconception_id: str
    suggestion_type: str  # "exercise", "review", "explanation", "practice"
    title: str
    description: str
    estimated_time_minutes: int
    priority: float  # 0-1, higher = more urgent
    resources: list[str]  # Links to relevant materials

    def to_dict(self) -> dict:
        return {
            "misconception_id": self.misconception_id,
            "suggestion_type": self.suggestion_type,
            "title": self.title,
            "description": self.description,
            "estimated_time_minutes": self.estimated_time_minutes,
            "priority": self.priority,
            "resources": self.resources,
        }


class MisconceptionTracker:
    """
    Tracks and analyzes student misconceptions.

    Provides:
    - Pattern detection across exercises
    - Severity assessment
    - Remediation suggestions
    - Progress tracking
    """

    # Common misconception patterns by category
    COMMON_PATTERNS = {
        "programming": {
            "off_by_one": {
                "name": "Off-by-one errors",
                "description": "Errors in loop bounds or array indices",
                "keywords": ["index", "bound", "length", "loop", "array"],
                "severity": MisconceptionSeverity.MEDIUM,
            },
            "mutation_confusion": {
                "name": "Mutation vs immutability confusion",
                "description": "Confusion about when values are mutated vs copied",
                "keywords": ["mut", "mutable", "copy", "clone", "reference"],
                "severity": MisconceptionSeverity.HIGH,
            },
            "scope_confusion": {
                "name": "Variable scope confusion",
                "description": "Misunderstanding of variable scope and lifetime",
                "keywords": ["scope", "lifetime", "shadow", "block"],
                "severity": MisconceptionSeverity.HIGH,
            },
            "type_mismatch": {
                "name": "Type system misunderstanding",
                "description": "Confusion about type conversions and compatibility",
                "keywords": ["type", "convert", "cast", "expected", "found"],
                "severity": MisconceptionSeverity.MEDIUM,
            },
        },
        "mathematics": {
            "order_of_operations": {
                "name": "Order of operations errors",
                "description": "Incorrect application of PEMDAS/BODMAS",
                "keywords": ["order", "parentheses", "precedence"],
                "severity": MisconceptionSeverity.HIGH,
            },
            "negative_numbers": {
                "name": "Negative number handling",
                "description": "Errors with negative number operations",
                "keywords": ["negative", "minus", "subtract"],
                "severity": MisconceptionSeverity.MEDIUM,
            },
            "fraction_operations": {
                "name": "Fraction operation errors",
                "description": "Incorrect fraction arithmetic",
                "keywords": ["fraction", "denominator", "numerator"],
                "severity": MisconceptionSeverity.MEDIUM,
            },
        },
        "language": {
            "false_cognates": {
                "name": "False cognate confusion",
                "description": "Confusing words that look similar but have different meanings",
                "keywords": ["similar", "looks like", "means"],
                "severity": MisconceptionSeverity.LOW,
            },
            "verb_conjugation": {
                "name": "Verb conjugation errors",
                "description": "Incorrect verb forms or tenses",
                "keywords": ["verb", "tense", "conjugate", "form"],
                "severity": MisconceptionSeverity.MEDIUM,
            },
            "gender_agreement": {
                "name": "Gender/number agreement",
                "description": "Errors in grammatical gender or number agreement",
                "keywords": ["gender", "masculine", "feminine", "plural"],
                "severity": MisconceptionSeverity.MEDIUM,
            },
        },
    }

    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize the misconception tracker.

        Args:
            storage_path: Path to store misconception data
        """
        self.storage_path = storage_path or Path.cwd() / ".tutor" / "misconceptions.json"
        self.misconceptions: dict[str, Misconception] = {}
        self._load_data()

    def record_error(
        self,
        exercise_id: str,
        exercise_type: str,
        topic: str,
        error_description: str,
        student_response: str,
        correct_response: str,
        misconception_id: Optional[str] = None,
        category: Optional[str] = None,
    ) -> Misconception:
        """
        Record an error and associate it with a misconception.

        Args:
            exercise_id: Exercise where error occurred
            exercise_type: Type of exercise
            topic: Topic being studied
            error_description: Description of the error
            student_response: What the student submitted
            correct_response: What was expected
            misconception_id: Known misconception ID (auto-detected if None)
            category: Category for pattern matching

        Returns:
            The misconception record
        """
        instance = MisconceptionInstance(
            exercise_id=exercise_id,
            exercise_type=exercise_type,
            topic=topic,
            error_description=error_description,
            student_response=student_response,
            correct_response=correct_response,
        )

        # Auto-detect misconception if not provided
        if not misconception_id:
            misconception_id = self._detect_misconception(
                error_description, student_response, category
            )

        # Create or update misconception
        if misconception_id in self.misconceptions:
            misconception = self.misconceptions[misconception_id]
            misconception.instances.append(instance)
            misconception.last_seen = datetime.now()
            misconception.times_occurred += 1

            # Update status based on pattern
            if misconception.status == MisconceptionStatus.RESOLVED:
                misconception.status = MisconceptionStatus.RECURRING
            elif misconception.is_improving:
                misconception.status = MisconceptionStatus.IMPROVING
        else:
            # Create new misconception
            pattern = self._get_pattern_info(misconception_id, category)

            misconception = Misconception(
                misconception_id=misconception_id,
                name=pattern.get("name", error_description[:50]),
                description=pattern.get("description", error_description),
                category=category or "general",
                related_topics=[topic],
                severity=pattern.get("severity", MisconceptionSeverity.MEDIUM),
                status=MisconceptionStatus.ACTIVE,
                instances=[instance],
                first_seen=datetime.now(),
                last_seen=datetime.now(),
                times_occurred=1,
                times_corrected=0,
                remediation_exercises=[],
            )
            self.misconceptions[misconception_id] = misconception

        # Update related topics
        if topic not in misconception.related_topics:
            misconception.related_topics.append(topic)

        self._save_data()
        return misconception

    def record_correction(self, misconception_id: str) -> Optional[Misconception]:
        """
        Record that a misconception was successfully corrected.

        Args:
            misconception_id: ID of the corrected misconception

        Returns:
            Updated misconception or None if not found
        """
        if misconception_id not in self.misconceptions:
            return None

        misconception = self.misconceptions[misconception_id]
        misconception.times_corrected += 1

        # Check if resolved
        if misconception.correction_rate > 0.8:
            days_since_last = (datetime.now() - misconception.last_seen).days
            if days_since_last > 7:
                misconception.status = MisconceptionStatus.RESOLVED

        self._save_data()
        return misconception

    def get_active_misconceptions(self) -> list[Misconception]:
        """Get all active (unresolved) misconceptions."""
        return [
            m for m in self.misconceptions.values()
            if m.status in [MisconceptionStatus.ACTIVE, MisconceptionStatus.RECURRING]
        ]

    def get_misconceptions_for_topic(self, topic: str) -> list[Misconception]:
        """Get misconceptions related to a specific topic."""
        return [
            m for m in self.misconceptions.values()
            if topic in m.related_topics
        ]

    def get_high_priority_misconceptions(self, limit: int = 5) -> list[Misconception]:
        """
        Get misconceptions that need immediate attention.

        Prioritizes by:
        1. Severity
        2. Frequency
        3. Recency
        """
        active = self.get_active_misconceptions()

        def priority_score(m: Misconception) -> float:
            severity_weight = {
                MisconceptionSeverity.CRITICAL: 4,
                MisconceptionSeverity.HIGH: 3,
                MisconceptionSeverity.MEDIUM: 2,
                MisconceptionSeverity.LOW: 1,
            }

            # Base score from severity
            score = severity_weight[m.severity]

            # Boost for frequency
            score += min(m.times_occurred / 10, 2)

            # Boost for recency (within last week)
            days_ago = (datetime.now() - m.last_seen).days
            if days_ago < 7:
                score += (7 - days_ago) / 7

            # Penalty for improving
            if m.status == MisconceptionStatus.IMPROVING:
                score *= 0.7

            # Boost for recurring (was fixed, came back)
            if m.status == MisconceptionStatus.RECURRING:
                score *= 1.3

            return score

        sorted_misconceptions = sorted(active, key=priority_score, reverse=True)
        return sorted_misconceptions[:limit]

    def get_remediation_suggestions(
        self,
        misconception_id: Optional[str] = None,
        limit: int = 5
    ) -> list[RemediationSuggestion]:
        """
        Get suggestions for addressing misconceptions.

        Args:
            misconception_id: Specific misconception (or None for all)
            limit: Maximum suggestions to return

        Returns:
            List of remediation suggestions
        """
        if misconception_id:
            misconceptions = [self.misconceptions.get(misconception_id)]
            misconceptions = [m for m in misconceptions if m]
        else:
            misconceptions = self.get_high_priority_misconceptions(limit)

        suggestions = []

        for m in misconceptions:
            # Create suggestions based on severity and type
            if m.severity in [MisconceptionSeverity.CRITICAL, MisconceptionSeverity.HIGH]:
                suggestions.append(RemediationSuggestion(
                    misconception_id=m.misconception_id,
                    suggestion_type="review",
                    title=f"Review: {m.name}",
                    description=f"Review the fundamental concept behind {m.name}. "
                               f"This misconception has appeared {m.times_occurred} times.",
                    estimated_time_minutes=15,
                    priority=0.9 if m.severity == MisconceptionSeverity.CRITICAL else 0.8,
                    resources=m.related_topics,
                ))

            suggestions.append(RemediationSuggestion(
                misconception_id=m.misconception_id,
                suggestion_type="practice",
                title=f"Practice: {m.name}",
                description=f"Complete targeted exercises to address {m.name}.",
                estimated_time_minutes=20,
                priority=0.7,
                resources=m.remediation_exercises or m.related_topics,
            ))

            if m.status == MisconceptionStatus.RECURRING:
                suggestions.append(RemediationSuggestion(
                    misconception_id=m.misconception_id,
                    suggestion_type="explanation",
                    title=f"Deep Dive: {m.name}",
                    description=f"This misconception has reappeared after being resolved. "
                               f"A deeper understanding may be needed.",
                    estimated_time_minutes=30,
                    priority=0.85,
                    resources=m.related_topics,
                ))

        # Sort by priority
        suggestions.sort(key=lambda s: s.priority, reverse=True)
        return suggestions[:limit]

    def get_statistics(self) -> dict:
        """Get overall misconception statistics."""
        total = len(self.misconceptions)
        if total == 0:
            return {
                "total_misconceptions": 0,
                "active": 0,
                "resolved": 0,
                "by_severity": {},
                "by_category": {},
            }

        by_status = defaultdict(int)
        by_severity = defaultdict(int)
        by_category = defaultdict(int)

        for m in self.misconceptions.values():
            by_status[m.status.value] += 1
            by_severity[m.severity.value] += 1
            by_category[m.category] += 1

        return {
            "total_misconceptions": total,
            "active": by_status["active"] + by_status["recurring"],
            "resolved": by_status["resolved"],
            "improving": by_status["improving"],
            "by_status": dict(by_status),
            "by_severity": dict(by_severity),
            "by_category": dict(by_category),
            "resolution_rate": by_status["resolved"] / total if total > 0 else 0,
        }

    def get_warning_for_topic(self, topic: str) -> Optional[str]:
        """
        Get a warning message if the student has misconceptions in a topic.

        Args:
            topic: Topic about to be studied

        Returns:
            Warning message or None
        """
        topic_misconceptions = self.get_misconceptions_for_topic(topic)
        active = [m for m in topic_misconceptions if m.status != MisconceptionStatus.RESOLVED]

        if not active:
            return None

        high_severity = [m for m in active if m.severity in [
            MisconceptionSeverity.HIGH, MisconceptionSeverity.CRITICAL
        ]]

        if high_severity:
            names = ", ".join(m.name for m in high_severity[:3])
            return (
                f"⚠️ Watch out! You've had difficulty with: {names}. "
                f"Pay special attention to these concepts in this lesson."
            )
        elif active:
            return (
                f"💡 Tip: You've had some misconceptions in this area before. "
                f"Take your time and review if anything seems unclear."
            )

        return None

    def _detect_misconception(
        self,
        error_description: str,
        student_response: str,
        category: Optional[str]
    ) -> str:
        """Auto-detect misconception type from error patterns."""
        error_lower = error_description.lower()
        response_lower = student_response.lower()
        combined = error_lower + " " + response_lower

        # Check known patterns
        if category and category in self.COMMON_PATTERNS:
            patterns = self.COMMON_PATTERNS[category]
            for pattern_id, pattern_info in patterns.items():
                keywords = pattern_info.get("keywords", [])
                if any(kw in combined for kw in keywords):
                    return pattern_id

        # Generate ID from error description
        words = error_description.split()[:5]
        return "_".join(w.lower() for w in words if w.isalnum())

    def _get_pattern_info(self, pattern_id: str, category: Optional[str]) -> dict:
        """Get information about a known pattern."""
        if category and category in self.COMMON_PATTERNS:
            patterns = self.COMMON_PATTERNS[category]
            if pattern_id in patterns:
                return patterns[pattern_id]
        return {}

    def _load_data(self) -> None:
        """Load misconception data from storage."""
        if not self.storage_path.exists():
            return

        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for item in data.get("misconceptions", []):
                instances = [
                    MisconceptionInstance(
                        exercise_id=i["exercise_id"],
                        exercise_type=i["exercise_type"],
                        topic=i["topic"],
                        error_description=i["error_description"],
                        student_response=i["student_response"],
                        correct_response=i["correct_response"],
                        occurred_at=datetime.fromisoformat(i["occurred_at"]),
                    )
                    for i in item.get("instances", [])
                ]

                misconception = Misconception(
                    misconception_id=item["misconception_id"],
                    name=item["name"],
                    description=item["description"],
                    category=item["category"],
                    related_topics=item["related_topics"],
                    severity=MisconceptionSeverity(item["severity"]),
                    status=MisconceptionStatus(item["status"]),
                    instances=instances,
                    first_seen=datetime.fromisoformat(item["first_seen"]),
                    last_seen=datetime.fromisoformat(item["last_seen"]),
                    times_occurred=item["times_occurred"],
                    times_corrected=item["times_corrected"],
                    remediation_exercises=item.get("remediation_exercises", []),
                    notes=item.get("notes", ""),
                )
                self.misconceptions[misconception.misconception_id] = misconception

        except (json.JSONDecodeError, KeyError, ValueError):
            pass

    def _save_data(self) -> None:
        """Save misconception data to storage."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "misconceptions": [m.to_dict() for m in self.misconceptions.values()],
            "updated_at": datetime.now().isoformat(),
        }

        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
