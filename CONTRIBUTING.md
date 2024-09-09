# Contributing

We greatly appreciate contributions to the project! Please read the guidelines
below to get started.

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
