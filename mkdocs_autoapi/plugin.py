"""Plugin definition for mkdocs-autoapi."""

# built-in imports
import collections
from pathlib import Path
import tempfile
import urllib.parse
from typing import Literal

# third-party imports
from jinja2 import Environment
from mkdocs.config import Config
from mkdocs.config import config_options
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation, Section
from mkdocs.structure.pages import Page

# local imports
from mkdocs_autoapi.autoapi import create_docs
from mkdocs_autoapi.generate_files.editor import FilesEditor
from mkdocs_autoapi.literate_nav import resolve
from mkdocs_autoapi.section_index import rewrite
from mkdocs_autoapi.section_index.section_page import SectionPage


class AutoApiPluginConfig(Config):
    """Configuration options for plugin."""

    project_root = config_options.Dir(exists=True, default=".")
    exclude = config_options.ListOfItems(config_options.Type(str), default=[])


class AutoApiPlugin(BasePlugin[AutoApiPluginConfig]):
    """Plugin logic definition."""

    def on_startup(self, *, command: Literal['build', 'gh-deploy', 'serve'], dirty: bool) -> None:
        """Add command to the configuration."""
        self.config.update({"command": command})


    def on_files(self, files: Files, config: MkDocsConfig) -> Files:
        """Generate autoAPI documentation files.

        Steps:
            1.  Create a temporary directory to store the generated files.
            2.  Exclude the virtual environment from the documentation if it is
                not already excluded.
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
        if "**/venv/**/*.py" not in self.config.exclude:
            self.config.exclude.append("**/venv/**/*.py")
        if "**/.venv/**/*.py" not in self.config.exclude:
            self.config.exclude.append("**/.venv/**/*.py")

        # Step 4
        with FilesEditor(
            files=files,
            config=config,
            directory=self._dir.name,
        ) as editor:
            try:
                create_docs(
                    config=config,
                )
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
                    # The page becomes a section-page.
                    page.__class__ = SectionPage
                    assert isinstance(page, SectionPage)
                    page.is_section = page.is_page = True
                    page.title = section.title
                    page.parent = section.parent
                    # The page leaves the section but takes over children that used to be its peers.
                    section.children.pop(0)
                    page.children = section.children
                    for child in page.children:
                        child.parent = page
                    # The page replaces the section; the section will be garbage-collected.
                    items[i] = page
        self._nav = nav
        return nav

    def on_env(self, env: Environment, config, files) -> Environment:
        assert env.loader is not None
        env.loader = self._loader = rewrite.TemplateRewritingLoader(env.loader)
        return env

    def on_page_context(self, context, page, config, nav):
        if nav != self._nav:
            self._nav = nav

    def on_page_content(
        self,
        html: str,
        page: Page,
        config: MkDocsConfig,
        files: Files,
    ) -> str:
        repo_url = config.repo_url
        edit_uri = config.edit_uri

        src_path = page.file.src_uri
        if src_path in self._edit_paths:
            path = self._edit_paths.pop(src_path)
            if repo_url and edit_uri:
                if not edit_uri.startswith("?", "#") and not repo_url.endswith("/"):
                    repo_url += "/"

                page.edit_url = path and urllib.parse.urljoin(
                    base=urllib.parse.urljoin(base=repo_url, url=edit_uri),
                    url=path,
                )

        return html
