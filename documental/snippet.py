from .document import RootDocument


class Snippet(RootDocument):
    def __init__(self):
        super().__init__()

        self.type = "Snippet"

    def __str__(self):
        return super().__str__()
