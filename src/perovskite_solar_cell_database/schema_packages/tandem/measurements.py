from nomad.datamodel.data import ArchiveSection
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.metainfo import Datetime, MEnum, Quantity, Section, SubSection
from nomad.metainfo.metainfo import SchemaPackage

m_package = SchemaPackage()


### Subsections called by measurements
class Measurement(ArchiveSection):
    """
    Measurement of a solar cell.
    """

    time_stamp = Quantity(
        description='Date the measurement was performed.',
        type=Datetime,
        a_eln=ELNAnnotation(component='DateTimeEditQuantity'),
    )

    age_of_device = Quantity(
        description='Age of the device at the time of measurement start.',
        type=float,
        unit='hr',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='hr'),
    )

    duration = Quantity(
        type=float,
        description='Duration of the measurement.',
        unit='minute',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='minute'
        ),
    )

    certified = Quantity(
        description='TRUE if the measurement was certified by an external certification institute, FALSE otherwise.',
        type=bool,
        default=False,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    device_subset = Quantity(
        description="""
                Describes if the measurement was done on the compleat device or on an individual subcell. 
                0 = measurement was done on the complete device, 
                1 = measurement was done on the bottom subcell, 
                2 = measurement was done on the second subcell (top cell in a 2-junction device)
                3 = measurement was done on the third subcell (top cell in a 3-junction device)
                """,
        type=int,
        default=0,
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
            minValue=0,
        ),
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

    def normalize(self, archive, logger):
        super().normalize(archive, logger)

        # Ensure FF is between 0 and 1
        if hasattr(self, 'fill_factor') and self.fill_factor is not None:
            if self.fill_factor > 2.0:
                self.fill_factor = self.fill_factor / 100


class JVRawData(ArchiveSection):
    """
    Raw data of a JV scan.
    """

    voltage = Quantity(
        description='Voltage during the measurement.', type=float, shape=['*']
    )

    current = Quantity(
        description='Current density during the measurement.',
        type=float,
        shape=['*'],
    )


class JVConditions(ArchiveSection):
    """
    Parameters of a JV scan.
    """

    scan_direction = Quantity(
        description=('The scan direction of the JV measurement. Forward or reverse.'),
        type=MEnum(['forward', 'reversed']),
        a_eln=ELNAnnotation(component='EnumEditQuantity'),
    )

    scan_speed = Quantity(
        description='Speed of the scan.',
        type=float,
        unit='mV/s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mV/s'),
    )

    voltage_step = Quantity(
        description='Voltage step of the scan.',
        type=float,
        unit='mV',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mV'),
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

    source_meter = Quantity(
        description='Brand name and model of the Source-meter used for the measurement.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )


class EnvironmentalConditions(ArchiveSection):
    """
    Environmental conditions during the activity.
    """

    ambient_conditions = Quantity(
        description='TRUE if the activity is occurring in in uncontrolled ambient conditions. FALSE otherwise',
        type=bool,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    in_glove_box = Quantity(
        type=bool,
        shape=[],
        description="""True if the the activity was performed in a glove box, False otherwise.
            """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    atmosphere = Quantity(
        description='Atmosphere during the activity.',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'air',
                    'dry air',
                    'N2',
                    'Ar',
                    'He',
                    'O2',
                    'H2',
                    'vacuum',
                    'other',
                ]
            ),
        ),
    )

    relative_humidity = Quantity(
        description='Relative humidity during the activity. In %, i.e. a number between 0 and 100.',
        type=float,
        # unit='%',
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    ambient_temperature = Quantity(
        description='Ambient temperature during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    device_temperature = Quantity(
        description='The temperature of the device during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    pressure = Quantity(
        description='The atmospheric pressure during the activity.',
        type=float,
        unit='Pa',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='Pa'),
    )

    oxygen_concentration = Quantity(
        description='The oxygen concentration during the activity. In %, i.e. a number between 0 and 100.',
        type=float,
        # unit='%',
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )


class EnvironmentalConditionsOutdoor(ArchiveSection):
    """
    Environmental conditions during the activity.
    """

    ambient_temperature_min = Quantity(
        description='Minimum ambient temperature during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    ambient_temperature_max = Quantity(
        description='Maximum ambient temperature during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    ambient_temperature_average = Quantity(
        description='Average ambient temperature during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    device_temperature_min = Quantity(
        description='Minimum temperature of the device during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    device_temperature_max = Quantity(
        description='Maximum temperature of the device during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    device_temperature_average = Quantity(
        description='Average temperature of the device during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    relative_humidity_min = Quantity(
        description='Minimum relative humidity during the activity. In %, i.e. a number between 0 and 100.',
        type=float,
        # unit='%',
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    relative_humidity_max = Quantity(
        description='Maximum relative humidity during the activity. In %, i.e. a number between 0 and 100.',
        type=float,
        # unit='%',
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    relative_humidity_average = Quantity(
        description='Average relative humidity during the activity. In %, i.e. a number between 0 and 100.',
        type=float,
        # unit='%',
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )


class Illumination(ArchiveSection):
    """
    Details about the illumination used for the measurement.
    """

    intensity = Quantity(
        description='Intensity of the illumination.',
        type=float,
        unit='W/m^2',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='W/m^2'),
    )

    illuminance = Quantity(
        description='Illuminance of the illumination. Mostly important for low light indoor measurements.',
        type=float,
        unit='lx',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='lx'),
    )

    direction = Quantity(
        description='Direction of the illumination with respect to the device.',
        type=MEnum(['substrate', 'superstrate']),
        a_eln=ELNAnnotation(component='EnumEditQuantity'),
    )

    mask = Quantity(
        description='TRUE if a shadow mask used during the measurement.',
        type=bool,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    mask_area = Quantity(
        description='Area of the shadow mask used during the measurement.',
        type=float,
        unit='cm^2',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='cm^2'),
    )

    uv_filter = Quantity(
        description='TRUE if a UV-filter is used. FALSE otherwise.',
        type=bool,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    top_cell_filter = Quantity(
        description='TRUE if the measurement is done on a subcell and the light is filtered trough the remaining subcells. e.g. a silicon bottom cell is measured under light flittered by a perovskite top cell.',
        type=bool,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )


class LightSource(ArchiveSection):
    """
    Details about the light source used for the measurement.
    """

    spectrum = Quantity(
        description='Spectrum of the illumination.',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'Dark',
                    'AM1.5',
                    'AM1.5G',
                    'AM0',
                    'AM1.0',
                    'UV',
                    'UVA',
                    'UVB',
                    'Monochromatic',
                    'Ambient indoor',
                    'Ambient outdoor',
                    'Other',
                ]
            ),
        ),
    )

    light_source = Quantity(
        description='Type of illumination.',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'Dark conditions',
                    'Solar simulator unspecified',
                    'Metal halide',
                    'Sulfur plasma',
                    'LED',
                    'White led',
                    'Xenon',
                    'Halogen',
                    'Laser',
                    'Incandescent',
                    'Fluorescent',
                    'Ambient indoor',
                    'Ambient outdoor',
                    'UV',
                    'Proton source',
                    'Other',
                ]
            ),
        ),
    )

    solar_simulator_class = Quantity(
        description='Class of the solar simulator.',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'AAA',
                    'AAB',
                    'AAC',
                    'ABA',
                    'ABB',
                    'ABC',
                    'ACA',
                    'ACB',
                    'ACC',
                    'BAA',
                    'BAB',
                    'BAC',
                    'BBA',
                    'BBB',
                    'BBC',
                    'BCA',
                    'BCB',
                    'BCC',
                    'CAA',
                    'CAB',
                    'CAC',
                    'CBA',
                    'CBB',
                    'CBC',
                    'CCA',
                    'CCB',
                    'CCC',
                ]
            ),
        ),
    )

    light_source_model = Quantity(
        description='The brand name and model of the light source/solar simulator used',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    peak_wavelength = Quantity(
        type=float,
        description='Peak wavelength of the light.',
        unit='nm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='nm'),
    )

    # Spectrum data
    intensity = Quantity(description='The light intensity.', type=float, shape=['*'])

    wavelength = Quantity(description='the wavelength.', type=float, shape=['*'])


class Preconditioning(ArchiveSection):
    """
    Preconditioning conditions before the measurement.
    """

    protocol = Quantity(
        description='Protocol for the preconditioning. Light soaking, potential biasing, etc.',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'Light soaking',
                    'Potential biasing',
                    'Current biasing',
                    'Temperature biasing',
                    'Other',
                ]
            ),
        ),
    )

    duration = Quantity(
        description='Time of the preconditioning program.',
        type=float,
        unit='s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='s'),
    )

    potential = Quantity(
        description='Potential during the activity.',
        type=float,
        unit='V',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='V'),
    )

    light_intensity = Quantity(
        description='Light intensity of the activity.',
        type=float,
        unit='W/m^2',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='W/m^2'),
    )

    current_density = Quantity(
        description='Current density during the activity.',
        type=float,
        unit='mA/cm^2',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='mA/cm^2'
        ),
    )

    # Subsections
    environmental_conditions = SubSection(
        section_def=EnvironmentalConditions,
        description='Environmental conditions during the activity.',
    )


