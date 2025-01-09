"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.optimization.system_optimiser._2306 import (
        DesignStateTargetRatio,
    )
    from mastapy._private.system_model.optimization.system_optimiser._2307 import (
        PlanetGearOptions,
    )
    from mastapy._private.system_model.optimization.system_optimiser._2308 import (
        SystemOptimiser,
    )
    from mastapy._private.system_model.optimization.system_optimiser._2309 import (
        SystemOptimiserDetails,
    )
    from mastapy._private.system_model.optimization.system_optimiser._2310 import (
        ToothNumberFinder,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.optimization.system_optimiser._2306": [
            "DesignStateTargetRatio"
        ],
        "_private.system_model.optimization.system_optimiser._2307": [
            "PlanetGearOptions"
        ],
        "_private.system_model.optimization.system_optimiser._2308": [
            "SystemOptimiser"
        ],
        "_private.system_model.optimization.system_optimiser._2309": [
            "SystemOptimiserDetails"
        ],
        "_private.system_model.optimization.system_optimiser._2310": [
            "ToothNumberFinder"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "DesignStateTargetRatio",
    "PlanetGearOptions",
    "SystemOptimiser",
    "SystemOptimiserDetails",
    "ToothNumberFinder",
)
