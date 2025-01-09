"""Part"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model import _2272

_PART = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Part")

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.math_utility import _1577
    from mastapy._private.system_model.connections_and_sockets import _2341
    from mastapy._private.system_model.import_export import _2311
    from mastapy._private.system_model.part_model import (
        _2503,
        _2504,
        _2505,
        _2506,
        _2509,
        _2512,
        _2513,
        _2514,
        _2517,
        _2518,
        _2522,
        _2523,
        _2524,
        _2525,
        _2532,
        _2533,
        _2534,
        _2535,
        _2536,
        _2538,
        _2541,
        _2543,
        _2544,
        _2547,
        _2549,
        _2550,
        _2552,
    )
    from mastapy._private.system_model.part_model.couplings import (
        _2652,
        _2654,
        _2655,
        _2657,
        _2658,
        _2660,
        _2661,
        _2663,
        _2664,
        _2665,
        _2666,
        _2668,
        _2675,
        _2676,
        _2677,
        _2683,
        _2684,
        _2685,
        _2687,
        _2688,
        _2689,
        _2690,
        _2691,
        _2693,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2643, _2644, _2645
    from mastapy._private.system_model.part_model.gears import (
        _2588,
        _2589,
        _2590,
        _2591,
        _2592,
        _2593,
        _2594,
        _2595,
        _2596,
        _2597,
        _2598,
        _2599,
        _2600,
        _2601,
        _2602,
        _2603,
        _2604,
        _2605,
        _2607,
        _2609,
        _2610,
        _2611,
        _2612,
        _2613,
        _2614,
        _2615,
        _2616,
        _2617,
        _2618,
        _2619,
        _2620,
        _2621,
        _2622,
        _2623,
        _2624,
        _2625,
        _2626,
        _2627,
        _2628,
        _2629,
    )
    from mastapy._private.system_model.part_model.shaft_model import _2555

    Self = TypeVar("Self", bound="Part")
    CastSelf = TypeVar("CastSelf", bound="Part._Cast_Part")


__docformat__ = "restructuredtext en"
__all__ = ("Part",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Part:
    """Special nested class for casting Part to subclasses."""

    __parent__: "Part"

    @property
    def design_entity(self: "CastSelf") -> "_2272.DesignEntity":
        return self.__parent__._cast(_2272.DesignEntity)

    @property
    def assembly(self: "CastSelf") -> "_2503.Assembly":
        return self.__parent__._cast(_2503.Assembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2504.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2504

        return self.__parent__._cast(_2504.AbstractAssembly)

    @property
    def abstract_shaft(self: "CastSelf") -> "_2505.AbstractShaft":
        from mastapy._private.system_model.part_model import _2505

        return self.__parent__._cast(_2505.AbstractShaft)

    @property
    def abstract_shaft_or_housing(self: "CastSelf") -> "_2506.AbstractShaftOrHousing":
        from mastapy._private.system_model.part_model import _2506

        return self.__parent__._cast(_2506.AbstractShaftOrHousing)

    @property
    def bearing(self: "CastSelf") -> "_2509.Bearing":
        from mastapy._private.system_model.part_model import _2509

        return self.__parent__._cast(_2509.Bearing)

    @property
    def bolt(self: "CastSelf") -> "_2512.Bolt":
        from mastapy._private.system_model.part_model import _2512

        return self.__parent__._cast(_2512.Bolt)

    @property
    def bolted_joint(self: "CastSelf") -> "_2513.BoltedJoint":
        from mastapy._private.system_model.part_model import _2513

        return self.__parent__._cast(_2513.BoltedJoint)

    @property
    def component(self: "CastSelf") -> "_2514.Component":
        from mastapy._private.system_model.part_model import _2514

        return self.__parent__._cast(_2514.Component)

    @property
    def connector(self: "CastSelf") -> "_2517.Connector":
        from mastapy._private.system_model.part_model import _2517

        return self.__parent__._cast(_2517.Connector)

    @property
    def datum(self: "CastSelf") -> "_2518.Datum":
        from mastapy._private.system_model.part_model import _2518

        return self.__parent__._cast(_2518.Datum)

    @property
    def external_cad_model(self: "CastSelf") -> "_2522.ExternalCADModel":
        from mastapy._private.system_model.part_model import _2522

        return self.__parent__._cast(_2522.ExternalCADModel)

    @property
    def fe_part(self: "CastSelf") -> "_2523.FEPart":
        from mastapy._private.system_model.part_model import _2523

        return self.__parent__._cast(_2523.FEPart)

    @property
    def flexible_pin_assembly(self: "CastSelf") -> "_2524.FlexiblePinAssembly":
        from mastapy._private.system_model.part_model import _2524

        return self.__parent__._cast(_2524.FlexiblePinAssembly)

    @property
    def guide_dxf_model(self: "CastSelf") -> "_2525.GuideDxfModel":
        from mastapy._private.system_model.part_model import _2525

        return self.__parent__._cast(_2525.GuideDxfModel)

    @property
    def mass_disc(self: "CastSelf") -> "_2532.MassDisc":
        from mastapy._private.system_model.part_model import _2532

        return self.__parent__._cast(_2532.MassDisc)

    @property
    def measurement_component(self: "CastSelf") -> "_2533.MeasurementComponent":
        from mastapy._private.system_model.part_model import _2533

        return self.__parent__._cast(_2533.MeasurementComponent)

    @property
    def microphone(self: "CastSelf") -> "_2534.Microphone":
        from mastapy._private.system_model.part_model import _2534

        return self.__parent__._cast(_2534.Microphone)

    @property
    def microphone_array(self: "CastSelf") -> "_2535.MicrophoneArray":
        from mastapy._private.system_model.part_model import _2535

        return self.__parent__._cast(_2535.MicrophoneArray)

    @property
    def mountable_component(self: "CastSelf") -> "_2536.MountableComponent":
        from mastapy._private.system_model.part_model import _2536

        return self.__parent__._cast(_2536.MountableComponent)

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
    def root_assembly(self: "CastSelf") -> "_2547.RootAssembly":
        from mastapy._private.system_model.part_model import _2547

        return self.__parent__._cast(_2547.RootAssembly)

    @property
    def specialised_assembly(self: "CastSelf") -> "_2549.SpecialisedAssembly":
        from mastapy._private.system_model.part_model import _2549

        return self.__parent__._cast(_2549.SpecialisedAssembly)

    @property
    def unbalanced_mass(self: "CastSelf") -> "_2550.UnbalancedMass":
        from mastapy._private.system_model.part_model import _2550

        return self.__parent__._cast(_2550.UnbalancedMass)

    @property
    def virtual_component(self: "CastSelf") -> "_2552.VirtualComponent":
        from mastapy._private.system_model.part_model import _2552

        return self.__parent__._cast(_2552.VirtualComponent)

    @property
    def shaft(self: "CastSelf") -> "_2555.Shaft":
        from mastapy._private.system_model.part_model.shaft_model import _2555

        return self.__parent__._cast(_2555.Shaft)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2588.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2588

        return self.__parent__._cast(_2588.AGMAGleasonConicalGear)

    @property
    def agma_gleason_conical_gear_set(
        self: "CastSelf",
    ) -> "_2589.AGMAGleasonConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2589

        return self.__parent__._cast(_2589.AGMAGleasonConicalGearSet)

    @property
    def bevel_differential_gear(self: "CastSelf") -> "_2590.BevelDifferentialGear":
        from mastapy._private.system_model.part_model.gears import _2590

        return self.__parent__._cast(_2590.BevelDifferentialGear)

    @property
    def bevel_differential_gear_set(
        self: "CastSelf",
    ) -> "_2591.BevelDifferentialGearSet":
        from mastapy._private.system_model.part_model.gears import _2591

        return self.__parent__._cast(_2591.BevelDifferentialGearSet)

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
    def bevel_gear_set(self: "CastSelf") -> "_2595.BevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2595

        return self.__parent__._cast(_2595.BevelGearSet)

    @property
    def concept_gear(self: "CastSelf") -> "_2596.ConceptGear":
        from mastapy._private.system_model.part_model.gears import _2596

        return self.__parent__._cast(_2596.ConceptGear)

    @property
    def concept_gear_set(self: "CastSelf") -> "_2597.ConceptGearSet":
        from mastapy._private.system_model.part_model.gears import _2597

        return self.__parent__._cast(_2597.ConceptGearSet)

    @property
    def conical_gear(self: "CastSelf") -> "_2598.ConicalGear":
        from mastapy._private.system_model.part_model.gears import _2598

        return self.__parent__._cast(_2598.ConicalGear)

    @property
    def conical_gear_set(self: "CastSelf") -> "_2599.ConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2599

        return self.__parent__._cast(_2599.ConicalGearSet)

    @property
    def cylindrical_gear(self: "CastSelf") -> "_2600.CylindricalGear":
        from mastapy._private.system_model.part_model.gears import _2600

        return self.__parent__._cast(_2600.CylindricalGear)

    @property
    def cylindrical_gear_set(self: "CastSelf") -> "_2601.CylindricalGearSet":
        from mastapy._private.system_model.part_model.gears import _2601

        return self.__parent__._cast(_2601.CylindricalGearSet)

    @property
    def cylindrical_planet_gear(self: "CastSelf") -> "_2602.CylindricalPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2602

        return self.__parent__._cast(_2602.CylindricalPlanetGear)

    @property
    def face_gear(self: "CastSelf") -> "_2603.FaceGear":
        from mastapy._private.system_model.part_model.gears import _2603

        return self.__parent__._cast(_2603.FaceGear)

    @property
    def face_gear_set(self: "CastSelf") -> "_2604.FaceGearSet":
        from mastapy._private.system_model.part_model.gears import _2604

        return self.__parent__._cast(_2604.FaceGearSet)

    @property
    def gear(self: "CastSelf") -> "_2605.Gear":
        from mastapy._private.system_model.part_model.gears import _2605

        return self.__parent__._cast(_2605.Gear)

    @property
    def gear_set(self: "CastSelf") -> "_2607.GearSet":
        from mastapy._private.system_model.part_model.gears import _2607

        return self.__parent__._cast(_2607.GearSet)

    @property
    def hypoid_gear(self: "CastSelf") -> "_2609.HypoidGear":
        from mastapy._private.system_model.part_model.gears import _2609

        return self.__parent__._cast(_2609.HypoidGear)

    @property
    def hypoid_gear_set(self: "CastSelf") -> "_2610.HypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2610

        return self.__parent__._cast(_2610.HypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_conical_gear(
        self: "CastSelf",
    ) -> "_2611.KlingelnbergCycloPalloidConicalGear":
        from mastapy._private.system_model.part_model.gears import _2611

        return self.__parent__._cast(_2611.KlingelnbergCycloPalloidConicalGear)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set(
        self: "CastSelf",
    ) -> "_2612.KlingelnbergCycloPalloidConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2612

        return self.__parent__._cast(_2612.KlingelnbergCycloPalloidConicalGearSet)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear(
        self: "CastSelf",
    ) -> "_2613.KlingelnbergCycloPalloidHypoidGear":
        from mastapy._private.system_model.part_model.gears import _2613

        return self.__parent__._cast(_2613.KlingelnbergCycloPalloidHypoidGear)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "CastSelf",
    ) -> "_2614.KlingelnbergCycloPalloidHypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2614

        return self.__parent__._cast(_2614.KlingelnbergCycloPalloidHypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "CastSelf",
    ) -> "_2615.KlingelnbergCycloPalloidSpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2615

        return self.__parent__._cast(_2615.KlingelnbergCycloPalloidSpiralBevelGear)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
        self: "CastSelf",
    ) -> "_2616.KlingelnbergCycloPalloidSpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2616

        return self.__parent__._cast(_2616.KlingelnbergCycloPalloidSpiralBevelGearSet)

    @property
    def planetary_gear_set(self: "CastSelf") -> "_2617.PlanetaryGearSet":
        from mastapy._private.system_model.part_model.gears import _2617

        return self.__parent__._cast(_2617.PlanetaryGearSet)

    @property
    def spiral_bevel_gear(self: "CastSelf") -> "_2618.SpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2618

        return self.__parent__._cast(_2618.SpiralBevelGear)

    @property
    def spiral_bevel_gear_set(self: "CastSelf") -> "_2619.SpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2619

        return self.__parent__._cast(_2619.SpiralBevelGearSet)

    @property
    def straight_bevel_diff_gear(self: "CastSelf") -> "_2620.StraightBevelDiffGear":
        from mastapy._private.system_model.part_model.gears import _2620

        return self.__parent__._cast(_2620.StraightBevelDiffGear)

    @property
    def straight_bevel_diff_gear_set(
        self: "CastSelf",
    ) -> "_2621.StraightBevelDiffGearSet":
        from mastapy._private.system_model.part_model.gears import _2621

        return self.__parent__._cast(_2621.StraightBevelDiffGearSet)

    @property
    def straight_bevel_gear(self: "CastSelf") -> "_2622.StraightBevelGear":
        from mastapy._private.system_model.part_model.gears import _2622

        return self.__parent__._cast(_2622.StraightBevelGear)

    @property
    def straight_bevel_gear_set(self: "CastSelf") -> "_2623.StraightBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2623

        return self.__parent__._cast(_2623.StraightBevelGearSet)

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
    def worm_gear_set(self: "CastSelf") -> "_2627.WormGearSet":
        from mastapy._private.system_model.part_model.gears import _2627

        return self.__parent__._cast(_2627.WormGearSet)

    @property
    def zerol_bevel_gear(self: "CastSelf") -> "_2628.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2628

        return self.__parent__._cast(_2628.ZerolBevelGear)

    @property
    def zerol_bevel_gear_set(self: "CastSelf") -> "_2629.ZerolBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2629

        return self.__parent__._cast(_2629.ZerolBevelGearSet)

    @property
    def cycloidal_assembly(self: "CastSelf") -> "_2643.CycloidalAssembly":
        from mastapy._private.system_model.part_model.cycloidal import _2643

        return self.__parent__._cast(_2643.CycloidalAssembly)

    @property
    def cycloidal_disc(self: "CastSelf") -> "_2644.CycloidalDisc":
        from mastapy._private.system_model.part_model.cycloidal import _2644

        return self.__parent__._cast(_2644.CycloidalDisc)

    @property
    def ring_pins(self: "CastSelf") -> "_2645.RingPins":
        from mastapy._private.system_model.part_model.cycloidal import _2645

        return self.__parent__._cast(_2645.RingPins)

    @property
    def belt_drive(self: "CastSelf") -> "_2652.BeltDrive":
        from mastapy._private.system_model.part_model.couplings import _2652

        return self.__parent__._cast(_2652.BeltDrive)

    @property
    def clutch(self: "CastSelf") -> "_2654.Clutch":
        from mastapy._private.system_model.part_model.couplings import _2654

        return self.__parent__._cast(_2654.Clutch)

    @property
    def clutch_half(self: "CastSelf") -> "_2655.ClutchHalf":
        from mastapy._private.system_model.part_model.couplings import _2655

        return self.__parent__._cast(_2655.ClutchHalf)

    @property
    def concept_coupling(self: "CastSelf") -> "_2657.ConceptCoupling":
        from mastapy._private.system_model.part_model.couplings import _2657

        return self.__parent__._cast(_2657.ConceptCoupling)

    @property
    def concept_coupling_half(self: "CastSelf") -> "_2658.ConceptCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2658

        return self.__parent__._cast(_2658.ConceptCouplingHalf)

    @property
    def coupling(self: "CastSelf") -> "_2660.Coupling":
        from mastapy._private.system_model.part_model.couplings import _2660

        return self.__parent__._cast(_2660.Coupling)

    @property
    def coupling_half(self: "CastSelf") -> "_2661.CouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2661

        return self.__parent__._cast(_2661.CouplingHalf)

    @property
    def cvt(self: "CastSelf") -> "_2663.CVT":
        from mastapy._private.system_model.part_model.couplings import _2663

        return self.__parent__._cast(_2663.CVT)

    @property
    def cvt_pulley(self: "CastSelf") -> "_2664.CVTPulley":
        from mastapy._private.system_model.part_model.couplings import _2664

        return self.__parent__._cast(_2664.CVTPulley)

    @property
    def part_to_part_shear_coupling(
        self: "CastSelf",
    ) -> "_2665.PartToPartShearCoupling":
        from mastapy._private.system_model.part_model.couplings import _2665

        return self.__parent__._cast(_2665.PartToPartShearCoupling)

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
    def rolling_ring_assembly(self: "CastSelf") -> "_2676.RollingRingAssembly":
        from mastapy._private.system_model.part_model.couplings import _2676

        return self.__parent__._cast(_2676.RollingRingAssembly)

    @property
    def shaft_hub_connection(self: "CastSelf") -> "_2677.ShaftHubConnection":
        from mastapy._private.system_model.part_model.couplings import _2677

        return self.__parent__._cast(_2677.ShaftHubConnection)

    @property
    def spring_damper(self: "CastSelf") -> "_2683.SpringDamper":
        from mastapy._private.system_model.part_model.couplings import _2683

        return self.__parent__._cast(_2683.SpringDamper)

    @property
    def spring_damper_half(self: "CastSelf") -> "_2684.SpringDamperHalf":
        from mastapy._private.system_model.part_model.couplings import _2684

        return self.__parent__._cast(_2684.SpringDamperHalf)

    @property
    def synchroniser(self: "CastSelf") -> "_2685.Synchroniser":
        from mastapy._private.system_model.part_model.couplings import _2685

        return self.__parent__._cast(_2685.Synchroniser)

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
    def torque_converter(self: "CastSelf") -> "_2690.TorqueConverter":
        from mastapy._private.system_model.part_model.couplings import _2690

        return self.__parent__._cast(_2690.TorqueConverter)

    @property
    def torque_converter_pump(self: "CastSelf") -> "_2691.TorqueConverterPump":
        from mastapy._private.system_model.part_model.couplings import _2691

        return self.__parent__._cast(_2691.TorqueConverterPump)

    @property
    def torque_converter_turbine(self: "CastSelf") -> "_2693.TorqueConverterTurbine":
        from mastapy._private.system_model.part_model.couplings import _2693

        return self.__parent__._cast(_2693.TorqueConverterTurbine)

    @property
    def part(self: "CastSelf") -> "Part":
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
class Part(_2272.DesignEntity):
    """Part

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def two_d_drawing(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TwoDDrawing")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def two_d_drawing_full_model(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TwoDDrawingFullModel")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def three_d_isometric_view(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThreeDIsometricView")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def three_d_view(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThreeDView")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def three_d_view_orientated_in_xy_plane_with_z_axis_pointing_into_the_screen(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThreeDViewOrientatedInXyPlaneWithZAxisPointingIntoTheScreen"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def three_d_view_orientated_in_xy_plane_with_z_axis_pointing_out_of_the_screen(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThreeDViewOrientatedInXyPlaneWithZAxisPointingOutOfTheScreen"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def three_d_view_orientated_in_xz_plane_with_y_axis_pointing_into_the_screen(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThreeDViewOrientatedInXzPlaneWithYAxisPointingIntoTheScreen"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def three_d_view_orientated_in_xz_plane_with_y_axis_pointing_out_of_the_screen(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThreeDViewOrientatedInXzPlaneWithYAxisPointingOutOfTheScreen"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def three_d_view_orientated_in_yz_plane_with_x_axis_pointing_into_the_screen(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThreeDViewOrientatedInYzPlaneWithXAxisPointingIntoTheScreen"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def three_d_view_orientated_in_yz_plane_with_x_axis_pointing_out_of_the_screen(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThreeDViewOrientatedInYzPlaneWithXAxisPointingOutOfTheScreen"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def drawing_number(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "DrawingNumber")

        if temp is None:
            return ""

        return temp

    @drawing_number.setter
    @enforce_parameter_types
    def drawing_number(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "DrawingNumber", str(value) if value is not None else ""
        )

    @property
    def editable_name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "EditableName")

        if temp is None:
            return ""

        return temp

    @editable_name.setter
    @enforce_parameter_types
    def editable_name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "EditableName", str(value) if value is not None else ""
        )

    @property
    def full_name_without_root_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FullNameWithoutRootName")

        if temp is None:
            return ""

        return temp

    @property
    def mass(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Mass")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @mass.setter
    @enforce_parameter_types
    def mass(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Mass", value)

    @property
    def unique_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UniqueName")

        if temp is None:
            return ""

        return temp

    @property
    def mass_properties_from_design(self: "Self") -> "_1577.MassProperties":
        """mastapy.math_utility.MassProperties

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MassPropertiesFromDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def mass_properties_from_design_including_planetary_duplicates(
        self: "Self",
    ) -> "_1577.MassProperties":
        """mastapy.math_utility.MassProperties

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MassPropertiesFromDesignIncludingPlanetaryDuplicates"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connections(self: "Self") -> "List[_2341.Connection]":
        """List[mastapy.system_model.connections_and_sockets.Connection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Connections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def local_connections(self: "Self") -> "List[_2341.Connection]":
        """List[mastapy.system_model.connections_and_sockets.Connection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LocalConnections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @enforce_parameter_types
    def connections_to(self: "Self", part: "Part") -> "List[_2341.Connection]":
        """List[mastapy.system_model.connections_and_sockets.Connection]

        Args:
            part (mastapy.system_model.part_model.Part)
        """
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(
                self.wrapped, "ConnectionsTo", part.wrapped if part else None
            )
        )

    @enforce_parameter_types
    def copy_to(self: "Self", container: "_2503.Assembly") -> "Part":
        """mastapy.system_model.part_model.Part

        Args:
            container (mastapy.system_model.part_model.Assembly)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "CopyTo", container.wrapped if container else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    def create_geometry_export_options(self: "Self") -> "_2311.GeometryExportOptions":
        """mastapy.system_model.import_export.GeometryExportOptions"""
        method_result = pythonnet_method_call(
            self.wrapped, "CreateGeometryExportOptions"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    def delete_connections(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "DeleteConnections")

    @property
    def cast_to(self: "Self") -> "_Cast_Part":
        """Cast to another type.

        Returns:
            _Cast_Part
        """
        return _Cast_Part(self)
