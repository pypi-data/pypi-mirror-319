"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bearings.bearing_designs.rolling._2203 import (
        AngularContactBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2204 import (
        AngularContactThrustBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2205 import (
        AsymmetricSphericalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2206 import (
        AxialThrustCylindricalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2207 import (
        AxialThrustNeedleRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2208 import BallBearing
    from mastapy._private.bearings.bearing_designs.rolling._2209 import (
        BallBearingShoulderDefinition,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2210 import (
        BarrelRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2211 import (
        BearingProtection,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2212 import (
        BearingProtectionDetailsModifier,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2213 import (
        BearingProtectionLevel,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2214 import (
        BearingTypeExtraInformation,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2215 import CageBridgeShape
    from mastapy._private.bearings.bearing_designs.rolling._2216 import (
        CrossedRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2217 import (
        CylindricalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2218 import (
        DeepGrooveBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2219 import DiameterSeries
    from mastapy._private.bearings.bearing_designs.rolling._2220 import (
        FatigueLoadLimitCalculationMethodEnum,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2221 import (
        FourPointContactAngleDefinition,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2222 import (
        FourPointContactBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2223 import (
        GeometricConstants,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2224 import (
        GeometricConstantsForRollingFrictionalMoments,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2225 import (
        GeometricConstantsForSlidingFrictionalMoments,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2226 import HeightSeries
    from mastapy._private.bearings.bearing_designs.rolling._2227 import (
        MultiPointContactBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2228 import (
        NeedleRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2229 import (
        NonBarrelRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2230 import RollerBearing
    from mastapy._private.bearings.bearing_designs.rolling._2231 import RollerEndShape
    from mastapy._private.bearings.bearing_designs.rolling._2232 import RollerRibDetail
    from mastapy._private.bearings.bearing_designs.rolling._2233 import RollingBearing
    from mastapy._private.bearings.bearing_designs.rolling._2234 import (
        RollingBearingElement,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2235 import (
        SelfAligningBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2236 import (
        SKFSealFrictionalMomentConstants,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2237 import SleeveType
    from mastapy._private.bearings.bearing_designs.rolling._2238 import (
        SphericalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2239 import (
        SphericalRollerThrustBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2240 import (
        TaperRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2241 import (
        ThreePointContactBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2242 import (
        ThrustBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2243 import (
        ToroidalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2244 import WidthSeries
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bearings.bearing_designs.rolling._2203": [
            "AngularContactBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2204": [
            "AngularContactThrustBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2205": [
            "AsymmetricSphericalRollerBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2206": [
            "AxialThrustCylindricalRollerBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2207": [
            "AxialThrustNeedleRollerBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2208": ["BallBearing"],
        "_private.bearings.bearing_designs.rolling._2209": [
            "BallBearingShoulderDefinition"
        ],
        "_private.bearings.bearing_designs.rolling._2210": ["BarrelRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2211": ["BearingProtection"],
        "_private.bearings.bearing_designs.rolling._2212": [
            "BearingProtectionDetailsModifier"
        ],
        "_private.bearings.bearing_designs.rolling._2213": ["BearingProtectionLevel"],
        "_private.bearings.bearing_designs.rolling._2214": [
            "BearingTypeExtraInformation"
        ],
        "_private.bearings.bearing_designs.rolling._2215": ["CageBridgeShape"],
        "_private.bearings.bearing_designs.rolling._2216": ["CrossedRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2217": ["CylindricalRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2218": ["DeepGrooveBallBearing"],
        "_private.bearings.bearing_designs.rolling._2219": ["DiameterSeries"],
        "_private.bearings.bearing_designs.rolling._2220": [
            "FatigueLoadLimitCalculationMethodEnum"
        ],
        "_private.bearings.bearing_designs.rolling._2221": [
            "FourPointContactAngleDefinition"
        ],
        "_private.bearings.bearing_designs.rolling._2222": [
            "FourPointContactBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2223": ["GeometricConstants"],
        "_private.bearings.bearing_designs.rolling._2224": [
            "GeometricConstantsForRollingFrictionalMoments"
        ],
        "_private.bearings.bearing_designs.rolling._2225": [
            "GeometricConstantsForSlidingFrictionalMoments"
        ],
        "_private.bearings.bearing_designs.rolling._2226": ["HeightSeries"],
        "_private.bearings.bearing_designs.rolling._2227": [
            "MultiPointContactBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2228": ["NeedleRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2229": ["NonBarrelRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2230": ["RollerBearing"],
        "_private.bearings.bearing_designs.rolling._2231": ["RollerEndShape"],
        "_private.bearings.bearing_designs.rolling._2232": ["RollerRibDetail"],
        "_private.bearings.bearing_designs.rolling._2233": ["RollingBearing"],
        "_private.bearings.bearing_designs.rolling._2234": ["RollingBearingElement"],
        "_private.bearings.bearing_designs.rolling._2235": ["SelfAligningBallBearing"],
        "_private.bearings.bearing_designs.rolling._2236": [
            "SKFSealFrictionalMomentConstants"
        ],
        "_private.bearings.bearing_designs.rolling._2237": ["SleeveType"],
        "_private.bearings.bearing_designs.rolling._2238": ["SphericalRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2239": [
            "SphericalRollerThrustBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2240": ["TaperRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2241": [
            "ThreePointContactBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2242": ["ThrustBallBearing"],
        "_private.bearings.bearing_designs.rolling._2243": ["ToroidalRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2244": ["WidthSeries"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AngularContactBallBearing",
    "AngularContactThrustBallBearing",
    "AsymmetricSphericalRollerBearing",
    "AxialThrustCylindricalRollerBearing",
    "AxialThrustNeedleRollerBearing",
    "BallBearing",
    "BallBearingShoulderDefinition",
    "BarrelRollerBearing",
    "BearingProtection",
    "BearingProtectionDetailsModifier",
    "BearingProtectionLevel",
    "BearingTypeExtraInformation",
    "CageBridgeShape",
    "CrossedRollerBearing",
    "CylindricalRollerBearing",
    "DeepGrooveBallBearing",
    "DiameterSeries",
    "FatigueLoadLimitCalculationMethodEnum",
    "FourPointContactAngleDefinition",
    "FourPointContactBallBearing",
    "GeometricConstants",
    "GeometricConstantsForRollingFrictionalMoments",
    "GeometricConstantsForSlidingFrictionalMoments",
    "HeightSeries",
    "MultiPointContactBallBearing",
    "NeedleRollerBearing",
    "NonBarrelRollerBearing",
    "RollerBearing",
    "RollerEndShape",
    "RollerRibDetail",
    "RollingBearing",
    "RollingBearingElement",
    "SelfAligningBallBearing",
    "SKFSealFrictionalMomentConstants",
    "SleeveType",
    "SphericalRollerBearing",
    "SphericalRollerThrustBearing",
    "TaperRollerBearing",
    "ThreePointContactBallBearing",
    "ThrustBallBearing",
    "ToroidalRollerBearing",
    "WidthSeries",
)
