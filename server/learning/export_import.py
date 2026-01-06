"""
Export/Import System

Allows students to:
- Export their complete learning progress
- Import progress from another device/backup
- Generate shareable progress reports
- Create backups before major changes
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional
import json
import hashlib
import base64
import gzip
from enum import Enum


class ExportFormat(Enum):
    """Available export formats."""
    JSON = "json"  # Full JSON export
    JSON_COMPRESSED = "json.gz"  # Compressed JSON
    MARKDOWN = "md"  # Human-readable report
    PORTABLE = "tutor"  # Portable format with checksum


@dataclass
class ExportResult:
    """Result of an export operation."""
    format: ExportFormat
    filepath: Path
    size_bytes: int
    checksum: str
    created_at: datetime
    includes: list[str]  # What's included

    def to_dict(self) -> dict:
        return {
            "format": self.format.value,
            "filepath": str(self.filepath),
            "size_bytes": self.size_bytes,
            "checksum": self.checksum,
            "created_at": self.created_at.isoformat(),
            "includes": self.includes,
        }


@dataclass
class ImportResult:
    """Result of an import operation."""
    success: bool
    items_imported: dict[str, int]  # Category -> count
    conflicts: list[dict]  # Conflicting items
    warnings: list[str]
    errors: list[str]

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "items_imported": self.items_imported,
            "conflicts": self.conflicts,
            "warnings": self.warnings,
            "errors": self.errors,
        }


class ProgressExporter:
    """
    Handles exporting learning progress.

    Supports multiple formats for different use cases:
    - JSON: Full backup, machine-readable
    - Compressed: Space-efficient backup
    - Markdown: Human-readable progress report
    - Portable: Transfer between devices
    """

    def __init__(self, tutor_path: Optional[Path] = None):
        """
        Initialize the exporter.

        Args:
            tutor_path: Path to .tutor directory
        """
        self.tutor_path = tutor_path or Path.cwd() / ".tutor"

    def export(
        self,
        format: ExportFormat = ExportFormat.JSON,
        output_path: Optional[Path] = None,
        include_sessions: bool = True,
        include_evaluations: bool = True,
    ) -> ExportResult:
        """
        Export learning progress.

        Args:
            format: Export format
            output_path: Where to save (auto-generated if None)
            include_sessions: Include session history
            include_evaluations: Include evaluation history

        Returns:
            ExportResult with details
        """
        # Gather data
        data = self._gather_data(include_sessions, include_evaluations)

        # Generate output path
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tutor_export_{timestamp}.{format.value}"
            output_path = self.tutor_path.parent / filename

        # Export based on format
        if format == ExportFormat.JSON:
            return self._export_json(data, output_path)
        elif format == ExportFormat.JSON_COMPRESSED:
            return self._export_compressed(data, output_path)
        elif format == ExportFormat.MARKDOWN:
            return self._export_markdown(data, output_path)
        elif format == ExportFormat.PORTABLE:
            return self._export_portable(data, output_path)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _gather_data(self, include_sessions: bool, include_evaluations: bool) -> dict:
        """Gather all data for export."""
        data = {
            "version": "2.0",
            "exported_at": datetime.now().isoformat(),
            "config": self._load_json("config.json"),
            "progress": self._load_json("progress.json"),
            "curriculum": self._load_json("curriculum.json"),
            "srs": self._load_json("srs.json"),
            "learning_profile": self._load_json("learning_profile.json"),
            "misconceptions": self._load_json("misconceptions.json"),
            "gamification": self._load_json("gamification.json"),
        }

        if include_sessions:
            data["sessions"] = self._gather_sessions()

        if include_evaluations:
            data["evaluations"] = self._load_json("evaluations.json")

        return data

    def _gather_sessions(self) -> list[dict]:
        """Gather all session files."""
        sessions = []
        sessions_dir = self.tutor_path / "sessions"

        if sessions_dir.exists():
            for session_file in sessions_dir.glob("*.json"):
                session = self._load_json(f"sessions/{session_file.name}")
                if session:
                    sessions.append(session)

        return sessions

    def _export_json(self, data: dict, output_path: Path) -> ExportResult:
        """Export as plain JSON."""
        content = json.dumps(data, indent=2, ensure_ascii=False)
        output_path.write_text(content, encoding='utf-8')

        return ExportResult(
            format=ExportFormat.JSON,
            filepath=output_path,
            size_bytes=output_path.stat().st_size,
            checksum=self._calculate_checksum(content),
            created_at=datetime.now(),
            includes=list(data.keys()),
        )

    def _export_compressed(self, data: dict, output_path: Path) -> ExportResult:
        """Export as compressed JSON."""
        content = json.dumps(data, ensure_ascii=False)
        compressed = gzip.compress(content.encode('utf-8'))
        output_path.write_bytes(compressed)

        return ExportResult(
            format=ExportFormat.JSON_COMPRESSED,
            filepath=output_path,
            size_bytes=output_path.stat().st_size,
            checksum=self._calculate_checksum(content),
            created_at=datetime.now(),
            includes=list(data.keys()),
        )

    def _export_markdown(self, data: dict, output_path: Path) -> ExportResult:
        """Export as human-readable Markdown report."""
        config = data.get("config", {})
        progress = data.get("progress", {})
        stats = progress.get("statistics", {})
        gamification = data.get("gamification", {})

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

            status_emoji = "✅" if status == "completed" else "🔄" if status == "in_progress" else "⬜"
            md_lines.append(f"- {status_emoji} **{module_id}**: {completed}/{total} exercises")

        # Gamification
        if gamification:
            md_lines.extend([
                f"",
                f"## Achievements",
                f"",
                f"**Level:** {gamification.get('level', 1)}",
                f"**XP:** {gamification.get('xp', 0)}",
                f"",
                f"### Badges Earned",
                f"",
            ])

            badges = gamification.get("earned_badges", [])
            for badge in badges:
                md_lines.append(f"- {badge.get('icon', '🏅')} **{badge.get('name')}** - {badge.get('description')}")

        # Personal bests
        personal_bests = gamification.get("personal_bests", {})
        if personal_bests:
            md_lines.extend([
                f"",
                f"### Personal Bests",
                f"",
            ])
            for category, pb in personal_bests.items():
                md_lines.append(f"- **{category}**: {pb.get('value')} ({pb.get('context')})")

        content = "\n".join(md_lines)
        output_path.write_text(content, encoding='utf-8')

        return ExportResult(
            format=ExportFormat.MARKDOWN,
            filepath=output_path,
            size_bytes=output_path.stat().st_size,
            checksum=self._calculate_checksum(content),
            created_at=datetime.now(),
            includes=["config", "progress", "gamification"],
        )

    def _export_portable(self, data: dict, output_path: Path) -> ExportResult:
        """Export in portable format with integrity check."""
        # Create wrapper with checksum
        content = json.dumps(data, ensure_ascii=False)
        checksum = self._calculate_checksum(content)

        portable_data = {
            "format": "tutor_portable_v2",
            "checksum": checksum,
            "created_at": datetime.now().isoformat(),
            "data": base64.b64encode(gzip.compress(content.encode('utf-8'))).decode('ascii'),
        }

        output_content = json.dumps(portable_data, indent=2)
        output_path.write_text(output_content, encoding='utf-8')

        return ExportResult(
            format=ExportFormat.PORTABLE,
            filepath=output_path,
            size_bytes=output_path.stat().st_size,
            checksum=checksum,
            created_at=datetime.now(),
            includes=list(data.keys()),
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

    def _calculate_checksum(self, content: str) -> str:
        """Calculate SHA256 checksum of content."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()


