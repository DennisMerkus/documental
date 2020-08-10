import unittest

from bs4 import BeautifulSoup
from omnilingual import LanguageCode

from documental.extract.epub import EpubReader

from .alice_opf import opf


class TestEpubReader(unittest.TestCase):
    def test_extracts_metadata(self):
        reader = EpubReader()

        reader.extract_metadata(BeautifulSoup(opf, "lxml"))

        self.assertEqual(reader.title, "Alice's Adventures in Wonderland")
        self.assertEqual(reader.author, "Lewis Carroll")
        self.assertEqual(reader.language, LanguageCode.English)

    def test_loads_Alice_in_Wonderland_epub(self):
        reader = EpubReader()

        reader.load_epub("./tests/extract/epub/alice.epub")

        reader.create_document()
