"""DetailedBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_designs import _2202

_DETAILED_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns", "DetailedBearing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_designs import _2198
    from mastapy._private.bearings.bearing_designs.fluid_film import (
        _2256,
        _2258,
        _2260,
        _2262,
        _2263,
        _2264,
    )
    from mastapy._private.bearings.bearing_designs.rolling import (
        _2203,
        _2204,
        _2205,
        _2206,
        _2207,
        _2208,
        _2210,
        _2216,
        _2217,
        _2218,
        _2222,
        _2227,
        _2228,
        _2229,
        _2230,
        _2233,
        _2235,
        _2238,
        _2239,
        _2240,
        _2241,
        _2242,
        _2243,
    )

    Self = TypeVar("Self", bound="DetailedBearing")
    CastSelf = TypeVar("CastSelf", bound="DetailedBearing._Cast_DetailedBearing")


__docformat__ = "restructuredtext en"
__all__ = ("DetailedBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DetailedBearing:
    """Special nested class for casting DetailedBearing to subclasses."""

    __parent__: "DetailedBearing"

    @property
    def non_linear_bearing(self: "CastSelf") -> "_2202.NonLinearBearing":
        return self.__parent__._cast(_2202.NonLinearBearing)

    @property
    def bearing_design(self: "CastSelf") -> "_2198.BearingDesign":
        from mastapy._private.bearings.bearing_designs import _2198

        return self.__parent__._cast(_2198.BearingDesign)

    @property
    def angular_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2203.AngularContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2203

        return self.__parent__._cast(_2203.AngularContactBallBearing)

    @property
    def angular_contact_thrust_ball_bearing(
        self: "CastSelf",
    ) -> "_2204.AngularContactThrustBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2204

        return self.__parent__._cast(_2204.AngularContactThrustBallBearing)

    @property
    def asymmetric_spherical_roller_bearing(
        self: "CastSelf",
    ) -> "_2205.AsymmetricSphericalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2205

        return self.__parent__._cast(_2205.AsymmetricSphericalRollerBearing)

    @property
    def axial_thrust_cylindrical_roller_bearing(
        self: "CastSelf",
    ) -> "_2206.AxialThrustCylindricalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2206

        return self.__parent__._cast(_2206.AxialThrustCylindricalRollerBearing)

    @property
    def axial_thrust_needle_roller_bearing(
        self: "CastSelf",
    ) -> "_2207.AxialThrustNeedleRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2207

        return self.__parent__._cast(_2207.AxialThrustNeedleRollerBearing)

    @property
    def ball_bearing(self: "CastSelf") -> "_2208.BallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2208

        return self.__parent__._cast(_2208.BallBearing)

    @property
    def barrel_roller_bearing(self: "CastSelf") -> "_2210.BarrelRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2210

        return self.__parent__._cast(_2210.BarrelRollerBearing)

    @property
    def crossed_roller_bearing(self: "CastSelf") -> "_2216.CrossedRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2216

        return self.__parent__._cast(_2216.CrossedRollerBearing)

    @property
    def cylindrical_roller_bearing(
        self: "CastSelf",
    ) -> "_2217.CylindricalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2217

        return self.__parent__._cast(_2217.CylindricalRollerBearing)

    @property
    def deep_groove_ball_bearing(self: "CastSelf") -> "_2218.DeepGrooveBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2218

        return self.__parent__._cast(_2218.DeepGrooveBallBearing)

    @property
    def four_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2222.FourPointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2222

        return self.__parent__._cast(_2222.FourPointContactBallBearing)

    @property
    def multi_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2227.MultiPointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2227

        return self.__parent__._cast(_2227.MultiPointContactBallBearing)

    @property
    def needle_roller_bearing(self: "CastSelf") -> "_2228.NeedleRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2228

        return self.__parent__._cast(_2228.NeedleRollerBearing)

    @property
    def non_barrel_roller_bearing(self: "CastSelf") -> "_2229.NonBarrelRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2229

        return self.__parent__._cast(_2229.NonBarrelRollerBearing)

    @property
    def roller_bearing(self: "CastSelf") -> "_2230.RollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2230

        return self.__parent__._cast(_2230.RollerBearing)

    @property
    def rolling_bearing(self: "CastSelf") -> "_2233.RollingBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2233

        return self.__parent__._cast(_2233.RollingBearing)

    @property
    def self_aligning_ball_bearing(self: "CastSelf") -> "_2235.SelfAligningBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2235

        return self.__parent__._cast(_2235.SelfAligningBallBearing)

    @property
    def spherical_roller_bearing(self: "CastSelf") -> "_2238.SphericalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2238

        return self.__parent__._cast(_2238.SphericalRollerBearing)

    @property
    def spherical_roller_thrust_bearing(
        self: "CastSelf",
    ) -> "_2239.SphericalRollerThrustBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2239

        return self.__parent__._cast(_2239.SphericalRollerThrustBearing)

    @property
    def taper_roller_bearing(self: "CastSelf") -> "_2240.TaperRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2240

        return self.__parent__._cast(_2240.TaperRollerBearing)

    @property
    def three_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2241.ThreePointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2241

        return self.__parent__._cast(_2241.ThreePointContactBallBearing)

    @property
    def thrust_ball_bearing(self: "CastSelf") -> "_2242.ThrustBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2242

        return self.__parent__._cast(_2242.ThrustBallBearing)

    @property
    def toroidal_roller_bearing(self: "CastSelf") -> "_2243.ToroidalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2243

        return self.__parent__._cast(_2243.ToroidalRollerBearing)

    @property
    def pad_fluid_film_bearing(self: "CastSelf") -> "_2256.PadFluidFilmBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2256

        return self.__parent__._cast(_2256.PadFluidFilmBearing)

    @property
    def plain_grease_filled_journal_bearing(
        self: "CastSelf",
    ) -> "_2258.PlainGreaseFilledJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2258

        return self.__parent__._cast(_2258.PlainGreaseFilledJournalBearing)

    @property
    def plain_journal_bearing(self: "CastSelf") -> "_2260.PlainJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2260

        return self.__parent__._cast(_2260.PlainJournalBearing)

    @property
    def plain_oil_fed_journal_bearing(
        self: "CastSelf",
    ) -> "_2262.PlainOilFedJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2262

        return self.__parent__._cast(_2262.PlainOilFedJournalBearing)

    @property
    def tilting_pad_journal_bearing(
        self: "CastSelf",
    ) -> "_2263.TiltingPadJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2263

        return self.__parent__._cast(_2263.TiltingPadJournalBearing)

    @property
    def tilting_pad_thrust_bearing(self: "CastSelf") -> "_2264.TiltingPadThrustBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2264

        return self.__parent__._cast(_2264.TiltingPadThrustBearing)

    @property
    def detailed_bearing(self: "CastSelf") -> "DetailedBearing":
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
class DetailedBearing(_2202.NonLinearBearing):
    """DetailedBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DETAILED_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_DetailedBearing":
        """Cast to another type.

        Returns:
            _Cast_DetailedBearing
        """
        return _Cast_DetailedBearing(self)
