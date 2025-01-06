import pytest
import os
from src.tools_files import (
    create_directory, dir_val, ensure_dir,
    file_copy, file_delete, file_list,
    file_move, file_read, file_write,
    get_file_age_minutes
)

@pytest.fixture
def temp_test_dir(tmp_path):
    """Create a temporary test directory"""
    return tmp_path

def test_directory_operations(temp_test_dir):
    """Test directory operations"""
    test_dir = temp_test_dir / "test_dir"
    
    create_directory(test_dir)
    assert test_dir.exists()
    
    assert dir_val(test_dir) is True
    ensure_dir(test_dir / "subdir")
    assert (test_dir / "subdir").exists()

def test_file_operations(temp_test_dir):
    """Test file operations"""
    test_file = temp_test_dir / "test.txt"
    test_content = "Hello, World!"
    
    file_write(test_file, test_content)
    assert test_file.exists()
    assert file_read(test_file) == test_content
    
    copy_file = temp_test_dir / "copy.txt"
    file_copy(test_file, copy_file)
    assert copy_file.exists()
    
    move_file = temp_test_dir / "moved.txt"
    file_move(copy_file, move_file)
    assert move_file.exists()
    assert not copy_file.exists()
    
    file_delete(test_file)
    assert not test_file.exists() 