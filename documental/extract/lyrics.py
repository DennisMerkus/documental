import re

from bs4 import BeautifulSoup

from omnilingual import LanguageCode

from documental.document import Section
from documental.lyrics import Line, Lyrics
from documental.text import Text


class LyricsExtractor(object):
    # por: https://www.letras.mus.br/
    def __init__(self):
        pass

    def extract_lyrics(
        self, html: str, language: LanguageCode = LanguageCode.Undetermined
    ) -> Lyrics:
        lyrics = Lyrics()

        soup = BeautifulSoup(html, "lxml")

        for p in soup.find("article").find_all("p"):
            lines = re.split(r"<br(\w+/)?>", p.text)

            section = Section()

            for line in lines:
                section.add_child(Line().add_child(Text(line, language)))

            lyrics.add_child(section)

        return lyrics
