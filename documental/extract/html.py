import logging
from typing import Dict, Optional

from bs4 import BeautifulSoup, NavigableString

from documental import Document
from documental.html import (
    BareLink,
    Figure,
    Heading,
    Image,
    Images,
    Link,
    UnorderedList,
    Style,
    StyledText,
)
from documental.text import Text

from .url import absolute_url, is_url


def extract_figure(soup: BeautifulSoup) -> Optional[Document]:
    img = soup.find("img")

    if img:
        image = Image(img.attrs["src"])

        figcaption = soup.find("figcaption")

        if figcaption:
            return Figure(image, figcaption.get_text())
        else:
            return Figure(image)
    else:
        logging.warning("Could not find an <img> in <figure>")

        return None


def extract_link(soup: BeautifulSoup, page_url: str) -> Optional[Document]:
    if "href" not in soup.attrs or not soup.attrs["href"]:
        logging.warning("[Extract] <a> does not have href\n%s" % (soup))

        return None

    href = soup.attrs["href"].strip()

    if href.startswith("/"):
        href = absolute_url(page_url, href)

    # Extract an Image if that's the only thing the <a> contains
    if len(soup.contents) == 1 and soup.contents[0].name == "img":
        image = soup.contents[0]

        return Images(Image(source=image.attrs["src"], url=soup.attrs["href"]))
    else:
        text = soup.get_text().strip()

        # If the URL is shown verbatim, add it as such
        if text == soup.attrs["href"] or is_url(text) or len(text) == 0:
            return BareLink(href)
        else:
            return Link(href).add_child(Text(soup.get_text()))


def extract_list(soup: BeautifulSoup) -> UnorderedList:
    document = UnorderedList()

    for li in soup.find_all("li"):
        document.add_child(Text(li.get_text()))

    return document


def extract_heading(soup: BeautifulSoup) -> Heading:
    heading = Heading(level=int(soup.name[1]))

    heading.add_child(Text(soup.get_text()))

    return heading


styles: Dict[str, Style] = {
    "b": Style.Bold,
    "i": Style.Italics,
    "del": Style.Strikethrough,
    "ins": Style.Underlined,
    "em": Style.Emphasis,
    "u": Style.Misspelled,
    "small": Style.Small,
}


def extract_styled_elements(soup: BeautifulSoup) -> StyledText:
    return StyledText(styles[soup.name])


def extract_text(soup: NavigableString) -> Text:
    return Text(soup.string.strip())
