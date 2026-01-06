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
- Spaced repetition for knowledge retention
- Learning style adaptation
- Comprehensive analytics

Note: Code validation is handled directly by Claude via Bash commands,
which provides more flexibility and doesn't require language-specific validators.

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
            missing = [p for p in prereqs if modules.get(p, {}).get("status") != "completed"]
            continue

        # Find first incomplete topic/exercise
        topics = mod.get("topics", [])
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

    # Count exercises - handle both integer counts and lists of exercises
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
def get_learning_style() -> dict:
    """
    Get the detected learning style profile.

    Returns:
        Learning style analysis and content recommendations
    """
    try:
        from learning import LearningStyleAnalyzer

        analyzer = LearningStyleAnalyzer(get_tutor_path() / "learning_profile.json")
        summary = analyzer.get_style_summary()
        recommendations = analyzer.get_content_recommendations()

        return {
            "success": True,
            "style_summary": summary,
            "content_recommendations": recommendations,
        }
    except ImportError:
        return {
            "success": False,
            "error": "Learning style module not available",
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

    Updates progress, SRS, learning style, and skill assessments.

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
# GAMIFICATION TOOLS
# ============================================================================

@mcp.tool()
def check_achievements(event_type: str, **event_details) -> dict:
    """
    Check for new achievements based on an event.

    Args:
        event_type: Type of event (exercise_completed, session_started, etc.)
        **event_details: Additional event details (score, attempts, time_minutes, etc.)

    Returns:
        Newly earned badges and challenge updates
    """
    try:
        from learning import GamificationEngine

        progress = load_json(get_tutor_path() / "progress.json")
        engine = GamificationEngine(progress, get_tutor_path() / "gamification.json")

        event = {"type": event_type, **event_details}
        new_badges = engine.check_achievements(event)
        challenge_update = engine.update_challenge_progress(event)

        return {
            "success": True,
            "new_badges": [b.to_dict() for b in new_badges],
            "challenge_update": challenge_update,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
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

        progress = load_json(get_tutor_path() / "progress.json")
        engine = GamificationEngine(progress, get_tutor_path() / "gamification.json")

        summary = engine.get_progress_summary()
        all_badges = engine.get_all_badges()
        milestones = engine.get_milestones()

        return {
            "success": True,
            "summary": summary,
            "all_badges": all_badges,
            "milestones": [m.to_dict() for m in milestones],
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
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

        progress = load_json(get_tutor_path() / "progress.json")
        engine = GamificationEngine(progress, get_tutor_path() / "gamification.json")

        challenge = engine.get_current_challenge()

        return {
            "success": True,
            "challenge": challenge.to_dict() if challenge else None,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


# ============================================================================
# EXPORT/IMPORT TOOLS
# ============================================================================

@mcp.tool()
def export_progress(
    format: str = "json",
    include_sessions: bool = True,
    include_evaluations: bool = True,
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
        result = exporter.export(
            format=ExportFormat(format),
            include_sessions=include_sessions,
            include_evaluations=include_evaluations,
        )

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
    create_backup: bool = True,
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
            create_backup=create_backup,
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
        result = importer.validate_import_file(Path(filepath))

        return {
            "success": True,
            "validation": result,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


# Run the server
if __name__ == "__main__":
    mcp.run()
