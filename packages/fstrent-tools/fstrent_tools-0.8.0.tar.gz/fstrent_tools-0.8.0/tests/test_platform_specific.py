import platform
import pytest
from src import tools_terminal, tools_voice

@pytest.mark.skipif(platform.system() != 'Windows', 
                   reason="Windows-specific tests")
class TestWindowsFeatures:
    def test_windows_voice(self):
        """Test Windows-specific voice features"""
        pass

@pytest.mark.skipif(platform.system() != 'Linux', 
                   reason="Linux-specific tests")
class TestLinuxFeatures:
    def test_linux_terminal(self):
        """Test Linux-specific terminal features"""
        pass 