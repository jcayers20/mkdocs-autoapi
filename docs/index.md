# mkdocs-autoapi

`mkdocs-autoapi` is a plugin for [MkDocs](https://www.mkdocs.org) that generates
API documentation from your project's source code. The plugin leverages the
functionality provided by [mkdocstrings](https://mkdocstrings.github.io/) and
locates all Python modules in your project to create a set of reference pages.

## Installation

### Requirements

`mkdocs-autoapi` requires the following:

* Python version 3.6 or higher
* MkDocs version 1.4.0 or higher
* mkdocstrings version 0.19.0 or higher

In addition, you must install an `mkdocstrings`
[handler](https://mkdocstrings.github.io/usage/handlers/) for your project's
programming language. We currently only support Python, but support for more
languages is planned.

### Installation via `pip`

To install `mkdocs-autoapi` with `pip`:

```bash
pip install mkdocs-autoapi
```

Extras are provided to support installation of `mkdocstrings``s Python handler:

```bash
pip install mkdocs-autoapi[python] # new Python handler
```

```bash
pip install mkdocs-autoapi[python-legacy] # legacy Python handler
```

## Basic Usage

To get started using `mkdocs-autoapi`, simply add the following to `mkdocs.yml`:

```yaml

plugins:
  - ... other plugin configuration ...
  - mkdocs-autoapi
  - mkdocstrings
```

For details on configuration and examples, see the [Usage](usage.md) section.
