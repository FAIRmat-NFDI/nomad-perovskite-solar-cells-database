from nomad.datamodel.data import ArchiveSection
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.metainfo import MEnum, Quantity, Section, SubSection
from nomad.metainfo.metainfo import SchemaPackage

m_package = SchemaPackage()


class EncapsulationData(ArchiveSection):
    """
    Encapsulation specific data.
    """

    water_vapour_transmission_rate = Quantity(
        type=float,
        unit='g/m**2/hr',
        shape=[],
        description='The water vapour transmission rate',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='g/m**2/hr'
        ),
    )

    oxygen_vapour_transmission_rate = Quantity(
        type=float,
        unit='cm**3/m**2/hr',
        shape=[],
        description='The oxygen transmission rate',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='cm**3/m**2/hr'
        ),
    )
