"""CVTBeltConnectionPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows import _4139

_CVT_BELT_CONNECTION_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows",
    "CVTBeltConnectionPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2727, _2729, _2731
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7702,
        _7705,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4165,
        _4198,
    )
    from mastapy._private.system_model.connections_and_sockets import _2342

    Self = TypeVar("Self", bound="CVTBeltConnectionPowerFlow")
    CastSelf = TypeVar(
        "CastSelf", bound="CVTBeltConnectionPowerFlow._Cast_CVTBeltConnectionPowerFlow"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CVTBeltConnectionPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CVTBeltConnectionPowerFlow:
    """Special nested class for casting CVTBeltConnectionPowerFlow to subclasses."""

    __parent__: "CVTBeltConnectionPowerFlow"

    @property
    def belt_connection_power_flow(self: "CastSelf") -> "_4139.BeltConnectionPowerFlow":
        return self.__parent__._cast(_4139.BeltConnectionPowerFlow)

    @property
    def inter_mountable_component_connection_power_flow(
        self: "CastSelf",
    ) -> "_4198.InterMountableComponentConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4198

        return self.__parent__._cast(_4198.InterMountableComponentConnectionPowerFlow)

    @property
    def connection_power_flow(self: "CastSelf") -> "_4165.ConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4165

        return self.__parent__._cast(_4165.ConnectionPowerFlow)

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7705.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7705,
        )

        return self.__parent__._cast(_7705.ConnectionStaticLoadAnalysisCase)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7702.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7702,
        )

        return self.__parent__._cast(_7702.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2727.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2727

        return self.__parent__._cast(_2727.ConnectionAnalysis)

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
    def cvt_belt_connection_power_flow(
        self: "CastSelf",
    ) -> "CVTBeltConnectionPowerFlow":
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
class CVTBeltConnectionPowerFlow(_4139.BeltConnectionPowerFlow):
    """CVTBeltConnectionPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CVT_BELT_CONNECTION_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2342.CVTBeltConnection":
        """mastapy.system_model.connections_and_sockets.CVTBeltConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CVTBeltConnectionPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_CVTBeltConnectionPowerFlow
        """
        return _Cast_CVTBeltConnectionPowerFlow(self)
