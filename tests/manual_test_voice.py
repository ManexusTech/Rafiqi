import asyncio
from src.voice.handler import VoiceHandler

async def test_voice_interaction():
    handler = VoiceHandler()
    
    print("\n=== Testing Voice Recognition ===")
    print("Speak something when 'Listening...' appears")
    text = handler.listen()
    print(f"Recognition result: {text}")
    
    print("\n=== Testing Text-to-Speech ===")
    test_text = "This is a test of the text to speech system."
    print(f"Speaking: '{test_text}'")
    handler.speak(test_text)
    
    print("\n=== Testing AI Integration ===")
    print("Speak a question when 'Listening...' appears")
    user_input = handler.listen()
    if user_input not in ["No speech detected", "Could not understand audio", "Could not request results"]:
        print("Processing with AI...")
        response = await handler.process_with_ai(user_input)
        print(f"AI Response: {response}")
        print("Speaking response...")
        handler.speak(response)

async def main():
    try:
        await test_voice_interaction()
    except Exception as e:
        print(f"Error during test: {str(e)}")
    
    print("\nTest completed!")

if __name__ == "__main__":
    asyncio.run(main()) 