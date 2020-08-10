from documental.document import RootDocument, ParentDocument


class Lyrics(RootDocument):
    def __init__(self):
        super().__init__()

        self.type = "Lyrics"

    def __str__(self):
        return super().__str__()


class Line(ParentDocument):
    def __init__(self):
        super().__init__()

        self.type = "Line"

    def __str__(self):
        return super().__str__()
