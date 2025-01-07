import pytest
import os
from src.tools_sounds import (
    play_beep, play_cash, play_doh,
    play_file, play_sw_imperial_march
)

@pytest.mark.sound
class TestSounds:
    def test_sound_files_exist(self):
        """Verify sound files exist"""
        sound_dir = os.path.join(os.path.dirname(__file__), '..', 'sounds')
        required_files = ['doh.wav', 'thunder.wav', 'wolf.wav', 'wolf2.wav']
        
        for file in required_files:
            assert os.path.exists(os.path.join(sound_dir, file))
    
    @pytest.mark.skipif(not os.environ.get('RUN_SOUND_TESTS'),
                       reason="Sound playback tests disabled")
    def test_sound_playback(self):
        """Test sound playback functions"""
        play_beep()  # Should not raise exception
        play_doh()   # Should not raise exception 