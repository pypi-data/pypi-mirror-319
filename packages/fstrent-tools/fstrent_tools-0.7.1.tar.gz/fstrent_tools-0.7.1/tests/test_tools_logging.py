import pytest
import logging
import os
from src.tools_logging import (
    log_debug, log_error, log_exception,
    log_info, log_warning, plogit, setup_logger
)

@pytest.fixture
def temp_log_file(tmp_path):
    """Create a temporary log file"""
    return tmp_path / "test.log"

def test_logger_setup(temp_log_file):
    """Test logger setup"""
    logger = setup_logger("test_logger", str(temp_log_file))
    assert isinstance(logger, logging.Logger)
    assert os.path.exists(temp_log_file)

def test_logging_levels(temp_log_file):
    """Test different logging levels"""
    logger = setup_logger("test_logger", str(temp_log_file))
    
    test_msg = "Test message"
    log_debug(test_msg, logger=logger)
    log_info(test_msg, logger=logger)
    log_warning(test_msg, logger=logger)
    log_error(test_msg, logger=logger)
    
    with open(temp_log_file) as f:
        content = f.read()
        assert "DEBUG" in content
        assert "INFO" in content
        assert "WARNING" in content
        assert "ERROR" in content

def test_exception_logging(temp_log_file):
    """Test exception logging"""
    logger = setup_logger("test_logger", str(temp_log_file))
    
    try:
        raise ValueError("Test error")
    except ValueError as e:
        log_exception(e, logger=logger)
    
    with open(temp_log_file) as f:
        content = f.read()
        assert "ValueError" in content
        assert "Test error" in content

def test_plogit(temp_log_file, capsys):
    """Test print and log functionality"""
    logger = setup_logger("test_logger", str(temp_log_file))
    
    test_msg = "Test message"
    plogit(test_msg, logger=logger)
    
    # Check console output
    captured = capsys.readouterr()
    assert test_msg in captured.out
    
    # Check log file
    with open(temp_log_file) as f:
        assert test_msg in f.read() 