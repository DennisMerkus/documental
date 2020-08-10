import unittest

from omnilingual import LanguageCode

from documental.text import Text


class TestText(unittest.TestCase):
    def test_equal_texts(self):
        self.assertEqual(
            Text("Hello, World!", LanguageCode.English),
            Text("Hello, World!", LanguageCode.English),
        )
        self.assertEqual(Text(""), Text(""))

    def test_inequal_texts(self):
        self.assertNotEqual(
            Text("Hallo!", LanguageCode.Dutch), Text("Hallo!", LanguageCode.German)
        )
        self.assertNotEqual(Text(""), Text("            "))

    def test_dict_conversion(self):
        text = Text("Hello, World!")

        text_id = text.id

        self.assertNotEqual(text_id, None)
        self.assertDictEqual(
            text.as_dict(),
            {"id": text_id, "type": "Text", "text": "Hello, World!", "language": "und"},
        )
