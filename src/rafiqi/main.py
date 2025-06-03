from .core.assistant import Assistant
import asyncio

async def main():
    assistant = Assistant()
    print("Welcome to Rafiqi - Your AI Assistant!")
    await assistant.start_interaction()

if __name__ == "__main__":
    asyncio.run(main()) 