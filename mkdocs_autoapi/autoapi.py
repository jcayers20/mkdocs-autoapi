"""Logic used to implement AutoAPI functionality.

As I work through the build, I'll update the documentation for this module.
"""

# built-in imports
import os
from collections import OrderedDict
from pathlib import Path
from typing import Iterable, List, Optional, Set

# third-party imports
from mkdocs.config.defaults import MkDocsConfig

# local imports
import mkdocs_autoapi
from mkdocs_autoapi.generate_files import nav
from mkdocs_autoapi.logging import get_logger

logger = get_logger("mkdocs-autoapi")


def identify_files_to_document(
    path: Path,
    autoapi_file_patterns: List[str],
    autoapi_ignore: Optional[Iterable[str]] = None,
) -> Set[Path]:
    """Get a set of all Python files for which documentation must be generated.

    This function finds all Python files located in `path`, then removes any
    that match at least one member of `autoapi_ignore`.

    Steps:
        1.  Get set of all files matching `autoapi_file_patterns` in `path`.
        2.  For each pattern in `autoapi_ignore`, get set of all files matching
            the pattern and reduce the set of Python files to only those files
            that *do not* match the pattern.
        3.  Return the final set of files to include.

    Args:
        path:
            The path to search.
        autoapi_file_patterns:
            The patterns to search for.
        autoapi_ignore:
            The patterns to autoapi_ignore.

    Returns (Set[pathlib.Path]):
        The set of all Python files in `path` that *do not* match any member of
        `autoapi_ignore`.
    """
    # Step 1
    reversed_autoapi_file_patterns = autoapi_file_patterns.copy()
    reversed_autoapi_file_patterns.reverse()

    # Step 1
    files_to_document = OrderedDict()
    for pattern in reversed_autoapi_file_patterns:
        pattern_matches = set(path.rglob(pattern=pattern))
        for file in pattern_matches:
            file_key = file.with_suffix(suffix="")
            files_to_document.update({file_key: file})
    files_to_document = set(files_to_document.values())

    # Step 2
    if autoapi_ignore:
        for pattern in autoapi_ignore:
            autoapi_ignored_files = set(path.glob(pattern=pattern))
            files_to_document = files_to_document.difference(
                autoapi_ignored_files
            )

    # Step 3
    return {p.resolve() for p in files_to_document}


def add_autoapi_nav_entry(
    config: MkDocsConfig,
) -> None:
    """Add the AutoAPI section to the navigation.

    Steps:
        1.  Create the `autoapi_root_ref` variable.
        2.  Create the `autoapi_section_title` variable.
        3.  Append the AutoAPI section to the navigation.

    Args:
        config:
            The MkDocs configuration object.

    Returns:
        None; the navigation is updated in place.
    """
    # Step 1
    if not config["autoapi_root"].endswith("/"):
        autoapi_root_ref = f"{config['autoapi_root']}/"
    else:
        autoapi_root_ref = config["autoapi_root"]

    # Step 2
    if config["autoapi_add_nav_entry"] is True:
        autoapi_section_title = "API Reference"
    else:
        autoapi_section_title = config["autoapi_add_nav_entry"]

    # Step 3
    config.nav.append({autoapi_section_title: autoapi_root_ref})


