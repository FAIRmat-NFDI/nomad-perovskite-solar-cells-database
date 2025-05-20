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
        description=""" The subcells that are part of this module. Enumerate the cells from 1 to n, where n is the number of subcells to
        in the module. Start counting from the bottom. For example, if the module is made of subcells 1 and 2, then the value should be 1,2.
        If the module is made of subcells 2 and 3, then the value should be 2,3.
        For a monolithic module, the values should be 1, .., n, where n is the number of subcells in the device.
            """,
        type=MEnum(['1', '2', '3', '4', '1, 2', '2, 3', '3, 4', '1, 2, 3', '2, 3, 4', '1, 2, 3, 4']),
        a_eln=ELNAnnotation(component='EnumEditQuantity'),
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