import pytest
from src.tools_time import (
    calc_elapsed, dttm_get, get_now,
    now_utc_get, sleep, sleep_until,
    temp_timer_begin, temp_timer_end
)
from datetime import datetime, timedelta
import time

def test_time_functions():
    """Test time utility functions"""
    now = get_now()
    assert isinstance(now, datetime)
    
    utc_now = now_utc_get()
    assert isinstance(utc_now, datetime)
    
    start = temp_timer_begin()
    time.sleep(0.1)
    elapsed = temp_timer_end(start)
    assert elapsed >= 0.1

def test_sleep_functions():
    """Test sleep functions"""
    start = time.time()
    sleep(0.1)
    elapsed = time.time() - start
    assert elapsed >= 0.1
    
    future = datetime.now() + timedelta(seconds=0.1)
    sleep_until(future)
    assert datetime.now() >= future 