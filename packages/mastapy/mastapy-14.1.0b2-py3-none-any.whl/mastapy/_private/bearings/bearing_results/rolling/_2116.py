"""LoadedTaperRollerBearingResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_results.rolling import _2092

_LOADED_TAPER_ROLLER_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedTaperRollerBearingResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _1942
    from mastapy._private.bearings.bearing_results import _2017, _2022, _2025
    from mastapy._private.bearings.bearing_results.rolling import _2097, _2101

    Self = TypeVar("Self", bound="LoadedTaperRollerBearingResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedTaperRollerBearingResults._Cast_LoadedTaperRollerBearingResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedTaperRollerBearingResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedTaperRollerBearingResults:
    """Special nested class for casting LoadedTaperRollerBearingResults to subclasses."""

    __parent__: "LoadedTaperRollerBearingResults"

    @property
    def loaded_non_barrel_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2092.LoadedNonBarrelRollerBearingResults":
        return self.__parent__._cast(_2092.LoadedNonBarrelRollerBearingResults)

    @property
    def loaded_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2097.LoadedRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2097

        return self.__parent__._cast(_2097.LoadedRollerBearingResults)

    @property
    def loaded_rolling_bearing_results(
        self: "CastSelf",
    ) -> "_2101.LoadedRollingBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2101

        return self.__parent__._cast(_2101.LoadedRollingBearingResults)

    @property
    def loaded_detailed_bearing_results(
        self: "CastSelf",
    ) -> "_2022.LoadedDetailedBearingResults":
        from mastapy._private.bearings.bearing_results import _2022

        return self.__parent__._cast(_2022.LoadedDetailedBearingResults)

    @property
    def loaded_non_linear_bearing_results(
        self: "CastSelf",
    ) -> "_2025.LoadedNonLinearBearingResults":
        from mastapy._private.bearings.bearing_results import _2025

        return self.__parent__._cast(_2025.LoadedNonLinearBearingResults)

    @property
    def loaded_bearing_results(self: "CastSelf") -> "_2017.LoadedBearingResults":
        from mastapy._private.bearings.bearing_results import _2017

        return self.__parent__._cast(_2017.LoadedBearingResults)

    @property
    def bearing_load_case_results_lightweight(
        self: "CastSelf",
    ) -> "_1942.BearingLoadCaseResultsLightweight":
        from mastapy._private.bearings import _1942

        return self.__parent__._cast(_1942.BearingLoadCaseResultsLightweight)

    @property
    def loaded_taper_roller_bearing_results(
        self: "CastSelf",
    ) -> "LoadedTaperRollerBearingResults":
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
class LoadedTaperRollerBearingResults(_2092.LoadedNonBarrelRollerBearingResults):
    """LoadedTaperRollerBearingResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_TAPER_ROLLER_BEARING_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedTaperRollerBearingResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedTaperRollerBearingResults
        """
        return _Cast_LoadedTaperRollerBearingResults(self)
