"""Calendar integration for Rafiqi"""
from datetime import datetime
from typing import Optional, Dict, Any, List
from ...plugins import RafiqiPlugin
from .calendar_service import CalendarService

class CalendarPlugin(RafiqiPlugin):
    def __init__(self):
        self.calendar_service = CalendarService()
    
    @property
    def name(self) -> str:
        return "calendar"
    
    @property
    def description(self) -> str:
        return "Manages your calendar events and schedules (iCal format)"
    
    @property
    def commands(self) -> List[str]:
        return [
            "add_event",
            "list_events",
            "export_calendar",
            "import_calendar"
        ]
    
    async def handle_command(self, command: str, args: Dict[str, Any]) -> str:
        if command == "add_event":
            return await self.calendar_service.create_event(
                title=args.get("title"),
                start_time=args.get("start_time"),
                end_time=args.get("end_time"),
                description=args.get("description")
            )
        elif command == "list_events":
            events = await self.calendar_service.list_events(
                start_date=args.get("start_date"),
                end_date=args.get("end_date")
            )
            if not events:
                return "No events found for this period."
            
            return "\n".join(
                f"- {event['title']} at {event['start_time']}"
                for event in events
            )
        elif command == "export_calendar":
            return await self.calendar_service.export_calendar(
                output_path=args.get("output_path")
            )
        elif command == "import_calendar":
            return await self.calendar_service.import_calendar(
                ical_file=args.get("ical_file")
            )
        # Add other command handlers
        
    async def add_event(self, title: str, start_time: datetime, 
                       end_time: datetime, description: Optional[str] = None) -> str:
        """Add a new event to calendar"""
        try:
            event_id = await self.calendar_service.create_event(
                title, start_time, end_time, description
            )
            return f"Successfully added event: {title}"
        except Exception as e:
            return f"Failed to add event: {str(e)}"
    
    async def list_events(self, start_date: datetime, end_date: datetime) -> str:
        """List events between dates"""
        try:
            events = await self.calendar_service.get_events(start_date, end_date)
            if not events:
                return "No events found for this period."
            
            return "\n".join(
                f"- {event['title']} at {event['start_time']}"
                for event in events
            )
        except Exception as e:
            return f"Failed to list events: {str(e)}" 