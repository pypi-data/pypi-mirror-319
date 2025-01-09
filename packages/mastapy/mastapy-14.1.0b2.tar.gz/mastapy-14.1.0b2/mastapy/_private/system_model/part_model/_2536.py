"""MountableComponent"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2514

_MOUNTABLE_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MountableComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2272
    from mastapy._private.system_model.connections_and_sockets import (
        _2338,
        _2341,
        _2345,
    )
    from mastapy._private.system_model.part_model import (
        _2505,
        _2509,
        _2515,
        _2517,
        _2532,
        _2533,
        _2538,
        _2540,
        _2541,
        _2543,
        _2544,
        _2550,
        _2552,
    )
    from mastapy._private.system_model.part_model.couplings import (
        _2655,
        _2658,
        _2661,
        _2664,
        _2666,
        _2668,
        _2675,
        _2677,
        _2684,
        _2687,
        _2688,
        _2689,
        _2691,
        _2693,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2645
    from mastapy._private.system_model.part_model.gears import (
        _2588,
        _2590,
        _2592,
        _2593,
        _2594,
        _2596,
        _2598,
        _2600,
        _2602,
        _2603,
        _2605,
        _2609,
        _2611,
        _2613,
        _2615,
        _2618,
        _2620,
        _2622,
        _2624,
        _2625,
        _2626,
        _2628,
    )

    Self = TypeVar("Self", bound="MountableComponent")
    CastSelf = TypeVar("CastSelf", bound="MountableComponent._Cast_MountableComponent")


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MountableComponent:
    """Special nested class for casting MountableComponent to subclasses."""

    __parent__: "MountableComponent"

    @property
    def component(self: "CastSelf") -> "_2514.Component":
        return self.__parent__._cast(_2514.Component)

    @property
    def part(self: "CastSelf") -> "_2540.Part":
        from mastapy._private.system_model.part_model import _2540

        return self.__parent__._cast(_2540.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2272.DesignEntity":
        from mastapy._private.system_model import _2272

        return self.__parent__._cast(_2272.DesignEntity)

    @property
    def bearing(self: "CastSelf") -> "_2509.Bearing":
        from mastapy._private.system_model.part_model import _2509

        return self.__parent__._cast(_2509.Bearing)

    @property
    def connector(self: "CastSelf") -> "_2517.Connector":
        from mastapy._private.system_model.part_model import _2517

        return self.__parent__._cast(_2517.Connector)

    @property
    def mass_disc(self: "CastSelf") -> "_2532.MassDisc":
        from mastapy._private.system_model.part_model import _2532

        return self.__parent__._cast(_2532.MassDisc)

    @property
    def measurement_component(self: "CastSelf") -> "_2533.MeasurementComponent":
        from mastapy._private.system_model.part_model import _2533

        return self.__parent__._cast(_2533.MeasurementComponent)

    @property
    def oil_seal(self: "CastSelf") -> "_2538.OilSeal":
        from mastapy._private.system_model.part_model import _2538

        return self.__parent__._cast(_2538.OilSeal)

    @property
    def planet_carrier(self: "CastSelf") -> "_2541.PlanetCarrier":
        from mastapy._private.system_model.part_model import _2541

        return self.__parent__._cast(_2541.PlanetCarrier)

    @property
    def point_load(self: "CastSelf") -> "_2543.PointLoad":
        from mastapy._private.system_model.part_model import _2543

        return self.__parent__._cast(_2543.PointLoad)

    @property
    def power_load(self: "CastSelf") -> "_2544.PowerLoad":
        from mastapy._private.system_model.part_model import _2544

        return self.__parent__._cast(_2544.PowerLoad)

    @property
    def unbalanced_mass(self: "CastSelf") -> "_2550.UnbalancedMass":
        from mastapy._private.system_model.part_model import _2550

        return self.__parent__._cast(_2550.UnbalancedMass)

    @property
    def virtual_component(self: "CastSelf") -> "_2552.VirtualComponent":
        from mastapy._private.system_model.part_model import _2552

        return self.__parent__._cast(_2552.VirtualComponent)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2588.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2588

        return self.__parent__._cast(_2588.AGMAGleasonConicalGear)

    @property
    def bevel_differential_gear(self: "CastSelf") -> "_2590.BevelDifferentialGear":
        from mastapy._private.system_model.part_model.gears import _2590

        return self.__parent__._cast(_2590.BevelDifferentialGear)

    @property
    def bevel_differential_planet_gear(
        self: "CastSelf",
    ) -> "_2592.BevelDifferentialPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2592

        return self.__parent__._cast(_2592.BevelDifferentialPlanetGear)

    @property
    def bevel_differential_sun_gear(
        self: "CastSelf",
    ) -> "_2593.BevelDifferentialSunGear":
        from mastapy._private.system_model.part_model.gears import _2593

        return self.__parent__._cast(_2593.BevelDifferentialSunGear)

    @property
    def bevel_gear(self: "CastSelf") -> "_2594.BevelGear":
        from mastapy._private.system_model.part_model.gears import _2594

        return self.__parent__._cast(_2594.BevelGear)

    @property
    def concept_gear(self: "CastSelf") -> "_2596.ConceptGear":
        from mastapy._private.system_model.part_model.gears import _2596

        return self.__parent__._cast(_2596.ConceptGear)

    @property
    def conical_gear(self: "CastSelf") -> "_2598.ConicalGear":
        from mastapy._private.system_model.part_model.gears import _2598

        return self.__parent__._cast(_2598.ConicalGear)

    @property
    def cylindrical_gear(self: "CastSelf") -> "_2600.CylindricalGear":
        from mastapy._private.system_model.part_model.gears import _2600

        return self.__parent__._cast(_2600.CylindricalGear)

    @property
    def cylindrical_planet_gear(self: "CastSelf") -> "_2602.CylindricalPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2602

        return self.__parent__._cast(_2602.CylindricalPlanetGear)

    @property
    def face_gear(self: "CastSelf") -> "_2603.FaceGear":
        from mastapy._private.system_model.part_model.gears import _2603

        return self.__parent__._cast(_2603.FaceGear)

    @property
    def gear(self: "CastSelf") -> "_2605.Gear":
        from mastapy._private.system_model.part_model.gears import _2605

        return self.__parent__._cast(_2605.Gear)

    @property
    def hypoid_gear(self: "CastSelf") -> "_2609.HypoidGear":
        from mastapy._private.system_model.part_model.gears import _2609

        return self.__parent__._cast(_2609.HypoidGear)

    @property
    def klingelnberg_cyclo_palloid_conical_gear(
        self: "CastSelf",
    ) -> "_2611.KlingelnbergCycloPalloidConicalGear":
        from mastapy._private.system_model.part_model.gears import _2611

        return self.__parent__._cast(_2611.KlingelnbergCycloPalloidConicalGear)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear(
        self: "CastSelf",
    ) -> "_2613.KlingelnbergCycloPalloidHypoidGear":
        from mastapy._private.system_model.part_model.gears import _2613

        return self.__parent__._cast(_2613.KlingelnbergCycloPalloidHypoidGear)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "CastSelf",
    ) -> "_2615.KlingelnbergCycloPalloidSpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2615

        return self.__parent__._cast(_2615.KlingelnbergCycloPalloidSpiralBevelGear)

    @property
    def spiral_bevel_gear(self: "CastSelf") -> "_2618.SpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2618

        return self.__parent__._cast(_2618.SpiralBevelGear)

    @property
    def straight_bevel_diff_gear(self: "CastSelf") -> "_2620.StraightBevelDiffGear":
        from mastapy._private.system_model.part_model.gears import _2620

        return self.__parent__._cast(_2620.StraightBevelDiffGear)

    @property
    def straight_bevel_gear(self: "CastSelf") -> "_2622.StraightBevelGear":
        from mastapy._private.system_model.part_model.gears import _2622

        return self.__parent__._cast(_2622.StraightBevelGear)

    @property
    def straight_bevel_planet_gear(self: "CastSelf") -> "_2624.StraightBevelPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2624

        return self.__parent__._cast(_2624.StraightBevelPlanetGear)

    @property
    def straight_bevel_sun_gear(self: "CastSelf") -> "_2625.StraightBevelSunGear":
        from mastapy._private.system_model.part_model.gears import _2625

        return self.__parent__._cast(_2625.StraightBevelSunGear)

    @property
    def worm_gear(self: "CastSelf") -> "_2626.WormGear":
        from mastapy._private.system_model.part_model.gears import _2626

        return self.__parent__._cast(_2626.WormGear)

    @property
    def zerol_bevel_gear(self: "CastSelf") -> "_2628.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2628

        return self.__parent__._cast(_2628.ZerolBevelGear)

    @property
    def ring_pins(self: "CastSelf") -> "_2645.RingPins":
        from mastapy._private.system_model.part_model.cycloidal import _2645

        return self.__parent__._cast(_2645.RingPins)

    @property
    def clutch_half(self: "CastSelf") -> "_2655.ClutchHalf":
        from mastapy._private.system_model.part_model.couplings import _2655

        return self.__parent__._cast(_2655.ClutchHalf)

    @property
    def concept_coupling_half(self: "CastSelf") -> "_2658.ConceptCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2658

        return self.__parent__._cast(_2658.ConceptCouplingHalf)

    @property
    def coupling_half(self: "CastSelf") -> "_2661.CouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2661

        return self.__parent__._cast(_2661.CouplingHalf)

    @property
    def cvt_pulley(self: "CastSelf") -> "_2664.CVTPulley":
        from mastapy._private.system_model.part_model.couplings import _2664

        return self.__parent__._cast(_2664.CVTPulley)

    @property
    def part_to_part_shear_coupling_half(
        self: "CastSelf",
    ) -> "_2666.PartToPartShearCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2666

        return self.__parent__._cast(_2666.PartToPartShearCouplingHalf)

    @property
    def pulley(self: "CastSelf") -> "_2668.Pulley":
        from mastapy._private.system_model.part_model.couplings import _2668

        return self.__parent__._cast(_2668.Pulley)

    @property
    def rolling_ring(self: "CastSelf") -> "_2675.RollingRing":
        from mastapy._private.system_model.part_model.couplings import _2675

        return self.__parent__._cast(_2675.RollingRing)

    @property
    def shaft_hub_connection(self: "CastSelf") -> "_2677.ShaftHubConnection":
        from mastapy._private.system_model.part_model.couplings import _2677

        return self.__parent__._cast(_2677.ShaftHubConnection)

    @property
    def spring_damper_half(self: "CastSelf") -> "_2684.SpringDamperHalf":
        from mastapy._private.system_model.part_model.couplings import _2684

        return self.__parent__._cast(_2684.SpringDamperHalf)

    @property
    def synchroniser_half(self: "CastSelf") -> "_2687.SynchroniserHalf":
        from mastapy._private.system_model.part_model.couplings import _2687

        return self.__parent__._cast(_2687.SynchroniserHalf)

    @property
    def synchroniser_part(self: "CastSelf") -> "_2688.SynchroniserPart":
        from mastapy._private.system_model.part_model.couplings import _2688

        return self.__parent__._cast(_2688.SynchroniserPart)

    @property
    def synchroniser_sleeve(self: "CastSelf") -> "_2689.SynchroniserSleeve":
        from mastapy._private.system_model.part_model.couplings import _2689

        return self.__parent__._cast(_2689.SynchroniserSleeve)

    @property
    def torque_converter_pump(self: "CastSelf") -> "_2691.TorqueConverterPump":
        from mastapy._private.system_model.part_model.couplings import _2691

        return self.__parent__._cast(_2691.TorqueConverterPump)

    @property
    def torque_converter_turbine(self: "CastSelf") -> "_2693.TorqueConverterTurbine":
        from mastapy._private.system_model.part_model.couplings import _2693

        return self.__parent__._cast(_2693.TorqueConverterTurbine)

    @property
    def mountable_component(self: "CastSelf") -> "MountableComponent":
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
class MountableComponent(_2514.Component):
    """MountableComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOUNTABLE_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def rotation_about_axis(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RotationAboutAxis")

        if temp is None:
            return 0.0

        return temp

    @rotation_about_axis.setter
    @enforce_parameter_types
    def rotation_about_axis(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RotationAboutAxis",
            float(value) if value is not None else 0.0,
        )

    @property
    def inner_component(self: "Self") -> "_2505.AbstractShaft":
        """mastapy.system_model.part_model.AbstractShaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerComponent")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def inner_connection(self: "Self") -> "_2341.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerConnection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def inner_socket(self: "Self") -> "_2345.CylindricalSocket":
        """mastapy.system_model.connections_and_sockets.CylindricalSocket

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerSocket")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def is_mounted(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsMounted")

        if temp is None:
            return False

        return temp

    @enforce_parameter_types
    def mount_on(
        self: "Self", shaft: "_2505.AbstractShaft", offset: "float" = float("nan")
    ) -> "_2338.CoaxialConnection":
        """mastapy.system_model.connections_and_sockets.CoaxialConnection

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)
        """
        offset = float(offset)
        method_result = pythonnet_method_call(
            self.wrapped,
            "MountOn",
            shaft.wrapped if shaft else None,
            offset if offset else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def try_mount_on(
        self: "Self", shaft: "_2505.AbstractShaft", offset: "float" = float("nan")
    ) -> "_2515.ComponentsConnectedResult":
        """mastapy.system_model.part_model.ComponentsConnectedResult

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)
        """
        offset = float(offset)
        method_result = pythonnet_method_call(
            self.wrapped,
            "TryMountOn",
            shaft.wrapped if shaft else None,
            offset if offset else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_MountableComponent":
        """Cast to another type.

        Returns:
            _Cast_MountableComponent
        """
        return _Cast_MountableComponent(self)
