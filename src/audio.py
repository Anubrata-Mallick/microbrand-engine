import os
from elevenlabs.client import ElevenLabs

def generate_voiceover(text: str, voice_id: str = "JBFqnCBsd6RMkjVDRZzb") -> bytes:
    """Generates an MP3 audio voiceover using ElevenLabs API."""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY is not set.")
        
    client = ElevenLabs(api_key=api_key)
    audio_generator = client.text_to_speech.convert(
        voice_id=voice_id,  # Default: 'George' / warm authentic voice
        text=text,
        model_id="eleven_multilingual_v2"
    )
    
    # Read generator into raw bytes for Streamlit playback
    return b"".join(audio_generator)