class CertificationDetails(ArchiveSection):
    """
    Details about the certification of the measurement.
    """

    certifying_institution = Quantity(
        description='Name of the certifying institution.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    certification_protocol = Quantity(
        description='The name of the protocol used.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    certification_date = Quantity(
        description='The date of the official certificate.',
        type=Datetime,
        a_eln=ELNAnnotation(component='DateTimeEditQuantity'),
    )


class EQEResults(ArchiveSection):
    """
    Results of an EQE measurement.
    """

    integrated_short_circuit_current_density = Quantity(
        description='Integrated Short-circuit current density.',
        type=float,
        unit='mA/cm^2',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='mA/cm^2'
        ),
    )

    eqe_onset = Quantity(
        description='The onset where the EQE starts to increase. Is a proxy for the band gap',
        type=float,
        unit='nm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='nm'),
    )

    eqe_inflection_point = Quantity(
        description='The inflection point after which the EQE starts to increase. Is a proxy for the band gap',
        type=float,
        unit='nm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='nm'),
    )

    eqe_max = Quantity(
        description='The maximum EQE value. In %, i.e. a number between 0 and 100.',
        type=float,
        # unit='%',
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )


class EQEConditions(ArchiveSection):
    """
    EQE conditions
    """

    wavelength_at_start = Quantity(
        description='Wavelength at start of measurement',
        type=float,
        unit='nm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='nm'),
    )

    wavelength_at_end = Quantity(
        description='Wavelength at end of measurement',
        type=float,
        unit='nm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='nm'),
    )

    step_size = Quantity(
        description='The size of the steps in the scanning',
        type=float,
        unit='nm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='nm'),
    )

    integration_time = Quantity(
        description='Integration time for each wavelength',
        type=float,
        unit='s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='s'),
    )

    scan_speed = Quantity(
        description='Scan speed',
        type=float,
        unit='nm/s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='nm/s'),
    )

    equipment = Quantity(
        description='Brand name and model of the equipment used for the measurement.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )


class EQERawData(ArchiveSection):
    """
    Raw data of an EQE measurement.
    """

    eqe = Quantity(description='The EQE.', type=float, shape=['*'])

    wavelength = Quantity(description='the wavelength.', type=float, shape=['*'])


class StabilizedPerformanceResults(ArchiveSection):
    """
    Results of a stabilized measurement .
    """

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


class StabilizedPerformanceDetails(ArchiveSection):
    """
    Details for stabilized performance measurements.
    """

    type_of_measurement = Quantity(
        description='Type of measurement.',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'constant potential',
                    'constant current',
                    'maximum power point tracking',
                ]
            ),
        ),
    )

    potential = Quantity(
        description='The potential (if measured at constant potential)',
        type=float,
        unit='V',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='V'),
    )

    current_density = Quantity(
        description='The current density (if measured at constant current)',
        type=float,
        unit='mA/cm^2',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='mA/cm^2'
        ),
    )

    source_meter = Quantity(
        description='Brand name of the Source-meter used for the measurement.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )


class StabilizedPerformanceRawData(ArchiveSection):
    """
    Raw data of an EQE measurement.
    """

    power_conversion_efficiency = Quantity(
        description='The power conversion efficiency.', type=float, shape=['*']
    )

    time = Quantity(description='The time', type=float, shape=['*'])


class StabilityResults(ArchiveSection):
    """
    Results of a stability measurement.
    """

    power_conversion_efficiency_start = Quantity(
        description='Power conversion efficiency at the start of the measurement.',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    power_conversion_efficiency_end = Quantity(
        description='Power conversion efficiency at the end of the measurement. ',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    burn_in = Quantity(
        description='TRUE if if an initial burn in period is observed. FALSE otherwise.',
        type=bool,
        default=False,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    burn_in_length = Quantity(
        description='Length of the burn in period.',
        type=float,
        unit='hr',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='hr'),
    )

    power_conversion_efficiency_after_burn_in = Quantity(
        description='Power conversion efficiency at the end of the burn in phase.',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    power_conversion_efficiency_1000h = Quantity(
        description='Power conversion efficiency after 1000h.',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    T95 = Quantity(
        description='The time after which the cell have degraded to 95 % of the initial efficiency.',
        type=float,
        unit='hr',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='hr'),
    )

    T95s = Quantity(
        description='The time after which the cell have degraded to 95 % of the efficiency reached after the initial burn in period.',
        type=float,
        unit='hr',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='hr'),
    )

    T80 = Quantity(
        description='The time after which the cell have degraded to 80 % of the initial efficiency.',
        type=float,
        unit='hr',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='hr'),
    )

    T80s = Quantity(
        description='The time after which the cell have degraded to 80 % of the efficiency reached after the initial burn in period.',
        type=float,
        unit='hr',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='hr'),
    )

    energy_yield = Quantity(
        description='The energy yield during the measurement.',
        type=float,
        unit='kWh/m^2',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='kWh/m^2'
        ),
    )

    energy_yield = Quantity(
        description='The yearly average energy yield during the measurement in kWh/m^2/year.',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )


