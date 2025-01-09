"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.property._1902 import DeletableCollectionMember
    from mastapy._private.utility.property._1903 import DutyCyclePropertySummary
    from mastapy._private.utility.property._1904 import DutyCyclePropertySummaryForce
    from mastapy._private.utility.property._1905 import (
        DutyCyclePropertySummaryPercentage,
    )
    from mastapy._private.utility.property._1906 import (
        DutyCyclePropertySummarySmallAngle,
    )
    from mastapy._private.utility.property._1907 import DutyCyclePropertySummaryStress
    from mastapy._private.utility.property._1908 import (
        DutyCyclePropertySummaryVeryShortLength,
    )
    from mastapy._private.utility.property._1909 import EnumWithBoolean
    from mastapy._private.utility.property._1910 import ListWithSelectedItemAndImage
    from mastapy._private.utility.property._1911 import (
        NamedRangeWithOverridableMinAndMax,
    )
    from mastapy._private.utility.property._1912 import TypedObjectsWithOption
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.property._1902": ["DeletableCollectionMember"],
        "_private.utility.property._1903": ["DutyCyclePropertySummary"],
        "_private.utility.property._1904": ["DutyCyclePropertySummaryForce"],
        "_private.utility.property._1905": ["DutyCyclePropertySummaryPercentage"],
        "_private.utility.property._1906": ["DutyCyclePropertySummarySmallAngle"],
        "_private.utility.property._1907": ["DutyCyclePropertySummaryStress"],
        "_private.utility.property._1908": ["DutyCyclePropertySummaryVeryShortLength"],
        "_private.utility.property._1909": ["EnumWithBoolean"],
        "_private.utility.property._1910": ["ListWithSelectedItemAndImage"],
        "_private.utility.property._1911": ["NamedRangeWithOverridableMinAndMax"],
        "_private.utility.property._1912": ["TypedObjectsWithOption"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "DeletableCollectionMember",
    "DutyCyclePropertySummary",
    "DutyCyclePropertySummaryForce",
    "DutyCyclePropertySummaryPercentage",
    "DutyCyclePropertySummarySmallAngle",
    "DutyCyclePropertySummaryStress",
    "DutyCyclePropertySummaryVeryShortLength",
    "EnumWithBoolean",
    "ListWithSelectedItemAndImage",
    "NamedRangeWithOverridableMinAndMax",
    "TypedObjectsWithOption",
)
