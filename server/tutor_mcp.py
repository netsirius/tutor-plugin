#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "fastmcp>=2.0.0",
# ]
# ///
"""
Tutor MCP Server

Provides tools for the Tutor plugin to manage learning progress
and interact with the curriculum.

Supports:
- Progress tracking and curriculum management
- Adaptive learning with skill gap analysis
- Spaced repetition (SM-2) for knowledge retention
- Misconception tracking
- Prerequisites verification
- Comprehensive analytics

Run with uv (recommended - no venv needed):
    uv run tutor_mcp.py

Or with pip:
    pip install fastmcp
    python tutor_mcp.py
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

from fastmcp import FastMCP

# Add the server directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Initialize the MCP server
mcp = FastMCP("tutor-tools")

# Get paths
PLUGIN_ROOT = Path(os.environ.get("TUTOR_PLUGIN_ROOT", Path(__file__).parent.parent))


def get_tutor_path() -> Path:
    """Get the .tutor directory path in current working directory."""
    return Path.cwd() / ".tutor"


def load_json(filepath: Path) -> dict:
    """Load a JSON file."""
    if not filepath.exists():
        return {}
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(filepath: Path, data: dict):
    """Save data to a JSON file."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ============================================================================
# PROGRESS TOOLS
# ============================================================================

@mcp.tool()
def get_student_progress() -> dict:
    """
    Get the current student's learning progress.

    Returns a dictionary with:
    - config: Course configuration
    - progress: Detailed progress including modules and exercises
    - statistics: Overall stats (time spent, scores, streak)
    - has_curriculum: Whether a curriculum is loaded
    """
    tutor_path = get_tutor_path()

    config = load_json(tutor_path / "config.json")
    progress = load_json(tutor_path / "progress.json")
    curriculum = load_json(tutor_path / "curriculum.json")

    return {
        "has_active_course": bool(config),
        "config": config,
        "progress": progress,
        "has_curriculum": bool(curriculum.get("modules")),
        "current_module": progress.get("current_module"),
        "current_topic": progress.get("current_topic"),
        "statistics": progress.get("statistics", {})
    }


@mcp.tool()
def update_exercise_progress(
    module_id: str,
    exercise_id: str,
    status: str,
    score: int = 0,
    attempts: int = 1
) -> dict:
    """
    Update the progress for a specific exercise.

    Args:
        module_id: The module containing the exercise (e.g., "02-ownership")
        exercise_id: The exercise identifier (e.g., "ex01_borrowing")
        status: Either "in_progress" or "completed"
        score: Score achieved (0-100), only relevant if completed
        attempts: Number of attempts made

    Returns:
        Updated progress summary
    """
    tutor_path = get_tutor_path()
    progress_file = tutor_path / "progress.json"
    progress = load_json(progress_file)

    if "modules" not in progress:
        progress["modules"] = {}

    if module_id not in progress["modules"]:
        progress["modules"][module_id] = {
            "status": "in_progress",
            "started_at": datetime.now().isoformat(),
            "exercises": {}
        }

    progress["modules"][module_id]["exercises"][exercise_id] = {
        "status": status,
        "updated_at": datetime.now().isoformat(),
        "attempts": attempts,
        "score": score if status == "completed" else None
    }

    # Update current position
    progress["current_module"] = module_id

    # Update statistics if completed
    if status == "completed":
        stats = progress.get("statistics", {})
        stats["total_exercises_completed"] = stats.get("total_exercises_completed", 0) + 1

        # Recalculate average
        total_score = 0
        count = 0
        for mod in progress["modules"].values():
            for ex in mod.get("exercises", {}).values():
                if ex.get("status") == "completed" and ex.get("score"):
                    total_score += ex["score"]
                    count += 1

        if count > 0:
            stats["average_score"] = round(total_score / count, 1)

        progress["statistics"] = stats

    save_json(progress_file, progress)

    return {
        "success": True,
        "module": module_id,
        "exercise": exercise_id,
        "status": status,
        "new_average": progress.get("statistics", {}).get("average_score", 0)
    }


@mcp.tool()
def get_next_lesson() -> dict:
    """
    Get the recommended next lesson based on current progress.

    Returns the next module and topic to study, considering:
    - Completed prerequisites
    - Current progress
    - Areas needing reinforcement
    """
    tutor_path = get_tutor_path()

    progress = load_json(tutor_path / "progress.json")
    curriculum = load_json(tutor_path / "curriculum.json")

    if not curriculum.get("modules"):
        return {
            "status": "no_curriculum",
            "message": "No curriculum loaded. Please set up a curriculum first."
        }

    modules = progress.get("modules", {})

    for mod in curriculum["modules"]:
        mod_id = mod["id"]
        mod_progress = modules.get(mod_id, {})

        if mod_progress.get("status") == "completed":
            continue

        # Check prerequisites
        prereqs = mod.get("prerequisites", [])
        prereqs_met = all(
            modules.get(p, {}).get("status") == "completed"
            for p in prereqs
        )

        if not prereqs_met:
            continue

        # Find first incomplete topic/exercise
        exercises = mod.get("exercises", [])
        mod_exercises = mod_progress.get("exercises", {})

        for ex in exercises:
            if mod_exercises.get(ex["id"], {}).get("status") != "completed":
                return {
                    "status": "next_found",
                    "module_id": mod_id,
                    "module_title": mod["title"],
                    "next_item": "exercise",
                    "exercise_id": ex["id"],
                    "exercise_title": ex.get("title", ex["id"]),
                    "difficulty": ex.get("difficulty", "unknown"),
                    "related_topics": ex.get("topics", [])
                }

        # All exercises done, suggest completing module
        return {
            "status": "module_ready_to_complete",
            "module_id": mod_id,
            "module_title": mod["title"],
            "message": "All exercises completed. Ready to mark module as complete."
        }

    return {
        "status": "curriculum_complete",
        "message": "Congratulations! You have completed the entire curriculum!"
    }


