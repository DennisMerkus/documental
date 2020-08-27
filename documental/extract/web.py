import logging
from typing import Optional

from bs4 import BeautifulSoup, NavigableString, Tag

from documental.document import Article, Document, ParentDocument, RootDocument, Section
from documental.html import (
    Blockquote,
    Breakline,
    Container,
    Heading,
    Image,
    Images,
    Paragraph,
)
from documental.text import Text

from .html import (
    extract_figure,
    extract_heading,
    extract_link,
    extract_list,
    extract_styled_elements,
    extract_text,
)


class WebExtractor(object):
    def __init__(self):
        self.url = None

    def extract_document(self, html: str, title: str, url: str) -> RootDocument:
        logging.debug("Extracting Document from HTML")

        soup = BeautifulSoup(html, "lxml")

        self.url = url

        document = Article()
        document.add_child(Heading().add_child(Text(title)))
        self.extract_children(soup, document)

        return document

    def extract_children(
        self, soup: BeautifulSoup, parent: ParentDocument
    ) -> ParentDocument:
        for child in soup.children:
            extracted_child = self.extract_document_soup(child)

            if extracted_child is not None:
                parent.add_child(extracted_child)

        return parent

    # TODO: Extract twitter quotes
    def extract_document_soup(self, soup: BeautifulSoup) -> Optional[Document]:
        if type(soup) is NavigableString:
            return extract_text(soup)
        elif type(soup) is Tag:
            # TODO: time
            # TODO: ul>li
            # TODO: em (semantic emphasis)
            # TODO: <table>
            if soup.name in [
                "html",
                "body",
                "div",
            ]:  # Beautifulsoup adds <html> and <body> when creating the DOM
                return self.extract_children(soup, Container())
            # Skip these for now, do something more sensible later if applicable
            # TODO: Do something more sensible with <strong> (semantic emphasis)
            elif soup.name in ["span", "strong", "time"]:
                return self.extract_children(soup, Container())
            elif soup.name == "article":
                return self.extract_children(soup, Container())
            elif soup.name == "header":
                return self.extract_children(soup, Container())
            elif soup.name == "section":
                return self.extract_children(soup, Section())
            elif soup.name == "main":
                return self.extract_children(soup, Container())
            elif soup.name == "footer":
                return self.extract_children(soup, Container())
            elif soup.name == "p":
                paragraph = self.extract_children(soup, Paragraph())

                if len(paragraph.children) == 0:
                    logging.debug("[Extract] Paragraph was empty")
                    return None
                else:
                    return paragraph
            elif soup.name == "blockquote":
                return self.extract_children(soup, Blockquote())
            elif soup.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                return extract_heading(soup)
            elif soup.name in ["b", "i", "del", "ins", "em", "u", "small"]:
                return self.extract_children(soup, extract_styled_elements(soup))
            elif soup.name == "a":
                return extract_link(soup, self.url)
            # TODO: Extract labels and/or alt-text
            elif soup.name == "img":
                if "src" in soup.attrs:
                    return Images(Image(source=soup.attrs["src"]))
                else:
                    logging.warning("[Extract] Image did not have source\n%s" % (soup))
                    return None
            elif soup.name == "figure":
                return extract_figure(soup)
            elif soup.name == "figcaption":
                return self.extract_children(soup, Container())
            elif soup.name == "br":
                return Breakline()
            elif soup.name == "nav":
                # Ignore navs for now
                logging.debug("[Extract] Ignoring nav\n%s" % (soup))
                return None
            elif soup.name == "ul":
                return extract_list(soup)
            elif soup.name in ["dl", "ol"]:
                # Can be a list, but can also be a nav or other styled thing
                logging.debug("[Extract] Ignoring list\n%s" % (soup))
                return None
            else:
                logging.warning("Unhandled element type %s\n%s" % (soup.name, soup))
                return None
        else:
            raise ValueError("Unhandled child type %s" % (type(soup)))
