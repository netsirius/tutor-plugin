"""
Dynamic Prerequisites System

Automatically infers and validates prerequisites:
- Extracts prerequisites from curriculum structure
- Detects implicit dependencies from content
- Validates readiness before starting new topics
- Suggests remediation when prerequisites are missing
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import json
from pathlib import Path
from collections import defaultdict


class PrerequisiteStatus(Enum):
    """Status of a prerequisite."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    NEEDS_REVIEW = "needs_review"  # Completed but struggling


class ReadinessLevel(Enum):
    """How ready the student is for a topic."""
    READY = "ready"  # All prerequisites met
    MOSTLY_READY = "mostly_ready"  # Minor gaps
    NOT_READY = "not_ready"  # Missing key prerequisites
    BLOCKED = "blocked"  # Critical prerequisites missing


@dataclass
class Prerequisite:
    """A prerequisite relationship."""
    source_topic: str  # The prerequisite topic
    target_topic: str  # The topic that requires it
    importance: float  # 0-1, how critical this prerequisite is
    relationship_type: str  # "required", "recommended", "helpful"
    inferred: bool  # Whether this was auto-detected

    def to_dict(self) -> dict:
        return {
            "source_topic": self.source_topic,
            "target_topic": self.target_topic,
            "importance": self.importance,
            "relationship_type": self.relationship_type,
            "inferred": self.inferred,
        }


@dataclass
class TopicReadiness:
    """Assessment of readiness for a topic."""
    topic_id: str
    topic_title: str
    readiness: ReadinessLevel
    prerequisites_met: list[str]
    prerequisites_missing: list[str]
    prerequisites_partial: list[str]  # In progress or needs review
    confidence_score: float  # 0-1
    estimated_prep_time_minutes: int
    suggestions: list[str]

    def to_dict(self) -> dict:
        return {
            "topic_id": self.topic_id,
            "topic_title": self.topic_title,
            "readiness": self.readiness.value,
            "prerequisites_met": self.prerequisites_met,
            "prerequisites_missing": self.prerequisites_missing,
            "prerequisites_partial": self.prerequisites_partial,
            "confidence_score": self.confidence_score,
            "estimated_prep_time_minutes": self.estimated_prep_time_minutes,
            "suggestions": self.suggestions,
        }


@dataclass
class LearningPath:
    """A recommended path to learn a target topic."""
    target_topic: str
    path: list[str]  # Ordered list of topics to complete
    total_estimated_minutes: int
    critical_prerequisites: list[str]
    optional_prerequisites: list[str]

    def to_dict(self) -> dict:
        return {
            "target_topic": self.target_topic,
            "path": self.path,
            "total_estimated_minutes": self.total_estimated_minutes,
            "critical_prerequisites": self.critical_prerequisites,
            "optional_prerequisites": self.optional_prerequisites,
        }


