import os
import urllib.parse
from typing import Dict, List
from zipfile import ZipFile

from bs4 import BeautifulSoup, NavigableString, Tag
from omnilingual import LanguageCode
from omnilingual.language import Language

from documental import Text
from documental.book import Book, Chapter, ParentDocument
from documental.html import Heading, HorizontalRule, Paragraph


class EpubReader(object):
    # Based on https://github.com/rupa/epub/blob/master/epub.py
    def __init__(self):
        self.CONTAINER_PATH = "META-INF/container.xml"

        self.base_directory = ""

        self.title = ""
        self.author = ""

        self.language: LanguageCode = LanguageCode.Undetermined

        self.items: Dict[str, str] = {}

        self.sections: List[BeautifulSoup] = []

    def load_epub(self, file_name: str) -> Book:
        with ZipFile(file_name, "r") as epub_file:
            opf = self.find_opf(epub_file)

            self.extract_metadata(opf)

            self.extract_items(opf, epub_file)

        return self.create_document()

    def find_opf(self, epub: ZipFile) -> BeautifulSoup:
        with epub.open(self.CONTAINER_PATH) as container_file:
            soup = BeautifulSoup(container_file.read(), "lxml")

            self.opf_path = soup.find("rootfile").attrs["full-path"]

            self.base_directory = os.path.dirname(urllib.parse.unquote(self.opf_path))

        with epub.open(self.opf_path) as opf_file:
            return BeautifulSoup(opf_file.read(), "lxml")

    def extract_metadata(self, opf: BeautifulSoup) -> None:
        self.title = opf.find("dc:title").text
        self.author = opf.find("dc:creator").text

        language_code = opf.find("dc:language").text

        if language_code is not None:
            language = Language.where(tag=language_code)

            self.language = language.code

    def extract_items(self, opf: BeautifulSoup, epub: ZipFile) -> None:
        manifest: Dict[str, str] = {}
        spine: List[str] = []

        for item in opf.find("manifest").find_all("item"):
            manifest[item["id"]] = urllib.parse.unquote(item["href"])

        for item in opf.find("spine").find_all("itemref"):
            spine.append(item["idref"])

        for item_id in spine:
            with epub.open(
                os.path.join(self.base_directory, manifest[item_id])
            ) as section_file:
                section = BeautifulSoup(section_file.read(), "lxml").find("body")

                self.sections.append(section)

    def create_document(self) -> Book:
        book = Book()

        current_section: ParentDocument = book

        for section in self.sections:
            chapter = Chapter()

            book.add_child(chapter)

            current_section = chapter

            for tag in section.contents:
                if isinstance(tag, NavigableString):
                    text = tag.string.strip()

                    if len(text) > 0:
                        current_section.add_child(Text(tag, self.language))
                elif isinstance(tag, Tag):
                    if tag.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                        level = int(tag.name[-1])

                        current_section.add_child(
                            Heading(level).add_child(Text(tag.text, self.language))
                        )
                    elif tag.name == "p":
                        current_section.add_child(
                            Paragraph().add_child(Text(tag.text, self.language))
                        )
                    elif tag.name in ["div", "svg"]:
                        pass
                    elif tag.name == "hr":
                        current_section.add_child(HorizontalRule())
                    else:
                        raise NotImplementedError(
                            "Unhandled book tag %s %s" % (tag.name, tag)
                        )

        return book
