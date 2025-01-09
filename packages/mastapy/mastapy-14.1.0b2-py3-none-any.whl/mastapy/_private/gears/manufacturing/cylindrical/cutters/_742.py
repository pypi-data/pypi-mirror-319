"""CylindricalGearPlungeShaverDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.cylindrical import _641
from mastapy._private.gears.manufacturing.cylindrical.cutters import _741

_CYLINDRICAL_GEAR_PLUNGE_SHAVER_DATABASE = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters",
    "CylindricalGearPlungeShaverDatabase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.databases import _1890, _1894, _1897

    Self = TypeVar("Self", bound="CylindricalGearPlungeShaverDatabase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearPlungeShaverDatabase._Cast_CylindricalGearPlungeShaverDatabase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearPlungeShaverDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearPlungeShaverDatabase:
    """Special nested class for casting CylindricalGearPlungeShaverDatabase to subclasses."""

    __parent__: "CylindricalGearPlungeShaverDatabase"

    @property
    def cylindrical_cutter_database(
        self: "CastSelf",
    ) -> "_641.CylindricalCutterDatabase":
        return self.__parent__._cast(_641.CylindricalCutterDatabase)

    @property
    def named_database(self: "CastSelf") -> "_1894.NamedDatabase":
        from mastapy._private.utility.databases import _1894

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
    def cylindrical_gear_plunge_shaver_database(
        self: "CastSelf",
    ) -> "CylindricalGearPlungeShaverDatabase":
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
class CylindricalGearPlungeShaverDatabase(
    _641.CylindricalCutterDatabase[_741.CylindricalGearPlungeShaver]
):
    """CylindricalGearPlungeShaverDatabase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_PLUNGE_SHAVER_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearPlungeShaverDatabase":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearPlungeShaverDatabase
        """
        return _Cast_CylindricalGearPlungeShaverDatabase(self)
