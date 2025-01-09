"""Combination"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_COMBINATION = python_net_import("SMT.MastaAPI.Utility.KeyBindings", "Combination")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Combination")
    CastSelf = TypeVar("CastSelf", bound="Combination._Cast_Combination")


__docformat__ = "restructuredtext en"
__all__ = ("Combination",)


class Combination(Enum):
    """Combination

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _COMBINATION

    AND = 0
    ANDOR = 1
    OR = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


Combination.__setattr__ = __enum_setattr
Combination.__delattr__ = __enum_delattr
