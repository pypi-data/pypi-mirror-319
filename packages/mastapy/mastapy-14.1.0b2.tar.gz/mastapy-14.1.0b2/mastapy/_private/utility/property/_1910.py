"""ListWithSelectedItemAndImage"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from PIL.Image import Image

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.scripting import _7729
from mastapy._private.utility.property import _7743

_LIST_WITH_SELECTED_ITEM_AND_IMAGE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "ListWithSelectedItemAndImage"
)

if TYPE_CHECKING:
    from typing import Any, Type

    Self = TypeVar("Self", bound="ListWithSelectedItemAndImage")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ListWithSelectedItemAndImage._Cast_ListWithSelectedItemAndImage",
    )

T = TypeVar("T")

__docformat__ = "restructuredtext en"
__all__ = ("ListWithSelectedItemAndImage",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ListWithSelectedItemAndImage:
    """Special nested class for casting ListWithSelectedItemAndImage to subclasses."""

    __parent__: "ListWithSelectedItemAndImage"

    @property
    def list_with_selected_item(self: "CastSelf") -> "_7744.ListWithSelectedItem":
        return self.__parent__._cast(_7744.ListWithSelectedItem)

    @property
    def list_with_selected_item_and_image(
        self: "CastSelf",
    ) -> "ListWithSelectedItemAndImage":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class ListWithSelectedItemAndImage(
    list_with_selected_item.ListWithSelectedItem_NamedTuple2_T,
    Image,
    _7743.IListWithSelectedItem,
    _7729.IWrapSMTType,
):
    """ListWithSelectedItemAndImage

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _LIST_WITH_SELECTED_ITEM_AND_IMAGE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ListWithSelectedItemAndImage":
        """Cast to another type.

        Returns:
            _Cast_ListWithSelectedItemAndImage
        """
        return _Cast_ListWithSelectedItemAndImage(self)
