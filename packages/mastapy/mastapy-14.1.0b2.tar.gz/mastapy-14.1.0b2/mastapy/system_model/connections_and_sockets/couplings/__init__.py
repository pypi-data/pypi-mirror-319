"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.connections_and_sockets.couplings._2411 import (
        ClutchConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2412 import (
        ClutchSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2413 import (
        ConceptCouplingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2414 import (
        ConceptCouplingSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2415 import (
        CouplingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2416 import (
        CouplingSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2417 import (
        PartToPartShearCouplingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2418 import (
        PartToPartShearCouplingSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2419 import (
        SpringDamperConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2420 import (
        SpringDamperSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2421 import (
        TorqueConverterConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2422 import (
        TorqueConverterPumpSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2423 import (
        TorqueConverterTurbineSocket,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.connections_and_sockets.couplings._2411": [
            "ClutchConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2412": [
            "ClutchSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2413": [
            "ConceptCouplingConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2414": [
            "ConceptCouplingSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2415": [
            "CouplingConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2416": [
            "CouplingSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2417": [
            "PartToPartShearCouplingConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2418": [
            "PartToPartShearCouplingSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2419": [
            "SpringDamperConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2420": [
            "SpringDamperSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2421": [
            "TorqueConverterConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2422": [
            "TorqueConverterPumpSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2423": [
            "TorqueConverterTurbineSocket"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ClutchConnection",
    "ClutchSocket",
    "ConceptCouplingConnection",
    "ConceptCouplingSocket",
    "CouplingConnection",
    "CouplingSocket",
    "PartToPartShearCouplingConnection",
    "PartToPartShearCouplingSocket",
    "SpringDamperConnection",
    "SpringDamperSocket",
    "TorqueConverterConnection",
    "TorqueConverterPumpSocket",
    "TorqueConverterTurbineSocket",
)
