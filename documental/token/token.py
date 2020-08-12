import uuid

from typing import Any, Dict


class Token(object):
    def __init__(self, token_type="Token"):
        self.id: str = str(uuid.uuid1())
        self.type: str = token_type

    def __iter__(self):
        yield self

    def as_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "type": self.type}

    def as_token_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "type": self.type}
