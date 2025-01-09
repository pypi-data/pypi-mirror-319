"""CylindricalSocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2365

_CYLINDRICAL_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "CylindricalSocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2335,
        _2336,
        _2343,
        _2348,
        _2349,
        _2351,
        _2352,
        _2353,
        _2354,
        _2355,
        _2357,
        _2358,
        _2359,
        _2362,
        _2363,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import (
        _2412,
        _2414,
        _2416,
        _2418,
        _2420,
        _2422,
        _2423,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2402,
        _2403,
        _2405,
        _2406,
        _2408,
        _2409,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2379

    Self = TypeVar("Self", bound="CylindricalSocket")
    CastSelf = TypeVar("CastSelf", bound="CylindricalSocket._Cast_CylindricalSocket")


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalSocket:
    """Special nested class for casting CylindricalSocket to subclasses."""

    __parent__: "CylindricalSocket"

    @property
    def socket(self: "CastSelf") -> "_2365.Socket":
        return self.__parent__._cast(_2365.Socket)

    @property
    def bearing_inner_socket(self: "CastSelf") -> "_2335.BearingInnerSocket":
        from mastapy._private.system_model.connections_and_sockets import _2335

        return self.__parent__._cast(_2335.BearingInnerSocket)

    @property
    def bearing_outer_socket(self: "CastSelf") -> "_2336.BearingOuterSocket":
        from mastapy._private.system_model.connections_and_sockets import _2336

        return self.__parent__._cast(_2336.BearingOuterSocket)

    @property
    def cvt_pulley_socket(self: "CastSelf") -> "_2343.CVTPulleySocket":
        from mastapy._private.system_model.connections_and_sockets import _2343

        return self.__parent__._cast(_2343.CVTPulleySocket)

    @property
    def inner_shaft_socket(self: "CastSelf") -> "_2348.InnerShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2348

        return self.__parent__._cast(_2348.InnerShaftSocket)

    @property
    def inner_shaft_socket_base(self: "CastSelf") -> "_2349.InnerShaftSocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2349

        return self.__parent__._cast(_2349.InnerShaftSocketBase)

    @property
    def mountable_component_inner_socket(
        self: "CastSelf",
    ) -> "_2351.MountableComponentInnerSocket":
        from mastapy._private.system_model.connections_and_sockets import _2351

        return self.__parent__._cast(_2351.MountableComponentInnerSocket)

    @property
    def mountable_component_outer_socket(
        self: "CastSelf",
    ) -> "_2352.MountableComponentOuterSocket":
        from mastapy._private.system_model.connections_and_sockets import _2352

        return self.__parent__._cast(_2352.MountableComponentOuterSocket)

    @property
    def mountable_component_socket(
        self: "CastSelf",
    ) -> "_2353.MountableComponentSocket":
        from mastapy._private.system_model.connections_and_sockets import _2353

        return self.__parent__._cast(_2353.MountableComponentSocket)

    @property
    def outer_shaft_socket(self: "CastSelf") -> "_2354.OuterShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2354

        return self.__parent__._cast(_2354.OuterShaftSocket)

    @property
    def outer_shaft_socket_base(self: "CastSelf") -> "_2355.OuterShaftSocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2355

        return self.__parent__._cast(_2355.OuterShaftSocketBase)

    @property
    def planetary_socket(self: "CastSelf") -> "_2357.PlanetarySocket":
        from mastapy._private.system_model.connections_and_sockets import _2357

        return self.__parent__._cast(_2357.PlanetarySocket)

    @property
    def planetary_socket_base(self: "CastSelf") -> "_2358.PlanetarySocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2358

        return self.__parent__._cast(_2358.PlanetarySocketBase)

    @property
    def pulley_socket(self: "CastSelf") -> "_2359.PulleySocket":
        from mastapy._private.system_model.connections_and_sockets import _2359

        return self.__parent__._cast(_2359.PulleySocket)

    @property
    def rolling_ring_socket(self: "CastSelf") -> "_2362.RollingRingSocket":
        from mastapy._private.system_model.connections_and_sockets import _2362

        return self.__parent__._cast(_2362.RollingRingSocket)

    @property
    def shaft_socket(self: "CastSelf") -> "_2363.ShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2363

        return self.__parent__._cast(_2363.ShaftSocket)

    @property
    def cylindrical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2379.CylindricalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2379

        return self.__parent__._cast(_2379.CylindricalGearTeethSocket)

    @property
    def cycloidal_disc_axial_left_socket(
        self: "CastSelf",
    ) -> "_2402.CycloidalDiscAxialLeftSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2402,
        )

        return self.__parent__._cast(_2402.CycloidalDiscAxialLeftSocket)

    @property
    def cycloidal_disc_axial_right_socket(
        self: "CastSelf",
    ) -> "_2403.CycloidalDiscAxialRightSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2403,
        )

        return self.__parent__._cast(_2403.CycloidalDiscAxialRightSocket)

    @property
    def cycloidal_disc_inner_socket(
        self: "CastSelf",
    ) -> "_2405.CycloidalDiscInnerSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2405,
        )

        return self.__parent__._cast(_2405.CycloidalDiscInnerSocket)

    @property
    def cycloidal_disc_outer_socket(
        self: "CastSelf",
    ) -> "_2406.CycloidalDiscOuterSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2406,
        )

        return self.__parent__._cast(_2406.CycloidalDiscOuterSocket)

    @property
    def cycloidal_disc_planetary_bearing_socket(
        self: "CastSelf",
    ) -> "_2408.CycloidalDiscPlanetaryBearingSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2408,
        )

        return self.__parent__._cast(_2408.CycloidalDiscPlanetaryBearingSocket)

    @property
    def ring_pins_socket(self: "CastSelf") -> "_2409.RingPinsSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2409,
        )

        return self.__parent__._cast(_2409.RingPinsSocket)

    @property
    def clutch_socket(self: "CastSelf") -> "_2412.ClutchSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2412,
        )

        return self.__parent__._cast(_2412.ClutchSocket)

    @property
    def concept_coupling_socket(self: "CastSelf") -> "_2414.ConceptCouplingSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2414,
        )

        return self.__parent__._cast(_2414.ConceptCouplingSocket)

    @property
    def coupling_socket(self: "CastSelf") -> "_2416.CouplingSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2416,
        )

        return self.__parent__._cast(_2416.CouplingSocket)

    @property
    def part_to_part_shear_coupling_socket(
        self: "CastSelf",
    ) -> "_2418.PartToPartShearCouplingSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2418,
        )

        return self.__parent__._cast(_2418.PartToPartShearCouplingSocket)

    @property
    def spring_damper_socket(self: "CastSelf") -> "_2420.SpringDamperSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2420,
        )

        return self.__parent__._cast(_2420.SpringDamperSocket)

    @property
    def torque_converter_pump_socket(
        self: "CastSelf",
    ) -> "_2422.TorqueConverterPumpSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2422,
        )

        return self.__parent__._cast(_2422.TorqueConverterPumpSocket)

    @property
    def torque_converter_turbine_socket(
        self: "CastSelf",
    ) -> "_2423.TorqueConverterTurbineSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2423,
        )

        return self.__parent__._cast(_2423.TorqueConverterTurbineSocket)

    @property
    def cylindrical_socket(self: "CastSelf") -> "CylindricalSocket":
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
class CylindricalSocket(_2365.Socket):
    """CylindricalSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalSocket":
        """Cast to another type.

        Returns:
            _Cast_CylindricalSocket
        """
        return _Cast_CylindricalSocket(self)
