"""BearingSettingsDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings import _1948
from mastapy._private.utility.databases import _1894

_BEARING_SETTINGS_DATABASE = python_net_import(
    "SMT.MastaAPI.Bearings", "BearingSettingsDatabase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.databases import _1890, _1897

    Self = TypeVar("Self", bound="BearingSettingsDatabase")
    CastSelf = TypeVar(
        "CastSelf", bound="BearingSettingsDatabase._Cast_BearingSettingsDatabase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingSettingsDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BearingSettingsDatabase:
    """Special nested class for casting BearingSettingsDatabase to subclasses."""

    __parent__: "BearingSettingsDatabase"

    @property
    def named_database(self: "CastSelf") -> "_1894.NamedDatabase":
        return self.__parent__._cast(_1894.NamedDatabase)

    @property
    def sql_database(self: "CastSelf") -> "_1897.SQLDatabase":
        pass

        from mastapy._private.utility.databases import _1897

        return self.__parent__._cast(_1897.SQLDatabase)

    @property
    def database(self: "CastSelf") -> "_1890.Database":
        pass

        from mastapy._private.utility.databases import _1890

        return self.__parent__._cast(_1890.Database)

    @property
    def bearing_settings_database(self: "CastSelf") -> "BearingSettingsDatabase":
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
class BearingSettingsDatabase(_1894.NamedDatabase[_1948.BearingSettingsItem]):
    """BearingSettingsDatabase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEARING_SETTINGS_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_BearingSettingsDatabase":
        """Cast to another type.

        Returns:
            _Cast_BearingSettingsDatabase
        """
        return _Cast_BearingSettingsDatabase(self)
