"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3857 import (
        AbstractAssemblyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3858 import (
        AbstractShaftOrHousingStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3859 import (
        AbstractShaftStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3860 import (
        AbstractShaftToMountableComponentConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3861 import (
        AGMAGleasonConicalGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3862 import (
        AGMAGleasonConicalGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3863 import (
        AGMAGleasonConicalGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3864 import (
        AssemblyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3865 import (
        BearingStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3866 import (
        BeltConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3867 import (
        BeltDriveStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3868 import (
        BevelDifferentialGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3869 import (
        BevelDifferentialGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3870 import (
        BevelDifferentialGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3871 import (
        BevelDifferentialPlanetGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3872 import (
        BevelDifferentialSunGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3873 import (
        BevelGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3874 import (
        BevelGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3875 import (
        BevelGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3876 import (
        BoltedJointStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3877 import (
        BoltStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3878 import (
        ClutchConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3879 import (
        ClutchHalfStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3880 import (
        ClutchStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3881 import (
        CoaxialConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3882 import (
        ComponentStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3883 import (
        ConceptCouplingConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3884 import (
        ConceptCouplingHalfStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3885 import (
        ConceptCouplingStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3886 import (
        ConceptGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3887 import (
        ConceptGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3888 import (
        ConceptGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3889 import (
        ConicalGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3890 import (
        ConicalGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3891 import (
        ConicalGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3892 import (
        ConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3893 import (
        ConnectorStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3894 import (
        CouplingConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3895 import (
        CouplingHalfStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3896 import (
        CouplingStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3897 import (
        CriticalSpeed,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3898 import (
        CVTBeltConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3899 import (
        CVTPulleyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3900 import (
        CVTStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3901 import (
        CycloidalAssemblyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3902 import (
        CycloidalDiscCentralBearingConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3903 import (
        CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3904 import (
        CycloidalDiscStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3905 import (
        CylindricalGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3906 import (
        CylindricalGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3907 import (
        CylindricalGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3908 import (
        CylindricalPlanetGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3909 import (
        DatumStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3910 import (
        DynamicModelForStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3911 import (
        ExternalCADModelStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3912 import (
        FaceGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3913 import (
        FaceGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3914 import (
        FaceGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3915 import (
        FEPartStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3916 import (
        FlexiblePinAssemblyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3917 import (
        GearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3918 import (
        GearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3919 import (
        GearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3920 import (
        GuideDxfModelStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3921 import (
        HypoidGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3922 import (
        HypoidGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3923 import (
        HypoidGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3924 import (
        InterMountableComponentConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3925 import (
        KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3926 import (
        KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3927 import (
        KlingelnbergCycloPalloidConicalGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3928 import (
        KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3929 import (
        KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3930 import (
        KlingelnbergCycloPalloidHypoidGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3931 import (
        KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3932 import (
        KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3933 import (
        KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3934 import (
        MassDiscStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3935 import (
        MeasurementComponentStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3936 import (
        MicrophoneArrayStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3937 import (
        MicrophoneStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3938 import (
        MountableComponentStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3939 import (
        OilSealStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3940 import (
        PartStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3941 import (
        PartToPartShearCouplingConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3942 import (
        PartToPartShearCouplingHalfStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3943 import (
        PartToPartShearCouplingStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3944 import (
        PlanetaryConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3945 import (
        PlanetaryGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3946 import (
        PlanetCarrierStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3947 import (
        PointLoadStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3948 import (
        PowerLoadStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3949 import (
        PulleyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3950 import (
        RingPinsStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3951 import (
        RingPinsToDiscConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3952 import (
        RollingRingAssemblyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3953 import (
        RollingRingConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3954 import (
        RollingRingStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3955 import (
        RootAssemblyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3956 import (
        ShaftHubConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3957 import (
        ShaftStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3958 import (
        ShaftToMountableComponentConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3959 import (
        SpecialisedAssemblyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3960 import (
        SpiralBevelGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3961 import (
        SpiralBevelGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3962 import (
        SpiralBevelGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3963 import (
        SpringDamperConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3964 import (
        SpringDamperHalfStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3965 import (
        SpringDamperStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3966 import (
        StabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3967 import (
        StabilityAnalysisDrawStyle,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3968 import (
        StabilityAnalysisOptions,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3969 import (
        StraightBevelDiffGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3970 import (
        StraightBevelDiffGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3971 import (
        StraightBevelDiffGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3972 import (
        StraightBevelGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3973 import (
        StraightBevelGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3974 import (
        StraightBevelGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3975 import (
        StraightBevelPlanetGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3976 import (
        StraightBevelSunGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3977 import (
        SynchroniserHalfStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3978 import (
        SynchroniserPartStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3979 import (
        SynchroniserSleeveStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3980 import (
        SynchroniserStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3981 import (
        TorqueConverterConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3982 import (
        TorqueConverterPumpStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3983 import (
        TorqueConverterStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3984 import (
        TorqueConverterTurbineStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3985 import (
        UnbalancedMassStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3986 import (
        VirtualComponentStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3987 import (
        WormGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3988 import (
        WormGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3989 import (
        WormGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3990 import (
        ZerolBevelGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3991 import (
        ZerolBevelGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._3992 import (
        ZerolBevelGearStabilityAnalysis,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results.stability_analyses._3857": [
            "AbstractAssemblyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3858": [
            "AbstractShaftOrHousingStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3859": [
            "AbstractShaftStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3860": [
            "AbstractShaftToMountableComponentConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3861": [
            "AGMAGleasonConicalGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3862": [
            "AGMAGleasonConicalGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3863": [
            "AGMAGleasonConicalGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3864": [
            "AssemblyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3865": [
            "BearingStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3866": [
            "BeltConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3867": [
            "BeltDriveStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3868": [
            "BevelDifferentialGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3869": [
            "BevelDifferentialGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3870": [
            "BevelDifferentialGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3871": [
            "BevelDifferentialPlanetGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3872": [
            "BevelDifferentialSunGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3873": [
            "BevelGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3874": [
            "BevelGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3875": [
            "BevelGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3876": [
            "BoltedJointStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3877": [
            "BoltStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3878": [
            "ClutchConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3879": [
            "ClutchHalfStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3880": [
            "ClutchStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3881": [
            "CoaxialConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3882": [
            "ComponentStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3883": [
            "ConceptCouplingConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3884": [
            "ConceptCouplingHalfStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3885": [
            "ConceptCouplingStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3886": [
            "ConceptGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3887": [
            "ConceptGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3888": [
            "ConceptGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3889": [
            "ConicalGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3890": [
            "ConicalGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3891": [
            "ConicalGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3892": [
            "ConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3893": [
            "ConnectorStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3894": [
            "CouplingConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3895": [
            "CouplingHalfStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3896": [
            "CouplingStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3897": [
            "CriticalSpeed"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3898": [
            "CVTBeltConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3899": [
            "CVTPulleyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3900": [
            "CVTStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3901": [
            "CycloidalAssemblyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3902": [
            "CycloidalDiscCentralBearingConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3903": [
            "CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3904": [
            "CycloidalDiscStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3905": [
            "CylindricalGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3906": [
            "CylindricalGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3907": [
            "CylindricalGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3908": [
            "CylindricalPlanetGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3909": [
            "DatumStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3910": [
            "DynamicModelForStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3911": [
            "ExternalCADModelStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3912": [
            "FaceGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3913": [
            "FaceGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3914": [
            "FaceGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3915": [
            "FEPartStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3916": [
            "FlexiblePinAssemblyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3917": [
            "GearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3918": [
            "GearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3919": [
            "GearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3920": [
            "GuideDxfModelStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3921": [
            "HypoidGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3922": [
            "HypoidGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3923": [
            "HypoidGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3924": [
            "InterMountableComponentConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3925": [
            "KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3926": [
            "KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3927": [
            "KlingelnbergCycloPalloidConicalGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3928": [
            "KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3929": [
            "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3930": [
            "KlingelnbergCycloPalloidHypoidGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3931": [
            "KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3932": [
            "KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3933": [
            "KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3934": [
            "MassDiscStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3935": [
            "MeasurementComponentStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3936": [
            "MicrophoneArrayStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3937": [
            "MicrophoneStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3938": [
            "MountableComponentStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3939": [
            "OilSealStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3940": [
            "PartStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3941": [
            "PartToPartShearCouplingConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3942": [
            "PartToPartShearCouplingHalfStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3943": [
            "PartToPartShearCouplingStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3944": [
            "PlanetaryConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3945": [
            "PlanetaryGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3946": [
            "PlanetCarrierStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3947": [
            "PointLoadStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3948": [
            "PowerLoadStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3949": [
            "PulleyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3950": [
            "RingPinsStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3951": [
            "RingPinsToDiscConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3952": [
            "RollingRingAssemblyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3953": [
            "RollingRingConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3954": [
            "RollingRingStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3955": [
            "RootAssemblyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3956": [
            "ShaftHubConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3957": [
            "ShaftStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3958": [
            "ShaftToMountableComponentConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3959": [
            "SpecialisedAssemblyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3960": [
            "SpiralBevelGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3961": [
            "SpiralBevelGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3962": [
            "SpiralBevelGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3963": [
            "SpringDamperConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3964": [
            "SpringDamperHalfStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3965": [
            "SpringDamperStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3966": [
            "StabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3967": [
            "StabilityAnalysisDrawStyle"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3968": [
            "StabilityAnalysisOptions"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3969": [
            "StraightBevelDiffGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3970": [
            "StraightBevelDiffGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3971": [
            "StraightBevelDiffGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3972": [
            "StraightBevelGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3973": [
            "StraightBevelGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3974": [
            "StraightBevelGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3975": [
            "StraightBevelPlanetGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3976": [
            "StraightBevelSunGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3977": [
            "SynchroniserHalfStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3978": [
            "SynchroniserPartStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3979": [
            "SynchroniserSleeveStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3980": [
            "SynchroniserStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3981": [
            "TorqueConverterConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3982": [
            "TorqueConverterPumpStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3983": [
            "TorqueConverterStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3984": [
            "TorqueConverterTurbineStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3985": [
            "UnbalancedMassStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3986": [
            "VirtualComponentStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3987": [
            "WormGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3988": [
            "WormGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3989": [
            "WormGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3990": [
            "ZerolBevelGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3991": [
            "ZerolBevelGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._3992": [
            "ZerolBevelGearStabilityAnalysis"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractAssemblyStabilityAnalysis",
    "AbstractShaftOrHousingStabilityAnalysis",
    "AbstractShaftStabilityAnalysis",
    "AbstractShaftToMountableComponentConnectionStabilityAnalysis",
    "AGMAGleasonConicalGearMeshStabilityAnalysis",
    "AGMAGleasonConicalGearSetStabilityAnalysis",
    "AGMAGleasonConicalGearStabilityAnalysis",
    "AssemblyStabilityAnalysis",
    "BearingStabilityAnalysis",
    "BeltConnectionStabilityAnalysis",
    "BeltDriveStabilityAnalysis",
    "BevelDifferentialGearMeshStabilityAnalysis",
    "BevelDifferentialGearSetStabilityAnalysis",
    "BevelDifferentialGearStabilityAnalysis",
    "BevelDifferentialPlanetGearStabilityAnalysis",
    "BevelDifferentialSunGearStabilityAnalysis",
    "BevelGearMeshStabilityAnalysis",
    "BevelGearSetStabilityAnalysis",
    "BevelGearStabilityAnalysis",
    "BoltedJointStabilityAnalysis",
    "BoltStabilityAnalysis",
    "ClutchConnectionStabilityAnalysis",
    "ClutchHalfStabilityAnalysis",
    "ClutchStabilityAnalysis",
    "CoaxialConnectionStabilityAnalysis",
    "ComponentStabilityAnalysis",
    "ConceptCouplingConnectionStabilityAnalysis",
    "ConceptCouplingHalfStabilityAnalysis",
    "ConceptCouplingStabilityAnalysis",
    "ConceptGearMeshStabilityAnalysis",
    "ConceptGearSetStabilityAnalysis",
    "ConceptGearStabilityAnalysis",
    "ConicalGearMeshStabilityAnalysis",
    "ConicalGearSetStabilityAnalysis",
    "ConicalGearStabilityAnalysis",
    "ConnectionStabilityAnalysis",
    "ConnectorStabilityAnalysis",
    "CouplingConnectionStabilityAnalysis",
    "CouplingHalfStabilityAnalysis",
    "CouplingStabilityAnalysis",
    "CriticalSpeed",
    "CVTBeltConnectionStabilityAnalysis",
    "CVTPulleyStabilityAnalysis",
    "CVTStabilityAnalysis",
    "CycloidalAssemblyStabilityAnalysis",
    "CycloidalDiscCentralBearingConnectionStabilityAnalysis",
    "CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis",
    "CycloidalDiscStabilityAnalysis",
    "CylindricalGearMeshStabilityAnalysis",
    "CylindricalGearSetStabilityAnalysis",
    "CylindricalGearStabilityAnalysis",
    "CylindricalPlanetGearStabilityAnalysis",
    "DatumStabilityAnalysis",
    "DynamicModelForStabilityAnalysis",
    "ExternalCADModelStabilityAnalysis",
    "FaceGearMeshStabilityAnalysis",
    "FaceGearSetStabilityAnalysis",
    "FaceGearStabilityAnalysis",
    "FEPartStabilityAnalysis",
    "FlexiblePinAssemblyStabilityAnalysis",
    "GearMeshStabilityAnalysis",
    "GearSetStabilityAnalysis",
    "GearStabilityAnalysis",
    "GuideDxfModelStabilityAnalysis",
    "HypoidGearMeshStabilityAnalysis",
    "HypoidGearSetStabilityAnalysis",
    "HypoidGearStabilityAnalysis",
    "InterMountableComponentConnectionStabilityAnalysis",
    "KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis",
    "KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis",
    "KlingelnbergCycloPalloidConicalGearStabilityAnalysis",
    "KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis",
    "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis",
    "KlingelnbergCycloPalloidHypoidGearStabilityAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis",
    "MassDiscStabilityAnalysis",
    "MeasurementComponentStabilityAnalysis",
    "MicrophoneArrayStabilityAnalysis",
    "MicrophoneStabilityAnalysis",
    "MountableComponentStabilityAnalysis",
    "OilSealStabilityAnalysis",
    "PartStabilityAnalysis",
    "PartToPartShearCouplingConnectionStabilityAnalysis",
    "PartToPartShearCouplingHalfStabilityAnalysis",
    "PartToPartShearCouplingStabilityAnalysis",
    "PlanetaryConnectionStabilityAnalysis",
    "PlanetaryGearSetStabilityAnalysis",
    "PlanetCarrierStabilityAnalysis",
    "PointLoadStabilityAnalysis",
    "PowerLoadStabilityAnalysis",
    "PulleyStabilityAnalysis",
    "RingPinsStabilityAnalysis",
    "RingPinsToDiscConnectionStabilityAnalysis",
    "RollingRingAssemblyStabilityAnalysis",
    "RollingRingConnectionStabilityAnalysis",
    "RollingRingStabilityAnalysis",
    "RootAssemblyStabilityAnalysis",
    "ShaftHubConnectionStabilityAnalysis",
    "ShaftStabilityAnalysis",
    "ShaftToMountableComponentConnectionStabilityAnalysis",
    "SpecialisedAssemblyStabilityAnalysis",
    "SpiralBevelGearMeshStabilityAnalysis",
    "SpiralBevelGearSetStabilityAnalysis",
    "SpiralBevelGearStabilityAnalysis",
    "SpringDamperConnectionStabilityAnalysis",
    "SpringDamperHalfStabilityAnalysis",
    "SpringDamperStabilityAnalysis",
    "StabilityAnalysis",
    "StabilityAnalysisDrawStyle",
    "StabilityAnalysisOptions",
    "StraightBevelDiffGearMeshStabilityAnalysis",
    "StraightBevelDiffGearSetStabilityAnalysis",
    "StraightBevelDiffGearStabilityAnalysis",
    "StraightBevelGearMeshStabilityAnalysis",
    "StraightBevelGearSetStabilityAnalysis",
    "StraightBevelGearStabilityAnalysis",
    "StraightBevelPlanetGearStabilityAnalysis",
    "StraightBevelSunGearStabilityAnalysis",
    "SynchroniserHalfStabilityAnalysis",
    "SynchroniserPartStabilityAnalysis",
    "SynchroniserSleeveStabilityAnalysis",
    "SynchroniserStabilityAnalysis",
    "TorqueConverterConnectionStabilityAnalysis",
    "TorqueConverterPumpStabilityAnalysis",
    "TorqueConverterStabilityAnalysis",
    "TorqueConverterTurbineStabilityAnalysis",
    "UnbalancedMassStabilityAnalysis",
    "VirtualComponentStabilityAnalysis",
    "WormGearMeshStabilityAnalysis",
    "WormGearSetStabilityAnalysis",
    "WormGearStabilityAnalysis",
    "ZerolBevelGearMeshStabilityAnalysis",
    "ZerolBevelGearSetStabilityAnalysis",
    "ZerolBevelGearStabilityAnalysis",
)
