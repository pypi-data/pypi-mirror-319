"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.configurations._2694 import (
        ActiveFESubstructureSelection,
    )
    from mastapy._private.system_model.part_model.configurations._2695 import (
        ActiveFESubstructureSelectionGroup,
    )
    from mastapy._private.system_model.part_model.configurations._2696 import (
        ActiveShaftDesignSelection,
    )
    from mastapy._private.system_model.part_model.configurations._2697 import (
        ActiveShaftDesignSelectionGroup,
    )
    from mastapy._private.system_model.part_model.configurations._2698 import (
        BearingDetailConfiguration,
    )
    from mastapy._private.system_model.part_model.configurations._2699 import (
        BearingDetailSelection,
    )
    from mastapy._private.system_model.part_model.configurations._2700 import (
        DesignConfiguration,
    )
    from mastapy._private.system_model.part_model.configurations._2701 import (
        PartDetailConfiguration,
    )
    from mastapy._private.system_model.part_model.configurations._2702 import (
        PartDetailSelection,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.configurations._2694": [
            "ActiveFESubstructureSelection"
        ],
        "_private.system_model.part_model.configurations._2695": [
            "ActiveFESubstructureSelectionGroup"
        ],
        "_private.system_model.part_model.configurations._2696": [
            "ActiveShaftDesignSelection"
        ],
        "_private.system_model.part_model.configurations._2697": [
            "ActiveShaftDesignSelectionGroup"
        ],
        "_private.system_model.part_model.configurations._2698": [
            "BearingDetailConfiguration"
        ],
        "_private.system_model.part_model.configurations._2699": [
            "BearingDetailSelection"
        ],
        "_private.system_model.part_model.configurations._2700": [
            "DesignConfiguration"
        ],
        "_private.system_model.part_model.configurations._2701": [
            "PartDetailConfiguration"
        ],
        "_private.system_model.part_model.configurations._2702": [
            "PartDetailSelection"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ActiveFESubstructureSelection",
    "ActiveFESubstructureSelectionGroup",
    "ActiveShaftDesignSelection",
    "ActiveShaftDesignSelectionGroup",
    "BearingDetailConfiguration",
    "BearingDetailSelection",
    "DesignConfiguration",
    "PartDetailConfiguration",
    "PartDetailSelection",
)
