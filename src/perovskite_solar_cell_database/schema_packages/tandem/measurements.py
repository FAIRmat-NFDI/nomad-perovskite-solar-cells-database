from nomad.datamodel.data import ArchiveSection, EntryData
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.datamodel.metainfo.basesections import Experiment, ExperimentStep
from nomad.metainfo import Quantity, Section, SubSection
from nomad.metainfo.data_type import Enum

from .tandem import Storage


class Illumination(ArchiveSection):
    """
    Illumination conditions of the measurement.
    """

    type = Quantity(
        type=str,
        description='Type of illumination.',
    )

    brand = Quantity(
        type=str,
        description='The brand name and model number of the light source/solar simulator used',
    )

    simulator_class = Quantity(
        type=str,
        description='Class of the simulator.',
    )

    intensity = Quantity(
        type=float,
        description='Intensity of the illumination.',
        unit='W/m^2',
        a_el=ELNAnnotation(defaultDisplayUnit='W/m^2'),
    )

    spectrum = Quantity(
        type=str,
        description='Spectrum of the illumination.',
    )

    # TODO: Handle range as well as single value
    wavelength = Quantity(
        type=float,
        description='Wavelength of the illumination.',
        unit='nm',
        a_el=ELNAnnotation(defaultDisplayUnit='nm'),
    )

    direction = Quantity(
        type=Enum('Substrate', 'Superstrate'),
        description='Direction of the illumination.',
    )

    mask = Quantity(
        type=bool,
        description='Mask used for the illumination.',
    )

    mask_area = Quantity(
        type=float,
        description='Area of the mask.',
        unit='cm^2',
        a_eln=ELNAnnotation(defaultDisplayUnit='cm^2'),
    )


