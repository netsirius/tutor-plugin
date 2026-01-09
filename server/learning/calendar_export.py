"""
Calendar Export Module

Exports study plans to various calendar formats:
- Google Calendar (via .ics or API)
- Apple Calendar (.ics)
- Outlook (.ics)
- Generic iCalendar format
"""

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from enum import Enum
from pathlib import Path
from typing import Optional
import json
import hashlib
from urllib.parse import urlencode


class CalendarProvider(Enum):
    """Supported calendar providers."""
    GOOGLE = "google"
    APPLE = "apple"
    OUTLOOK = "outlook"
    GENERIC = "generic"


class EventType(Enum):
    """Types of calendar events."""
    STUDY_SESSION = "study_session"
    EXAM = "exam"
    DEADLINE = "deadline"
    REMINDER = "reminder"
    SIMULATION = "simulation"


@dataclass
class CalendarEvent:
    """A calendar event."""
    id: str
    title: str
    start: datetime
    end: datetime
    event_type: EventType
    description: str = ""
    location: Optional[str] = None
    topic_id: Optional[str] = None
    reminders: list[int] = field(default_factory=lambda: [30, 5])  # minutes before
    color: Optional[str] = None
    is_all_day: bool = False
    url: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "event_type": self.event_type.value,
            "description": self.description,
            "location": self.location,
            "topic_id": self.topic_id,
            "reminders": self.reminders,
            "color": self.color,
            "is_all_day": self.is_all_day,
            "url": self.url,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CalendarEvent":
        data = data.copy()
        data["start"] = datetime.fromisoformat(data["start"])
        data["end"] = datetime.fromisoformat(data["end"])
        data["event_type"] = EventType(data["event_type"])
        return cls(**data)

    def to_ics(self) -> str:
        """Convert to iCalendar format."""
        lines = [
            "BEGIN:VEVENT",
            f"UID:{self.id}@tutor",
            f"DTSTAMP:{datetime.now().strftime('%Y%m%dT%H%M%SZ')}",
        ]

        if self.is_all_day:
            lines.append(f"DTSTART;VALUE=DATE:{self.start.strftime('%Y%m%d')}")
            lines.append(f"DTEND;VALUE=DATE:{self.end.strftime('%Y%m%d')}")
        else:
            lines.append(f"DTSTART:{self.start.strftime('%Y%m%dT%H%M%S')}")
            lines.append(f"DTEND:{self.end.strftime('%Y%m%dT%H%M%S')}")

        lines.append(f"SUMMARY:{self._escape_ics(self.title)}")

        if self.description:
            lines.append(f"DESCRIPTION:{self._escape_ics(self.description)}")

        if self.location:
            lines.append(f"LOCATION:{self._escape_ics(self.location)}")

        if self.url:
            lines.append(f"URL:{self.url}")

        # Add reminders
        for minutes in self.reminders:
            lines.append("BEGIN:VALARM")
            lines.append("ACTION:DISPLAY")
            lines.append(f"TRIGGER:-PT{minutes}M")
            lines.append(f"DESCRIPTION:Reminder: {self.title}")
            lines.append("END:VALARM")

        lines.append("END:VEVENT")

        return "\r\n".join(lines)

    def _escape_ics(self, text: str) -> str:
        """Escape text for iCalendar format."""
        return text.replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;").replace("\n", "\\n")

    def to_google_calendar_url(self) -> str:
        """Generate a Google Calendar add event URL."""
        params = {
            "action": "TEMPLATE",
            "text": self.title,
            "dates": f"{self.start.strftime('%Y%m%dT%H%M%S')}/{self.end.strftime('%Y%m%dT%H%M%S')}",
            "details": self.description,
        }

        if self.location:
            params["location"] = self.location

        return f"https://calendar.google.com/calendar/render?{urlencode(params)}"


@dataclass
class CalendarExport:
    """Result of a calendar export."""
    provider: CalendarProvider
    events_count: int
    file_path: Optional[Path] = None
    ics_content: Optional[str] = None
    google_urls: list[str] = field(default_factory=list)
    success: bool = True
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "provider": self.provider.value,
            "events_count": self.events_count,
            "file_path": str(self.file_path) if self.file_path else None,
            "google_urls": self.google_urls,
            "success": self.success,
            "error": self.error,
        }


