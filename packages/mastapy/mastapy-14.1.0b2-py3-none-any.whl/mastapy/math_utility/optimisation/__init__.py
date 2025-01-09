"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.math_utility.optimisation._1598 import AbstractOptimisable
    from mastapy._private.math_utility.optimisation._1599 import (
        DesignSpaceSearchStrategyDatabase,
    )
    from mastapy._private.math_utility.optimisation._1600 import InputSetter
    from mastapy._private.math_utility.optimisation._1601 import Optimisable
    from mastapy._private.math_utility.optimisation._1602 import OptimisationHistory
    from mastapy._private.math_utility.optimisation._1603 import OptimizationInput
    from mastapy._private.math_utility.optimisation._1604 import OptimizationVariable
    from mastapy._private.math_utility.optimisation._1605 import (
        ParetoOptimisationFilter,
    )
    from mastapy._private.math_utility.optimisation._1606 import ParetoOptimisationInput
    from mastapy._private.math_utility.optimisation._1607 import (
        ParetoOptimisationOutput,
    )
    from mastapy._private.math_utility.optimisation._1608 import (
        ParetoOptimisationStrategy,
    )
    from mastapy._private.math_utility.optimisation._1609 import (
        ParetoOptimisationStrategyBars,
    )
    from mastapy._private.math_utility.optimisation._1610 import (
        ParetoOptimisationStrategyChartInformation,
    )
    from mastapy._private.math_utility.optimisation._1611 import (
        ParetoOptimisationStrategyDatabase,
    )
    from mastapy._private.math_utility.optimisation._1612 import (
        ParetoOptimisationVariable,
    )
    from mastapy._private.math_utility.optimisation._1613 import (
        ParetoOptimisationVariableBase,
    )
    from mastapy._private.math_utility.optimisation._1614 import (
        PropertyTargetForDominantCandidateSearch,
    )
    from mastapy._private.math_utility.optimisation._1615 import (
        ReportingOptimizationInput,
    )
    from mastapy._private.math_utility.optimisation._1616 import (
        SpecifyOptimisationInputAs,
    )
    from mastapy._private.math_utility.optimisation._1617 import TargetingPropertyTo
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.math_utility.optimisation._1598": ["AbstractOptimisable"],
        "_private.math_utility.optimisation._1599": [
            "DesignSpaceSearchStrategyDatabase"
        ],
        "_private.math_utility.optimisation._1600": ["InputSetter"],
        "_private.math_utility.optimisation._1601": ["Optimisable"],
        "_private.math_utility.optimisation._1602": ["OptimisationHistory"],
        "_private.math_utility.optimisation._1603": ["OptimizationInput"],
        "_private.math_utility.optimisation._1604": ["OptimizationVariable"],
        "_private.math_utility.optimisation._1605": ["ParetoOptimisationFilter"],
        "_private.math_utility.optimisation._1606": ["ParetoOptimisationInput"],
        "_private.math_utility.optimisation._1607": ["ParetoOptimisationOutput"],
        "_private.math_utility.optimisation._1608": ["ParetoOptimisationStrategy"],
        "_private.math_utility.optimisation._1609": ["ParetoOptimisationStrategyBars"],
        "_private.math_utility.optimisation._1610": [
            "ParetoOptimisationStrategyChartInformation"
        ],
        "_private.math_utility.optimisation._1611": [
            "ParetoOptimisationStrategyDatabase"
        ],
        "_private.math_utility.optimisation._1612": ["ParetoOptimisationVariable"],
        "_private.math_utility.optimisation._1613": ["ParetoOptimisationVariableBase"],
        "_private.math_utility.optimisation._1614": [
            "PropertyTargetForDominantCandidateSearch"
        ],
        "_private.math_utility.optimisation._1615": ["ReportingOptimizationInput"],
        "_private.math_utility.optimisation._1616": ["SpecifyOptimisationInputAs"],
        "_private.math_utility.optimisation._1617": ["TargetingPropertyTo"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractOptimisable",
    "DesignSpaceSearchStrategyDatabase",
    "InputSetter",
    "Optimisable",
    "OptimisationHistory",
    "OptimizationInput",
    "OptimizationVariable",
    "ParetoOptimisationFilter",
    "ParetoOptimisationInput",
    "ParetoOptimisationOutput",
    "ParetoOptimisationStrategy",
    "ParetoOptimisationStrategyBars",
    "ParetoOptimisationStrategyChartInformation",
    "ParetoOptimisationStrategyDatabase",
    "ParetoOptimisationVariable",
    "ParetoOptimisationVariableBase",
    "PropertyTargetForDominantCandidateSearch",
    "ReportingOptimizationInput",
    "SpecifyOptimisationInputAs",
    "TargetingPropertyTo",
)
