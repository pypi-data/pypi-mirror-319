"""NeedleRollerBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_designs.rolling import _2217

_NEEDLE_ROLLER_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "NeedleRollerBearing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_designs import _2198, _2199, _2202
    from mastapy._private.bearings.bearing_designs.rolling import _2229, _2230, _2233

    Self = TypeVar("Self", bound="NeedleRollerBearing")
    CastSelf = TypeVar(
        "CastSelf", bound="NeedleRollerBearing._Cast_NeedleRollerBearing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("NeedleRollerBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NeedleRollerBearing:
    """Special nested class for casting NeedleRollerBearing to subclasses."""

    __parent__: "NeedleRollerBearing"

    @property
    def cylindrical_roller_bearing(
        self: "CastSelf",
    ) -> "_2217.CylindricalRollerBearing":
        return self.__parent__._cast(_2217.CylindricalRollerBearing)

    @property
    def non_barrel_roller_bearing(self: "CastSelf") -> "_2229.NonBarrelRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2229

        return self.__parent__._cast(_2229.NonBarrelRollerBearing)

    @property
    def roller_bearing(self: "CastSelf") -> "_2230.RollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2230

        return self.__parent__._cast(_2230.RollerBearing)

    @property
    def rolling_bearing(self: "CastSelf") -> "_2233.RollingBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2233

        return self.__parent__._cast(_2233.RollingBearing)

    @property
    def detailed_bearing(self: "CastSelf") -> "_2199.DetailedBearing":
        from mastapy._private.bearings.bearing_designs import _2199

        return self.__parent__._cast(_2199.DetailedBearing)

    @property
    def non_linear_bearing(self: "CastSelf") -> "_2202.NonLinearBearing":
        from mastapy._private.bearings.bearing_designs import _2202

        return self.__parent__._cast(_2202.NonLinearBearing)

    @property
    def bearing_design(self: "CastSelf") -> "_2198.BearingDesign":
        from mastapy._private.bearings.bearing_designs import _2198

        return self.__parent__._cast(_2198.BearingDesign)

    @property
    def needle_roller_bearing(self: "CastSelf") -> "NeedleRollerBearing":
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
class NeedleRollerBearing(_2217.CylindricalRollerBearing):
    """NeedleRollerBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NEEDLE_ROLLER_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_NeedleRollerBearing":
        """Cast to another type.

        Returns:
            _Cast_NeedleRollerBearing
        """
        return _Cast_NeedleRollerBearing(self)
