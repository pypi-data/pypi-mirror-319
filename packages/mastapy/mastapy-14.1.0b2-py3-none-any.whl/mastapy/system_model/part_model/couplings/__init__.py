"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.couplings._2652 import BeltDrive
    from mastapy._private.system_model.part_model.couplings._2653 import BeltDriveType
    from mastapy._private.system_model.part_model.couplings._2654 import Clutch
    from mastapy._private.system_model.part_model.couplings._2655 import ClutchHalf
    from mastapy._private.system_model.part_model.couplings._2656 import ClutchType
    from mastapy._private.system_model.part_model.couplings._2657 import ConceptCoupling
    from mastapy._private.system_model.part_model.couplings._2658 import (
        ConceptCouplingHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2659 import (
        ConceptCouplingHalfPositioning,
    )
    from mastapy._private.system_model.part_model.couplings._2660 import Coupling
    from mastapy._private.system_model.part_model.couplings._2661 import CouplingHalf
    from mastapy._private.system_model.part_model.couplings._2662 import (
        CrowningSpecification,
    )
    from mastapy._private.system_model.part_model.couplings._2663 import CVT
    from mastapy._private.system_model.part_model.couplings._2664 import CVTPulley
    from mastapy._private.system_model.part_model.couplings._2665 import (
        PartToPartShearCoupling,
    )
    from mastapy._private.system_model.part_model.couplings._2666 import (
        PartToPartShearCouplingHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2667 import (
        PitchErrorFlankOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2668 import Pulley
    from mastapy._private.system_model.part_model.couplings._2669 import (
        RigidConnectorSettings,
    )
    from mastapy._private.system_model.part_model.couplings._2670 import (
        RigidConnectorStiffnessType,
    )
    from mastapy._private.system_model.part_model.couplings._2671 import (
        RigidConnectorTiltStiffnessTypes,
    )
    from mastapy._private.system_model.part_model.couplings._2672 import (
        RigidConnectorToothLocation,
    )
    from mastapy._private.system_model.part_model.couplings._2673 import (
        RigidConnectorToothSpacingType,
    )
    from mastapy._private.system_model.part_model.couplings._2674 import (
        RigidConnectorTypes,
    )
    from mastapy._private.system_model.part_model.couplings._2675 import RollingRing
    from mastapy._private.system_model.part_model.couplings._2676 import (
        RollingRingAssembly,
    )
    from mastapy._private.system_model.part_model.couplings._2677 import (
        ShaftHubConnection,
    )
    from mastapy._private.system_model.part_model.couplings._2678 import (
        SplineFitOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2679 import (
        SplineHalfManufacturingError,
    )
    from mastapy._private.system_model.part_model.couplings._2680 import (
        SplineLeadRelief,
    )
    from mastapy._private.system_model.part_model.couplings._2681 import (
        SplinePitchErrorInputType,
    )
    from mastapy._private.system_model.part_model.couplings._2682 import (
        SplinePitchErrorOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2683 import SpringDamper
    from mastapy._private.system_model.part_model.couplings._2684 import (
        SpringDamperHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2685 import Synchroniser
    from mastapy._private.system_model.part_model.couplings._2686 import (
        SynchroniserCone,
    )
    from mastapy._private.system_model.part_model.couplings._2687 import (
        SynchroniserHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2688 import (
        SynchroniserPart,
    )
    from mastapy._private.system_model.part_model.couplings._2689 import (
        SynchroniserSleeve,
    )
    from mastapy._private.system_model.part_model.couplings._2690 import TorqueConverter
    from mastapy._private.system_model.part_model.couplings._2691 import (
        TorqueConverterPump,
    )
    from mastapy._private.system_model.part_model.couplings._2692 import (
        TorqueConverterSpeedRatio,
    )
    from mastapy._private.system_model.part_model.couplings._2693 import (
        TorqueConverterTurbine,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.couplings._2652": ["BeltDrive"],
        "_private.system_model.part_model.couplings._2653": ["BeltDriveType"],
        "_private.system_model.part_model.couplings._2654": ["Clutch"],
        "_private.system_model.part_model.couplings._2655": ["ClutchHalf"],
        "_private.system_model.part_model.couplings._2656": ["ClutchType"],
        "_private.system_model.part_model.couplings._2657": ["ConceptCoupling"],
        "_private.system_model.part_model.couplings._2658": ["ConceptCouplingHalf"],
        "_private.system_model.part_model.couplings._2659": [
            "ConceptCouplingHalfPositioning"
        ],
        "_private.system_model.part_model.couplings._2660": ["Coupling"],
        "_private.system_model.part_model.couplings._2661": ["CouplingHalf"],
        "_private.system_model.part_model.couplings._2662": ["CrowningSpecification"],
        "_private.system_model.part_model.couplings._2663": ["CVT"],
        "_private.system_model.part_model.couplings._2664": ["CVTPulley"],
        "_private.system_model.part_model.couplings._2665": ["PartToPartShearCoupling"],
        "_private.system_model.part_model.couplings._2666": [
            "PartToPartShearCouplingHalf"
        ],
        "_private.system_model.part_model.couplings._2667": ["PitchErrorFlankOptions"],
        "_private.system_model.part_model.couplings._2668": ["Pulley"],
        "_private.system_model.part_model.couplings._2669": ["RigidConnectorSettings"],
        "_private.system_model.part_model.couplings._2670": [
            "RigidConnectorStiffnessType"
        ],
        "_private.system_model.part_model.couplings._2671": [
            "RigidConnectorTiltStiffnessTypes"
        ],
        "_private.system_model.part_model.couplings._2672": [
            "RigidConnectorToothLocation"
        ],
        "_private.system_model.part_model.couplings._2673": [
            "RigidConnectorToothSpacingType"
        ],
        "_private.system_model.part_model.couplings._2674": ["RigidConnectorTypes"],
        "_private.system_model.part_model.couplings._2675": ["RollingRing"],
        "_private.system_model.part_model.couplings._2676": ["RollingRingAssembly"],
        "_private.system_model.part_model.couplings._2677": ["ShaftHubConnection"],
        "_private.system_model.part_model.couplings._2678": ["SplineFitOptions"],
        "_private.system_model.part_model.couplings._2679": [
            "SplineHalfManufacturingError"
        ],
        "_private.system_model.part_model.couplings._2680": ["SplineLeadRelief"],
        "_private.system_model.part_model.couplings._2681": [
            "SplinePitchErrorInputType"
        ],
        "_private.system_model.part_model.couplings._2682": ["SplinePitchErrorOptions"],
        "_private.system_model.part_model.couplings._2683": ["SpringDamper"],
        "_private.system_model.part_model.couplings._2684": ["SpringDamperHalf"],
        "_private.system_model.part_model.couplings._2685": ["Synchroniser"],
        "_private.system_model.part_model.couplings._2686": ["SynchroniserCone"],
        "_private.system_model.part_model.couplings._2687": ["SynchroniserHalf"],
        "_private.system_model.part_model.couplings._2688": ["SynchroniserPart"],
        "_private.system_model.part_model.couplings._2689": ["SynchroniserSleeve"],
        "_private.system_model.part_model.couplings._2690": ["TorqueConverter"],
        "_private.system_model.part_model.couplings._2691": ["TorqueConverterPump"],
        "_private.system_model.part_model.couplings._2692": [
            "TorqueConverterSpeedRatio"
        ],
        "_private.system_model.part_model.couplings._2693": ["TorqueConverterTurbine"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BeltDrive",
    "BeltDriveType",
    "Clutch",
    "ClutchHalf",
    "ClutchType",
    "ConceptCoupling",
    "ConceptCouplingHalf",
    "ConceptCouplingHalfPositioning",
    "Coupling",
    "CouplingHalf",
    "CrowningSpecification",
    "CVT",
    "CVTPulley",
    "PartToPartShearCoupling",
    "PartToPartShearCouplingHalf",
    "PitchErrorFlankOptions",
    "Pulley",
    "RigidConnectorSettings",
    "RigidConnectorStiffnessType",
    "RigidConnectorTiltStiffnessTypes",
    "RigidConnectorToothLocation",
    "RigidConnectorToothSpacingType",
    "RigidConnectorTypes",
    "RollingRing",
    "RollingRingAssembly",
    "ShaftHubConnection",
    "SplineFitOptions",
    "SplineHalfManufacturingError",
    "SplineLeadRelief",
    "SplinePitchErrorInputType",
    "SplinePitchErrorOptions",
    "SpringDamper",
    "SpringDamperHalf",
    "Synchroniser",
    "SynchroniserCone",
    "SynchroniserHalf",
    "SynchroniserPart",
    "SynchroniserSleeve",
    "TorqueConverter",
    "TorqueConverterPump",
    "TorqueConverterSpeedRatio",
    "TorqueConverterTurbine",
)
