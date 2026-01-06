"""
Spaced Repetition System

Implements a spaced repetition algorithm to optimize knowledge retention.
Based on the SM-2 algorithm with modifications for programming concepts.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
import math
import json
from pathlib import Path


@dataclass
class ReviewItem:
    """An item scheduled for spaced repetition review."""
    item_id: str  # Unique identifier (e.g., "skill:ownership" or "exercise:ex01")
    item_type: str  # "skill", "exercise", "concept", "flashcard"
    content_ref: str  # Reference to the actual content
    title: str

    # SM-2 algorithm state
    easiness_factor: float = 2.5  # E-Factor, min 1.3
    interval_days: int = 1  # Current interval
    repetition_count: int = 0  # Number of successful reviews
    last_review: Optional[datetime] = None
    next_review: Optional[datetime] = None

    # Additional metadata
    created_at: datetime = field(default_factory=datetime.now)
    total_reviews: int = 0
    correct_reviews: int = 0

    @property
    def is_due(self) -> bool:
        """Check if item is due for review."""
        if self.next_review is None:
            return True
        return datetime.now() >= self.next_review

    @property
    def days_until_due(self) -> int:
        """Days until next review (negative if overdue)."""
        if self.next_review is None:
            return 0
        delta = self.next_review - datetime.now()
        return delta.days

    @property
    def retention_rate(self) -> float:
        """Percentage of correct reviews."""
        if self.total_reviews == 0:
            return 0.0
        return self.correct_reviews / self.total_reviews

    def to_dict(self) -> dict:
        return {
            "item_id": self.item_id,
            "item_type": self.item_type,
            "content_ref": self.content_ref,
            "title": self.title,
            "easiness_factor": self.easiness_factor,
            "interval_days": self.interval_days,
            "repetition_count": self.repetition_count,
            "last_review": self.last_review.isoformat() if self.last_review else None,
            "next_review": self.next_review.isoformat() if self.next_review else None,
            "created_at": self.created_at.isoformat(),
            "total_reviews": self.total_reviews,
            "correct_reviews": self.correct_reviews,
            "is_due": self.is_due,
            "days_until_due": self.days_until_due,
            "retention_rate": self.retention_rate,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ReviewItem":
        return cls(
            item_id=data["item_id"],
            item_type=data["item_type"],
            content_ref=data["content_ref"],
            title=data["title"],
            easiness_factor=data.get("easiness_factor", 2.5),
            interval_days=data.get("interval_days", 1),
            repetition_count=data.get("repetition_count", 0),
            last_review=datetime.fromisoformat(data["last_review"]) if data.get("last_review") else None,
            next_review=datetime.fromisoformat(data["next_review"]) if data.get("next_review") else None,
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else datetime.now(),
            total_reviews=data.get("total_reviews", 0),
            correct_reviews=data.get("correct_reviews", 0),
        )


class SpacedRepetitionSystem:
    """
    Spaced Repetition System using modified SM-2 algorithm.

    The system schedules reviews at increasing intervals based on
    how well the student remembers the material.

    Quality ratings:
    - 0: Complete blackout, no memory
    - 1: Incorrect response, remembered upon seeing answer
    - 2: Incorrect response, but answer seemed easy to recall
    - 3: Correct response with serious difficulty
    - 4: Correct response after some hesitation
    - 5: Perfect response
    """

    # Quality thresholds
    QUALITY_PERFECT = 5
    QUALITY_HESITATION = 4
    QUALITY_DIFFICULT = 3
    QUALITY_EASY_INCORRECT = 2
    QUALITY_REMEMBERED_AFTER = 1
    QUALITY_BLACKOUT = 0

    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize the spaced repetition system.

        Args:
            storage_path: Path to store review data (default: .tutor/srs.json)
        """
        self.storage_path = storage_path or Path.cwd() / ".tutor" / "srs.json"
        self.items: dict[str, ReviewItem] = {}
        self._load()

    def add_item(
        self,
        item_id: str,
        item_type: str,
        content_ref: str,
        title: str,
    ) -> ReviewItem:
        """
        Add a new item to the SRS.

        Args:
            item_id: Unique identifier
            item_type: Type of item
            content_ref: Reference to content
            title: Display title

        Returns:
            The created ReviewItem
        """
        if item_id in self.items:
            return self.items[item_id]

        item = ReviewItem(
            item_id=item_id,
            item_type=item_type,
            content_ref=content_ref,
            title=title,
            next_review=datetime.now(),  # Due immediately
        )

        self.items[item_id] = item
        self._save()
        return item

    def record_review(self, item_id: str, quality: int) -> ReviewItem:
        """
        Record a review and update scheduling.

        Uses SM-2 algorithm to calculate next review date.

        Args:
            item_id: Item that was reviewed
            quality: Quality of recall (0-5)

        Returns:
            Updated ReviewItem with new schedule
        """
        quality = max(0, min(5, quality))  # Clamp to 0-5

        if item_id not in self.items:
            raise ValueError(f"Item {item_id} not found")

        item = self.items[item_id]
        item.total_reviews += 1
        item.last_review = datetime.now()

        if quality >= 3:
            item.correct_reviews += 1

        # SM-2 Algorithm
        if quality < 3:
            # Reset on failure
            item.repetition_count = 0
            item.interval_days = 1
        else:
            # Update easiness factor
            item.easiness_factor = max(
                1.3,
                item.easiness_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
            )

            # Update interval
            if item.repetition_count == 0:
                item.interval_days = 1
            elif item.repetition_count == 1:
                item.interval_days = 6
            else:
                item.interval_days = math.ceil(item.interval_days * item.easiness_factor)

            item.repetition_count += 1

        # Schedule next review
        item.next_review = datetime.now() + timedelta(days=item.interval_days)

        self._save()
        return item

    def get_due_items(self, limit: int = 20) -> list[ReviewItem]:
        """
        Get items that are due for review.

        Args:
            limit: Maximum number of items to return

        Returns:
            List of due items, sorted by priority
        """
        due = [item for item in self.items.values() if item.is_due]

        # Sort by priority:
        # 1. Most overdue first
        # 2. Lower easiness factor (harder items) first
        due.sort(key=lambda i: (
            i.days_until_due,  # Negative for overdue
            i.easiness_factor,
        ))

        return due[:limit]

    def get_upcoming_items(self, days: int = 7) -> list[ReviewItem]:
        """
        Get items scheduled for review in the next N days.

        Args:
            days: Number of days to look ahead

        Returns:
            List of upcoming items with their scheduled dates
        """
        cutoff = datetime.now() + timedelta(days=days)

        upcoming = [
            item for item in self.items.values()
            if item.next_review and item.next_review <= cutoff
        ]

        upcoming.sort(key=lambda i: i.next_review or datetime.max)
        return upcoming

    def get_statistics(self) -> dict:
        """
        Get SRS statistics.

        Returns:
            Dictionary with stats about the review system
        """
        if not self.items:
            return {
                "total_items": 0,
                "due_now": 0,
                "due_today": 0,
                "due_this_week": 0,
                "average_retention": 0.0,
                "mature_items": 0,
                "learning_items": 0,
            }

        now = datetime.now()
        today_end = now.replace(hour=23, minute=59, second=59)
        week_end = now + timedelta(days=7)

        mature_items = [i for i in self.items.values() if i.interval_days >= 21]
        learning_items = [i for i in self.items.values() if i.interval_days < 21]

        due_now = len([i for i in self.items.values() if i.is_due])
        due_today = len([
            i for i in self.items.values()
            if i.next_review and i.next_review <= today_end
        ])
        due_this_week = len([
            i for i in self.items.values()
            if i.next_review and i.next_review <= week_end
        ])

        total_retention = sum(i.retention_rate for i in self.items.values())
        avg_retention = total_retention / len(self.items) if self.items else 0

        return {
            "total_items": len(self.items),
            "due_now": due_now,
            "due_today": due_today,
            "due_this_week": due_this_week,
            "average_retention": round(avg_retention * 100, 1),
            "mature_items": len(mature_items),
            "learning_items": len(learning_items),
            "items_by_type": self._count_by_type(),
        }

    def _count_by_type(self) -> dict[str, int]:
        """Count items by type."""
        counts: dict[str, int] = {}
        for item in self.items.values():
            counts[item.item_type] = counts.get(item.item_type, 0) + 1
        return counts

    def _load(self):
        """Load items from storage."""
        if not self.storage_path.exists():
            return

        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for item_data in data.get("items", []):
                item = ReviewItem.from_dict(item_data)
                self.items[item.item_id] = item

        except (json.JSONDecodeError, KeyError):
            pass

    def _save(self):
        """Save items to storage."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "version": 1,
            "updated_at": datetime.now().isoformat(),
            "items": [item.to_dict() for item in self.items.values()],
        }

        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


def quality_from_exercise_result(score: int, attempts: int) -> int:
    """
    Convert exercise result to SRS quality rating.

    Args:
        score: Exercise score (0-100)
        attempts: Number of attempts

    Returns:
        Quality rating (0-5)
    """
    if attempts > 3:
        # Multiple attempts suggests difficulty
        if score >= 80:
            return 3  # Correct but difficult
        return 2 if score >= 50 else 1

    if score >= 95:
        return 5  # Perfect
    elif score >= 80:
        return 4  # Correct with hesitation
    elif score >= 60:
        return 3  # Correct but difficult
    elif score >= 40:
        return 2  # Incorrect but familiar
    else:
        return 1 if score > 0 else 0
