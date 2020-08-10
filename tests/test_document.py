import unittest

from omnilingual import LanguageCode

from documental.document import Article
from documental.html import Paragraph
from documental.text import Text


class TestDocument(unittest.TestCase):
    def test_can_create_a_simple_document(self):
        Article().add_child(
            Paragraph().add_child(Text("Hello, World!", LanguageCode.English))
        )
