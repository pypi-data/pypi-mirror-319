"""Bolt"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model import _2514

_BOLT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Bolt")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bolts import _1541
    from mastapy._private.system_model import _2272
    from mastapy._private.system_model.part_model import _2513, _2540

    Self = TypeVar("Self", bound="Bolt")
    CastSelf = TypeVar("CastSelf", bound="Bolt._Cast_Bolt")


__docformat__ = "restructuredtext en"
__all__ = ("Bolt",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Bolt:
    """Special nested class for casting Bolt to subclasses."""

    __parent__: "Bolt"

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
    def bolt(self: "CastSelf") -> "Bolt":
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
class Bolt(_2514.Component):
    """Bolt

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BOLT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def bolted_joint(self: "Self") -> "_2513.BoltedJoint":
        """mastapy.system_model.part_model.BoltedJoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BoltedJoint")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def loaded_bolt(self: "Self") -> "_1541.LoadedBolt":
        """mastapy.bolts.LoadedBolt

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadedBolt")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_Bolt":
        """Cast to another type.

        Returns:
            _Cast_Bolt
        """
        return _Cast_Bolt(self)
