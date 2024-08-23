"""Init file for the generate_files module.

As I work through the build, I'll update the documentation for this module.
"""

from .nav import *
from .editor import *


def __getattr__(name: str):
    return getattr(FilesEditor.current(), name)
