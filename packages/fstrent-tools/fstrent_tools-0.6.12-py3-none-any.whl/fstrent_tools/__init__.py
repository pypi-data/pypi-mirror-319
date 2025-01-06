"""
fstrent_tools - A comprehensive collection of Python utility functions.
"""

__version__ = "0.6.12"

# Import all functions from each module
from .tools_convert import *
from .tools_debug import *
from .tools_decorators import *
from .tools_dicts import *
from .tools_errors import *
from .tools_eval import *
from .tools_files import *
from .tools_formatting import *
from .tools_hyperlinks import *
from .tools_json import *
from .tools_logging import *
from .tools_object import *
from .tools_print import *
from .tools_python import *
from .tools_settings import *
from .tools_sounds import *
from .tools_speak import *
from .tools_strings import *
from .tools_terminal import *
from .tools_time import *
from .tools_video import *
from .tools_voice import *

# Define __all__ to specify which names should be exported
__all__ = []

# Dynamically collect all exported names from imported modules
for module_name in ['tools_convert', 'tools_debug', 'tools_decorators', 'tools_dicts', 'tools_errors', 'tools_eval', 'tools_files', 'tools_formatting', 'tools_hyperlinks', 'tools_json', 'tools_logging', 'tools_object', 'tools_print', 'tools_python', 'tools_settings', 'tools_sounds', 'tools_speak', 'tools_strings', 'tools_terminal', 'tools_time', 'tools_video', 'tools_voice']:
    module = globals().get(module_name)
    if module and hasattr(module, '__all__'):
        __all__.extend(module.__all__)
