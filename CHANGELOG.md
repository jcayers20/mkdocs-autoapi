# Changelog

All notable changes to this project will be documented in this file.

The format is based on
[Keep a Changelog](https://www.keepachangelog.com/en/1.0.0/) and this project
adheres to [Semantic Versioning](https://www.semver.org/spec/v2.0.0.html).

## 0.3.0 - 2024-09-30

[View Changes on GitHub](https://github.com/jcayers20/mkdocs-autoapi/compare/0.2.0...0.3.0)

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

[View Changes on GitHub](https://www.github.com/jcayers20/mkdocs-autoapi/compare/0.2.0...0.2.1)

### Bug Fixes

- Fixed an ill-formed link in the requirements documentation
- Fixed a typo in a function name (this function was not user-facing)


## 0.2.0 - 2024-08-26

[View Changes on GitHub](https://www.github.com/jcayers20/mkdocs-autoapi/compare/0.1.6...0.2.0)

### Features

- Added documentation
- Added new configuration options:
  - `generate_local_output`: Define whether to create local copies of the
    auto-generated API documentation
  - `output_dir`: Define the directory in which the auto-generated API
    documentation will be stored
- Various bug fixes and improvements


## 0.1.6 - 2024-06-06

[View on GitHub](https://www.github.com/jcayers20/mkdocs-autoapi/tree/0.1.6)

First working version of the plugin.
