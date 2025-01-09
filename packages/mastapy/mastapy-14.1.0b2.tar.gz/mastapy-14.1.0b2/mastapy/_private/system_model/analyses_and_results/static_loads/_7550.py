"""CycloidalDiscLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.static_loads import _7498

_CYCLOIDAL_DISC_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "CycloidalDiscLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2729, _2731, _2735
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7499,
        _7528,
        _7621,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2644

    Self = TypeVar("Self", bound="CycloidalDiscLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="CycloidalDiscLoadCase._Cast_CycloidalDiscLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalDiscLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalDiscLoadCase:
    """Special nested class for casting CycloidalDiscLoadCase to subclasses."""

    __parent__: "CycloidalDiscLoadCase"

    @property
    def abstract_shaft_load_case(self: "CastSelf") -> "_7498.AbstractShaftLoadCase":
        return self.__parent__._cast(_7498.AbstractShaftLoadCase)

    @property
    def abstract_shaft_or_housing_load_case(
        self: "CastSelf",
    ) -> "_7499.AbstractShaftOrHousingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7499,
        )

        return self.__parent__._cast(_7499.AbstractShaftOrHousingLoadCase)

    @property
    def component_load_case(self: "CastSelf") -> "_7528.ComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7528,
        )

        return self.__parent__._cast(_7528.ComponentLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "_7621.PartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7621,
        )

        return self.__parent__._cast(_7621.PartLoadCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2735.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2735

        return self.__parent__._cast(_2735.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2731.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2731

        return self.__parent__._cast(_2731.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2729.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2729

        return self.__parent__._cast(_2729.DesignEntityAnalysis)

    @property
    def cycloidal_disc_load_case(self: "CastSelf") -> "CycloidalDiscLoadCase":
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
class CycloidalDiscLoadCase(_7498.AbstractShaftLoadCase):
    """CycloidalDiscLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYCLOIDAL_DISC_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2644.CycloidalDisc":
        """mastapy.system_model.part_model.cycloidal.CycloidalDisc

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CycloidalDiscLoadCase":
        """Cast to another type.

        Returns:
            _Cast_CycloidalDiscLoadCase
        """
        return _Cast_CycloidalDiscLoadCase(self)
