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

### Ignoring Patterns

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

### Including API Documentation in Navigation

To include the API documentation created by the plugin in your site's
navigation, you can add the following configuration to your `mkdocs.yml` file:

```yaml
nav:
  - ... other navigation sections ...
  - API Reference: autoapi/
  - ... other navigation sections ...
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
