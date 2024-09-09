"""Logic to resolve directories in navigation."""

# built-in imports
import os
from typing import Optional, Tuple, Union

# third-party imports
import mkdocs.structure
from mkdocs.structure.pages import Page

# local imports
from mkdocs_autoapi.generate_files.editor import Files
from mkdocs_autoapi.literate_nav import parser
from mkdocs_autoapi.literate_nav.globber import MkDocsGlobber


def resolve_directories_in_nav(
    nav_data,
    files: Files,
    nav_file_name: str,
    implicit_index: bool,
    markdown_config: Optional[dict] = None,
):
    """Replace `directory/` references in MkDocs nav config.

    Directories, if found, are resolved by the rules of literate nav insertion:
    If it has a literate nav file, that is used. Otherwise, an implicit nav is
    generated.
    """

    def get_nav_for_dir(path: str) -> Union[Tuple[str, str], None]:
        file = files.get_file_from_path(os.path.join(path, nav_file_name))
        if not file:
            return None

        # Prevent the warning in case the user doesn't also end up including
        # this page in the final nav, maybe they want it only for the purpose of
        # feeding to this plugin.
        try:  # MkDocs 1.5+
            if file.inclusion.is_in_nav():
                file.inclusion = (
                    mkdocs.structure.files.InclusionLevel.NOT_IN_NAV
                )
        except AttributeError:
            # https://github.com/mkdocs/mkdocs/blob/ff0b726056/mkdocs/structure/nav.py#L113
            Page(None, file, {})  # type: ignore[arg-type]

        # https://github.com/mkdocs/mkdocs/blob/fa5aa4a26e/mkdocs/structure/pages.py#L120
        with open(file.abs_src_path, encoding="utf-8-sig") as f:
            return nav_file_name, f.read()

    globber = MkDocsGlobber(files)
    nav_parser = parser.NavParser(
        get_nav_for_dir,
        globber,
        implicit_index=implicit_index,
        markdown_config=markdown_config,
    )

    result = None
    if not nav_data or get_nav_for_dir("."):
        result = nav_parser.markdown_to_nav()
    return result or nav_parser.resolve_yaml_nav(nav_data or [])
