# Usage

## Setting the Project Root

By default, the plugin considers the directory containing `mkdocs.yml` the
project root directory. To use a different directory, specify the directory
path in the `project_root` configuration option. The path can be absolute or
relative to the directory containing `mkdocs.yml`.

```yaml
plugins:
  - ... other plugin configuration ...
  - mkdocs-autoapi:
      project_root: path/to/project/root
  - mkdocstrings
```

A common use case for this option is projects using the
[src layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/).

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
    the `*.py` files in the top-level directory. To exclude these items, we can
    set `project_root` to `src`:

    ```yaml title="mkdocs.yml"
    plugins:
      - ... other plugin configuration ...
      - mkdocs-autoapi:
          project_root: src # or /path/to/project/src
      - mkdocstrings
    ```

## Excluding Patterns

The `exclude` configuration option allows for exclusion of files matching the
specified pattern(s). This option accepts a list of
[glob](https://man7.org/linux/man-pages/man7/glob.7.html) patterns. These
patterns are evaluated relative to [project_root](#setting-the-project-root).

!!! note
    The following patterns are commonly used for virtual environments and are
    always excluded:

    `./.venv/**/*.py` <br>
    `./venv/**/*.py`

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

    Suppose we want to exclude all files named `lorem.py` and all files
    in the `second_module` directory. We can add the following configuration to
    `mkdocs.yml`:

    ```yaml title="mkdocs.yml"
    plugins:
      - ... other plugin configuration ...
      - mkdocs-autoapi:
          exclude:
            - **/lorem.py
            - second_module/**/*.py
      - mkdocstrings
    ```

## Including API Documentation in Navigation

Auto-generated API documentation is saved to the `autoapi` directory. To include
API documentation in your site's navigation, add the following configuration to
`mkdocs.yml`:

```yaml title="mkdocs.yml"
nav:
  - ... other navigation sections ...
  - API Reference: autoapi/
  - ... other navigation sections ...
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


