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

## Including and Ignoring Patterns

The `autoapi_ignore` configuration option allows for exclusion of files matching
the specified pattern(s). This option accepts a list of [glob](https://man7.org/linux/man-pages/man7/glob.7.html)
patterns. These patterns are evaluated relative to
[autoapi_dir](#setting-the-project-root).

Likewise, the `autoapi_file_patterns` configuration option allows for control of
which files are included in the API reference. This option also accepts a list
of glob patterns which are evaluated (recursively) relative to `autoapi_dir`. By
default, all files with `.py` and `.pyi` extensions are included.

!!! note
    The following patterns are commonly used for virtual environments and are
    always ignored:

    `venv/**/*` <br>
    `.venv/**/*`

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
          autoapi_file_patterns:
            - *.py # ignoring .pyi to improve performance since no stubs present
      - mkdocstrings
    ```

## Controlling Output

The plugin supports two configuration options for
controlling output:

1. `autoapi_keep_files` (`bool`): If `True`, then the plugin will generate local
    copies of the Markdown files in `<docs_dir>/<autoapi_root>`. If `False`,
    Markdown files will only be created in temp directory. Default is `False`.
2. `autoapi_root` (`str`): The directory in which to save the generated Markdown
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
    plugins:
      - ... other plugin configuration ...
      - mkdocs-autoapi:
          autoapi_keep_files: True
          autoapi_root: api
      - mkdocstrings
    ```

## Disabling API Documentation Generation

To disable API documentation generation, set the `autoapi_generate_api_docs`
configuration option to `False`. This is useful when transitioning to manual
documentation or when the API documentation is not needed.

## Including API Documentation in Navigation

The inclusion of API documentation in the navigation can be controlled via the
configuration option `autoapi_add_nav_entry`. This option accepts either a
boolean value or a string. Behavior is as follows:

* If `True`, then a section named "API Reference" will be added to the end of
the navigation.
* If `False`, then no section for the API documentation will be added. In this
case, a manual link to the API documentation can be added to the navigation.
* If a string, then a section with the specified name will be added to the end
of the navigation.

!!! example

    To include the API documentation in the navigation under the section
    "Reference", add the following configuration to `mkdocs.yml`:

    ```yaml title="mkdocs.yml"
    plugins:
      - ... other plugin configuration ...
      - mkdocs-autoapi:
          autoapi_add_nav_entry: Reference
      - mkdocstrings
    ```

!!! example

    To disable automatic addition of the API documentation to the navigation and
    instead add a manual link, add the following configuration to `mkdocs.yml`:

    ```yaml title="mkdocs.yml"
    nav:
      - Home: index.md
      - API: autoapi/ # target should be `autoapi_root`
      - Examples: examples.md

    plugins:
      - ... other plugin configuration ...
      - mkdocs-autoapi:
          autoapi_add_nav_entry: False
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

    plugins:
      - search
      - mkdocs-autoapi
      - mkdocstrings
    ```
