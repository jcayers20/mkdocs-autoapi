"""File editor logic - copied from mkdocs-gen-files."""

# built-in imports
import collections
import os
import os.path
import pathlib
import shutil
from typing import IO, MutableMapping, Optional, Union

# third-party imports
from mkdocs.config import load_config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File, Files


def file_sort_key(f: File):
    """Sort key for file."""
    parts = pathlib.PurePosixPath(f.src_uri).parts
    return tuple(
        chr(f.name != "index" if i == len(parts) - 1 else 2) + p
        for i, p in enumerate(parts)
    )


class FilesEditor:
    """Context manager for editing files in a MkDocs build."""

    config: MkDocsConfig
    """The current MkDocs [config](https://www.mkdocs.org/user-guide/plugins/#config)."""
    directory: str
    """The base directory for `open()` ([docs_dir](https://www.mkdocs.org/user-guide/configuration/#docs_dir))."""
    edit_paths: MutableMapping[str, Union[str, None]]

    def open(
        self, name: str, mode, buffering=-1, encoding=None, *args, **kwargs
    ) -> IO:
        """Open a file under `docs_dir` virtually.

        This function, for all intents and purposes, is just an `open()` which
        pretends that it is running under [docs_dir](https://www.mkdocs.org/user-guide/configuration/#docs_dir).
        Write operations don't affect the actual files when running as part of
        an MkDocs build, but they do become part of the site build.
        """
        path = self._get_file(name, new="w" in mode)
        if encoding is None and "b" not in mode:
            encoding = "utf-8"
        return open(path, mode, buffering, encoding, *args, **kwargs)

    def _get_file(self, name: str, new: bool = False) -> str:
        """Get file path for `name`, creating it if necessary."""
        new_f = File(
            name,
            src_dir=self.directory,
            dest_dir=self.config.site_dir,
            use_directory_urls=self.config.use_directory_urls,
        )
        new_f.generated_by = "mkdocs-gen-files"  # type: ignore[attr-defined]
        normname = pathlib.PurePath(name).as_posix()

        if new or normname not in self._files:
            os.makedirs(os.path.dirname(new_f.abs_src_path), exist_ok=True)
            self._files[normname] = new_f
            self.edit_paths.setdefault(normname, None)
            return new_f.abs_src_path

        f = self._files[normname]
        if f.abs_src_path != new_f.abs_src_path:
            os.makedirs(os.path.dirname(new_f.abs_src_path), exist_ok=True)
            self._files[normname] = new_f
            self.edit_paths.setdefault(normname, None)
            shutil.copyfile(f.abs_src_path, new_f.abs_src_path)
            return new_f.abs_src_path

        return f.abs_src_path

    def set_edit_path(self, name: str, edit_name: Union[str, None]) -> None:
        """Choose a file path to use for the edit URI of this file."""
        self.edit_paths[pathlib.PurePath(name).as_posix()] = edit_name and str(
            edit_name
        )

    def __init__(
        self,
        files: Files,
        config: MkDocsConfig,
        directory: Optional[str] = None,
    ):
        """Initialize a FilesEditor object."""
        self._files: MutableMapping[str, File] = collections.ChainMap(
            {}, {f.src_uri: f for f in files}
        )
        self.config = config
        if directory is None:
            directory = config.docs_dir
        self.directory = directory
        self.edit_paths = {}

    _current = None
    _default = None

    @classmethod
    def current(cls):
        """Get FilesEditor instance for current MkDocs build.

        If used as part of a MkDocs build (*gen-files* plugin), it's an instance
        using virtual files that feed back into the build.

        If not, this still tries to load the MkDocs config to find out the
        `docs_dir`, and then actually performs any file writes that happen via
        `.open()`.

        Warning:
            This is global (not thread-safe).
        """
        if cls._current:
            return cls._current
        if not cls._default:
            config = load_config("mkdocs.yml")
            config.plugins.run_event("config", config)
            cls._default = FilesEditor(Files([]), config)
        return cls._default

    def __enter__(self):
        """Set current instance to this one."""
        type(self)._current = self
        return self

    def __exit__(self, *exc):
        """Clear current instance."""
        type(self)._current = None

    @property
    def files(self) -> Files:
        """Access current file structure.

        [Files]: https://github.com/mkdocs/mkdocs/blob/master/mkdocs/structure/files.py
        """
        files = sorted(self._files.values(), key=file_sort_key)
        return Files(files)
