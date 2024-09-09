"""Section page definition."""

# built-in imports

# third-party imports
from mkdocs.structure.nav import Section
from mkdocs.structure.pages import Page


class SectionPage(Section, Page):
    """A page that is also a section."""

    def __init__(self, title: str, file, config, children):
        """Initialize a SectionPage instance."""
        Page.__init__(self, title=title, file=file, config=config)
        Section.__init__(self, title=title, children=children)
        self.is_section = self.is_page = True

    active = Page.active  # type: ignore[assignment]

    def __repr__(self):
        """Return a string representation of the SectionPage instance."""
        result = Page.__repr__(self)
        if not result.startswith("Section"):
            result = "Section" + result
        return result

    def __eq__(self, other):
        """Check whether SectionPage instance is equal to another object."""
        return object.__eq__(self, other)

    def __ne__(self, other):
        """Check whether SectionPage instance is not equal to another object."""
        return not (self == other)

    def __hash__(self):
        """Get the hash of the SectionPage instance."""
        return object.__hash__(self)
