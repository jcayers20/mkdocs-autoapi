"""Logic used to implement AutoAPI functionality.

As I work through the build, I'll update the documentation for this module.
"""

# built-in imports
import os
from pathlib import Path
from typing import Iterable, Optional, Set

# third-party imports
from mkdocs.config.defaults import MkDocsConfig

# local imports
import mkdocs_autoapi
from mkdocs_autoapi.generate_files import editor
from mkdocs_autoapi.generate_files import nav


def identify_files_to_document(
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
            excluded_files = set(path.glob(pattern=pattern))
            files_to_document = files_to_document.difference(excluded_files)

    # Step 3
    return {p.resolve() for p in files_to_document}


def create_docs(
    config: MkDocsConfig,
) -> None:
    """Use AutoAPI approach to create documentation for a project.

    Steps:
        1.  Define variables.
        2.  Create a new `Nav` object.
        3.  Get the set of all Python files to document.
        4.  For each file found:
            1.  Get the module path and document path.
            2.  Get the module path parts.
            3.  Remove the last part of the module path parts if it is
                "\\_\\_init\\_\\_".
            4.  Create a new entry in the `Nav` object.
            5.  Create the module identifier.
            6.  Create the documentation file.
            7.  Set the edit path.
        5.  Write the navigation to `autoapi/summary.md`.

    Args:
        config:
            The MkDocs configuration object.

    Returns:
        None.
    """
    # Step 1
    root = Path(config["project_root"])
    exclude = config["exclude"]
    docs_dir = Path(config["docs_dir"])
    output_dir = config["output_dir"]
    generate_local_output = config["generate_local_output"]
    local_summary_path = docs_dir / output_dir / "summary.md"
    temp_summary_path = f"{output_dir}/summary.md"

    # Step 2
    navigation = nav.Nav()

    # Step 3
    files_to_document = identify_files_to_document(path=root, exclude=exclude)

    # Step 4
    if (root / "__init__.py").exists():
        root = root.parent

    # Step 4
    for file in sorted(files_to_document):

        # Step 4.1
        try:
            module_path = file.relative_to(root.resolve()).parent.with_suffix("")
        except ValueError:
            module_path = Path("")
        doc_path = file.relative_to(file.parent).with_suffix(".md")
        full_temp_doc_path = output_dir / module_path / doc_path
        full_local_doc_path = docs_dir / full_temp_doc_path

        # Step 4.2
        module_path_parts = list(module_path.parts)
        module_path_parts.append(doc_path.stem)
        module_path_parts = tuple(module_path_parts)

        # Step 4.3
        if module_path_parts[-1] == "__init__":
            if len(module_path_parts) == 1:
                continue
            module_path_parts = module_path_parts[:-1]
            doc_path = doc_path.with_name("index.md")
            full_local_doc_path = full_local_doc_path.with_name("index.md")
            full_temp_doc_path = full_temp_doc_path.with_name("index.md")

        # Step 4.4
        navigation[module_path_parts] = (module_path / doc_path).as_posix()

        # Step 4.5
        module_identifier = ".".join(module_path_parts)

        # Step 4.6
        if generate_local_output:
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

        # Step 4.7
        mkdocs_autoapi.generate_files.set_edit_path(full_temp_doc_path, file)

    # Step 5
    if generate_local_output:
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

    with mkdocs_autoapi.generate_files.open(temp_summary_path, "w") as temp_nav_file:
        temp_nav_file.writelines(navigation.build_literate_nav())