class MeasurementConditions(ArchiveSection):
    """
    Section for listing conditions and measurement protocol of a measurement.
    """

    duration = Quantity(
        type=float,
        description='Duration of the measurement.',
        unit='minute',
    )

    atmosphere = Quantity(
        type=str,
        description='Atmosphere during the measurement.',
    )

    humidity_relative = Quantity(
        type=float,
        description='Humidity during the measurement.',
        unit='dimensionless',
    )

    temperature = Quantity(
        type=float,
        description='Temperature during the measurement.',
        unit='K',
        a_eln=ELNAnnotation(defaultDisplayUnit='celsius'),
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
        type=str,
        description='Protocol for the preconditioning. Light soaking, potential biasing, etc.',
    )

    duration = Quantity(
        type=float,
        description='Time of the preconditioning.',
        unit='s',
    )

    potential = Quantity(
        type=float,
        description='Potential of the preconditioning.',
        unit='V',
    )

    light_intensity = Quantity(
        type=float,
        description='Light intensity of the preconditioning.',
        unit='W/m^2',
        a_eln=ELNAnnotation(defaultDisplayUnit='W/m^2'),
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

    component = Quantity(
        type=Enum('Whole Device', 'Bottom Cell', 'Top Cell', 'Other'),
        description=(
            'Component of the solar cell that is being measured (e.g., the whole device or a subcell).'
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
        type=float,
        description='Speed of the scan.',
        unit='mV/s',
        a_eln=ELNAnnotation(defaultDisplayUnit='mV/s'),
    )

    delay_time = Quantity(
        type=float,
        description='Delay time before the scan.',
        unit='milliseconds',
        a_el=ELNAnnotation(defaultDisplayUnit='ms'),
    )

    integration_time = Quantity(
        type=float,
        description='Integration time of the scan.',
        unit='milliseconds',
        a_eln=ELNAnnotation(defaultDisplayUnit='ms'),
    )

    voltage_step = Quantity(
        type=float,
        description='Voltage step of the scan.',
        unit='mV',
    )


class JVResults(ArchiveSection):
    """
    Results of a single JV scan.
    """

    short_circuit_current_density = Quantity(
        type=float,
        description='Short-circuit current density.',
        unit='mA/cm^2',
        a_eln=ELNAnnotation(defaultDisplayUnit='mA/cm^2'),
    )

    open_circuit_voltage = Quantity(
        type=float,
        description='Open-circuit voltage.',
        unit='V',
    )

    fill_factor = Quantity(
        type=float,
        description='Fill factor.',
    )

    power_conversion_efficiency = Quantity(
        type=float,
        description='Power conversion efficiency.',
    )

    maximum_power_point_voltage = Quantity(
        type=float,
        description='Voltage at maximum power.',
        unit='V',
    )

    maximum_power_point_current_density = Quantity(
        type=float,
        description='Current at maximum power.',
        unit='mA/cm^2',
        a_eln=ELNAnnotation(defaultDisplayUnit='mA/cm^2'),
    )

    resistance_series = Quantity(
        type=float,
        description='Series resistance.',
        unit='ohm*cm^2',
        a_eln=ELNAnnotation(defaultDisplayUnit='ohm*cm^2'),
    )

    resistance_shunt = Quantity(
        type=float,
        description='Shunt resistance.',
        unit='ohm*cm^2',
        a_eln=ELNAnnotation(defaultDisplayUnit='ohm*cm^2'),
    )


class JVMeasurement(Measurement):
    """
    JV measurement.
    """

    source = Quantity(
        type=Enum('This device', 'Analogous free standing cell', 'Unknown'),
        description=(
            'Indicates whether the measurement was performed on this specific device '
            'or on an analogous free standing cell.'
        ),
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
    )

    metric_unit = Quantity(
        type=str,
        description='Unit of the metric to be stabilised.',
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
        type=float,
        description='Initial power conversion efficiency.',
    )

    burn_in_observed = Quantity(
        type=bool,
        description='Burn in observed.',
    )

    power_conversion_efficiency_end = Quantity(
        type=float,
        description='End of experiment power conversion efficiency.',
    )

    power_conversion_efficiency_t95 = Quantity(
        type=float,
        description=(
            'The time after which the cell performance has degraded by 5 % '
            'with respect to the initial performance.'
        ),
        unit='hour',
    )

    power_conversion_efficiency_ts95 = Quantity(
        type=float,
        description=(
            'The time after which the cell performance has degraded by 5 % '
            'with respect to the performance after any initial burn in phase.'
        ),
        unit='hour',
    )

    power_conversion_efficiency_t80 = Quantity(
        type=float,
        description=(
            'The time after which the cell performance has degraded by 20 % '
            'with respect to the initial performance.'
        ),
        unit='hour',
    )

    power_conversion_efficiency_ts80 = Quantity(
        type=float,
        description=(
            'The time after which the cell performance has degraded by 20 % '
            'with respect to the performance after any initial burn in phase.'
        ),
        unit='hour',
    )

    power_conversion_efficiency_t80_est = Quantity(
        type=float,
        description=(
            'An estimated T80 for cells that were not measured sufficiently long '
            'for them to degrade by 20 %, with respect to the initial performance.'
        ),
        unit='hour',
    )

    power_conversion_efficiency_ts80_est = Quantity(
        type=float,
        description=(
            'An estimated Ts80 for cells that were not measured sufficiently long '
            'for them to degrade by 20 %, with respect to the performance after any '
            'initial burn in phase.'
        ),
        unit='hour',
    )

    power_conversion_efficiency_after_1000h = Quantity(
        type=float,
        description='Power conversion efficiency after 1000 hours.',
    )

    lifetime_energy_yield = Quantity(
        type=float,
        description='Lifetime energy yield.',
        unit='kWh/m^2',
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


class PerformedMeasurements(ArchiveSection):
    """
    Section for listing all measurements performed on this solar cell.
    """

    # JV measurements

    jv_full_device_forward = SubSection(
        section_def=JVMeasurement,
        description='JV measurement of the full device in the forward direction.',
    )

    jv_full_device_reverse = SubSection(
        section_def=JVMeasurement,
        description='JV measurement of the full device in the reverse direction.',
    )

    jv_bottom_cell = SubSection(
        section_def=JVMeasurement,
        description='JV measurement of the bottom cell.',
    )

    jv_bottom_cell_shaded = SubSection(
        section_def=JVMeasurement,
        description='JV measurement of the bottom cell under shading.',
    )

    jv_top_cell = SubSection(
        section_def=JVMeasurement,
        description='JV measurement of the top cell.',
    )

    # Stabilised performance measurements

    stabilised_performance_full_device = SubSection(
        section_def=StabilisedPerformance,
        description='Stabilised performance measurement of the full device.',
    )

    # TODO: Add measurements for subcells?

    # EQE

    eqe_full_device = SubSection(
        section_def=ExternalQuantumEfficiency,
        description='External quantum efficiency measurement of the full device.',
    )

    eqe_bottom_cell = SubSection(
        section_def=ExternalQuantumEfficiency,
        description='External quantum efficiency measurement of the bottom cell.',
    )

    eqe_bottom_cell_shaded = SubSection(
        section_def=ExternalQuantumEfficiency,
        description='External quantum efficiency measurement of the bottom cell under shading.',
    )

    eqe_top_cell = SubSection(
        section_def=ExternalQuantumEfficiency,
        description='External quantum efficiency measurement of the top cell.',
    )

    # Transmission

    transmission_bottom_cell = SubSection(
        section_def=Transmission,
        description='Transmission measurement of the bottom cell.',
    )

    transmission_top_cell = SubSection(
        section_def=Transmission,
        description='Transmission measurement of the top cell.',
    )

    # Stability

    stability = SubSection(
        section_def=StabilityMeasurement,
        description='Stability measurement.',
    )
