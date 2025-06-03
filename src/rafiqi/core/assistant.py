from ..handlers.text_handler import TextHandler
import asyncio

class Assistant:
    """Core assistant class that handles text interactions with AI."""
    def __init__(self):
        self.text_handler = TextHandler()
        self.is_running = False

    async def start_interaction(self):
        """Start text-based interaction"""
        self.is_running = True
        print("Rafiqi is ready! Type your message (or 'quit' to exit):")
        
        while self.is_running:
            user_input = input("> ")
            
            if user_input.lower() in ["quit", "exit", "stop"]:
                self.is_running = False
                print("Goodbye!")
                break

            ai_response = await self.text_handler.process_with_ai(user_input)
            print(f"\nRafiqi: {ai_response}\n") 