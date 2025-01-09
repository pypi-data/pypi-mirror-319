"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility_gui.charts._1919 import BubbleChartDefinition
    from mastapy._private.utility_gui.charts._1920 import ConstantLine
    from mastapy._private.utility_gui.charts._1921 import CustomLineChart
    from mastapy._private.utility_gui.charts._1922 import CustomTableAndChart
    from mastapy._private.utility_gui.charts._1923 import LegacyChartMathChartDefinition
    from mastapy._private.utility_gui.charts._1924 import MatrixVisualisationDefinition
    from mastapy._private.utility_gui.charts._1925 import ModeConstantLine
    from mastapy._private.utility_gui.charts._1926 import NDChartDefinition
    from mastapy._private.utility_gui.charts._1927 import (
        ParallelCoordinatesChartDefinition,
    )
    from mastapy._private.utility_gui.charts._1928 import PointsForSurface
    from mastapy._private.utility_gui.charts._1929 import ScatterChartDefinition
    from mastapy._private.utility_gui.charts._1930 import Series2D
    from mastapy._private.utility_gui.charts._1931 import SMTAxis
    from mastapy._private.utility_gui.charts._1932 import ThreeDChartDefinition
    from mastapy._private.utility_gui.charts._1933 import ThreeDVectorChartDefinition
    from mastapy._private.utility_gui.charts._1934 import TwoDChartDefinition
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility_gui.charts._1919": ["BubbleChartDefinition"],
        "_private.utility_gui.charts._1920": ["ConstantLine"],
        "_private.utility_gui.charts._1921": ["CustomLineChart"],
        "_private.utility_gui.charts._1922": ["CustomTableAndChart"],
        "_private.utility_gui.charts._1923": ["LegacyChartMathChartDefinition"],
        "_private.utility_gui.charts._1924": ["MatrixVisualisationDefinition"],
        "_private.utility_gui.charts._1925": ["ModeConstantLine"],
        "_private.utility_gui.charts._1926": ["NDChartDefinition"],
        "_private.utility_gui.charts._1927": ["ParallelCoordinatesChartDefinition"],
        "_private.utility_gui.charts._1928": ["PointsForSurface"],
        "_private.utility_gui.charts._1929": ["ScatterChartDefinition"],
        "_private.utility_gui.charts._1930": ["Series2D"],
        "_private.utility_gui.charts._1931": ["SMTAxis"],
        "_private.utility_gui.charts._1932": ["ThreeDChartDefinition"],
        "_private.utility_gui.charts._1933": ["ThreeDVectorChartDefinition"],
        "_private.utility_gui.charts._1934": ["TwoDChartDefinition"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BubbleChartDefinition",
    "ConstantLine",
    "CustomLineChart",
    "CustomTableAndChart",
    "LegacyChartMathChartDefinition",
    "MatrixVisualisationDefinition",
    "ModeConstantLine",
    "NDChartDefinition",
    "ParallelCoordinatesChartDefinition",
    "PointsForSurface",
    "ScatterChartDefinition",
    "Series2D",
    "SMTAxis",
    "ThreeDChartDefinition",
    "ThreeDVectorChartDefinition",
    "TwoDChartDefinition",
)
