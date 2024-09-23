"""Plugin definition for mkdocs-autoapi."""

# built-in imports
import collections
import os
import tempfile
import urllib.parse
from pathlib import Path
from typing import Optional

# third-party imports
from jinja2 import Environment
from mkdocs.config import Config, config_options
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation, Section
from mkdocs.structure.pages import Page

# local imports
from mkdocs_autoapi.autoapi import add_autoapi_nav_entry, create_docs
from mkdocs_autoapi.generate_files.editor import FilesEditor
from mkdocs_autoapi.literate_nav import resolve
from mkdocs_autoapi.logging import get_logger
from mkdocs_autoapi.section_index import rewrite
from mkdocs_autoapi.section_index.section_page import SectionPage

logger = get_logger(name="mkdocs-autoapi")


class AutoApiPluginConfig(Config):
    """Configuration options for plugin."""

    autoapi_dir = config_options.Dir(exists=True, default=".")
    autoapi_file_patterns = config_options.ListOfItems(
        config_options.Type(str),
        default=["*.py", "*.pyi"],
    )
    autoapi_ignore = config_options.ListOfItems(
        config_options.Type(str), default=[]
    )
    autoapi_keep_files = config_options.Type(bool, default=False)
    autoapi_generate_api_docs = config_options.Type(bool, default=True)
    autoapi_add_nav_entry = config_options.Type((str, bool), default=True)
    autoapi_root = config_options.Type(str, default="autoapi")


