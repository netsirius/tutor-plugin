"""
Gamification System

Provides light gamification to increase engagement:
- Achievement badges
- Weekly challenges
- Progress milestones
- Streak tracking
- Personal bests (vs yourself, not others)
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
import json
from pathlib import Path
import random


class BadgeCategory(Enum):
    """Categories of achievement badges."""
    MILESTONE = "milestone"  # Completing X exercises, modules, etc.
    STREAK = "streak"  # Consistency achievements
    MASTERY = "mastery"  # High scores, perfect exercises
    EXPLORATION = "exploration"  # Trying new things
    IMPROVEMENT = "improvement"  # Personal growth
    CHALLENGE = "challenge"  # Completing weekly/special challenges


class BadgeRarity(Enum):
    """Rarity levels for badges."""
    COMMON = "common"  # Easy to get
    UNCOMMON = "uncommon"  # Requires some effort
    RARE = "rare"  # Significant achievement
    EPIC = "epic"  # Major milestone
    LEGENDARY = "legendary"  # Exceptional achievement


@dataclass
class Badge:
    """An achievement badge."""
    badge_id: str
    name: str
    description: str
    category: BadgeCategory
    rarity: BadgeRarity
    icon: str  # Emoji representation
    requirement: str  # Human-readable requirement
    earned_at: Optional[datetime] = None
    progress: float = 0.0  # 0-1 progress towards earning

    def to_dict(self) -> dict:
        return {
            "badge_id": self.badge_id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "rarity": self.rarity.value,
            "icon": self.icon,
            "requirement": self.requirement,
            "earned": self.earned_at is not None,
            "earned_at": self.earned_at.isoformat() if self.earned_at else None,
            "progress": self.progress,
        }


@dataclass
class Challenge:
    """A weekly or special challenge."""
    challenge_id: str
    name: str
    description: str
    challenge_type: str  # "weekly", "daily", "special"
    requirements: dict  # What needs to be done
    reward_badge: Optional[str]  # Badge ID to award
    reward_xp: int
    start_date: datetime
    end_date: datetime
    completed: bool = False
    progress: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "challenge_id": self.challenge_id,
            "name": self.name,
            "description": self.description,
            "challenge_type": self.challenge_type,
            "requirements": self.requirements,
            "reward_badge": self.reward_badge,
            "reward_xp": self.reward_xp,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "completed": self.completed,
            "progress": self.progress,
            "time_remaining": str(self.end_date - datetime.now()) if self.end_date > datetime.now() else "Expired",
        }


@dataclass
class PersonalBest:
    """A personal best record."""
    category: str
    value: float
    achieved_at: datetime
    context: str  # What was being done

    def to_dict(self) -> dict:
        return {
            "category": self.category,
            "value": self.value,
            "achieved_at": self.achieved_at.isoformat(),
            "context": self.context,
        }


@dataclass
class Milestone:
    """A progress milestone."""
    milestone_id: str
    name: str
    description: str
    target_value: int
    current_value: int
    reached: bool
    reached_at: Optional[datetime]

    def to_dict(self) -> dict:
        return {
            "milestone_id": self.milestone_id,
            "name": self.name,
            "description": self.description,
            "target_value": self.target_value,
            "current_value": self.current_value,
            "progress_percent": min(100, self.current_value / self.target_value * 100),
            "reached": self.reached,
            "reached_at": self.reached_at.isoformat() if self.reached_at else None,
        }


class GamificationEngine:
    """
    Manages gamification features for the tutor.

    Focus is on personal growth, not competition.
    """

    # Available badges definition
    BADGE_DEFINITIONS = {
        # Milestone badges
        "first_exercise": Badge(
            "first_exercise", "First Steps", "Complete your first exercise",
            BadgeCategory.MILESTONE, BadgeRarity.COMMON, "🎯",
            "Complete 1 exercise"
        ),
        "ten_exercises": Badge(
            "ten_exercises", "Getting Warmed Up", "Complete 10 exercises",
            BadgeCategory.MILESTONE, BadgeRarity.COMMON, "💪",
            "Complete 10 exercises"
        ),
        "fifty_exercises": Badge(
            "fifty_exercises", "Dedicated Learner", "Complete 50 exercises",
            BadgeCategory.MILESTONE, BadgeRarity.UNCOMMON, "📚",
            "Complete 50 exercises"
        ),
        "hundred_exercises": Badge(
            "hundred_exercises", "Century Club", "Complete 100 exercises",
            BadgeCategory.MILESTONE, BadgeRarity.RARE, "🏆",
            "Complete 100 exercises"
        ),
        "first_module": Badge(
            "first_module", "Module Master", "Complete your first module",
            BadgeCategory.MILESTONE, BadgeRarity.COMMON, "📦",
            "Complete 1 module"
        ),
        "five_modules": Badge(
            "five_modules", "Knowledge Seeker", "Complete 5 modules",
            BadgeCategory.MILESTONE, BadgeRarity.UNCOMMON, "🎓",
            "Complete 5 modules"
        ),

        # Streak badges
        "streak_3": Badge(
            "streak_3", "Consistent", "Maintain a 3-day streak",
            BadgeCategory.STREAK, BadgeRarity.COMMON, "🔥",
            "Study for 3 days in a row"
        ),
        "streak_7": Badge(
            "streak_7", "Week Warrior", "Maintain a 7-day streak",
            BadgeCategory.STREAK, BadgeRarity.UNCOMMON, "⚡",
            "Study for 7 days in a row"
        ),
        "streak_30": Badge(
            "streak_30", "Monthly Master", "Maintain a 30-day streak",
            BadgeCategory.STREAK, BadgeRarity.RARE, "🌟",
            "Study for 30 days in a row"
        ),
        "streak_100": Badge(
            "streak_100", "Unstoppable", "Maintain a 100-day streak",
            BadgeCategory.STREAK, BadgeRarity.LEGENDARY, "👑",
            "Study for 100 days in a row"
        ),

        # Mastery badges
        "perfect_score": Badge(
            "perfect_score", "Perfectionist", "Get a perfect score on an exercise",
            BadgeCategory.MASTERY, BadgeRarity.COMMON, "💯",
            "Score 100% on any exercise"
        ),
        "five_perfect": Badge(
            "five_perfect", "High Achiever", "Get 5 perfect scores",
            BadgeCategory.MASTERY, BadgeRarity.UNCOMMON, "🌟",
            "Score 100% on 5 exercises"
        ),
        "first_try": Badge(
            "first_try", "Natural Talent", "Pass an exercise on first try with 90%+",
            BadgeCategory.MASTERY, BadgeRarity.UNCOMMON, "🎯",
            "Score 90%+ on first attempt"
        ),
        "speed_demon": Badge(
            "speed_demon", "Speed Demon", "Complete an exercise in under 5 minutes with 80%+",
            BadgeCategory.MASTERY, BadgeRarity.RARE, "⚡",
            "Fast completion with high score"
        ),

        # Improvement badges
        "comeback": Badge(
            "comeback", "Comeback Kid", "Improve from failing to passing on same exercise",
            BadgeCategory.IMPROVEMENT, BadgeRarity.COMMON, "📈",
            "Fail then pass the same exercise"
        ),
        "big_improvement": Badge(
            "big_improvement", "Level Up", "Improve your average score by 20%",
            BadgeCategory.IMPROVEMENT, BadgeRarity.UNCOMMON, "🚀",
            "Significant score improvement"
        ),
        "consistency_improvement": Badge(
            "consistency_improvement", "Steady Progress", "Improve scores for 5 exercises in a row",
            BadgeCategory.IMPROVEMENT, BadgeRarity.RARE, "📊",
            "Consistent improvement trend"
        ),

        # Exploration badges
        "early_bird": Badge(
            "early_bird", "Early Bird", "Study before 8 AM",
            BadgeCategory.EXPLORATION, BadgeRarity.COMMON, "🌅",
            "Start a session before 8 AM"
        ),
        "night_owl": Badge(
            "night_owl", "Night Owl", "Study after 10 PM",
            BadgeCategory.EXPLORATION, BadgeRarity.COMMON, "🦉",
            "Start a session after 10 PM"
        ),
        "weekend_warrior": Badge(
            "weekend_warrior", "Weekend Warrior", "Study on both Saturday and Sunday",
            BadgeCategory.EXPLORATION, BadgeRarity.COMMON, "🗓️",
            "Study on weekend days"
        ),
        "try_everything": Badge(
            "try_everything", "Curious Mind", "Try 5 different exercise types",
            BadgeCategory.EXPLORATION, BadgeRarity.UNCOMMON, "🔍",
            "Experience variety in learning"
        ),

        # Challenge badges
        "weekly_champion": Badge(
            "weekly_champion", "Weekly Champion", "Complete a weekly challenge",
            BadgeCategory.CHALLENGE, BadgeRarity.UNCOMMON, "🏅",
            "Complete any weekly challenge"
        ),
        "challenge_streak": Badge(
            "challenge_streak", "Challenge Accepted", "Complete 4 weekly challenges in a row",
            BadgeCategory.CHALLENGE, BadgeRarity.RARE, "🎖️",
            "Monthly challenge completion"
        ),
    }

    # Weekly challenge templates
    WEEKLY_CHALLENGES = [
        {
            "name": "Exercise Marathon",
            "description": "Complete 15 exercises this week",
            "requirements": {"exercises_completed": 15},
            "reward_xp": 100,
        },
        {
            "name": "Perfect Week",
            "description": "Get 3 perfect scores this week",
            "requirements": {"perfect_scores": 3},
            "reward_xp": 150,
        },
        {
            "name": "Streak Builder",
            "description": "Study every day this week",
            "requirements": {"streak_days": 7},
            "reward_xp": 200,
        },
        {
            "name": "Deep Dive",
            "description": "Spend 3+ hours studying this week",
            "requirements": {"study_minutes": 180},
            "reward_xp": 120,
        },
        {
            "name": "Review Master",
            "description": "Complete 10 spaced repetition reviews",
            "requirements": {"reviews_completed": 10},
            "reward_xp": 80,
        },
        {
            "name": "First Try Streak",
            "description": "Pass 5 exercises on first attempt",
            "requirements": {"first_try_passes": 5},
            "reward_xp": 150,
        },
    ]

    def __init__(self, progress: dict, storage_path: Optional[Path] = None):
        """
        Initialize the gamification engine.

        Args:
            progress: Student progress data
            storage_path: Path to store gamification data
        """
        self.progress = progress
        self.storage_path = storage_path or Path.cwd() / ".tutor" / "gamification.json"

        self.earned_badges: dict[str, Badge] = {}
        self.active_challenges: list[Challenge] = []
        self.completed_challenges: list[str] = []
        self.personal_bests: dict[str, PersonalBest] = {}
        self.xp: int = 0
        self.level: int = 1

        self._load_data()

    def check_achievements(self, event: dict) -> list[Badge]:
        """
        Check for new achievements based on an event.

        Args:
            event: Dict with event info (type, details)

        Returns:
            List of newly earned badges
        """
        new_badges = []

        # Extract stats
        stats = self.progress.get("statistics", {})
        total_exercises = stats.get("total_exercises_completed", 0)
        streak = stats.get("streak_days", 0)
        avg_score = stats.get("average_score", 0)

        # Count modules
        modules = self.progress.get("modules", {})
        completed_modules = sum(
            1 for m in modules.values()
            if m.get("status") == "completed"
        )

        # Check milestone badges
        milestone_checks = [
            ("first_exercise", total_exercises >= 1),
            ("ten_exercises", total_exercises >= 10),
            ("fifty_exercises", total_exercises >= 50),
            ("hundred_exercises", total_exercises >= 100),
            ("first_module", completed_modules >= 1),
            ("five_modules", completed_modules >= 5),
        ]

        for badge_id, condition in milestone_checks:
            if condition and badge_id not in self.earned_badges:
                badge = self._earn_badge(badge_id)
                if badge:
                    new_badges.append(badge)

        # Check streak badges
        streak_checks = [
            ("streak_3", streak >= 3),
            ("streak_7", streak >= 7),
            ("streak_30", streak >= 30),
            ("streak_100", streak >= 100),
        ]

        for badge_id, condition in streak_checks:
            if condition and badge_id not in self.earned_badges:
                badge = self._earn_badge(badge_id)
                if badge:
                    new_badges.append(badge)

        # Check event-specific badges
        if event.get("type") == "exercise_completed":
            score = event.get("score", 0)
            attempts = event.get("attempts", 1)
            time_minutes = event.get("time_minutes", 0)

            # Perfect score
            if score == 100 and "perfect_score" not in self.earned_badges:
                badge = self._earn_badge("perfect_score")
                if badge:
                    new_badges.append(badge)

            # First try with high score
            if attempts == 1 and score >= 90 and "first_try" not in self.earned_badges:
                badge = self._earn_badge("first_try")
                if badge:
                    new_badges.append(badge)

            # Speed demon
            if time_minutes < 5 and score >= 80 and "speed_demon" not in self.earned_badges:
                badge = self._earn_badge("speed_demon")
                if badge:
                    new_badges.append(badge)

        # Check time-based badges
        if event.get("type") == "session_started":
            hour = datetime.now().hour
            if hour < 8 and "early_bird" not in self.earned_badges:
                badge = self._earn_badge("early_bird")
                if badge:
                    new_badges.append(badge)
            elif hour >= 22 and "night_owl" not in self.earned_badges:
                badge = self._earn_badge("night_owl")
                if badge:
                    new_badges.append(badge)

        # Update challenges
        self._update_challenges(event)

        self._save_data()
        return new_badges

    def get_current_challenge(self) -> Optional[Challenge]:
        """Get the current active weekly challenge."""
        now = datetime.now()

        # Check if we have a valid active challenge
        for challenge in self.active_challenges:
            if challenge.start_date <= now <= challenge.end_date and not challenge.completed:
                return challenge

        # Generate new weekly challenge if none active
        return self._generate_weekly_challenge()

    def update_challenge_progress(self, event: dict) -> Optional[dict]:
        """
        Update progress on active challenges.

        Args:
            event: Event that occurred

        Returns:
            Challenge completion info if completed
        """
        challenge = self.get_current_challenge()
        if not challenge:
            return None

        # Update progress based on event type
        if event.get("type") == "exercise_completed":
            challenge.progress["exercises_completed"] = \
                challenge.progress.get("exercises_completed", 0) + 1

            if event.get("score") == 100:
                challenge.progress["perfect_scores"] = \
                    challenge.progress.get("perfect_scores", 0) + 1

            if event.get("attempts") == 1 and event.get("score", 0) >= 60:
                challenge.progress["first_try_passes"] = \
                    challenge.progress.get("first_try_passes", 0) + 1

        elif event.get("type") == "session_ended":
            challenge.progress["study_minutes"] = \
                challenge.progress.get("study_minutes", 0) + event.get("duration_minutes", 0)

        elif event.get("type") == "review_completed":
            challenge.progress["reviews_completed"] = \
                challenge.progress.get("reviews_completed", 0) + 1

        # Check completion
        completed = all(
            challenge.progress.get(key, 0) >= value
            for key, value in challenge.requirements.items()
        )

        if completed and not challenge.completed:
            challenge.completed = True
            self.completed_challenges.append(challenge.challenge_id)
            self.xp += challenge.reward_xp

            # Check for challenge badges
            if "weekly_champion" not in self.earned_badges:
                self._earn_badge("weekly_champion")

            consecutive = self._count_consecutive_challenges()
            if consecutive >= 4 and "challenge_streak" not in self.earned_badges:
                self._earn_badge("challenge_streak")

            self._save_data()

            return {
                "completed": True,
                "challenge": challenge.to_dict(),
                "xp_earned": challenge.reward_xp,
                "total_xp": self.xp,
            }

        self._save_data()
        return None

    def check_personal_best(self, category: str, value: float, context: str) -> Optional[PersonalBest]:
        """
        Check if a value is a new personal best.

        Args:
            category: Category of the record (e.g., "highest_score", "fastest_completion")
            value: The value achieved
            context: What was being done

        Returns:
            PersonalBest if new record, None otherwise
        """
        current_best = self.personal_bests.get(category)

        is_new_best = (
            current_best is None or
            (category.startswith("highest") and value > current_best.value) or
            (category.startswith("fastest") and value < current_best.value) or
            (category.startswith("longest") and value > current_best.value)
        )

        if is_new_best:
            new_best = PersonalBest(
                category=category,
                value=value,
                achieved_at=datetime.now(),
                context=context,
            )
            self.personal_bests[category] = new_best
            self._save_data()
            return new_best

        return None

    def get_progress_summary(self) -> dict:
        """Get a summary of gamification progress."""
        return {
            "level": self.level,
            "xp": self.xp,
            "xp_to_next_level": self._xp_for_level(self.level + 1) - self.xp,
            "badges_earned": len(self.earned_badges),
            "total_badges": len(self.BADGE_DEFINITIONS),
            "challenges_completed": len(self.completed_challenges),
            "current_challenge": self.get_current_challenge().to_dict() if self.get_current_challenge() else None,
            "recent_badges": [
                b.to_dict() for b in sorted(
                    self.earned_badges.values(),
                    key=lambda x: x.earned_at or datetime.min,
                    reverse=True
                )[:5]
            ],
            "personal_bests": {k: v.to_dict() for k, v in self.personal_bests.items()},
        }

    def get_all_badges(self) -> dict:
        """Get all badges with their status."""
        all_badges = {}

        for badge_id, badge_def in self.BADGE_DEFINITIONS.items():
            if badge_id in self.earned_badges:
                all_badges[badge_id] = self.earned_badges[badge_id].to_dict()
            else:
                # Show unearned badge with progress
                badge = Badge(
                    badge_id=badge_def.badge_id,
                    name=badge_def.name,
                    description=badge_def.description,
                    category=badge_def.category,
                    rarity=badge_def.rarity,
                    icon=badge_def.icon,
                    requirement=badge_def.requirement,
                )
                badge.progress = self._calculate_badge_progress(badge_id)
                all_badges[badge_id] = badge.to_dict()

        return all_badges

    def get_milestones(self) -> list[Milestone]:
        """Get progress towards major milestones."""
        stats = self.progress.get("statistics", {})
        total_exercises = stats.get("total_exercises_completed", 0)
        streak = stats.get("streak_days", 0)

        milestones = [
            Milestone(
                "exercises_10", "10 Exercises", "Complete 10 exercises",
                10, min(10, total_exercises), total_exercises >= 10,
                None  # Would need to track when reached
            ),
            Milestone(
                "exercises_50", "50 Exercises", "Complete 50 exercises",
                50, min(50, total_exercises), total_exercises >= 50,
                None
            ),
            Milestone(
                "exercises_100", "100 Exercises", "Complete 100 exercises",
                100, min(100, total_exercises), total_exercises >= 100,
                None
            ),
            Milestone(
                "streak_7", "Week Streak", "Maintain a 7-day streak",
                7, min(7, streak), streak >= 7,
                None
            ),
            Milestone(
                "streak_30", "Month Streak", "Maintain a 30-day streak",
                30, min(30, streak), streak >= 30,
                None
            ),
        ]

        return milestones

    def _earn_badge(self, badge_id: str) -> Optional[Badge]:
        """Award a badge to the student."""
        if badge_id not in self.BADGE_DEFINITIONS:
            return None

        badge_def = self.BADGE_DEFINITIONS[badge_id]
        badge = Badge(
            badge_id=badge_def.badge_id,
            name=badge_def.name,
            description=badge_def.description,
            category=badge_def.category,
            rarity=badge_def.rarity,
            icon=badge_def.icon,
            requirement=badge_def.requirement,
            earned_at=datetime.now(),
            progress=1.0,
        )

        self.earned_badges[badge_id] = badge

        # Award XP based on rarity
        xp_rewards = {
            BadgeRarity.COMMON: 10,
            BadgeRarity.UNCOMMON: 25,
            BadgeRarity.RARE: 50,
            BadgeRarity.EPIC: 100,
            BadgeRarity.LEGENDARY: 250,
        }
        self.xp += xp_rewards.get(badge.rarity, 10)

        # Check for level up
        self._check_level_up()

        return badge

    def _calculate_badge_progress(self, badge_id: str) -> float:
        """Calculate progress towards a badge."""
        stats = self.progress.get("statistics", {})

        progress_calcs = {
            "first_exercise": stats.get("total_exercises_completed", 0) / 1,
            "ten_exercises": stats.get("total_exercises_completed", 0) / 10,
            "fifty_exercises": stats.get("total_exercises_completed", 0) / 50,
            "hundred_exercises": stats.get("total_exercises_completed", 0) / 100,
            "streak_3": stats.get("streak_days", 0) / 3,
            "streak_7": stats.get("streak_days", 0) / 7,
            "streak_30": stats.get("streak_days", 0) / 30,
            "streak_100": stats.get("streak_days", 0) / 100,
        }

        return min(1.0, progress_calcs.get(badge_id, 0))

    def _generate_weekly_challenge(self) -> Challenge:
        """Generate a new weekly challenge."""
        template = random.choice(self.WEEKLY_CHALLENGES)

        # Start from Monday of current week
        today = datetime.now()
        monday = today - timedelta(days=today.weekday())
        monday = monday.replace(hour=0, minute=0, second=0, microsecond=0)
        sunday = monday + timedelta(days=6, hours=23, minutes=59, seconds=59)

        challenge = Challenge(
            challenge_id=f"weekly_{monday.strftime('%Y%m%d')}",
            name=template["name"],
            description=template["description"],
            challenge_type="weekly",
            requirements=template["requirements"],
            reward_badge=None,
            reward_xp=template["reward_xp"],
            start_date=monday,
            end_date=sunday,
        )

        self.active_challenges.append(challenge)
        return challenge

    def _update_challenges(self, event: dict) -> None:
        """Update all active challenges based on event."""
        self.update_challenge_progress(event)

    def _count_consecutive_challenges(self) -> int:
        """Count consecutive completed weekly challenges."""
        # Simplified - would need proper date tracking
        return len([c for c in self.completed_challenges if c.startswith("weekly_")])

    def _check_level_up(self) -> bool:
        """Check and apply level up if XP threshold reached."""
        while self.xp >= self._xp_for_level(self.level + 1):
            self.level += 1
        return True

    def _xp_for_level(self, level: int) -> int:
        """Calculate XP required for a level."""
        # Simple exponential curve
        return int(100 * (level ** 1.5))

    def _load_data(self) -> None:
        """Load gamification data from storage."""
        if not self.storage_path.exists():
            return

        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.xp = data.get("xp", 0)
            self.level = data.get("level", 1)
            self.completed_challenges = data.get("completed_challenges", [])

            for badge_data in data.get("earned_badges", []):
                badge = Badge(
                    badge_id=badge_data["badge_id"],
                    name=badge_data["name"],
                    description=badge_data["description"],
                    category=BadgeCategory(badge_data["category"]),
                    rarity=BadgeRarity(badge_data["rarity"]),
                    icon=badge_data["icon"],
                    requirement=badge_data.get("requirement", ""),
                    earned_at=datetime.fromisoformat(badge_data["earned_at"]) if badge_data.get("earned_at") else None,
                    progress=1.0,
                )
                self.earned_badges[badge.badge_id] = badge

            for pb_data in data.get("personal_bests", {}).values():
                pb = PersonalBest(
                    category=pb_data["category"],
                    value=pb_data["value"],
                    achieved_at=datetime.fromisoformat(pb_data["achieved_at"]),
                    context=pb_data["context"],
                )
                self.personal_bests[pb.category] = pb

        except (json.JSONDecodeError, KeyError, ValueError):
            pass

    def _save_data(self) -> None:
        """Save gamification data to storage."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "xp": self.xp,
            "level": self.level,
            "earned_badges": [b.to_dict() for b in self.earned_badges.values()],
            "completed_challenges": self.completed_challenges,
            "personal_bests": {k: v.to_dict() for k, v in self.personal_bests.items()},
            "active_challenges": [c.to_dict() for c in self.active_challenges],
            "updated_at": datetime.now().isoformat(),
        }

        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
