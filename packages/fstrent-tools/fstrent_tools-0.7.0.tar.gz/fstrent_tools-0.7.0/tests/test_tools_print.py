import pytest
from src.tools_print import (
    clear_screen, print_adv, print_clickable_link,
    print_func_name, print_line, section_header
)

def test_print_functions(capsys):
    """Test print functions"""
    print_adv("Test message")
    captured = capsys.readouterr()
    assert "Test message" in captured.out
    
    print_line("-", 10)
    captured = capsys.readouterr()
    assert "-" * 10 in captured.out
    
    section_header("Test Section")
    captured = capsys.readouterr()
    assert "Test Section" in captured.out 