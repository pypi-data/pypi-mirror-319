"""AGMAGleasonConicalGear"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model.gears import _2598

_AGMA_GLEASON_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGear"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2272
    from mastapy._private.system_model.part_model import _2514, _2536, _2540
    from mastapy._private.system_model.part_model.gears import (
        _2590,
        _2592,
        _2593,
        _2594,
        _2605,
        _2609,
        _2618,
        _2620,
        _2622,
        _2624,
        _2625,
        _2628,
    )

    Self = TypeVar("Self", bound="AGMAGleasonConicalGear")
    CastSelf = TypeVar(
        "CastSelf", bound="AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGear:
    """Special nested class for casting AGMAGleasonConicalGear to subclasses."""

    __parent__: "AGMAGleasonConicalGear"

    @property
    def conical_gear(self: "CastSelf") -> "_2598.ConicalGear":
        return self.__parent__._cast(_2598.ConicalGear)

    @property
    def gear(self: "CastSelf") -> "_2605.Gear":
        from mastapy._private.system_model.part_model.gears import _2605

        return self.__parent__._cast(_2605.Gear)

    @property
    def mountable_component(self: "CastSelf") -> "_2536.MountableComponent":
        from mastapy._private.system_model.part_model import _2536

        return self.__parent__._cast(_2536.MountableComponent)

    @property
    def component(self: "CastSelf") -> "_2514.Component":
        from mastapy._private.system_model.part_model import _2514

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
    def hypoid_gear(self: "CastSelf") -> "_2609.HypoidGear":
        from mastapy._private.system_model.part_model.gears import _2609

        return self.__parent__._cast(_2609.HypoidGear)

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
    def zerol_bevel_gear(self: "CastSelf") -> "_2628.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2628

        return self.__parent__._cast(_2628.ZerolBevelGear)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "AGMAGleasonConicalGear":
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
class AGMAGleasonConicalGear(_2598.ConicalGear):
    """AGMAGleasonConicalGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AGMAGleasonConicalGear":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGear
        """
        return _Cast_AGMAGleasonConicalGear(self)
