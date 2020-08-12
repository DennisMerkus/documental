from .token import Token

from typing import Any, Dict, List, Optional

from omnilingual import LanguageCode, PartOfSpeech
from omnilingual.features import Features

from pydantic import BaseModel


class BaseWordToken(Token):
    def __init__(
        self,
        token_type: str,
        language: LanguageCode,
        lemma: str,
        pos: PartOfSpeech = PartOfSpeech.Nil,
        tags: List[str] = [],
        features: Features = Features(),
    ):
        super().__init__(token_type)

        self.language: LanguageCode = language
        self.lemma: str = lemma
        self.pos: PartOfSpeech = pos
        self.tags: List[str] = tags
        self.features = features

        self.lexemeIds: List[str] = []
        self.pronounce: Dict[str, Any] = {}

    def __eq__(self, other):
        if isinstance(other, BaseWordToken):
            return (
                self.language == other.language
                and self.lemma == other.lemma
                and self.pos == other.pos
                and self.tags == other.tags
                and self.features == other.features
            )
        else:
            return False

    def as_dict(self) -> Dict[str, Any]:
        data = super().as_dict()

        data["language"] = self.language.value
        data["lemma"] = self.lemma
        data["lexemeIds"] = self.lexemeIds
        data["pos"] = self.pos.value
        data["tags"] = self.tags
        data["pronounce"] = self.pronounce

        data["features"] = self.features.dict()

        return data


class WordToken(BaseWordToken):
    def __init__(
        self,
        text: str,
        language: LanguageCode,
        lemma: Optional[str] = None,
        pos: PartOfSpeech = PartOfSpeech.Nil,
        tags: List[str] = [],
        features: Features = Features(),
    ):
        super().__init__(
            "Word", language, lemma if lemma is not None else text, pos, tags, features
        )

        self.text: str = text

    def __eq__(self, other):
        if isinstance(other, WordToken):
            return self.text == other.text and super().__eq__(other)
        else:
            return False

    def __repr__(self):
        return "<Word %s:%s:%s:%s:%s:%s>" % (
            self.text,
            self.language,
            self.lemma,
            str(self.pos),
            str(self.tags),
            str(self.features),
        )

    def as_dict(self) -> Dict[str, Any]:
        data = super().as_dict()

        data["text"] = self.text

        return data


class RubyCharacter(BaseModel):
    base: str
    text: str


class RubyToken(BaseWordToken):
    def __init__(
        self,
        characters: List[RubyCharacter],
        language: LanguageCode,
        lemma: str,
        pos: PartOfSpeech,
        tags: List[str] = [],
        features: Features = Features(),
    ):
        super().__init__("Ruby", language, lemma, pos, tags, features)

        self.characters: List[RubyCharacter] = characters

    def as_dict(self) -> Dict[str, Any]:
        data = super().as_dict()

        data["characters"] = [character.dict() for character in self.characters]

        return data
