"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model._2269 import Design
    from mastapy._private.system_model._2270 import ComponentDampingOption
    from mastapy._private.system_model._2271 import (
        ConceptCouplingSpeedRatioSpecificationMethod,
    )
    from mastapy._private.system_model._2272 import DesignEntity
    from mastapy._private.system_model._2273 import DesignEntityId
    from mastapy._private.system_model._2274 import DesignSettings
    from mastapy._private.system_model._2275 import DutyCycleImporter
    from mastapy._private.system_model._2276 import DutyCycleImporterDesignEntityMatch
    from mastapy._private.system_model._2277 import ExternalFullFELoader
    from mastapy._private.system_model._2278 import HypoidWindUpRemovalMethod
    from mastapy._private.system_model._2279 import IncludeDutyCycleOption
    from mastapy._private.system_model._2280 import MAAElectricMachineGroup
    from mastapy._private.system_model._2281 import MASTASettings
    from mastapy._private.system_model._2282 import MemorySummary
    from mastapy._private.system_model._2283 import MeshStiffnessModel
    from mastapy._private.system_model._2284 import (
        PlanetPinManufacturingErrorsCoordinateSystem,
    )
    from mastapy._private.system_model._2285 import (
        PowerLoadDragTorqueSpecificationMethod,
    )
    from mastapy._private.system_model._2286 import (
        PowerLoadInputTorqueSpecificationMethod,
    )
    from mastapy._private.system_model._2287 import PowerLoadPIDControlSpeedInputType
    from mastapy._private.system_model._2288 import PowerLoadType
    from mastapy._private.system_model._2289 import RelativeComponentAlignment
    from mastapy._private.system_model._2290 import RelativeOffsetOption
    from mastapy._private.system_model._2291 import SystemReporting
    from mastapy._private.system_model._2292 import (
        ThermalExpansionOptionForGroundedNodes,
    )
    from mastapy._private.system_model._2293 import TransmissionTemperatureSet
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model._2269": ["Design"],
        "_private.system_model._2270": ["ComponentDampingOption"],
        "_private.system_model._2271": ["ConceptCouplingSpeedRatioSpecificationMethod"],
        "_private.system_model._2272": ["DesignEntity"],
        "_private.system_model._2273": ["DesignEntityId"],
        "_private.system_model._2274": ["DesignSettings"],
        "_private.system_model._2275": ["DutyCycleImporter"],
        "_private.system_model._2276": ["DutyCycleImporterDesignEntityMatch"],
        "_private.system_model._2277": ["ExternalFullFELoader"],
        "_private.system_model._2278": ["HypoidWindUpRemovalMethod"],
        "_private.system_model._2279": ["IncludeDutyCycleOption"],
        "_private.system_model._2280": ["MAAElectricMachineGroup"],
        "_private.system_model._2281": ["MASTASettings"],
        "_private.system_model._2282": ["MemorySummary"],
        "_private.system_model._2283": ["MeshStiffnessModel"],
        "_private.system_model._2284": ["PlanetPinManufacturingErrorsCoordinateSystem"],
        "_private.system_model._2285": ["PowerLoadDragTorqueSpecificationMethod"],
        "_private.system_model._2286": ["PowerLoadInputTorqueSpecificationMethod"],
        "_private.system_model._2287": ["PowerLoadPIDControlSpeedInputType"],
        "_private.system_model._2288": ["PowerLoadType"],
        "_private.system_model._2289": ["RelativeComponentAlignment"],
        "_private.system_model._2290": ["RelativeOffsetOption"],
        "_private.system_model._2291": ["SystemReporting"],
        "_private.system_model._2292": ["ThermalExpansionOptionForGroundedNodes"],
        "_private.system_model._2293": ["TransmissionTemperatureSet"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "Design",
    "ComponentDampingOption",
    "ConceptCouplingSpeedRatioSpecificationMethod",
    "DesignEntity",
    "DesignEntityId",
    "DesignSettings",
    "DutyCycleImporter",
    "DutyCycleImporterDesignEntityMatch",
    "ExternalFullFELoader",
    "HypoidWindUpRemovalMethod",
    "IncludeDutyCycleOption",
    "MAAElectricMachineGroup",
    "MASTASettings",
    "MemorySummary",
    "MeshStiffnessModel",
    "PlanetPinManufacturingErrorsCoordinateSystem",
    "PowerLoadDragTorqueSpecificationMethod",
    "PowerLoadInputTorqueSpecificationMethod",
    "PowerLoadPIDControlSpeedInputType",
    "PowerLoadType",
    "RelativeComponentAlignment",
    "RelativeOffsetOption",
    "SystemReporting",
    "ThermalExpansionOptionForGroundedNodes",
    "TransmissionTemperatureSet",
)