class PrerequisiteManager:
    """
    Manages prerequisite relationships and readiness assessment.

    Features:
    - Auto-infers prerequisites from curriculum
    - Validates topic readiness
    - Generates optimal learning paths
    - Provides remediation suggestions
    """

    # Common implicit prerequisites by subject area
    IMPLICIT_PREREQUISITES = {
        "programming": {
            "functions": ["variables", "types"],
            "loops": ["variables", "conditions"],
            "arrays": ["variables", "loops"],
            "structs": ["variables", "types"],
            "ownership": ["variables", "functions", "references"],
            "borrowing": ["ownership", "references"],
            "lifetimes": ["borrowing", "functions"],
            "generics": ["types", "functions", "structs"],
            "traits": ["generics", "structs"],
            "error_handling": ["types", "enums", "pattern_matching"],
            "async": ["functions", "closures", "traits"],
            "macros": ["functions", "traits", "syntax"],
            "modules": ["functions", "structs", "visibility"],
            "testing": ["functions", "assertions", "modules"],
            "closures": ["functions", "ownership"],
            "iterators": ["loops", "closures", "traits"],
            "smart_pointers": ["ownership", "references", "heap"],
            "concurrency": ["ownership", "threads", "sync"],
        },
        "mathematics": {
            "algebra": ["arithmetic", "variables"],
            "equations": ["algebra", "operations"],
            "functions": ["equations", "graphs"],
            "quadratics": ["algebra", "factoring", "equations"],
            "polynomials": ["algebra", "exponents"],
            "trigonometry": ["geometry", "ratios", "angles"],
            "calculus_limits": ["functions", "infinity"],
            "derivatives": ["limits", "slopes", "functions"],
            "integrals": ["derivatives", "area", "summation"],
            "differential_equations": ["derivatives", "integrals", "equations"],
            "linear_algebra": ["matrices", "vectors", "equations"],
            "probability": ["fractions", "combinations", "statistics_basics"],
            "statistics": ["probability", "mean_median", "distributions"],
        },
        "language": {
            "basic_conversation": ["greetings", "common_phrases"],
            "grammar_basics": ["alphabet", "pronunciation", "vocabulary_basics"],
            "verb_conjugation": ["grammar_basics", "pronouns"],
            "tenses": ["verb_conjugation", "time_expressions"],
            "complex_sentences": ["simple_sentences", "conjunctions", "tenses"],
            "reading": ["vocabulary_intermediate", "grammar_intermediate"],
            "writing": ["reading", "grammar_advanced", "vocabulary_advanced"],
            "listening": ["pronunciation", "vocabulary_intermediate"],
            "speaking": ["listening", "pronunciation", "grammar_intermediate"],
        },
    }

    # Keyword associations for inferring prerequisites
    KEYWORD_ASSOCIATIONS = {
        "programming": {
            "mut": ["ownership", "mutability"],
            "borrow": ["ownership", "references"],
            "&": ["references"],
            "lifetime": ["borrowing", "references"],
            "'a": ["lifetimes"],
            "impl": ["structs", "traits"],
            "trait": ["traits", "generics"],
            "enum": ["types", "pattern_matching"],
            "match": ["pattern_matching", "enums"],
            "Result": ["error_handling", "enums"],
            "Option": ["enums", "null_safety"],
            "async": ["async", "futures"],
            "await": ["async"],
            "Arc": ["smart_pointers", "concurrency"],
            "Rc": ["smart_pointers"],
            "Box": ["heap", "smart_pointers"],
            "Vec": ["arrays", "heap"],
            "HashMap": ["arrays", "hashing"],
            "closure": ["closures", "functions"],
            "iterator": ["iterators", "traits"],
        },
    }

    def __init__(
        self,
        curriculum: dict,
        progress: dict,
        storage_path: Optional[Path] = None
    ):
        """
        Initialize the prerequisite manager.

        Args:
            curriculum: Current curriculum data
            progress: Student progress data
            storage_path: Path to store prerequisite data
        """
        self.curriculum = curriculum
        self.progress = progress
        self.storage_path = storage_path or Path.cwd() / ".tutor" / "prerequisites.json"

        self.prerequisites: dict[str, list[Prerequisite]] = defaultdict(list)
        self.topic_info: dict[str, dict] = {}

        self._load_data()
        self._extract_from_curriculum()
        self._infer_implicit_prerequisites()

    def check_readiness(self, topic_id: str) -> TopicReadiness:
        """
        Check if the student is ready for a topic.

        Args:
            topic_id: The topic to check

        Returns:
            TopicReadiness assessment
        """
        prereqs = self.prerequisites.get(topic_id, [])
        topic_info = self.topic_info.get(topic_id, {})

        met = []
        missing = []
        partial = []

        for prereq in prereqs:
            status = self._get_topic_status(prereq.source_topic)

            if status == PrerequisiteStatus.COMPLETED:
                met.append(prereq.source_topic)
            elif status == PrerequisiteStatus.NOT_STARTED:
                missing.append(prereq.source_topic)
            else:  # IN_PROGRESS or NEEDS_REVIEW
                partial.append(prereq.source_topic)

        # Determine readiness level
        required_prereqs = [p for p in prereqs if p.relationship_type == "required"]
        required_missing = [p.source_topic for p in required_prereqs if p.source_topic in missing]

        if not missing and not partial:
            readiness = ReadinessLevel.READY
            confidence = 1.0
        elif required_missing:
            readiness = ReadinessLevel.BLOCKED
            confidence = 0.2
        elif missing:
            readiness = ReadinessLevel.NOT_READY
            confidence = 0.4
        elif partial:
            readiness = ReadinessLevel.MOSTLY_READY
            confidence = 0.7
        else:
            readiness = ReadinessLevel.READY
            confidence = 0.9

        # Estimate prep time
        prep_time = len(missing) * 30 + len(partial) * 15  # minutes

        # Generate suggestions
        suggestions = []
        if required_missing:
            suggestions.append(
                f"Complete these required prerequisites first: {', '.join(required_missing[:3])}"
            )
        if partial:
            suggestions.append(
                f"Finish or review: {', '.join(partial[:3])}"
            )
        if readiness == ReadinessLevel.READY:
            suggestions.append("You're ready to start this topic!")

        return TopicReadiness(
            topic_id=topic_id,
            topic_title=topic_info.get("title", topic_id),
            readiness=readiness,
            prerequisites_met=met,
            prerequisites_missing=missing,
            prerequisites_partial=partial,
            confidence_score=confidence,
            estimated_prep_time_minutes=prep_time,
            suggestions=suggestions,
        )

    def get_learning_path(self, target_topic: str) -> LearningPath:
        """
        Generate an optimal learning path to a target topic.

        Args:
            target_topic: The topic to learn

        Returns:
            LearningPath with ordered topics
        """
        # Build dependency graph
        all_prereqs = self._get_all_prerequisites(target_topic)

        # Topological sort
        path = self._topological_sort(target_topic, all_prereqs)

        # Filter out completed topics
        completed = self._get_completed_topics()
        path = [t for t in path if t not in completed]

        # Separate critical vs optional
        critical = []
        optional = []

        for topic in path:
            prereqs = self.prerequisites.get(target_topic, [])
            is_required = any(
                p.source_topic == topic and p.relationship_type == "required"
                for p in prereqs
            )
            if is_required:
                critical.append(topic)
            else:
                optional.append(topic)

        # Estimate time
        total_time = len(path) * 30  # 30 min per topic average

        return LearningPath(
            target_topic=target_topic,
            path=path,
            total_estimated_minutes=total_time,
            critical_prerequisites=critical,
            optional_prerequisites=optional,
        )

    def add_prerequisite(
        self,
        source_topic: str,
        target_topic: str,
        importance: float = 0.8,
        relationship_type: str = "required",
    ) -> None:
        """
        Add a prerequisite relationship.

        Args:
            source_topic: The prerequisite topic
            target_topic: The topic that requires it
            importance: How important (0-1)
            relationship_type: "required", "recommended", "helpful"
        """
        prereq = Prerequisite(
            source_topic=source_topic,
            target_topic=target_topic,
            importance=importance,
            relationship_type=relationship_type,
            inferred=False,
        )

        # Avoid duplicates
        existing = [p for p in self.prerequisites[target_topic] if p.source_topic == source_topic]
        if not existing:
            self.prerequisites[target_topic].append(prereq)
            self._save_data()

    def get_prerequisites_for(self, topic_id: str) -> list[Prerequisite]:
        """Get all prerequisites for a topic."""
        return self.prerequisites.get(topic_id, [])

    def get_topics_requiring(self, topic_id: str) -> list[str]:
        """Get all topics that require this topic as a prerequisite."""
        requiring = []
        for target, prereqs in self.prerequisites.items():
            if any(p.source_topic == topic_id for p in prereqs):
                requiring.append(target)
        return requiring

    def validate_curriculum_order(self) -> list[dict]:
        """
        Validate that the curriculum order respects prerequisites.

        Returns:
            List of issues found
        """
        issues = []
        modules = self.curriculum.get("modules", [])

        topic_order = []
        for module in modules:
            topics = module.get("topics", [])
            for topic in topics:
                topic_id = topic.get("id") if isinstance(topic, dict) else topic
                topic_order.append(topic_id)

        for i, topic_id in enumerate(topic_order):
            prereqs = self.prerequisites.get(topic_id, [])
            for prereq in prereqs:
                if prereq.relationship_type == "required":
                    try:
                        prereq_idx = topic_order.index(prereq.source_topic)
                        if prereq_idx > i:
                            issues.append({
                                "type": "order_violation",
                                "topic": topic_id,
                                "prerequisite": prereq.source_topic,
                                "message": f"'{topic_id}' appears before its prerequisite '{prereq.source_topic}'",
                            })
                    except ValueError:
                        issues.append({
                            "type": "missing_prerequisite",
                            "topic": topic_id,
                            "prerequisite": prereq.source_topic,
                            "message": f"Prerequisite '{prereq.source_topic}' for '{topic_id}' not in curriculum",
                        })

        return issues

    def suggest_curriculum_improvements(self) -> list[dict]:
        """
        Suggest improvements to curriculum based on prerequisite analysis.

        Returns:
            List of suggestions
        """
        suggestions = []

        # Check for order issues
        issues = self.validate_curriculum_order()
        for issue in issues:
            suggestions.append({
                "type": "reorder",
                "priority": "high",
                "suggestion": issue["message"],
            })

        # Check for missing foundational topics
        all_prereqs = set()
        all_topics = set()

        for module in self.curriculum.get("modules", []):
            for topic in module.get("topics", []):
                topic_id = topic.get("id") if isinstance(topic, dict) else topic
                all_topics.add(topic_id)

        for prereqs in self.prerequisites.values():
            for prereq in prereqs:
                all_prereqs.add(prereq.source_topic)

        missing_foundations = all_prereqs - all_topics
        for missing in missing_foundations:
            suggestions.append({
                "type": "add_topic",
                "priority": "medium",
                "topic": missing,
                "suggestion": f"Consider adding '{missing}' as a foundational topic",
            })

        return suggestions

    def _extract_from_curriculum(self) -> None:
        """Extract explicit prerequisites from curriculum."""
        for module in self.curriculum.get("modules", []):
            module_id = module.get("id")

            # Module-level prerequisites
            for prereq_id in module.get("prerequisites", []):
                self.add_prerequisite(
                    source_topic=prereq_id,
                    target_topic=module_id,
                    importance=0.9,
                    relationship_type="required",
                )

            # Topic-level information
            for topic in module.get("topics", []):
                if isinstance(topic, dict):
                    topic_id = topic.get("id")
                    self.topic_info[topic_id] = topic

                    # Topic prerequisites
                    for prereq_id in topic.get("prerequisites", []):
                        self.add_prerequisite(
                            source_topic=prereq_id,
                            target_topic=topic_id,
                            importance=0.8,
                            relationship_type="required",
                        )

    def _infer_implicit_prerequisites(self) -> None:
        """Infer prerequisites based on common patterns."""
        subject_type = self.curriculum.get("subject_type", "programming")
        implicit_map = self.IMPLICIT_PREREQUISITES.get(subject_type, {})

        for module in self.curriculum.get("modules", []):
            for topic in module.get("topics", []):
                topic_id = topic.get("id") if isinstance(topic, dict) else topic
                topic_lower = topic_id.lower()

                # Check against implicit prerequisites
                for target_key, prereq_list in implicit_map.items():
                    if target_key in topic_lower:
                        for prereq in prereq_list:
                            # Only add if prerequisite exists in curriculum
                            if self._topic_exists(prereq):
                                existing = [
                                    p for p in self.prerequisites[topic_id]
                                    if p.source_topic == prereq
                                ]
                                if not existing:
                                    self.prerequisites[topic_id].append(Prerequisite(
                                        source_topic=prereq,
                                        target_topic=topic_id,
                                        importance=0.6,
                                        relationship_type="recommended",
                                        inferred=True,
                                    ))

    def _topic_exists(self, topic_id: str) -> bool:
        """Check if a topic exists in the curriculum."""
        for module in self.curriculum.get("modules", []):
            if module.get("id") == topic_id:
                return True
            for topic in module.get("topics", []):
                t_id = topic.get("id") if isinstance(topic, dict) else topic
                if t_id == topic_id:
                    return True
        return False

    def _get_topic_status(self, topic_id: str) -> PrerequisiteStatus:
        """Get the completion status of a topic."""
        modules_progress = self.progress.get("modules", {})

        for module_id, module_data in modules_progress.items():
            if module_id == topic_id:
                status = module_data.get("status", "not_started")
                if status == "completed":
                    return PrerequisiteStatus.COMPLETED
                elif status == "in_progress":
                    return PrerequisiteStatus.IN_PROGRESS

            exercises = module_data.get("exercises", {})
            if topic_id in exercises:
                ex_status = exercises[topic_id].get("status", "not_started")
                if ex_status == "completed":
                    return PrerequisiteStatus.COMPLETED
                elif ex_status == "in_progress":
                    return PrerequisiteStatus.IN_PROGRESS

        return PrerequisiteStatus.NOT_STARTED

    def _get_completed_topics(self) -> set[str]:
        """Get set of completed topic IDs."""
        completed = set()
        for module_id, module_data in self.progress.get("modules", {}).items():
            if module_data.get("status") == "completed":
                completed.add(module_id)
            for ex_id, ex_data in module_data.get("exercises", {}).items():
                if ex_data.get("status") == "completed":
                    completed.add(f"{module_id}:{ex_id}")
        return completed

    def _get_all_prerequisites(self, topic_id: str, visited: Optional[set] = None) -> set[str]:
        """Recursively get all prerequisites for a topic."""
        if visited is None:
            visited = set()

        if topic_id in visited:
            return set()

        visited.add(topic_id)
        prereqs = set()

        for prereq in self.prerequisites.get(topic_id, []):
            prereqs.add(prereq.source_topic)
            prereqs.update(self._get_all_prerequisites(prereq.source_topic, visited))

        return prereqs

    def _topological_sort(self, target: str, all_prereqs: set[str]) -> list[str]:
        """Sort topics in dependency order."""
        # Build adjacency list
        graph = defaultdict(list)
        in_degree = defaultdict(int)

        topics = all_prereqs | {target}

        for topic in topics:
            in_degree[topic] = 0

        for topic in topics:
            for prereq in self.prerequisites.get(topic, []):
                if prereq.source_topic in topics:
                    graph[prereq.source_topic].append(topic)
                    in_degree[topic] += 1

        # Kahn's algorithm
        queue = [t for t in topics if in_degree[t] == 0]
        result = []

        while queue:
            node = queue.pop(0)
            result.append(node)

            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return result

    def _load_data(self) -> None:
        """Load prerequisite data from storage."""
        if not self.storage_path.exists():
            return

        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for item in data.get("prerequisites", []):
                prereq = Prerequisite(
                    source_topic=item["source_topic"],
                    target_topic=item["target_topic"],
                    importance=item["importance"],
                    relationship_type=item["relationship_type"],
                    inferred=item.get("inferred", False),
                )
                self.prerequisites[prereq.target_topic].append(prereq)

        except (json.JSONDecodeError, KeyError, ValueError):
            pass

    def _save_data(self) -> None:
        """Save prerequisite data to storage."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        all_prereqs = []
        for prereqs in self.prerequisites.values():
            all_prereqs.extend([p.to_dict() for p in prereqs if not p.inferred])

        data = {
            "prerequisites": all_prereqs,
            "updated_at": datetime.now().isoformat(),
        }

        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
