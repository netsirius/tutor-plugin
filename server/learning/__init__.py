"""
Adaptive Learning Engine

This module provides intelligent learning features including:
- Skill gap analysis
- Spaced repetition (SM-2 algorithm)
- Performance analytics
- Personalized recommendations
- Structured evaluation (multiple types)
- Misconception tracking
- Dynamic prerequisites
- Export/Import progress

The engine adapts to individual learning patterns and optimizes
the learning path for each student.
"""

from .adaptive_engine import AdaptiveLearningEngine
from .skill_analyzer import SkillAnalyzer, SkillGap
from .spaced_repetition import SpacedRepetitionSystem, ReviewItem
from .analytics import LearningAnalytics, PerformanceMetrics
from .recommendations import RecommendationEngine, Recommendation
from .evaluation import EvaluationEngine, ExerciseType, EvaluationResult
from .misconceptions import MisconceptionTracker, Misconception, MisconceptionSeverity
from .prerequisites import PrerequisiteManager, TopicReadiness, LearningPath
from .export_import import ProgressExporter, ProgressImporter, ExportFormat

__all__ = [
    # Core engine
    "AdaptiveLearningEngine",
    # Skill analysis
    "SkillAnalyzer",
    "SkillGap",
    # Spaced repetition
    "SpacedRepetitionSystem",
    "ReviewItem",
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
    # Export/Import
    "ProgressExporter",
    "ProgressImporter",
    "ExportFormat",
]
