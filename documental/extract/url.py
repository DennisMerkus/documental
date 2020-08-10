from urllib.parse import urljoin, urlparse


def is_url(text: str) -> bool:
    result = urlparse(text)

    return all([result.netloc != "", result.path != ""])


def absolute_url(url: str, relative: str) -> str:
    return urljoin(url, relative)
