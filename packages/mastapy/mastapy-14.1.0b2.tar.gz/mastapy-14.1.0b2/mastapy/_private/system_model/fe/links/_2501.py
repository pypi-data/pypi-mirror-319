"""ShaftHubConnectionFELink"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.fe.links import _2494

_SHAFT_HUB_CONNECTION_FE_LINK = python_net_import(
    "SMT.MastaAPI.SystemModel.FE.Links", "ShaftHubConnectionFELink"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.fe.links import _2488, _2495

    Self = TypeVar("Self", bound="ShaftHubConnectionFELink")
    CastSelf = TypeVar(
        "CastSelf", bound="ShaftHubConnectionFELink._Cast_ShaftHubConnectionFELink"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftHubConnectionFELink",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftHubConnectionFELink:
    """Special nested class for casting ShaftHubConnectionFELink to subclasses."""

    __parent__: "ShaftHubConnectionFELink"

    @property
    def multi_node_connector_fe_link(
        self: "CastSelf",
    ) -> "_2494.MultiNodeConnectorFELink":
        return self.__parent__._cast(_2494.MultiNodeConnectorFELink)

    @property
    def multi_node_fe_link(self: "CastSelf") -> "_2495.MultiNodeFELink":
        from mastapy._private.system_model.fe.links import _2495

        return self.__parent__._cast(_2495.MultiNodeFELink)

    @property
    def fe_link(self: "CastSelf") -> "_2488.FELink":
        from mastapy._private.system_model.fe.links import _2488

        return self.__parent__._cast(_2488.FELink)

    @property
    def shaft_hub_connection_fe_link(self: "CastSelf") -> "ShaftHubConnectionFELink":
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
class ShaftHubConnectionFELink(_2494.MultiNodeConnectorFELink):
    """ShaftHubConnectionFELink

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_HUB_CONNECTION_FE_LINK

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftHubConnectionFELink":
        """Cast to another type.

        Returns:
            _Cast_ShaftHubConnectionFELink
        """
        return _Cast_ShaftHubConnectionFELink(self)
