"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model._2503 import Assembly
    from mastapy._private.system_model.part_model._2504 import AbstractAssembly
    from mastapy._private.system_model.part_model._2505 import AbstractShaft
    from mastapy._private.system_model.part_model._2506 import AbstractShaftOrHousing
    from mastapy._private.system_model.part_model._2507 import (
        AGMALoadSharingTableApplicationLevel,
    )
    from mastapy._private.system_model.part_model._2508 import (
        AxialInternalClearanceTolerance,
    )
    from mastapy._private.system_model.part_model._2509 import Bearing
    from mastapy._private.system_model.part_model._2510 import BearingF0InputMethod
    from mastapy._private.system_model.part_model._2511 import (
        BearingRaceMountingOptions,
    )
    from mastapy._private.system_model.part_model._2512 import Bolt
    from mastapy._private.system_model.part_model._2513 import BoltedJoint
    from mastapy._private.system_model.part_model._2514 import Component
    from mastapy._private.system_model.part_model._2515 import ComponentsConnectedResult
    from mastapy._private.system_model.part_model._2516 import ConnectedSockets
    from mastapy._private.system_model.part_model._2517 import Connector
    from mastapy._private.system_model.part_model._2518 import Datum
    from mastapy._private.system_model.part_model._2519 import (
        ElectricMachineSearchRegionSpecificationMethod,
    )
    from mastapy._private.system_model.part_model._2520 import EnginePartLoad
    from mastapy._private.system_model.part_model._2521 import EngineSpeed
    from mastapy._private.system_model.part_model._2522 import ExternalCADModel
    from mastapy._private.system_model.part_model._2523 import FEPart
    from mastapy._private.system_model.part_model._2524 import FlexiblePinAssembly
    from mastapy._private.system_model.part_model._2525 import GuideDxfModel
    from mastapy._private.system_model.part_model._2526 import GuideImage
    from mastapy._private.system_model.part_model._2527 import GuideModelUsage
    from mastapy._private.system_model.part_model._2528 import (
        InnerBearingRaceMountingOptions,
    )
    from mastapy._private.system_model.part_model._2529 import (
        InternalClearanceTolerance,
    )
    from mastapy._private.system_model.part_model._2530 import LoadSharingModes
    from mastapy._private.system_model.part_model._2531 import LoadSharingSettings
    from mastapy._private.system_model.part_model._2532 import MassDisc
    from mastapy._private.system_model.part_model._2533 import MeasurementComponent
    from mastapy._private.system_model.part_model._2534 import Microphone
    from mastapy._private.system_model.part_model._2535 import MicrophoneArray
    from mastapy._private.system_model.part_model._2536 import MountableComponent
    from mastapy._private.system_model.part_model._2537 import OilLevelSpecification
    from mastapy._private.system_model.part_model._2538 import OilSeal
    from mastapy._private.system_model.part_model._2539 import (
        OuterBearingRaceMountingOptions,
    )
    from mastapy._private.system_model.part_model._2540 import Part
    from mastapy._private.system_model.part_model._2541 import PlanetCarrier
    from mastapy._private.system_model.part_model._2542 import PlanetCarrierSettings
    from mastapy._private.system_model.part_model._2543 import PointLoad
    from mastapy._private.system_model.part_model._2544 import PowerLoad
    from mastapy._private.system_model.part_model._2545 import (
        RadialInternalClearanceTolerance,
    )
    from mastapy._private.system_model.part_model._2546 import (
        RollingBearingElementLoadCase,
    )
    from mastapy._private.system_model.part_model._2547 import RootAssembly
    from mastapy._private.system_model.part_model._2548 import (
        ShaftDiameterModificationDueToRollingBearingRing,
    )
    from mastapy._private.system_model.part_model._2549 import SpecialisedAssembly
    from mastapy._private.system_model.part_model._2550 import UnbalancedMass
    from mastapy._private.system_model.part_model._2551 import (
        UnbalancedMassInclusionOption,
    )
    from mastapy._private.system_model.part_model._2552 import VirtualComponent
    from mastapy._private.system_model.part_model._2553 import (
        WindTurbineBladeModeDetails,
    )
    from mastapy._private.system_model.part_model._2554 import (
        WindTurbineSingleBladeDetails,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model._2503": ["Assembly"],
        "_private.system_model.part_model._2504": ["AbstractAssembly"],
        "_private.system_model.part_model._2505": ["AbstractShaft"],
        "_private.system_model.part_model._2506": ["AbstractShaftOrHousing"],
        "_private.system_model.part_model._2507": [
            "AGMALoadSharingTableApplicationLevel"
        ],
        "_private.system_model.part_model._2508": ["AxialInternalClearanceTolerance"],
        "_private.system_model.part_model._2509": ["Bearing"],
        "_private.system_model.part_model._2510": ["BearingF0InputMethod"],
        "_private.system_model.part_model._2511": ["BearingRaceMountingOptions"],
        "_private.system_model.part_model._2512": ["Bolt"],
        "_private.system_model.part_model._2513": ["BoltedJoint"],
        "_private.system_model.part_model._2514": ["Component"],
        "_private.system_model.part_model._2515": ["ComponentsConnectedResult"],
        "_private.system_model.part_model._2516": ["ConnectedSockets"],
        "_private.system_model.part_model._2517": ["Connector"],
        "_private.system_model.part_model._2518": ["Datum"],
        "_private.system_model.part_model._2519": [
            "ElectricMachineSearchRegionSpecificationMethod"
        ],
        "_private.system_model.part_model._2520": ["EnginePartLoad"],
        "_private.system_model.part_model._2521": ["EngineSpeed"],
        "_private.system_model.part_model._2522": ["ExternalCADModel"],
        "_private.system_model.part_model._2523": ["FEPart"],
        "_private.system_model.part_model._2524": ["FlexiblePinAssembly"],
        "_private.system_model.part_model._2525": ["GuideDxfModel"],
        "_private.system_model.part_model._2526": ["GuideImage"],
        "_private.system_model.part_model._2527": ["GuideModelUsage"],
        "_private.system_model.part_model._2528": ["InnerBearingRaceMountingOptions"],
        "_private.system_model.part_model._2529": ["InternalClearanceTolerance"],
        "_private.system_model.part_model._2530": ["LoadSharingModes"],
        "_private.system_model.part_model._2531": ["LoadSharingSettings"],
        "_private.system_model.part_model._2532": ["MassDisc"],
        "_private.system_model.part_model._2533": ["MeasurementComponent"],
        "_private.system_model.part_model._2534": ["Microphone"],
        "_private.system_model.part_model._2535": ["MicrophoneArray"],
        "_private.system_model.part_model._2536": ["MountableComponent"],
        "_private.system_model.part_model._2537": ["OilLevelSpecification"],
        "_private.system_model.part_model._2538": ["OilSeal"],
        "_private.system_model.part_model._2539": ["OuterBearingRaceMountingOptions"],
        "_private.system_model.part_model._2540": ["Part"],
        "_private.system_model.part_model._2541": ["PlanetCarrier"],
        "_private.system_model.part_model._2542": ["PlanetCarrierSettings"],
        "_private.system_model.part_model._2543": ["PointLoad"],
        "_private.system_model.part_model._2544": ["PowerLoad"],
        "_private.system_model.part_model._2545": ["RadialInternalClearanceTolerance"],
        "_private.system_model.part_model._2546": ["RollingBearingElementLoadCase"],
        "_private.system_model.part_model._2547": ["RootAssembly"],
        "_private.system_model.part_model._2548": [
            "ShaftDiameterModificationDueToRollingBearingRing"
        ],
        "_private.system_model.part_model._2549": ["SpecialisedAssembly"],
        "_private.system_model.part_model._2550": ["UnbalancedMass"],
        "_private.system_model.part_model._2551": ["UnbalancedMassInclusionOption"],
        "_private.system_model.part_model._2552": ["VirtualComponent"],
        "_private.system_model.part_model._2553": ["WindTurbineBladeModeDetails"],
        "_private.system_model.part_model._2554": ["WindTurbineSingleBladeDetails"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "Assembly",
    "AbstractAssembly",
    "AbstractShaft",
    "AbstractShaftOrHousing",
    "AGMALoadSharingTableApplicationLevel",
    "AxialInternalClearanceTolerance",
    "Bearing",
    "BearingF0InputMethod",
    "BearingRaceMountingOptions",
    "Bolt",
    "BoltedJoint",
    "Component",
    "ComponentsConnectedResult",
    "ConnectedSockets",
    "Connector",
    "Datum",
    "ElectricMachineSearchRegionSpecificationMethod",
    "EnginePartLoad",
    "EngineSpeed",
    "ExternalCADModel",
    "FEPart",
    "FlexiblePinAssembly",
    "GuideDxfModel",
    "GuideImage",
    "GuideModelUsage",
    "InnerBearingRaceMountingOptions",
    "InternalClearanceTolerance",
    "LoadSharingModes",
    "LoadSharingSettings",
    "MassDisc",
    "MeasurementComponent",
    "Microphone",
    "MicrophoneArray",
    "MountableComponent",
    "OilLevelSpecification",
    "OilSeal",
    "OuterBearingRaceMountingOptions",
    "Part",
    "PlanetCarrier",
    "PlanetCarrierSettings",
    "PointLoad",
    "PowerLoad",
    "RadialInternalClearanceTolerance",
    "RollingBearingElementLoadCase",
    "RootAssembly",
    "ShaftDiameterModificationDueToRollingBearingRing",
    "SpecialisedAssembly",
    "UnbalancedMass",
    "UnbalancedMassInclusionOption",
    "VirtualComponent",
    "WindTurbineBladeModeDetails",
    "WindTurbineSingleBladeDetails",
)