class StabilityDetails(ArchiveSection):
    """
    Details for stability measurements.
    """

    potential_bias_regime = Quantity(
        description='The potential regime during the measurement e.g. open circuit, constant potential, constant current,  maximum powerpoint tracking, etc.',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'maximum power point tracking',
                    'open circuit',
                    'constant potential',
                    'constant current',
                    'constant resistance',
                    'other',
                ]
            ),
        ),
    )

    periodic_jv_measurements = Quantity(
        description="""TRUE if there has been a periodicity to the load of the cell in terms of for example potential, 
        current, resistance, or temperature during the stability measurements""",
        type=bool,
        default=False,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    evaluation_periodicity = Quantity(
        description='The length between the JV measurements. If the device is evaluated by periodically doing JV-measurements (as common for evaluation of stability in the dark)',
        type=float,
        unit='hr',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='hr'),
    )

    potential = Quantity(
        description='The potential (if measured at constant potential)',
        type=float,
        unit='V',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='V'),
    )

    current_density = Quantity(
        description='The current density (if measured at constant current)',
        type=float,
        unit='mA/cm^2',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='mA/cm^2'
        ),
    )

    resistance = Quantity(
        description='The resistance the device is held at (if measured at constant resistance)',
        type=float,
        unit='ohm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='ohm'),
    )

    source_meter = Quantity(
        description='Brand name and model of the Source-meter used for the measurement.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )


class StabilityRawData(ArchiveSection):
    """
    Raw data of an EQE measurement.
    """

    power_conversion_efficiency = Quantity(
        description='The power conversion efficiency.', type=float, shape=['*']
    )

    time = Quantity(description='The time', type=float, shape=['*'])


class LoadCycleSegments(ArchiveSection):
    """
    Details for load cycling measurements.
    """

    duration = Quantity(
        description='Duration of the segment.',
        type=float,
        unit='minute',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='minute'
        ),
    )

    potential_bias_regime = Quantity(
        description='The potential regime during the measurement e.g. open circuit, constant potential, constant current,  maximum powerpoint tracking, etc.',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'maximum power point tracking',
                    'open circuit',
                    'constant potential',
                    'constant current',
                    'constant resistance',
                    'other',
                ]
            ),
        ),
    )

    potential = Quantity(
        description='The potential (if measured at constant potential)',
        type=float,
        unit='V',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='V'),
    )

    current_density = Quantity(
        description='The current density (if measured at constant current)',
        type=float,
        unit='mA/cm^2',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='mA/cm^2'
        ),
    )

    resistance = Quantity(
        description='The resistance the device is held at (if measured at constant resistance)',
        type=float,
        unit='ohm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='ohm'),
    )

    environmental_conditions = SubSection(
        section_def=EnvironmentalConditions,
        description='Environmental conditions during the activity.',
    )

    light_source = SubSection(
        section_def=LightSource,
        description='Details about the light source used for the measurement.',
    )

    illumination = SubSection(
        section_def=Illumination,
        description='Details about the illumination used for the measurement.',
    )


