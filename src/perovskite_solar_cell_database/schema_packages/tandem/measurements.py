from nomad.datamodel.data import ArchiveSection
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.metainfo import MEnum, Quantity, Section, SubSection
from nomad.metainfo.metainfo import SchemaPackage

from perovskite_solar_cell_database.schema_packages.tandem.layer_stack import Storage

m_package = SchemaPackage()


class Illumination(ArchiveSection):
    """
    Illumination conditions of the measurement.
    """

    type = Quantity(
        description='Type of illumination.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    brand = Quantity(
        description='The brand name and model number of the light source/solar simulator used',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    simulator_class = Quantity(
        description='Class of the simulator.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    intensity = Quantity(
        description='Intensity of the illumination.',
        type=float,
        unit='W/m^2',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='W/m^2'),
    )

    spectrum = Quantity(
        description='Spectrum of the illumination.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    # TODO: Handle range as well as single value
    wavelength = Quantity(
        type=float,
        description='Wavelength of the illumination.',
        unit='nm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='nm'),
    )

    direction = Quantity(
        description='Direction of the illumination.',
        type=MEnum('Substrate', 'Superstrate'),
        a_eln=ELNAnnotation(component='EnumEditQuantity'),
    )

    mask = Quantity(
        description='Mask used for the illumination.',
        type=bool,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    mask_area = Quantity(
        description='Area of the mask.',
        type=float,
        unit='cm^2',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='cm^2'),
    )


class MeasurementConditions(ArchiveSection):
    """
    Section for listing conditions and measurement protocol of a measurement.
    """

    duration = Quantity(
        type=float,
        description='Duration of the measurement.',
        unit='minute',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='minute'
        ),
    )

    atmosphere = Quantity(
        type=str,
        description='Atmosphere during the measurement.',
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    humidity_relative = Quantity(
        type=float,
        description='Humidity during the measurement.',
        unit='dimensionless',
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    temperature = Quantity(
        type=float,
        description='Temperature during the measurement.',
        unit='K',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='K'),
    )

    illumination = SubSection(
        section_def=Illumination,
        description='Illumination conditions of the measurement.',
    )


class Preconditioning(ArchiveSection):
    """
    Preconditioning conditions before the measurement.
    """

    protocol = Quantity(
        description='Protocol for the preconditioning. Light soaking, potential biasing, etc.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    duration = Quantity(
        description='Time of the preconditioning.',
        type=float,
        unit='s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='s'),
    )

    potential = Quantity(
        description='Potential of the preconditioning.',
        type=float,
        unit='V',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='V'),
    )

    light_intensity = Quantity(
        description='Light intensity of the preconditioning.',
        type=float,
        unit='W/m^2',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='W/m^2'),
    )


class MeasurementResults(ArchiveSection):
    pass


class Measurement(ArchiveSection):
    """
    Measurement of a solar cell.
    """

    method = Quantity(
        type=str,
        description='Method of the measurement.',
    )

    certified = Quantity(
        description='TRUE if the measurement was certified, FALSE otherwise.',
        type=bool,
        default=False,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    subcell_association = Quantity(
        description='Indicates the association of the layer with a subcell. A value of 0 signifies that the entire device is monolithic. Any value greater than 0 associates the layer with a specific subcell, numbered sequentially from the bottom.',
        type=int,
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
            minValue=0,
        ),
    )

    conditions = SubSection(
        section_def=MeasurementConditions,
        description='Conditions of the measurement.',
    )

    preconditioning = SubSection(
        section_def=Preconditioning,
        description='Preconditioning conditions before the measurement.',
    )

    storage = SubSection(
        section_def=Storage,
        description='Storage conditions before of the measurement.',
    )

    results = SubSection(
        section_def=MeasurementResults,
        description='Results of the measurement.',
    )


class JVConditions(MeasurementConditions):
    """
    Parameters of a JV scan.
    """

    speed = Quantity(
        description='Speed of the scan.',
        type=float,
        unit='mV/s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mV/s'),
    )

    delay_time = Quantity(
        description='Delay time before the scan.',
        type=float,
        unit='milliseconds',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='ms'),
    )

    integration_time = Quantity(
        description='Integration time of the scan.',
        type=float,
        unit='milliseconds',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='ms'),
    )

    voltage_step = Quantity(
        description='Voltage step of the scan.',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mV'),
    )


class JVResults(ArchiveSection):
    """
    Results of a single JV scan.
    """

    short_circuit_current_density = Quantity(
        description='Short-circuit current density.',
        type=float,
        unit='mA/cm^2',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='mA/cm^2'
        ),
    )

    open_circuit_voltage = Quantity(
        description='Open-circuit voltage.',
        type=float,
        unit='V',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='V'),
    )

    fill_factor = Quantity(
        description='Fill factor.',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    power_conversion_efficiency = Quantity(
        description='Power conversion efficiency.',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    maximum_power_point_voltage = Quantity(
        description='Voltage at maximum power.',
        type=float,
        unit='V',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='V'),
    )

    maximum_power_point_current_density = Quantity(
        description='Current at maximum power.',
        type=float,
        unit='mA/cm^2',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='mA/cm^2'
        ),
    )

    resistance_series = Quantity(
        description='Series resistance.',
        type=float,
        unit='ohm*cm^2',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='ohm*cm^2'
        ),
    )

    resistance_shunt = Quantity(
        description='Shunt resistance.',
        type=float,
        unit='ohm*cm^2',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='ohm*cm^2'
        ),
    )


