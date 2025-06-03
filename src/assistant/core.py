from ..voice.handler import VoiceHandler

class Assistant:
    """
    Core assistant class that coordinates different components and handles user interactions.
    """
    def __init__(self):
        self.voice_handler = VoiceHandler()
        self.is_listening = False

    def start_voice_interaction(self):
        """Start voice-based interaction"""
        self.is_listening = True
        while self.is_listening:
            # Listen for voice input
            user_input = self.voice_handler.listen()
            
            if user_input.lower() in ["stop", "quit", "exit"]:
                self.is_listening = False
                self.voice_handler.speak("Goodbye!")
                break

            # Process with AI if we got valid input
            if user_input not in ["No speech detected", "Could not understand audio", "Could not request results"]:
                # Get AI response
                ai_response = self.voice_handler.process_with_ai(user_input)
                
                # Speak the response
                self.voice_handler.speak(ai_response)
            else:
                self.voice_handler.speak(user_input)

    def process_text_input(self, text):
        """Process text input and return AI response"""
        return self.voice_handler.process_with_ai(text) 