class LoadCycle(ArchiveSection):
    """
    Details for load cycling measurements.
    """

    number_of_cycles = Quantity(
        description='The number of load cycles during the measurement.',
        type=int,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    number_of_segments_in_cycle = Quantity(
        description='The number of segments in the load cycle.',
        type=int,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    segments = SubSection(
        section_def=LoadCycleSegments,
        description='Details for the segments in the load cycle.',
        repeats=True,
    )


class OutdoorPerformanceDetails(StabilityDetails):
    """
    Details for outdoor performance measurements.
    """

    time_stamp_start = Quantity(
        description='Date and time the measurement was started.',
        type=Datetime,
        a_eln=ELNAnnotation(component='DateTimeEditQuantity'),
    )

    time_stamp_end = Quantity(
        description='Date and time the measurement was started.',
        type=Datetime,
        a_eln=ELNAnnotation(component='DateTimeEditQuantity'),
    )

    illuminated = Quantity(
        description='TRUE if the device is illuminated during the stability evaluation. FALSE if the stability reefer to stability under dark conditions.',
        type=bool,
        default=False,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    country = Quantity(
        description='The country where the measurement was done.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    city = Quantity(
        description='The city where the measurement was done.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    latitude = Quantity(
        description='The latitude of the measurement location.',
        type=float,
        unit='degrees',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='degrees'
        ),
    )

    longitude = Quantity(
        description='The latitude of the measurement location.',
        type=float,
        unit='degrees',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='degrees'
        ),
    )

    tilt = Quantity(
        description='The tilt of the device during the measurement.',
        type=float,
        unit='degrees',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='degrees'
        ),
    )

    direction = Quantity(
        description="""The direction of the device during the measurement.
        0 is north
        90 is east
        180 is south
        270 is west""",
        type=float,
        unit='degrees',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='degrees'
        ),
    )

    number_of_solar_tracking_axes = Quantity(
        description='The number of solar tracking axes. 0 means a stationary device.',
        type=int,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )


