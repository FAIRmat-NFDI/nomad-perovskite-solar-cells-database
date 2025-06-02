from nomad.datamodel.data import ArchiveSection
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.metainfo import MEnum, Quantity, Section, SubSection
from nomad.metainfo.metainfo import SchemaPackage

m_package = SchemaPackage()


class Module(ArchiveSection):
    """
    This sections defines module relevant data
    """

    subcell_association = Quantity(
        description=""" The subcells that are part of this module. 0 menas that the module is monolithic.
        If not all the subcells are in the form of a module, e.g. a perovksite module could be on top of 
        a silicon cell in a 4-terminal configuration, enumerate the cells (from 1 to n) that are in the module. 
        A perovksite module on a cilicon cell would be 2.
        A perovksite tandem module on a cilidon cell in a 3 junction 4 terminal device woudl be [2, 3]  

            """,
        type=int,
        shape=['*'],
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    number_of_cells = Quantity(
        description='The number of cells in the module',
        type=int,
        default=0,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    total_area = Quantity(
        description='The total area of the module.',
        type=float,
        unit='cm^2',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='cm^2'),
    )

    active_area = Quantity(
        description='The active area of the module.',
        type=float,
        unit='cm^2',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='cm^2'),
    )

    cell_area = Quantity(
        description='The total area of each individual cell.',
        type=float,
        unit='cm^2',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='cm^2'),
    )

    scribe_width = Quantity(
        description='The width of the scribe lines separating the cells.',
        type=float,
        unit='mm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mm'),
    )


class ModuleData(ArchiveSection):
    """
    This section stores module specific data.
    """

    # Boolean quantities
    monolithic_module = Quantity(
        description='TRUE if the device is a monolithic module.',
        type=bool,
        default=False,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    contains_monolithic_subcell = Quantity(
        description='TRUE if one or more of the subcells are modules.',
        type=bool,
        default=False,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    # Subsections
    subcells = SubSection(
        description="""Describe each module in the stack.""",
        section_def=Module,
        repeats=True,
    )


m_package.__init_metainfo__()
