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
- University context management
- Dynamic study planning
- Exam preparation
- Calendar export

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

# University and planning modules
from .university_context import (
    UniversityContextManager,
    UniversityConfig,
    LearningContext,
    LearningStyle,
    StudyPace,
    TopicStatus,
    Subject,
    ExamInfo,
    SyllabusUnit,
    LearnerProfile,
)
from .study_planner import (
    StudyPlanner,
    StudyPlan,
    StudySession,
    DailyPlan,
    SessionType,
    PlanAdjustmentType,
)
from .exam_preparation import (
    ExamPreparationEngine,
    ExamSimulation,
    ExamPrepMode,
    ExamPrepPlan,
    QuestionType,
)
from .calendar_export import (
    CalendarExporter,
    CalendarEvent,
    CalendarExport,
    CalendarProvider,
    EventType,
)

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
    # University context
    "UniversityContextManager",
    "UniversityConfig",
    "LearningContext",
    "LearningStyle",
    "StudyPace",
    "TopicStatus",
    "Subject",
    "ExamInfo",
    "SyllabusUnit",
    "LearnerProfile",
    # Study planning
    "StudyPlanner",
    "StudyPlan",
    "StudySession",
    "DailyPlan",
    "SessionType",
    "PlanAdjustmentType",
    # Exam preparation
    "ExamPreparationEngine",
    "ExamSimulation",
    "ExamPrepMode",
    "ExamPrepPlan",
    "QuestionType",
    # Calendar export
    "CalendarExporter",
    "CalendarEvent",
    "CalendarExport",
    "CalendarProvider",
    "EventType",
]
