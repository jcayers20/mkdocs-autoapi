# Usage

## Setting the Project Root

By default, the plugin considers the directory containing `mkdocs.yml` the
project root directory. To use a different directory, specify the directory
path in the `autoapi_dir` configuration option. The path can be absolute or
relative to the directory containing `mkdocs.yml`.

```yaml
plugins:
  - ... other plugin configuration ...
  - mkdocs-autoapi:
      autoapi_dir: path/to/autoapi/dir
  - mkdocstrings
```

A common use case for this option is projects using the
[src layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/).

!!! note "Notes"

    If a directory containing `__init__.py` is specified, then the directory
    will be included in the relative path of its children. If not, then the
    directory will not be included.

    Be sure to include the `autoapi_dir` directory in the `paths` configuration
    for the `mkdocstrings` handler to ensure that the documentation is generated
    relative to the correct directory. If `autoapi_dir` does not contain
    `__init__.py`, then `autoapi_dir` must be included. If it does, then the
    parent directory of `autoapi_dir` must be included. For more information,
    see the `mkdocstrings` [documentation](https://mkdocstrings.github.io/python/usage/#using-the-paths-option).

!!! example

    Consider a project with the following structure:

    ```tree
    project/
        .venv/
            ...
        docs/
            index.md
        src/
            awesome_package/
                __init__.py
                module.py
        tools/
            generate_awesomeness.py
            decrease_world_suck.py
        mkdocs.yml
        noxfile.py
        pyproject.toml
        README.md
        setup.py
    ```

    For this project, it may or may not be desirable to include the `tools`
    directory in the API reference and we probably don't want to include
    the `*.py` files in the top-level directory. To ignore these items, we can
    set `autoapi_dir` to `src`:

    ```yaml title="mkdocs.yml"
    plugins:
      - ... other plugin configuration ...
      - mkdocs-autoapi:
          autoapi_dir: src # or /path/to/project/src
      - mkdocstrings:
          handlers:
            python:
              paths:
                - src
    ```

## Ignoring Patterns

The `autoapi_ignore` configuration option allows for exclusion of files matching
the specified pattern(s). This option accepts a list of [glob](https://man7.org/linux/man-pages/man7/glob.7.html)
patterns. These patterns are evaluated relative to
[autoapi_dir](#setting-the-project-root).

!!! note
    The following patterns are commonly used for virtual environments and are
    always ignored:

    `venv/**/*.py` <br>
    `.venv/**/*.py`

!!! example

    Consider a project with the following structure:

    ```tree
    project/
        docs/
            index.md
        module/
            __init__.py
            lorem.py
            ipsum.py
            dolor.py
        second_module/
            __init__.py
            lorem.py
            sit.py
            amet.py
        mkdocs.yml
        README.md
    ```

    Suppose we want to ignore all files named `lorem.py` and all files in the
    `second_module` directory. We can add the following configuration to
    `mkdocs.yml`:

    ```yaml title="mkdocs.yml"
    plugins:
      - ... other plugin configuration ...
      - mkdocs-autoapi:
          autoapi_ignore:
            - **/lorem.py
            - second_module/**/*.py
      - mkdocstrings
    ```

## Controlling Output

The plugin supports two configuration options for
controlling output:

1. `generate_local_output` (`bool`): If `True`, then the plugin will generate
   local copies of the Markdown files in `<docs_dir>/<output_dir>`. If `False`,
   Markdown files will only be created in temp directory. Default is `False`.
2. `output_dir` (`str`): The directory in which to save the generated Markdown
   files. For local output, this directory is relative to `docs_dir`. Default
   is `autoapi`.

!!! example

    Consider a project with the following structure:

    ```tree
    project/
        docs/
            index.md
        module/
            __init__.py
            lorem.py
            ipsum.py
            dolor.py
        second_module/
            __init__.py
            lorem.py
            sit.py
            amet.py
        mkdocs.yml
        README.md
    ```

    To generate local copies of the Markdown files in a directory named `api`,
    add the following configuration to `mkdocs.yml`:

    ```yaml title="mkdocs.yml"
    nav:
      - ... other navigation sections ...
      - API Reference: api/
      - ... other navigation sections ...

    plugins:
      - ... other plugin configuration ...
      - mkdocs-autoapi:
          generate_local_output: True
          output_dir: api
      - mkdocstrings
    ```

## Putting It All Together

!!! example

    Consider a project with the following structure:

    ```tree
    project/
        docs/
            index.md
        module/
            __init__.py
            lorem.py
            ipsum.py
            dolor.py
        second_module/
            __init__.py
            lorem.py
            sit.py
            amet.py
        mkdocs.yml
        README.md
    ```

    A minimal `mkdocs.yml` file for this project might look like this:

    ```yaml title="mkdocs.yml"
    site_name: Project

    nav:
      - Home: index.md
      - API Reference: autoapi/

    plugins:
      - search
      - mkdocs-autoapi
      - mkdocstrings
    ```
