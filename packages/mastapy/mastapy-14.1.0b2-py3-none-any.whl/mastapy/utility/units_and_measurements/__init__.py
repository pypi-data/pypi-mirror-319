"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.units_and_measurements._1663 import (
        DegreesMinutesSeconds,
    )
    from mastapy._private.utility.units_and_measurements._1664 import EnumUnit
    from mastapy._private.utility.units_and_measurements._1665 import InverseUnit
    from mastapy._private.utility.units_and_measurements._1666 import MeasurementBase
    from mastapy._private.utility.units_and_measurements._1667 import (
        MeasurementSettings,
    )
    from mastapy._private.utility.units_and_measurements._1668 import MeasurementSystem
    from mastapy._private.utility.units_and_measurements._1669 import SafetyFactorUnit
    from mastapy._private.utility.units_and_measurements._1670 import TimeUnit
    from mastapy._private.utility.units_and_measurements._1671 import Unit
    from mastapy._private.utility.units_and_measurements._1672 import UnitGradient
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.units_and_measurements._1663": ["DegreesMinutesSeconds"],
        "_private.utility.units_and_measurements._1664": ["EnumUnit"],
        "_private.utility.units_and_measurements._1665": ["InverseUnit"],
        "_private.utility.units_and_measurements._1666": ["MeasurementBase"],
        "_private.utility.units_and_measurements._1667": ["MeasurementSettings"],
        "_private.utility.units_and_measurements._1668": ["MeasurementSystem"],
        "_private.utility.units_and_measurements._1669": ["SafetyFactorUnit"],
        "_private.utility.units_and_measurements._1670": ["TimeUnit"],
        "_private.utility.units_and_measurements._1671": ["Unit"],
        "_private.utility.units_and_measurements._1672": ["UnitGradient"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "DegreesMinutesSeconds",
    "EnumUnit",
    "InverseUnit",
    "MeasurementBase",
    "MeasurementSettings",
    "MeasurementSystem",
    "SafetyFactorUnit",
    "TimeUnit",
    "Unit",
    "UnitGradient",
)
