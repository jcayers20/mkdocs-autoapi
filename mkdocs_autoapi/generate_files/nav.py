"""Logic used to implement Nav class.

As I work through the build, I'll update the documentation for this module.
"""

import dataclasses
import os
from typing import Iterable, Mapping, Optional, Tuple, Union


class Nav:
    """MkDocs navigation data structure."""

    _markdown_special_characters = tuple("!#()*+-[\\]_`{}")
    """The set of characters that need to be escaped in Markdown."""

    def __init__(self):
        """Initialize a Nav object."""
        self._data = dict()

    @dataclasses.dataclass
    class Item:
        """Define a navigation item."""

        level: int
        """The item's nesting level. Starts at 0."""
        title: str
        """The item's title."""
        filename: Optional[str]
        """The path the item links to. If None, item is section, not link."""

    def __setitem__(self, keys: Union[str, Tuple[str, ...]], value: str):
        """Add file link into the nav, under the sequence of titles.

        For example, writing `nav["Foo", "Bar"] = "foo/bar.md"` would mean
        creating a nav:
            `{"Foo": {"Bar": "foo/bar.md"}}`.

        Then, writing `nav["Foo", "Another"] = "test.md"` would merge with the
        existing sections where possible:
            `{"Foo": {"Bar": "foo/bar.md", "Another": "test.md"}}`.

        `keys` here can be any non-empty sequence of strings, it's just that
        Python implicitly creates a tuple from the comma-separated items in
        those square brackets.
        """
        if isinstance(keys, str):
            keys = (keys,)
        cur = self._data
        if not keys:
            raise ValueError(
                f"Navigation path must not be empty (got {keys!r})"
            )
        for key in keys:
            if not isinstance(key, str):
                message = f"Navigation path must consist of strings, but got a {type(key)}"  # noqa: E501
                raise TypeError(message)
            if not key:
                raise ValueError(
                    f"Navigation name parts must not be empty (got {keys!r})"
                )
            cur = cur.setdefault(key, {})
        cur[None] = os.fspath(value)

    def items(self) -> Iterable[Item]:
        """Allows viewing the nav as a flattened sequence."""
        return self._items(self._data, 0)

    @classmethod
    def _items(cls, data: Mapping, level: int) -> Iterable[Item]:
        for key, value in data.items():
            if key is not None:
                yield cls.Item(level=level, title=key, filename=value.get(None))
                yield from cls._items(value, level + 1)

    def build_literate_nav(self, indentation: int = 0) -> Iterable[str]:
        """Build a sequence of lines for a literate navigation file.

        Steps:
            1.  For each item in the navigation:
                1.1.    Get the title and filename of the item.
                1.2.    Escape the title if it starts with a markdown escape
                       character.
                1.3.    If the item has a filename, format it as a Markdown
                        link.
                1.4.    Yield the formatted line.

        Args:
            indentation:
                The number of spaces to indent the whole nav. Useful when the
                nav is a part of a larger file. Defaults to 0.

        Yields:
            The lines of the navigation file.

        See Also:
            [mkdocs-literate-nav](https://github.com/oprypin/mkdocs-literate-nav)
        """
        # Step 1
        for item in self.items():
            # Step 1.1
            title = item.title
            file = item.filename

            # Step 1.2
            if title.startswith(self._markdown_special_characters):
                title = f"\\{title}"

            # Step 1.3
            if item.filename is not None:
                line = f"[{title}]({file})"
            else:
                line = title

            # Step 1.4
            indent = " " * (indentation + (4 * item.level))
            yield f"{indent}* {line}\n"
