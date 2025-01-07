import pytest
import os
from src.tools_sounds import (
    play_beep, play_cash, play_doh,
    play_file, play_sw_imperial_march
)

@pytest.fixture
def sound_files():
    """Fixture to verify sound files exist"""
    sound_dir = os.path.join(os.path.dirname(__file__), '..', 'sounds')
    return {
        'doh': os.path.join(sound_dir, 'doh.wav'),
        'thunder': os.path.join(sound_dir, 'thunder.wav'),
        'wolf': os.path.join(sound_dir, 'wolf.wav'),
        'wolf2': os.path.join(sound_dir, 'wolf2.wav')
    }

def test_sound_files_exist(sound_files):
    """Test that all required sound files exist"""
    for name, path in sound_files.items():
        assert os.path.exists(path), f"Sound file {name} not found at {path}"

@pytest.mark.skipif(not os.environ.get('RUN_SOUND_TESTS'),
                   reason="Sound tests disabled")
class TestSoundPlayback:
    def test_play_sound_file(self, sound_files):
        """Test playing specific sound files"""
        for path in sound_files.values():
            play_file(path)
    
    def test_play_effects(self):
        """Test playing sound effects"""
        play_beep()
        play_cash()
        play_doh()
        play_sw_imperial_march() 