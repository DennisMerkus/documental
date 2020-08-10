# Documental

Unified interface for handling different structured document types.

Documental includes support for parsing HTML pages, EPUB ebooks, and subtitles (WIP).

## Usage

To create a document

```python
from omnilingual import LanguageCode

from documental import Article
from documental.html import Paragraph
from documental.text import Text

article = Article().add_child(
    Paragraph().add_child(Text("Hello, World!", LanguageCode.English))
)
```
