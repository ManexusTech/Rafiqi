import asyncio
from pathlib import Path
from src.rafiqi.plugins.calendar import CalendarPlugin
from datetime import datetime, timedelta

async def test_calendar_operations():
    # Initialize the calendar plugin
    calendar = CalendarPlugin()
    
    # Test directory paths
    test_dir = Path(__file__).parent / 'calendar_data'
    sample_calendar = test_dir / 'sample_calendars' / 'test_calendar.ics'
    export_path = test_dir / 'exports' / 'exported_calendar.ics'
    
    print("\n=== Testing Calendar Operations ===")
    
    # 1. Import test calendar
    print("\nImporting test calendar...")
    result = await calendar.handle_command('import_calendar', {'ical_file': str(sample_calendar)})
    print(result)
    
    # 2. List events
    print("\nListing events for next 7 days...")
    start_date = datetime.now()
    end_date = start_date + timedelta(days=7)
    result = await calendar.handle_command('list_events', {
        'start_date': start_date,
        'end_date': end_date
    })
    print(result)
    
    # 3. Add new event
    print("\nAdding new event...")
    result = await calendar.handle_command('add_event', {
        'title': 'New Test Event',
        'start_time': datetime.now() + timedelta(days=1),
        'end_time': datetime.now() + timedelta(days=1, hours=1),
        'description': 'This is a new test event'
    })
    print(result)
    
    # 4. Export calendar
    print("\nExporting calendar...")
    result = await calendar.handle_command('export_calendar', {
        'output_path': str(export_path)
    })
    print(result)

if __name__ == "__main__":
    asyncio.run(test_calendar_operations()) 