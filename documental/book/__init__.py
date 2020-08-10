from ..document import RootDocument, ParentDocument


class Book(RootDocument):
    def __init__(self):
        super().__init__()

        self.type = "Book"

    def __str__(self):
        return super().__str__()


class Chapter(ParentDocument):
    def __init__(self):
        super().__init__()

        self.type = "Chapter"

    def __str__(self):
        return super().__str__()
