import pytest
import asyncio
from unittest.mock import Mock, patch
from src.voice.handler import VoiceHandler

@pytest.fixture
def voice_handler():
    return VoiceHandler()

def test_initialization(voice_handler):
    """Test if VoiceHandler initializes correctly"""
    assert voice_handler.recognizer is not None
    assert voice_handler.tts_engine is not None
    assert voice_handler.client is not None
    assert len(voice_handler.conversation_history) == 1
    assert voice_handler.conversation_history[0]["role"] == "system"

@pytest.mark.asyncio
async def test_process_with_ai():
    """Test AI processing with a mock response"""
    handler = VoiceHandler()
    
    # Mock the OpenAI response
    mock_response = Mock()
    mock_response.choices = [Mock(message=Mock(content="Test response"))]
    
    with patch.object(handler.client.chat.completions, 'create', return_value=mock_response):
        response = await handler.process_with_ai("Test input")
        assert response == "Test response"
        assert len(handler.conversation_history) == 3  # system + user + assistant

@pytest.mark.asyncio
async def test_conversation_history_limit():
    """Test if conversation history is properly limited"""
    handler = VoiceHandler()
    
    # Mock the OpenAI response
    mock_response = Mock()
    mock_response.choices = [Mock(message=Mock(content="Test response"))]
    
    # Generate more than 10 conversation turns
    with patch.object(handler.client.chat.completions, 'create', return_value=mock_response):
        for i in range(12):
            await handler.process_with_ai(f"Test input {i}")
    
    # Check if history is limited to 11 messages (1 system + 10 conversation)
    assert len(handler.conversation_history) == 11
    assert handler.conversation_history[0]["role"] == "system"

def test_error_handling(voice_handler):
    """Test error handling in speech recognition"""
    with patch('speech_recognition.Recognizer.listen', side_effect=Exception("Test error")):
        result = voice_handler.listen()
        assert "Could not request results" in result 