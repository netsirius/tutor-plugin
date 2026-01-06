"""
Structured Evaluation System

Supports multiple evaluation types:
- Code exercises (with test execution)
- Multiple choice questions
- Free text responses
- Math problems (process and result)
- Translations
- Fill-in-the-blank
- Matching exercises
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import json
from pathlib import Path


class ExerciseType(Enum):
    """Types of exercises that can be evaluated."""
    CODE = "code"
    MULTIPLE_CHOICE = "multiple_choice"
    FREE_TEXT = "free_text"
    MATH = "math"
    TRANSLATION = "translation"
    FILL_BLANK = "fill_blank"
    MATCHING = "matching"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    ESSAY = "essay"


@dataclass
class EvaluationCriterion:
    """A single criterion for evaluation."""
    name: str
    description: str
    max_points: int
    weight: float = 1.0


@dataclass
class CriterionResult:
    """Result for a single evaluation criterion."""
    criterion: str
    points_earned: int
    max_points: int
    feedback: str
    passed: bool


@dataclass
class EvaluationResult:
    """Complete result of an exercise evaluation."""
    exercise_id: str
    exercise_type: ExerciseType
    score: int  # 0-100
    passed: bool
    feedback: str
    detailed_feedback: str
    criteria_results: list[CriterionResult]
    misconceptions: list[str]
    strengths: list[str]
    suggestions: list[str]
    time_spent_seconds: Optional[int]
    attempts: int
    evaluated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "exercise_id": self.exercise_id,
            "exercise_type": self.exercise_type.value,
            "score": self.score,
            "passed": self.passed,
            "feedback": self.feedback,
            "detailed_feedback": self.detailed_feedback,
            "criteria_results": [
                {
                    "criterion": cr.criterion,
                    "points_earned": cr.points_earned,
                    "max_points": cr.max_points,
                    "feedback": cr.feedback,
                    "passed": cr.passed,
                }
                for cr in self.criteria_results
            ],
            "misconceptions": self.misconceptions,
            "strengths": self.strengths,
            "suggestions": self.suggestions,
            "time_spent_seconds": self.time_spent_seconds,
            "attempts": self.attempts,
            "evaluated_at": self.evaluated_at.isoformat(),
        }


@dataclass
class ExerciseDefinition:
    """Definition of an exercise for evaluation."""
    exercise_id: str
    exercise_type: ExerciseType
    title: str
    description: str
    criteria: list[EvaluationCriterion]
    passing_score: int = 60
    max_attempts: Optional[int] = None
    hints_available: int = 3
    time_limit_minutes: Optional[int] = None

    # Type-specific fields
    correct_answer: Optional[str] = None  # For multiple choice, true/false
    correct_answers: Optional[list[str]] = None  # For multiple correct answers
    answer_key: Optional[dict] = None  # For matching exercises
    rubric: Optional[dict] = None  # For essay/free text
    test_cases: Optional[list[dict]] = None  # For code exercises
    acceptable_answers: Optional[list[str]] = None  # For short answer

    def to_dict(self) -> dict:
        return {
            "exercise_id": self.exercise_id,
            "exercise_type": self.exercise_type.value,
            "title": self.title,
            "description": self.description,
            "criteria": [
                {
                    "name": c.name,
                    "description": c.description,
                    "max_points": c.max_points,
                    "weight": c.weight,
                }
                for c in self.criteria
            ],
            "passing_score": self.passing_score,
            "max_attempts": self.max_attempts,
            "hints_available": self.hints_available,
            "time_limit_minutes": self.time_limit_minutes,
        }


class EvaluationEngine:
    """
    Engine for evaluating different types of exercises.

    Note: This provides structure and tracking. The actual evaluation
    logic is performed by Claude, which can assess any type of response.
    """

    # Default criteria by exercise type
    DEFAULT_CRITERIA = {
        ExerciseType.CODE: [
            EvaluationCriterion("correctness", "Code produces correct output", 40),
            EvaluationCriterion("tests_pass", "All tests pass", 30),
            EvaluationCriterion("code_quality", "Clean, readable code", 15),
            EvaluationCriterion("efficiency", "Efficient solution", 15),
        ],
        ExerciseType.MULTIPLE_CHOICE: [
            EvaluationCriterion("correct_selection", "Correct answer selected", 100),
        ],
        ExerciseType.FREE_TEXT: [
            EvaluationCriterion("accuracy", "Factually accurate", 40),
            EvaluationCriterion("completeness", "Covers all key points", 30),
            EvaluationCriterion("clarity", "Clear and well-organized", 20),
            EvaluationCriterion("depth", "Shows understanding", 10),
        ],
        ExerciseType.MATH: [
            EvaluationCriterion("correct_answer", "Final answer is correct", 40),
            EvaluationCriterion("process", "Shows correct work/process", 40),
            EvaluationCriterion("notation", "Proper mathematical notation", 10),
            EvaluationCriterion("explanation", "Clear explanation", 10),
        ],
        ExerciseType.TRANSLATION: [
            EvaluationCriterion("accuracy", "Meaning preserved", 40),
            EvaluationCriterion("grammar", "Grammatically correct", 25),
            EvaluationCriterion("vocabulary", "Appropriate word choices", 20),
            EvaluationCriterion("naturalness", "Sounds natural", 15),
        ],
        ExerciseType.FILL_BLANK: [
            EvaluationCriterion("correct_answers", "Blanks filled correctly", 100),
        ],
        ExerciseType.MATCHING: [
            EvaluationCriterion("correct_matches", "Items matched correctly", 100),
        ],
        ExerciseType.TRUE_FALSE: [
            EvaluationCriterion("correct_answer", "Correct answer selected", 100),
        ],
        ExerciseType.SHORT_ANSWER: [
            EvaluationCriterion("accuracy", "Answer is correct", 60),
            EvaluationCriterion("completeness", "Answer is complete", 40),
        ],
        ExerciseType.ESSAY: [
            EvaluationCriterion("thesis", "Clear thesis/main argument", 20),
            EvaluationCriterion("evidence", "Supporting evidence", 25),
            EvaluationCriterion("organization", "Logical organization", 20),
            EvaluationCriterion("analysis", "Critical analysis", 25),
            EvaluationCriterion("writing", "Writing quality", 10),
        ],
    }

    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize the evaluation engine.

        Args:
            storage_path: Path to store evaluation history
        """
        self.storage_path = storage_path or Path.cwd() / ".tutor" / "evaluations.json"
        self.evaluations: list[EvaluationResult] = []
        self._load_history()

    def get_criteria_for_type(self, exercise_type: ExerciseType) -> list[EvaluationCriterion]:
        """Get default evaluation criteria for an exercise type."""
        return self.DEFAULT_CRITERIA.get(exercise_type, [])

    def create_exercise(
        self,
        exercise_id: str,
        exercise_type: ExerciseType,
        title: str,
        description: str,
        custom_criteria: Optional[list[EvaluationCriterion]] = None,
        **kwargs
    ) -> ExerciseDefinition:
        """
        Create an exercise definition.

        Args:
            exercise_id: Unique identifier
            exercise_type: Type of exercise
            title: Exercise title
            description: Exercise description
            custom_criteria: Custom evaluation criteria (uses defaults if None)
            **kwargs: Type-specific parameters

        Returns:
            ExerciseDefinition ready for evaluation
        """
        criteria = custom_criteria or self.get_criteria_for_type(exercise_type)

        return ExerciseDefinition(
            exercise_id=exercise_id,
            exercise_type=exercise_type,
            title=title,
            description=description,
            criteria=criteria,
            **kwargs
        )

    def record_evaluation(
        self,
        exercise_id: str,
        exercise_type: ExerciseType,
        score: int,
        feedback: str,
        detailed_feedback: str = "",
        criteria_results: Optional[list[CriterionResult]] = None,
        misconceptions: Optional[list[str]] = None,
        strengths: Optional[list[str]] = None,
        suggestions: Optional[list[str]] = None,
        time_spent_seconds: Optional[int] = None,
        attempts: int = 1,
    ) -> EvaluationResult:
        """
        Record an evaluation result.

        Args:
            exercise_id: Exercise identifier
            exercise_type: Type of exercise
            score: Score achieved (0-100)
            feedback: Brief feedback message
            detailed_feedback: Detailed explanation
            criteria_results: Results for each criterion
            misconceptions: Identified misconceptions
            strengths: Identified strengths
            suggestions: Suggestions for improvement
            time_spent_seconds: Time taken
            attempts: Number of attempts

        Returns:
            EvaluationResult
        """
        result = EvaluationResult(
            exercise_id=exercise_id,
            exercise_type=exercise_type,
            score=score,
            passed=score >= 60,
            feedback=feedback,
            detailed_feedback=detailed_feedback,
            criteria_results=criteria_results or [],
            misconceptions=misconceptions or [],
            strengths=strengths or [],
            suggestions=suggestions or [],
            time_spent_seconds=time_spent_seconds,
            attempts=attempts,
        )

        self.evaluations.append(result)
        self._save_history()

        return result

    def get_evaluation_history(
        self,
        exercise_id: Optional[str] = None,
        exercise_type: Optional[ExerciseType] = None,
        limit: int = 50,
    ) -> list[EvaluationResult]:
        """
        Get evaluation history with optional filters.

        Args:
            exercise_id: Filter by exercise ID
            exercise_type: Filter by exercise type
            limit: Maximum results to return

        Returns:
            List of evaluation results
        """
        results = self.evaluations

        if exercise_id:
            results = [r for r in results if r.exercise_id == exercise_id]

        if exercise_type:
            results = [r for r in results if r.exercise_type == exercise_type]

        return results[-limit:]

    def get_statistics_by_type(self) -> dict[str, dict]:
        """
        Get evaluation statistics grouped by exercise type.

        Returns:
            Statistics for each exercise type
        """
        stats = {}

        for exercise_type in ExerciseType:
            type_results = [
                r for r in self.evaluations
                if r.exercise_type == exercise_type
            ]

            if not type_results:
                continue

            scores = [r.score for r in type_results]
            passed = sum(1 for r in type_results if r.passed)

            stats[exercise_type.value] = {
                "total_attempts": len(type_results),
                "passed": passed,
                "failed": len(type_results) - passed,
                "pass_rate": passed / len(type_results) * 100,
                "average_score": sum(scores) / len(scores),
                "highest_score": max(scores),
                "lowest_score": min(scores),
            }

        return stats

    def get_common_misconceptions(self, limit: int = 10) -> list[tuple[str, int]]:
        """
        Get most common misconceptions across all evaluations.

        Args:
            limit: Maximum misconceptions to return

        Returns:
            List of (misconception, count) tuples
        """
        misconception_counts: dict[str, int] = {}

        for result in self.evaluations:
            for misconception in result.misconceptions:
                misconception_counts[misconception] = misconception_counts.get(misconception, 0) + 1

        sorted_misconceptions = sorted(
            misconception_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_misconceptions[:limit]

    def _load_history(self) -> None:
        """Load evaluation history from storage."""
        if not self.storage_path.exists():
            return

        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for item in data.get("evaluations", []):
                result = EvaluationResult(
                    exercise_id=item["exercise_id"],
                    exercise_type=ExerciseType(item["exercise_type"]),
                    score=item["score"],
                    passed=item["passed"],
                    feedback=item["feedback"],
                    detailed_feedback=item.get("detailed_feedback", ""),
                    criteria_results=[
                        CriterionResult(
                            criterion=cr["criterion"],
                            points_earned=cr["points_earned"],
                            max_points=cr["max_points"],
                            feedback=cr["feedback"],
                            passed=cr["passed"],
                        )
                        for cr in item.get("criteria_results", [])
                    ],
                    misconceptions=item.get("misconceptions", []),
                    strengths=item.get("strengths", []),
                    suggestions=item.get("suggestions", []),
                    time_spent_seconds=item.get("time_spent_seconds"),
                    attempts=item.get("attempts", 1),
                    evaluated_at=datetime.fromisoformat(item["evaluated_at"]),
                )
                self.evaluations.append(result)
        except (json.JSONDecodeError, KeyError, ValueError):
            pass

    def _save_history(self) -> None:
        """Save evaluation history to storage."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "evaluations": [e.to_dict() for e in self.evaluations],
            "updated_at": datetime.now().isoformat(),
        }

        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


# Evaluation prompt templates for Claude
EVALUATION_PROMPTS = {
    ExerciseType.CODE: """
Evaluate this code submission:

**Exercise:** {title}
**Description:** {description}

**Student's Code:**
```
{submission}
```

Evaluate based on these criteria:
{criteria}

Provide:
1. Score (0-100)
2. Brief feedback (1-2 sentences)
3. Detailed feedback explaining what's good and what needs improvement
4. Any misconceptions identified
5. Strengths shown
6. Suggestions for improvement
""",

    ExerciseType.MULTIPLE_CHOICE: """
Evaluate this multiple choice response:

**Question:** {description}
**Options:** {options}
**Correct Answer:** {correct_answer}
**Student's Answer:** {submission}

Provide:
1. Score (0 or 100)
2. Brief feedback
3. If wrong, explain why the correct answer is right
4. Any misconceptions shown by the wrong answer
""",

    ExerciseType.MATH: """
Evaluate this math problem solution:

**Problem:** {description}
**Expected Answer:** {correct_answer}

**Student's Work:**
{submission}

Evaluate based on:
- Final answer correctness (40%)
- Process/work shown (40%)
- Mathematical notation (10%)
- Explanation clarity (10%)

Provide:
1. Score (0-100)
2. Brief feedback
3. Detailed feedback on the solution process
4. Any mathematical misconceptions
5. Suggestions for improvement
""",

    ExerciseType.TRANSLATION: """
Evaluate this translation:

**Source Text ({source_lang}):** {source_text}
**Target Language:** {target_lang}

**Student's Translation:**
{submission}

Evaluate based on:
- Meaning preservation (40%)
- Grammar correctness (25%)
- Vocabulary appropriateness (20%)
- Naturalness (15%)

Provide:
1. Score (0-100)
2. Brief feedback
3. Detailed feedback with specific corrections
4. Common mistakes identified
5. Suggestions for improvement
""",

    ExerciseType.FREE_TEXT: """
Evaluate this free text response:

**Question/Prompt:** {description}
**Key Points Expected:** {key_points}

**Student's Response:**
{submission}

Evaluate based on:
- Accuracy (40%)
- Completeness (30%)
- Clarity (20%)
- Depth of understanding (10%)

Provide:
1. Score (0-100)
2. Brief feedback
3. Detailed feedback
4. Missing key points
5. Misconceptions if any
6. Suggestions for improvement
""",
}
