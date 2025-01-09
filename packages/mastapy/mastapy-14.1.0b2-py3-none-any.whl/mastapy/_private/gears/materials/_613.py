"""CylindricalGearMaterialDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.materials import _289

_CYLINDRICAL_GEAR_MATERIAL_DATABASE = python_net_import(
    "SMT.MastaAPI.Gears.Materials", "CylindricalGearMaterialDatabase"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.gears.materials import _610, _611, _612, _614
    from mastapy._private.utility.databases import _1890, _1894, _1897

    Self = TypeVar("Self", bound="CylindricalGearMaterialDatabase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearMaterialDatabase._Cast_CylindricalGearMaterialDatabase",
    )

T = TypeVar("T", bound="_612.CylindricalGearMaterial")

__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearMaterialDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearMaterialDatabase:
    """Special nested class for casting CylindricalGearMaterialDatabase to subclasses."""

    __parent__: "CylindricalGearMaterialDatabase"

    @property
    def material_database(self: "CastSelf") -> "_289.MaterialDatabase":
        return self.__parent__._cast(_289.MaterialDatabase)

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
    def cylindrical_gear_agma_material_database(
        self: "CastSelf",
    ) -> "_610.CylindricalGearAGMAMaterialDatabase":
        from mastapy._private.gears.materials import _610

        return self.__parent__._cast(_610.CylindricalGearAGMAMaterialDatabase)

    @property
    def cylindrical_gear_iso_material_database(
        self: "CastSelf",
    ) -> "_611.CylindricalGearISOMaterialDatabase":
        from mastapy._private.gears.materials import _611

        return self.__parent__._cast(_611.CylindricalGearISOMaterialDatabase)

    @property
    def cylindrical_gear_plastic_material_database(
        self: "CastSelf",
    ) -> "_614.CylindricalGearPlasticMaterialDatabase":
        from mastapy._private.gears.materials import _614

        return self.__parent__._cast(_614.CylindricalGearPlasticMaterialDatabase)

    @property
    def cylindrical_gear_material_database(
        self: "CastSelf",
    ) -> "CylindricalGearMaterialDatabase":
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
class CylindricalGearMaterialDatabase(_289.MaterialDatabase[T]):
    """CylindricalGearMaterialDatabase

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MATERIAL_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearMaterialDatabase":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearMaterialDatabase
        """
        return _Cast_CylindricalGearMaterialDatabase(self)
