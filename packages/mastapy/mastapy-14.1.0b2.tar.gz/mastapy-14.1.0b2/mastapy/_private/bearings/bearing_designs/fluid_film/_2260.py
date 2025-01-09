"""PlainJournalBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.bearing_designs import _2199

_PLAIN_JOURNAL_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm", "PlainJournalBearing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_designs import _2198, _2202
    from mastapy._private.bearings.bearing_designs.fluid_film import _2258, _2262

    Self = TypeVar("Self", bound="PlainJournalBearing")
    CastSelf = TypeVar(
        "CastSelf", bound="PlainJournalBearing._Cast_PlainJournalBearing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlainJournalBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlainJournalBearing:
    """Special nested class for casting PlainJournalBearing to subclasses."""

    __parent__: "PlainJournalBearing"

    @property
    def detailed_bearing(self: "CastSelf") -> "_2199.DetailedBearing":
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
    def plain_grease_filled_journal_bearing(
        self: "CastSelf",
    ) -> "_2258.PlainGreaseFilledJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2258

        return self.__parent__._cast(_2258.PlainGreaseFilledJournalBearing)

    @property
    def plain_oil_fed_journal_bearing(
        self: "CastSelf",
    ) -> "_2262.PlainOilFedJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2262

        return self.__parent__._cast(_2262.PlainOilFedJournalBearing)

    @property
    def plain_journal_bearing(self: "CastSelf") -> "PlainJournalBearing":
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
class PlainJournalBearing(_2199.DetailedBearing):
    """PlainJournalBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLAIN_JOURNAL_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def diametrical_clearance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DiametricalClearance")

        if temp is None:
            return 0.0

        return temp

    @diametrical_clearance.setter
    @enforce_parameter_types
    def diametrical_clearance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DiametricalClearance",
            float(value) if value is not None else 0.0,
        )

    @property
    def land_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LandWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    def land_width_to_diameter_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LandWidthToDiameterRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_PlainJournalBearing":
        """Cast to another type.

        Returns:
            _Cast_PlainJournalBearing
        """
        return _Cast_PlainJournalBearing(self)
