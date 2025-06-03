import os
from openai import OpenAI
from dotenv import load_dotenv
import asyncio

load_dotenv()

class TextHandler:
    def __init__(self):
        # Initialize OpenAI client
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Configure conversation history
        self.conversation_history = [
            {"role": "system", "content": "You are Rafiqi, a helpful AI assistant. Keep your responses concise and natural."}
        ]

    async def process_with_ai(self, text):
        """Process text with OpenAI API"""
        try:
            # Add user message to conversation history
            self.conversation_history.append({"role": "user", "content": text})
            
            # Get AI response
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model="gpt-3.5-turbo",
                messages=self.conversation_history
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