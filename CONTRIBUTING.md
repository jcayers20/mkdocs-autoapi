# Contributing

We greatly appreciate contributions to the project! Please read the guidelines
below to get started.

## Issues and Discussions

If you've found a bug, have a question, or have an idea for a new feature,
please first check the [existing issues](https://github.com/jcayers20/mkdocs-autoapi/issues)
to see if your issue has already been reported. If it hasn't, you can create a
new issue by clicking the "New Issue" button on the issues page. The sections
below provide guidance on what to include in your issue.

### Bug Reports

When creating an issue for a bug, please include the following information:
* A clear and descriptive title starting with "Bug: "
* A detailed description of the bug
* Steps to reproduce the bug (preferably with a minimal working example)

### Feature Requests

When creating an issue for a feature request, please include the following
information:
* A clear and descriptive title starting with "Feature: "
* A detailed description of the feature

### Questions

If you have a question, please feel free to ask it in the [discussions](https://github.com/jcayers20/mkdocs-autoapi/discussions).
We'll do our best to answer as soon as possible. If your question ends up being
a bug or feature request, we'll work with you to create an issue for it.

## Setting Up a Local Development Environment

### Getting a Local Copy of the Project

To get started, you'll need to fork the repository and clone it to your machine.
GitHub has [a great guide](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo?tool=webui)
on how to do this.

### Creating a Virtual Environment

We recommend using a virtual environment to keep your environment isolated for
your work on this project. You can do this easily through the terminal. Note
that the project is intended to work with Python 3.6 or later, so we recommend
that you configure your interpreter to use Python 3.6.

On Linux:
```bash
$ python3 -m venv path/to/virtual_environment_directory # create
$ source path/to/virtual_environment_directory/bin/activate # activate
```

On Windows:
```shell
> python -m venv path\to\virtual_environment_directory # create
> path\to\virtual_environment_directory\Scripts\activate # activate
```

Python IDE's generally have built-in support for virtual environments, so you
can also set up a virtual environment through your IDE. Here are instructions
for setting up a virtual environment in some popular IDE's:
* [PyCharm](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html)
* [VS Code](https://code.visualstudio.com/docs/python/environments)

### Installing Requirements

Requirements are listed in `requirements.txt`. You can install them with pip:

```bash
pip install -r requirements.txt
```

### Enabling Pre-Commit Hooks

We use pre-commit hooks to ensure that code is formatted consistently. Please be
sure to enable these hooks before making changes.

```bash
pre-commit install
```

Once enabled, the pre-commit hooks will run automatically when you attempt to
commit changes. The first time you run the hooks, they may take a while to
complete as the environment is set up.

Note: Having `ruff` run on save will help you catch formatting problems before
they are caught by the pre-commit hooks. You can enable this in your IDE.

* [PyCharm](https://plugins.jetbrains.com/plugin/20574-ruff)
* [VS Code](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)

### Creating a Working Branch

Before you start making changes, you'll need to create a new branch to work in.
This helps keep your changes isolated from the main branch and makes it easier
to submit a pull request when you're done.

```bash
git checkout -b your-branch-name [source-branch-name]
```

Note that `source-branch-name` is the branch you're branching from. For now,
this will generally be `develop`. In the future, we will have versioned branches
for the next bugfix release, the next minor release, and the next major release.
Once we get there, you'll want to branch from the appropriate version branch.
* Bug fixes: Next bugfix release branch
* Features that are backwards-compatible: Next minor release branch
* Features that are not backwards-compatible: Next major release branch

## Submitting a Pull Request

When you're ready to submit your changes, you'll need to create a [pull request](https://docs.github.com/en/pull-requests).
to merge your changes into the appropriate branch. We'll review your changes,
provide feedback, and work with you to get your changes merged. Here are a few
things to keep in mind when submitting a pull request:

1. **Use a Descriptive Title**: Your pull request title should be descriptive
   and concise. It should give us a good idea of what your changes are about.
2. **Describe Your Changes**: Be sure to provide a clear description of the
   changes you've made and why you've made them. This helps us understand your
   changes.
3. **Reference Issues**: If your changes are related to an issue, be sure to
reference that issue in your pull request. If your work completes an issue, then
use closing keywords (e.g., `closes`, `fixes`, `resolves`) so that the issue
will be automatically closed when the pull request is merged.
