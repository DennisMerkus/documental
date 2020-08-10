import unittest

from documental.document import Article
from documental.html import BareLink, Heading, Style, StyledText
from documental.text import Text
from documental.extract.web import WebExtractor


class TestWebExtractor(unittest.TestCase):
    def test_extracts_bare_link(self):
        title = "中国はマルウェアによるウイグル族の監視活動を数年にわたって行っていたと判明"
        url = "https://gigazine.net/news/20200702-china-uighur-surveillance-malware/"
        excerpt = """
            <b>lookout-uyghur-malware-tr-us.pdf</b>
            <br>
            <b>(PDFファイル)<a href="https://www.lookout.com/documents/threat-reports/us/lookout-uyghur-malware-tr-us.pdf" target="_blank">https://www.lookout.com/documents/threat-reports/us/lookout-uyghur-malware-tr-us.pdf<br>
            </a></b>
        """

        extractor = WebExtractor()

        document = extractor.extract_document(excerpt, title, url)

        expected = (
            Article()
            .add_child(Heading().add_child(Text(title)))
            .add_child(
                StyledText(Style.Bold).add_child(
                    Text("lookout-uyghur-malware-tr-us.pdf")
                )
            )
            .add_child(
                StyledText(Style.Bold)
                .add_child(Text("(PDFファイル)"))
                .add_child(
                    BareLink(
                        "https://www.lookout.com/documents/threat-reports/us/lookout-uyghur-malware-tr-us.pdf"
                    )
                )
            )
        )

        self.assertEqual(document, expected)
