"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bearings.bearing_designs._2198 import BearingDesign
    from mastapy._private.bearings.bearing_designs._2199 import DetailedBearing
    from mastapy._private.bearings.bearing_designs._2200 import DummyRollingBearing
    from mastapy._private.bearings.bearing_designs._2201 import LinearBearing
    from mastapy._private.bearings.bearing_designs._2202 import NonLinearBearing
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bearings.bearing_designs._2198": ["BearingDesign"],
        "_private.bearings.bearing_designs._2199": ["DetailedBearing"],
        "_private.bearings.bearing_designs._2200": ["DummyRollingBearing"],
        "_private.bearings.bearing_designs._2201": ["LinearBearing"],
        "_private.bearings.bearing_designs._2202": ["NonLinearBearing"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BearingDesign",
    "DetailedBearing",
    "DummyRollingBearing",
    "LinearBearing",
    "NonLinearBearing",
)
