"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.fe.version_comparer._2482 import DesignResults
    from mastapy._private.system_model.fe.version_comparer._2483 import (
        FESubstructureResults,
    )
    from mastapy._private.system_model.fe.version_comparer._2484 import (
        FESubstructureVersionComparer,
    )
    from mastapy._private.system_model.fe.version_comparer._2485 import LoadCaseResults
    from mastapy._private.system_model.fe.version_comparer._2486 import LoadCasesToRun
    from mastapy._private.system_model.fe.version_comparer._2487 import (
        NodeComparisonResult,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.fe.version_comparer._2482": ["DesignResults"],
        "_private.system_model.fe.version_comparer._2483": ["FESubstructureResults"],
        "_private.system_model.fe.version_comparer._2484": [
            "FESubstructureVersionComparer"
        ],
        "_private.system_model.fe.version_comparer._2485": ["LoadCaseResults"],
        "_private.system_model.fe.version_comparer._2486": ["LoadCasesToRun"],
        "_private.system_model.fe.version_comparer._2487": ["NodeComparisonResult"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "DesignResults",
    "FESubstructureResults",
    "FESubstructureVersionComparer",
    "LoadCaseResults",
    "LoadCasesToRun",
    "NodeComparisonResult",
)
