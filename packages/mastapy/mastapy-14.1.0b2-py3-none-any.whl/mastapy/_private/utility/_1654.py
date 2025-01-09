"""PerMachineSettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)
from mastapy._private.utility import _1655

_PER_MACHINE_SETTINGS = python_net_import("SMT.MastaAPI.Utility", "PerMachineSettings")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _1966
    from mastapy._private.gears.gear_designs.cylindrical import _1049
    from mastapy._private.gears.ltca.cylindrical import _886
    from mastapy._private.gears.materials import _618
    from mastapy._private.nodal_analysis import _71
    from mastapy._private.nodal_analysis.geometry_modeller_link import _172
    from mastapy._private.system_model.part_model import _2542
    from mastapy._private.utility import _1656, _1657
    from mastapy._private.utility.cad_export import _1898
    from mastapy._private.utility.databases import _1893
    from mastapy._private.utility.scripting import _1801
    from mastapy._private.utility.units_and_measurements import _1667

    Self = TypeVar("Self", bound="PerMachineSettings")
    CastSelf = TypeVar("CastSelf", bound="PerMachineSettings._Cast_PerMachineSettings")


__docformat__ = "restructuredtext en"
__all__ = ("PerMachineSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PerMachineSettings:
    """Special nested class for casting PerMachineSettings to subclasses."""

    __parent__: "PerMachineSettings"

    @property
    def persistent_singleton(self: "CastSelf") -> "_1655.PersistentSingleton":
        return self.__parent__._cast(_1655.PersistentSingleton)

    @property
    def fe_user_settings(self: "CastSelf") -> "_71.FEUserSettings":
        from mastapy._private.nodal_analysis import _71

        return self.__parent__._cast(_71.FEUserSettings)

    @property
    def geometry_modeller_settings(self: "CastSelf") -> "_172.GeometryModellerSettings":
        from mastapy._private.nodal_analysis.geometry_modeller_link import _172

        return self.__parent__._cast(_172.GeometryModellerSettings)

    @property
    def gear_material_expert_system_factor_settings(
        self: "CastSelf",
    ) -> "_618.GearMaterialExpertSystemFactorSettings":
        from mastapy._private.gears.materials import _618

        return self.__parent__._cast(_618.GearMaterialExpertSystemFactorSettings)

    @property
    def cylindrical_gear_fe_settings(
        self: "CastSelf",
    ) -> "_886.CylindricalGearFESettings":
        from mastapy._private.gears.ltca.cylindrical import _886

        return self.__parent__._cast(_886.CylindricalGearFESettings)

    @property
    def cylindrical_gear_defaults(self: "CastSelf") -> "_1049.CylindricalGearDefaults":
        from mastapy._private.gears.gear_designs.cylindrical import _1049

        return self.__parent__._cast(_1049.CylindricalGearDefaults)

    @property
    def program_settings(self: "CastSelf") -> "_1656.ProgramSettings":
        from mastapy._private.utility import _1656

        return self.__parent__._cast(_1656.ProgramSettings)

    @property
    def pushbullet_settings(self: "CastSelf") -> "_1657.PushbulletSettings":
        from mastapy._private.utility import _1657

        return self.__parent__._cast(_1657.PushbulletSettings)

    @property
    def measurement_settings(self: "CastSelf") -> "_1667.MeasurementSettings":
        from mastapy._private.utility.units_and_measurements import _1667

        return self.__parent__._cast(_1667.MeasurementSettings)

    @property
    def scripting_setup(self: "CastSelf") -> "_1801.ScriptingSetup":
        from mastapy._private.utility.scripting import _1801

        return self.__parent__._cast(_1801.ScriptingSetup)

    @property
    def database_settings(self: "CastSelf") -> "_1893.DatabaseSettings":
        from mastapy._private.utility.databases import _1893

        return self.__parent__._cast(_1893.DatabaseSettings)

    @property
    def cad_export_settings(self: "CastSelf") -> "_1898.CADExportSettings":
        from mastapy._private.utility.cad_export import _1898

        return self.__parent__._cast(_1898.CADExportSettings)

    @property
    def skf_settings(self: "CastSelf") -> "_1966.SKFSettings":
        from mastapy._private.bearings import _1966

        return self.__parent__._cast(_1966.SKFSettings)

    @property
    def planet_carrier_settings(self: "CastSelf") -> "_2542.PlanetCarrierSettings":
        from mastapy._private.system_model.part_model import _2542

        return self.__parent__._cast(_2542.PlanetCarrierSettings)

    @property
    def per_machine_settings(self: "CastSelf") -> "PerMachineSettings":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class PerMachineSettings(_1655.PersistentSingleton):
    """PerMachineSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PER_MACHINE_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    def reset_to_defaults(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ResetToDefaults")

    @property
    def cast_to(self: "Self") -> "_Cast_PerMachineSettings":
        """Cast to another type.

        Returns:
            _Cast_PerMachineSettings
        """
        return _Cast_PerMachineSettings(self)