# ============================================================================
# CURRICULUM TOOLS
# ============================================================================

@mcp.tool()
def get_curriculum() -> dict:
    """
    Get the current curriculum structure.

    Returns the full curriculum with modules, topics, and exercises.
    """
    tutor_path = get_tutor_path()
    curriculum = load_json(tutor_path / "curriculum.json")

    if not curriculum:
        return {
            "status": "no_curriculum",
            "message": "No curriculum loaded yet."
        }

    return {
        "status": "loaded",
        "curriculum": curriculum
    }


@mcp.tool()
def save_curriculum(curriculum_data: str) -> dict:
    """
    Save a new curriculum.

    Args:
        curriculum_data: JSON string containing the curriculum structure

    Returns:
        Success status and summary of the curriculum
    """
    tutor_path = get_tutor_path()
    tutor_path.mkdir(parents=True, exist_ok=True)

    try:
        curriculum = json.loads(curriculum_data)
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"Invalid JSON: {str(e)}"
        }

    # Validate basic structure
    if "modules" not in curriculum:
        return {
            "success": False,
            "error": "Curriculum must have a 'modules' array"
        }

    save_json(tutor_path / "curriculum.json", curriculum)

    # Count exercises
    total_exercises = 0
    for m in curriculum["modules"]:
        exercises = m.get("exercises", 0)
        if isinstance(exercises, int):
            total_exercises += exercises
        elif isinstance(exercises, list):
            total_exercises += len(exercises)

    return {
        "success": True,
        "title": curriculum.get("title", "Untitled"),
        "language": curriculum.get("language", "unknown"),
        "modules_count": len(curriculum["modules"]),
        "total_exercises": total_exercises
    }


# ============================================================================
# SESSION TOOLS
# ============================================================================

@mcp.tool()
def start_study_session() -> dict:
    """
    Start a new study session. Records the start time and updates streak.

    Returns session info including current streak.
    """
    tutor_path = get_tutor_path()
    progress_file = tutor_path / "progress.json"
    progress = load_json(progress_file)

    today = datetime.now().strftime("%Y-%m-%d")
    stats = progress.get("statistics", {})

    # Update streak
    last_session = stats.get("last_session")
    if last_session:
        last_date = datetime.strptime(last_session, "%Y-%m-%d")
        today_date = datetime.strptime(today, "%Y-%m-%d")
        diff = (today_date - last_date).days

        if diff == 1:
            stats["streak_days"] = stats.get("streak_days", 0) + 1
        elif diff > 1:
            stats["streak_days"] = 1
    else:
        stats["streak_days"] = 1

    stats["last_session"] = today
    progress["statistics"] = stats
    save_json(progress_file, progress)

    # Create session file
    sessions_dir = tutor_path / "sessions"
    sessions_dir.mkdir(exist_ok=True)

    session = {
        "date": today,
        "started_at": datetime.now().isoformat(),
        "topics_covered": [],
        "exercises_completed": []
    }
    save_json(sessions_dir / f"{today}.json", session)

    return {
        "success": True,
        "date": today,
        "streak": stats["streak_days"],
        "message": f"Session started! Current streak: {stats['streak_days']} days"
    }


@mcp.tool()
def end_study_session(topics_covered: list[str], exercises_completed: list[str]) -> dict:
    """
    End the current study session.

    Args:
        topics_covered: List of topic IDs covered in this session
        exercises_completed: List of exercise IDs completed in this session

    Returns session summary including duration.
    """
    tutor_path = get_tutor_path()
    today = datetime.now().strftime("%Y-%m-%d")

    session_file = tutor_path / "sessions" / f"{today}.json"
    session = load_json(session_file)

    if not session:
        return {
            "success": False,
            "error": "No active session found for today"
        }

    session["ended_at"] = datetime.now().isoformat()
    session["topics_covered"] = topics_covered
    session["exercises_completed"] = exercises_completed

    # Calculate duration
    if session.get("started_at"):
        start = datetime.fromisoformat(session["started_at"])
        end = datetime.now()
        duration_minutes = int((end - start).total_seconds() / 60)
        session["duration_minutes"] = duration_minutes

        # Update total time
        progress_file = tutor_path / "progress.json"
        progress = load_json(progress_file)
        stats = progress.get("statistics", {})
        stats["total_time_minutes"] = stats.get("total_time_minutes", 0) + duration_minutes
        progress["statistics"] = stats
        save_json(progress_file, progress)

    save_json(session_file, session)

    return {
        "success": True,
        "duration_minutes": session.get("duration_minutes", 0),
        "topics_covered": len(topics_covered),
        "exercises_completed": len(exercises_completed),
        "total_study_time_hours": round(
            load_json(tutor_path / "progress.json").get("statistics", {}).get("total_time_minutes", 0) / 60,
            1
        )
    }


# ============================================================================
# SPACED REPETITION TOOLS (SM-2)
# ============================================================================

