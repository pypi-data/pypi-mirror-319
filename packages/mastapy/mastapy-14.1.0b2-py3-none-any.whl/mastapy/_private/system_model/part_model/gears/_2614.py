"""KlingelnbergCycloPalloidHypoidGearSet"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model.gears import _2612

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidHypoidGearSet"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1011
    from mastapy._private.system_model import _2272
    from mastapy._private.system_model.connections_and_sockets.gears import _2388
    from mastapy._private.system_model.part_model import _2504, _2540, _2549
    from mastapy._private.system_model.part_model.gears import _2599, _2607, _2613

    Self = TypeVar("Self", bound="KlingelnbergCycloPalloidHypoidGearSet")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidHypoidGearSet._Cast_KlingelnbergCycloPalloidHypoidGearSet",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidHypoidGearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidHypoidGearSet:
    """Special nested class for casting KlingelnbergCycloPalloidHypoidGearSet to subclasses."""

    __parent__: "KlingelnbergCycloPalloidHypoidGearSet"

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set(
        self: "CastSelf",
    ) -> "_2612.KlingelnbergCycloPalloidConicalGearSet":
        return self.__parent__._cast(_2612.KlingelnbergCycloPalloidConicalGearSet)

    @property
    def conical_gear_set(self: "CastSelf") -> "_2599.ConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2599

        return self.__parent__._cast(_2599.ConicalGearSet)

    @property
    def gear_set(self: "CastSelf") -> "_2607.GearSet":
        from mastapy._private.system_model.part_model.gears import _2607

        return self.__parent__._cast(_2607.GearSet)

    @property
    def specialised_assembly(self: "CastSelf") -> "_2549.SpecialisedAssembly":
        from mastapy._private.system_model.part_model import _2549

        return self.__parent__._cast(_2549.SpecialisedAssembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2504.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2504

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
    def klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidHypoidGearSet":
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
class KlingelnbergCycloPalloidHypoidGearSet(
    _2612.KlingelnbergCycloPalloidConicalGearSet
):
    """KlingelnbergCycloPalloidHypoidGearSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def klingelnberg_conical_gear_set_design(
        self: "Self",
    ) -> "_1011.KlingelnbergCycloPalloidHypoidGearSetDesign":
        """mastapy.gears.gear_designs.klingelnberg_hypoid.KlingelnbergCycloPalloidHypoidGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "KlingelnbergConicalGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_design(
        self: "Self",
    ) -> "_1011.KlingelnbergCycloPalloidHypoidGearSetDesign":
        """mastapy.gears.gear_designs.klingelnberg_hypoid.KlingelnbergCycloPalloidHypoidGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidHypoidGearSetDesign"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears(
        self: "Self",
    ) -> "List[_2613.KlingelnbergCycloPalloidHypoidGear]":
        """List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidHypoidGears"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes(
        self: "Self",
    ) -> "List[_2388.KlingelnbergCycloPalloidHypoidGearMesh]":
        """List[mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidHypoidMeshes"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_KlingelnbergCycloPalloidHypoidGearSet":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidHypoidGearSet
        """
        return _Cast_KlingelnbergCycloPalloidHypoidGearSet(self)
