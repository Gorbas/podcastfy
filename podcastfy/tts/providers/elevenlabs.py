"""ElevenLabs TTS provider implementation."""

from elevenlabs import client as elevenlabs_client
from elevenlabs.types import VoiceSettings
from ..base import TTSProvider
from typing import List, Optional

class ElevenLabsTTS(TTSProvider):
    def __init__(self, api_key: str, model: str = "eleven_multilingual_v2"):
        """
        Initialize ElevenLabs TTS provider.

        Args:
            api_key (str): ElevenLabs API key
            model (str): Model name to use. Defaults to "eleven_multilingual_v2"
        """
        self.client = elevenlabs_client.ElevenLabs(api_key=api_key)
        self.model = model

    def generate_audio(self, text: str, voice: str, model: str, voice2: str = None) -> bytes:
        """Generate audio using ElevenLabs API."""
        voice_id, voice_dict = self.parse_voice(voice)

        voice = self.get_voice(voice_id)
        voiceSettings = voice.settings
        if 'stability' not in voice_dict:
            voice_dict['stability'] = voiceSettings.stability
        if 'similarity_boost' not in voice_dict:
            voice_dict['similarity_boost'] = voiceSettings.similarity_boost
        if 'style' not in voice_dict:
            voice_dict['style'] = voiceSettings.style
        if 'use_speaker_boost' not in voice_dict:
            voice_dict['use_speaker_boost'] = voiceSettings.use_speaker_boost
        if 'speed' not in voice_dict:
            voice_dict['speed'] = voiceSettings.speed

        voiceSettings = VoiceSettings(
            stability=voice_dict['stability'],
            similarity_boost=voice_dict['similarity_boost'],
            style=voice_dict['style'],
            use_speaker_boost=voice_dict['use_speaker_boost'],
            speed=voice_dict['speed']
        )
        audio = self.client.generate(
            text=text,
            voice=voice,
            voice_settings=voiceSettings,
            model=model
        )
        return b''.join(chunk for chunk in audio if chunk)

    def get_voice(self, voice_id: str):
        """Get voice object from ElevenLabs API."""
        return self.client.voices.get(
            voice_id=voice_id,
            with_settings=True
        )

    def parse_voice(self, voice: str):
        """Parse voice string into a dictionary."""
        voice = voice.replace(' ', '')
        voice = voice.replace(')', '')
        voice = voice.split('(')

        voice_name = voice[0]
        voice_dict = {}

        if len(voice) > 1:
            voice = voice[1].split('|')
            for v in voice:
                v = v.split('=')
                key = v[0]
                value = v[1]
                if key in ['stability', 'similarity_boost', 'style', 'speed']:
                    voice_dict[key] = float(value)
                elif key == 'use_speaker_boost':
                    voice_dict[key] = value.lower() == 'true' or value == '1' or value.lower() == 'yes'
                else:
                    voice_dict[key] = value

        return voice_name, voice_dict

    def get_supported_tags(self) -> List[str]:
        """Get supported SSML tags."""
        return ['lang', 'p', 'phoneme', 's', 'sub']