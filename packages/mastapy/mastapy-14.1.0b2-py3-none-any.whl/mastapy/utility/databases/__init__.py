"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.databases._1890 import Database
    from mastapy._private.utility.databases._1891 import DatabaseConnectionSettings
    from mastapy._private.utility.databases._1892 import DatabaseKey
    from mastapy._private.utility.databases._1893 import DatabaseSettings
    from mastapy._private.utility.databases._1894 import NamedDatabase
    from mastapy._private.utility.databases._1895 import NamedDatabaseItem
    from mastapy._private.utility.databases._1896 import NamedKey
    from mastapy._private.utility.databases._1897 import SQLDatabase
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.databases._1890": ["Database"],
        "_private.utility.databases._1891": ["DatabaseConnectionSettings"],
        "_private.utility.databases._1892": ["DatabaseKey"],
        "_private.utility.databases._1893": ["DatabaseSettings"],
        "_private.utility.databases._1894": ["NamedDatabase"],
        "_private.utility.databases._1895": ["NamedDatabaseItem"],
        "_private.utility.databases._1896": ["NamedKey"],
        "_private.utility.databases._1897": ["SQLDatabase"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "Database",
    "DatabaseConnectionSettings",
    "DatabaseKey",
    "DatabaseSettings",
    "NamedDatabase",
    "NamedDatabaseItem",
    "NamedKey",
    "SQLDatabase",
)
