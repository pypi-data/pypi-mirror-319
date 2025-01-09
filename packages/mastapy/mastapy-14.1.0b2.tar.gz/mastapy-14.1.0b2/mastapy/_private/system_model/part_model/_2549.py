"""SpecialisedAssembly"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model import _2504

_SPECIALISED_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "SpecialisedAssembly"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2272
    from mastapy._private.system_model.part_model import _2513, _2524, _2535, _2540
    from mastapy._private.system_model.part_model.couplings import (
        _2652,
        _2654,
        _2657,
        _2660,
        _2663,
        _2665,
        _2676,
        _2683,
        _2685,
        _2690,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2643
    from mastapy._private.system_model.part_model.gears import (
        _2589,
        _2591,
        _2595,
        _2597,
        _2599,
        _2601,
        _2604,
        _2607,
        _2610,
        _2612,
        _2614,
        _2616,
        _2617,
        _2619,
        _2621,
        _2623,
        _2627,
        _2629,
    )

    Self = TypeVar("Self", bound="SpecialisedAssembly")
    CastSelf = TypeVar(
        "CastSelf", bound="SpecialisedAssembly._Cast_SpecialisedAssembly"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssembly",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpecialisedAssembly:
    """Special nested class for casting SpecialisedAssembly to subclasses."""

    __parent__: "SpecialisedAssembly"

    @property
    def abstract_assembly(self: "CastSelf") -> "_2504.AbstractAssembly":
        return self.__parent__._cast(_2504.AbstractAssembly)

    @property
    def part(self: "CastSelf") -> "_2540.Part":
        from mastapy._private.system_model.part_model import _2540

        return self.__parent__._cast(_2540.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2272.DesignEntity":
        from mastapy._private.system_model import _2272

        return self.__parent__._cast(_2272.DesignEntity)

    @property
    def bolted_joint(self: "CastSelf") -> "_2513.BoltedJoint":
        from mastapy._private.system_model.part_model import _2513

        return self.__parent__._cast(_2513.BoltedJoint)

    @property
    def flexible_pin_assembly(self: "CastSelf") -> "_2524.FlexiblePinAssembly":
        from mastapy._private.system_model.part_model import _2524

        return self.__parent__._cast(_2524.FlexiblePinAssembly)

    @property
    def microphone_array(self: "CastSelf") -> "_2535.MicrophoneArray":
        from mastapy._private.system_model.part_model import _2535

        return self.__parent__._cast(_2535.MicrophoneArray)

    @property
    def agma_gleason_conical_gear_set(
        self: "CastSelf",
    ) -> "_2589.AGMAGleasonConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2589

        return self.__parent__._cast(_2589.AGMAGleasonConicalGearSet)

    @property
    def bevel_differential_gear_set(
        self: "CastSelf",
    ) -> "_2591.BevelDifferentialGearSet":
        from mastapy._private.system_model.part_model.gears import _2591

        return self.__parent__._cast(_2591.BevelDifferentialGearSet)

    @property
    def bevel_gear_set(self: "CastSelf") -> "_2595.BevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2595

        return self.__parent__._cast(_2595.BevelGearSet)

    @property
    def concept_gear_set(self: "CastSelf") -> "_2597.ConceptGearSet":
        from mastapy._private.system_model.part_model.gears import _2597

        return self.__parent__._cast(_2597.ConceptGearSet)

    @property
    def conical_gear_set(self: "CastSelf") -> "_2599.ConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2599

        return self.__parent__._cast(_2599.ConicalGearSet)

    @property
    def cylindrical_gear_set(self: "CastSelf") -> "_2601.CylindricalGearSet":
        from mastapy._private.system_model.part_model.gears import _2601

        return self.__parent__._cast(_2601.CylindricalGearSet)

    @property
    def face_gear_set(self: "CastSelf") -> "_2604.FaceGearSet":
        from mastapy._private.system_model.part_model.gears import _2604

        return self.__parent__._cast(_2604.FaceGearSet)

    @property
    def gear_set(self: "CastSelf") -> "_2607.GearSet":
        from mastapy._private.system_model.part_model.gears import _2607

        return self.__parent__._cast(_2607.GearSet)

    @property
    def hypoid_gear_set(self: "CastSelf") -> "_2610.HypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2610

        return self.__parent__._cast(_2610.HypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set(
        self: "CastSelf",
    ) -> "_2612.KlingelnbergCycloPalloidConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2612

        return self.__parent__._cast(_2612.KlingelnbergCycloPalloidConicalGearSet)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "CastSelf",
    ) -> "_2614.KlingelnbergCycloPalloidHypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2614

        return self.__parent__._cast(_2614.KlingelnbergCycloPalloidHypoidGearSet)

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
    def spiral_bevel_gear_set(self: "CastSelf") -> "_2619.SpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2619

        return self.__parent__._cast(_2619.SpiralBevelGearSet)

    @property
    def straight_bevel_diff_gear_set(
        self: "CastSelf",
    ) -> "_2621.StraightBevelDiffGearSet":
        from mastapy._private.system_model.part_model.gears import _2621

        return self.__parent__._cast(_2621.StraightBevelDiffGearSet)

    @property
    def straight_bevel_gear_set(self: "CastSelf") -> "_2623.StraightBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2623

        return self.__parent__._cast(_2623.StraightBevelGearSet)

    @property
    def worm_gear_set(self: "CastSelf") -> "_2627.WormGearSet":
        from mastapy._private.system_model.part_model.gears import _2627

        return self.__parent__._cast(_2627.WormGearSet)

    @property
    def zerol_bevel_gear_set(self: "CastSelf") -> "_2629.ZerolBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2629

        return self.__parent__._cast(_2629.ZerolBevelGearSet)

    @property
    def cycloidal_assembly(self: "CastSelf") -> "_2643.CycloidalAssembly":
        from mastapy._private.system_model.part_model.cycloidal import _2643

        return self.__parent__._cast(_2643.CycloidalAssembly)

    @property
    def belt_drive(self: "CastSelf") -> "_2652.BeltDrive":
        from mastapy._private.system_model.part_model.couplings import _2652

        return self.__parent__._cast(_2652.BeltDrive)

    @property
    def clutch(self: "CastSelf") -> "_2654.Clutch":
        from mastapy._private.system_model.part_model.couplings import _2654

        return self.__parent__._cast(_2654.Clutch)

    @property
    def concept_coupling(self: "CastSelf") -> "_2657.ConceptCoupling":
        from mastapy._private.system_model.part_model.couplings import _2657

        return self.__parent__._cast(_2657.ConceptCoupling)

    @property
    def coupling(self: "CastSelf") -> "_2660.Coupling":
        from mastapy._private.system_model.part_model.couplings import _2660

        return self.__parent__._cast(_2660.Coupling)

    @property
    def cvt(self: "CastSelf") -> "_2663.CVT":
        from mastapy._private.system_model.part_model.couplings import _2663

        return self.__parent__._cast(_2663.CVT)

    @property
    def part_to_part_shear_coupling(
        self: "CastSelf",
    ) -> "_2665.PartToPartShearCoupling":
        from mastapy._private.system_model.part_model.couplings import _2665

        return self.__parent__._cast(_2665.PartToPartShearCoupling)

    @property
    def rolling_ring_assembly(self: "CastSelf") -> "_2676.RollingRingAssembly":
        from mastapy._private.system_model.part_model.couplings import _2676

        return self.__parent__._cast(_2676.RollingRingAssembly)

    @property
    def spring_damper(self: "CastSelf") -> "_2683.SpringDamper":
        from mastapy._private.system_model.part_model.couplings import _2683

        return self.__parent__._cast(_2683.SpringDamper)

    @property
    def synchroniser(self: "CastSelf") -> "_2685.Synchroniser":
        from mastapy._private.system_model.part_model.couplings import _2685

        return self.__parent__._cast(_2685.Synchroniser)

    @property
    def torque_converter(self: "CastSelf") -> "_2690.TorqueConverter":
        from mastapy._private.system_model.part_model.couplings import _2690

        return self.__parent__._cast(_2690.TorqueConverter)

    @property
    def specialised_assembly(self: "CastSelf") -> "SpecialisedAssembly":
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
class SpecialisedAssembly(_2504.AbstractAssembly):
    """SpecialisedAssembly

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPECIALISED_ASSEMBLY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_SpecialisedAssembly":
        """Cast to another type.

        Returns:
            _Cast_SpecialisedAssembly
        """
        return _Cast_SpecialisedAssembly(self)
