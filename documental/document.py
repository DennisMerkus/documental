from __future__ import annotations

import uuid
from itertools import chain
from typing import Any, Dict, List

from omnilingual import LanguageCode


class Document(object):
    """
    JSON-friendly document format for use with NLP tools while maintaining
    document structure.

    Features:
    - Hierarchical document structure (Chapters, Paragraphs, Sentences)
    - Tokens
    - Overlapping Spans and Phrases to group tokens together and annotate them
    """

    def __init__(self):
        # A unique id to use for identification in the document tree
        self.id: str = str(uuid.uuid1())

        self.should_combine_similar = False

        self.type: str = "Document"

        self.language: LanguageCode = LanguageCode.Undetermined

    def as_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
        }

    def __iter__(self):
        yield self


class ParentDocument(Document):
    def __init__(self):
        super().__init__()

        self.children: List[Document] = []

    def __eq__(self, other):
        if not isinstance(other, ParentDocument):
            return False

        if len(self.children) != len(other.children):
            return False

        if self.type != other.type:
            return False

        for index in range(len(self.children)):
            if self.children[index] != other.children[index]:
                return False

        return True

    def __iter__(self):
        yield self

        for child in chain(*map(iter, self.children)):
            yield child

    def __str__(self):
        return "<%s [%s]>" % (self.type, [str(child) for child in self.children],)

    def word_count(self) -> int:
        return sum([child.word_count() for child in self.children])

    def all_lexemes(self) -> Dict[str, Dict[Any, Any]]:
        lexemes: Dict[str, Dict[Any, Any]] = {}

        for child in self.children:
            lexemes.update(child.all_lexemes())

        return lexemes

    def all_words(self) -> Dict[str, Dict[str, Any]]:
        tokens: Dict[str, Dict[str, Any]] = {}

        for child in self.children:
            tokens.update(child.all_words())

        return tokens

    def add_child(self, element: Document) -> ParentDocument:
        if isinstance(element, Container):
            for child in element.children:
                self.add_child(child)

            return self
        elif isinstance(element, Document):
            if self.can_combine_with_last_child(element):
                self.combine_children_with_last(element)
            else:
                self.children.append(element)

            return self
        else:
            raise TypeError("Expected a Document, not %s" % (type(element)))

    def replace_child(self, index: int, element) -> None:
        if index < len(self.children):
            self.children[index] = element

    def replace_range(self, index: int, elements: List[Document]) -> None:
        if index < len(self.children):
            self.children[index:index] = elements

    def can_combine_with_last_child(self, document):
        if len(self.children) == 0:
            return False
        else:
            children_types_match = self.children[-1].type == document.type

            return children_types_match and document.should_combine_similar

    def combine_children_with_last(self, document):
        for element in document.children:
            self.children[-1].add_child(element)

    def as_dict(self) -> Dict[str, Any]:
        data = super().as_dict()

        data["children"] = [child.as_dict() for child in self.children]

        return data


class RootDocument(ParentDocument):
    def __init__(self):
        super().__init__()

    def __eq__(self, other):
        if not isinstance(other, RootDocument):
            return False

        return super().__eq__(other)

    def __str__(self):
        return super().__str__()

    def as_dict(self):
        data = super().as_dict()

        data["words"] = self.all_words()
        data["lexemes"] = self.all_lexemes()

        return data


class Container(ParentDocument):
    """
    Special type whose children simply get added to the parent document's
    children.
    """

    def __init__(self):
        super().__init__()

        self.type = "Container"


class Article(RootDocument):
    def __init__(self):
        super().__init__()

        self.type = "Article"

    def __str__(self):
        return super().__str__()


class Section(ParentDocument):
    def __init__(self):
        super().__init__()

        self.type = "Section"

    def __str__(self):
        return super().__str__()
