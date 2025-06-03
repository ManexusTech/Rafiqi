import speech_recognition as sr
from openai import OpenAI
import pyttsx3
import os
from dotenv import load_dotenv

load_dotenv()

class VoiceHandler:
    def __init__(self):
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        
        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def listen(self):
        """Listen for voice input and convert to text"""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio)
                return text
            except sr.WaitTimeoutError:
                return "No speech detected"
            except sr.UnknownValueError:
                return "Could not understand audio"
            except sr.RequestError:
                return "Could not request results"

    def speak(self, text):
        """Convert text to speech"""
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    async def process_with_ai(self, text):
        """Process text with OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Rafiqi, a helpful AI assistant."},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error processing with AI: {str(e)}" 