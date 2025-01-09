"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.report._1804 import AdHocCustomTable
    from mastapy._private.utility.report._1805 import AxisSettings
    from mastapy._private.utility.report._1806 import BlankRow
    from mastapy._private.utility.report._1807 import CadPageOrientation
    from mastapy._private.utility.report._1808 import CadPageSize
    from mastapy._private.utility.report._1809 import CadTableBorderType
    from mastapy._private.utility.report._1810 import ChartDefinition
    from mastapy._private.utility.report._1811 import SMTChartPointShape
    from mastapy._private.utility.report._1812 import CustomChart
    from mastapy._private.utility.report._1813 import CustomDrawing
    from mastapy._private.utility.report._1814 import CustomGraphic
    from mastapy._private.utility.report._1815 import CustomImage
    from mastapy._private.utility.report._1816 import CustomReport
    from mastapy._private.utility.report._1817 import CustomReportCadDrawing
    from mastapy._private.utility.report._1818 import CustomReportChart
    from mastapy._private.utility.report._1819 import CustomReportChartItem
    from mastapy._private.utility.report._1820 import CustomReportColumn
    from mastapy._private.utility.report._1821 import CustomReportColumns
    from mastapy._private.utility.report._1822 import CustomReportDefinitionItem
    from mastapy._private.utility.report._1823 import CustomReportHorizontalLine
    from mastapy._private.utility.report._1824 import CustomReportHtmlItem
    from mastapy._private.utility.report._1825 import CustomReportItem
    from mastapy._private.utility.report._1826 import CustomReportItemContainer
    from mastapy._private.utility.report._1827 import (
        CustomReportItemContainerCollection,
    )
    from mastapy._private.utility.report._1828 import (
        CustomReportItemContainerCollectionBase,
    )
    from mastapy._private.utility.report._1829 import (
        CustomReportItemContainerCollectionItem,
    )
    from mastapy._private.utility.report._1830 import CustomReportKey
    from mastapy._private.utility.report._1831 import CustomReportMultiPropertyItem
    from mastapy._private.utility.report._1832 import CustomReportMultiPropertyItemBase
    from mastapy._private.utility.report._1833 import CustomReportNameableItem
    from mastapy._private.utility.report._1834 import CustomReportNamedItem
    from mastapy._private.utility.report._1835 import CustomReportPropertyItem
    from mastapy._private.utility.report._1836 import CustomReportStatusItem
    from mastapy._private.utility.report._1837 import CustomReportTab
    from mastapy._private.utility.report._1838 import CustomReportTabs
    from mastapy._private.utility.report._1839 import CustomReportText
    from mastapy._private.utility.report._1840 import CustomRow
    from mastapy._private.utility.report._1841 import CustomSubReport
    from mastapy._private.utility.report._1842 import CustomTable
    from mastapy._private.utility.report._1843 import DefinitionBooleanCheckOptions
    from mastapy._private.utility.report._1844 import DynamicCustomReportItem
    from mastapy._private.utility.report._1845 import FontStyle
    from mastapy._private.utility.report._1846 import FontWeight
    from mastapy._private.utility.report._1847 import HeadingSize
    from mastapy._private.utility.report._1848 import SimpleChartDefinition
    from mastapy._private.utility.report._1849 import UserTextRow
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.report._1804": ["AdHocCustomTable"],
        "_private.utility.report._1805": ["AxisSettings"],
        "_private.utility.report._1806": ["BlankRow"],
        "_private.utility.report._1807": ["CadPageOrientation"],
        "_private.utility.report._1808": ["CadPageSize"],
        "_private.utility.report._1809": ["CadTableBorderType"],
        "_private.utility.report._1810": ["ChartDefinition"],
        "_private.utility.report._1811": ["SMTChartPointShape"],
        "_private.utility.report._1812": ["CustomChart"],
        "_private.utility.report._1813": ["CustomDrawing"],
        "_private.utility.report._1814": ["CustomGraphic"],
        "_private.utility.report._1815": ["CustomImage"],
        "_private.utility.report._1816": ["CustomReport"],
        "_private.utility.report._1817": ["CustomReportCadDrawing"],
        "_private.utility.report._1818": ["CustomReportChart"],
        "_private.utility.report._1819": ["CustomReportChartItem"],
        "_private.utility.report._1820": ["CustomReportColumn"],
        "_private.utility.report._1821": ["CustomReportColumns"],
        "_private.utility.report._1822": ["CustomReportDefinitionItem"],
        "_private.utility.report._1823": ["CustomReportHorizontalLine"],
        "_private.utility.report._1824": ["CustomReportHtmlItem"],
        "_private.utility.report._1825": ["CustomReportItem"],
        "_private.utility.report._1826": ["CustomReportItemContainer"],
        "_private.utility.report._1827": ["CustomReportItemContainerCollection"],
        "_private.utility.report._1828": ["CustomReportItemContainerCollectionBase"],
        "_private.utility.report._1829": ["CustomReportItemContainerCollectionItem"],
        "_private.utility.report._1830": ["CustomReportKey"],
        "_private.utility.report._1831": ["CustomReportMultiPropertyItem"],
        "_private.utility.report._1832": ["CustomReportMultiPropertyItemBase"],
        "_private.utility.report._1833": ["CustomReportNameableItem"],
        "_private.utility.report._1834": ["CustomReportNamedItem"],
        "_private.utility.report._1835": ["CustomReportPropertyItem"],
        "_private.utility.report._1836": ["CustomReportStatusItem"],
        "_private.utility.report._1837": ["CustomReportTab"],
        "_private.utility.report._1838": ["CustomReportTabs"],
        "_private.utility.report._1839": ["CustomReportText"],
        "_private.utility.report._1840": ["CustomRow"],
        "_private.utility.report._1841": ["CustomSubReport"],
        "_private.utility.report._1842": ["CustomTable"],
        "_private.utility.report._1843": ["DefinitionBooleanCheckOptions"],
        "_private.utility.report._1844": ["DynamicCustomReportItem"],
        "_private.utility.report._1845": ["FontStyle"],
        "_private.utility.report._1846": ["FontWeight"],
        "_private.utility.report._1847": ["HeadingSize"],
        "_private.utility.report._1848": ["SimpleChartDefinition"],
        "_private.utility.report._1849": ["UserTextRow"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AdHocCustomTable",
    "AxisSettings",
    "BlankRow",
    "CadPageOrientation",
    "CadPageSize",
    "CadTableBorderType",
    "ChartDefinition",
    "SMTChartPointShape",
    "CustomChart",
    "CustomDrawing",
    "CustomGraphic",
    "CustomImage",
    "CustomReport",
    "CustomReportCadDrawing",
    "CustomReportChart",
    "CustomReportChartItem",
    "CustomReportColumn",
    "CustomReportColumns",
    "CustomReportDefinitionItem",
    "CustomReportHorizontalLine",
    "CustomReportHtmlItem",
    "CustomReportItem",
    "CustomReportItemContainer",
    "CustomReportItemContainerCollection",
    "CustomReportItemContainerCollectionBase",
    "CustomReportItemContainerCollectionItem",
    "CustomReportKey",
    "CustomReportMultiPropertyItem",
    "CustomReportMultiPropertyItemBase",
    "CustomReportNameableItem",
    "CustomReportNamedItem",
    "CustomReportPropertyItem",
    "CustomReportStatusItem",
    "CustomReportTab",
    "CustomReportTabs",
    "CustomReportText",
    "CustomRow",
    "CustomSubReport",
    "CustomTable",
    "DefinitionBooleanCheckOptions",
    "DynamicCustomReportItem",
    "FontStyle",
    "FontWeight",
    "HeadingSize",
    "SimpleChartDefinition",
    "UserTextRow",
)
