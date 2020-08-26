import unittest

from bs4 import BeautifulSoup, NavigableString

from documental.html import BareLink, Link, Heading, UnorderedList, Figure, Image
from documental.text import Text
from documental.extract.html import (
    extract_link,
    extract_heading,
    extract_list,
    extract_figure,
    extract_text,
)


class TestHtmlExtraction(unittest.TestCase):
    def test_extracts_link(self):
        link = extract_link(
            BeautifulSoup('<a href="some.domain">with text</a>', "lxml").find("a"),
            "my.domain.com",
        )

        self.assertEqual(link, Link("some.domain").add_child(Text("with text")))

    def test_extracts_bare_link(self):
        bare_link = extract_link(
            BeautifulSoup('<a href="some.domain">some.domain</a>', "lxml").find("a"),
            "my.domain.com",
        )

        self.assertEqual(bare_link, BareLink("some.domain"))

    def test_extracts_heading(self):
        heading = extract_heading(
            BeautifulSoup("<h1>A Great Title</h1>", "lxml").find("h1")
        )

        self.assertEqual(heading, Heading(level=1).add_child(Text("A Great Title")))

    def test_extracts_unordered_list(self):
        html = """
        <ul>
            <li>One</li>
            <li>Two</li>
            <li>Three</li>
        </ul>
        """

        unordered_list = extract_list(BeautifulSoup(html, "lxml").find("ul"))

        self.assertEqual(
            unordered_list,
            UnorderedList()
            .add_child(Text("One"))
            .add_child(Text("Two"))
            .add_child(Text("Three")),
        )

    def test_extracts_figure_without_caption(self):
        # TODO: Something weird with Figure's equality function
        html = """
        <figure>
            <img src="clouds.png" />
        </figure>
        """

        figure = extract_figure(BeautifulSoup(html, "lxml").find("figure"))

        expected = Figure(Image("clouds.png"))

        self.assertEqual(figure, expected)

    def test_extracts_strings(self):
        text = extract_text(NavigableString("unicorn"))

        self.assertEqual(text, Text("unicorn"))
