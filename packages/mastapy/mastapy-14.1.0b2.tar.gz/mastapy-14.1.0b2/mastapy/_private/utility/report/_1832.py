"""CustomReportMultiPropertyItemBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.report import _1833

_CUSTOM_REPORT_MULTI_PROPERTY_ITEM_BASE = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportMultiPropertyItemBase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2014, _2018, _2026
    from mastapy._private.gears.gear_designs.cylindrical import _1073
    from mastapy._private.shafts import _20
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
        _4825,
        _4829,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
        _2929,
    )
    from mastapy._private.utility.report import _1818, _1825, _1831, _1842
    from mastapy._private.utility_gui.charts import _1921, _1922

    Self = TypeVar("Self", bound="CustomReportMultiPropertyItemBase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CustomReportMultiPropertyItemBase._Cast_CustomReportMultiPropertyItemBase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportMultiPropertyItemBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportMultiPropertyItemBase:
    """Special nested class for casting CustomReportMultiPropertyItemBase to subclasses."""

    __parent__: "CustomReportMultiPropertyItemBase"

    @property
    def custom_report_nameable_item(
        self: "CastSelf",
    ) -> "_1833.CustomReportNameableItem":
        return self.__parent__._cast(_1833.CustomReportNameableItem)

    @property
    def custom_report_item(self: "CastSelf") -> "_1825.CustomReportItem":
        from mastapy._private.utility.report import _1825

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
    def custom_report_chart(self: "CastSelf") -> "_1818.CustomReportChart":
        from mastapy._private.utility.report import _1818

        return self.__parent__._cast(_1818.CustomReportChart)

    @property
    def custom_report_multi_property_item(
        self: "CastSelf",
    ) -> "_1831.CustomReportMultiPropertyItem":
        from mastapy._private.utility.report import _1831

        return self.__parent__._cast(_1831.CustomReportMultiPropertyItem)

    @property
    def custom_table(self: "CastSelf") -> "_1842.CustomTable":
        from mastapy._private.utility.report import _1842

        return self.__parent__._cast(_1842.CustomTable)

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
    def custom_report_multi_property_item_base(
        self: "CastSelf",
    ) -> "CustomReportMultiPropertyItemBase":
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
class CustomReportMultiPropertyItemBase(_1833.CustomReportNameableItem):
    """CustomReportMultiPropertyItemBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_MULTI_PROPERTY_ITEM_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportMultiPropertyItemBase":
        """Cast to another type.

        Returns:
            _Cast_CustomReportMultiPropertyItemBase
        """
        return _Cast_CustomReportMultiPropertyItemBase(self)
