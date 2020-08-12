import unittest

from documental.token.word import RubyCharacter, RubyToken

from omnilingual import LanguageCode, PartOfSpeech


class TestRuby(unittest.TestCase):
    def test_generates_correct_dict(self):
        word = RubyToken(
            [RubyCharacter(base="二", text="に")],
            LanguageCode.Japanese,
            "二",
            PartOfSpeech.Number,
        )

        word_dict = word.as_dict()

        self.assertEqual(word_dict["type"], "Ruby")
        self.assertEqual(word_dict["language"], LanguageCode.Japanese.value)
        self.assertEqual(word_dict["lemma"], "二")
        self.assertEqual(word_dict["pos"], PartOfSpeech.Number.value)
        self.assertListEqual(word_dict["characters"], [{"base": "二", "text": "に"}])

