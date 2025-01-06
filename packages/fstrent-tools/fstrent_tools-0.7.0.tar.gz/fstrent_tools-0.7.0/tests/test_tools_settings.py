import pytest
import tempfile
import os
from src.tools_settings import (
    get_setting, set_setting, load_settings,
    save_settings, reset_settings
)

@pytest.fixture
def temp_settings_file():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        yield f.name
    os.unlink(f.name)

def test_settings_operations(temp_settings_file):
    """Test settings operations"""
    # Test setting and getting
    set_setting("test_key", "test_value", temp_settings_file)
    assert get_setting("test_key", temp_settings_file) == "test_value"
    
    # Test saving and loading
    settings = {"key1": "value1", "key2": "value2"}
    save_settings(settings, temp_settings_file)
    loaded = load_settings(temp_settings_file)
    assert loaded == settings
    
    # Test reset
    reset_settings(temp_settings_file)
    assert load_settings(temp_settings_file) == {} 