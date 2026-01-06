#!/usr/bin/env python3
"""
Learning Progress Manager for the Tutor Plugin

This script manages student learning progress, including:
- Initialization of new courses
- Progress tracking (modules, exercises)
- Session management
- Recommendations for next topics
- Progress reports
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import argparse


TUTOR_DIR = ".tutor"
CONFIG_FILE = "config.json"
PROGRESS_FILE = "progress.json"
CURRICULUM_FILE = "curriculum.json"
SESSIONS_DIR = "sessions"


def get_tutor_path() -> Path:
    """Get the .tutor directory path in current working directory."""
    return Path.cwd() / TUTOR_DIR


def ensure_tutor_dir():
    """Create .tutor directory if it doesn't exist."""
    tutor_path = get_tutor_path()
    tutor_path.mkdir(exist_ok=True)
    (tutor_path / SESSIONS_DIR).mkdir(exist_ok=True)


def load_json(filename: str) -> dict:
    """Load a JSON file from .tutor directory."""
    filepath = get_tutor_path() / filename
    if not filepath.exists():
        return {}
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(filename: str, data: dict):
    """Save data to a JSON file in .tutor directory."""
    ensure_tutor_dir()
    filepath = get_tutor_path() / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def init_course(language: str, level: str, student_name: str = "estudiante"):
    """Initialize a new course with default configuration."""
    ensure_tutor_dir()

    # Create config
    config = {
        "language": language,
        "student_name": student_name,
        "level": level,
        "started_at": datetime.now().isoformat(),
        "goals": [],
        "time_per_session": "1h",
        "curriculum_source": "pending",
        "preferences": {
            "explanation_style": "detailed",
            "exercise_difficulty": "adaptive",
            "show_hints": True
        }
    }
    save_json(CONFIG_FILE, config)

    # Create initial progress
    progress = {
        "current_module": None,
        "current_topic": None,
        "modules": {},
        "statistics": {
            "total_time_minutes": 0,
            "total_exercises_completed": 0,
            "total_exercises_attempted": 0,
            "average_score": 0,
            "streak_days": 0,
            "last_session": None
        }
    }
    save_json(PROGRESS_FILE, progress)

    print(json.dumps({
        "status": "initialized",
        "language": language,
        "level": level,
        "message": f"Course initialized for {language} at {level} level"
    }))


def get_progress():
    """Get current progress as JSON."""
    config = load_json(CONFIG_FILE)
    progress = load_json(PROGRESS_FILE)
    curriculum = load_json(CURRICULUM_FILE)

    result = {
        "config": config,
        "progress": progress,
        "curriculum_loaded": bool(curriculum),
        "has_active_course": bool(config)
    }
    print(json.dumps(result, indent=2))


def complete_exercise(module: str, exercise: str, score: int, attempts: int):
    """Mark an exercise as completed and update statistics."""
    progress = load_json(PROGRESS_FILE)

    if "modules" not in progress:
        progress["modules"] = {}

    if module not in progress["modules"]:
        progress["modules"][module] = {
            "status": "in_progress",
            "started_at": datetime.now().isoformat(),
            "exercises": {}
        }

    # Update exercise
    progress["modules"][module]["exercises"][exercise] = {
        "status": "completed",
        "completed_at": datetime.now().isoformat(),
        "attempts": attempts,
        "score": score
    }

    # Update statistics
    stats = progress.get("statistics", {})
    stats["total_exercises_completed"] = stats.get("total_exercises_completed", 0) + 1
    stats["total_exercises_attempted"] = stats.get("total_exercises_attempted", 0) + attempts

    # Recalculate average score
    total_score = 0
    count = 0
    for mod_data in progress["modules"].values():
        for ex_data in mod_data.get("exercises", {}).values():
            if ex_data.get("status") == "completed":
                total_score += ex_data.get("score", 0)
                count += 1

    if count > 0:
        stats["average_score"] = round(total_score / count, 1)

    progress["statistics"] = stats
    progress["current_module"] = module

    save_json(PROGRESS_FILE, progress)

    print(json.dumps({
        "status": "success",
        "module": module,
        "exercise": exercise,
        "score": score,
        "new_average": stats.get("average_score", 0)
    }))


