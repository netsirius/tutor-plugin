"""
Export/Import System (Simplified)

Allows students to:
- Export their learning progress to JSON or Markdown
- Import progress from a backup file
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import json
from enum import Enum


class ExportFormat(Enum):
    """Available export formats."""
    JSON = "json"
    MARKDOWN = "md"


@dataclass
class ExportResult:
    """Result of an export operation."""
    format: ExportFormat
    filepath: Path
    size_bytes: int
    created_at: datetime
    includes: list[str]

    def to_dict(self) -> dict:
        return {
            "format": self.format.value,
            "filepath": str(self.filepath),
            "size_bytes": self.size_bytes,
            "created_at": self.created_at.isoformat(),
            "includes": self.includes,
        }


@dataclass
class ImportResult:
    """Result of an import operation."""
    success: bool
    items_imported: dict[str, int]
    warnings: list[str]
    errors: list[str]

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "items_imported": self.items_imported,
            "warnings": self.warnings,
            "errors": self.errors,
        }


class ProgressExporter:
    """Handles exporting learning progress."""

    def __init__(self, tutor_path: Path = None):
        self.tutor_path = tutor_path or Path.cwd() / ".tutor"

    def export(
        self,
        format: ExportFormat = ExportFormat.JSON,
        output_path: Path = None,
    ) -> ExportResult:
        """Export learning progress."""
        data = self._gather_data()

        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tutor_export_{timestamp}.{format.value}"
            output_path = self.tutor_path.parent / filename

        if format == ExportFormat.JSON:
            return self._export_json(data, output_path)
        else:
            return self._export_markdown(data, output_path)

    def _gather_data(self) -> dict:
        """Gather all data for export."""
        return {
            "version": "2.0",
            "exported_at": datetime.now().isoformat(),
            "config": self._load_json("config.json"),
            "progress": self._load_json("progress.json"),
            "curriculum": self._load_json("curriculum.json"),
            "srs": self._load_json("srs.json"),
            "misconceptions": self._load_json("misconceptions.json"),
        }

    def _export_json(self, data: dict, output_path: Path) -> ExportResult:
        """Export as JSON."""
        content = json.dumps(data, indent=2, ensure_ascii=False)
        output_path.write_text(content, encoding='utf-8')

        return ExportResult(
            format=ExportFormat.JSON,
            filepath=output_path,
            size_bytes=output_path.stat().st_size,
            created_at=datetime.now(),
            includes=list(data.keys()),
        )

    def _export_markdown(self, data: dict, output_path: Path) -> ExportResult:
        """Export as Markdown report."""
        config = data.get("config", {})
        progress = data.get("progress", {})
        stats = progress.get("statistics", {})

        md_lines = [
            f"# Learning Progress Report",
            f"",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"**Subject:** {config.get('subject', 'Unknown')}",
            f"**Level:** {config.get('level', 'Unknown')}",
            f"",
            f"## Statistics",
            f"",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total Exercises | {stats.get('total_exercises_completed', 0)} |",
            f"| Average Score | {stats.get('average_score', 0):.1f}% |",
            f"| Current Streak | {stats.get('streak_days', 0)} days |",
            f"| Total Study Time | {stats.get('total_time_minutes', 0) / 60:.1f} hours |",
            f"",
            f"## Modules Progress",
            f"",
        ]

        modules = progress.get("modules", {})
        for module_id, module_data in modules.items():
            status = module_data.get("status", "not_started")
            exercises = module_data.get("exercises", {})
            completed = sum(1 for e in exercises.values() if e.get("status") == "completed")
            total = len(exercises)

            emoji = "✅" if status == "completed" else "🔄" if status == "in_progress" else "⬜"
            md_lines.append(f"- {emoji} **{module_id}**: {completed}/{total} exercises")

        content = "\n".join(md_lines)
        output_path.write_text(content, encoding='utf-8')

        return ExportResult(
            format=ExportFormat.MARKDOWN,
            filepath=output_path,
            size_bytes=output_path.stat().st_size,
            created_at=datetime.now(),
            includes=["config", "progress"],
        )

    def _load_json(self, filename: str) -> dict:
        """Load a JSON file from tutor path."""
        filepath = self.tutor_path / filename
        if not filepath.exists():
            return {}
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}


class ProgressImporter:
    """Handles importing learning progress."""

    def __init__(self, tutor_path: Path = None):
        self.tutor_path = tutor_path or Path.cwd() / ".tutor"

    def import_progress(self, filepath: Path) -> ImportResult:
        """Import learning progress from a file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            return ImportResult(
                success=False,
                items_imported={},
                warnings=[],
                errors=[f"Failed to load import file: {str(e)}"],
            )

        # Validate
        if "progress" not in data:
            return ImportResult(
                success=False,
                items_imported={},
                warnings=[],
                errors=["Missing required section: progress"],
            )

        # Import each section
        items_imported = {}
        warnings = []

        for section in ["config", "progress", "curriculum", "srs", "misconceptions"]:
            if section in data and data[section]:
                self._save_json(f"{section}.json", data[section])
                items_imported[section] = 1

        return ImportResult(
            success=True,
            items_imported=items_imported,
            warnings=warnings,
            errors=[],
        )

    def _save_json(self, filename: str, data: dict) -> None:
        """Save data to a JSON file."""
        filepath = self.tutor_path / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
