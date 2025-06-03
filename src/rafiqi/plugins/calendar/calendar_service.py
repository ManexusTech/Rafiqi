"""Google Calendar Service implementation"""
from datetime import datetime
from typing import Optional, List, Dict
import json
from icalendar import Calendar, Event, vText
from pathlib import Path
import pytz
from uuid import uuid4

class CalendarService:
    def __init__(self):
        self.calendar = Calendar()
        self.calendar.add('prodid', '-//Rafiqi Calendar//EN')
        self.calendar.add('version', '2.0')
        self.calendar_file = Path.home() / '.rafiqi' / 'calendar.ics'
        self._load_calendar()

    def _load_calendar(self):
        """Load existing calendar if it exists"""
        try:
            if self.calendar_file.exists():
                with open(self.calendar_file, 'rb') as f:
                    self.calendar = Calendar.from_ical(f.read())
        except Exception as e:
            print(f"Error loading calendar: {e}")
            # Create new calendar if loading fails
            self.calendar = Calendar()
            self.calendar.add('prodid', '-//Rafiqi Calendar//EN')
            self.calendar.add('version', '2.0')

    def _save_calendar(self):
        """Save calendar to file"""
        try:
            self.calendar_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.calendar_file, 'wb') as f:
                f.write(self.calendar.to_ical())
        except Exception as e:
            print(f"Error saving calendar: {e}")

    async def create_event(self, title: str, start_time: datetime,
                         end_time: datetime, description: Optional[str] = None) -> str:
        """Create a new calendar event"""
        try:
            event = Event()
            event.add('summary', title)
            event.add('dtstart', start_time)
            event.add('dtend', end_time)
            event.add('description', description or "")
            event.add('uid', str(uuid4()))
            
            # Add event to calendar
            self.calendar.add_component(event)
            self._save_calendar()
            
            # Generate iCal file for this specific event
            single_event_cal = Calendar()
            single_event_cal.add('prodid', '-//Rafiqi Calendar//EN')
            single_event_cal.add('version', '2.0')
            single_event_cal.add_component(event)
            
            # Save single event to a separate file
            event_file = Path.home() / '.rafiqi' / 'events' / f"{title.replace(' ', '_')}.ics"
            event_file.parent.mkdir(parents=True, exist_ok=True)
            with open(event_file, 'wb') as f:
                f.write(single_event_cal.to_ical())
            
            return f"Successfully created event: {title}\nEvent file saved at: {event_file}"
        except Exception as e:
            return f"Failed to create event: {str(e)}"

    async def list_events(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """List events between start and end date"""
        try:
            events = []
            for component in self.calendar.walk():
                if component.name == "VEVENT":
                    event_start = component.get('dtstart').dt
                    if isinstance(event_start, datetime):
                        event_start = event_start.replace(tzinfo=None)
                    
                    if start_date <= event_start <= end_date:
                        events.append({
                            'id': str(component.get('uid')),
                            'title': str(component.get('summary')),
                            'start_time': str(component.get('dtstart').dt),
                            'end_time': str(component.get('dtend').dt),
                            'description': str(component.get('description', ''))
                        })
            return events
        except Exception as e:
            print(f"Error fetching events: {str(e)}")
            return []

    async def export_calendar(self, output_path: Optional[str] = None) -> str:
        """Export entire calendar as ICS file"""
        try:
            if output_path:
                output_file = Path(output_path)
            else:
                output_file = Path.home() / 'Downloads' / 'rafiqi_calendar.ics'
            
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'wb') as f:
                f.write(self.calendar.to_ical())
            
            return f"Calendar exported to: {output_file}"
        except Exception as e:
            return f"Failed to export calendar: {str(e)}"

    async def import_calendar(self, ical_file: str) -> str:
        """Import events from an ICS file"""
        try:
            with open(ical_file, 'rb') as f:
                imported_cal = Calendar.from_ical(f.read())
            
            events_added = 0
            for component in imported_cal.walk():
                if component.name == "VEVENT":
                    self.calendar.add_component(component)
                    events_added += 1
            
            self._save_calendar()
            return f"Successfully imported {events_added} events"
        except Exception as e:
            return f"Failed to import calendar: {str(e)}" 