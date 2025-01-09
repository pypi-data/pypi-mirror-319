"""CustomReportNameableItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.report import _1825

_CUSTOM_REPORT_NAMEABLE_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportNameableItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2014, _2015, _2018, _2026
    from mastapy._private.gears.gear_designs.cylindrical import _1073
    from mastapy._private.shafts import _20
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
        _4825,
        _4829,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4490,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
        _2929,
    )
    from mastapy._private.utility.report import (
        _1804,
        _1812,
        _1813,
        _1814,
        _1815,
        _1817,
        _1818,
        _1822,
        _1824,
        _1831,
        _1832,
        _1834,
        _1836,
        _1839,
        _1841,
        _1842,
        _1844,
    )
    from mastapy._private.utility_gui.charts import _1921, _1922

    Self = TypeVar("Self", bound="CustomReportNameableItem")
    CastSelf = TypeVar(
        "CastSelf", bound="CustomReportNameableItem._Cast_CustomReportNameableItem"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportNameableItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportNameableItem:
    """Special nested class for casting CustomReportNameableItem to subclasses."""

    __parent__: "CustomReportNameableItem"

    @property
    def custom_report_item(self: "CastSelf") -> "_1825.CustomReportItem":
        return self.__parent__._cast(_1825.CustomReportItem)

    @property
    def shaft_damage_results_table_and_chart(
        self: "CastSelf",
    ) -> "_20.ShaftDamageResultsTableAndChart":
        from mastapy._private.shafts import _20

        return self.__parent__._cast(_20.ShaftDamageResultsTableAndChart)

    @property
    def cylindrical_gear_table_with_mg_charts(
        self: "CastSelf",
    ) -> "_1073.CylindricalGearTableWithMGCharts":
        from mastapy._private.gears.gear_designs.cylindrical import _1073

        return self.__parent__._cast(_1073.CylindricalGearTableWithMGCharts)

    @property
    def ad_hoc_custom_table(self: "CastSelf") -> "_1804.AdHocCustomTable":
        from mastapy._private.utility.report import _1804

        return self.__parent__._cast(_1804.AdHocCustomTable)

    @property
    def custom_chart(self: "CastSelf") -> "_1812.CustomChart":
        from mastapy._private.utility.report import _1812

        return self.__parent__._cast(_1812.CustomChart)

    @property
    def custom_drawing(self: "CastSelf") -> "_1813.CustomDrawing":
        from mastapy._private.utility.report import _1813

        return self.__parent__._cast(_1813.CustomDrawing)

    @property
    def custom_graphic(self: "CastSelf") -> "_1814.CustomGraphic":
        from mastapy._private.utility.report import _1814

        return self.__parent__._cast(_1814.CustomGraphic)

    @property
    def custom_image(self: "CastSelf") -> "_1815.CustomImage":
        from mastapy._private.utility.report import _1815

        return self.__parent__._cast(_1815.CustomImage)

    @property
    def custom_report_cad_drawing(self: "CastSelf") -> "_1817.CustomReportCadDrawing":
        from mastapy._private.utility.report import _1817

        return self.__parent__._cast(_1817.CustomReportCadDrawing)

    @property
    def custom_report_chart(self: "CastSelf") -> "_1818.CustomReportChart":
        from mastapy._private.utility.report import _1818

        return self.__parent__._cast(_1818.CustomReportChart)

    @property
    def custom_report_definition_item(
        self: "CastSelf",
    ) -> "_1822.CustomReportDefinitionItem":
        from mastapy._private.utility.report import _1822

        return self.__parent__._cast(_1822.CustomReportDefinitionItem)

    @property
    def custom_report_html_item(self: "CastSelf") -> "_1824.CustomReportHtmlItem":
        from mastapy._private.utility.report import _1824

        return self.__parent__._cast(_1824.CustomReportHtmlItem)

    @property
    def custom_report_multi_property_item(
        self: "CastSelf",
    ) -> "_1831.CustomReportMultiPropertyItem":
        from mastapy._private.utility.report import _1831

        return self.__parent__._cast(_1831.CustomReportMultiPropertyItem)

    @property
    def custom_report_multi_property_item_base(
        self: "CastSelf",
    ) -> "_1832.CustomReportMultiPropertyItemBase":
        from mastapy._private.utility.report import _1832

        return self.__parent__._cast(_1832.CustomReportMultiPropertyItemBase)

    @property
    def custom_report_named_item(self: "CastSelf") -> "_1834.CustomReportNamedItem":
        from mastapy._private.utility.report import _1834

        return self.__parent__._cast(_1834.CustomReportNamedItem)

    @property
    def custom_report_status_item(self: "CastSelf") -> "_1836.CustomReportStatusItem":
        from mastapy._private.utility.report import _1836

        return self.__parent__._cast(_1836.CustomReportStatusItem)

    @property
    def custom_report_text(self: "CastSelf") -> "_1839.CustomReportText":
        from mastapy._private.utility.report import _1839

        return self.__parent__._cast(_1839.CustomReportText)

    @property
    def custom_sub_report(self: "CastSelf") -> "_1841.CustomSubReport":
        from mastapy._private.utility.report import _1841

        return self.__parent__._cast(_1841.CustomSubReport)

    @property
    def custom_table(self: "CastSelf") -> "_1842.CustomTable":
        from mastapy._private.utility.report import _1842

        return self.__parent__._cast(_1842.CustomTable)

    @property
    def dynamic_custom_report_item(self: "CastSelf") -> "_1844.DynamicCustomReportItem":
        from mastapy._private.utility.report import _1844

        return self.__parent__._cast(_1844.DynamicCustomReportItem)

    @property
    def custom_line_chart(self: "CastSelf") -> "_1921.CustomLineChart":
        from mastapy._private.utility_gui.charts import _1921

        return self.__parent__._cast(_1921.CustomLineChart)

    @property
    def custom_table_and_chart(self: "CastSelf") -> "_1922.CustomTableAndChart":
        from mastapy._private.utility_gui.charts import _1922

        return self.__parent__._cast(_1922.CustomTableAndChart)

    @property
    def loaded_ball_element_chart_reporter(
        self: "CastSelf",
    ) -> "_2014.LoadedBallElementChartReporter":
        from mastapy._private.bearings.bearing_results import _2014

        return self.__parent__._cast(_2014.LoadedBallElementChartReporter)

    @property
    def loaded_bearing_chart_reporter(
        self: "CastSelf",
    ) -> "_2015.LoadedBearingChartReporter":
        from mastapy._private.bearings.bearing_results import _2015

        return self.__parent__._cast(_2015.LoadedBearingChartReporter)

    @property
    def loaded_bearing_temperature_chart(
        self: "CastSelf",
    ) -> "_2018.LoadedBearingTemperatureChart":
        from mastapy._private.bearings.bearing_results import _2018

        return self.__parent__._cast(_2018.LoadedBearingTemperatureChart)

    @property
    def loaded_roller_element_chart_reporter(
        self: "CastSelf",
    ) -> "_2026.LoadedRollerElementChartReporter":
        from mastapy._private.bearings.bearing_results import _2026

        return self.__parent__._cast(_2026.LoadedRollerElementChartReporter)

    @property
    def shaft_system_deflection_sections_report(
        self: "CastSelf",
    ) -> "_2929.ShaftSystemDeflectionSectionsReport":
        from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
            _2929,
        )

        return self.__parent__._cast(_2929.ShaftSystemDeflectionSectionsReport)

    @property
    def parametric_study_histogram(
        self: "CastSelf",
    ) -> "_4490.ParametricStudyHistogram":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4490,
        )

        return self.__parent__._cast(_4490.ParametricStudyHistogram)

    @property
    def campbell_diagram_report(self: "CastSelf") -> "_4825.CampbellDiagramReport":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
            _4825,
        )

        return self.__parent__._cast(_4825.CampbellDiagramReport)

    @property
    def per_mode_results_report(self: "CastSelf") -> "_4829.PerModeResultsReport":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
            _4829,
        )

        return self.__parent__._cast(_4829.PerModeResultsReport)

    @property
    def custom_report_nameable_item(self: "CastSelf") -> "CustomReportNameableItem":
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
class CustomReportNameableItem(_1825.CustomReportItem):
    """CustomReportNameableItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_NAMEABLE_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    def x_position_for_cad(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "XPositionForCAD")

        if temp is None:
            return 0.0

        return temp

    @x_position_for_cad.setter
    @enforce_parameter_types
    def x_position_for_cad(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "XPositionForCAD", float(value) if value is not None else 0.0
        )

    @property
    def y_position_for_cad(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "YPositionForCAD")

        if temp is None:
            return 0.0

        return temp

    @y_position_for_cad.setter
    @enforce_parameter_types
    def y_position_for_cad(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "YPositionForCAD", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportNameableItem":
        """Cast to another type.

        Returns:
            _Cast_CustomReportNameableItem
        """
        return _Cast_CustomReportNameableItem(self)
