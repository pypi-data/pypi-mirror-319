"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles._6675 import (
        ExcelBatchDutyCycleCreator,
    )
    from mastapy._private.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles._6676 import (
        ExcelBatchDutyCycleSpectraCreatorDetails,
    )
    from mastapy._private.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles._6677 import (
        ExcelFileDetails,
    )
    from mastapy._private.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles._6678 import (
        ExcelSheet,
    )
    from mastapy._private.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles._6679 import (
        ExcelSheetDesignStateSelector,
    )
    from mastapy._private.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles._6680 import (
        MASTAFileDetails,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles._6675": [
            "ExcelBatchDutyCycleCreator"
        ],
        "_private.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles._6676": [
            "ExcelBatchDutyCycleSpectraCreatorDetails"
        ],
        "_private.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles._6677": [
            "ExcelFileDetails"
        ],
        "_private.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles._6678": [
            "ExcelSheet"
        ],
        "_private.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles._6679": [
            "ExcelSheetDesignStateSelector"
        ],
        "_private.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles._6680": [
            "MASTAFileDetails"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ExcelBatchDutyCycleCreator",
    "ExcelBatchDutyCycleSpectraCreatorDetails",
    "ExcelFileDetails",
    "ExcelSheet",
    "ExcelSheetDesignStateSelector",
    "MASTAFileDetails",
)
