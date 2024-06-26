"""Logic used to implement AutoAPI functionality.

As I work through the build, I'll update the documentation for this module.
"""

# built-in imports
import os
from pathlib import Path
from typing import Iterable, Optional, Set

# third-party imports

# local imports
import mkdocs_autoapi
from mkdocs_autoapi.generate_files import editor
from mkdocs_autoapi.generate_files import nav


def identify_files_to_documment(
    path: Path,
    exclude: Optional[Iterable[str]] = None,
) -> Set[Path]:
    """Get a set of all Python files for which documentation must be generated.

    This function finds all Python files located in `path`, then removes any
    that match at least one member of `exclude`.

    Steps:
        1.  Get set of all Python files in `path`.
        2.  For each pattern in `exclude`, get set of all files matching the
            pattern and reduce the set of Python files to only those files that
            *do not* match the pattern.
        3.  Return the final set of files to include.

    Args:
        path:
            The path to search.
        exclude:
            The patterns to exclude.

    Returns (Set[pathlib.Path]):
        The set of all Python files in `path` that *do not* match any member of
        `exclude`.
    """
    # Step 1
    files_to_document = set(path.rglob(pattern="*.py"))

    # Step 2
    if exclude:
        for pattern in exclude:
            excluded_files = set(path.rglob(pattern=pattern))
            files_to_document = files_to_document.difference(excluded_files)

    # Step 3
    return {p.resolve() for p in files_to_document}


def create_docs(
    root: Path,
    exclude: Optional[Iterable[str]] = None,
) -> None:
    """Use AutoAPI approach to create documentation for a project.

    Steps:
        1.  Create a new `Nav` object.
        2.  Get the set of all Python files to document.
        3.  For each file found:
            1.  Get the module path and document path.
            2.  Get the module path parts.
            3.  Remove the last part of the module path parts if it is
                "\_\_init\_\_".
            4.  Create a new entry in the `Nav` object.
            5.  Create the module identifier.
            6.  Create the documentation file.
            7.  Set the edit path.
        4.  Write the navigation to `autoapi/summary.md`.

    Args:
        root:
            The root directory of the project.
        exclude:
            The patterns to exclude. Defaults to None.
        output_target:
            The target directory for the generated AutoAPI documentation.
            Defaults to None.
        summary_target:
            The target file for the generated AutoAPI summary. Defaults to None.

    Returns:
        None.
    """
    # Step 1
    navigation = nav.Nav()

    # Step 2
    files_to_document = identify_files_to_documment(path=root, exclude=exclude)

    # Step 3
    for file in sorted(files_to_document):

        # Step 3.1
        try:
            module_path = file.relative_to(root.resolve()).parent.with_suffix("")
        except ValueError:
            module_path = Path("")
        doc_path = file.relative_to(file.parent).with_suffix(".md")
        full_doc_path = "autoapi" / module_path / doc_path

        # Step 3.2
        module_path_parts = list(module_path.parts)
        module_path_parts.append(doc_path.stem)
        module_path_parts = tuple(module_path_parts)

        # Step 3.3
        if module_path_parts[-1] == "__init__":
            module_path_parts = module_path_parts[:-1]
            doc_path = doc_path.with_name("index.md")
            full_doc_path = full_doc_path.with_name("index.md")

        # Step 3.4
        navigation[module_path_parts] = (module_path / doc_path).as_posix()

        # Step 3.5
        module_identifier = ".".join(module_path_parts)

        # Step 3.6

        if not full_doc_path.parents[0].exists():
            print(full_doc_path)
            os.makedirs(full_doc_path.parents[0])
        with open(full_doc_path, "w") as doc:
            print(f"::: {module_identifier}", file=doc)
        with mkdocs_autoapi.generate_files.open(full_doc_path, "w") as doc:
            print(f"::: {module_identifier}", file=doc)

        # Step 3.7
        mkdocs_autoapi.generate_files.set_edit_path(full_doc_path, file)

    # Step 4
    with mkdocs_autoapi.generate_files.open("autoapi/summary.md", "w") as nav_file:
        nav_file.writelines(navigation.build_literate_nav())
