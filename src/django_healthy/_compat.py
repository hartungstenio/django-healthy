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
    from enum import StrEnum
    from typing import NotRequired, Self, TypedDict
else:
    from enum import Enum
    from typing import no_type_check

    from typing_extensions import NotRequired, Self, TypedDict

    class StrEnum(str, Enum):
        @no_type_check
        @staticmethod
        def _generate_next_value_(name, start, count, last_values):  # noqa: ARG004
            return name.lower()


__all__ = [
    "Mapping",
    "MutableMapping",
    "NotRequired",
    "Self",
    "StrEnum",
    "TypeAlias",
    "TypedDict",
]
