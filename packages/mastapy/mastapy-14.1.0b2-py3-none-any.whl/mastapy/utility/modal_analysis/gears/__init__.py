"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.modal_analysis.gears._1861 import GearMeshForTE
    from mastapy._private.utility.modal_analysis.gears._1862 import GearOrderForTE
    from mastapy._private.utility.modal_analysis.gears._1863 import GearPositions
    from mastapy._private.utility.modal_analysis.gears._1864 import HarmonicOrderForTE
    from mastapy._private.utility.modal_analysis.gears._1865 import LabelOnlyOrder
    from mastapy._private.utility.modal_analysis.gears._1866 import OrderForTE
    from mastapy._private.utility.modal_analysis.gears._1867 import OrderSelector
    from mastapy._private.utility.modal_analysis.gears._1868 import OrderWithRadius
    from mastapy._private.utility.modal_analysis.gears._1869 import RollingBearingOrder
    from mastapy._private.utility.modal_analysis.gears._1870 import ShaftOrderForTE
    from mastapy._private.utility.modal_analysis.gears._1871 import (
        UserDefinedOrderForTE,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.modal_analysis.gears._1861": ["GearMeshForTE"],
        "_private.utility.modal_analysis.gears._1862": ["GearOrderForTE"],
        "_private.utility.modal_analysis.gears._1863": ["GearPositions"],
        "_private.utility.modal_analysis.gears._1864": ["HarmonicOrderForTE"],
        "_private.utility.modal_analysis.gears._1865": ["LabelOnlyOrder"],
        "_private.utility.modal_analysis.gears._1866": ["OrderForTE"],
        "_private.utility.modal_analysis.gears._1867": ["OrderSelector"],
        "_private.utility.modal_analysis.gears._1868": ["OrderWithRadius"],
        "_private.utility.modal_analysis.gears._1869": ["RollingBearingOrder"],
        "_private.utility.modal_analysis.gears._1870": ["ShaftOrderForTE"],
        "_private.utility.modal_analysis.gears._1871": ["UserDefinedOrderForTE"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "GearMeshForTE",
    "GearOrderForTE",
    "GearPositions",
    "HarmonicOrderForTE",
    "LabelOnlyOrder",
    "OrderForTE",
    "OrderSelector",
    "OrderWithRadius",
    "RollingBearingOrder",
    "ShaftOrderForTE",
    "UserDefinedOrderForTE",
)
