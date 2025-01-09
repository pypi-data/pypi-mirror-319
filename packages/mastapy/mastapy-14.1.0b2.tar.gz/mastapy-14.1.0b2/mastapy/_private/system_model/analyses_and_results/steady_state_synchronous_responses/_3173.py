"""SteadyStateSynchronousResponse"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7701

_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses",
    "SteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2728
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7699,
        _7714,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3175,
    )

    Self = TypeVar("Self", bound="SteadyStateSynchronousResponse")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SteadyStateSynchronousResponse._Cast_SteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SteadyStateSynchronousResponse:
    """Special nested class for casting SteadyStateSynchronousResponse to subclasses."""

    __parent__: "SteadyStateSynchronousResponse"

    @property
    def compound_analysis_case(self: "CastSelf") -> "_7701.CompoundAnalysisCase":
        return self.__parent__._cast(_7701.CompoundAnalysisCase)

    @property
    def static_load_analysis_case(self: "CastSelf") -> "_7714.StaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7714,
        )

        return self.__parent__._cast(_7714.StaticLoadAnalysisCase)

    @property
    def analysis_case(self: "CastSelf") -> "_7699.AnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7699,
        )

        return self.__parent__._cast(_7699.AnalysisCase)

    @property
    def context(self: "CastSelf") -> "_2728.Context":
        from mastapy._private.system_model.analyses_and_results import _2728

        return self.__parent__._cast(_2728.Context)

    @property
    def steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "SteadyStateSynchronousResponse":
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
class SteadyStateSynchronousResponse(_7701.CompoundAnalysisCase):
    """SteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STEADY_STATE_SYNCHRONOUS_RESPONSE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def steady_state_analysis_options(
        self: "Self",
    ) -> "_3175.SteadyStateSynchronousResponseOptions":
        """mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.SteadyStateSynchronousResponseOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SteadyStateAnalysisOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_SteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_SteadyStateSynchronousResponse
        """
        return _Cast_SteadyStateSynchronousResponse(self)
