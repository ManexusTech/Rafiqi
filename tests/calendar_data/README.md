# Calendar Test Data

This directory contains test calendars and data for testing Rafiqi's calendar functionality.

## Directory Structure
- `sample_calendars/`: Contains sample calendar files for import testing
- `exports/`: Directory where test exports are saved

## Usage
1. Place your calendar files in `sample_calendars/`
2. Run the test script:
   ```bash
   python -m tests.test_calendar_operations
   ```
3. Check exported calendars in `exports/`

## File Formats
- All calendar files should be in iCalendar (.ics) format
- Sample calendars should include various event types for comprehensive testing 