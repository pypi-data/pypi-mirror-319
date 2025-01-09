"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.import_from_cad._2566 import (
        AbstractShaftFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2567 import (
        ClutchFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2568 import (
        ComponentFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2569 import (
        ComponentFromCADBase,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2570 import (
        ConceptBearingFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2571 import (
        ConnectorFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2572 import (
        CylindricalGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2573 import (
        CylindricalGearInPlanetarySetFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2574 import (
        CylindricalPlanetGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2575 import (
        CylindricalRingGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2576 import (
        CylindricalSunGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2577 import (
        HousedOrMounted,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2578 import (
        MountableComponentFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2579 import (
        PlanetShaftFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2580 import (
        PulleyFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2581 import (
        RigidConnectorFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2582 import (
        RollingBearingFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2583 import (
        ShaftFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2584 import (
        ShaftFromCADAuto,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.import_from_cad._2566": [
            "AbstractShaftFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2567": ["ClutchFromCAD"],
        "_private.system_model.part_model.import_from_cad._2568": ["ComponentFromCAD"],
        "_private.system_model.part_model.import_from_cad._2569": [
            "ComponentFromCADBase"
        ],
        "_private.system_model.part_model.import_from_cad._2570": [
            "ConceptBearingFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2571": ["ConnectorFromCAD"],
        "_private.system_model.part_model.import_from_cad._2572": [
            "CylindricalGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2573": [
            "CylindricalGearInPlanetarySetFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2574": [
            "CylindricalPlanetGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2575": [
            "CylindricalRingGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2576": [
            "CylindricalSunGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2577": ["HousedOrMounted"],
        "_private.system_model.part_model.import_from_cad._2578": [
            "MountableComponentFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2579": [
            "PlanetShaftFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2580": ["PulleyFromCAD"],
        "_private.system_model.part_model.import_from_cad._2581": [
            "RigidConnectorFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2582": [
            "RollingBearingFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2583": ["ShaftFromCAD"],
        "_private.system_model.part_model.import_from_cad._2584": ["ShaftFromCADAuto"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractShaftFromCAD",
    "ClutchFromCAD",
    "ComponentFromCAD",
    "ComponentFromCADBase",
    "ConceptBearingFromCAD",
    "ConnectorFromCAD",
    "CylindricalGearFromCAD",
    "CylindricalGearInPlanetarySetFromCAD",
    "CylindricalPlanetGearFromCAD",
    "CylindricalRingGearFromCAD",
    "CylindricalSunGearFromCAD",
    "HousedOrMounted",
    "MountableComponentFromCAD",
    "PlanetShaftFromCAD",
    "PulleyFromCAD",
    "RigidConnectorFromCAD",
    "RollingBearingFromCAD",
    "ShaftFromCAD",
    "ShaftFromCADAuto",
)
