"""
Adaptive Learning Engine

This module provides intelligent learning features including:
- Skill gap analysis
- Knowledge graph
- Spaced repetition
- Learning style adaptation
- Performance analytics
- Personalized recommendations
- Structured evaluation (multiple types)
- Misconception tracking
- Dynamic prerequisites
- Gamification (badges, challenges, milestones)
- Export/Import progress

The engine adapts to individual learning patterns and optimizes
the learning path for each student.
"""

from .adaptive_engine import AdaptiveLearningEngine
from .skill_analyzer import SkillAnalyzer, SkillGap
from .knowledge_graph import KnowledgeGraph, Topic, Prerequisite
from .spaced_repetition import SpacedRepetitionSystem, ReviewItem
from .learning_styles import LearningStyleAnalyzer, LearningStyle
from .analytics import LearningAnalytics, PerformanceMetrics
from .recommendations import RecommendationEngine, Recommendation
from .evaluation import EvaluationEngine, ExerciseType, EvaluationResult
from .misconceptions import MisconceptionTracker, Misconception, MisconceptionSeverity
from .prerequisites import PrerequisiteManager, TopicReadiness, LearningPath
from .gamification import GamificationEngine, Badge, Challenge, Milestone
from .export_import import ProgressExporter, ProgressImporter, ExportFormat

__all__ = [
    # Core engine
    "AdaptiveLearningEngine",
    # Skill analysis
    "SkillAnalyzer",
    "SkillGap",
    # Knowledge graph
    "KnowledgeGraph",
    "Topic",
    "Prerequisite",
    # Spaced repetition
    "SpacedRepetitionSystem",
    "ReviewItem",
    # Learning styles
    "LearningStyleAnalyzer",
    "LearningStyle",
    # Analytics
    "LearningAnalytics",
    "PerformanceMetrics",
    # Recommendations
    "RecommendationEngine",
    "Recommendation",
    # Evaluation
    "EvaluationEngine",
    "ExerciseType",
    "EvaluationResult",
    # Misconceptions
    "MisconceptionTracker",
    "Misconception",
    "MisconceptionSeverity",
    # Prerequisites
    "PrerequisiteManager",
    "TopicReadiness",
    "LearningPath",
    # Gamification
    "GamificationEngine",
    "Badge",
    "Challenge",
    "Milestone",
    # Export/Import
    "ProgressExporter",
    "ProgressImporter",
    "ExportFormat",
]