class TransmissionResults(ArchiveSection):
    """
    Results of a transmission measurement.
    """

    average_transmission = Quantity(
        description='The average transmission in the visible range (400-700 nm)',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )


class TransmissionDetails(ArchiveSection):
    """
    Details for transmission measurements.
    """

    wavelength_at_start = Quantity(
        description='Wavelength at start of measurement',
        type=float,
        unit='nm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='nm'),
    )

    wavelength_at_end = Quantity(
        description='Wavelength at end of measurement',
        type=float,
        unit='nm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='nm'),
    )

    step_size = Quantity(
        description='The size of the steps in the scanning',
        type=float,
        unit='nm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='nm'),
    )

    equipment = Quantity(
        description='Brand name and model of the equipment used for the measurement.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )


class TransmissionRawData(ArchiveSection):
    """
    Raw data of an Transmission measurement.
    """

    transmission = Quantity(description='The transmission.', type=float, shape=['*'])

    wavelength = Quantity(description='the wavelength.', type=float, shape=['*'])


class FlexibilityResults(ArchiveSection):
    """
    Results of a flexibility measurement.
    """

    power_conversion_efficiency_start = Quantity(
        description='Power conversion efficiency at the start of the measurement.',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    power_conversion_efficiency_end = Quantity(
        description='Power conversion efficiency at the end of the measurement. ',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )


class FlexibilityDetails(ArchiveSection):
    """
    Details for flexibility measurements.
    """

    number_of_bending_cycles = Quantity(
        description='The number of bending cycles.',
        type=int,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    bending_radius = Quantity(
        description='The bending radius in degrees.',
        type=float,
        unit='degree',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='degree'
        ),
    )


### Measurements
class JV(Measurement):
    """
    JV measurement.
    """

    light_regime = Quantity(
        description=(
            """
                     The light regime during the JV measurement e.g.
                     Standard light (AM 1.5)
                     Dark
                     Concentrated light
                     Indoor light
                     Other 
                     """
        ),
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'dark',
                    'standard light',
                    'concentrated light',
                    'indoor light',
                    'other',
                ]
            ),
        ),
    )

    preconditioned = Quantity(
        description='TRUE if the device has been preconditioned before the measurement, FALSE otherwise.',
        type=bool,
        default=False,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    # Subsections
    results = SubSection(
        section_def=JVResults,
        description='Results of the JV measurement.',
    )

    measurement_conditions = SubSection(
        section_def=JVConditions,
        description='Measurement details.',
    )

    environmental_conditions = SubSection(
        section_def=EnvironmentalConditions,
        description='Environmental conditions during the activity.',
    )

    light_source = SubSection(
        section_def=LightSource,
        description='Details about the light source used for the measurement.',
    )

    illumination = SubSection(
        section_def=Illumination,
        description='Details about the illumination used for the measurement.',
    )

    preconditioned_conditions = SubSection(
        section_def=Preconditioning,
        description='Preconditioning conditions before the measurement.',
    )

    sample_history = SubSection(
        section_def=EnvironmentalConditions,
        description="""A description of the conditions under which the sample have been stored between
        the finalization of the device and the described measurement.""",
    )

    certification_details = SubSection(
        section_def=CertificationDetails,
        description='Details about the certification of the measurement.',
    )

    raw_data = SubSection(
        section_def=JVRawData,
        description='Raw data from the JV measurement.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'JV'


class ExternalQuantumEfficiency(Measurement):
    """
    EQE measurement.
    """

    preconditioned = Quantity(
        description='TRUE if the device has been preconditioned before the measurement, FALSE otherwise.',
        type=bool,
        default=False,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    bias_light = Quantity(
        description='TRUE if the measurement is done under bias light, FALSE otherwise.',
        type=bool,
        default=False,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    # Subsections
    results = SubSection(
        section_def=EQEResults,
        description='Results of the EQE measurement.',
    )

    measurement_conditions = SubSection(
        section_def=EQEConditions,
        description='Measurement details.',
    )

    environmental_conditions = SubSection(
        section_def=EnvironmentalConditions,
        description='Environmental conditions during the activity.',
    )

    bias_light_source = SubSection(
        section_def=LightSource,
        description='Details about the light source used for the bias light.',
    )

    bias_illumination = SubSection(
        section_def=Illumination,
        description='Details about the bias illumination used for the measurement.',
    )

    preconditioned_conditions = SubSection(
        section_def=Preconditioning,
        description='Preconditioning conditions before the measurement.',
    )

    sample_history = SubSection(
        section_def=EnvironmentalConditions,
        description="""A description of the conditions under which the sample have been stored between
        the finalization of the device and the described measurement.""",
    )

    certification_details = SubSection(
        section_def=CertificationDetails,
        description='Details about the certification of the measurement.',
    )

    raw_data = SubSection(
        section_def=EQERawData,
        description='Raw data from the EQE measurement.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'EQE'


class StabilizedPerformance(Measurement):
    """
    Stabilized performance
    """

    light_regime = Quantity(
        description=(
            """
                     The light regime during the JV measurement e.g.
                     Standard light (AM 1.5)
                     Dark
                     Concentrated light
                     Indoor light
                     Other 
                     """
        ),
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'dark',
                    'standard light',
                    'concentrated light',
                    'indoor light',
                    'other',
                ]
            ),
        ),
    )

    preconditioned = Quantity(
        description='TRUE if the device has been preconditioned before the measurement, FALSE otherwise.',
        type=bool,
        default=False,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    # Subsections
    results = SubSection(
        section_def=StabilizedPerformanceResults,
        description='The results from the measurement.',
    )

    measurement_conditions = SubSection(
        section_def=StabilizedPerformanceDetails,
        description='The results from the measurement.',
    )

    environmental_conditions = SubSection(
        section_def=EnvironmentalConditions,
        description='Environmental conditions during the activity.',
    )

    light_source = SubSection(
        section_def=LightSource,
        description='Details about the light source used for the measurement.',
    )

    illumination = SubSection(
        section_def=Illumination,
        description='Details about the illumination used for the measurement.',
    )

    preconditioned_conditions = SubSection(
        section_def=Preconditioning,
        description='Preconditioning conditions before the measurement.',
    )

    sample_history = SubSection(
        section_def=EnvironmentalConditions,
        description="""A description of the conditions under which the sample have been stored between
        the finalization of the device and the described measurement.""",
    )

    certification_details = SubSection(
        section_def=CertificationDetails,
        description='Details about the certification of the measurement.',
    )

    raw_data = SubSection(
        section_def=StabilizedPerformanceRawData,
        description='Raw data from the stabilized performance measurement.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'Stabilized Performance'


class Stability(Measurement):
    """
    Stability measurement.
    """

    illuminated = Quantity(
        description='TRUE if the device is illuminated during the stability evaluation. FALSE if the stability reefer to stability under dark conditions.',
        type=bool,
        default=False,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    load_cycling = Quantity(
        description='TRUE if the load have been cycled during the stability measurements.',
        type=bool,
        default=False,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    stability_protocol = Quantity(
        description=(
            """
                         The measurement protocol. For definitions and classifications of stability protocols, 
                         see https://www.nature.com/articles/s41560-019-0529-5  
                     """
        ),
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'ISOS-D-1',
                    'ISOS-D-1I',
                    'ISOS-D-2',
                    'ISOS-D-2I',
                    'ISOS-D-3',
                    'ISOS-V-1',
                    'ISOS-V-1I',
                    'ISOS-V-2',
                    'ISOS-V-2I',
                    'ISOS-V-3',
                    'ISOS-L-1',
                    'ISOS-L-1I',
                    'ISOS-L-2',
                    'ISOS-L-2I',
                    'ISOS-L-3',
                    'ISOS-O-1',
                    'ISOS-O-2',
                    'ISOS-O-3',
                    'ISOS-T-1',
                    'ISOS-T-1I',
                    'ISOS-T-2',
                    'ISOS-T-2I',
                    'ISOS-T-3',
                    'ISOS-LC-1',
                    'ISOS-LC-1I',
                    'ISOS-LC-2',
                    'ISOS-LC-2I',
                    'ISOS-LC-3',
                    'ISOS-LC-3I',
                    'ISOS-LT-1',
                    'ISOS-LT-2',
                    'ISOS-LT-3',
                ]
            ),
        ),
    )

    # Subsections
    results = SubSection(
        section_def=StabilityResults,
        description='Results of the stability measurement.',
    )

    measurement_conditions = SubSection(
        section_def=StabilityDetails,
        description='Measurement details.',
    )

    environmental_conditions = SubSection(
        section_def=EnvironmentalConditions,
        description='Environmental conditions during the activity.',
    )

    illumination = SubSection(
        section_def=Illumination,
        description='Details about the illumination used for the measurement.',
    )

    light_source = SubSection(
        section_def=LightSource,
        description='Details about the light source used for the measurement.',
    )

    load_cycling_conditions = SubSection(
        section_def=LoadCycle,
        description='Details about how the load of the cell have varied during the stability.',
    )

    sample_history = SubSection(
        section_def=EnvironmentalConditions,
        description="""A description of the conditions under which the sample have been stored between
        the finalization of the device and the described measurement.""",
    )

    certification_details = SubSection(
        section_def=CertificationDetails,
        description='Details about the certification of the measurement.',
    )

    # JV measurements
    jv_measurements = SubSection(
        section_def=JV,
        description='JV measurements during the stability measurement.',
        repeats=True,
    )

    raw_data = SubSection(
        section_def=StabilityRawData,
        description='Raw data from the stability measurement.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'Stability'


class OutdoorPerformance(Measurement):
    """
    Outdoor performance measurements.
    """

    load_cycling = Quantity(
        description='TRUE if the load have been cycled during the stability measurements.',
        type=bool,
        default=False,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    stability_protocol = Quantity(
        description=(
            """
                         The measurement protocol. For definitions and classifications of stability protocols, 
                         see https://www.nature.com/articles/s41560-019-0529-5  
                     """
        ),
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'ISOS-O-1',
                    'ISOS-O-2',
                    'ISOS-O-3',
                    'Other',
                ]
            ),
        ),
    )

    # Subsections
    results = SubSection(
        section_def=StabilityResults,
        description='Results of the stability measurement.',
    )

    outdoor_performance_details = SubSection(
        section_def=OutdoorPerformanceDetails,
        description='Details for outdoor performance measurements.',
    )

    environmental_conditions = SubSection(
        section_def=EnvironmentalConditionsOutdoor,
        description='Environmental conditions during the activity.',
    )

    measurement_conditions = SubSection(
        section_def=StabilityDetails,
        description='Measurement details.',
    )

    load_cycling_conditions = SubSection(
        section_def=LoadCycle,
        description='Details about how the load of the cell have varied during the stability.',
    )

    sample_history = SubSection(
        section_def=EnvironmentalConditions,
        description="""A description of the conditions under which the sample have been stored between
        the finalization of the device and the described measurement.""",
    )

    certification_details = SubSection(
        section_def=CertificationDetails,
        description='Details about the certification of the measurement.',
    )

    # JV measurements
    jv_measurements = SubSection(
        section_def=JV,
        description='JV measurements during the stability measurement.',
        repeats=True,
    )

    raw_data = SubSection(
        section_def=StabilityRawData,
        description='Raw data from the stability measurement.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'Outdoor Performance'


class Transmission(Measurement):
    """
    Transmission measurement.
    """

    # Subsections
    results = SubSection(
        section_def=TransmissionResults,
        description='Results of the EQE measurement.',
    )

    measurement_conditions = SubSection(
        section_def=TransmissionDetails,
        description='Measurement details.',
    )

    environmental_conditions = SubSection(
        section_def=EnvironmentalConditions,
        description='Environmental conditions during the activity.',
    )

    sample_history = SubSection(
        section_def=EnvironmentalConditions,
        description="""A description of the conditions under which the sample have been stored between
        the finalization of the device and the described measurement.""",
    )

    certification_details = SubSection(
        section_def=CertificationDetails,
        description='Details about the certification of the measurement.',
    )

    raw_data = SubSection(
        section_def=TransmissionRawData,
        description='Raw data from the trnsmission measurement.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'Transmission'


class Flexibility(Measurement):
    """
    Flexibility measurement.
    """

    # Subsections
    results = SubSection(
        section_def=FlexibilityResults,
        description='Results of the flexibility measurement.',
    )

    measurement_conditions = SubSection(
        section_def=FlexibilityDetails,
        description='Measurement details.',
    )

    environmental_conditions = SubSection(
        section_def=EnvironmentalConditions,
        description='Environmental conditions during the activity.',
    )

    sample_history = SubSection(
        section_def=EnvironmentalConditions,
        description="""A description of the conditions under which the sample have been stored between
        the finalization of the device and the described measurement.""",
    )

    certification_details = SubSection(
        section_def=CertificationDetails,
        description='Details about the certification of the measurement.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'Flexibility'


### Master class putting everything together
class PerformedMeasurements(ArchiveSection):
    """
    Section for listing all measurements performed on this solar cell.
    """

    jv = SubSection(
        description='JV measurements performed on this device.',
        section_def=JV,
        repeats=True,
    )

    eqe = SubSection(
        description='EQE measurements performed on this device.',
        section_def=ExternalQuantumEfficiency,
        repeats=True,
    )

    stabilized_performance = SubSection(
        description='Performance measurements performed on this device.',
        section_def=StabilizedPerformance,
        repeats=True,
    )

    stability = SubSection(
        description='Stability measurements performed on this device.',
        section_def=Stability,
        repeats=True,
    )

    transmission = SubSection(
        description='Transmission measurements performed on this device.',
        section_def=Transmission,
        repeats=True,
    )

    flexibility = SubSection(
        description='Transmission measurements performed on this device.',
        section_def=Flexibility,
        repeats=True,
    )

    outdoor_performance = SubSection(
        description='Outdoor measurements.',
        section_def=OutdoorPerformance,
        repeats=True,
    )


m_package.__init_metainfo__()
