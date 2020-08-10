import unittest

from omnilingual import LanguageCode

from documental.extract.lyrics import LyricsExtractor

from .letras import quero


class TestLyricsExtractor(unittest.TestCase):
    def test_extracts_quero_succesfully(self):
        extractor = LyricsExtractor()

        extractor.extract_lyrics(quero, LanguageCode.Portuguese)
