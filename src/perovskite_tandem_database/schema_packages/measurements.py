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

    simulator_class = Quantity(
        type=str,
        description='Class of the simulator.',
    )

    intensity = Quantity(
        type=float,
        description='Intensity of the illumination.',
        unit='W/m^2',
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


class TestConditions(ArchiveSection):
    """
    Conditions of the measurement.
    """

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


class Preconditioning(ArchiveSection):
    """
    Preconditioning conditions before the measurement.
    """

    protocol = Quantity(
        type=str,
        description='Protocol for the preconditioning.',
    )

    time = Quantity(
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
    )


class Scan(ExperimentStep):
    """
    Scan conditions of the measurement.
    """

    direction = Quantity(
        type=Enum('Forward', 'Reverse'),
        description='Direction of the scan.',
    )

    jsc = Quantity(
        type=float,
        description='Short-circuit current density.',
        unit='mA/cm^2',
    )

    Voc = Quantity(
        type=float,
        description='Open-circuit voltage.',
        unit='V',
    )

    FF = Quantity(
        type=float,
        description='Fill factor.',
        unit='dimensionless',
    )

    PCE = Quantity(
        type=float,
        description='Power conversion efficiency.',
        unit='dimensionless',
    )

    Vmp = Quantity(
        type=float,
        description='Voltage at maximum power.',
        unit='V',
    )

    jmp = Quantity(
        type=float,
        description='Current at maximum power.',
        unit='mA/cm^2',
    )

    Rs = Quantity(
        type=float,
        description='Series resistance.',
        unit='Ohm cm^2',
    )

    Rsh = Quantity(
        type=float,
        description='Shunt resistance.',
        unit='Ohm cm^2',
    )


class JV(Experiment):
    """
    JV measurement.
    """

    illumination = SubSection(
        section_def=Illumination,
        description='Illumination conditions of the measurement.',
    )

    test_conditions = SubSection(
        section_def=TestConditions,
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

    steps = SubSection(
        section_def=Scan,
        description='Results of a JV scan.',
    )
