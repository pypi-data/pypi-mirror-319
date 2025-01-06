import os
import pytest
from src import tools_files

def test_file_operations(tmp_path):
    """Test file handling functions"""
    # Create a temporary test file
    test_file = tmp_path / "test.txt"
    test_content = "Hello, World!"
    
    # Test file writing
    tools_files.file_write(test_file, test_content)
    assert test_file.exists()
    
    # Test file reading
    content = tools_files.file_read(test_file)
    assert content == test_content
    
    # Test file deletion
    tools_files.file_delete(test_file)
    assert not test_file.exists()

def test_directory_operations(tmp_path):
    """Test directory handling functions"""
    test_dir = tmp_path / "test_dir"
    
    # Test directory creation
    tools_files.create_directory(test_dir)
    assert test_dir.exists() 