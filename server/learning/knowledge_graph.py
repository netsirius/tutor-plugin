"""
Knowledge Graph

Represents the relationships between topics, concepts, and skills.
Used for intelligent navigation and prerequisite tracking.
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import json
from pathlib import Path


class RelationType(Enum):
    """Types of relationships between topics."""
    PREREQUISITE = "prerequisite"  # A must be learned before B
    RELATED = "related"  # A and B are related but independent
    BUILDS_ON = "builds_on"  # B extends A
    ALTERNATIVE = "alternative"  # B is an alternative to A
    PART_OF = "part_of"  # A is part of B


@dataclass
class Topic:
    """A topic or concept in the knowledge graph."""
    topic_id: str
    title: str
    description: str = ""
    subject: str = "programming"  # programming, math, science, language, etc.
    difficulty: int = 1  # 1-5
    estimated_minutes: int = 30
    keywords: list[str] = field(default_factory=list)
    resources: list[str] = field(default_factory=list)  # URLs or file paths

    def to_dict(self) -> dict:
        return {
            "topic_id": self.topic_id,
            "title": self.title,
            "description": self.description,
            "subject": self.subject,
            "difficulty": self.difficulty,
            "estimated_minutes": self.estimated_minutes,
            "keywords": self.keywords,
            "resources": self.resources,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Topic":
        return cls(
            topic_id=data["topic_id"],
            title=data["title"],
            description=data.get("description", ""),
            subject=data.get("subject", "programming"),
            difficulty=data.get("difficulty", 1),
            estimated_minutes=data.get("estimated_minutes", 30),
            keywords=data.get("keywords", []),
            resources=data.get("resources", []),
        )


@dataclass
class Prerequisite:
    """A prerequisite relationship between topics."""
    from_topic: str  # Topic ID that is required
    to_topic: str  # Topic ID that requires it
    relation_type: RelationType = RelationType.PREREQUISITE
    strength: float = 1.0  # 0.0-1.0, how strongly required

    def to_dict(self) -> dict:
        return {
            "from_topic": self.from_topic,
            "to_topic": self.to_topic,
            "relation_type": self.relation_type.value,
            "strength": self.strength,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Prerequisite":
        return cls(
            from_topic=data["from_topic"],
            to_topic=data["to_topic"],
            relation_type=RelationType(data.get("relation_type", "prerequisite")),
            strength=data.get("strength", 1.0),
        )


class KnowledgeGraph:
    """
    A graph of topics and their relationships.

    Supports:
    - Finding prerequisites for a topic
    - Finding related topics
    - Computing learning paths
    - Identifying knowledge gaps
    """

    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize the knowledge graph.

        Args:
            storage_path: Path to store graph data
        """
        self.storage_path = storage_path or Path.cwd() / ".tutor" / "knowledge_graph.json"
        self.topics: dict[str, Topic] = {}
        self.edges: list[Prerequisite] = []
        self._adjacency: dict[str, list[str]] = {}  # topic -> [prerequisite topics]
        self._reverse_adjacency: dict[str, list[str]] = {}  # topic -> [topics that depend on it]
        self._load()

    def add_topic(self, topic: Topic) -> None:
        """Add a topic to the graph."""
        self.topics[topic.topic_id] = topic
        if topic.topic_id not in self._adjacency:
            self._adjacency[topic.topic_id] = []
        if topic.topic_id not in self._reverse_adjacency:
            self._reverse_adjacency[topic.topic_id] = []
        self._save()

    def add_prerequisite(self, prerequisite: Prerequisite) -> None:
        """Add a prerequisite relationship."""
        self.edges.append(prerequisite)

        # Update adjacency lists
        if prerequisite.to_topic not in self._adjacency:
            self._adjacency[prerequisite.to_topic] = []
        self._adjacency[prerequisite.to_topic].append(prerequisite.from_topic)

        if prerequisite.from_topic not in self._reverse_adjacency:
            self._reverse_adjacency[prerequisite.from_topic] = []
        self._reverse_adjacency[prerequisite.from_topic].append(prerequisite.to_topic)

        self._save()

    def get_prerequisites(self, topic_id: str, recursive: bool = True) -> list[str]:
        """
        Get prerequisites for a topic.

        Args:
            topic_id: Topic to get prerequisites for
            recursive: If True, get all transitive prerequisites

        Returns:
            List of prerequisite topic IDs
        """
        if topic_id not in self._adjacency:
            return []

        if not recursive:
            return self._adjacency[topic_id].copy()

        # BFS for all transitive prerequisites
        visited = set()
        queue = self._adjacency.get(topic_id, []).copy()
        result = []

        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            result.append(current)
            queue.extend(self._adjacency.get(current, []))

        return result

    def get_dependents(self, topic_id: str, recursive: bool = True) -> list[str]:
        """
        Get topics that depend on this topic.

        Args:
            topic_id: Topic to get dependents for
            recursive: If True, get all transitive dependents

        Returns:
            List of dependent topic IDs
        """
        if topic_id not in self._reverse_adjacency:
            return []

        if not recursive:
            return self._reverse_adjacency[topic_id].copy()

        # BFS for all transitive dependents
        visited = set()
        queue = self._reverse_adjacency.get(topic_id, []).copy()
        result = []

        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            result.append(current)
            queue.extend(self._reverse_adjacency.get(current, []))

        return result

    def get_learning_path(
        self,
        target_topics: list[str],
        completed_topics: Optional[set[str]] = None
    ) -> list[str]:
        """
        Compute an optimal learning path to reach target topics.

        Uses topological sort with priority by:
        1. Prerequisites first
        2. Lower difficulty first
        3. Shorter time first

        Args:
            target_topics: Topics to learn
            completed_topics: Topics already mastered (to skip)

        Returns:
            Ordered list of topic IDs to learn
        """
        completed = completed_topics or set()

        # Collect all required topics
        required = set()
        for target in target_topics:
            if target not in completed:
                required.add(target)
                for prereq in self.get_prerequisites(target, recursive=True):
                    if prereq not in completed:
                        required.add(prereq)

        # Topological sort with Kahn's algorithm
        # Count incoming edges for each topic
        in_degree = {t: 0 for t in required}
        for topic in required:
            for prereq in self._adjacency.get(topic, []):
                if prereq in required:
                    in_degree[topic] += 1

        # Start with topics that have no prerequisites (in required set)
        queue = [t for t in required if in_degree[t] == 0]

        # Sort by difficulty and time
        def priority(topic_id):
            topic = self.topics.get(topic_id)
            if topic:
                return (topic.difficulty, topic.estimated_minutes)
            return (5, 60)

        queue.sort(key=priority)

        result = []
        while queue:
            # Take highest priority (lowest difficulty/time)
            queue.sort(key=priority)
            current = queue.pop(0)
            result.append(current)

            # Update in-degrees
            for dependent in self._reverse_adjacency.get(current, []):
                if dependent in required:
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        queue.append(dependent)

        return result

    def get_related_topics(
        self,
        topic_id: str,
        max_distance: int = 2
    ) -> list[tuple[str, int]]:
        """
        Get topics related to a given topic.

        Args:
            topic_id: Starting topic
            max_distance: Maximum graph distance

        Returns:
            List of (topic_id, distance) tuples
        """
        if topic_id not in self.topics:
            return []

        # BFS to find nearby topics
        visited = {topic_id: 0}
        queue = [(topic_id, 0)]
        result = []

        while queue:
            current, distance = queue.pop(0)

            if distance > 0:
                result.append((current, distance))

            if distance >= max_distance:
                continue

            # Add neighbors (prerequisites and dependents)
            neighbors = (
                self._adjacency.get(current, []) +
                self._reverse_adjacency.get(current, [])
            )

            for neighbor in neighbors:
                if neighbor not in visited:
                    visited[neighbor] = distance + 1
                    queue.append((neighbor, distance + 1))

        result.sort(key=lambda x: x[1])
        return result

    def find_gaps(
        self,
        completed_topics: set[str],
        target_topics: list[str]
    ) -> list[str]:
        """
        Find topics that are missing to reach targets.

        Args:
            completed_topics: Topics already learned
            target_topics: Topics to reach

        Returns:
            List of missing topic IDs
        """
        missing = []

        for target in target_topics:
            if target in completed_topics:
                continue

            missing.append(target)

            for prereq in self.get_prerequisites(target, recursive=True):
                if prereq not in completed_topics and prereq not in missing:
                    missing.append(prereq)

        return missing

    def suggest_next_topics(
        self,
        completed_topics: set[str],
        limit: int = 5
    ) -> list[str]:
        """
        Suggest next topics to learn based on completed topics.

        Suggests topics whose prerequisites are met.

        Args:
            completed_topics: Topics already learned
            limit: Maximum suggestions

        Returns:
            List of suggested topic IDs
        """
        suggestions = []

        for topic_id in self.topics:
            if topic_id in completed_topics:
                continue

            # Check if all prerequisites are met
            prereqs = self.get_prerequisites(topic_id, recursive=False)
            if all(p in completed_topics for p in prereqs):
                suggestions.append(topic_id)

        # Sort by difficulty and estimated time
        def priority(tid):
            topic = self.topics.get(tid)
            return (topic.difficulty, topic.estimated_minutes) if topic else (5, 60)

        suggestions.sort(key=priority)
        return suggestions[:limit]

    def search_topics(self, query: str) -> list[Topic]:
        """
        Search for topics by keyword.

        Args:
            query: Search query

        Returns:
            List of matching topics
        """
        query_lower = query.lower()
        results = []

        for topic in self.topics.values():
            # Check title, description, and keywords
            if (
                query_lower in topic.title.lower() or
                query_lower in topic.description.lower() or
                any(query_lower in k.lower() for k in topic.keywords)
            ):
                results.append(topic)

        return results

    def get_statistics(self) -> dict:
        """Get statistics about the knowledge graph."""
        return {
            "total_topics": len(self.topics),
            "total_edges": len(self.edges),
            "topics_by_subject": self._count_by_subject(),
            "topics_by_difficulty": self._count_by_difficulty(),
            "average_prerequisites": sum(len(v) for v in self._adjacency.values()) / max(1, len(self.topics)),
        }

    def _count_by_subject(self) -> dict[str, int]:
        """Count topics by subject."""
        counts: dict[str, int] = {}
        for topic in self.topics.values():
            counts[topic.subject] = counts.get(topic.subject, 0) + 1
        return counts

    def _count_by_difficulty(self) -> dict[int, int]:
        """Count topics by difficulty."""
        counts: dict[int, int] = {}
        for topic in self.topics.values():
            counts[topic.difficulty] = counts.get(topic.difficulty, 0) + 1
        return counts

    def _load(self):
        """Load graph from storage."""
        if not self.storage_path.exists():
            return

        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for topic_data in data.get("topics", []):
                topic = Topic.from_dict(topic_data)
                self.topics[topic.topic_id] = topic

            for edge_data in data.get("edges", []):
                edge = Prerequisite.from_dict(edge_data)
                self.edges.append(edge)

            # Rebuild adjacency lists
            self._rebuild_adjacency()

        except (json.JSONDecodeError, KeyError):
            pass

    def _save(self):
        """Save graph to storage."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "version": 1,
            "topics": [t.to_dict() for t in self.topics.values()],
            "edges": [e.to_dict() for e in self.edges],
        }

        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _rebuild_adjacency(self):
        """Rebuild adjacency lists from edges."""
        self._adjacency = {t: [] for t in self.topics}
        self._reverse_adjacency = {t: [] for t in self.topics}

        for edge in self.edges:
            if edge.to_topic not in self._adjacency:
                self._adjacency[edge.to_topic] = []
            self._adjacency[edge.to_topic].append(edge.from_topic)

            if edge.from_topic not in self._reverse_adjacency:
                self._reverse_adjacency[edge.from_topic] = []
            self._reverse_adjacency[edge.from_topic].append(edge.to_topic)
