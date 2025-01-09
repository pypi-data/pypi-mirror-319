"""OuterShaftSocketBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2363

_OUTER_SHAFT_SOCKET_BASE = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "OuterShaftSocketBase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2345,
        _2354,
        _2365,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import _2403

    Self = TypeVar("Self", bound="OuterShaftSocketBase")
    CastSelf = TypeVar(
        "CastSelf", bound="OuterShaftSocketBase._Cast_OuterShaftSocketBase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("OuterShaftSocketBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OuterShaftSocketBase:
    """Special nested class for casting OuterShaftSocketBase to subclasses."""

    __parent__: "OuterShaftSocketBase"

    @property
    def shaft_socket(self: "CastSelf") -> "_2363.ShaftSocket":
        return self.__parent__._cast(_2363.ShaftSocket)

    @property
    def cylindrical_socket(self: "CastSelf") -> "_2345.CylindricalSocket":
        from mastapy._private.system_model.connections_and_sockets import _2345

        return self.__parent__._cast(_2345.CylindricalSocket)

    @property
    def socket(self: "CastSelf") -> "_2365.Socket":
        from mastapy._private.system_model.connections_and_sockets import _2365

        return self.__parent__._cast(_2365.Socket)

    @property
    def outer_shaft_socket(self: "CastSelf") -> "_2354.OuterShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2354

        return self.__parent__._cast(_2354.OuterShaftSocket)

    @property
    def cycloidal_disc_axial_right_socket(
        self: "CastSelf",
    ) -> "_2403.CycloidalDiscAxialRightSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2403,
        )

        return self.__parent__._cast(_2403.CycloidalDiscAxialRightSocket)

    @property
    def outer_shaft_socket_base(self: "CastSelf") -> "OuterShaftSocketBase":
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
class OuterShaftSocketBase(_2363.ShaftSocket):
    """OuterShaftSocketBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _OUTER_SHAFT_SOCKET_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_OuterShaftSocketBase":
        """Cast to another type.

        Returns:
            _Cast_OuterShaftSocketBase
        """
        return _Cast_OuterShaftSocketBase(self)
