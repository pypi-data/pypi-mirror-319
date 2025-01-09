"""MouseButtonCombination"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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

_MOUSE_BUTTON_COMBINATION = python_net_import(
    "SMT.MastaAPI.Utility.KeyBindings", "MouseButtonCombination"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.utility.key_bindings import _1874

    Self = TypeVar("Self", bound="MouseButtonCombination")
    CastSelf = TypeVar(
        "CastSelf", bound="MouseButtonCombination._Cast_MouseButtonCombination"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MouseButtonCombination",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MouseButtonCombination:
    """Special nested class for casting MouseButtonCombination to subclasses."""

    __parent__: "MouseButtonCombination"

    @property
    def mouse_button_combination(self: "CastSelf") -> "MouseButtonCombination":
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
class MouseButtonCombination(_0.APIBase):
    """MouseButtonCombination

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOUSE_BUTTON_COMBINATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def combining_operation(self: "Self") -> "_1874.Combination":
        """mastapy.utility.key_bindings.Combination"""
        temp = pythonnet_property_get(self.wrapped, "CombiningOperation")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.KeyBindings.Combination"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility.key_bindings._1874", "Combination"
        )(value)

    @combining_operation.setter
    @enforce_parameter_types
    def combining_operation(self: "Self", value: "_1874.Combination") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Utility.KeyBindings.Combination"
        )
        pythonnet_property_set(self.wrapped, "CombiningOperation", value)

    @property
    def mouse_button_a(self: "Self") -> "System.Windows.Forms.MouseButtons":
        """System.Windows.Forms.MouseButtons"""
        temp = pythonnet_property_get(self.wrapped, "MouseButtonA")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "System.Windows.Forms.MouseButtons")

        if value is None:
            return None

        return constructor.new_from_mastapy("System.Windows.Forms.System", "Windows")(
            value
        )

    @mouse_button_a.setter
    @enforce_parameter_types
    def mouse_button_a(
        self: "Self", value: "System.Windows.Forms.MouseButtons"
    ) -> None:
        value = conversion.mp_to_pn_enum(value, "System.Windows.Forms.MouseButtons")
        pythonnet_property_set(self.wrapped, "MouseButtonA", value)

    @property
    def mouse_button_b(self: "Self") -> "System.Windows.Forms.MouseButtons":
        """System.Windows.Forms.MouseButtons"""
        temp = pythonnet_property_get(self.wrapped, "MouseButtonB")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "System.Windows.Forms.MouseButtons")

        if value is None:
            return None

        return constructor.new_from_mastapy("System.Windows.Forms.System", "Windows")(
            value
        )

    @mouse_button_b.setter
    @enforce_parameter_types
    def mouse_button_b(
        self: "Self", value: "System.Windows.Forms.MouseButtons"
    ) -> None:
        value = conversion.mp_to_pn_enum(value, "System.Windows.Forms.MouseButtons")
        pythonnet_property_set(self.wrapped, "MouseButtonB", value)

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
    def cast_to(self: "Self") -> "_Cast_MouseButtonCombination":
        """Cast to another type.

        Returns:
            _Cast_MouseButtonCombination
        """
        return _Cast_MouseButtonCombination(self)
