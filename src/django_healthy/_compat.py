import sys

if sys.version_info >= (3, 9):
    from collections.abc import Mapping, MutableMapping
else:
    from typing import Mapping, MutableMapping

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

if sys.version_info >= (3, 11):
    from typing import NotRequired, Self, TypedDict
else:
    from typing_extensions import NotRequired, Self, TypedDict


__all__ = [
    "Mapping",
    "MutableMapping",
    "NotRequired",
    "Self",
    "TypeAlias",
    "TypedDict",
]
