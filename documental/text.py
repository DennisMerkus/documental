from __future__ import annotations

from typing import Any, Dict
from omnilingual import LanguageCode

from .document import Document


class Text(Document):
    def __init__(self, text: str, language: LanguageCode = LanguageCode.Undetermined):
        super().__init__()

        self.type = "Text"
        self.text: str = text

        self.language: LanguageCode = language

    def __eq__(self, other) -> bool:
        if not isinstance(other, Text):
            return False

        return self.text == other.text and self.language == other.language

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Text:
        return Text(text=data["text"], language=data["language"])

    def as_dict(self):
        data = super().as_dict()

        data["text"] = self.text

        data["language"] = self.language.value

        return data
