import re
from typing import Optional

__all__ = [
    'extract_url',
    'is_valid_url',
    'make_clickable',
    'print_clickable_link',
    'short_link'
]

def _supports_hyperlinks() -> bool:
    """Check if the terminal supports hyperlinks."""
    import os
    
    # Check if NO_COLOR is set (respecting the NO_COLOR standard)
    if os.getenv('NO_COLOR') is not None:
        return False
        
    # Check for known terminals that support hyperlinks
    term = os.getenv('TERM', '')
    if 'xterm' in term or 'vte' in term or 'kitty' in term:
        return True
        
    # Check for Windows Terminal
    if os.getenv('WT_SESSION'):
        return True
        
    return False

def short_link(url: str, display_text: Optional[str] = None) -> str:
    """Create a clickable terminal hyperlink with optional display text."""
    display = display_text or url
    if _supports_hyperlinks():
        return f'\033]8;;{url}\033\\{display}\033]8;;\033\\'
    return display  # Fallback to just showing the display text

def make_clickable(text: str, url: str) -> str:
    """Make text clickable with a URL."""
    return short_link(url, text)

def extract_url(hyperlink: str) -> Optional[str]:
    """Extract URL from a terminal hyperlink."""
    pattern = r'\033\]8;;(.*?)\033\\'
    match = re.search(pattern, hyperlink)
    return match.group(1) if match else None

def is_valid_url(url: str) -> bool:
    """Check if string is a valid URL."""
    pattern = r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$'
    return bool(re.match(pattern, url))

def print_clickable_link(url, display_text):
    # Use the OSC 8 escape sequence to start the hyperlink
    # Then use the ST escape to stop it.
    print(f'\033]8;;{url}\033\\{display_text}\033]8;;\033\\')

