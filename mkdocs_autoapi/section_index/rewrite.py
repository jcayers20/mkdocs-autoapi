"""Logic for rewriting the navigation data."""

# built-in imports
import pathlib
import textwrap
from typing import Callable, Optional, Tuple, Union

from jinja2 import BaseLoader, Environment

__all__ = ["TemplateRewritingLoader"]


class TemplateRewritingLoader(BaseLoader):
    """A Jinja2 template loader that rewrites certain templates."""

    def __init__(self, loader: BaseLoader):
        """Initialize a TemplateRewritingLoader instance."""
        self.loader = loader
        self.found_supported_theme = False

    def get_source(
        self,
        environment: Environment,
        template: str,
    ) -> Tuple[str, str, Union[Callable[[], bool], None]]:
        """Get the source of a template."""
        src, filename, uptodate = self.loader.get_source(environment, template)
        old_src = src
        assert filename is not None
        path = pathlib.Path(filename).as_posix()

        if path.endswith("/mkdocs/templates/sitemap.xml"):
            src = _transform_mkdocs_sitemap_template(src)
        else:
            # the second path is used in MkDocs-Material >= 9.4
            if path.endswith(
                (
                    "/material/partials/nav-item.html",
                    "/material/templates/partials/nav-item.html",
                ),
            ):
                src = _transform_material_nav_item_template(src)
            elif path.endswith(
                (
                    "/material/partials/tabs-item.html",
                    "/material/templates/partials/tabs-item.html",
                ),
            ):
                src = _transform_material_tabs_item_template(src)
            elif path.endswith("/themes/readthedocs/base.html"):
                src = _transform_readthedocs_base_template(src)
            elif path.endswith("/nature/base.html"):
                src = None  # Just works!
            else:
                return src, filename, uptodate
            self.found_supported_theme = True

        return src or old_src, filename, uptodate


def _transform_mkdocs_sitemap_template(src: str) -> Union[str, None]:
    """Transform the sitemap template."""
    if " in pages " in src:
        return None
    # The below only for versions <= 1.1.2.
    return src.replace(
        "{%- else %}",
        "{%- endif %}{% if item.url %}",
    )


def _transform_material_nav_item_template(src: str) -> str:
    """Transform the Material for MkDocs nav-item template."""
    if "navigation.indexes" in src:
        return src.replace(
            "{% set indexes = [] %}",
            "{% set indexes = [nav_item] if nav_item.url else [] %}",
        ).replace(
            "{% if nav_item.children | length > 1 %}",
            "{% if nav_item.children %}",
        )

    # The above only for versions >= 7.3, the below only for versions < 7.3.
    src = src.replace(
        "{% if nav_item.children %}",
        "{% if nav_item.children and not ('navigation.tabs' in features and level == 1 and not nav_item.active and nav_item.url) %}",  # noqa: E501
    )

    repl = """\
        {% if nav_item.url %}
          <a href="{{ nav_item.url | url }}" class="md-nav__link{% if nav_item == page %} md-nav__link--active{% endif %}"
            style="margin: initial; padding: initial; pointer-events: initial">
        {% endif %}
          [...]
        {% if nav_item.url %}</a>{% endif %}
    """  # noqa: E501
    lines = src.split("\n")
    for i, (line1, line2) in enumerate(zip(lines, lines[1:])):
        for a, b in (line1, line2), (line2, line1):
            if "md-nav__icon" in a and b.endswith("{{ nav_item.title }}"):
                lines[i : i + 2] = (a, _replace_line(b, repl))
                break
    return "\n".join(lines)


def _transform_material_tabs_item_template(src: str) -> str:
    """Transform the Material for MkDocs tabs-item template."""
    src = src.replace(
        "{% if first.children %}", "{% if first.children and not first.url %}"
    )
    # The above only for versions >= 9.2
    src = src.replace(
        "{% if nav_item.children %}",
        "{% if nav_item.children and not nav_item.url %}",
    )
    # The above only for versions > 6.1.7, the below only for versions <= 6.1.7.
    return src.replace(
        "(nav_item.children | first).url",
        "(nav_item.url or (nav_item.children | first).url)",
    ).replace(
        "if (nav_item.children | first).children",
        "if (nav_item.children | first).children and not nav_item.url",
    )


def _transform_readthedocs_base_template(src: str) -> Union[str, None]:
    """Transform the ReadTheDocs base template."""
    if " if nav_item.is_page " in src:
        return None
    # The below only for versions < 1.6:
    repl = """\
        {% if nav_item.url %}
            <ul><li{% if nav_item == page %} class="current"{% endif %}>
                <a href="{{ nav_item.url|url }}" style="padding: 0; font-size: inherit; line-height: inherit">
        {% endif %}
                [...]
        {% if nav_item.url %}
                </a>
            </li></ul>
        {% endif %}
    """  # noqa: E501
    lines = src.split("\n")
    for i, line in enumerate(lines):
        if "{{ nav_item.title }}" in line:
            lines[i] = _replace_line(lines[i], repl)
    return "\n".join(lines)


def _replace_line(
    line: str,
    wrapper: str,
    new_line: Optional[str] = None,
) -> str:
    """Replace a line with a wrapper."""
    leading_space = line[: -len(line.lstrip())]
    if new_line is None:
        new_line = line.lstrip()
    new_text = textwrap.dedent(wrapper.rstrip()).replace("[...]", new_line)
    return textwrap.indent(new_text, leading_space)