@mcp.tool()
def get_spaced_repetition_items() -> dict:
    """
    Get items due for spaced repetition review.

    Returns:
        Items due for review and SRS statistics
    """
    try:
        from learning import SpacedRepetitionSystem

        srs = SpacedRepetitionSystem(get_tutor_path() / "srs.json")
        due_items = srs.get_due_items()
        stats = srs.get_statistics()

        return {
            "success": True,
            "due_items": [item.to_dict() for item in due_items],
            "statistics": stats,
        }
    except ImportError:
        return {
            "success": False,
            "error": "Spaced repetition module not available",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


@mcp.tool()
def record_srs_review(item_id: str, quality: int) -> dict:
    """
    Record a spaced repetition review result.

    Args:
        item_id: ID of the item reviewed
        quality: Quality of recall (0-5)
            - 0: Complete blackout
            - 1: Incorrect, remembered upon seeing answer
            - 2: Incorrect, but answer seemed easy
            - 3: Correct with serious difficulty
            - 4: Correct after hesitation
            - 5: Perfect response

    Returns:
        Updated item schedule
    """
    try:
        from learning import SpacedRepetitionSystem

        srs = SpacedRepetitionSystem(get_tutor_path() / "srs.json")
        item = srs.record_review(item_id, quality)

        return {
            "success": True,
            "item": item.to_dict(),
            "next_review": item.next_review.isoformat() if item.next_review else None,
        }
    except ImportError:
        return {
            "success": False,
            "error": "Spaced repetition module not available",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


# ============================================================================
# ADAPTIVE LEARNING TOOLS
# ============================================================================

@mcp.tool()
def get_skill_gaps() -> dict:
    """
    Analyze current skills and identify gaps for improvement.

    Returns skill assessments, gaps, and recommended learning path.
    """
    try:
        from learning import AdaptiveLearningEngine

        engine = AdaptiveLearningEngine(get_tutor_path())
        skills = engine.skill_analyzer.analyze_all_skills()
        gaps = engine.skill_analyzer.identify_gaps()
        strengths = engine.skill_analyzer.get_strengths()

        return {
            "success": True,
            "total_skills_assessed": len(skills),
            "skill_levels": {s.skill_id: s.to_dict() for s in skills.values()},
            "gaps": [g.to_dict() for g in gaps[:10]],
            "strengths": [s.to_dict() for s in strengths[:5]],
        }
    except ImportError:
        return {
            "success": False,
            "error": "Adaptive learning module not available",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


@mcp.tool()
def get_learning_recommendations(available_minutes: int = 60, context: str = "general") -> dict:
    """
    Get personalized learning recommendations.

    Args:
        available_minutes: Time available for study
        context: Study context - "general", "quick_practice", "deep_learning", or "review"

    Returns:
        List of personalized recommendations
    """
    try:
        from learning import AdaptiveLearningEngine

        engine = AdaptiveLearningEngine(get_tutor_path())
        recommendations = engine.get_recommendations(available_minutes, context)

        return {
            "success": True,
            "context": context,
            "available_minutes": available_minutes,
            "recommendations": [r.to_dict() for r in recommendations],
        }
    except ImportError:
        return {
            "success": False,
            "error": "Adaptive learning module not available",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


@mcp.tool()
def get_learning_analytics() -> dict:
    """
    Get comprehensive learning analytics and insights.

    Returns:
        Performance metrics, trends, and improvement suggestions
    """
    try:
        from learning import AdaptiveLearningEngine

        engine = AdaptiveLearningEngine(get_tutor_path())
        report = engine.get_comprehensive_report()

        return {
            "success": True,
            **report,
        }
    except ImportError:
        return {
            "success": False,
            "error": "Analytics module not available",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


@mcp.tool()
def start_adaptive_session() -> dict:
    """
    Start an adaptive learning session.

    Returns:
        Session info, recommendations, and personalized content settings
    """
    try:
        from learning import AdaptiveLearningEngine

        engine = AdaptiveLearningEngine(get_tutor_path())
        session_info = engine.start_session()

        return {
            "success": True,
            **session_info,
        }
    except ImportError:
        # Fallback to basic session
        return start_study_session()
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


@mcp.tool()
def record_exercise_completion(
    module_id: str,
    exercise_id: str,
    score: int,
    attempts: int,
    time_spent_minutes: int
) -> dict:
    """
    Record exercise completion with full adaptive tracking.

    Updates progress, SRS, and skill assessments.

    Args:
        module_id: Module containing the exercise
        exercise_id: Exercise ID
        score: Score achieved (0-100)
        attempts: Number of attempts
        time_spent_minutes: Time spent on exercise

    Returns:
        Summary of all updates
    """
    try:
        from learning import AdaptiveLearningEngine

        engine = AdaptiveLearningEngine(get_tutor_path())
        result = engine.record_exercise_completion(
            module_id, exercise_id, score, attempts, time_spent_minutes
        )

        return {
            "success": True,
            **result,
        }
    except ImportError:
        # Fallback to basic progress update
        return update_exercise_progress(
            module_id, exercise_id,
            "completed" if score >= 60 else "in_progress",
            score, attempts
        )
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


# ============================================================================
# EVALUATION TOOLS
# ============================================================================

@mcp.tool()
def record_evaluation(
    exercise_id: str,
    exercise_type: str,
    score: int,
    feedback: str,
    detailed_feedback: str = "",
    misconceptions: list[str] = None,
    strengths: list[str] = None,
    suggestions: list[str] = None,
    time_spent_seconds: int = None,
    attempts: int = 1,
) -> dict:
    """
    Record an evaluation result for any exercise type.

    Supports: code, multiple_choice, free_text, math, translation, fill_blank, matching, etc.

    Args:
        exercise_id: Exercise identifier
        exercise_type: Type of exercise (code, multiple_choice, free_text, math, translation, etc.)
        score: Score achieved (0-100)
        feedback: Brief feedback message
        detailed_feedback: Detailed explanation
        misconceptions: List of identified misconceptions
        strengths: List of strengths shown
        suggestions: List of improvement suggestions
        time_spent_seconds: Time taken
        attempts: Number of attempts

    Returns:
        Evaluation result details
    """
    try:
        from learning import EvaluationEngine, ExerciseType

        engine = EvaluationEngine(get_tutor_path() / "evaluations.json")

        result = engine.record_evaluation(
            exercise_id=exercise_id,
            exercise_type=ExerciseType(exercise_type),
            score=score,
            feedback=feedback,
            detailed_feedback=detailed_feedback,
            misconceptions=misconceptions or [],
            strengths=strengths or [],
            suggestions=suggestions or [],
            time_spent_seconds=time_spent_seconds,
            attempts=attempts,
        )

        return {
            "success": True,
            "evaluation": result.to_dict(),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


@mcp.tool()
def get_evaluation_statistics() -> dict:
    """
    Get evaluation statistics grouped by exercise type.

    Returns:
        Statistics for each exercise type including pass rates, averages, etc.
    """
    try:
        from learning import EvaluationEngine

        engine = EvaluationEngine(get_tutor_path() / "evaluations.json")
        stats = engine.get_statistics_by_type()
        common_misconceptions = engine.get_common_misconceptions()

        return {
            "success": True,
            "statistics_by_type": stats,
            "common_misconceptions": [
                {"misconception": m, "count": c}
                for m, c in common_misconceptions
            ],
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


# ============================================================================
# MISCONCEPTION TOOLS
# ============================================================================

@mcp.tool()
def record_misconception(
    exercise_id: str,
    exercise_type: str,
    topic: str,
    error_description: str,
    student_response: str,
    correct_response: str,
    category: str = None,
) -> dict:
    """
    Record an error/misconception for tracking and analysis.

    Args:
        exercise_id: Exercise where error occurred
        exercise_type: Type of exercise
        topic: Topic being studied
        error_description: Description of the error
        student_response: What the student submitted
        correct_response: What was expected
        category: Category (programming, mathematics, language, etc.)

    Returns:
        Misconception tracking result
    """
    try:
        from learning import MisconceptionTracker

        tracker = MisconceptionTracker(get_tutor_path() / "misconceptions.json")

        misconception = tracker.record_error(
            exercise_id=exercise_id,
            exercise_type=exercise_type,
            topic=topic,
            error_description=error_description,
            student_response=student_response,
            correct_response=correct_response,
            category=category,
        )

        return {
            "success": True,
            "misconception": misconception.to_dict(),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


@mcp.tool()
def get_misconception_analysis() -> dict:
    """
    Get analysis of student misconceptions.

    Returns:
        Active misconceptions, remediation suggestions, and statistics
    """
    try:
        from learning import MisconceptionTracker

        tracker = MisconceptionTracker(get_tutor_path() / "misconceptions.json")

        active = tracker.get_active_misconceptions()
        high_priority = tracker.get_high_priority_misconceptions()
        suggestions = tracker.get_remediation_suggestions()
        stats = tracker.get_statistics()

        return {
            "success": True,
            "active_misconceptions": [m.to_dict() for m in active],
            "high_priority": [m.to_dict() for m in high_priority],
            "remediation_suggestions": [s.to_dict() for s in suggestions],
            "statistics": stats,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


@mcp.tool()
def get_topic_warning(topic: str) -> dict:
    """
    Get a warning if student has misconceptions in a topic.

    Args:
        topic: Topic about to be studied

    Returns:
        Warning message if applicable
    """
    try:
        from learning import MisconceptionTracker

        tracker = MisconceptionTracker(get_tutor_path() / "misconceptions.json")
        warning = tracker.get_warning_for_topic(topic)

        return {
            "success": True,
            "has_warning": warning is not None,
            "warning": warning,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


# ============================================================================
# PREREQUISITE TOOLS
# ============================================================================

@mcp.tool()
def check_topic_readiness(topic_id: str) -> dict:
    """
    Check if the student is ready for a topic based on prerequisites.

    Args:
        topic_id: The topic to check

    Returns:
        Readiness assessment with met/missing prerequisites
    """
    try:
        from learning import PrerequisiteManager

        progress = load_json(get_tutor_path() / "progress.json")
        curriculum = load_json(get_tutor_path() / "curriculum.json")

        manager = PrerequisiteManager(curriculum, progress, get_tutor_path() / "prerequisites.json")
        readiness = manager.check_readiness(topic_id)

        return {
            "success": True,
            "readiness": readiness.to_dict(),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


@mcp.tool()
def get_learning_path_to(target_topic: str) -> dict:
    """
    Get the optimal learning path to a target topic.

    Args:
        target_topic: The topic to learn

    Returns:
        Ordered learning path with prerequisites
    """
    try:
        from learning import PrerequisiteManager

        progress = load_json(get_tutor_path() / "progress.json")
        curriculum = load_json(get_tutor_path() / "curriculum.json")

        manager = PrerequisiteManager(curriculum, progress, get_tutor_path() / "prerequisites.json")
        path = manager.get_learning_path(target_topic)

        return {
            "success": True,
            "learning_path": path.to_dict(),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


# ============================================================================
# UNIVERSITY CONTEXT TOOLS
# ============================================================================

@mcp.tool()
def get_university_config() -> dict:
    """
    Get the university-specific configuration.

    Returns:
        University config including subject, exams, syllabus, and learner profile
    """
    tutor_path = get_tutor_path()
    config = load_json(tutor_path / "university_config.json")

    if not config:
        return {
            "success": False,
            "has_university_config": False,
            "message": "No university configuration found. Use /tutor:init to set up."
        }

    return {
        "success": True,
        "has_university_config": True,
        "config": config
    }


@mcp.tool()
def add_exam(
    name: str,
    date: str,
    exam_type: str = "final",
    weight: int = 100,
    duration_minutes: int = 120,
    topics: list[str] = None
) -> dict:
    """
    Add an exam to the university configuration.

    Args:
        name: Exam name (e.g., "Final Exam", "Midterm")
        date: Exam date in YYYY-MM-DD format
        exam_type: Type of exam (midterm, final, quiz, practice)
        weight: Weight in final grade (0-100)
        duration_minutes: Duration of the exam
        topics: List of topic IDs included in the exam

    Returns:
        Updated exam list
    """
    tutor_path = get_tutor_path()
    config = load_json(tutor_path / "university_config.json")

    if not config:
        config = {"exams": []}

    if "exams" not in config:
        config["exams"] = []

    exam = {
        "id": f"exam_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "name": name,
        "date": date,
        "type": exam_type,
        "weight": weight,
        "duration_minutes": duration_minutes,
        "topics_included": topics or [],
        "created_at": datetime.now().isoformat()
    }

    config["exams"].append(exam)
    save_json(tutor_path / "university_config.json", config)

    # Calculate days until exam
    exam_date = datetime.strptime(date, "%Y-%m-%d")
    days_until = (exam_date - datetime.now()).days

    return {
        "success": True,
        "exam": exam,
        "days_until_exam": days_until,
        "total_exams": len(config["exams"])
    }


@mcp.tool()
def add_syllabus_unit(
    name: str,
    weight: int = 10,
    estimated_hours: float = 4,
    prerequisites: list[str] = None,
    topics: list[str] = None,
    description: str = ""
) -> dict:
    """
    Add a unit to the syllabus.

    Args:
        name: Unit name (e.g., "Binary Trees", "Graphs")
        weight: Weight in exam (0-100)
        estimated_hours: Estimated study hours
        prerequisites: List of prerequisite unit IDs
        topics: List of subtopics
        description: Unit description

    Returns:
        Updated syllabus
    """
    tutor_path = get_tutor_path()
    config = load_json(tutor_path / "university_config.json")

    if not config:
        config = {"syllabus_units": []}

    if "syllabus_units" not in config:
        config["syllabus_units"] = []

    # Generate ID from name
    unit_id = f"u{len(config['syllabus_units']) + 1}-{name.lower().replace(' ', '-')[:20]}"

    unit = {
        "id": unit_id,
        "name": name,
        "description": description,
        "weight": weight,
        "estimated_hours": estimated_hours,
        "order": len(config["syllabus_units"]) + 1,
        "prerequisites": prerequisites or [],
        "topics": topics or [],
        "resources": []
    }

    config["syllabus_units"].append(unit)
    save_json(tutor_path / "university_config.json", config)

    # Update topic status
    topic_status = load_json(tutor_path / "topic_status.json") or {}
    topic_status[unit_id] = "new"
    save_json(tutor_path / "topic_status.json", topic_status)

    return {
        "success": True,
        "unit": unit,
        "total_units": len(config["syllabus_units"]),
        "total_hours": sum(u.get("estimated_hours", 0) for u in config["syllabus_units"])
    }


@mcp.tool()
def get_topic_status() -> dict:
    """
    Get the status of all topics in the syllabus.

    Returns:
        Status of each topic (new, in_progress, learned, mastered, rusty)
    """
    tutor_path = get_tutor_path()
    topic_status = load_json(tutor_path / "topic_status.json")
    config = load_json(tutor_path / "university_config.json")

    if not config or "syllabus_units" not in config:
        return {
            "success": False,
            "message": "No syllabus configured"
        }

    # Build detailed status
    units_with_status = []
    status_counts = {"new": 0, "in_progress": 0, "learned": 0, "mastered": 0, "rusty": 0}

    for unit in config["syllabus_units"]:
        status = topic_status.get(unit["id"], "new")
        status_counts[status] = status_counts.get(status, 0) + 1

        units_with_status.append({
            "id": unit["id"],
            "name": unit["name"],
            "status": status,
            "weight": unit.get("weight", 0),
            "estimated_hours": unit.get("estimated_hours", 0)
        })

    return {
        "success": True,
        "units": units_with_status,
        "summary": status_counts,
        "completion_percentage": round(
            (status_counts.get("learned", 0) + status_counts.get("mastered", 0)) /
            max(len(units_with_status), 1) * 100
        )
    }


@mcp.tool()
def update_topic_status(topic_id: str, new_status: str) -> dict:
    """
    Update the status of a topic.

    Args:
        topic_id: The topic ID to update
        new_status: New status (new, in_progress, learned, mastered, rusty, extending)

    Returns:
        Updated status
    """
    valid_statuses = ["new", "in_progress", "learned", "mastered", "rusty", "extending", "reinforcing"]

    if new_status not in valid_statuses:
        return {
            "success": False,
            "error": f"Invalid status. Must be one of: {valid_statuses}"
        }

    tutor_path = get_tutor_path()
    topic_status = load_json(tutor_path / "topic_status.json") or {}

    old_status = topic_status.get(topic_id, "new")
    topic_status[topic_id] = new_status
    save_json(tutor_path / "topic_status.json", topic_status)

    return {
        "success": True,
        "topic_id": topic_id,
        "old_status": old_status,
        "new_status": new_status
    }


# ============================================================================
# STUDY PLANNER TOOLS
# ============================================================================

@mcp.tool()
def generate_study_plan(
    hours_per_week: float = 8,
    study_days: list[str] = None,
    preferred_session_minutes: int = 45
) -> dict:
    """
    Generate a personalized study plan based on syllabus and exam dates.

    Args:
        hours_per_week: Available study hours per week
        study_days: Days available for study (e.g., ["mon", "tue", "wed"])
        preferred_session_minutes: Preferred session duration

    Returns:
        Generated study plan
    """
    try:
        from learning import StudyPlanner

        tutor_path = get_tutor_path()
        config = load_json(tutor_path / "university_config.json")

        if not config:
            return {
                "success": False,
                "error": "No university configuration found"
            }

        planner = StudyPlanner(tutor_path)
        plan = planner.generate_plan(
            hours_per_week=hours_per_week,
            study_days=study_days or ["mon", "tue", "wed", "thu", "fri"],
            session_minutes=preferred_session_minutes
        )

        return {
            "success": True,
            "plan": plan.to_dict() if hasattr(plan, 'to_dict') else plan
        }
    except ImportError:
        return {
            "success": False,
            "error": "Study planner module not available"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def get_today_plan() -> dict:
    """
    Get the study plan for today.

    Returns:
        Today's sessions and recommendations
    """
    try:
        from learning import StudyPlanner

        planner = StudyPlanner(get_tutor_path())
        today_plan = planner.get_today_plan()

        return {
            "success": True,
            "today": today_plan.to_dict() if hasattr(today_plan, 'to_dict') else today_plan
        }
    except ImportError:
        return {
            "success": False,
            "error": "Study planner module not available"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def get_week_overview() -> dict:
    """
    Get the study plan overview for the current week.

    Returns:
        Week overview with daily plans
    """
    try:
        from learning import StudyPlanner

        planner = StudyPlanner(get_tutor_path())
        week = planner.get_week_overview()

        return {
            "success": True,
            "week_overview": week
        }
    except ImportError:
        return {
            "success": False,
            "error": "Study planner module not available"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def adjust_study_plan(reason: str, adjustment_type: str = "reschedule") -> dict:
    """
    Adjust the study plan due to changes.

    Args:
        reason: Reason for adjustment (e.g., "missed_session", "exam_moved", "time_change")
        adjustment_type: Type of adjustment (reschedule, compress, extend)

    Returns:
        Adjusted plan
    """
    try:
        from learning import StudyPlanner

        planner = StudyPlanner(get_tutor_path())
        adjusted = planner.adjust_plan(reason=reason, adjustment_type=adjustment_type)

        return {
            "success": True,
            "adjusted_plan": adjusted
        }
    except ImportError:
        return {
            "success": False,
            "error": "Study planner module not available"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ============================================================================
# EXAM PREPARATION TOOLS
# ============================================================================

@mcp.tool()
def get_exam_prep_status() -> dict:
    """
    Get the current exam preparation status and mode.

    Returns:
        Exam prep status including days until exam, mode, and recommendations
    """
    try:
        from learning import ExamPreparationEngine

        engine = ExamPreparationEngine(get_tutor_path())
        status = engine.get_status()

        return {
            "success": True,
            **status
        }
    except ImportError:
        # Fallback basic implementation
        tutor_path = get_tutor_path()
        config = load_json(tutor_path / "university_config.json")

        if not config or "exams" not in config or not config["exams"]:
            return {
                "success": True,
                "has_exam": False,
                "message": "No exams configured"
            }

        # Find next exam
        now = datetime.now()
        next_exam = None
        for exam in config["exams"]:
            exam_date = datetime.strptime(exam["date"], "%Y-%m-%d")
            if exam_date > now:
                if not next_exam or exam_date < datetime.strptime(next_exam["date"], "%Y-%m-%d"):
                    next_exam = exam

        if not next_exam:
            return {
                "success": True,
                "has_exam": False,
                "message": "No upcoming exams"
            }

        days_until = (datetime.strptime(next_exam["date"], "%Y-%m-%d") - now).days

        # Determine mode
        if days_until > 14:
            mode = "FULL"
        elif days_until > 7:
            mode = "STANDARD"
        elif days_until > 3:
            mode = "INTENSIVE"
        elif days_until > 1:
            mode = "EMERGENCY"
        else:
            mode = "LAST_MINUTE"

        return {
            "success": True,
            "has_exam": True,
            "next_exam": next_exam,
            "days_until_exam": days_until,
            "mode": mode
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def create_exam_simulation(
    duration_minutes: int = 90,
    question_count: int = 25,
    topics: list[str] = None,
    question_types: dict = None
) -> dict:
    """
    Create an exam simulation.

    Args:
        duration_minutes: Duration of the simulation
        question_count: Number of questions
        topics: Specific topics to include (or all if None)
        question_types: Distribution of question types as percentages (0-100).
            Available types: multiple_choice, true_false, short_answer, long_answer,
            coding, problem_solving, fill_blank, matching.
            Example: {"multiple_choice": 40, "short_answer": 30, "coding": 30}
            If not provided, uses default: 40% multiple_choice, 30% short_answer,
            20% problem_solving, 10% true_false

    Returns:
        Simulation setup with questions
    """
    try:
        from learning import ExamPreparationEngine, QuestionType

        engine = ExamPreparationEngine(get_tutor_path())

        # Convert question_types dict to QuestionType enum
        question_distribution = None
        if question_types:
            question_distribution = {}
            type_mapping = {
                "multiple_choice": QuestionType.MULTIPLE_CHOICE,
                "true_false": QuestionType.TRUE_FALSE,
                "short_answer": QuestionType.SHORT_ANSWER,
                "long_answer": QuestionType.LONG_ANSWER,
                "coding": QuestionType.CODING,
                "problem_solving": QuestionType.PROBLEM_SOLVING,
                "fill_blank": QuestionType.FILL_BLANK,
                "matching": QuestionType.MATCHING,
            }
            for q_type, percentage in question_types.items():
                if q_type in type_mapping:
                    question_distribution[type_mapping[q_type]] = percentage / 100.0

        # Get topics from config if not provided
        tutor_path = get_tutor_path()
        if not topics:
            config = load_json(tutor_path / "university_config.json")
            if config and "syllabus_units" in config:
                topics = config["syllabus_units"]
            else:
                topics = [{"id": "general", "name": "General", "weight": 100}]
        elif isinstance(topics, list) and topics and isinstance(topics[0], str):
            # Convert topic IDs to topic dicts
            config = load_json(tutor_path / "university_config.json")
            if config and "syllabus_units" in config:
                topic_map = {u["id"]: u for u in config["syllabus_units"]}
                topics = [topic_map.get(t, {"id": t, "name": t, "weight": 10}) for t in topics]

        simulation = engine.create_simulation(
            name=f"Simulacro {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            duration_minutes=duration_minutes,
            topics=topics,
            question_distribution=question_distribution
        )

        return {
            "success": True,
            "simulation": simulation.to_dict() if hasattr(simulation, 'to_dict') else simulation,
            "question_types_used": {
                k.value: f"{v*100:.0f}%"
                for k, v in (question_distribution or {
                    QuestionType.MULTIPLE_CHOICE: 0.4,
                    QuestionType.SHORT_ANSWER: 0.3,
                    QuestionType.PROBLEM_SOLVING: 0.2,
                    QuestionType.TRUE_FALSE: 0.1,
                }).items()
            }
        }
    except ImportError:
        return {
            "success": False,
            "error": "Exam preparation module not available"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def get_simulation_results(simulation_id: str) -> dict:
    """
    Get the results of a completed exam simulation.

    Args:
        simulation_id: ID of the simulation

    Returns:
        Detailed results and analysis
    """
    try:
        from learning import ExamPreparationEngine

        engine = ExamPreparationEngine(get_tutor_path())
        results = engine.get_simulation_results(simulation_id)

        return {
            "success": True,
            "results": results
        }
    except ImportError:
        return {
            "success": False,
            "error": "Exam preparation module not available"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ============================================================================
# CALENDAR EXPORT TOOLS
# ============================================================================

@mcp.tool()
def export_to_calendar(
    provider: str = "ics",
    include_sessions: bool = True,
    include_exams: bool = True,
    include_reminders: bool = True
) -> dict:
    """
    Export study plan to calendar format.

    Args:
        provider: Calendar provider (ics, google, apple, outlook)
        include_sessions: Include study sessions
        include_exams: Include exam dates
        include_reminders: Add reminder notifications

    Returns:
        Export result with file path or URLs
    """
    try:
        from learning import CalendarExporter

        exporter = CalendarExporter(get_tutor_path())
        result = exporter.export(
            provider=provider,
            include_sessions=include_sessions,
            include_exams=include_exams,
            include_reminders=include_reminders
        )

        return {
            "success": True,
            "export": result.to_dict() if hasattr(result, 'to_dict') else result
        }
    except ImportError:
        return {
            "success": False,
            "error": "Calendar export module not available"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def get_calendar_events(days_ahead: int = 7) -> dict:
    """
    Get upcoming calendar events for the study plan.

    Args:
        days_ahead: Number of days to look ahead

    Returns:
        List of upcoming events
    """
    try:
        from learning import CalendarExporter

        exporter = CalendarExporter(get_tutor_path())
        events = exporter.get_upcoming_events(days_ahead=days_ahead)

        return {
            "success": True,
            "events": [e.to_dict() if hasattr(e, 'to_dict') else e for e in events]
        }
    except ImportError:
        return {
            "success": False,
            "error": "Calendar export module not available"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ============================================================================
# LEARNING STYLE TOOLS
# ============================================================================

@mcp.tool()
def get_learning_style() -> dict:
    """
    Get the detected learning style profile.

    Returns:
        Learning style analysis and content recommendations
    """
    try:
        from learning import AdaptiveLearningEngine

        engine = AdaptiveLearningEngine(get_tutor_path())
        style = engine.learning_style_detector.get_profile()

        return {
            "success": True,
            "learning_style": style.to_dict() if hasattr(style, 'to_dict') else style
        }
    except ImportError:
        # Fallback to config
        tutor_path = get_tutor_path()
        config = load_json(tutor_path / "config.json")
        uni_config = load_json(tutor_path / "university_config.json")

        style = (
            uni_config.get("learner_profile", {}).get("style") or
            config.get("preferences", {}).get("learning_style") or
            "auto_detect"
        )

        return {
            "success": True,
            "learning_style": {
                "primary": style,
                "detected": style != "auto_detect"
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def update_learning_style(style: str) -> dict:
    """
    Update the preferred learning style.

    Args:
        style: Learning style (visual, practical, theoretical, mixed, auto_detect)

    Returns:
        Updated configuration
    """
    valid_styles = ["visual", "practical", "theoretical", "mixed", "auto_detect"]

    if style not in valid_styles:
        return {
            "success": False,
            "error": f"Invalid style. Must be one of: {valid_styles}"
        }

    tutor_path = get_tutor_path()

    # Update both configs
    config = load_json(tutor_path / "config.json") or {}
    if "preferences" not in config:
        config["preferences"] = {}
    config["preferences"]["learning_style"] = style
    save_json(tutor_path / "config.json", config)

    uni_config = load_json(tutor_path / "university_config.json")
    if uni_config:
        if "learner_profile" not in uni_config:
            uni_config["learner_profile"] = {}
        uni_config["learner_profile"]["style"] = style
        save_json(tutor_path / "university_config.json", uni_config)

    return {
        "success": True,
        "learning_style": style
    }


# ============================================================================
# GAMIFICATION TOOLS
# ============================================================================

@mcp.tool()
def check_achievements(event_type: str, event_details: dict = None) -> dict:
    """
    Check for new achievements based on an event.

    Args:
        event_type: Type of event (exercise_completed, session_started, etc.)
        event_details: Additional event details (score, attempts, time_minutes, etc.)

    Returns:
        Newly earned badges and challenge updates
    """
    try:
        from learning import GamificationEngine

        engine = GamificationEngine(get_tutor_path() / "gamification.json")
        result = engine.check_achievements(event_type, event_details or {})

        return {
            "success": True,
            **result
        }
    except ImportError:
        return {
            "success": True,
            "new_badges": [],
            "challenges_updated": []
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def get_gamification_progress() -> dict:
    """
    Get gamification progress summary.

    Returns:
        Level, XP, badges, challenges, milestones, and personal bests
    """
    try:
        from learning import GamificationEngine

        engine = GamificationEngine(get_tutor_path() / "gamification.json")
        progress = engine.get_progress()

        return {
            "success": True,
            **progress
        }
    except ImportError:
        return {
            "success": True,
            "level": 1,
            "xp": 0,
            "badges": [],
            "challenges": []
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def get_current_challenge() -> dict:
    """
    Get the current active weekly challenge.

    Returns:
        Challenge details and progress
    """
    try:
        from learning import GamificationEngine

        engine = GamificationEngine(get_tutor_path() / "gamification.json")
        challenge = engine.get_current_challenge()

        return {
            "success": True,
            "challenge": challenge
        }
    except ImportError:
        return {
            "success": True,
            "challenge": None,
            "message": "No active challenge"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ============================================================================
# EXPORT/IMPORT TOOLS
# ============================================================================

@mcp.tool()
def export_progress(
    format: str = "json",
    include_sessions: bool = True,
    include_evaluations: bool = True
) -> dict:
    """
    Export learning progress to a file.

    Args:
        format: Export format (json, json.gz, md, tutor)
        include_sessions: Include session history
        include_evaluations: Include evaluation history

    Returns:
        Export result with file path
    """
    try:
        from learning import ProgressExporter, ExportFormat

        exporter = ProgressExporter(get_tutor_path())
        result = exporter.export(format=ExportFormat(format))

        return {
            "success": True,
            "export": result.to_dict(),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


@mcp.tool()
def import_progress(
    filepath: str,
    merge_strategy: str = "newer_wins",
    create_backup: bool = True
) -> dict:
    """
    Import learning progress from a file.

    Args:
        filepath: Path to import file
        merge_strategy: How to handle conflicts (newer_wins, import_wins, existing_wins, merge)
        create_backup: Create backup before import

    Returns:
        Import result with details
    """
    try:
        from learning import ProgressImporter
        from pathlib import Path

        importer = ProgressImporter(get_tutor_path())
        result = importer.import_progress(
            filepath=Path(filepath),
            merge_strategy=merge_strategy,
            create_backup=create_backup
        )

        return {
            "success": result.success,
            "import_result": result.to_dict(),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


@mcp.tool()
def validate_import_file(filepath: str) -> dict:
    """
    Validate an import file without importing.

    Args:
        filepath: Path to import file

    Returns:
        Validation result with preview
    """
    try:
        from learning import ProgressImporter
        from pathlib import Path

        importer = ProgressImporter(get_tutor_path())
        result = importer.validate(filepath=Path(filepath))

        return {
            "success": True,
            "validation": result.to_dict() if hasattr(result, 'to_dict') else result,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


# ============================================================================
# PROJECT-BASED LEARNING TOOLS
# ============================================================================

@mcp.tool()
def get_project_status() -> dict:
    """
    Get the current project status for project-based learning context.

    Returns:
        Project info including name, objective, milestones, and current progress
    """
    tutor_path = get_tutor_path()
    config = load_json(tutor_path / "config.json")
    university_config = load_json(tutor_path / "university_config.json")
    topic_status = load_json(tutor_path / "topic_status.json")

    if config.get("context") != "project":
        return {
            "is_project": False,
            "message": "Current context is not a project"
        }

    subject = university_config.get("subject", {})
    syllabus = university_config.get("syllabus_units", [])

    # Calculate milestone progress
    milestones = {}
    for unit in syllabus:
        if unit.get("is_milestone"):
            milestone_id = unit.get("id")
            status = topic_status.get(milestone_id, "new")
            milestones[milestone_id] = {
                "name": unit.get("name"),
                "deliverable": unit.get("deliverable"),
                "status": status
            }

    # Calculate overall progress
    total_units = len(syllabus)
    completed = sum(1 for u in syllabus if topic_status.get(u.get("id")) in ["learned", "mastered"])

    return {
        "is_project": True,
        "project_name": subject.get("name"),
        "objective": subject.get("objective"),
        "technologies": subject.get("technologies", []),
        "progress_percentage": round((completed / total_units * 100) if total_units > 0 else 0, 1),
        "milestones": milestones,
        "units_total": total_units,
        "units_completed": completed,
    }


@mcp.tool()
def get_project_capabilities() -> dict:
    """
    Get what the project can currently do based on completed units.

    Returns:
        List of capabilities (deliverables) from completed units
    """
    tutor_path = get_tutor_path()
    config = load_json(tutor_path / "config.json")
    university_config = load_json(tutor_path / "university_config.json")
    topic_status = load_json(tutor_path / "topic_status.json")

    if config.get("context") != "project":
        return {
            "is_project": False,
            "capabilities": []
        }

    syllabus = university_config.get("syllabus_units", [])

    capabilities = []
    next_capability = None

    for unit in sorted(syllabus, key=lambda x: x.get("order", 0)):
        unit_id = unit.get("id")
        status = topic_status.get(unit_id, "new")
        deliverable = unit.get("deliverable")

        if deliverable:
            if status in ["learned", "mastered"]:
                capabilities.append(deliverable)
            elif next_capability is None:
                next_capability = deliverable

    return {
        "is_project": True,
        "current_capabilities": capabilities,
        "next_capability": next_capability,
    }


@mcp.tool()
def get_next_build_task() -> dict:
    """
    Get the next task to build in the project.

    Returns:
        Next task with its details, why it matters, and what user will learn
    """
    tutor_path = get_tutor_path()
    config = load_json(tutor_path / "config.json")
    university_config = load_json(tutor_path / "university_config.json")
    topic_status = load_json(tutor_path / "topic_status.json")

    if config.get("context") != "project":
        return {
            "is_project": False,
            "task": None
        }

    syllabus = university_config.get("syllabus_units", [])

    # Find first incomplete task respecting prerequisites
    for unit in sorted(syllabus, key=lambda x: x.get("order", 0)):
        unit_id = unit.get("id")
        status = topic_status.get(unit_id, "new")

        if status in ["learned", "mastered"]:
            continue

        # Check prerequisites
        prereqs = unit.get("prerequisites", [])
        prereqs_met = all(
            topic_status.get(p) in ["learned", "mastered"]
            for p in prereqs
        )

        if prereqs_met:
            return {
                "is_project": True,
                "task": {
                    "id": unit_id,
                    "name": unit.get("name"),
                    "description": unit.get("description"),
                    "why_for_goal": unit.get("why_for_goal"),
                    "deliverable": unit.get("deliverable"),
                    "estimated_hours": unit.get("estimated_hours"),
                    "is_milestone": unit.get("is_milestone", False),
                    "status": status,
                }
            }

    return {
        "is_project": True,
        "task": None,
        "message": "All tasks completed! Project is done."
    }


# Run the server
if __name__ == "__main__":
    mcp.run()
