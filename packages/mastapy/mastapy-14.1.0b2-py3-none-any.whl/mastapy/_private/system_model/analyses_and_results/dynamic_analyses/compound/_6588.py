"""CycloidalDiscCentralBearingConnectionCompoundDynamicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
    _6568,
)

_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_COMPOUND_DYNAMIC_ANALYSIS = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound",
        "CycloidalDiscCentralBearingConnectionCompoundDynamicAnalysis",
    )
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2729
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7703,
        _7707,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6455,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
        _6547,
        _6579,
        _6643,
    )

    Self = TypeVar(
        "Self", bound="CycloidalDiscCentralBearingConnectionCompoundDynamicAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="CycloidalDiscCentralBearingConnectionCompoundDynamicAnalysis._Cast_CycloidalDiscCentralBearingConnectionCompoundDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalDiscCentralBearingConnectionCompoundDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalDiscCentralBearingConnectionCompoundDynamicAnalysis:
    """Special nested class for casting CycloidalDiscCentralBearingConnectionCompoundDynamicAnalysis to subclasses."""

    __parent__: "CycloidalDiscCentralBearingConnectionCompoundDynamicAnalysis"

    @property
    def coaxial_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6568.CoaxialConnectionCompoundDynamicAnalysis":
        return self.__parent__._cast(_6568.CoaxialConnectionCompoundDynamicAnalysis)

    @property
    def shaft_to_mountable_component_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6643.ShaftToMountableComponentConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6643,
        )

        return self.__parent__._cast(
            _6643.ShaftToMountableComponentConnectionCompoundDynamicAnalysis
        )

    @property
    def abstract_shaft_to_mountable_component_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6547.AbstractShaftToMountableComponentConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6547,
        )

        return self.__parent__._cast(
            _6547.AbstractShaftToMountableComponentConnectionCompoundDynamicAnalysis
        )

    @property
    def connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6579.ConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6579,
        )

        return self.__parent__._cast(_6579.ConnectionCompoundDynamicAnalysis)

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
    def cycloidal_disc_central_bearing_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "CycloidalDiscCentralBearingConnectionCompoundDynamicAnalysis":
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
class CycloidalDiscCentralBearingConnectionCompoundDynamicAnalysis(
    _6568.CoaxialConnectionCompoundDynamicAnalysis
):
    """CycloidalDiscCentralBearingConnectionCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_COMPOUND_DYNAMIC_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6455.CycloidalDiscCentralBearingConnectionDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.CycloidalDiscCentralBearingConnectionDynamicAnalysis]

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
    ) -> "List[_6455.CycloidalDiscCentralBearingConnectionDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.CycloidalDiscCentralBearingConnectionDynamicAnalysis]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_CycloidalDiscCentralBearingConnectionCompoundDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CycloidalDiscCentralBearingConnectionCompoundDynamicAnalysis
        """
        return _Cast_CycloidalDiscCentralBearingConnectionCompoundDynamicAnalysis(self)
