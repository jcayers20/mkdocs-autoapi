# mkdocs-autoapi

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
in the `project_root` configuration option:

```yaml
plugins:
  - ... other plugin configuration ...
  - mkdocs-autoapi:
      project_root: /path/to/project/root
  - mkdocstrings
```

### Excluding Patterns

You can exclude files and directories from the documentation by specifying a
value in the `exclude` configuration option. This option accepts a list of
glob patterns. Note that the following patterns are always excluded:

* `**/.venv/**/`
* `**/venv/**/`

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

To exclude all files named `lorem.py`, you can add the following configuration
to your `mkdocs.yml` file:

```yaml
plugins:
  - ... other plugin configuration ...
  - mkdocs-autoapi:
      exclude:
        - "**/lorem.py"
  - mkdocstrings
```

## Contributing

Contributions are always welcome! Please submit a pull request or open an issue
to get started.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/jcayers20/mkdocs-autoapi/blob/main/LICENSE) file
for more information.
