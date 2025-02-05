# Changelog

All notable changes to this project will be documented in this file.

The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.4.0 - 2025-02-05

[View Changes on GitHub](https://github.com/jcayers20/mkdocs-autoapi/compare/0.3.2...0.4.0)

### Bug Fixes

- Fixed `mkdocs` crash if both `repo_url` and `edit_uri` were provided in
`mkdocs.yml`
- Fixed navigation when using the `mkdocs` theme

### Features

- Enabled VBA support

## 0.3.2 - 2024-11-01

[View Changes on GitHub](https://github.com/jcayers20/mkdocs-autoapi/compare/0.3.1...0.3.2)

### Bug Fixes

- Fixed incorrect optional dependency configuration

## 0.3.1 - 2024-10-03

[View Changes on GitHub](https://github.com/jcayers20/mkdocs-autoapi/compare/0.3.0...0.3.1)

### Developer Support

- Added GitHub Actions for automated package publishing and release/milestone
  management on push to the `main` branch

## 0.3.0 - 2024-09-30

[View Changes on GitHub](https://github.com/jcayers20/mkdocs-autoapi/compare/0.2.1...0.3.0)

### Developer Support

- Added pre-commit hooks for code formatting and linting
- Added a development guide (`CONTRIBUTING.md`) to the documentation
- Added some logging to the plugin to help with debugging

### Features

- Renamed all existing configuration options to align with names used in
  `sphinx-autoapi`:
  - `project_root` to `autoapi_dir`
  - `exclude` to `autoapi_ignore`
  - `generate_local_output` to `autoapi_keep_files`
  - `output_dir` to `autoapi_root`
- Added new configuration options based on `sphinx-autoapi`:
  - `autoapi_file_patterns`: Define which files to include in the auto-generated
    documentation
  - `autoapi_generate_api_docs`: Define whether to generate API documentation
  - `autoapi_add_nav_entry`:  Define whether to add a navigation entry for the
    API documentation


## 0.2.1 - 2024-08-27

[View Changes on GitHub](https://github.com/jcayers20/mkdocs-autoapi/compare/0.2.0...0.2.1)

### Bug Fixes

- Fixed an ill-formed link in the requirements documentation
- Fixed a typo in a function name (this function was not user-facing)


## 0.2.0 - 2024-08-26

[View Changes on GitHub](https://github.com/jcayers20/mkdocs-autoapi/compare/0.1.6...0.2.0)

### Features

- Added documentation
- Added new configuration options:
  - `generate_local_output`: Define whether to create local copies of the
    auto-generated API documentation
  - `output_dir`: Define the directory in which the auto-generated API
    documentation will be stored
- Various bug fixes and improvements


## 0.1.6 - 2024-06-06

[View on GitHub](https://github.com/jcayers20/mkdocs-autoapi/tree/0.1.6)

First working version of the plugin.