class AutoApiPlugin(BasePlugin[AutoApiPluginConfig]):
    """Plugin logic definition."""

    def on_config(self, config: MkDocsConfig) -> Optional[Config]:
        """Validate the plugin configuration.

        # Step 1
            1.  Check if `mkdocstrings` is included in plugin configuration.
            2a. If `mkdocstrings` is included, then validate its configuration.
                1.  Get the `mkdocstrings` configuration object.
                2.  If `mkdocstrings` is not enabled, then warn the user.
                3.  Get the `handlers` configuration.
                4.  Identify the AutoAPI directory. If the value provided by the
                    user is a Python package, then get the parent directory.
                    Otherwise, use the provided value.
                5.  Check if the AutoAPI directory is included in the paths for
                    each `mkdocstrings` handler. If not, then warn the user.
            2b. If `mkdocstrings` is not included, then warn the user.
            3.  Return.


        Args:
            config:
                The MkDocs configuration object.

        Returns:
            The validated plugin configuration.
        """
        # Step 1
        logger.debug(msg="Validating plugin configuration ...")
        is_mkdocstrings_included = "mkdocstrings" in list(config.plugins.keys())

        # Step 2a
        if is_mkdocstrings_included:
            # Step 2a.1
            mkdocstrings_configuration = config.plugins["mkdocstrings"].config

            # Step 2a.2
            if not mkdocstrings_configuration.enabled:
                logger.warning(
                    msg="mkdocstrings is not enabled.\n    HINT: Set `enabled: True` in mkdocstrings configuration."  # noqa: E501
                )

            # Step 2a.3
            mkdocstrings_handlers_configuration = (
                mkdocstrings_configuration.handlers
            )
            if mkdocstrings_handlers_configuration == dict():
                mkdocstrings_handlers_configuration = {
                    mkdocstrings_configuration.default_handler: {"paths": ["."]}
                }

            # Step 2a.4
            autoapi_dir = Path(self.config.autoapi_dir).absolute()
            if "__init__.py" in os.listdir(autoapi_dir):
                autoapi_dir = autoapi_dir.parent.absolute()

            # Step 2a.5
            mkdocs_yml_dir = Path(config.config_file_path).parent.absolute()
            for handler in mkdocstrings_handlers_configuration.keys():
                paths = [
                    Path(
                        os.path.abspath(os.path.join(mkdocs_yml_dir, p))
                    ).absolute()
                    for p in mkdocstrings_handlers_configuration[handler][
                        "paths"
                    ]
                ]
                if autoapi_dir not in paths:
                    relative_autoapi_dir = os.path.relpath(
                        path=autoapi_dir,
                        start=mkdocs_yml_dir,
                    ).replace("\\", "/")
                    logger.warning(
                        msg=f'AutoAPI directory not found in paths for `mkdocstrings` handler "{handler}".\n    HINT: Add "{relative_autoapi_dir}" to the `paths` list in the `mkdocstrings` handler configuration.'  # noqa: E501
                    )

        # Step 2b
        else:
            logger.warning(
                msg="mkdocstrings is not included in mkdocs configuration.\n    HINT: Add `mkdocstrings` to the `plugins` list in mkdocs configuration file."  # noqa: E501
            )

        # Step 3
        return config

    def on_files(self, files: Files, config: MkDocsConfig) -> Files:
        """Generate autoAPI documentation files.

        Steps:
            1.  Create a temporary directory to store the generated files.
            2.  Ignore the virtual environment from the documentation if it is
                not already ignored.
            3.  Create the autoAPI documentation files.
            4.  Store the paths of the generated files.
            5.  Return the updated files object.

        Args:
            files:
                The MkDocs files object.
            config:
                The MkDocs configuration.

        Returns:
            The updated MkDocs files object.
        """
        # Step 1
        self._dir = tempfile.TemporaryDirectory(
            prefix="autoapi",
        )
        config.update(self.config)

        # Step 2
        if "venv/**/*.py" not in self.config.autoapi_ignore:
            self.config.autoapi_ignore.append("venv/**/*.py")
        if ".venv/**/*.py" not in self.config.autoapi_ignore:
            self.config.autoapi_ignore.append(".venv/**/*.py")

        # Step 4
        with FilesEditor(
            files=files,
            config=config,
            directory=self._dir.name,
        ) as editor:
            try:
                if self.config.autoapi_generate_api_docs:
                    create_docs(config=config)
                elif self.config.autoapi_add_nav_entry:
                    add_autoapi_nav_entry(config=config)
                    logger.debug(msg="Added AutoAPI section to navigation.")
            except Exception as e:
                raise PluginError(str(e))

        # Step 5
        self._edit_paths = dict(editor.edit_paths)

        # Step 6
        markdown_extensions = config.markdown_extensions
        markdown_config = {
            "markdown_extensions": markdown_extensions,
            "extension_configs": config["mdx_configs"],
            "tab_length": 4,
        }

        # Step 7
        config.nav = resolve.resolve_directories_in_nav(
            nav_data=config.nav,
            files=editor.files,
            nav_file_name="summary.md",
            implicit_index=False,
            markdown_config=markdown_config,
        )
        self._files = editor.files

        # Step 8
        return editor.files

    def on_nav(self, nav: Navigation, config, files) -> Navigation:
        """Apply plugin-specific transformations to the navigation."""
        todo = collections.deque((nav.items,))
        while todo:
            items = todo.popleft()
            for i, section in enumerate(items):
                if not isinstance(section, Section) or not section.children:
                    continue
                todo.append(section.children)
                page = section.children[0]
                if not isinstance(page, Page):
                    continue
                assert not page.children
                if not page.title and page.url:
                    page.__class__ = SectionPage
                    assert isinstance(page, SectionPage)
                    page.is_section = page.is_page = True
                    page.title = section.title
                    page.parent = section.parent
                    section.children.pop(0)
                    page.children = section.children
                    for child in page.children:
                        child.parent = page
                    items[i] = page
        self._nav = nav
        return nav

    def on_env(self, env: Environment, config, files) -> Environment:
        """Apply plugin-specific transformations to the Jinja environment."""
        assert env.loader is not None
        env.loader = self._loader = rewrite.TemplateRewritingLoader(env.loader)
        return env

    def on_page_context(self, context, page, config, nav):
        """Apply plugin-specific transformations to a page's context."""
        if nav != self._nav:
            self._nav = nav

    def on_page_content(
        self,
        html: str,
        page: Page,
        config: MkDocsConfig,
        files: Files,
    ) -> str:
        """Apply plugin-specific transformations to a page's content."""
        if self.config.autoapi_generate_api_docs:
            repo_url = config.repo_url
            edit_uri = config.edit_uri

            src_path = page.file.src_uri
            if src_path in self._edit_paths:
                path = self._edit_paths.pop(src_path)
                if repo_url and edit_uri:
                    if not edit_uri.startswith(
                        "?", "#"
                    ) and not repo_url.endswith("/"):
                        repo_url += "/"

                    page.edit_url = path and urllib.parse.urljoin(
                        base=urllib.parse.urljoin(base=repo_url, url=edit_uri),
                        url=path,
                    )

        return html
