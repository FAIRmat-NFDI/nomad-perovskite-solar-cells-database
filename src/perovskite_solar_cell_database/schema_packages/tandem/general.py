from nomad.datamodel.data import ArchiveSection
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.metainfo import Datetime, MEnum, Quantity, Section, SubSection
from nomad.metainfo.metainfo import SchemaPackage

m_package = SchemaPackage()


class SubCellOrigin(ArchiveSection):
    """
    A section describing a sub cell in a tandem solar cell.
    """

    commercial = Quantity(
        description='TRUE if the sub cell was bought commercially, FALSE if it is a lab-made unit',
        type=bool,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    supplier = Quantity(
        description='Origin of the subcell. This will most often be a company or the lab of a research group',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )


class General(ArchiveSection):
    """
    This section stores general configuration information about a tandem solar cell.
    """

    # Top level data
    architecture = Quantity(
        description='The general architecture of the tandem device. For 4-terminal devices and other configurations where there are two independent sub cells simply stacked on top of each other, define this as “stacked”',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'Stacked',
                    'Monolithic',
                    'Laminated',
                    'Spectral splitter',
                    'Wide bandgap cell used as reflector',
                    'Other',
                ],
            ),
        ),
    )

    number_of_terminals = Quantity(
        description='The number of terminals in the device. The most common configurations are 2 and 4',
        type=int,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    number_of_junctions = Quantity(
        description='The number of junctions in the device.',
        type=int,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    photoabsorbers = Quantity(
        description='List of the photoabsorbers starting from the bottom of the device stack.',
        type=str,
        shape=['*'],
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'Silicon',
                    'Perovskite',
                    'CIGS',
                    'CZTS',
                    'CIS',
                    'GaAs',
                    'OPV',
                    'OSC',
                    'DSSC',
                    'Quantum dot',
                ]
            ),
        ),
    )

    photoabsorbers_bandgaps = Quantity(
        description="""
            List of the band gap values of the respective photo absorbers.
            - The layers must line up with the previous filed.
            - State band gaps in eV
            - If there are uncertainties, state the best estimate, e.g write 1.5 and not 1.45-1.55
            - Every photo absorber has a band gap. If it is unknown, state this as 0
        """,
        type=float,
        # unit = 'eV', # arrays with units not yet supported
        shape=['*'],
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    production_date = Quantity(
        description='Date the device was finalized.',
        type=Datetime,
        a_eln=ELNAnnotation(component='DateTimeEditQuantity'),
    )

    # Boolean quantities
    flexible = Quantity(
        description='TRUE if the device is flexible and bendable, FALSE if it is rigid.',
        type=bool,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    semitransparent = Quantity(
        description="""
        TRUE if the device is semitransparent. That is usually only the case when there are no thick completely covering metal electrodes.
        FALSE if it is opaque.""",
        type=bool,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    contains_textured_layers = Quantity(
        description='TRUE if the device contains textured layers with the purpose of light management.',
        type=bool,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    bifacial = Quantity(
        description='True if the cell is bifacial, i.e. design to absorb light from both sides.',
        type=bool,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    encapsulated = Quantity(
        description='True if the cell is encapsulated.',
        type=bool,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    module = Quantity(
        description='TRUE if device is a module composed of several identical cells located side by side, either in series or in parallel.',
        type=bool,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    contains_antireflective_coating = Quantity(
        description='TRUE if the device contains one or more anti reflective coatings or other layers specifically dealing with light management.',
        type=bool,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    # Physical footprint
    substrate_area = Quantity(
        description='The total area of the substrate on which the device is deposited.',
        type=float,
        unit='cm^2',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='cm^2'),
    )

    cell_area = Quantity(
        description='The total area of the cell. The dark area. Is typically defined as the overlap between the front and back contacts.',
        type=float,
        unit='cm^2',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='cm^2'),
    )

    active_area = Quantity(
        description='The effective area of the cell during IV and stability measurements under illumination. If measured with a mask, this corresponds to the area of the hole in the mask. Otherwise this area is the same as the cell area.',
        type=float,
        unit='cm^2',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='cm^2'),
    )

    number_of_cells = Quantity(
        description='The number of individual solar cells, or pixels, on the substrate on which the reported cell is made',
        type=int,
        default=0,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    # Derived quantities
    photoabsorbers_string = Quantity(
        description="""A single string describing the combination of photoabsorbers in the cell. 
            Can be generated automatically from the photoabsorbers field.
            Example: "silicon-perovskite", "CIGS-Perovskite", "silicon-Perovskite-perovskite", etc.
            """,
        type=str,
    )

    stack_sequence = Quantity(
        description="""A list of the materials in the layers of the stack. <br/>  
        If a proper device stack section is provided, the stack sequence can be generated from that one.

        * Start with the layer in the bottom of the device (i.e. that is furthest from the sun) and work up from that.
        * If two materials, e.g. A and B, are mixed in one layer, list the materials in alphabetic order and separate them with semicolons, as in (A; B)
        * The perovskite layer is stated as “Perovskite”, regardless of composition, mixtures, dimensionality etc. Those details are provided elsewhere. 
        * Use common abbreviations when possible but spell them out when there is risk for confusion. 
            """,
        type=str,
    )

    number_of_layers = Quantity(
        description='Number of layers in the stack.',
        type=int,
        shape=[],
    )

    # Subsections
    subcells = SubSection(
        description="""A list of the origin of each subcell, i.e. if it is lab made or commercially bought. <br/>
            The list should start with the bottom cell (i.e. the cell furthers from the sun) and work upwards. <br/> 
            For a monolithic device, there is no hard boundary between the top and the bottom cell, but it is usually quite clear if one part was bought commercially. <br/> 
            Each entry (subcell) in the list comes with the following key-value pairs.
            """,
        section_def=SubCellOrigin,
        repeats=True,
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)

        # Generate the photoabsorber string
        if self.photoabsorbers and len(self.photoabsorbers) > 0:
            self.photoabsorbers_string = '-'.join(self.photoabsorbers)


m_package.__init_metainfo__()
