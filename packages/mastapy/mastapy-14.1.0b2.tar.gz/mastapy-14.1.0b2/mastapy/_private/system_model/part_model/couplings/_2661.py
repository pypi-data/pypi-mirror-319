"""CouplingHalf"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2536

_COUPLING_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "CouplingHalf"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.system_model import _2272
    from mastapy._private.system_model.part_model import _2514, _2540
    from mastapy._private.system_model.part_model.couplings import (
        _2655,
        _2658,
        _2664,
        _2666,
        _2668,
        _2675,
        _2684,
        _2687,
        _2688,
        _2689,
        _2691,
        _2693,
    )

    Self = TypeVar("Self", bound="CouplingHalf")
    CastSelf = TypeVar("CastSelf", bound="CouplingHalf._Cast_CouplingHalf")


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHalf",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingHalf:
    """Special nested class for casting CouplingHalf to subclasses."""

    __parent__: "CouplingHalf"

    @property
    def mountable_component(self: "CastSelf") -> "_2536.MountableComponent":
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
    def clutch_half(self: "CastSelf") -> "_2655.ClutchHalf":
        from mastapy._private.system_model.part_model.couplings import _2655

        return self.__parent__._cast(_2655.ClutchHalf)

    @property
    def concept_coupling_half(self: "CastSelf") -> "_2658.ConceptCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2658

        return self.__parent__._cast(_2658.ConceptCouplingHalf)

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
    def coupling_half(self: "CastSelf") -> "CouplingHalf":
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
class CouplingHalf(_2536.MountableComponent):
    """CouplingHalf

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_HALF

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def bore(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Bore")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @bore.setter
    @enforce_parameter_types
    def bore(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Bore", value)

    @property
    def diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Diameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @diameter.setter
    @enforce_parameter_types
    def diameter(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Diameter", value)

    @property
    def width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0.0

        return temp

    @width.setter
    @enforce_parameter_types
    def width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingHalf":
        """Cast to another type.

        Returns:
            _Cast_CouplingHalf
        """
        return _Cast_CouplingHalf(self)
