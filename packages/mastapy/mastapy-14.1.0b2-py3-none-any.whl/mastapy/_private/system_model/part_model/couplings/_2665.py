"""PartToPartShearCoupling"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model.couplings import _2660

_PART_TO_PART_SHEAR_COUPLING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "PartToPartShearCoupling"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2272
    from mastapy._private.system_model.connections_and_sockets.couplings import _2417
    from mastapy._private.system_model.part_model import _2504, _2540, _2549

    Self = TypeVar("Self", bound="PartToPartShearCoupling")
    CastSelf = TypeVar(
        "CastSelf", bound="PartToPartShearCoupling._Cast_PartToPartShearCoupling"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartToPartShearCoupling",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartToPartShearCoupling:
    """Special nested class for casting PartToPartShearCoupling to subclasses."""

    __parent__: "PartToPartShearCoupling"

    @property
    def coupling(self: "CastSelf") -> "_2660.Coupling":
        return self.__parent__._cast(_2660.Coupling)

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
    def part_to_part_shear_coupling(self: "CastSelf") -> "PartToPartShearCoupling":
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
class PartToPartShearCoupling(_2660.Coupling):
    """PartToPartShearCoupling

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_TO_PART_SHEAR_COUPLING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def part_to_part_shear_coupling_connection(
        self: "Self",
    ) -> "_2417.PartToPartShearCouplingConnection":
        """mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PartToPartShearCouplingConnection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PartToPartShearCoupling":
        """Cast to another type.

        Returns:
            _Cast_PartToPartShearCoupling
        """
        return _Cast_PartToPartShearCoupling(self)
