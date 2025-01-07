import pytest
import platform
from src.tools_terminal import clear_screen
from src.tools_sounds import play_sound

def test_platform_detection():
    """Test platform-specific detection"""
    system = platform.system()
    assert system in ['Windows', 'Linux', 'Darwin']

@pytest.mark.skipif(platform.system() != 'Windows', 
                   reason="Windows-specific test")
def test_windows_features():
    """Test Windows-specific features"""
    # Add Windows-specific tests here
    pass

@pytest.mark.skipif(platform.system() != 'Linux',
                   reason="Linux-specific test")
def test_linux_features():
    """Test Linux-specific features"""
    # Add Linux-specific tests here
    pass

@pytest.mark.skipif(platform.system() != 'Darwin',
                   reason="MacOS-specific test")
def test_macos_features():
    """Test MacOS-specific features"""
    # Add MacOS-specific tests here
    pass 