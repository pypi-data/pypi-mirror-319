import pytest
from src.tools_hyperlinks import (
    extract_url, is_valid_url, make_clickable,
    print_clickable_link, short_link
)
from io import StringIO
import sys

def test_url_validation():
    """Test URL validation functions"""
    assert is_valid_url("https://example.com") is True
    assert is_valid_url("not_a_url") is False
    assert is_valid_url("http://localhost:8000") is True

def test_url_extraction():
    """Test URL extraction from terminal links"""
    test_link = "\033]8;;https://example.com\033\\Click me\033]8;;\033\\"
    assert extract_url(test_link) == "https://example.com"

def test_link_creation():
    """Test hyperlink creation functions"""
    url = "https://example.com"
    text = "Click me"
    
    clickable = make_clickable(text, url)
    assert url in clickable
    assert text in clickable
    
    short = short_link(url, text)
    assert url in short
    assert text in short

def test_print_clickable(capsys):
    """Test printing clickable links"""
    url = "https://example.com"
    text = "Click me"
    
    print_clickable_link(url, text)
    captured = capsys.readouterr()
    assert url in captured.out
    assert text in captured.out 