"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.fe.links._2488 import FELink
    from mastapy._private.system_model.fe.links._2489 import ElectricMachineStatorFELink
    from mastapy._private.system_model.fe.links._2490 import FELinkWithSelection
    from mastapy._private.system_model.fe.links._2491 import GearMeshFELink
    from mastapy._private.system_model.fe.links._2492 import (
        GearWithDuplicatedMeshesFELink,
    )
    from mastapy._private.system_model.fe.links._2493 import MultiAngleConnectionFELink
    from mastapy._private.system_model.fe.links._2494 import MultiNodeConnectorFELink
    from mastapy._private.system_model.fe.links._2495 import MultiNodeFELink
    from mastapy._private.system_model.fe.links._2496 import (
        PlanetaryConnectorMultiNodeFELink,
    )
    from mastapy._private.system_model.fe.links._2497 import PlanetBasedFELink
    from mastapy._private.system_model.fe.links._2498 import PlanetCarrierFELink
    from mastapy._private.system_model.fe.links._2499 import PointLoadFELink
    from mastapy._private.system_model.fe.links._2500 import RollingRingConnectionFELink
    from mastapy._private.system_model.fe.links._2501 import ShaftHubConnectionFELink
    from mastapy._private.system_model.fe.links._2502 import SingleNodeFELink
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.fe.links._2488": ["FELink"],
        "_private.system_model.fe.links._2489": ["ElectricMachineStatorFELink"],
        "_private.system_model.fe.links._2490": ["FELinkWithSelection"],
        "_private.system_model.fe.links._2491": ["GearMeshFELink"],
        "_private.system_model.fe.links._2492": ["GearWithDuplicatedMeshesFELink"],
        "_private.system_model.fe.links._2493": ["MultiAngleConnectionFELink"],
        "_private.system_model.fe.links._2494": ["MultiNodeConnectorFELink"],
        "_private.system_model.fe.links._2495": ["MultiNodeFELink"],
        "_private.system_model.fe.links._2496": ["PlanetaryConnectorMultiNodeFELink"],
        "_private.system_model.fe.links._2497": ["PlanetBasedFELink"],
        "_private.system_model.fe.links._2498": ["PlanetCarrierFELink"],
        "_private.system_model.fe.links._2499": ["PointLoadFELink"],
        "_private.system_model.fe.links._2500": ["RollingRingConnectionFELink"],
        "_private.system_model.fe.links._2501": ["ShaftHubConnectionFELink"],
        "_private.system_model.fe.links._2502": ["SingleNodeFELink"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "FELink",
    "ElectricMachineStatorFELink",
    "FELinkWithSelection",
    "GearMeshFELink",
    "GearWithDuplicatedMeshesFELink",
    "MultiAngleConnectionFELink",
    "MultiNodeConnectorFELink",
    "MultiNodeFELink",
    "PlanetaryConnectorMultiNodeFELink",
    "PlanetBasedFELink",
    "PlanetCarrierFELink",
    "PointLoadFELink",
    "RollingRingConnectionFELink",
    "ShaftHubConnectionFELink",
    "SingleNodeFELink",
)
