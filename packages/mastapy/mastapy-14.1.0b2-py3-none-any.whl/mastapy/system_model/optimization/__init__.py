"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.optimization._2295 import (
        ConicalGearOptimisationStrategy,
    )
    from mastapy._private.system_model.optimization._2296 import (
        ConicalGearOptimizationStep,
    )
    from mastapy._private.system_model.optimization._2297 import (
        ConicalGearOptimizationStrategyDatabase,
    )
    from mastapy._private.system_model.optimization._2298 import (
        CylindricalGearOptimisationStrategy,
    )
    from mastapy._private.system_model.optimization._2299 import (
        CylindricalGearOptimizationStep,
    )
    from mastapy._private.system_model.optimization._2300 import (
        MeasuredAndFactorViewModel,
    )
    from mastapy._private.system_model.optimization._2301 import (
        MicroGeometryOptimisationTarget,
    )
    from mastapy._private.system_model.optimization._2302 import OptimizationStep
    from mastapy._private.system_model.optimization._2303 import OptimizationStrategy
    from mastapy._private.system_model.optimization._2304 import (
        OptimizationStrategyBase,
    )
    from mastapy._private.system_model.optimization._2305 import (
        OptimizationStrategyDatabase,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.optimization._2295": ["ConicalGearOptimisationStrategy"],
        "_private.system_model.optimization._2296": ["ConicalGearOptimizationStep"],
        "_private.system_model.optimization._2297": [
            "ConicalGearOptimizationStrategyDatabase"
        ],
        "_private.system_model.optimization._2298": [
            "CylindricalGearOptimisationStrategy"
        ],
        "_private.system_model.optimization._2299": ["CylindricalGearOptimizationStep"],
        "_private.system_model.optimization._2300": ["MeasuredAndFactorViewModel"],
        "_private.system_model.optimization._2301": ["MicroGeometryOptimisationTarget"],
        "_private.system_model.optimization._2302": ["OptimizationStep"],
        "_private.system_model.optimization._2303": ["OptimizationStrategy"],
        "_private.system_model.optimization._2304": ["OptimizationStrategyBase"],
        "_private.system_model.optimization._2305": ["OptimizationStrategyDatabase"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConicalGearOptimisationStrategy",
    "ConicalGearOptimizationStep",
    "ConicalGearOptimizationStrategyDatabase",
    "CylindricalGearOptimisationStrategy",
    "CylindricalGearOptimizationStep",
    "MeasuredAndFactorViewModel",
    "MicroGeometryOptimisationTarget",
    "OptimizationStep",
    "OptimizationStrategy",
    "OptimizationStrategyBase",
    "OptimizationStrategyDatabase",
)
