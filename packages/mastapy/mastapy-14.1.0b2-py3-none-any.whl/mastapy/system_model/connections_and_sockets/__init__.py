"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.connections_and_sockets._2334 import (
        AbstractShaftToMountableComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2335 import (
        BearingInnerSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2336 import (
        BearingOuterSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2337 import (
        BeltConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2338 import (
        CoaxialConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2339 import (
        ComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2340 import (
        ComponentMeasurer,
    )
    from mastapy._private.system_model.connections_and_sockets._2341 import Connection
    from mastapy._private.system_model.connections_and_sockets._2342 import (
        CVTBeltConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2343 import (
        CVTPulleySocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2344 import (
        CylindricalComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2345 import (
        CylindricalSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2346 import (
        DatumMeasurement,
    )
    from mastapy._private.system_model.connections_and_sockets._2347 import (
        ElectricMachineStatorSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2348 import (
        InnerShaftSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2349 import (
        InnerShaftSocketBase,
    )
    from mastapy._private.system_model.connections_and_sockets._2350 import (
        InterMountableComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2351 import (
        MountableComponentInnerSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2352 import (
        MountableComponentOuterSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2353 import (
        MountableComponentSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2354 import (
        OuterShaftSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2355 import (
        OuterShaftSocketBase,
    )
    from mastapy._private.system_model.connections_and_sockets._2356 import (
        PlanetaryConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2357 import (
        PlanetarySocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2358 import (
        PlanetarySocketBase,
    )
    from mastapy._private.system_model.connections_and_sockets._2359 import PulleySocket
    from mastapy._private.system_model.connections_and_sockets._2360 import (
        RealignmentResult,
    )
    from mastapy._private.system_model.connections_and_sockets._2361 import (
        RollingRingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2362 import (
        RollingRingSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2363 import ShaftSocket
    from mastapy._private.system_model.connections_and_sockets._2364 import (
        ShaftToMountableComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2365 import Socket
    from mastapy._private.system_model.connections_and_sockets._2366 import (
        SocketConnectionOptions,
    )
    from mastapy._private.system_model.connections_and_sockets._2367 import (
        SocketConnectionSelection,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.connections_and_sockets._2334": [
            "AbstractShaftToMountableComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2335": ["BearingInnerSocket"],
        "_private.system_model.connections_and_sockets._2336": ["BearingOuterSocket"],
        "_private.system_model.connections_and_sockets._2337": ["BeltConnection"],
        "_private.system_model.connections_and_sockets._2338": ["CoaxialConnection"],
        "_private.system_model.connections_and_sockets._2339": ["ComponentConnection"],
        "_private.system_model.connections_and_sockets._2340": ["ComponentMeasurer"],
        "_private.system_model.connections_and_sockets._2341": ["Connection"],
        "_private.system_model.connections_and_sockets._2342": ["CVTBeltConnection"],
        "_private.system_model.connections_and_sockets._2343": ["CVTPulleySocket"],
        "_private.system_model.connections_and_sockets._2344": [
            "CylindricalComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2345": ["CylindricalSocket"],
        "_private.system_model.connections_and_sockets._2346": ["DatumMeasurement"],
        "_private.system_model.connections_and_sockets._2347": [
            "ElectricMachineStatorSocket"
        ],
        "_private.system_model.connections_and_sockets._2348": ["InnerShaftSocket"],
        "_private.system_model.connections_and_sockets._2349": ["InnerShaftSocketBase"],
        "_private.system_model.connections_and_sockets._2350": [
            "InterMountableComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2351": [
            "MountableComponentInnerSocket"
        ],
        "_private.system_model.connections_and_sockets._2352": [
            "MountableComponentOuterSocket"
        ],
        "_private.system_model.connections_and_sockets._2353": [
            "MountableComponentSocket"
        ],
        "_private.system_model.connections_and_sockets._2354": ["OuterShaftSocket"],
        "_private.system_model.connections_and_sockets._2355": ["OuterShaftSocketBase"],
        "_private.system_model.connections_and_sockets._2356": ["PlanetaryConnection"],
        "_private.system_model.connections_and_sockets._2357": ["PlanetarySocket"],
        "_private.system_model.connections_and_sockets._2358": ["PlanetarySocketBase"],
        "_private.system_model.connections_and_sockets._2359": ["PulleySocket"],
        "_private.system_model.connections_and_sockets._2360": ["RealignmentResult"],
        "_private.system_model.connections_and_sockets._2361": [
            "RollingRingConnection"
        ],
        "_private.system_model.connections_and_sockets._2362": ["RollingRingSocket"],
        "_private.system_model.connections_and_sockets._2363": ["ShaftSocket"],
        "_private.system_model.connections_and_sockets._2364": [
            "ShaftToMountableComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2365": ["Socket"],
        "_private.system_model.connections_and_sockets._2366": [
            "SocketConnectionOptions"
        ],
        "_private.system_model.connections_and_sockets._2367": [
            "SocketConnectionSelection"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractShaftToMountableComponentConnection",
    "BearingInnerSocket",
    "BearingOuterSocket",
    "BeltConnection",
    "CoaxialConnection",
    "ComponentConnection",
    "ComponentMeasurer",
    "Connection",
    "CVTBeltConnection",
    "CVTPulleySocket",
    "CylindricalComponentConnection",
    "CylindricalSocket",
    "DatumMeasurement",
    "ElectricMachineStatorSocket",
    "InnerShaftSocket",
    "InnerShaftSocketBase",
    "InterMountableComponentConnection",
    "MountableComponentInnerSocket",
    "MountableComponentOuterSocket",
    "MountableComponentSocket",
    "OuterShaftSocket",
    "OuterShaftSocketBase",
    "PlanetaryConnection",
    "PlanetarySocket",
    "PlanetarySocketBase",
    "PulleySocket",
    "RealignmentResult",
    "RollingRingConnection",
    "RollingRingSocket",
    "ShaftSocket",
    "ShaftToMountableComponentConnection",
    "Socket",
    "SocketConnectionOptions",
    "SocketConnectionSelection",
)
