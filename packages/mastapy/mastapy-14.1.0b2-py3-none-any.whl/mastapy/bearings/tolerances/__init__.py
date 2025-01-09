"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bearings.tolerances._1968 import BearingConnectionComponent
    from mastapy._private.bearings.tolerances._1969 import InternalClearanceClass
    from mastapy._private.bearings.tolerances._1970 import BearingToleranceClass
    from mastapy._private.bearings.tolerances._1971 import (
        BearingToleranceDefinitionOptions,
    )
    from mastapy._private.bearings.tolerances._1972 import FitType
    from mastapy._private.bearings.tolerances._1973 import InnerRingTolerance
    from mastapy._private.bearings.tolerances._1974 import InnerSupportTolerance
    from mastapy._private.bearings.tolerances._1975 import InterferenceDetail
    from mastapy._private.bearings.tolerances._1976 import InterferenceTolerance
    from mastapy._private.bearings.tolerances._1977 import ITDesignation
    from mastapy._private.bearings.tolerances._1978 import MountingSleeveDiameterDetail
    from mastapy._private.bearings.tolerances._1979 import OuterRingTolerance
    from mastapy._private.bearings.tolerances._1980 import OuterSupportTolerance
    from mastapy._private.bearings.tolerances._1981 import RaceRoundnessAtAngle
    from mastapy._private.bearings.tolerances._1982 import RadialSpecificationMethod
    from mastapy._private.bearings.tolerances._1983 import RingDetail
    from mastapy._private.bearings.tolerances._1984 import RingTolerance
    from mastapy._private.bearings.tolerances._1985 import RoundnessSpecification
    from mastapy._private.bearings.tolerances._1986 import RoundnessSpecificationType
    from mastapy._private.bearings.tolerances._1987 import SupportDetail
    from mastapy._private.bearings.tolerances._1988 import SupportMaterialSource
    from mastapy._private.bearings.tolerances._1989 import SupportTolerance
    from mastapy._private.bearings.tolerances._1990 import (
        SupportToleranceLocationDesignation,
    )
    from mastapy._private.bearings.tolerances._1991 import ToleranceCombination
    from mastapy._private.bearings.tolerances._1992 import TypeOfFit
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bearings.tolerances._1968": ["BearingConnectionComponent"],
        "_private.bearings.tolerances._1969": ["InternalClearanceClass"],
        "_private.bearings.tolerances._1970": ["BearingToleranceClass"],
        "_private.bearings.tolerances._1971": ["BearingToleranceDefinitionOptions"],
        "_private.bearings.tolerances._1972": ["FitType"],
        "_private.bearings.tolerances._1973": ["InnerRingTolerance"],
        "_private.bearings.tolerances._1974": ["InnerSupportTolerance"],
        "_private.bearings.tolerances._1975": ["InterferenceDetail"],
        "_private.bearings.tolerances._1976": ["InterferenceTolerance"],
        "_private.bearings.tolerances._1977": ["ITDesignation"],
        "_private.bearings.tolerances._1978": ["MountingSleeveDiameterDetail"],
        "_private.bearings.tolerances._1979": ["OuterRingTolerance"],
        "_private.bearings.tolerances._1980": ["OuterSupportTolerance"],
        "_private.bearings.tolerances._1981": ["RaceRoundnessAtAngle"],
        "_private.bearings.tolerances._1982": ["RadialSpecificationMethod"],
        "_private.bearings.tolerances._1983": ["RingDetail"],
        "_private.bearings.tolerances._1984": ["RingTolerance"],
        "_private.bearings.tolerances._1985": ["RoundnessSpecification"],
        "_private.bearings.tolerances._1986": ["RoundnessSpecificationType"],
        "_private.bearings.tolerances._1987": ["SupportDetail"],
        "_private.bearings.tolerances._1988": ["SupportMaterialSource"],
        "_private.bearings.tolerances._1989": ["SupportTolerance"],
        "_private.bearings.tolerances._1990": ["SupportToleranceLocationDesignation"],
        "_private.bearings.tolerances._1991": ["ToleranceCombination"],
        "_private.bearings.tolerances._1992": ["TypeOfFit"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BearingConnectionComponent",
    "InternalClearanceClass",
    "BearingToleranceClass",
    "BearingToleranceDefinitionOptions",
    "FitType",
    "InnerRingTolerance",
    "InnerSupportTolerance",
    "InterferenceDetail",
    "InterferenceTolerance",
    "ITDesignation",
    "MountingSleeveDiameterDetail",
    "OuterRingTolerance",
    "OuterSupportTolerance",
    "RaceRoundnessAtAngle",
    "RadialSpecificationMethod",
    "RingDetail",
    "RingTolerance",
    "RoundnessSpecification",
    "RoundnessSpecificationType",
    "SupportDetail",
    "SupportMaterialSource",
    "SupportTolerance",
    "SupportToleranceLocationDesignation",
    "ToleranceCombination",
    "TypeOfFit",
)
