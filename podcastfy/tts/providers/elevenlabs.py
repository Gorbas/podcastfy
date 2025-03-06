"""ElevenLabs TTS provider implementation."""

from elevenlabs import client as elevenlabs_client
from ..base import TTSProvider
from typing import List

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
        if 'stability' in voice_dict:
            voiceSettings.stability = voice_dict['stability']
        if 'similarity_boost' in voice_dict:
            voiceSettings.similarity_boost = voice_dict['similarity_boost']
        if 'style' in voice_dict:
            voiceSettings.style = voice_dict['style']
        if 'use_speaker_boost' in voice_dict:
            voiceSettings.use_speaker_boost = voice_dict['use_speaker_boost']
        if 'speed' in voice_dict:
            voiceSettings.speed = voice_dict['speed']

        # mock generation so that it will not actually generate audio, but it will simply write logs
        # audio = self.client.generate(
        #     text=text,
        #     voice=voice,
        #     voice_settings=voiceSettings,
        #     model=model
        # )
        # return b''.join(chunk for chunk in audio if chunk)

        # Print the parameters that we would pass to the API as string
        print(f"ElevenLabs API: text={text}, voice={voice}, voice_settings={voiceSettings}, model={model}")

        return b''

    def get_voice(self, voice_id: str) -> Voice:
        """Get voice object from ElevenLabs API."""
        return self.client.voices.get(
            voice_id=voice_id,
            with_settings=True
        )

    def parse_voice(self, voice: str) -> str, dict:
        """Parse voice string into a dictionary."""
        voice = voice.replace(' ', '')
        voice = voice.replace(')', '')
        voice = voice.split('(')

        voice_name = voice[0]

        if len(voice) > 1:
            voice = voice[1].split(',')

        voice_dict = {}
        for v in voice:
            v = v.split('=')
            voice_dict[v[0]] = v[1]
        return voice_name, voice_dict

    def get_supported_tags(self) -> List[str]:
        """Get supported SSML tags."""
        return ['lang', 'p', 'phoneme', 's', 'sub']