def complete_module(module: str, score: int):
    """Mark a module as completed."""
    progress = load_json(PROGRESS_FILE)

    if module in progress.get("modules", {}):
        progress["modules"][module]["status"] = "completed"
        progress["modules"][module]["completed_at"] = datetime.now().isoformat()
        progress["modules"][module]["score"] = score

        save_json(PROGRESS_FILE, progress)

        print(json.dumps({
            "status": "success",
            "module": module,
            "score": score,
            "message": f"Module {module} completed!"
        }))
    else:
        print(json.dumps({
            "status": "error",
            "message": f"Module {module} not found in progress"
        }))


def start_session():
    """Start a new study session."""
    progress = load_json(PROGRESS_FILE)
    today = datetime.now().strftime("%Y-%m-%d")

    # Check streak
    stats = progress.get("statistics", {})
    last_session = stats.get("last_session")

    if last_session:
        last_date = datetime.strptime(last_session, "%Y-%m-%d")
        today_date = datetime.strptime(today, "%Y-%m-%d")
        diff = (today_date - last_date).days

        if diff == 1:
            stats["streak_days"] = stats.get("streak_days", 0) + 1
        elif diff > 1:
            stats["streak_days"] = 1
        # if diff == 0, keep current streak (same day)
    else:
        stats["streak_days"] = 1

    stats["last_session"] = today
    progress["statistics"] = stats
    save_json(PROGRESS_FILE, progress)

    # Create session file
    session = {
        "date": today,
        "started_at": datetime.now().isoformat(),
        "topics_covered": [],
        "exercises_done": 0,
        "notes": []
    }
    save_json(f"{SESSIONS_DIR}/{today}.json", session)

    print(json.dumps({
        "status": "session_started",
        "date": today,
        "streak": stats["streak_days"]
    }))


def end_session(topics_covered: str, exercises_done: int):
    """End current study session."""
    today = datetime.now().strftime("%Y-%m-%d")
    session_file = f"{SESSIONS_DIR}/{today}.json"
    session = load_json(session_file)

    if session:
        session["ended_at"] = datetime.now().isoformat()
        session["topics_covered"] = topics_covered.split(",") if topics_covered else []
        session["exercises_done"] = exercises_done

        # Calculate duration
        if session.get("started_at"):
            start = datetime.fromisoformat(session["started_at"])
            end = datetime.now()
            duration_minutes = int((end - start).total_seconds() / 60)
            session["duration_minutes"] = duration_minutes

            # Update total time in progress
            progress = load_json(PROGRESS_FILE)
            stats = progress.get("statistics", {})
            stats["total_time_minutes"] = stats.get("total_time_minutes", 0) + duration_minutes
            progress["statistics"] = stats
            save_json(PROGRESS_FILE, progress)

        save_json(session_file, session)

        print(json.dumps({
            "status": "session_ended",
            "duration_minutes": session.get("duration_minutes", 0),
            "topics": session["topics_covered"],
            "exercises": exercises_done
        }))
    else:
        print(json.dumps({
            "status": "error",
            "message": "No active session found for today"
        }))


def recommend():
    """Get recommendation for next topic to study."""
    progress = load_json(PROGRESS_FILE)
    curriculum = load_json(CURRICULUM_FILE)

    if not curriculum:
        print(json.dumps({
            "status": "no_curriculum",
            "message": "No curriculum loaded. Use /tutor:curriculum to set one up."
        }))
        return

    modules = progress.get("modules", {})
    curriculum_modules = curriculum.get("modules", [])

    # Find first incomplete module
    for mod in curriculum_modules:
        mod_id = mod["id"]
        mod_progress = modules.get(mod_id, {})

        if mod_progress.get("status") != "completed":
            # Check prerequisites
            prereqs = mod.get("prerequisites", [])
            prereqs_met = all(
                modules.get(p, {}).get("status") == "completed"
                for p in prereqs
            )

            if prereqs_met:
                # Find first incomplete exercise in this module
                exercises = mod.get("exercises", [])
                mod_exercises = mod_progress.get("exercises", {})

                for ex in exercises:
                    ex_id = ex["id"]
                    if mod_exercises.get(ex_id, {}).get("status") != "completed":
                        print(json.dumps({
                            "status": "recommendation",
                            "module": mod_id,
                            "module_title": mod["title"],
                            "next_exercise": ex_id,
                            "exercise_title": ex["title"],
                            "difficulty": ex.get("difficulty", "unknown")
                        }))
                        return

                # All exercises done, but module not marked complete
                print(json.dumps({
                    "status": "recommendation",
                    "module": mod_id,
                    "module_title": mod["title"],
                    "action": "complete_module",
                    "message": "All exercises done. Review and complete module."
                }))
                return

    print(json.dumps({
        "status": "all_complete",
        "message": "Congratulations! You've completed the entire curriculum!"
    }))


