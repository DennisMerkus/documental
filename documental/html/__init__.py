from __future__ import annotations

from enum import Enum, unique
from typing import Any, Dict, Optional

from ..document import Container, Document, ParentDocument
from ..text import Text


@unique
class Style(Enum):
    Bold = "Bold"
    Italics = "Italics"
    Strikethrough = "Strikethrough"
    Underlined = "Underlined"
    Emphasis = "Emphasis"
    Misspelled = "Misspelled"
    Small = "Small"


class StyledText(ParentDocument):
    def __init__(self, style: Style):
        super().__init__()

        self.type = "Styled"

        self.style: Style = style

    def __eq__(self, other):
        if not isinstance(other, StyledText):
            return False

        return self.style == other.style

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> StyledText:
        return StyledText(style=data["style"])

    def as_dict(self) -> Dict[str, Any]:
        data = super().as_dict()

        data["style"] = self.style.value

        return data


class Paragraph(ParentDocument):
    def __init__(self):
        super().__init__()

        self.type = "Paragraph"


class Blockquote(ParentDocument):
    def __init__(self):
        super().__init__()

        self.type = "Blockquote"


class Heading(ParentDocument):
    def __init__(self, level=1):
        super().__init__()

        self.type = "Heading"
        self.level: int = level

    def __str__(self):
        return "<Heading %s>" % ("*" * self.level)

    def as_dict(self) -> Dict[str, Any]:
        data = super().as_dict()

        data["level"] = self.level

        return data


class Link(ParentDocument):
    def __init__(self, url: str):
        super().__init__()

        self.type = "Link"
        self.url: str = url

    def __eq__(self, other):
        if not isinstance(other, Link):
            return False

        return self.url == other.url

    def as_dict(self):
        data = super().as_dict()

        data["url"] = self.url

        return data


class BareLink(Document):
    def __init__(self, url: str):
        super().__init__()

        self.type = "BareLink"

        self.url: str = url

    def __eq__(self, other):
        if not isinstance(other, BareLink):
            return False

        return self.url == other.url

    def as_dict(self):
        data = super().as_dict()

        data["url"] = self.url

        return data


class Image(Document):
    def __init__(self, source: str, url: Optional[str] = None):
        super().__init__()

        self.type = "Image"

        self.source: str = source
        self.url: Optional[str] = url

    def __str__(self):
        return "<Image %s>" % (self.source)

    def as_dict(self):
        data = super().as_dict()

        data["source"] = self.source

        if self.url is not None:
            data["url"] = self.url

        return data


class Images(ParentDocument):
    def __init__(self, image: Optional[Image] = None):
        super().__init__()

        self.type = "Images"
        self.should_combine_similar = True

        if image is not None:
            self.add_child(image)


class UnorderedList(ParentDocument):
    def __init__(self):
        super().__init__()

        self.type = "UnorderedList"


class Figure(Container):
    def __init__(self, image: Image, caption: Optional[str] = None):
        super().__init__()

        self.add_child(Images(image))

        if caption is not None:
            self.add_child(Text(caption))

    def __eq__(self, other):
        if isinstance(other, Figure):
            if len(self.children) != len(other.children):
                return False

            for index in range(len(self.children)):
                if self.children[index] != other.children[index]:
                    return False

            return True

        return False

    def __str__(self):
        return "<Figure [%s]>" % (",".join([str(child) for child in self.children]))


class HorizontalRule(Document):
    def __init__(self):
        super().__init__()

        self.type = "HorizontalRule"


class Breakline(Document):
    def __init__(self):
        super().__init__()

        self.type = "Breakline"