class ProgressImporter:
    """
    Handles importing learning progress.

    Supports:
    - Full restore from backup
    - Merge with existing progress
    - Conflict resolution
    """

    def __init__(self, tutor_path: Optional[Path] = None):
        """
        Initialize the importer.

        Args:
            tutor_path: Path to .tutor directory
        """
        self.tutor_path = tutor_path or Path.cwd() / ".tutor"

    def import_progress(
        self,
        filepath: Path,
        merge_strategy: str = "newer_wins",
        create_backup: bool = True,
    ) -> ImportResult:
        """
        Import learning progress from a file.

        Args:
            filepath: Path to import file
            merge_strategy: How to handle conflicts
                - "newer_wins": Keep newer data
                - "import_wins": Overwrite with import
                - "existing_wins": Keep existing data
                - "merge": Combine where possible
            create_backup: Create backup before import

        Returns:
            ImportResult with details
        """
        # Create backup if requested
        if create_backup and self.tutor_path.exists():
            self._create_backup()

        # Load import data
        try:
            data = self._load_import_file(filepath)
        except Exception as e:
            return ImportResult(
                success=False,
                items_imported={},
                conflicts=[],
                warnings=[],
                errors=[f"Failed to load import file: {str(e)}"],
            )

        # Validate data
        validation_errors = self._validate_data(data)
        if validation_errors:
            return ImportResult(
                success=False,
                items_imported={},
                conflicts=[],
                warnings=[],
                errors=validation_errors,
            )

        # Perform import
        items_imported = {}
        conflicts = []
        warnings = []

        # Import each section
        for section in ["config", "progress", "curriculum", "srs", "learning_profile",
                        "misconceptions", "gamification", "evaluations"]:
            if section in data and data[section]:
                result = self._import_section(section, data[section], merge_strategy)
                items_imported[section] = result["count"]
                conflicts.extend(result.get("conflicts", []))
                warnings.extend(result.get("warnings", []))

        # Import sessions
        if "sessions" in data and data["sessions"]:
            result = self._import_sessions(data["sessions"], merge_strategy)
            items_imported["sessions"] = result["count"]
            warnings.extend(result.get("warnings", []))

        return ImportResult(
            success=True,
            items_imported=items_imported,
            conflicts=conflicts,
            warnings=warnings,
            errors=[],
        )

    def validate_import_file(self, filepath: Path) -> dict:
        """
        Validate an import file without actually importing.

        Args:
            filepath: Path to import file

        Returns:
            Validation result with details
        """
        try:
            data = self._load_import_file(filepath)
        except Exception as e:
            return {
                "valid": False,
                "errors": [str(e)],
                "preview": None,
            }

        errors = self._validate_data(data)

        if errors:
            return {
                "valid": False,
                "errors": errors,
                "preview": None,
            }

        # Generate preview
        preview = {
            "version": data.get("version", "unknown"),
            "exported_at": data.get("exported_at", "unknown"),
            "sections": list(data.keys()),
            "progress_summary": self._summarize_progress(data.get("progress", {})),
        }

        return {
            "valid": True,
            "errors": [],
            "preview": preview,
        }

    def _load_import_file(self, filepath: Path) -> dict:
        """Load and decode import file."""
        content = filepath.read_text(encoding='utf-8')

        # Check if it's portable format
        try:
            wrapper = json.loads(content)
            if wrapper.get("format") == "tutor_portable_v2":
                # Verify checksum
                compressed_data = base64.b64decode(wrapper["data"])
                decompressed = gzip.decompress(compressed_data).decode('utf-8')

                checksum = hashlib.sha256(decompressed.encode('utf-8')).hexdigest()
                if checksum != wrapper["checksum"]:
                    raise ValueError("Checksum mismatch - file may be corrupted")

                return json.loads(decompressed)
        except (KeyError, TypeError):
            pass

        # Check if compressed
        if filepath.suffix == ".gz":
            with gzip.open(filepath, 'rt', encoding='utf-8') as f:
                return json.load(f)

        # Plain JSON
        return json.loads(content)

    def _validate_data(self, data: dict) -> list[str]:
        """Validate import data structure."""
        errors = []

        # Check version
        version = data.get("version", "")
        if version and not version.startswith("2."):
            errors.append(f"Incompatible version: {version}. Expected 2.x")

        # Check required sections
        if "progress" not in data:
            errors.append("Missing required section: progress")

        # Validate progress structure
        progress = data.get("progress", {})
        if progress and "modules" in progress:
            if not isinstance(progress["modules"], dict):
                errors.append("Invalid progress.modules format")

        return errors

    def _import_section(self, section: str, data: dict, merge_strategy: str) -> dict:
        """Import a single section."""
        filepath = self.tutor_path / f"{section}.json"
        existing = self._load_json(filepath) if filepath.exists() else {}

        result = {
            "count": 0,
            "conflicts": [],
            "warnings": [],
        }

        if merge_strategy == "import_wins" or not existing:
            # Direct overwrite
            self._save_json(filepath, data)
            result["count"] = 1
        elif merge_strategy == "existing_wins":
            # Keep existing
            result["warnings"].append(f"Skipped {section} (existing data preserved)")
        elif merge_strategy == "newer_wins":
            # Compare timestamps
            existing_time = existing.get("updated_at", "")
            import_time = data.get("updated_at", "")

            if import_time > existing_time:
                self._save_json(filepath, data)
                result["count"] = 1
            else:
                result["warnings"].append(f"Skipped {section} (existing is newer)")
        elif merge_strategy == "merge":
            # Deep merge
            merged = self._deep_merge(existing, data)
            self._save_json(filepath, merged)
            result["count"] = 1

        return result

    def _import_sessions(self, sessions: list, merge_strategy: str) -> dict:
        """Import session files."""
        sessions_dir = self.tutor_path / "sessions"
        sessions_dir.mkdir(parents=True, exist_ok=True)

        result = {
            "count": 0,
            "warnings": [],
        }

        for session in sessions:
            date = session.get("date", "")
            if not date:
                continue

            filepath = sessions_dir / f"{date}.json"

            if filepath.exists() and merge_strategy != "import_wins":
                result["warnings"].append(f"Skipped session {date} (already exists)")
                continue

            self._save_json(filepath, session)
            result["count"] += 1

        return result

    def _create_backup(self) -> Path:
        """Create a backup of current data."""
        exporter = ProgressExporter(self.tutor_path)
        result = exporter.export(
            format=ExportFormat.JSON_COMPRESSED,
            output_path=self.tutor_path.parent / f"tutor_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json.gz"
        )
        return result.filepath

    def _summarize_progress(self, progress: dict) -> dict:
        """Create a summary of progress data."""
        stats = progress.get("statistics", {})
        modules = progress.get("modules", {})

        return {
            "total_exercises": stats.get("total_exercises_completed", 0),
            "average_score": stats.get("average_score", 0),
            "streak_days": stats.get("streak_days", 0),
            "modules_count": len(modules),
            "completed_modules": sum(1 for m in modules.values() if m.get("status") == "completed"),
        }

    def _deep_merge(self, base: dict, update: dict) -> dict:
        """Deep merge two dictionaries."""
        result = base.copy()

        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value

        return result

    def _load_json(self, filepath: Path) -> dict:
        """Load a JSON file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def _save_json(self, filepath: Path, data: dict) -> None:
        """Save data to a JSON file."""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
