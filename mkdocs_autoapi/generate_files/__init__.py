"""Init file for the generate_files module.

As I work through the build, I'll update the documentation for this module.
"""

from .editor import FilesEditor
from .nav import Nav as Nav


def __getattr__(name: str):
    return getattr(FilesEditor.current(), name)
