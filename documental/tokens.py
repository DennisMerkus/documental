from __future__ import annotations

from typing import Any, List, Dict

from .document import Document
from .token import Token, WordToken


class Tokens(Document):
    def __init__(self, text: str):
        super().__init__()

        self.type = "Tokens"

        self.text: str = text.strip()
        self.tokens: List[Token] = []

    def __eq__(self, other):
        if not isinstance(other, Tokens):
            return False

        return self.text == other.text

    def word_count(self) -> int:
        return sum([1 if isinstance(token, WordToken) else 0 for token in self.tokens])

    def as_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "text": self.text,
            "tokens": [token.as_token_dict() for token in self.tokens],
            "wordCount": self.word_count(),
        }