class JVMeasurement(Measurement):
    """
    JV measurement.
    """

    source = Quantity(
        description=(
            'Indicates whether the measurement was performed on this specific device '
            'or on an analogous free standing cell.'
        ),
        type=MEnum('This device', 'Analogous free standing cell', 'Unknown'),
        a_eln=ELNAnnotation(component='EnumEditQuantity'),
    )

    conditions = SubSection(
        section_def=JVConditions,
        description='Conditions and protocol of the JV measurement.',
    )

    results = SubSection(
        section_def=JVResults,
        description='Results of the JV measurement.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'JV'


class StabilisedPerformanceConditions(MeasurementConditions):
    procedure = Quantity(
        type=str,
        description=(
            'Procedure of the stabilised performance measurement. '
            'Maximum power point tracking (MPPT), constant potential, etc.'
        ),
    )

    # TODO: Handle different metric types
    metric_value = Quantity(
        type=float,
        description='Value of the metric to be stabilised.',
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    metric_unit = Quantity(
        type=str,
        description='Unit of the metric to be stabilised.',
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )


class StabilisedPerformance(Measurement):
    """
    Stabilised performance measurement.
    """

    conditions = SubSection(
        section_def=StabilisedPerformanceConditions,
        description='Conditions of the stabilised performance measurement.',
    )

    results = SubSection(
        section_def=JVResults,
        description='Results of the stabilised performance measurement.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'Stabilised performance'


class EQEResults(ArchiveSection):
    integrated_short_circuit_current_density = Quantity(
        type=float,
        description='Integrated short-circuit current density.',
        unit='mA/cm^2',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='mA/cm^2'
        ),
    )


class ExternalQuantumEfficiency(Measurement):
    """
    External quantum efficiency measurement.
    """

    results = SubSection(
        section_def=EQEResults,
        description='Results of the external quantum efficiency measurement.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'External quantum efficiency'


class TransmissionResults(ArchiveSection):
    integrated_transmission = Quantity(
        type=float,
        description='Integrated transmission in the relevant wavelength range.',
        unit='dimensionless',
    )


class Transmission(Measurement):
    """
    Transmission measurement.
    """

    results = SubSection(
        section_def=TransmissionResults,
        description='Results of the transmission measurement.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'Transmission'


class StabilityConditions(MeasurementConditions):
    pass


class StabilityResults(ArchiveSection):
    power_conversion_efficiency_initial = Quantity(
        description='Initial power conversion efficiency.',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    burn_in_observed = Quantity(
        description='Burn in observed.',
        type=bool,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    power_conversion_efficiency_final = Quantity(
        description='End of experiment power conversion efficiency.',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    time_until_pce_95 = Quantity(
        description=(
            'The time after which the cell performance has degraded by 5 % '
            'with respect to the initial performance.'
        ),
        type=float,
        unit='hour',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='hour'),
    )

    time_after_burn_in_until_pce_95 = Quantity(
        description=(
            'The time after which the cell performance has degraded by 5 % '
            'with respect to the performance after any initial burn in phase.'
        ),
        type=float,
        unit='hour',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='hour'),
    )

    time_until_pce_80 = Quantity(
        description=(
            'The time after which the cell performance has degraded by 20 % '
            'with respect to the initial performance.'
        ),
        type=float,
        unit='hour',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='hour'),
    )

    time_after_burn_in_until_pce_80 = Quantity(
        description=(
            'The time after which the cell performance has degraded by 20 % '
            'with respect to the performance after any initial burn in phase.'
        ),
        type=float,
        unit='hour',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='hour'),
    )

    time_after_until_pce_80_estimated = Quantity(
        description=(
            'An estimated T80 for cells that were not measured sufficiently long '
            'for them to degrade by 20 %, with respect to the initial performance.'
        ),
        type=float,
        unit='hour',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='hour'),
    )

    time_after_burn_in_until_pce_80_estimated = Quantity(
        description=(
            'An estimated Ts80 for cells that were not measured sufficiently long '
            'for them to degrade by 20 %, with respect to the performance after any '
            'initial burn in phase.'
        ),
        type=float,
        unit='hour',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='hour'),
    )

    power_conversion_efficiency_after_1000h = Quantity(
        description='Power conversion efficiency after 1000 hours.',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    lifetime_energy_yield = Quantity(
        description='Lifetime energy yield.',
        unit='kWh/m^2',
        type=float,
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='kWh/m^2'
        ),
    )


class StabilityMeasurement(Measurement):
    """
    Stability measurement.
    """

    conditions = SubSection(
        section_def=StabilityConditions,
        description='Conditions of the stability measurement.',
    )

    results = SubSection(
        section_def=StabilityResults,
        description='Results of the stability measurement.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'Stability'


class PerformedMeasurements(ArchiveSection):
    """
    Section for listing all measurements performed on this solar cell.
    """

    jv_measurements = SubSection(
        description='JV measurements performed on this device.',
        section_def=JVMeasurement,
        repeats=True,
    )

    eqe_measurements = SubSection(
        description='EQE measurements performed on this device.',
        section_def=ExternalQuantumEfficiency,
        repeats=True,
    )

    performance_measurements = SubSection(
        description='Performance measurements performed on this device.',
        section_def=StabilisedPerformance,
        repeats=True,
    )

    stability_measurements = SubSection(
        description='Stability measurements performed on this device.',
        section_def=StabilityMeasurement,
        repeats=True,
    )

    transmission_measurements = SubSection(
        description='Transmission measurements performed on this device.',
        section_def=Transmission,
        repeats=True,
    )


m_package.__init_metainfo__()
