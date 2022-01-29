from __future__ import annotations

from typing import (
    Pattern,
    Callable,
    Iterable,
    Union,
)

from bs4.element import (
    Tag,
    NavigableString,
)


_SimpleStrainable = Union[
    str, bool, None, bytes, Pattern[str], Callable[[str], bool], Callable[[Tag], bool]
]
_Strainable = Union[_SimpleStrainable, Iterable[_SimpleStrainable]]


def assert_find(
    obj: Tag,
    name: _Strainable | None = None,
    attrs: dict[str, _Strainable] | _Strainable | None = None,
    recursive: bool = True,
    text: _Strainable | None = None,
    **kwargs: _Strainable,
) -> Tag | NavigableString:
    """As a `Tag(...).find`, but if there is no search result, it causes an error."""
    if attrs is None:
        attrs = {}

    result = obj.find(name, attrs, recursive, text, **kwargs)
    if result is None:
        raise BeautifulSoupParserError(
            f"Page element with name: {name!r}, attrs: {attrs!r} not found"
        )
    return result


class BeautifulSoupParserError(Exception):
    """Error if parsed data is not valid."""
