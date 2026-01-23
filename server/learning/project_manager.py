"""
Project Manager Module

Comprehensive project-based learning management including:
- Project lifecycle (planning, building, testing, deploying)
- Build task management with different task types
- Project templates for common project types
- Milestone tracking and celebration
- Code review integration
- Architecture decision tracking
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from pathlib import Path
from typing import Optional
import json


class ProjectPhase(Enum):
    """Phases of a project lifecycle."""
    PLANNING = "planning"           # Defining requirements, architecture
    SETUP = "setup"                 # Environment setup, initial structure
    BUILDING = "building"           # Core development
    TESTING = "testing"             # Testing and quality assurance
    REFACTORING = "refactoring"     # Code improvement
    DOCUMENTING = "documenting"     # Documentation
    DEPLOYING = "deploying"         # Deployment preparation
    MAINTAINING = "maintaining"     # Post-deployment maintenance
    COMPLETED = "completed"         # Project finished


class TaskType(Enum):
    """Types of build tasks in a project."""
    FEATURE = "feature"             # New functionality
    BUGFIX = "bugfix"               # Fix issues
    REFACTOR = "refactor"           # Improve code structure
    TEST = "test"                   # Write tests
    DOCUMENTATION = "documentation" # Write docs
    SETUP = "setup"                 # Environment/tooling setup
    INTEGRATION = "integration"     # Connect components
    OPTIMIZATION = "optimization"   # Performance improvement
    SECURITY = "security"           # Security improvements
    DEPLOY = "deploy"               # Deployment tasks


class TaskDifficulty(Enum):
    """Difficulty levels for project tasks."""
    BEGINNER = "beginner"           # First steps, simple concepts
    EASY = "easy"                   # Basic implementation
    MEDIUM = "medium"               # Requires some thinking
    HARD = "hard"                   # Complex logic/integration
    EXPERT = "expert"               # Advanced patterns, optimization


class ProjectType(Enum):
    """Common project types with templates."""
    WEB_FRONTEND = "web_frontend"       # React, Vue, etc.
    WEB_BACKEND = "web_backend"         # API, server
    WEB_FULLSTACK = "web_fullstack"     # Full stack app
    CLI = "cli"                         # Command line tool
    LIBRARY = "library"                 # Reusable library
    MOBILE = "mobile"                   # Mobile app
    DATA_SCIENCE = "data_science"       # Data/ML project
    GAME = "game"                       # Game development
    DEVOPS = "devops"                   # Infrastructure/DevOps
    MICROSERVICES = "microservices"     # Distributed system
    CUSTOM = "custom"                   # User-defined


@dataclass
class BuildTask:
    """
    Represents a single build task in a project.

    More granular than SyllabusUnit, focused on actionable work.
    """
    id: str
    name: str
    description: str
    task_type: TaskType = TaskType.FEATURE
    difficulty: TaskDifficulty = TaskDifficulty.MEDIUM

    # What the task achieves
    deliverable: str = ""                    # What user can do after
    success_criteria: list[str] = field(default_factory=list)  # How to verify completion

    # Learning aspects
    concepts_taught: list[str] = field(default_factory=list)   # Concepts learned
    skills_practiced: list[str] = field(default_factory=list)  # Skills used

    # Implementation guidance
    hints: list[str] = field(default_factory=list)             # Progressive hints
    code_snippets: dict[str, str] = field(default_factory=dict)  # language -> example
    common_mistakes: list[str] = field(default_factory=list)   # Pitfalls to avoid

    # Dependencies
    prerequisites: list[str] = field(default_factory=list)     # Required task IDs
    files_to_create: list[str] = field(default_factory=list)   # Files task creates
    files_to_modify: list[str] = field(default_factory=list)   # Files task modifies

    # Metadata
    order: int = 0
    estimated_minutes: int = 30
    is_milestone: bool = False
    is_optional: bool = False
    parent_unit_id: Optional[str] = None    # Link to SyllabusUnit

    # Status tracking
    status: str = "pending"                 # pending, in_progress, completed, skipped
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    attempts: int = 0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "task_type": self.task_type.value,
            "difficulty": self.difficulty.value,
            "deliverable": self.deliverable,
            "success_criteria": self.success_criteria,
            "concepts_taught": self.concepts_taught,
            "skills_practiced": self.skills_practiced,
            "hints": self.hints,
            "code_snippets": self.code_snippets,
            "common_mistakes": self.common_mistakes,
            "prerequisites": self.prerequisites,
            "files_to_create": self.files_to_create,
            "files_to_modify": self.files_to_modify,
            "order": self.order,
            "estimated_minutes": self.estimated_minutes,
            "is_milestone": self.is_milestone,
            "is_optional": self.is_optional,
            "parent_unit_id": self.parent_unit_id,
            "status": self.status,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "attempts": self.attempts,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "BuildTask":
        data = data.copy()
        if "task_type" in data:
            data["task_type"] = TaskType(data["task_type"])
        if "difficulty" in data:
            data["difficulty"] = TaskDifficulty(data["difficulty"])
        if "started_at" in data and data["started_at"]:
            data["started_at"] = datetime.fromisoformat(data["started_at"])
        if "completed_at" in data and data["completed_at"]:
            data["completed_at"] = datetime.fromisoformat(data["completed_at"])
        return cls(**data)


@dataclass
class Milestone:
    """
    Represents a significant achievement in the project.
    """
    id: str
    name: str
    description: str

    # What marks completion
    required_tasks: list[str] = field(default_factory=list)     # Task IDs
    capabilities_unlocked: list[str] = field(default_factory=list)  # What user can now do

    # Celebration and motivation
    celebration_message: str = ""
    next_challenge: str = ""

    # Status
    status: str = "locked"          # locked, in_progress, completed
    completed_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "required_tasks": self.required_tasks,
            "capabilities_unlocked": self.capabilities_unlocked,
            "celebration_message": self.celebration_message,
            "next_challenge": self.next_challenge,
            "status": self.status,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Milestone":
        data = data.copy()
        if "completed_at" in data and data["completed_at"]:
            data["completed_at"] = datetime.fromisoformat(data["completed_at"])
        return cls(**data)


@dataclass
class ArchitectureDecision:
    """
    Records an architecture decision made during the project.
    """
    id: str
    title: str
    context: str                            # Why this decision was needed
    decision: str                           # What was decided
    alternatives: list[str] = field(default_factory=list)  # Other options considered
    consequences: list[str] = field(default_factory=list)  # Impact of decision

    # Learning value
    concepts_learned: list[str] = field(default_factory=list)

    # Metadata
    date: date = field(default_factory=date.today)
    status: str = "accepted"                # proposed, accepted, deprecated, superseded

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "context": self.context,
            "decision": self.decision,
            "alternatives": self.alternatives,
            "consequences": self.consequences,
            "concepts_learned": self.concepts_learned,
            "date": self.date.isoformat(),
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ArchitectureDecision":
        data = data.copy()
        if "date" in data:
            data["date"] = date.fromisoformat(data["date"])
        return cls(**data)


@dataclass
class ProjectConfig:
    """
    Complete configuration for a project-based learning experience.
    """
    # Basic info
    name: str
    description: str
    objective: str                          # What the project achieves
    project_type: ProjectType = ProjectType.CUSTOM

    # Technologies
    primary_language: str = ""
    technologies: list[str] = field(default_factory=list)
    frameworks: list[str] = field(default_factory=list)
    tools: list[str] = field(default_factory=list)

    # Learning aspects
    target_skills: list[str] = field(default_factory=list)
    difficulty_level: str = "intermediate"   # beginner, intermediate, advanced
    estimated_hours: float = 20.0

    # Current state
    current_phase: ProjectPhase = ProjectPhase.PLANNING
    current_task_id: Optional[str] = None

    # Structure
    tasks: list[BuildTask] = field(default_factory=list)
    milestones: list[Milestone] = field(default_factory=list)
    architecture_decisions: list[ArchitectureDecision] = field(default_factory=list)

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    last_activity: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "objective": self.objective,
            "project_type": self.project_type.value,
            "primary_language": self.primary_language,
            "technologies": self.technologies,
            "frameworks": self.frameworks,
            "tools": self.tools,
            "target_skills": self.target_skills,
            "difficulty_level": self.difficulty_level,
            "estimated_hours": self.estimated_hours,
            "current_phase": self.current_phase.value,
            "current_task_id": self.current_task_id,
            "tasks": [t.to_dict() for t in self.tasks],
            "milestones": [m.to_dict() for m in self.milestones],
            "architecture_decisions": [a.to_dict() for a in self.architecture_decisions],
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "last_activity": self.last_activity.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ProjectConfig":
        data = data.copy()

        # Convert enums
        if "project_type" in data:
            data["project_type"] = ProjectType(data["project_type"])
        if "current_phase" in data:
            data["current_phase"] = ProjectPhase(data["current_phase"])

        # Convert nested objects
        if "tasks" in data:
            data["tasks"] = [BuildTask.from_dict(t) for t in data["tasks"]]
        if "milestones" in data:
            data["milestones"] = [Milestone.from_dict(m) for m in data["milestones"]]
        if "architecture_decisions" in data:
            data["architecture_decisions"] = [
                ArchitectureDecision.from_dict(a) for a in data["architecture_decisions"]
            ]

        # Convert timestamps
        if "created_at" in data:
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if "started_at" in data and data["started_at"]:
            data["started_at"] = datetime.fromisoformat(data["started_at"])
        if "completed_at" in data and data["completed_at"]:
            data["completed_at"] = datetime.fromisoformat(data["completed_at"])
        if "last_activity" in data:
            data["last_activity"] = datetime.fromisoformat(data["last_activity"])

        return cls(**data)


class ProjectManager:
    """
    Manager for project-based learning.

    Handles:
    - Project initialization and configuration
    - Task management and progression
    - Milestone tracking
    - Architecture decision recording
    - Progress visualization
    """

    def __init__(self, tutor_path: Path):
        self.tutor_path = tutor_path
        self.project_file = tutor_path / "project.json"
        self.build_log_file = tutor_path / "build_log.json"

        self._project: Optional[ProjectConfig] = None
        self._build_log: list[dict] = []

        self._load()

    def _load(self) -> None:
        """Load project configuration and build log."""
        if self.project_file.exists():
            with open(self.project_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._project = ProjectConfig.from_dict(data)

        if self.build_log_file.exists():
            with open(self.build_log_file, 'r', encoding='utf-8') as f:
                self._build_log = json.load(f)

    def _save(self) -> None:
        """Save project configuration and build log."""
        self.tutor_path.mkdir(parents=True, exist_ok=True)

        if self._project:
            self._project.last_activity = datetime.now()
            with open(self.project_file, 'w', encoding='utf-8') as f:
                json.dump(self._project.to_dict(), f, indent=2, ensure_ascii=False)

        with open(self.build_log_file, 'w', encoding='utf-8') as f:
            json.dump(self._build_log, f, indent=2, ensure_ascii=False)

    @property
    def project(self) -> Optional[ProjectConfig]:
        return self._project

    @property
    def is_initialized(self) -> bool:
        return self._project is not None

    def initialize_project(
        self,
        name: str,
        description: str,
        objective: str,
        project_type: ProjectType = ProjectType.CUSTOM,
        primary_language: str = "",
        technologies: list[str] = None,
        target_skills: list[str] = None,
        difficulty_level: str = "intermediate",
        estimated_hours: float = 20.0,
    ) -> ProjectConfig:
        """
        Initialize a new project for project-based learning.

        Args:
            name: Project name
            description: Brief description
            objective: What the project achieves
            project_type: Type of project
            primary_language: Main programming language
            technologies: List of technologies used
            target_skills: Skills to learn/practice
            difficulty_level: Overall difficulty
            estimated_hours: Estimated time to complete

        Returns:
            Created project configuration
        """
        self._project = ProjectConfig(
            name=name,
            description=description,
            objective=objective,
            project_type=project_type,
            primary_language=primary_language,
            technologies=technologies or [],
            target_skills=target_skills or [],
            difficulty_level=difficulty_level,
            estimated_hours=estimated_hours,
        )
        self._save()

        self._log_event("project_created", {
            "name": name,
            "type": project_type.value,
        })

        return self._project

    def add_task(self, task: BuildTask) -> None:
        """Add a build task to the project."""
        if not self._project:
            raise ValueError("Project not initialized")

        # Set order if not specified
        if task.order == 0:
            task.order = len(self._project.tasks) + 1

        self._project.tasks.append(task)
        self._project.tasks.sort(key=lambda t: t.order)
        self._save()

        self._log_event("task_added", {
            "task_id": task.id,
            "name": task.name,
            "type": task.task_type.value,
        })

    def add_milestone(self, milestone: Milestone) -> None:
        """Add a milestone to the project."""
        if not self._project:
            raise ValueError("Project not initialized")

        self._project.milestones.append(milestone)
        self._save()

        self._log_event("milestone_added", {
            "milestone_id": milestone.id,
            "name": milestone.name,
        })

    def start_task(self, task_id: str) -> BuildTask:
        """
        Start working on a task.

        Args:
            task_id: ID of the task to start

        Returns:
            The started task
        """
        if not self._project:
            raise ValueError("Project not initialized")

        task = self._get_task(task_id)
        if not task:
            raise ValueError(f"Task not found: {task_id}")

        # Check prerequisites
        for prereq_id in task.prerequisites:
            prereq = self._get_task(prereq_id)
            if prereq and prereq.status != "completed":
                raise ValueError(f"Prerequisite not met: {prereq_id}")

        task.status = "in_progress"
        task.started_at = datetime.now()
        task.attempts += 1

        self._project.current_task_id = task_id

        # Update phase if needed
        if self._project.current_phase == ProjectPhase.PLANNING:
            self._project.current_phase = ProjectPhase.BUILDING
            if not self._project.started_at:
                self._project.started_at = datetime.now()

        self._save()

        self._log_event("task_started", {
            "task_id": task_id,
            "attempt": task.attempts,
        })

        return task

    def complete_task(self, task_id: str, feedback: str = "") -> dict:
        """
        Mark a task as completed.

        Args:
            task_id: ID of the completed task
            feedback: Optional feedback about the completion

        Returns:
            Completion result with any milestones achieved
        """
        if not self._project:
            raise ValueError("Project not initialized")

        task = self._get_task(task_id)
        if not task:
            raise ValueError(f"Task not found: {task_id}")

        task.status = "completed"
        task.completed_at = datetime.now()

        # Check for milestone completion
        completed_milestones = self._check_milestones()

        # Calculate time spent
        time_spent = 0
        if task.started_at:
            time_spent = int((datetime.now() - task.started_at).total_seconds() / 60)

        # Find next available task
        next_task = self._get_next_available_task()

        self._project.current_task_id = next_task.id if next_task else None

        # Check if project is complete
        if self._is_project_complete():
            self._project.current_phase = ProjectPhase.COMPLETED
            self._project.completed_at = datetime.now()

        self._save()

        self._log_event("task_completed", {
            "task_id": task_id,
            "time_spent_minutes": time_spent,
            "milestones_achieved": [m.id for m in completed_milestones],
        })

        return {
            "task": task.to_dict(),
            "time_spent_minutes": time_spent,
            "milestones_achieved": [m.to_dict() for m in completed_milestones],
            "next_task": next_task.to_dict() if next_task else None,
            "project_complete": self._is_project_complete(),
        }

    def skip_task(self, task_id: str, reason: str = "") -> BuildTask:
        """Skip an optional task."""
        if not self._project:
            raise ValueError("Project not initialized")

        task = self._get_task(task_id)
        if not task:
            raise ValueError(f"Task not found: {task_id}")

        if not task.is_optional:
            raise ValueError("Cannot skip required task")

        task.status = "skipped"
        self._save()

        self._log_event("task_skipped", {
            "task_id": task_id,
            "reason": reason,
        })

        return task

    def record_architecture_decision(
        self,
        title: str,
        context: str,
        decision: str,
        alternatives: list[str] = None,
        consequences: list[str] = None,
        concepts_learned: list[str] = None,
    ) -> ArchitectureDecision:
        """
        Record an architecture decision.

        Args:
            title: Decision title
            context: Why this decision was needed
            decision: What was decided
            alternatives: Other options considered
            consequences: Impact of the decision
            concepts_learned: What was learned

        Returns:
            The recorded decision
        """
        if not self._project:
            raise ValueError("Project not initialized")

        decision_id = f"adr_{len(self._project.architecture_decisions) + 1:03d}"

        adr = ArchitectureDecision(
            id=decision_id,
            title=title,
            context=context,
            decision=decision,
            alternatives=alternatives or [],
            consequences=consequences or [],
            concepts_learned=concepts_learned or [],
        )

        self._project.architecture_decisions.append(adr)
        self._save()

        self._log_event("architecture_decision", {
            "id": decision_id,
            "title": title,
        })

        return adr

    def get_project_status(self) -> dict:
        """
        Get comprehensive project status.

        Returns:
            Complete project status including progress, current task, milestones
        """
        if not self._project:
            return {
                "is_project": False,
                "message": "No project initialized",
            }

        # Calculate task statistics
        total_tasks = len(self._project.tasks)
        completed_tasks = sum(1 for t in self._project.tasks if t.status == "completed")
        skipped_tasks = sum(1 for t in self._project.tasks if t.status == "skipped")
        in_progress_tasks = sum(1 for t in self._project.tasks if t.status == "in_progress")

        # Calculate time spent
        total_time = 0
        for entry in self._build_log:
            if entry.get("event") == "task_completed":
                total_time += entry.get("data", {}).get("time_spent_minutes", 0)

        # Get current task
        current_task = None
        if self._project.current_task_id:
            current_task = self._get_task(self._project.current_task_id)

        # Get milestone status
        milestone_status = []
        for milestone in self._project.milestones:
            completed_reqs = sum(
                1 for t_id in milestone.required_tasks
                if self._get_task(t_id) and self._get_task(t_id).status == "completed"
            )
            milestone_status.append({
                "id": milestone.id,
                "name": milestone.name,
                "status": milestone.status,
                "progress": completed_reqs / max(len(milestone.required_tasks), 1) * 100,
            })

        # Calculate capabilities
        capabilities = []
        for task in self._project.tasks:
            if task.status == "completed" and task.deliverable:
                capabilities.append(task.deliverable)

        return {
            "is_project": True,
            "name": self._project.name,
            "description": self._project.description,
            "objective": self._project.objective,
            "project_type": self._project.project_type.value,
            "current_phase": self._project.current_phase.value,
            "difficulty_level": self._project.difficulty_level,

            "progress": {
                "percentage": round((completed_tasks / max(total_tasks, 1)) * 100, 1),
                "tasks_completed": completed_tasks,
                "tasks_total": total_tasks,
                "tasks_skipped": skipped_tasks,
                "tasks_in_progress": in_progress_tasks,
            },

            "time": {
                "total_minutes": total_time,
                "estimated_hours": self._project.estimated_hours,
                "estimated_remaining_hours": max(
                    0, self._project.estimated_hours - (total_time / 60)
                ),
            },

            "current_task": current_task.to_dict() if current_task else None,
            "milestones": milestone_status,
            "capabilities": capabilities,

            "technologies": self._project.technologies,
            "target_skills": self._project.target_skills,

            "started_at": self._project.started_at.isoformat() if self._project.started_at else None,
            "last_activity": self._project.last_activity.isoformat(),
        }

    def get_next_task(self) -> Optional[BuildTask]:
        """Get the next available task based on prerequisites."""
        return self._get_next_available_task()

    def get_task_by_id(self, task_id: str) -> Optional[BuildTask]:
        """Get a specific task by ID."""
        return self._get_task(task_id)

    def get_tasks_by_type(self, task_type: TaskType) -> list[BuildTask]:
        """Get all tasks of a specific type."""
        if not self._project:
            return []
        return [t for t in self._project.tasks if t.task_type == task_type]

    def get_tasks_by_status(self, status: str) -> list[BuildTask]:
        """Get all tasks with a specific status."""
        if not self._project:
            return []
        return [t for t in self._project.tasks if t.status == status]

    def get_roadmap(self) -> dict:
        """
        Get a visual roadmap of the project.

        Returns:
            Structured roadmap with phases, milestones, and task dependencies
        """
        if not self._project:
            return {"phases": []}

        # Group tasks by type/phase
        phases = {
            "setup": [],
            "core_features": [],
            "testing": [],
            "polish": [],
            "deploy": [],
        }

        for task in self._project.tasks:
            if task.task_type == TaskType.SETUP:
                phases["setup"].append(task)
            elif task.task_type in [TaskType.TEST, TaskType.DOCUMENTATION]:
                phases["testing"].append(task)
            elif task.task_type in [TaskType.REFACTOR, TaskType.OPTIMIZATION]:
                phases["polish"].append(task)
            elif task.task_type == TaskType.DEPLOY:
                phases["deploy"].append(task)
            else:
                phases["core_features"].append(task)

        # Build roadmap
        roadmap = []
        for phase_name, tasks in phases.items():
            if tasks:
                completed = sum(1 for t in tasks if t.status == "completed")
                roadmap.append({
                    "phase": phase_name,
                    "tasks_total": len(tasks),
                    "tasks_completed": completed,
                    "progress": round((completed / len(tasks)) * 100, 1),
                    "tasks": [
                        {
                            "id": t.id,
                            "name": t.name,
                            "status": t.status,
                            "is_milestone": t.is_milestone,
                        }
                        for t in sorted(tasks, key=lambda x: x.order)
                    ],
                })

        return {
            "project_name": self._project.name,
            "phases": roadmap,
            "milestones": [m.to_dict() for m in self._project.milestones],
        }

    def get_build_log(self, limit: int = 20) -> list[dict]:
        """Get recent build log entries."""
        return self._build_log[-limit:]

    def _get_task(self, task_id: str) -> Optional[BuildTask]:
        """Get a task by ID."""
        if not self._project:
            return None
        for task in self._project.tasks:
            if task.id == task_id:
                return task
        return None

    def _get_next_available_task(self) -> Optional[BuildTask]:
        """Find the next task that can be started."""
        if not self._project:
            return None

        for task in sorted(self._project.tasks, key=lambda t: t.order):
            if task.status in ["completed", "skipped"]:
                continue

            # Check prerequisites
            prereqs_met = all(
                self._get_task(p) and self._get_task(p).status == "completed"
                for p in task.prerequisites
            )

            if prereqs_met:
                return task

        return None

    def _check_milestones(self) -> list[Milestone]:
        """Check if any milestones were just completed."""
        if not self._project:
            return []

        completed = []

        for milestone in self._project.milestones:
            if milestone.status == "completed":
                continue

            # Check if all required tasks are done
            all_done = all(
                self._get_task(t_id) and self._get_task(t_id).status == "completed"
                for t_id in milestone.required_tasks
            )

            if all_done:
                milestone.status = "completed"
                milestone.completed_at = datetime.now()
                completed.append(milestone)

        return completed

    def _is_project_complete(self) -> bool:
        """Check if all required tasks are done."""
        if not self._project:
            return False

        for task in self._project.tasks:
            if not task.is_optional and task.status not in ["completed"]:
                return False
        return True

    def _log_event(self, event: str, data: dict) -> None:
        """Log a build event."""
        self._build_log.append({
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "data": data,
        })
        # Keep only last 100 events
        if len(self._build_log) > 100:
            self._build_log = self._build_log[-100:]


# ============================================================================
# PROJECT TEMPLATES
# ============================================================================

def get_project_template(project_type: ProjectType, language: str = "python") -> dict:
    """
    Get a project template with predefined tasks and milestones.

    Args:
        project_type: Type of project
        language: Primary programming language

    Returns:
        Template with tasks and milestones
    """
    templates = {
        ProjectType.WEB_BACKEND: _get_backend_template(language),
        ProjectType.WEB_FRONTEND: _get_frontend_template(language),
        ProjectType.CLI: _get_cli_template(language),
        ProjectType.LIBRARY: _get_library_template(language),
        ProjectType.WEB_FULLSTACK: _get_fullstack_template(language),
    }

    return templates.get(project_type, {"tasks": [], "milestones": []})


def _get_backend_template(language: str) -> dict:
    """Template for backend/API project."""
    return {
        "tasks": [
            {
                "id": "setup_project",
                "name": "Project Setup",
                "description": "Initialize project structure and dependencies",
                "task_type": "setup",
                "difficulty": "beginner",
                "deliverable": "Project initialized with proper structure",
                "success_criteria": [
                    "Project directory created",
                    "Dependencies installed",
                    "Git initialized",
                ],
                "order": 1,
            },
            {
                "id": "setup_database",
                "name": "Database Setup",
                "description": "Configure database connection and ORM",
                "task_type": "setup",
                "difficulty": "easy",
                "prerequisites": ["setup_project"],
                "deliverable": "Database connection working",
                "success_criteria": [
                    "Database schema defined",
                    "Connection pool configured",
                    "Migrations working",
                ],
                "order": 2,
            },
            {
                "id": "create_models",
                "name": "Create Data Models",
                "description": "Define domain models and relationships",
                "task_type": "feature",
                "difficulty": "medium",
                "prerequisites": ["setup_database"],
                "deliverable": "Data models defined",
                "order": 3,
                "is_milestone": True,
            },
            {
                "id": "crud_endpoints",
                "name": "CRUD API Endpoints",
                "description": "Implement Create, Read, Update, Delete endpoints",
                "task_type": "feature",
                "difficulty": "medium",
                "prerequisites": ["create_models"],
                "deliverable": "Basic CRUD operations available via API",
                "success_criteria": [
                    "POST endpoint creates resources",
                    "GET endpoint retrieves resources",
                    "PUT/PATCH endpoint updates resources",
                    "DELETE endpoint removes resources",
                ],
                "order": 4,
                "is_milestone": True,
            },
            {
                "id": "input_validation",
                "name": "Input Validation",
                "description": "Add request validation and error handling",
                "task_type": "feature",
                "difficulty": "medium",
                "prerequisites": ["crud_endpoints"],
                "deliverable": "API validates all inputs properly",
                "order": 5,
            },
            {
                "id": "authentication",
                "name": "Authentication",
                "description": "Implement user authentication",
                "task_type": "feature",
                "difficulty": "hard",
                "prerequisites": ["crud_endpoints"],
                "deliverable": "Users can register and login",
                "order": 6,
                "is_milestone": True,
            },
            {
                "id": "authorization",
                "name": "Authorization",
                "description": "Add role-based access control",
                "task_type": "security",
                "difficulty": "hard",
                "prerequisites": ["authentication"],
                "deliverable": "Resources protected by permissions",
                "order": 7,
            },
            {
                "id": "write_tests",
                "name": "Write Tests",
                "description": "Create unit and integration tests",
                "task_type": "test",
                "difficulty": "medium",
                "prerequisites": ["crud_endpoints"],
                "deliverable": "Test suite with good coverage",
                "success_criteria": [
                    "Unit tests for business logic",
                    "Integration tests for API endpoints",
                    "Tests can be run with single command",
                ],
                "order": 8,
            },
            {
                "id": "documentation",
                "name": "API Documentation",
                "description": "Document API endpoints",
                "task_type": "documentation",
                "difficulty": "easy",
                "prerequisites": ["crud_endpoints"],
                "deliverable": "API documentation generated",
                "order": 9,
            },
            {
                "id": "deploy",
                "name": "Deployment",
                "description": "Deploy to production",
                "task_type": "deploy",
                "difficulty": "medium",
                "prerequisites": ["write_tests", "documentation"],
                "deliverable": "API running in production",
                "order": 10,
                "is_milestone": True,
            },
        ],
        "milestones": [
            {
                "id": "mvp",
                "name": "MVP Complete",
                "description": "Minimum viable product ready",
                "required_tasks": ["crud_endpoints", "input_validation"],
                "capabilities_unlocked": ["Basic CRUD via API"],
                "celebration_message": "Your API can now handle basic operations!",
            },
            {
                "id": "secure_api",
                "name": "Secure API",
                "description": "Authentication and authorization complete",
                "required_tasks": ["authentication", "authorization"],
                "capabilities_unlocked": ["User authentication", "Protected resources"],
                "celebration_message": "Your API is now secure!",
            },
            {
                "id": "production_ready",
                "name": "Production Ready",
                "description": "Ready for real users",
                "required_tasks": ["write_tests", "documentation", "deploy"],
                "capabilities_unlocked": ["Production deployment"],
                "celebration_message": "Congratulations! Your API is live!",
            },
        ],
    }


def _get_frontend_template(language: str) -> dict:
    """Template for frontend project."""
    return {
        "tasks": [
            {
                "id": "setup_project",
                "name": "Project Setup",
                "description": "Initialize frontend project with build tools",
                "task_type": "setup",
                "difficulty": "beginner",
                "deliverable": "Dev server running",
                "order": 1,
            },
            {
                "id": "layout_structure",
                "name": "Layout Structure",
                "description": "Create basic page layout and navigation",
                "task_type": "feature",
                "difficulty": "easy",
                "prerequisites": ["setup_project"],
                "deliverable": "Navigation and layout working",
                "order": 2,
            },
            {
                "id": "component_library",
                "name": "Component Library",
                "description": "Create reusable UI components",
                "task_type": "feature",
                "difficulty": "medium",
                "prerequisites": ["layout_structure"],
                "deliverable": "Reusable components ready",
                "order": 3,
                "is_milestone": True,
            },
            {
                "id": "state_management",
                "name": "State Management",
                "description": "Implement application state management",
                "task_type": "feature",
                "difficulty": "medium",
                "prerequisites": ["component_library"],
                "deliverable": "State management working",
                "order": 4,
            },
            {
                "id": "api_integration",
                "name": "API Integration",
                "description": "Connect to backend API",
                "task_type": "integration",
                "difficulty": "medium",
                "prerequisites": ["state_management"],
                "deliverable": "Data flows from API to UI",
                "order": 5,
                "is_milestone": True,
            },
            {
                "id": "forms_validation",
                "name": "Forms and Validation",
                "description": "Create forms with validation",
                "task_type": "feature",
                "difficulty": "medium",
                "prerequisites": ["api_integration"],
                "deliverable": "Forms submit data correctly",
                "order": 6,
            },
            {
                "id": "styling",
                "name": "Styling and Theming",
                "description": "Polish visual design",
                "task_type": "feature",
                "difficulty": "easy",
                "prerequisites": ["component_library"],
                "deliverable": "Polished visual appearance",
                "order": 7,
            },
            {
                "id": "testing",
                "name": "Testing",
                "description": "Add component and e2e tests",
                "task_type": "test",
                "difficulty": "medium",
                "prerequisites": ["api_integration"],
                "deliverable": "Test coverage for key flows",
                "order": 8,
            },
            {
                "id": "build_optimize",
                "name": "Build Optimization",
                "description": "Optimize for production",
                "task_type": "optimization",
                "difficulty": "medium",
                "prerequisites": ["testing"],
                "deliverable": "Optimized production build",
                "order": 9,
            },
            {
                "id": "deploy",
                "name": "Deployment",
                "description": "Deploy to production",
                "task_type": "deploy",
                "difficulty": "easy",
                "prerequisites": ["build_optimize"],
                "deliverable": "App live in production",
                "order": 10,
                "is_milestone": True,
            },
        ],
        "milestones": [
            {
                "id": "ui_ready",
                "name": "UI Foundation",
                "description": "Core UI components ready",
                "required_tasks": ["component_library", "styling"],
                "capabilities_unlocked": ["Reusable UI components"],
            },
            {
                "id": "functional",
                "name": "Functional App",
                "description": "App works end-to-end",
                "required_tasks": ["api_integration", "forms_validation"],
                "capabilities_unlocked": ["Complete user flows"],
            },
            {
                "id": "production",
                "name": "Production Ready",
                "description": "Ready for real users",
                "required_tasks": ["testing", "deploy"],
                "capabilities_unlocked": ["Live application"],
            },
        ],
    }


def _get_cli_template(language: str) -> dict:
    """Template for CLI tool project."""
    return {
        "tasks": [
            {
                "id": "setup_project",
                "name": "Project Setup",
                "description": "Initialize CLI project",
                "task_type": "setup",
                "difficulty": "beginner",
                "deliverable": "CLI scaffold ready",
                "order": 1,
            },
            {
                "id": "argument_parsing",
                "name": "Argument Parsing",
                "description": "Set up command line argument handling",
                "task_type": "feature",
                "difficulty": "easy",
                "prerequisites": ["setup_project"],
                "deliverable": "CLI accepts arguments",
                "order": 2,
            },
            {
                "id": "core_command",
                "name": "Core Command",
                "description": "Implement main functionality",
                "task_type": "feature",
                "difficulty": "medium",
                "prerequisites": ["argument_parsing"],
                "deliverable": "Main command works",
                "order": 3,
                "is_milestone": True,
            },
            {
                "id": "subcommands",
                "name": "Subcommands",
                "description": "Add additional commands",
                "task_type": "feature",
                "difficulty": "medium",
                "prerequisites": ["core_command"],
                "deliverable": "Multiple commands available",
                "order": 4,
            },
            {
                "id": "output_formatting",
                "name": "Output Formatting",
                "description": "Format output nicely",
                "task_type": "feature",
                "difficulty": "easy",
                "prerequisites": ["core_command"],
                "deliverable": "Clean formatted output",
                "order": 5,
            },
            {
                "id": "error_handling",
                "name": "Error Handling",
                "description": "Handle errors gracefully",
                "task_type": "feature",
                "difficulty": "medium",
                "prerequisites": ["core_command"],
                "deliverable": "Helpful error messages",
                "order": 6,
            },
            {
                "id": "configuration",
                "name": "Configuration",
                "description": "Add config file support",
                "task_type": "feature",
                "difficulty": "medium",
                "prerequisites": ["core_command"],
                "deliverable": "Config file loading works",
                "order": 7,
                "is_optional": True,
            },
            {
                "id": "testing",
                "name": "Testing",
                "description": "Write CLI tests",
                "task_type": "test",
                "difficulty": "medium",
                "prerequisites": ["core_command"],
                "deliverable": "Test suite passing",
                "order": 8,
            },
            {
                "id": "documentation",
                "name": "Documentation",
                "description": "Write usage documentation",
                "task_type": "documentation",
                "difficulty": "easy",
                "prerequisites": ["core_command"],
                "deliverable": "README with usage examples",
                "order": 9,
            },
            {
                "id": "packaging",
                "name": "Packaging",
                "description": "Package for distribution",
                "task_type": "deploy",
                "difficulty": "medium",
                "prerequisites": ["testing", "documentation"],
                "deliverable": "Installable package",
                "order": 10,
                "is_milestone": True,
            },
        ],
        "milestones": [
            {
                "id": "working_cli",
                "name": "Working CLI",
                "description": "Core functionality ready",
                "required_tasks": ["core_command", "error_handling"],
                "capabilities_unlocked": ["Main CLI command"],
            },
            {
                "id": "complete_tool",
                "name": "Complete Tool",
                "description": "All features implemented",
                "required_tasks": ["subcommands", "output_formatting"],
                "capabilities_unlocked": ["Full CLI feature set"],
            },
            {
                "id": "distributable",
                "name": "Distributable",
                "description": "Ready for distribution",
                "required_tasks": ["testing", "documentation", "packaging"],
                "capabilities_unlocked": ["Public distribution"],
            },
        ],
    }


def _get_library_template(language: str) -> dict:
    """Template for library project."""
    return {
        "tasks": [
            {
                "id": "setup_project",
                "name": "Project Setup",
                "description": "Initialize library project",
                "task_type": "setup",
                "difficulty": "beginner",
                "deliverable": "Library scaffold ready",
                "order": 1,
            },
            {
                "id": "core_api",
                "name": "Core API",
                "description": "Design and implement core API",
                "task_type": "feature",
                "difficulty": "medium",
                "prerequisites": ["setup_project"],
                "deliverable": "Core functionality available",
                "order": 2,
                "is_milestone": True,
            },
            {
                "id": "extended_features",
                "name": "Extended Features",
                "description": "Add additional features",
                "task_type": "feature",
                "difficulty": "medium",
                "prerequisites": ["core_api"],
                "deliverable": "Full feature set",
                "order": 3,
            },
            {
                "id": "error_handling",
                "name": "Error Handling",
                "description": "Robust error handling",
                "task_type": "feature",
                "difficulty": "medium",
                "prerequisites": ["core_api"],
                "deliverable": "Clear error messages",
                "order": 4,
            },
            {
                "id": "testing",
                "name": "Comprehensive Testing",
                "description": "Write thorough tests",
                "task_type": "test",
                "difficulty": "medium",
                "prerequisites": ["core_api"],
                "deliverable": "High test coverage",
                "order": 5,
            },
            {
                "id": "documentation",
                "name": "API Documentation",
                "description": "Document all public APIs",
                "task_type": "documentation",
                "difficulty": "medium",
                "prerequisites": ["core_api"],
                "deliverable": "Complete API docs",
                "order": 6,
                "is_milestone": True,
            },
            {
                "id": "examples",
                "name": "Usage Examples",
                "description": "Create example code",
                "task_type": "documentation",
                "difficulty": "easy",
                "prerequisites": ["documentation"],
                "deliverable": "Working examples",
                "order": 7,
            },
            {
                "id": "packaging",
                "name": "Packaging",
                "description": "Prepare for publishing",
                "task_type": "deploy",
                "difficulty": "medium",
                "prerequisites": ["testing", "documentation"],
                "deliverable": "Published package",
                "order": 8,
                "is_milestone": True,
            },
        ],
        "milestones": [
            {
                "id": "usable",
                "name": "Usable Library",
                "description": "Library can be used",
                "required_tasks": ["core_api", "error_handling"],
                "capabilities_unlocked": ["Core library functionality"],
            },
            {
                "id": "documented",
                "name": "Documented",
                "description": "Library is documented",
                "required_tasks": ["documentation", "examples"],
                "capabilities_unlocked": ["Learning from docs"],
            },
            {
                "id": "published",
                "name": "Published",
                "description": "Library is public",
                "required_tasks": ["testing", "packaging"],
                "capabilities_unlocked": ["Anyone can install"],
            },
        ],
    }


def _get_fullstack_template(language: str) -> dict:
    """Template for fullstack project - combines backend and frontend."""
    backend = _get_backend_template(language)
    frontend = _get_frontend_template(language)

    # Prefix backend tasks
    for task in backend["tasks"]:
        task["id"] = f"backend_{task['id']}"
        task["name"] = f"Backend: {task['name']}"
        task["prerequisites"] = [f"backend_{p}" for p in task.get("prerequisites", [])]

    # Prefix frontend tasks and make them depend on backend API
    for task in frontend["tasks"]:
        task["id"] = f"frontend_{task['id']}"
        task["name"] = f"Frontend: {task['name']}"
        task["prerequisites"] = [f"frontend_{p}" for p in task.get("prerequisites", [])]
        # Offset order
        task["order"] = task["order"] + len(backend["tasks"])

    # Make frontend API integration depend on backend CRUD
    for task in frontend["tasks"]:
        if task["id"] == "frontend_api_integration":
            task["prerequisites"].append("backend_crud_endpoints")

    return {
        "tasks": backend["tasks"] + frontend["tasks"],
        "milestones": [
            {
                "id": "backend_mvp",
                "name": "Backend MVP",
                "description": "Backend API working",
                "required_tasks": ["backend_crud_endpoints"],
                "capabilities_unlocked": ["API endpoints available"],
            },
            {
                "id": "frontend_mvp",
                "name": "Frontend MVP",
                "description": "Frontend connects to backend",
                "required_tasks": ["frontend_api_integration"],
                "capabilities_unlocked": ["End-to-end data flow"],
            },
            {
                "id": "production",
                "name": "Production Ready",
                "description": "Full stack deployed",
                "required_tasks": ["backend_deploy", "frontend_deploy"],
                "capabilities_unlocked": ["Live application"],
            },
        ],
    }
