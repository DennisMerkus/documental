from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from omnilingual import LanguageCode
from omnilingual.features import NumType

from .token import Token
from .word import WordToken


class Ellision(Token):
    def __init__(self, text: str, words: List[WordToken], language: LanguageCode):
        super().__init__("Ellision")

        self.text = text
        self.words = words

        self.language = language

    def __eq__(self, other):
        if isinstance(other, Ellision):
            return (
                self.text == other.text
                and self.language == other.language
                and self.words == other.words
            )
        else:
            return False

    def __repr__(self):
        return "<Ellision %s:[%s]>" % (
            self.text,
            ", ".join([repr(word) for word in self.words]),
        )

    def as_dict(self) -> Dict[str, Any]:
        data = super().as_dict()

        data["text"] = self.text
        data["words"] = [word.as_dict() for word in self.words]
        data["language"] = self.language

        return data


class NumberToken(Token):
    def __init__(
        self,
        text: str,
        number: Union[int, float],
        pronunciation: List[Token],
        number_type: NumType = NumType.Card,
        language: LanguageCode = LanguageCode.Undetermined,
    ):
        super().__init__("Number")

        self.text: str = text.strip()
        self.number: Union[int, float] = number

        self.number_type: NumType = number_type

        self.pronunciation: List[Token] = pronunciation

    def __eq__(self, other):
        if isinstance(other, NumberToken):
            return (
                self.text == other.text
                and self.number_type == other.number_type
                and self.pronunciation == other.pronunciation
            )
        else:
            return False

    def __repr__(self):
        return "<Number %s:%d>" % (self.text, self.number)

    def as_dict(self):
        return self.as_token_dict()

    def as_token_dict(self):
        data = super().as_dict()

        data["text"] = self.text
        data["number"] = self.number

        data["number_type"] = self.number_type.value
        data["pronunciation"] = [token.as_dict() for token in self.pronunciation]

        return data


class BlockToken(Token):
    def __init__(self, text):
        super().__init__("Block")

        self.text = text

    def __eq__(self, other):
        if isinstance(other, BlockToken):
            return self.text == other.text
        else:
            return False

    def as_dict(self):
        return self.as_token_dict()

    def as_token_dict(self) -> Dict[str, Any]:
        data = super().as_dict()

        data["text"] = self.text

        return data


class SpaceToken(Token):
    def __init__(self, required: bool):
        super().__init__("Space")

        self.required: bool = required

    def __eq__(self, other):
        if isinstance(other, SpaceToken):
            return self.required == other.required
        else:
            return False

    def as_dict(self):
        return self.as_token_dict()

    def as_token_dict(self) -> Dict[str, Any]:
        data = super().as_dict()

        data["required"] = self.required

        return data


class PunctuationToken(Token):
    def __init__(
        self, text: str, sticks_left: bool = False, sticks_right: bool = False
    ):
        super().__init__("Punctuation")

        self.text = text

        self.sticks_left = sticks_left
        self.sticks_right = sticks_right

    def __repr__(self):
        return "<Punctuation %s%s%s >" % (
            "<" if self.sticks_left else "",
            self.text,
            ">" if self.sticks_right else "",
        )

    def __eq__(self, other):
        if isinstance(other, PunctuationToken):
            return self.text == other.text
        else:
            return False

    def as_dict(self):
        return self.as_token_dict()

    def as_token_dict(self) -> Dict[str, Any]:
        data = super().as_dict()

        data["punctuation"] = self.text

        return data


class LetterToken(Token):
    def __init__(self, letter: str):
        if len(letter) != 1:
            raise ValueError("Letter should be a string of length 1")

        super().__init__("Letter")

        self.letter = letter

    def __repr__(self):
        return self.letter

    def __eq__(self, other):
        if isinstance(other, LetterToken):
            return self.letter == other.letter
        else:
            return False

    def as_dict(self):
        return self.as_token_dict()

    def as_token_dict(self) -> Dict[str, Any]:
        data = super().as_dict()

        data["letter"] = self.letter

        return data
