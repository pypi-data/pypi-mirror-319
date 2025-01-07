from typing import Any, Union

from .tools_eval import HasVal

def to_int(val: Any, default: int = 0) -> int:
    """Convert value to integer with fallback default."""
    try:
        return int(val)
    except (ValueError, TypeError):
        return default

def to_float(val: Any, default: float = 0.0) -> float:
    """Convert value to float with fallback default."""
    try:
        return float(val)
    except (ValueError, TypeError):
        return default

def to_str(val: Any) -> str:
    """Convert value to string."""
    return str(val)

def int2tf(val: int) -> bool:
    """Convert integer to boolean (0 = False, non-0 = True)."""
    return bool(val)

def tf2int(val: bool) -> int:
    """Convert boolean to integer (False = 0, True = 1)."""
    return 1 if val else 0

def dec(val: Union[int, float], precision: int = 2) -> float:
    """Round a number to specified precision."""
    try:
        return round(float(val), precision)
    except (ValueError, TypeError):
        return 0.0

def dec_prec(val: Union[int, float], precision: int = 2) -> str:
    """Format a number with specified precision as string."""
    try:
        return f"{float(val):.{precision}f}"
    except (ValueError, TypeError):
        return f"0.{'0' * precision}"

def tf(val: Any) -> bool:
    """
    Convert various types to boolean.
    True values: 'yes', 'true', '1', 1, True
    False values: 'no', 'false', '0', 0, False, None
    """
    if isinstance(val, str):
        return val.lower() in ('yes', 'true', '1')
    return bool(val)

def IsEnglish(text: str) -> bool:
    """Check if text contains only ASCII characters."""
    try:
        text.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False

def getRaw(val: Any) -> str:
    """Get raw string representation of a value."""
    if isinstance(val, str):
        return f"'{val}'"
    return str(val) 