"""Definiton of the globber class."""

# built-in imports
import fnmatch
import re
from pathlib import PurePosixPath
from typing import Iterator, Union

# local imports
from mkdocs.structure.files import Files


class MkDocsGlobber:
    """Globber for MkDocs files."""

    def __init__(self, files: Files):
        """Initialize an MkDocsGlobber object.

        Args:
            files:
                The MkDocs files object.
        """
        self.files = {}
        self.dirs = {}
        self.index_dirs = {}

        for f in files:
            if not f.is_documentation_page():
                continue

            path = PurePosixPath("/", f.src_uri)
            self.files[path] = True
            tail, head = path.parent, path.name

            if f.name == "index":
                self.index_dirs[tail] = path

            while True:
                self.dirs[tail] = True

                if not head:
                    break

                tail, head = tail.parent, tail.name

    def isdir(self, path: str) -> bool:
        """Check if `path` is a directory."""
        return PurePosixPath("/", path) in self.dirs

    def glob(self, pattern: str) -> Iterator[str]:
        """Glob `pattern`."""
        pat_parts = PurePosixPath("/" + pattern).parts
        re_parts = [re.compile(fnmatch.translate(part)) for part in pat_parts]

        for collection in self.files, self.dirs:
            for path in collection:
                if len(path.parts) == len(re_parts):
                    zipped = zip(path.parts, re_parts)
                    next(
                        zipped
                    )  # Both path and pattern have a slash as their first part.
                    if all(re_part.match(part) for part, re_part in zipped):
                        yield str(path)[1:]

    def find_index(self, root: str) -> Union[str, None]:
        """Find the index file for `root`."""
        root_path = PurePosixPath("/", root)
        if root_path in self.index_dirs:
            return str(self.index_dirs[root_path])[1:]
        return None
