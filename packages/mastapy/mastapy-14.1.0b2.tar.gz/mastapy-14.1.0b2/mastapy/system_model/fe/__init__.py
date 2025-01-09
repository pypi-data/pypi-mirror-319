"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.fe._2424 import AlignConnectedComponentOptions
    from mastapy._private.system_model.fe._2425 import AlignmentMethod
    from mastapy._private.system_model.fe._2426 import AlignmentMethodForRaceBearing
    from mastapy._private.system_model.fe._2427 import AlignmentUsingAxialNodePositions
    from mastapy._private.system_model.fe._2428 import AngleSource
    from mastapy._private.system_model.fe._2429 import BaseFEWithSelection
    from mastapy._private.system_model.fe._2430 import BatchOperations
    from mastapy._private.system_model.fe._2431 import BearingNodeAlignmentOption
    from mastapy._private.system_model.fe._2432 import BearingNodeOption
    from mastapy._private.system_model.fe._2433 import BearingRaceNodeLink
    from mastapy._private.system_model.fe._2434 import BearingRacePosition
    from mastapy._private.system_model.fe._2435 import ComponentOrientationOption
    from mastapy._private.system_model.fe._2436 import ContactPairWithSelection
    from mastapy._private.system_model.fe._2437 import CoordinateSystemWithSelection
    from mastapy._private.system_model.fe._2438 import CreateConnectedComponentOptions
    from mastapy._private.system_model.fe._2439 import (
        CreateMicrophoneNormalToSurfaceOptions,
    )
    from mastapy._private.system_model.fe._2440 import DegreeOfFreedomBoundaryCondition
    from mastapy._private.system_model.fe._2441 import (
        DegreeOfFreedomBoundaryConditionAngular,
    )
    from mastapy._private.system_model.fe._2442 import (
        DegreeOfFreedomBoundaryConditionLinear,
    )
    from mastapy._private.system_model.fe._2443 import ElectricMachineDataSet
    from mastapy._private.system_model.fe._2444 import ElectricMachineDynamicLoadData
    from mastapy._private.system_model.fe._2445 import ElementFaceGroupWithSelection
    from mastapy._private.system_model.fe._2446 import ElementPropertiesWithSelection
    from mastapy._private.system_model.fe._2447 import FEEntityGroupWithSelection
    from mastapy._private.system_model.fe._2448 import FEExportSettings
    from mastapy._private.system_model.fe._2449 import FEPartDRIVASurfaceSelection
    from mastapy._private.system_model.fe._2450 import FEPartWithBatchOptions
    from mastapy._private.system_model.fe._2451 import FEStiffnessGeometry
    from mastapy._private.system_model.fe._2452 import FEStiffnessTester
    from mastapy._private.system_model.fe._2453 import FESubstructure
    from mastapy._private.system_model.fe._2454 import FESubstructureExportOptions
    from mastapy._private.system_model.fe._2455 import FESubstructureNode
    from mastapy._private.system_model.fe._2456 import FESubstructureNodeModeShape
    from mastapy._private.system_model.fe._2457 import FESubstructureNodeModeShapes
    from mastapy._private.system_model.fe._2458 import FESubstructureType
    from mastapy._private.system_model.fe._2459 import FESubstructureWithBatchOptions
    from mastapy._private.system_model.fe._2460 import FESubstructureWithSelection
    from mastapy._private.system_model.fe._2461 import (
        FESubstructureWithSelectionComponents,
    )
    from mastapy._private.system_model.fe._2462 import (
        FESubstructureWithSelectionForHarmonicAnalysis,
    )
    from mastapy._private.system_model.fe._2463 import (
        FESubstructureWithSelectionForModalAnalysis,
    )
    from mastapy._private.system_model.fe._2464 import (
        FESubstructureWithSelectionForStaticAnalysis,
    )
    from mastapy._private.system_model.fe._2465 import GearMeshingOptions
    from mastapy._private.system_model.fe._2466 import (
        IndependentMASTACreatedCondensationNode,
    )
    from mastapy._private.system_model.fe._2467 import (
        LinkComponentAxialPositionErrorReporter,
    )
    from mastapy._private.system_model.fe._2468 import LinkNodeSource
    from mastapy._private.system_model.fe._2469 import MaterialPropertiesWithSelection
    from mastapy._private.system_model.fe._2470 import (
        NodeBoundaryConditionStaticAnalysis,
    )
    from mastapy._private.system_model.fe._2471 import NodeGroupWithSelection
    from mastapy._private.system_model.fe._2472 import NodeSelectionDepthOption
    from mastapy._private.system_model.fe._2473 import (
        OptionsWhenExternalFEFileAlreadyExists,
    )
    from mastapy._private.system_model.fe._2474 import PerLinkExportOptions
    from mastapy._private.system_model.fe._2475 import PerNodeExportOptions
    from mastapy._private.system_model.fe._2476 import RaceBearingFE
    from mastapy._private.system_model.fe._2477 import RaceBearingFESystemDeflection
    from mastapy._private.system_model.fe._2478 import RaceBearingFEWithSelection
    from mastapy._private.system_model.fe._2479 import ReplacedShaftSelectionHelper
    from mastapy._private.system_model.fe._2480 import SystemDeflectionFEExportOptions
    from mastapy._private.system_model.fe._2481 import ThermalExpansionOption
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.fe._2424": ["AlignConnectedComponentOptions"],
        "_private.system_model.fe._2425": ["AlignmentMethod"],
        "_private.system_model.fe._2426": ["AlignmentMethodForRaceBearing"],
        "_private.system_model.fe._2427": ["AlignmentUsingAxialNodePositions"],
        "_private.system_model.fe._2428": ["AngleSource"],
        "_private.system_model.fe._2429": ["BaseFEWithSelection"],
        "_private.system_model.fe._2430": ["BatchOperations"],
        "_private.system_model.fe._2431": ["BearingNodeAlignmentOption"],
        "_private.system_model.fe._2432": ["BearingNodeOption"],
        "_private.system_model.fe._2433": ["BearingRaceNodeLink"],
        "_private.system_model.fe._2434": ["BearingRacePosition"],
        "_private.system_model.fe._2435": ["ComponentOrientationOption"],
        "_private.system_model.fe._2436": ["ContactPairWithSelection"],
        "_private.system_model.fe._2437": ["CoordinateSystemWithSelection"],
        "_private.system_model.fe._2438": ["CreateConnectedComponentOptions"],
        "_private.system_model.fe._2439": ["CreateMicrophoneNormalToSurfaceOptions"],
        "_private.system_model.fe._2440": ["DegreeOfFreedomBoundaryCondition"],
        "_private.system_model.fe._2441": ["DegreeOfFreedomBoundaryConditionAngular"],
        "_private.system_model.fe._2442": ["DegreeOfFreedomBoundaryConditionLinear"],
        "_private.system_model.fe._2443": ["ElectricMachineDataSet"],
        "_private.system_model.fe._2444": ["ElectricMachineDynamicLoadData"],
        "_private.system_model.fe._2445": ["ElementFaceGroupWithSelection"],
        "_private.system_model.fe._2446": ["ElementPropertiesWithSelection"],
        "_private.system_model.fe._2447": ["FEEntityGroupWithSelection"],
        "_private.system_model.fe._2448": ["FEExportSettings"],
        "_private.system_model.fe._2449": ["FEPartDRIVASurfaceSelection"],
        "_private.system_model.fe._2450": ["FEPartWithBatchOptions"],
        "_private.system_model.fe._2451": ["FEStiffnessGeometry"],
        "_private.system_model.fe._2452": ["FEStiffnessTester"],
        "_private.system_model.fe._2453": ["FESubstructure"],
        "_private.system_model.fe._2454": ["FESubstructureExportOptions"],
        "_private.system_model.fe._2455": ["FESubstructureNode"],
        "_private.system_model.fe._2456": ["FESubstructureNodeModeShape"],
        "_private.system_model.fe._2457": ["FESubstructureNodeModeShapes"],
        "_private.system_model.fe._2458": ["FESubstructureType"],
        "_private.system_model.fe._2459": ["FESubstructureWithBatchOptions"],
        "_private.system_model.fe._2460": ["FESubstructureWithSelection"],
        "_private.system_model.fe._2461": ["FESubstructureWithSelectionComponents"],
        "_private.system_model.fe._2462": [
            "FESubstructureWithSelectionForHarmonicAnalysis"
        ],
        "_private.system_model.fe._2463": [
            "FESubstructureWithSelectionForModalAnalysis"
        ],
        "_private.system_model.fe._2464": [
            "FESubstructureWithSelectionForStaticAnalysis"
        ],
        "_private.system_model.fe._2465": ["GearMeshingOptions"],
        "_private.system_model.fe._2466": ["IndependentMASTACreatedCondensationNode"],
        "_private.system_model.fe._2467": ["LinkComponentAxialPositionErrorReporter"],
        "_private.system_model.fe._2468": ["LinkNodeSource"],
        "_private.system_model.fe._2469": ["MaterialPropertiesWithSelection"],
        "_private.system_model.fe._2470": ["NodeBoundaryConditionStaticAnalysis"],
        "_private.system_model.fe._2471": ["NodeGroupWithSelection"],
        "_private.system_model.fe._2472": ["NodeSelectionDepthOption"],
        "_private.system_model.fe._2473": ["OptionsWhenExternalFEFileAlreadyExists"],
        "_private.system_model.fe._2474": ["PerLinkExportOptions"],
        "_private.system_model.fe._2475": ["PerNodeExportOptions"],
        "_private.system_model.fe._2476": ["RaceBearingFE"],
        "_private.system_model.fe._2477": ["RaceBearingFESystemDeflection"],
        "_private.system_model.fe._2478": ["RaceBearingFEWithSelection"],
        "_private.system_model.fe._2479": ["ReplacedShaftSelectionHelper"],
        "_private.system_model.fe._2480": ["SystemDeflectionFEExportOptions"],
        "_private.system_model.fe._2481": ["ThermalExpansionOption"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AlignConnectedComponentOptions",
    "AlignmentMethod",
    "AlignmentMethodForRaceBearing",
    "AlignmentUsingAxialNodePositions",
    "AngleSource",
    "BaseFEWithSelection",
    "BatchOperations",
    "BearingNodeAlignmentOption",
    "BearingNodeOption",
    "BearingRaceNodeLink",
    "BearingRacePosition",
    "ComponentOrientationOption",
    "ContactPairWithSelection",
    "CoordinateSystemWithSelection",
    "CreateConnectedComponentOptions",
    "CreateMicrophoneNormalToSurfaceOptions",
    "DegreeOfFreedomBoundaryCondition",
    "DegreeOfFreedomBoundaryConditionAngular",
    "DegreeOfFreedomBoundaryConditionLinear",
    "ElectricMachineDataSet",
    "ElectricMachineDynamicLoadData",
    "ElementFaceGroupWithSelection",
    "ElementPropertiesWithSelection",
    "FEEntityGroupWithSelection",
    "FEExportSettings",
    "FEPartDRIVASurfaceSelection",
    "FEPartWithBatchOptions",
    "FEStiffnessGeometry",
    "FEStiffnessTester",
    "FESubstructure",
    "FESubstructureExportOptions",
    "FESubstructureNode",
    "FESubstructureNodeModeShape",
    "FESubstructureNodeModeShapes",
    "FESubstructureType",
    "FESubstructureWithBatchOptions",
    "FESubstructureWithSelection",
    "FESubstructureWithSelectionComponents",
    "FESubstructureWithSelectionForHarmonicAnalysis",
    "FESubstructureWithSelectionForModalAnalysis",
    "FESubstructureWithSelectionForStaticAnalysis",
    "GearMeshingOptions",
    "IndependentMASTACreatedCondensationNode",
    "LinkComponentAxialPositionErrorReporter",
    "LinkNodeSource",
    "MaterialPropertiesWithSelection",
    "NodeBoundaryConditionStaticAnalysis",
    "NodeGroupWithSelection",
    "NodeSelectionDepthOption",
    "OptionsWhenExternalFEFileAlreadyExists",
    "PerLinkExportOptions",
    "PerNodeExportOptions",
    "RaceBearingFE",
    "RaceBearingFESystemDeflection",
    "RaceBearingFEWithSelection",
    "ReplacedShaftSelectionHelper",
    "SystemDeflectionFEExportOptions",
    "ThermalExpansionOption",
)
