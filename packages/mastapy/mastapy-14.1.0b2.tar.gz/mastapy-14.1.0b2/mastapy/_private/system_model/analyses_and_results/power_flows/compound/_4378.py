"""StraightBevelGearMeshCompoundPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
    _4284,
)

_STRAIGHT_BEVEL_GEAR_MESH_COMPOUND_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound",
    "StraightBevelGearMeshCompoundPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2729
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7703,
        _7707,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4245
    from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
        _4272,
        _4300,
        _4302,
        _4326,
        _4332,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2396

    Self = TypeVar("Self", bound="StraightBevelGearMeshCompoundPowerFlow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelGearMeshCompoundPowerFlow._Cast_StraightBevelGearMeshCompoundPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelGearMeshCompoundPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelGearMeshCompoundPowerFlow:
    """Special nested class for casting StraightBevelGearMeshCompoundPowerFlow to subclasses."""

    __parent__: "StraightBevelGearMeshCompoundPowerFlow"

    @property
    def bevel_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4284.BevelGearMeshCompoundPowerFlow":
        return self.__parent__._cast(_4284.BevelGearMeshCompoundPowerFlow)

    @property
    def agma_gleason_conical_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4272.AGMAGleasonConicalGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4272,
        )

        return self.__parent__._cast(_4272.AGMAGleasonConicalGearMeshCompoundPowerFlow)

    @property
    def conical_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4300.ConicalGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4300,
        )

        return self.__parent__._cast(_4300.ConicalGearMeshCompoundPowerFlow)

    @property
    def gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4326.GearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4326,
        )

        return self.__parent__._cast(_4326.GearMeshCompoundPowerFlow)

    @property
    def inter_mountable_component_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4332.InterMountableComponentConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4332,
        )

        return self.__parent__._cast(
            _4332.InterMountableComponentConnectionCompoundPowerFlow
        )

    @property
    def connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4302.ConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4302,
        )

        return self.__parent__._cast(_4302.ConnectionCompoundPowerFlow)

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7703.ConnectionCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7703,
        )

        return self.__parent__._cast(_7703.ConnectionCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7707.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7707,
        )

        return self.__parent__._cast(_7707.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2729.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2729

        return self.__parent__._cast(_2729.DesignEntityAnalysis)

    @property
    def straight_bevel_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "StraightBevelGearMeshCompoundPowerFlow":
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
class StraightBevelGearMeshCompoundPowerFlow(_4284.BevelGearMeshCompoundPowerFlow):
    """StraightBevelGearMeshCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_GEAR_MESH_COMPOUND_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2396.StraightBevelGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_design(self: "Self") -> "_2396.StraightBevelGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4245.StraightBevelGearMeshPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.StraightBevelGearMeshPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_4245.StraightBevelGearMeshPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.StraightBevelGearMeshPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelGearMeshCompoundPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelGearMeshCompoundPowerFlow
        """
        return _Cast_StraightBevelGearMeshCompoundPowerFlow(self)