def report():
    """Generate a progress report."""
    config = load_json(CONFIG_FILE)
    progress = load_json(PROGRESS_FILE)
    curriculum = load_json(CURRICULUM_FILE)

    stats = progress.get("statistics", {})
    modules = progress.get("modules", {})

    # Calculate module progress
    total_modules = len(curriculum.get("modules", []))
    completed_modules = sum(1 for m in modules.values() if m.get("status") == "completed")

    # Calculate exercise progress
    total_exercises = sum(
        len(m.get("exercises", []))
        for m in curriculum.get("modules", [])
    )

    report_data = {
        "language": config.get("language", "unknown"),
        "level": config.get("level", "unknown"),
        "started_at": config.get("started_at"),
        "modules": {
            "completed": completed_modules,
            "total": total_modules,
            "percentage": round(completed_modules / total_modules * 100, 1) if total_modules > 0 else 0
        },
        "exercises": {
            "completed": stats.get("total_exercises_completed", 0),
            "total": total_exercises,
            "percentage": round(stats.get("total_exercises_completed", 0) / total_exercises * 100, 1) if total_exercises > 0 else 0
        },
        "time_spent": {
            "minutes": stats.get("total_time_minutes", 0),
            "hours": round(stats.get("total_time_minutes", 0) / 60, 1)
        },
        "average_score": stats.get("average_score", 0),
        "streak_days": stats.get("streak_days", 0),
        "last_session": stats.get("last_session"),
        "current_module": progress.get("current_module"),
        "module_details": []
    }

    # Add per-module details
    for mod in curriculum.get("modules", []):
        mod_id = mod["id"]
        mod_progress = modules.get(mod_id, {})

        report_data["module_details"].append({
            "id": mod_id,
            "title": mod["title"],
            "status": mod_progress.get("status", "pending"),
            "score": mod_progress.get("score"),
            "exercises_completed": sum(
                1 for e in mod_progress.get("exercises", {}).values()
                if e.get("status") == "completed"
            ),
            "exercises_total": len(mod.get("exercises", []))
        })

    print(json.dumps(report_data, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Learning Progress Manager")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # init command
    init_parser = subparsers.add_parser("init", help="Initialize new course")
    init_parser.add_argument("--language", required=True, help="Programming language")
    init_parser.add_argument("--level", required=True, choices=["beginner", "intermediate", "advanced"])
    init_parser.add_argument("--name", default="estudiante", help="Student name")

    # get command
    subparsers.add_parser("get", help="Get current progress")

    # complete-exercise command
    ce_parser = subparsers.add_parser("complete-exercise", help="Mark exercise as completed")
    ce_parser.add_argument("--module", required=True, help="Module ID")
    ce_parser.add_argument("--exercise", required=True, help="Exercise ID")
    ce_parser.add_argument("--score", type=int, required=True, help="Score (0-100)")
    ce_parser.add_argument("--attempts", type=int, required=True, help="Number of attempts")

    # complete-module command
    cm_parser = subparsers.add_parser("complete-module", help="Mark module as completed")
    cm_parser.add_argument("--module", required=True, help="Module ID")
    cm_parser.add_argument("--score", type=int, required=True, help="Score (0-100)")

    # start-session command
    subparsers.add_parser("start-session", help="Start study session")

    # end-session command
    es_parser = subparsers.add_parser("end-session", help="End study session")
    es_parser.add_argument("--topics-covered", default="", help="Comma-separated topics")
    es_parser.add_argument("--exercises-done", type=int, default=0, help="Number of exercises done")

    # recommend command
    subparsers.add_parser("recommend", help="Get next topic recommendation")

    # report command
    subparsers.add_parser("report", help="Generate progress report")

    args = parser.parse_args()

    if args.command == "init":
        init_course(args.language, args.level, args.name)
    elif args.command == "get":
        get_progress()
    elif args.command == "complete-exercise":
        complete_exercise(args.module, args.exercise, args.score, args.attempts)
    elif args.command == "complete-module":
        complete_module(args.module, args.score)
    elif args.command == "start-session":
        start_session()
    elif args.command == "end-session":
        end_session(args.topics_covered, args.exercises_done)
    elif args.command == "recommend":
        recommend()
    elif args.command == "report":
        report()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
