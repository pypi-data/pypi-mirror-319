import pytest
from src.tools_terminal import clear_screen
import platform

@pytest.mark.skipif(platform.system() not in ['Windows', 'Linux', 'Darwin'],
                   reason="OS not supported")
def test_clear_screen():
    """Test clear screen function"""
    try:
        clear_screen()
        assert True  # If we get here, no exception was raised
    except Exception as e:
        pytest.fail(f"clear_screen() raised {e}") 