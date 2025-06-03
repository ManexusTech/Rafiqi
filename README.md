# Rafiqi: Offline AI Personal Assistant

## Overview
Rafiqi is an **offline personal assistant** built with privacy in mind. It operates entirely on your local device, providing the support of an intelligent assistant while ensuring that no data is sent to the cloud. With Rafiqi, you have a **companion** that's always there to help, without compromising your privacy.

### Key Features:
- **Voice Input**: Local speech-to-text and text-to-speech.
- **AI Integration**: Powered by OpenAI's GPT models
- **Privacy Focused**: Minimal data storage, with clear user control
- **Task Management**: Organize your life with reminders, to-do lists, and calendar events.
- **Modular**: Easily extendable with new plugins or functionalities.

### Getting Started

#### Requirements:
- Python 3.8+
- OpenAI API key
- Microphone for voice input
- Speakers for voice output

#### Installation:
1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Rafiqi.git
   cd Rafiqi
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a .env file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

5. Run the assistant:
   ```bash
   python src/main.py
   ```

### Usage
Once running, Rafiqi will listen for your voice input. Speak clearly into your microphone and wait for the response. Say "stop", "quit", or "exit" to end the session.

### Note
Make sure you have a working microphone and speakers set up on your system. The first time you run the program, you may need to grant microphone permissions.
