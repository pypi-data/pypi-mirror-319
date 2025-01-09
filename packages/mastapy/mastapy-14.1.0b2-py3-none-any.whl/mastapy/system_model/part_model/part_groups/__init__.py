"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.part_groups._2559 import (
        ConcentricOrParallelPartGroup,
    )
    from mastapy._private.system_model.part_model.part_groups._2560 import (
        ConcentricPartGroup,
    )
    from mastapy._private.system_model.part_model.part_groups._2561 import (
        ConcentricPartGroupParallelToThis,
    )
    from mastapy._private.system_model.part_model.part_groups._2562 import (
        DesignMeasurements,
    )
    from mastapy._private.system_model.part_model.part_groups._2563 import (
        ParallelPartGroup,
    )
    from mastapy._private.system_model.part_model.part_groups._2564 import (
        ParallelPartGroupSelection,
    )
    from mastapy._private.system_model.part_model.part_groups._2565 import PartGroup
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.part_groups._2559": [
            "ConcentricOrParallelPartGroup"
        ],
        "_private.system_model.part_model.part_groups._2560": ["ConcentricPartGroup"],
        "_private.system_model.part_model.part_groups._2561": [
            "ConcentricPartGroupParallelToThis"
        ],
        "_private.system_model.part_model.part_groups._2562": ["DesignMeasurements"],
        "_private.system_model.part_model.part_groups._2563": ["ParallelPartGroup"],
        "_private.system_model.part_model.part_groups._2564": [
            "ParallelPartGroupSelection"
        ],
        "_private.system_model.part_model.part_groups._2565": ["PartGroup"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConcentricOrParallelPartGroup",
    "ConcentricPartGroup",
    "ConcentricPartGroupParallelToThis",
    "DesignMeasurements",
    "ParallelPartGroup",
    "ParallelPartGroupSelection",
    "PartGroup",
)
