from nomad.datamodel.data import ArchiveSection
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.metainfo import MEnum, Quantity, Section, SubSection
from nomad.metainfo.metainfo import SchemaPackage

m_package = SchemaPackage()


class KeyPerformanceMetrics(ArchiveSection):
    """
    A section collecting the key performance metrics of the device
    """

    # Stabilized data
    power_conversion_efficiency_stabilized = Quantity(
        description='Stabilized power conversion efficiency.',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    # From IV curve
    power_conversion_efficiency = Quantity(
        description='Power conversion efficiency.',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
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

    fill_factor = Quantity(
        description='Fill factor.',
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

    # Stability data
    pce_1000h_isos_l1_start = Quantity(
        description="""Power conversion efficiency start of the measurement under ISOS L1 conditions, 
        i.e. AM 1.5, Maximum powerpoint (or held at constant potential close to the Vmp), 
        room temperature, inert atmosphere.""",
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    pce_1000h_isos_l1_end = Quantity(
        description="""Power conversion efficiency after 1000 h under ISOS L1 conditions, 
        i.e. AM 1.5, Maximum powerpoint (or held at constant potential close to the Vmp), 
        room temperature, inert atmosphere.""",
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    pce_1000h_isos_l3_start = Quantity(
        description='Power conversion efficiency after the start of the measurement under ISOS L3 conditions, i.e. AM 1.5, Maximum powerpoint, 85°C and 50 % RH',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    pce_1000h_isos_l3_end = Quantity(
        description='Power conversion efficiency after 1000 h under ISOS L3 conditions, i.e. AM 1.5, Maximum powerpoint, 85°C and 50 % RH',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    t80_isos_l1 = Quantity(
        description="""Time to 80 percent of initial power conversion efficiency after 1000 h under ISOS L1 conditions.
                i.e. AM 1.5, Maximum powerpoint (or held at constant potential close to the Vmp), 
                room temperature, inert atmosphere""",
        type=float,
        unit='hr',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='hr'),
    )

    t80_isos_l3 = Quantity(
        description='Time to 80 percent of initial power conversion efficiency after 1000 h under ISOS L3 conditions, i.e. AM 1.5, Maximum powerpoint, 85°C and 50 % RH',
        type=float,
        unit='hr',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='hr'),
    )


m_package.__init_metainfo__()
