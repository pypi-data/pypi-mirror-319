"""DesignEntity"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_DESIGN_ENTITY = python_net_import("SMT.MastaAPI.SystemModel", "DesignEntity")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model import _2269
    from mastapy._private.system_model.connections_and_sockets import (
        _2334,
        _2337,
        _2338,
        _2341,
        _2342,
        _2350,
        _2356,
        _2361,
        _2364,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import (
        _2411,
        _2413,
        _2415,
        _2417,
        _2419,
        _2421,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2404,
        _2407,
        _2410,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2368,
        _2370,
        _2372,
        _2374,
        _2376,
        _2378,
        _2380,
        _2382,
        _2384,
        _2387,
        _2388,
        _2389,
        _2392,
        _2394,
        _2396,
        _2398,
        _2400,
    )
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
        _2540,
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
    from mastapy._private.utility.model_validation import _1855, _1856
    from mastapy._private.utility.scripting import _1803

    Self = TypeVar("Self", bound="DesignEntity")
    CastSelf = TypeVar("CastSelf", bound="DesignEntity._Cast_DesignEntity")


__docformat__ = "restructuredtext en"
__all__ = ("DesignEntity",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DesignEntity:
    """Special nested class for casting DesignEntity to subclasses."""

    __parent__: "DesignEntity"

    @property
    def abstract_shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2334.AbstractShaftToMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2334

        return self.__parent__._cast(_2334.AbstractShaftToMountableComponentConnection)

    @property
    def belt_connection(self: "CastSelf") -> "_2337.BeltConnection":
        from mastapy._private.system_model.connections_and_sockets import _2337

        return self.__parent__._cast(_2337.BeltConnection)

    @property
    def coaxial_connection(self: "CastSelf") -> "_2338.CoaxialConnection":
        from mastapy._private.system_model.connections_and_sockets import _2338

        return self.__parent__._cast(_2338.CoaxialConnection)

    @property
    def connection(self: "CastSelf") -> "_2341.Connection":
        from mastapy._private.system_model.connections_and_sockets import _2341

        return self.__parent__._cast(_2341.Connection)

    @property
    def cvt_belt_connection(self: "CastSelf") -> "_2342.CVTBeltConnection":
        from mastapy._private.system_model.connections_and_sockets import _2342

        return self.__parent__._cast(_2342.CVTBeltConnection)

    @property
    def inter_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2350.InterMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2350

        return self.__parent__._cast(_2350.InterMountableComponentConnection)

    @property
    def planetary_connection(self: "CastSelf") -> "_2356.PlanetaryConnection":
        from mastapy._private.system_model.connections_and_sockets import _2356

        return self.__parent__._cast(_2356.PlanetaryConnection)

    @property
    def rolling_ring_connection(self: "CastSelf") -> "_2361.RollingRingConnection":
        from mastapy._private.system_model.connections_and_sockets import _2361

        return self.__parent__._cast(_2361.RollingRingConnection)

    @property
    def shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2364.ShaftToMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2364

        return self.__parent__._cast(_2364.ShaftToMountableComponentConnection)

    @property
    def agma_gleason_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2368.AGMAGleasonConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2368

        return self.__parent__._cast(_2368.AGMAGleasonConicalGearMesh)

    @property
    def bevel_differential_gear_mesh(
        self: "CastSelf",
    ) -> "_2370.BevelDifferentialGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2370

        return self.__parent__._cast(_2370.BevelDifferentialGearMesh)

    @property
    def bevel_gear_mesh(self: "CastSelf") -> "_2372.BevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2372

        return self.__parent__._cast(_2372.BevelGearMesh)

    @property
    def concept_gear_mesh(self: "CastSelf") -> "_2374.ConceptGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2374

        return self.__parent__._cast(_2374.ConceptGearMesh)

    @property
    def conical_gear_mesh(self: "CastSelf") -> "_2376.ConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2376

        return self.__parent__._cast(_2376.ConicalGearMesh)

    @property
    def cylindrical_gear_mesh(self: "CastSelf") -> "_2378.CylindricalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2378

        return self.__parent__._cast(_2378.CylindricalGearMesh)

    @property
    def face_gear_mesh(self: "CastSelf") -> "_2380.FaceGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2380

        return self.__parent__._cast(_2380.FaceGearMesh)

    @property
    def gear_mesh(self: "CastSelf") -> "_2382.GearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2382

        return self.__parent__._cast(_2382.GearMesh)

    @property
    def hypoid_gear_mesh(self: "CastSelf") -> "_2384.HypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2384

        return self.__parent__._cast(_2384.HypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2387.KlingelnbergCycloPalloidConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2387

        return self.__parent__._cast(_2387.KlingelnbergCycloPalloidConicalGearMesh)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh(
        self: "CastSelf",
    ) -> "_2388.KlingelnbergCycloPalloidHypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2388

        return self.__parent__._cast(_2388.KlingelnbergCycloPalloidHypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(
        self: "CastSelf",
    ) -> "_2389.KlingelnbergCycloPalloidSpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2389

        return self.__parent__._cast(_2389.KlingelnbergCycloPalloidSpiralBevelGearMesh)

    @property
    def spiral_bevel_gear_mesh(self: "CastSelf") -> "_2392.SpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2392

        return self.__parent__._cast(_2392.SpiralBevelGearMesh)

    @property
    def straight_bevel_diff_gear_mesh(
        self: "CastSelf",
    ) -> "_2394.StraightBevelDiffGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2394

        return self.__parent__._cast(_2394.StraightBevelDiffGearMesh)

    @property
    def straight_bevel_gear_mesh(self: "CastSelf") -> "_2396.StraightBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2396

        return self.__parent__._cast(_2396.StraightBevelGearMesh)

    @property
    def worm_gear_mesh(self: "CastSelf") -> "_2398.WormGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2398

        return self.__parent__._cast(_2398.WormGearMesh)

    @property
    def zerol_bevel_gear_mesh(self: "CastSelf") -> "_2400.ZerolBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2400

        return self.__parent__._cast(_2400.ZerolBevelGearMesh)

    @property
    def cycloidal_disc_central_bearing_connection(
        self: "CastSelf",
    ) -> "_2404.CycloidalDiscCentralBearingConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2404,
        )

        return self.__parent__._cast(_2404.CycloidalDiscCentralBearingConnection)

    @property
    def cycloidal_disc_planetary_bearing_connection(
        self: "CastSelf",
    ) -> "_2407.CycloidalDiscPlanetaryBearingConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2407,
        )

        return self.__parent__._cast(_2407.CycloidalDiscPlanetaryBearingConnection)

    @property
    def ring_pins_to_disc_connection(
        self: "CastSelf",
    ) -> "_2410.RingPinsToDiscConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2410,
        )

        return self.__parent__._cast(_2410.RingPinsToDiscConnection)

    @property
    def clutch_connection(self: "CastSelf") -> "_2411.ClutchConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2411,
        )

        return self.__parent__._cast(_2411.ClutchConnection)

    @property
    def concept_coupling_connection(
        self: "CastSelf",
    ) -> "_2413.ConceptCouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2413,
        )

        return self.__parent__._cast(_2413.ConceptCouplingConnection)

    @property
    def coupling_connection(self: "CastSelf") -> "_2415.CouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2415,
        )

        return self.__parent__._cast(_2415.CouplingConnection)

    @property
    def part_to_part_shear_coupling_connection(
        self: "CastSelf",
    ) -> "_2417.PartToPartShearCouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2417,
        )

        return self.__parent__._cast(_2417.PartToPartShearCouplingConnection)

    @property
    def spring_damper_connection(self: "CastSelf") -> "_2419.SpringDamperConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2419,
        )

        return self.__parent__._cast(_2419.SpringDamperConnection)

    @property
    def torque_converter_connection(
        self: "CastSelf",
    ) -> "_2421.TorqueConverterConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2421,
        )

        return self.__parent__._cast(_2421.TorqueConverterConnection)

    @property
    def assembly(self: "CastSelf") -> "_2503.Assembly":
        from mastapy._private.system_model.part_model import _2503

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
    def part(self: "CastSelf") -> "_2540.Part":
        from mastapy._private.system_model.part_model import _2540

        return self.__parent__._cast(_2540.Part)

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
    def design_entity(self: "CastSelf") -> "DesignEntity":
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
class DesignEntity(_0.APIBase):
    """DesignEntity

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DESIGN_ENTITY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def comment(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Comment")

        if temp is None:
            return ""

        return temp

    @comment.setter
    @enforce_parameter_types
    def comment(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Comment", str(value) if value is not None else ""
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
    def id(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ID")

        if temp is None:
            return ""

        return temp

    @property
    def icon(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Icon")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def small_icon(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SmallIcon")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

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
    def design_properties(self: "Self") -> "_2269.Design":
        """mastapy.system_model.Design

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignProperties")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def all_design_entities(self: "Self") -> "List[DesignEntity]":
        """List[mastapy.system_model.DesignEntity]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllDesignEntities")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def all_status_errors(self: "Self") -> "List[_1856.StatusItem]":
        """List[mastapy.utility.model_validation.StatusItem]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllStatusErrors")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def status(self: "Self") -> "_1855.Status":
        """mastapy.utility.model_validation.Status

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Status")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def user_specified_data(self: "Self") -> "_1803.UserSpecifiedData":
        """mastapy.utility.scripting.UserSpecifiedData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UserSpecifiedData")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    def delete(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Delete")

    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputDefaultReportTo", file_path if file_path else ""
        )

    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportTo", file_path if file_path else ""
        )

    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportAsTextTo", file_path if file_path else ""
        )

    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_DesignEntity":
        """Cast to another type.

        Returns:
            _Cast_DesignEntity
        """
        return _Cast_DesignEntity(self)
