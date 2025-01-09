"""BearingParametricStudyTool"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
    _4434,
)

_BEARING_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "BearingParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2016
    from mastapy._private.system_model.analyses_and_results import _2729, _2731, _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7709
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4423,
        _4485,
        _4497,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7510
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2776,
    )
    from mastapy._private.system_model.part_model import _2509

    Self = TypeVar("Self", bound="BearingParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf", bound="BearingParametricStudyTool._Cast_BearingParametricStudyTool"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BearingParametricStudyTool:
    """Special nested class for casting BearingParametricStudyTool to subclasses."""

    __parent__: "BearingParametricStudyTool"

    @property
    def connector_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4434.ConnectorParametricStudyTool":
        return self.__parent__._cast(_4434.ConnectorParametricStudyTool)

    @property
    def mountable_component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4485.MountableComponentParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4485,
        )

        return self.__parent__._cast(_4485.MountableComponentParametricStudyTool)

    @property
    def component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4423.ComponentParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4423,
        )

        return self.__parent__._cast(_4423.ComponentParametricStudyTool)

    @property
    def part_parametric_study_tool(self: "CastSelf") -> "_4497.PartParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4497,
        )

        return self.__parent__._cast(_4497.PartParametricStudyTool)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7709.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7709,
        )

        return self.__parent__._cast(_7709.PartAnalysisCase)

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
    def bearing_parametric_study_tool(self: "CastSelf") -> "BearingParametricStudyTool":
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
class BearingParametricStudyTool(_4434.ConnectorParametricStudyTool):
    """BearingParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEARING_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2509.Bearing":
        """mastapy.system_model.part_model.Bearing

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: "Self") -> "_7510.BearingLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def bearing_duty_cycle_results(
        self: "Self",
    ) -> "List[_2016.LoadedBearingDutyCycle]":
        """List[mastapy.bearings.bearing_results.LoadedBearingDutyCycle]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BearingDutyCycleResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_system_deflection_results(
        self: "Self",
    ) -> "List[_2776.BearingSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.BearingSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentSystemDeflectionResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def planetaries(self: "Self") -> "List[BearingParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.BearingParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Planetaries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_BearingParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_BearingParametricStudyTool
        """
        return _Cast_BearingParametricStudyTool(self)
