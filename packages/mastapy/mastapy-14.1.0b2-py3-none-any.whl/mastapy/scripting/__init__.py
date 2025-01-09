"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.scripting._7726 import ApiEnumForAttribute
    from mastapy._private.scripting._7727 import ApiVersion
    from mastapy._private.scripting._7728 import SMTBitmap
    from mastapy._private.scripting._7730 import MastaPropertyAttribute
    from mastapy._private.scripting._7731 import PythonCommand
    from mastapy._private.scripting._7732 import ScriptingCommand
    from mastapy._private.scripting._7733 import ScriptingExecutionCommand
    from mastapy._private.scripting._7734 import ScriptingObjectCommand
    from mastapy._private.scripting._7735 import ApiVersioning
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.scripting._7726": ["ApiEnumForAttribute"],
        "_private.scripting._7727": ["ApiVersion"],
        "_private.scripting._7728": ["SMTBitmap"],
        "_private.scripting._7730": ["MastaPropertyAttribute"],
        "_private.scripting._7731": ["PythonCommand"],
        "_private.scripting._7732": ["ScriptingCommand"],
        "_private.scripting._7733": ["ScriptingExecutionCommand"],
        "_private.scripting._7734": ["ScriptingObjectCommand"],
        "_private.scripting._7735": ["ApiVersioning"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ApiEnumForAttribute",
    "ApiVersion",
    "SMTBitmap",
    "MastaPropertyAttribute",
    "PythonCommand",
    "ScriptingCommand",
    "ScriptingExecutionCommand",
    "ScriptingObjectCommand",
    "ApiVersioning",
)
