"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.units_and_measurements.measurements._1673 import (
        Acceleration,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1674 import Angle
    from mastapy._private.utility.units_and_measurements.measurements._1675 import (
        AnglePerUnitTemperature,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1676 import (
        AngleSmall,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1677 import (
        AngleVerySmall,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1678 import (
        AngularAcceleration,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1679 import (
        AngularCompliance,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1680 import (
        AngularJerk,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1681 import (
        AngularStiffness,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1682 import (
        AngularVelocity,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1683 import Area
    from mastapy._private.utility.units_and_measurements.measurements._1684 import (
        AreaSmall,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1685 import (
        CarbonEmissionFactor,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1686 import (
        CurrentDensity,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1687 import (
        CurrentPerLength,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1688 import (
        Cycles,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1689 import (
        Damage,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1690 import (
        DamageRate,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1691 import (
        DataSize,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1692 import (
        Decibel,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1693 import (
        Density,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1694 import (
        ElectricalResistance,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1695 import (
        ElectricalResistivity,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1696 import (
        ElectricCurrent,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1697 import (
        Energy,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1698 import (
        EnergyPerUnitArea,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1699 import (
        EnergyPerUnitAreaSmall,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1700 import (
        EnergySmall,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1701 import Enum
    from mastapy._private.utility.units_and_measurements.measurements._1702 import (
        FlowRate,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1703 import Force
    from mastapy._private.utility.units_and_measurements.measurements._1704 import (
        ForcePerUnitLength,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1705 import (
        ForcePerUnitPressure,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1706 import (
        ForcePerUnitTemperature,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1707 import (
        FractionMeasurementBase,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1708 import (
        FractionPerTemperature,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1709 import (
        Frequency,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1710 import (
        FuelConsumptionEngine,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1711 import (
        FuelEfficiencyVehicle,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1712 import (
        Gradient,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1713 import (
        HeatConductivity,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1714 import (
        HeatTransfer,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1715 import (
        HeatTransferCoefficientForPlasticGearTooth,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1716 import (
        HeatTransferResistance,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1717 import (
        Impulse,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1718 import Index
    from mastapy._private.utility.units_and_measurements.measurements._1719 import (
        Inductance,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1720 import (
        Integer,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1721 import (
        InverseShortLength,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1722 import (
        InverseShortTime,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1723 import Jerk
    from mastapy._private.utility.units_and_measurements.measurements._1724 import (
        KinematicViscosity,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1725 import (
        LengthLong,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1726 import (
        LengthMedium,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1727 import (
        LengthPerUnitTemperature,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1728 import (
        LengthShort,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1729 import (
        LengthToTheFourth,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1730 import (
        LengthVeryLong,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1731 import (
        LengthVeryShort,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1732 import (
        LengthVeryShortPerLengthShort,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1733 import (
        LinearAngularDamping,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1734 import (
        LinearAngularStiffnessCrossTerm,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1735 import (
        LinearDamping,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1736 import (
        LinearFlexibility,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1737 import (
        LinearStiffness,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1738 import (
        MagneticFieldStrength,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1739 import (
        MagneticFlux,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1740 import (
        MagneticFluxDensity,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1741 import (
        MagneticVectorPotential,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1742 import (
        MagnetomotiveForce,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1743 import Mass
    from mastapy._private.utility.units_and_measurements.measurements._1744 import (
        MassPerUnitLength,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1745 import (
        MassPerUnitTime,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1746 import (
        MomentOfInertia,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1747 import (
        MomentOfInertiaPerUnitLength,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1748 import (
        MomentPerUnitPressure,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1749 import (
        Number,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1750 import (
        Percentage,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1751 import Power
    from mastapy._private.utility.units_and_measurements.measurements._1752 import (
        PowerPerSmallArea,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1753 import (
        PowerPerUnitTime,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1754 import (
        PowerSmall,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1755 import (
        PowerSmallPerArea,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1756 import (
        PowerSmallPerMass,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1757 import (
        PowerSmallPerUnitAreaPerUnitTime,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1758 import (
        PowerSmallPerUnitTime,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1759 import (
        PowerSmallPerVolume,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1760 import (
        Pressure,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1761 import (
        PressurePerUnitTime,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1762 import (
        PressureSmall,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1763 import (
        PressureVelocityProduct,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1764 import (
        PressureViscosityCoefficient,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1765 import Price
    from mastapy._private.utility.units_and_measurements.measurements._1766 import (
        PricePerUnitMass,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1767 import (
        QuadraticAngularDamping,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1768 import (
        QuadraticDrag,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1769 import (
        RescaledMeasurement,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1770 import (
        Rotatum,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1771 import (
        SafetyFactor,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1772 import (
        SpecificAcousticImpedance,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1773 import (
        SpecificHeat,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1774 import (
        SquareRootOfUnitForcePerUnitArea,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1775 import (
        StiffnessPerUnitFaceWidth,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1776 import (
        Stress,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1777 import (
        Temperature,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1778 import (
        TemperatureDifference,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1779 import (
        TemperaturePerUnitTime,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1780 import Text
    from mastapy._private.utility.units_and_measurements.measurements._1781 import (
        ThermalContactCoefficient,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1782 import (
        ThermalExpansionCoefficient,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1783 import (
        ThermoElasticFactor,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1784 import Time
    from mastapy._private.utility.units_and_measurements.measurements._1785 import (
        TimeShort,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1786 import (
        TimeVeryShort,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1787 import (
        Torque,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1788 import (
        TorqueConverterInverseK,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1789 import (
        TorqueConverterK,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1790 import (
        TorquePerCurrent,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1791 import (
        TorquePerSquareRootOfPower,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1792 import (
        TorquePerUnitTemperature,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1793 import (
        Velocity,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1794 import (
        VelocitySmall,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1795 import (
        Viscosity,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1796 import (
        Voltage,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1797 import (
        VoltagePerAngularVelocity,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1798 import (
        Volume,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1799 import (
        WearCoefficient,
    )
    from mastapy._private.utility.units_and_measurements.measurements._1800 import Yank
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.units_and_measurements.measurements._1673": ["Acceleration"],
        "_private.utility.units_and_measurements.measurements._1674": ["Angle"],
        "_private.utility.units_and_measurements.measurements._1675": [
            "AnglePerUnitTemperature"
        ],
        "_private.utility.units_and_measurements.measurements._1676": ["AngleSmall"],
        "_private.utility.units_and_measurements.measurements._1677": [
            "AngleVerySmall"
        ],
        "_private.utility.units_and_measurements.measurements._1678": [
            "AngularAcceleration"
        ],
        "_private.utility.units_and_measurements.measurements._1679": [
            "AngularCompliance"
        ],
        "_private.utility.units_and_measurements.measurements._1680": ["AngularJerk"],
        "_private.utility.units_and_measurements.measurements._1681": [
            "AngularStiffness"
        ],
        "_private.utility.units_and_measurements.measurements._1682": [
            "AngularVelocity"
        ],
        "_private.utility.units_and_measurements.measurements._1683": ["Area"],
        "_private.utility.units_and_measurements.measurements._1684": ["AreaSmall"],
        "_private.utility.units_and_measurements.measurements._1685": [
            "CarbonEmissionFactor"
        ],
        "_private.utility.units_and_measurements.measurements._1686": [
            "CurrentDensity"
        ],
        "_private.utility.units_and_measurements.measurements._1687": [
            "CurrentPerLength"
        ],
        "_private.utility.units_and_measurements.measurements._1688": ["Cycles"],
        "_private.utility.units_and_measurements.measurements._1689": ["Damage"],
        "_private.utility.units_and_measurements.measurements._1690": ["DamageRate"],
        "_private.utility.units_and_measurements.measurements._1691": ["DataSize"],
        "_private.utility.units_and_measurements.measurements._1692": ["Decibel"],
        "_private.utility.units_and_measurements.measurements._1693": ["Density"],
        "_private.utility.units_and_measurements.measurements._1694": [
            "ElectricalResistance"
        ],
        "_private.utility.units_and_measurements.measurements._1695": [
            "ElectricalResistivity"
        ],
        "_private.utility.units_and_measurements.measurements._1696": [
            "ElectricCurrent"
        ],
        "_private.utility.units_and_measurements.measurements._1697": ["Energy"],
        "_private.utility.units_and_measurements.measurements._1698": [
            "EnergyPerUnitArea"
        ],
        "_private.utility.units_and_measurements.measurements._1699": [
            "EnergyPerUnitAreaSmall"
        ],
        "_private.utility.units_and_measurements.measurements._1700": ["EnergySmall"],
        "_private.utility.units_and_measurements.measurements._1701": ["Enum"],
        "_private.utility.units_and_measurements.measurements._1702": ["FlowRate"],
        "_private.utility.units_and_measurements.measurements._1703": ["Force"],
        "_private.utility.units_and_measurements.measurements._1704": [
            "ForcePerUnitLength"
        ],
        "_private.utility.units_and_measurements.measurements._1705": [
            "ForcePerUnitPressure"
        ],
        "_private.utility.units_and_measurements.measurements._1706": [
            "ForcePerUnitTemperature"
        ],
        "_private.utility.units_and_measurements.measurements._1707": [
            "FractionMeasurementBase"
        ],
        "_private.utility.units_and_measurements.measurements._1708": [
            "FractionPerTemperature"
        ],
        "_private.utility.units_and_measurements.measurements._1709": ["Frequency"],
        "_private.utility.units_and_measurements.measurements._1710": [
            "FuelConsumptionEngine"
        ],
        "_private.utility.units_and_measurements.measurements._1711": [
            "FuelEfficiencyVehicle"
        ],
        "_private.utility.units_and_measurements.measurements._1712": ["Gradient"],
        "_private.utility.units_and_measurements.measurements._1713": [
            "HeatConductivity"
        ],
        "_private.utility.units_and_measurements.measurements._1714": ["HeatTransfer"],
        "_private.utility.units_and_measurements.measurements._1715": [
            "HeatTransferCoefficientForPlasticGearTooth"
        ],
        "_private.utility.units_and_measurements.measurements._1716": [
            "HeatTransferResistance"
        ],
        "_private.utility.units_and_measurements.measurements._1717": ["Impulse"],
        "_private.utility.units_and_measurements.measurements._1718": ["Index"],
        "_private.utility.units_and_measurements.measurements._1719": ["Inductance"],
        "_private.utility.units_and_measurements.measurements._1720": ["Integer"],
        "_private.utility.units_and_measurements.measurements._1721": [
            "InverseShortLength"
        ],
        "_private.utility.units_and_measurements.measurements._1722": [
            "InverseShortTime"
        ],
        "_private.utility.units_and_measurements.measurements._1723": ["Jerk"],
        "_private.utility.units_and_measurements.measurements._1724": [
            "KinematicViscosity"
        ],
        "_private.utility.units_and_measurements.measurements._1725": ["LengthLong"],
        "_private.utility.units_and_measurements.measurements._1726": ["LengthMedium"],
        "_private.utility.units_and_measurements.measurements._1727": [
            "LengthPerUnitTemperature"
        ],
        "_private.utility.units_and_measurements.measurements._1728": ["LengthShort"],
        "_private.utility.units_and_measurements.measurements._1729": [
            "LengthToTheFourth"
        ],
        "_private.utility.units_and_measurements.measurements._1730": [
            "LengthVeryLong"
        ],
        "_private.utility.units_and_measurements.measurements._1731": [
            "LengthVeryShort"
        ],
        "_private.utility.units_and_measurements.measurements._1732": [
            "LengthVeryShortPerLengthShort"
        ],
        "_private.utility.units_and_measurements.measurements._1733": [
            "LinearAngularDamping"
        ],
        "_private.utility.units_and_measurements.measurements._1734": [
            "LinearAngularStiffnessCrossTerm"
        ],
        "_private.utility.units_and_measurements.measurements._1735": ["LinearDamping"],
        "_private.utility.units_and_measurements.measurements._1736": [
            "LinearFlexibility"
        ],
        "_private.utility.units_and_measurements.measurements._1737": [
            "LinearStiffness"
        ],
        "_private.utility.units_and_measurements.measurements._1738": [
            "MagneticFieldStrength"
        ],
        "_private.utility.units_and_measurements.measurements._1739": ["MagneticFlux"],
        "_private.utility.units_and_measurements.measurements._1740": [
            "MagneticFluxDensity"
        ],
        "_private.utility.units_and_measurements.measurements._1741": [
            "MagneticVectorPotential"
        ],
        "_private.utility.units_and_measurements.measurements._1742": [
            "MagnetomotiveForce"
        ],
        "_private.utility.units_and_measurements.measurements._1743": ["Mass"],
        "_private.utility.units_and_measurements.measurements._1744": [
            "MassPerUnitLength"
        ],
        "_private.utility.units_and_measurements.measurements._1745": [
            "MassPerUnitTime"
        ],
        "_private.utility.units_and_measurements.measurements._1746": [
            "MomentOfInertia"
        ],
        "_private.utility.units_and_measurements.measurements._1747": [
            "MomentOfInertiaPerUnitLength"
        ],
        "_private.utility.units_and_measurements.measurements._1748": [
            "MomentPerUnitPressure"
        ],
        "_private.utility.units_and_measurements.measurements._1749": ["Number"],
        "_private.utility.units_and_measurements.measurements._1750": ["Percentage"],
        "_private.utility.units_and_measurements.measurements._1751": ["Power"],
        "_private.utility.units_and_measurements.measurements._1752": [
            "PowerPerSmallArea"
        ],
        "_private.utility.units_and_measurements.measurements._1753": [
            "PowerPerUnitTime"
        ],
        "_private.utility.units_and_measurements.measurements._1754": ["PowerSmall"],
        "_private.utility.units_and_measurements.measurements._1755": [
            "PowerSmallPerArea"
        ],
        "_private.utility.units_and_measurements.measurements._1756": [
            "PowerSmallPerMass"
        ],
        "_private.utility.units_and_measurements.measurements._1757": [
            "PowerSmallPerUnitAreaPerUnitTime"
        ],
        "_private.utility.units_and_measurements.measurements._1758": [
            "PowerSmallPerUnitTime"
        ],
        "_private.utility.units_and_measurements.measurements._1759": [
            "PowerSmallPerVolume"
        ],
        "_private.utility.units_and_measurements.measurements._1760": ["Pressure"],
        "_private.utility.units_and_measurements.measurements._1761": [
            "PressurePerUnitTime"
        ],
        "_private.utility.units_and_measurements.measurements._1762": ["PressureSmall"],
        "_private.utility.units_and_measurements.measurements._1763": [
            "PressureVelocityProduct"
        ],
        "_private.utility.units_and_measurements.measurements._1764": [
            "PressureViscosityCoefficient"
        ],
        "_private.utility.units_and_measurements.measurements._1765": ["Price"],
        "_private.utility.units_and_measurements.measurements._1766": [
            "PricePerUnitMass"
        ],
        "_private.utility.units_and_measurements.measurements._1767": [
            "QuadraticAngularDamping"
        ],
        "_private.utility.units_and_measurements.measurements._1768": ["QuadraticDrag"],
        "_private.utility.units_and_measurements.measurements._1769": [
            "RescaledMeasurement"
        ],
        "_private.utility.units_and_measurements.measurements._1770": ["Rotatum"],
        "_private.utility.units_and_measurements.measurements._1771": ["SafetyFactor"],
        "_private.utility.units_and_measurements.measurements._1772": [
            "SpecificAcousticImpedance"
        ],
        "_private.utility.units_and_measurements.measurements._1773": ["SpecificHeat"],
        "_private.utility.units_and_measurements.measurements._1774": [
            "SquareRootOfUnitForcePerUnitArea"
        ],
        "_private.utility.units_and_measurements.measurements._1775": [
            "StiffnessPerUnitFaceWidth"
        ],
        "_private.utility.units_and_measurements.measurements._1776": ["Stress"],
        "_private.utility.units_and_measurements.measurements._1777": ["Temperature"],
        "_private.utility.units_and_measurements.measurements._1778": [
            "TemperatureDifference"
        ],
        "_private.utility.units_and_measurements.measurements._1779": [
            "TemperaturePerUnitTime"
        ],
        "_private.utility.units_and_measurements.measurements._1780": ["Text"],
        "_private.utility.units_and_measurements.measurements._1781": [
            "ThermalContactCoefficient"
        ],
        "_private.utility.units_and_measurements.measurements._1782": [
            "ThermalExpansionCoefficient"
        ],
        "_private.utility.units_and_measurements.measurements._1783": [
            "ThermoElasticFactor"
        ],
        "_private.utility.units_and_measurements.measurements._1784": ["Time"],
        "_private.utility.units_and_measurements.measurements._1785": ["TimeShort"],
        "_private.utility.units_and_measurements.measurements._1786": ["TimeVeryShort"],
        "_private.utility.units_and_measurements.measurements._1787": ["Torque"],
        "_private.utility.units_and_measurements.measurements._1788": [
            "TorqueConverterInverseK"
        ],
        "_private.utility.units_and_measurements.measurements._1789": [
            "TorqueConverterK"
        ],
        "_private.utility.units_and_measurements.measurements._1790": [
            "TorquePerCurrent"
        ],
        "_private.utility.units_and_measurements.measurements._1791": [
            "TorquePerSquareRootOfPower"
        ],
        "_private.utility.units_and_measurements.measurements._1792": [
            "TorquePerUnitTemperature"
        ],
        "_private.utility.units_and_measurements.measurements._1793": ["Velocity"],
        "_private.utility.units_and_measurements.measurements._1794": ["VelocitySmall"],
        "_private.utility.units_and_measurements.measurements._1795": ["Viscosity"],
        "_private.utility.units_and_measurements.measurements._1796": ["Voltage"],
        "_private.utility.units_and_measurements.measurements._1797": [
            "VoltagePerAngularVelocity"
        ],
        "_private.utility.units_and_measurements.measurements._1798": ["Volume"],
        "_private.utility.units_and_measurements.measurements._1799": [
            "WearCoefficient"
        ],
        "_private.utility.units_and_measurements.measurements._1800": ["Yank"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "Acceleration",
    "Angle",
    "AnglePerUnitTemperature",
    "AngleSmall",
    "AngleVerySmall",
    "AngularAcceleration",
    "AngularCompliance",
    "AngularJerk",
    "AngularStiffness",
    "AngularVelocity",
    "Area",
    "AreaSmall",
    "CarbonEmissionFactor",
    "CurrentDensity",
    "CurrentPerLength",
    "Cycles",
    "Damage",
    "DamageRate",
    "DataSize",
    "Decibel",
    "Density",
    "ElectricalResistance",
    "ElectricalResistivity",
    "ElectricCurrent",
    "Energy",
    "EnergyPerUnitArea",
    "EnergyPerUnitAreaSmall",
    "EnergySmall",
    "Enum",
    "FlowRate",
    "Force",
    "ForcePerUnitLength",
    "ForcePerUnitPressure",
    "ForcePerUnitTemperature",
    "FractionMeasurementBase",
    "FractionPerTemperature",
    "Frequency",
    "FuelConsumptionEngine",
    "FuelEfficiencyVehicle",
    "Gradient",
    "HeatConductivity",
    "HeatTransfer",
    "HeatTransferCoefficientForPlasticGearTooth",
    "HeatTransferResistance",
    "Impulse",
    "Index",
    "Inductance",
    "Integer",
    "InverseShortLength",
    "InverseShortTime",
    "Jerk",
    "KinematicViscosity",
    "LengthLong",
    "LengthMedium",
    "LengthPerUnitTemperature",
    "LengthShort",
    "LengthToTheFourth",
    "LengthVeryLong",
    "LengthVeryShort",
    "LengthVeryShortPerLengthShort",
    "LinearAngularDamping",
    "LinearAngularStiffnessCrossTerm",
    "LinearDamping",
    "LinearFlexibility",
    "LinearStiffness",
    "MagneticFieldStrength",
    "MagneticFlux",
    "MagneticFluxDensity",
    "MagneticVectorPotential",
    "MagnetomotiveForce",
    "Mass",
    "MassPerUnitLength",
    "MassPerUnitTime",
    "MomentOfInertia",
    "MomentOfInertiaPerUnitLength",
    "MomentPerUnitPressure",
    "Number",
    "Percentage",
    "Power",
    "PowerPerSmallArea",
    "PowerPerUnitTime",
    "PowerSmall",
    "PowerSmallPerArea",
    "PowerSmallPerMass",
    "PowerSmallPerUnitAreaPerUnitTime",
    "PowerSmallPerUnitTime",
    "PowerSmallPerVolume",
    "Pressure",
    "PressurePerUnitTime",
    "PressureSmall",
    "PressureVelocityProduct",
    "PressureViscosityCoefficient",
    "Price",
    "PricePerUnitMass",
    "QuadraticAngularDamping",
    "QuadraticDrag",
    "RescaledMeasurement",
    "Rotatum",
    "SafetyFactor",
    "SpecificAcousticImpedance",
    "SpecificHeat",
    "SquareRootOfUnitForcePerUnitArea",
    "StiffnessPerUnitFaceWidth",
    "Stress",
    "Temperature",
    "TemperatureDifference",
    "TemperaturePerUnitTime",
    "Text",
    "ThermalContactCoefficient",
    "ThermalExpansionCoefficient",
    "ThermoElasticFactor",
    "Time",
    "TimeShort",
    "TimeVeryShort",
    "Torque",
    "TorqueConverterInverseK",
    "TorqueConverterK",
    "TorquePerCurrent",
    "TorquePerSquareRootOfPower",
    "TorquePerUnitTemperature",
    "Velocity",
    "VelocitySmall",
    "Viscosity",
    "Voltage",
    "VoltagePerAngularVelocity",
    "Volume",
    "WearCoefficient",
    "Yank",
)