class CalendarExporter:
    """
    Exports study plans to calendar formats.

    Supports:
    - iCalendar (.ics) file generation
    - Google Calendar URL generation
    - Direct Google Calendar API (if credentials available)
    """

    def __init__(self, tutor_path: Path, subject_name: str = "Study"):
        self.tutor_path = tutor_path
        self.subject_name = subject_name
        self.exports_dir = tutor_path / "calendar_exports"
        self.events_file = tutor_path / "calendar_events.json"

        self._events: list[CalendarEvent] = []
        self._load()

    def _load(self) -> None:
        """Load saved events."""
        if self.events_file.exists():
            with open(self.events_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._events = [CalendarEvent.from_dict(e) for e in data]

    def _save(self) -> None:
        """Save events."""
        self.tutor_path.mkdir(parents=True, exist_ok=True)
        with open(self.events_file, 'w', encoding='utf-8') as f:
            json.dump([e.to_dict() for e in self._events], f, indent=2, ensure_ascii=False)

    def create_event_from_session(
        self,
        session: dict,
        default_time: str = "18:00",
    ) -> CalendarEvent:
        """
        Create a calendar event from a study session.

        Args:
            session: Study session data
            default_time: Default start time if not specified

        Returns:
            CalendarEvent
        """
        session_date = date.fromisoformat(session["date"])
        start_time = session.get("start_time", default_time)

        # Parse start time
        hour, minute = map(int, start_time.split(":"))
        start_dt = datetime(session_date.year, session_date.month, session_date.day, hour, minute)
        duration = session.get("duration_minutes", 60)
        end_dt = start_dt + timedelta(minutes=duration)

        # Determine event type and emoji
        session_type = session.get("session_type", "learn_new")
        type_emoji = {
            "learn_new": "📚",
            "reinforce": "💪",
            "extend": "🚀",
            "review_srs": "🔄",
            "exam_prep": "📝",
            "simulate": "⏱️",
        }
        emoji = type_emoji.get(session_type, "📖")

        title = f"{emoji} {session.get('topic_name', 'Study Session')}"

        # Build description
        description_parts = [
            f"Topic: {session.get('topic_name', 'General')}",
            f"Type: {session_type.replace('_', ' ').title()}",
            f"Duration: {duration} minutes",
            "",
            "---",
            f"Subject: {self.subject_name}",
        ]

        if session.get("description"):
            description_parts.insert(0, session["description"])

        description_parts.append("")
        description_parts.append("Start your session: /tutor continue")

        # Generate unique ID
        event_id = hashlib.md5(
            f"{session_date}_{start_time}_{session.get('topic_id', '')}".encode()
        ).hexdigest()[:12]

        return CalendarEvent(
            id=f"tutor_{event_id}",
            title=title,
            start=start_dt,
            end=end_dt,
            event_type=EventType.STUDY_SESSION,
            description="\n".join(description_parts),
            topic_id=session.get("topic_id"),
            reminders=[30, 5],
            color="#4285F4",  # Google blue
        )

    def create_exam_event(
        self,
        exam: dict,
    ) -> CalendarEvent:
        """
        Create a calendar event for an exam.

        Args:
            exam: Exam data

        Returns:
            CalendarEvent
        """
        exam_date = date.fromisoformat(exam["date"])
        exam_time = exam.get("time", "09:00")

        hour, minute = map(int, exam_time.split(":"))
        start_dt = datetime(exam_date.year, exam_date.month, exam_date.day, hour, minute)
        duration = exam.get("duration_minutes", 120)
        end_dt = start_dt + timedelta(minutes=duration)

        title = f"⚡ EXAMEN: {exam.get('name', self.subject_name)}"

        description = f"""EXAMEN - {self.subject_name}

Duración: {duration} minutos
Tipo: {exam.get('type', 'Final')}

¡Buena suerte! 🍀

---
Preparado con Tutor"""

        return CalendarEvent(
            id=f"exam_{exam_date.isoformat()}",
            title=title,
            start=start_dt,
            end=end_dt,
            event_type=EventType.EXAM,
            description=description,
            location=exam.get("location"),
            reminders=[1440, 60, 30],  # 1 day, 1 hour, 30 min before
            color="#EA4335",  # Red
        )

    def add_events_from_plan(
        self,
        sessions: list[dict],
        exams: list[dict] = None,
        default_time: str = "18:00",
    ) -> int:
        """
        Add events from a study plan.

        Args:
            sessions: List of study sessions
            exams: List of exams
            default_time: Default start time

        Returns:
            Number of events added
        """
        count = 0

        for session in sessions:
            event = self.create_event_from_session(session, default_time)
            if event.id not in [e.id for e in self._events]:
                self._events.append(event)
                count += 1

        if exams:
            for exam in exams:
                event = self.create_exam_event(exam)
                if event.id not in [e.id for e in self._events]:
                    self._events.append(event)
                    count += 1

        self._save()
        return count

    def export_ics(
        self,
        filename: Optional[str] = None,
        calendar_name: Optional[str] = None,
    ) -> CalendarExport:
        """
        Export events to iCalendar (.ics) format.

        Args:
            filename: Output filename (without extension)
            calendar_name: Name of the calendar

        Returns:
            CalendarExport result
        """
        if not self._events:
            return CalendarExport(
                provider=CalendarProvider.GENERIC,
                events_count=0,
                success=False,
                error="No events to export",
            )

        cal_name = calendar_name or f"Estudio - {self.subject_name}"

        # Build iCalendar content
        lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//Tutor//Study Plan//EN",
            f"X-WR-CALNAME:{cal_name}",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH",
        ]

        for event in self._events:
            lines.append(event.to_ics())

        lines.append("END:VCALENDAR")

        ics_content = "\r\n".join(lines)

        # Save to file
        self.exports_dir.mkdir(parents=True, exist_ok=True)
        fname = filename or f"study_plan_{datetime.now().strftime('%Y%m%d')}"
        file_path = self.exports_dir / f"{fname}.ics"

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(ics_content)

        return CalendarExport(
            provider=CalendarProvider.GENERIC,
            events_count=len(self._events),
            file_path=file_path,
            ics_content=ics_content,
            success=True,
        )

    def export_google_urls(self) -> CalendarExport:
        """
        Generate Google Calendar URLs for all events.

        Returns:
            CalendarExport with Google Calendar URLs
        """
        urls = [event.to_google_calendar_url() for event in self._events]

        return CalendarExport(
            provider=CalendarProvider.GOOGLE,
            events_count=len(self._events),
            google_urls=urls,
            success=True,
        )

    def get_events_for_range(
        self,
        start_date: date,
        end_date: date,
    ) -> list[CalendarEvent]:
        """Get events within a date range."""
        return [
            e for e in self._events
            if start_date <= e.start.date() <= end_date
        ]

    def get_upcoming_events(self, days: int = 7) -> list[CalendarEvent]:
        """Get events for the next N days."""
        today = date.today()
        end = today + timedelta(days=days)
        return self.get_events_for_range(today, end)

    def clear_events(self) -> int:
        """Clear all events. Returns count of events cleared."""
        count = len(self._events)
        self._events = []
        self._save()
        return count

    def sync_with_plan(
        self,
        sessions: list[dict],
        exams: list[dict] = None,
    ) -> dict:
        """
        Sync events with a study plan, updating existing and adding new.

        Args:
            sessions: Current study sessions
            exams: Current exams

        Returns:
            Sync summary
        """
        # Track changes
        added = 0
        updated = 0
        removed = 0

        # Create set of new event IDs
        new_events = {}

        for session in sessions:
            event = self.create_event_from_session(session)
            new_events[event.id] = event

        if exams:
            for exam in exams:
                event = self.create_exam_event(exam)
                new_events[event.id] = event

        # Find events to remove (no longer in plan)
        current_ids = {e.id for e in self._events}
        new_ids = set(new_events.keys())

        to_remove = current_ids - new_ids
        removed = len(to_remove)

        # Update existing events
        for event in self._events:
            if event.id in new_events:
                new_event = new_events[event.id]
                if (event.start != new_event.start or
                    event.end != new_event.end or
                    event.title != new_event.title):
                    updated += 1

        # Add new events
        to_add = new_ids - current_ids
        added = len(to_add)

        # Replace events
        self._events = list(new_events.values())
        self._events.sort(key=lambda e: e.start)
        self._save()

        return {
            "added": added,
            "updated": updated,
            "removed": removed,
            "total": len(self._events),
        }

    def get_calendar_summary(self) -> dict:
        """Get a summary of the calendar."""
        if not self._events:
            return {
                "total_events": 0,
                "study_sessions": 0,
                "exams": 0,
                "next_event": None,
            }

        study_sessions = len([e for e in self._events if e.event_type == EventType.STUDY_SESSION])
        exams = len([e for e in self._events if e.event_type == EventType.EXAM])

        upcoming = [e for e in self._events if e.start > datetime.now()]
        next_event = min(upcoming, key=lambda e: e.start) if upcoming else None

        return {
            "total_events": len(self._events),
            "study_sessions": study_sessions,
            "exams": exams,
            "next_event": next_event.to_dict() if next_event else None,
            "date_range": {
                "start": min(e.start for e in self._events).isoformat(),
                "end": max(e.end for e in self._events).isoformat(),
            } if self._events else None,
        }
