import pytest
from src.tools_voice import (
    add_audio_to_video, change_audio_volume,
    convert_audio, extract_audio_from_video,
    get_audio_duration, list_voices,
    merge_audio, play_audio, speak
)
import os

@pytest.mark.skipif(not os.environ.get('RUN_VOICE_TESTS'),
                   reason="Voice tests are disabled by default")
class TestVoice:
    def test_voice_functions(self, tmp_path):
        """Test voice utility functions"""
        voices = list_voices()
        assert isinstance(voices, list)
    
    @pytest.mark.skip(reason="Requires audio hardware")
    def test_audio_playback(self):
        """Test audio playback"""
        speak("Test message")
        play_audio("test.wav")
    
    def test_audio_operations(self, tmp_path):
        """Test audio file operations"""
        test_audio = tmp_path / "test.wav"
        output_audio = tmp_path / "output.wav"
        
        # Mock audio file creation here
        
        with pytest.raises(FileNotFoundError):
            get_audio_duration("nonexistent.wav") 