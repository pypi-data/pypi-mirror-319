"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bearings.bearing_results.rolling.fitting._2178 import (
        InnerRingFittingThermalResults,
    )
    from mastapy._private.bearings.bearing_results.rolling.fitting._2179 import (
        InterferenceComponents,
    )
    from mastapy._private.bearings.bearing_results.rolling.fitting._2180 import (
        OuterRingFittingThermalResults,
    )
    from mastapy._private.bearings.bearing_results.rolling.fitting._2181 import (
        RingFittingThermalResults,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bearings.bearing_results.rolling.fitting._2178": [
            "InnerRingFittingThermalResults"
        ],
        "_private.bearings.bearing_results.rolling.fitting._2179": [
            "InterferenceComponents"
        ],
        "_private.bearings.bearing_results.rolling.fitting._2180": [
            "OuterRingFittingThermalResults"
        ],
        "_private.bearings.bearing_results.rolling.fitting._2181": [
            "RingFittingThermalResults"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "InnerRingFittingThermalResults",
    "InterferenceComponents",
    "OuterRingFittingThermalResults",
    "RingFittingThermalResults",
)
