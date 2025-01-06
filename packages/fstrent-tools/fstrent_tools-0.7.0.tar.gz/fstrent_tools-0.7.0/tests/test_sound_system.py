import os
import pytest
from src import tools_sounds

@pytest.mark.skipif(not os.environ.get('RUN_SOUND_TESTS'), 
                   reason="Sound tests are disabled by default")
class TestSoundSystem:
    def test_sound_files_exist(self):
        """Verify all required sound files are present"""
        sound_files = ['doh.wav', 'thunder.wav', 'wolf.wav', 'wolf2.wav']
        sound_dir = os.path.join(os.path.dirname(__file__), '..', 'sounds')
        
        for sound_file in sound_files:
            assert os.path.exists(os.path.join(sound_dir, sound_file))
    
    def test_play_functions(self):
        """Test sound playing functions"""
        # These tests might need to be mocked or skipped in CI
        pass 