def create_docs(
    config: MkDocsConfig,
) -> None:
    r"""Use AutoAPI approach to create documentation for a project.

    Steps:
        1.  Define variables.
        2.  Add the AutoAPI section to the navigation if desired.
        3.  Create a new `Nav` object.
        4.  Get the set of all Python files to document.
        5.  If `autoapi_dir` is a package, adjust `autoapi_dir` to its parent.
        6.  For each file found:
            1.  Get the module path and document path.
            2.  Get the module path parts.
            3.  Remove the last part of the module path parts if it is
                "\_\_init\_\_".
            4.  Create a new entry in the `Nav` object.
            5.  Create the module identifier.
            6.  Create the documentation file.
            7.  Set the edit path.
        7.  Write the navigation to `autoapi/summary.md`.

    Args:
        config:
            The MkDocs configuration object.

    Returns:
        None.
    """
    # Step 1
    logger.debug(msg="Generating AutoAPI documentation ...")
    autoapi_dir = Path(config["autoapi_dir"])
    autoapi_ignore = config["autoapi_ignore"]
    autoapi_file_patterns = config["autoapi_file_patterns"]
    autoapi_add_nav_entry = config["autoapi_add_nav_entry"]
    docs_dir = Path(config["docs_dir"])
    autoapi_root = config["autoapi_root"]
    autoapi_keep_files = config["autoapi_keep_files"]
    local_summary_path = docs_dir / autoapi_root / "summary.md"
    temp_summary_path = f"{autoapi_root}/summary.md"

    # Step 2
    if autoapi_add_nav_entry:
        add_autoapi_nav_entry(config=config)
        logger.debug(msg="... Added AutoAPI section to navigation ...")
    else:
        logger.debug(msg="... Skipped adding AutoAPI section to navigation ...")
    if autoapi_keep_files:
        local_path = docs_dir / autoapi_root
        logger.debug(
            msg=f"... AutoAPI files will be saved locally in {local_path} ..."
        )
    else:
        logger.debug(msg="... AutoAPI files will not be saved locally ...")

    # Step 3
    navigation = nav.Nav()

    # Step 4
    files_to_document = identify_files_to_document(
        path=autoapi_dir,
        autoapi_file_patterns=autoapi_file_patterns,
        autoapi_ignore=autoapi_ignore,
    )
    logger.debug(
        msg=f"... Found {len(files_to_document)} files to document ..."
    )

    # Step 5
    if (autoapi_dir / "__init__.py").exists():
        autoapi_dir = autoapi_dir.parent
        logger.debug(msg="... Adjusted AutoAPI directory to parent package ...")

    # Step 6
    for file in sorted(files_to_document):
        # Step 6.1
        try:
            module_path = file.relative_to(
                autoapi_dir.resolve()
            ).parent.with_suffix("")
        except ValueError:
            module_path = Path("")
        doc_path = file.relative_to(file.parent).with_suffix(".md")
        full_temp_doc_path = autoapi_root / module_path / doc_path
        full_local_doc_path = docs_dir / full_temp_doc_path

        # Step 6.2
        module_path_parts = list(module_path.parts)
        module_path_parts.append(doc_path.stem)
        module_path_parts = tuple(module_path_parts)

        # Step 6.3
        if module_path_parts[-1] == "__init__":
            if len(module_path_parts) == 1:
                continue
            module_path_parts = module_path_parts[:-1]
            doc_path = doc_path.with_name("index.md")
            full_local_doc_path = full_local_doc_path.with_name("index.md")
            full_temp_doc_path = full_temp_doc_path.with_name("index.md")

        # Step 6.4
        navigation[module_path_parts] = (module_path / doc_path).as_posix()

        # Step 6.5
        module_identifier = ".".join(module_path_parts)

        # Step 6.6
        if autoapi_keep_files:
            if not full_local_doc_path.parents[0].exists():
                os.makedirs(full_local_doc_path.parents[0])

            try:
                with open(full_local_doc_path, "r+") as doc:
                    old_content = doc.read()
                    new_content = f"::: {module_identifier}\n"

                    if old_content != new_content:
                        doc.seek(0)
                        doc.write(new_content)
                        doc.truncate()

            except FileNotFoundError:
                with open(full_local_doc_path, "w") as doc:
                    print(f"::: {module_identifier}", file=doc)

        with mkdocs_autoapi.generate_files.open(full_temp_doc_path, "w") as doc:
            print(f"::: {module_identifier}", file=doc)

        # Step 6.7
        mkdocs_autoapi.generate_files.set_edit_path(full_temp_doc_path, file)

    # Step 7
    if autoapi_keep_files:
        try:
            with open(local_summary_path, "r+") as local_nav_file:
                old_content = local_nav_file.read()
                literate_nav = list(navigation.build_literate_nav())
                new_content = "".join(literate_nav)

                if old_content != new_content:
                    local_nav_file.seek(0)
                    local_nav_file.write(new_content)
                    local_nav_file.truncate()

        except FileNotFoundError:
            with open(local_summary_path, "w") as local_nav_file:
                local_nav_file.writelines(navigation.build_literate_nav())

        logger.debug(
            msg=f"... Saved AutoAPI summary file locally in {local_summary_path} ..."  # noqa: E501
        )

    with mkdocs_autoapi.generate_files.open(
        temp_summary_path, "w"
    ) as temp_nav_file:
        temp_nav_file.writelines(navigation.build_literate_nav())
    logger.debug("... Finished generating AutoAPI documentation.")
