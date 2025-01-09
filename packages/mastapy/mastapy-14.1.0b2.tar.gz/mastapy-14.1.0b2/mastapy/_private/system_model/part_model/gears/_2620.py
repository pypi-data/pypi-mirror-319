"""StraightBevelDiffGear"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model.gears import _2594

_STRAIGHT_BEVEL_DIFF_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelDiffGear"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.straight_bevel_diff import _997
    from mastapy._private.system_model import _2272
    from mastapy._private.system_model.part_model import _2514, _2536, _2540
    from mastapy._private.system_model.part_model.gears import (
        _2588,
        _2598,
        _2605,
        _2624,
        _2625,
    )

    Self = TypeVar("Self", bound="StraightBevelDiffGear")
    CastSelf = TypeVar(
        "CastSelf", bound="StraightBevelDiffGear._Cast_StraightBevelDiffGear"
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelDiffGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelDiffGear:
    """Special nested class for casting StraightBevelDiffGear to subclasses."""

    __parent__: "StraightBevelDiffGear"

    @property
    def bevel_gear(self: "CastSelf") -> "_2594.BevelGear":
        return self.__parent__._cast(_2594.BevelGear)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2588.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2588

        return self.__parent__._cast(_2588.AGMAGleasonConicalGear)

    @property
    def conical_gear(self: "CastSelf") -> "_2598.ConicalGear":
        from mastapy._private.system_model.part_model.gears import _2598

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
    def straight_bevel_planet_gear(self: "CastSelf") -> "_2624.StraightBevelPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2624

        return self.__parent__._cast(_2624.StraightBevelPlanetGear)

    @property
    def straight_bevel_sun_gear(self: "CastSelf") -> "_2625.StraightBevelSunGear":
        from mastapy._private.system_model.part_model.gears import _2625

        return self.__parent__._cast(_2625.StraightBevelSunGear)

    @property
    def straight_bevel_diff_gear(self: "CastSelf") -> "StraightBevelDiffGear":
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
class StraightBevelDiffGear(_2594.BevelGear):
    """StraightBevelDiffGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_DIFF_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def bevel_gear_design(self: "Self") -> "_997.StraightBevelDiffGearDesign":
        """mastapy.gears.gear_designs.straight_bevel_diff.StraightBevelDiffGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def straight_bevel_diff_gear_design(
        self: "Self",
    ) -> "_997.StraightBevelDiffGearDesign":
        """mastapy.gears.gear_designs.straight_bevel_diff.StraightBevelDiffGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StraightBevelDiffGearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelDiffGear":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelDiffGear
        """
        return _Cast_StraightBevelDiffGear(self)
