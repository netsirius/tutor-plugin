#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "fastmcp>=2.0.0",
# ]
# ///
"""
Tutor MCP Server

Provides tools for the Tutor plugin to manage learning progress,
validate code, and interact with the curriculum.

Run with uv (recommended - no venv needed):
    uv run tutor_mcp.py

Or with pip:
    pip install fastmcp
    python tutor_mcp.py
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastmcp import FastMCP

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
# CODE VALIDATION TOOLS
# ============================================================================

@mcp.tool()
def validate_rust_code(project_path: str) -> dict:
    """
    Validate Rust code by running cargo check.

    Args:
        project_path: Path to the Rust project directory (containing Cargo.toml)

    Returns:
        Compilation result with success status, errors, and warnings
    """
    project = Path(project_path)

    if not (project / "Cargo.toml").exists():
        return {
            "success": False,
            "error": f"No Cargo.toml found in {project_path}"
        }

    try:
        result = subprocess.run(
            ["cargo", "check", "--message-format=short"],
            cwd=project,
            capture_output=True,
            text=True,
            timeout=60
        )

        return {
            "success": result.returncode == 0,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "has_errors": "error" in result.stderr.lower(),
            "has_warnings": "warning" in result.stderr.lower()
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Compilation timed out after 60 seconds"
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "cargo not found. Is Rust installed?"
        }


@mcp.tool()
def run_rust_tests(project_path: str, test_name: Optional[str] = None) -> dict:
    """
    Run Rust tests for a project.

    Args:
        project_path: Path to the Rust project directory
        test_name: Optional specific test name to run

    Returns:
        Test results including passed/failed counts and output
    """
    project = Path(project_path)

    if not (project / "Cargo.toml").exists():
        return {
            "success": False,
            "error": f"No Cargo.toml found in {project_path}"
        }

    cmd = ["cargo", "test"]
    if test_name:
        cmd.append(test_name)
    cmd.append("--")
    cmd.append("--nocapture")

    try:
        result = subprocess.run(
            cmd,
            cwd=project,
            capture_output=True,
            text=True,
            timeout=120
        )

        # Parse test results
        output = result.stdout + result.stderr
        passed = output.count("test result: ok")
        failed = "FAILED" in output

        # Count individual tests
        test_lines = [l for l in output.split('\n') if l.strip().startswith("test ")]
        tests_passed = sum(1 for l in test_lines if "... ok" in l)
        tests_failed = sum(1 for l in test_lines if "... FAILED" in l)

        return {
            "success": result.returncode == 0,
            "all_passed": not failed,
            "tests_passed": tests_passed,
            "tests_failed": tests_failed,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Tests timed out after 120 seconds"
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "cargo not found. Is Rust installed?"
        }


@mcp.tool()
def run_clippy(project_path: str) -> dict:
    """
    Run Clippy linter on a Rust project for code quality suggestions.

    Args:
        project_path: Path to the Rust project directory

    Returns:
        Clippy suggestions and warnings
    """
    project = Path(project_path)

    if not (project / "Cargo.toml").exists():
        return {
            "success": False,
            "error": f"No Cargo.toml found in {project_path}"
        }

    try:
        result = subprocess.run(
            ["cargo", "clippy", "--message-format=short"],
            cwd=project,
            capture_output=True,
            text=True,
            timeout=120
        )

        # Count warnings
        warnings = result.stderr.count("warning:")
        errors = result.stderr.count("error:")

        return {
            "success": result.returncode == 0,
            "warnings_count": warnings,
            "errors_count": errors,
            "output": result.stderr,
            "suggestions": [
                line.strip()
                for line in result.stderr.split('\n')
                if "warning:" in line or "help:" in line
            ]
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Clippy timed out after 120 seconds"
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "cargo clippy not found. Run: rustup component add clippy"
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


# Run the server
if __name__ == "__main__":
    mcp.run()
