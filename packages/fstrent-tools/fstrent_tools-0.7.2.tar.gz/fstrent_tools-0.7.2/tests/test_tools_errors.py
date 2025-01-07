import pytest
from src.tools_errors import format_exception

def test_format_exception():
    """Test exception formatting"""
    try:
        raise ValueError("Test error")
    except ValueError as e:
        formatted = format_exception(e)
        assert "ValueError" in formatted
        assert "Test error" in formatted
        assert "Traceback" in formatted 