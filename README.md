# mkdocs-autoapi

[![pypi version](https://img.shields.io/pypi/v/mkdocs-autoapi.svg)](https://pypi.org/project/mkdocs-autoapi/)
[![docs](https://readthedocs.org/projects/mkdocs-autoapi/badge/?version=latest)](https://mkdocs-autoapi.readthedocs.io/en/latest/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)


## Description

`mkdocs-autoapi` is a MkDocs plugin that automatically generates API
documentation from your project's source code. The idea for the plugin comes
from this [recipe](https://mkdocstrings.github.io/recipes/#automatic-code-reference-pages)
in the MkDocs documentation.

## Installation

### Requirements

* Python version 3.6 or higher
* MkDocs version 1.4.0 or higher
* mkdocstrings version 0.19.0 or higher

### Installation via `pip`

We recommend installing this package with `pip`:

```bash
pip install mkdocs-autoapi
```

## Usage

### Basic Usage

To use the plugin, add the following configuration to your `mkdocs.yml` file:

```yaml
plugins:
  - ... other plugin configuration ...
  - mkdocs-autoapi
  - mkdocstrings
```

### Setting the Project Root

By default, the plugin will use the current working directory as the project
root. If you would like to use a different directory, you can specify a value
in the `autoapi_dir` configuration option:

```yaml
plugins:
  - ... other plugin configuration ...
  - mkdocs-autoapi:
      autoapi_dir: /path/to/autoapi/dir
  - mkdocstrings
```

### Including and Ignoring Patterns

You can ignore files and directories from the documentation by specifying a
value in the `autoapi_ignore` configuration option. This option accepts a list
of glob patterns. Note that the following patterns are always ignored:

* `**/.venv/**/`
* `**/venv/**/`

Likewise, the `autoapi_file_patterns` configuration option allows for control of
which files are included in the API reference. This option also accepts a list
of glob patterns which are evaluated (recursively) relative to `autoapi_dir`. By
default, all files with `.py` and `.pyi` extensions are included.

As an example, suppose your project has the following structure:

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
    venv/
    mkdocs.yml
    README.md
```

To ignore all files named `lorem.py`, you can add the following configuration
to your `mkdocs.yml` file:

```yaml
plugins:
  - ... other plugin configuration ...
  - mkdocs-autoapi:
      autoapi_ignore:
        - "**/lorem.py"
      autoapi_file_patterns:
        - "*.py"
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

Example: To include the API documentation in the navigation under the section
"Reference", add the following configuration to `mkdocs.yml`:

```yaml
plugins:
  - ... other plugin configuration ...
  - mkdocs-autoapi:
      autoapi_add_nav_entry: Reference
  - mkdocstrings
```

Example: To disable the automatic addition of the API documentation to the
navigation and add a manual link to the API documentation, add the following
configuration to `mkdocs.yml`:

```yaml
nav:
  - ... other navigation configuration ...
  - API: autoapi/ # target should be `autoapi_root`
  - ... other navigation configuration ...
```

More information on navigation configuration can be found in the
[MkDocs User Guide](https://www.mkdocs.org/user-guide/configuration/#nav).

### Putting It All Together

Again, consider the following project structure:

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
    venv/
    mkdocs.yml
    README.md
```

A full `mkdocs.yml` for the project might look like this:

```yaml mkdocs.yml
site_name: Project

nav:
  - Home: index.md
  - API Reference: autoapi/

plugins:
  - mkdocs-autoapi
  - mkdocstrings

theme:
  name: readthedocs
```

More information MkDocs configuration through `mkdocs.yml` can be found in the
[MkDocs User Guide](https://www.mkdocs.org/user-guide/configuration/).

## Contributing

Contributions are always welcome! Please submit a pull request or open an issue
to get started.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/jcayers20/mkdocs-autoapi/blob/main/LICENSE) file
for more information.
