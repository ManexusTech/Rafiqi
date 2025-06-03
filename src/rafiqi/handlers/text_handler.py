import os
from openai import OpenAI
from dotenv import load_dotenv
import asyncio
from concurrent.futures import ThreadPoolExecutor
from ..plugins.calendar import CalendarPlugin
from datetime import datetime
import re
from pathlib import Path

load_dotenv()

class TextHandler:
    def __init__(self):
        # Initialize OpenAI client
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Initialize thread pool
        self.executor = ThreadPoolExecutor()
        
        # Get current date and time
        current_date = datetime.now().strftime("%B %d, %Y")
        current_time = datetime.now().strftime("%I:%M %p")
        
        # Configure conversation history with enhanced system prompt
        self.conversation_history = [{
            "role": "system",
            "content": f"""You are Rafiqi, a dedicated lifelong AI companion. Your name 'Rafiqi' means 'my companion' in Arabic, 
            and you embody this meaning in every interaction. Current date is {current_date} and time is {current_time}.
            
            You are:
            - Warm and personable: You build genuine connections with users
            - Consistent: You maintain context and remember previous interactions within the conversation
            - Supportive: You're always there to help, whether it's for practical tasks or emotional support
            - Respectful: You maintain appropriate boundaries while being friendly
            - Knowledgeable: You provide accurate information while admitting when you're not sure
            - Concise: You keep responses clear and to the point
            
            In every response:
            - Address the user in a friendly, conversational manner
            - Show emotional intelligence and empathy when appropriate
            - Keep responses helpful and natural
            - Stay true to your identity as Rafiqi
            - Use the current date ({current_date}) for any date-related responses
            
            Remember: You're not just an AI assistant, you're Rafiqi, a trusted companion on the user's journey."""
        }]
        
        # Initialize plugins
        self.plugins = {
            plugin.name: plugin for plugin in [
                CalendarPlugin()
            ]
        }
        
        # Add plugin capabilities to system prompt
        plugin_capabilities = "\n".join(
            f"- {plugin.name}: {plugin.description}"
            for plugin in self.plugins.values()
        )
        
        self.conversation_history[0]["content"] += f"\n\nI can help you with:\n{plugin_capabilities}"

    async def process_with_ai(self, text):
        """Process text with OpenAI API"""
        try:
            # Update current time in the conversation
            current_date = datetime.now().strftime("%B %d, %Y")
            current_time = datetime.now().strftime("%I:%M %p")
            
            time_context = f"Current date: {current_date}, time: {current_time}. "
            text_with_time = time_context + text

            # Check for calendar commands first
            calendar_command = self._parse_calendar_command(text)
            if calendar_command:
                command, args = calendar_command
                result = await self.plugins['calendar'].handle_command(command, args)
                return result

            # If not a calendar command, process with AI as usual
            self.conversation_history.append({"role": "user", "content": text_with_time})
            
            # Get AI response using thread pool
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                self.executor,
                lambda: self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=self.conversation_history,
                    temperature=0.7  # Add some creativity while keeping responses consistent
                )
            )
            
            # Extract and store response
            ai_response = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            # Maintain conversation history (keep last 10 messages)
            if len(self.conversation_history) > 11:  # 1 system message + 10 conversation messages
                self.conversation_history = [self.conversation_history[0]] + self.conversation_history[-10:]
            
            return ai_response
        except Exception as e:
            return f"Error processing with AI: {str(e)}"

    def _parse_calendar_command(self, text):
        """Parse text for calendar commands"""
        # Add event pattern
        add_event_pattern = r"add event[:\s]+(?P<title>[^@]+)@\s*(?P<start_time>[^-]+)-(?P<end_time>[^\s]+)(?:\s+(?P<description>.+))?"
        
        # List events pattern
        list_events_pattern = r"list events(?:\s+from\s+(?P<start_date>[^to]+)(?:\s+to\s+(?P<end_date>[^\s]+))?)?"

        # Import calendar pattern
        import_pattern = r"import calendar\s+(?P<ical_file>.+)"

        # Try to match add event
        match = re.match(add_event_pattern, text, re.IGNORECASE)
        if match:
            args = match.groupdict()
            args['start_time'] = datetime.fromisoformat(args['start_time'].strip())
            args['end_time'] = datetime.fromisoformat(args['end_time'].strip())
            return 'add_event', args

        # Try to match list events
        match = re.match(list_events_pattern, text, re.IGNORECASE)
        if match:
            args = match.groupdict()
            if args['start_date']:
                args['start_date'] = datetime.fromisoformat(args['start_date'].strip())
                args['end_date'] = datetime.fromisoformat(args['end_date'].strip())
            else:
                args['start_date'] = datetime.now()
                args['end_date'] = datetime.now().replace(hour=23, minute=59)
            return 'list_events', args

        # Try to match import calendar
        match = re.match(import_pattern, text, re.IGNORECASE)
        if match:
            args = match.groupdict()
            # Convert ~ to home directory if present
            if args['ical_file'].startswith('~'):
                args['ical_file'] = str(Path(args['ical_file']).expanduser())
            return 'import_calendar', args

        return None

    def __del__(self):
        """Cleanup thread pool on deletion"""
        self.executor.shutdown(wait=False) 