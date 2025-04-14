from nomad.datamodel.data import ArchiveSection
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.metainfo import MEnum, Quantity, Section, SubSection


class SubCell(ArchiveSection):
    """
    A section describing a sub cell in a tandem solar cell.
    """

    area = Quantity(
        description='The area of the sub cell',
        type=float,
        unit='cm^2',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='cm^2'),
    )

    module = Quantity(
        type=bool,
        description="""
        TRUE if a sub cell is in the form of a module, FALSE if it is a single cell
        It is for example possible to have a silicon bottom cell and a perovskite module as a top cell. In that case this would be marked as FALSE | TRUE
        """,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    commercial_unit = Quantity(
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

    architecture = Quantity(
        description='The general architecture of the tandem device. For 4-terminal devices and other configurations where there are two independent sub cells simply stacked on top of each other, define this as “stacked”',
        type=MEnum(['Stacked', 'Monolithic', 'Other']),
        default='Other',
        a_eln=ELNAnnotation(component='EnumEditQuantity'),
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

    number_of_cells = Quantity(
        description='The number of individual solar cells, or pixels, on the substrate on which the reported cell is made',
        type=int,
        default=0,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    photoabsorber = Quantity(
        description='List of the photoabsorbers starting from the bottom of the device stack.',
        type=MEnum(['Silicon', 'Perovskite', 'CIGS', 'OPV', 'OSC', 'DSSC', 'BHJ']),
        shape=['*'],
        a_eln=ELNAnnotation(component='EnumEditQuantity'),
    )

    photoabsorber_bandgaps = Quantity(
        description="""
            List of the band gap values of the respective photo absorbers.
            - The layers must line up with the previous filed.
            - State band gaps in eV
            - If there are uncertainties, state the best estimate, e.g write 1.5 and not 1.45-1.55
            - Every photo absorber has a band gap. If it is unknown, state this as ‘nan’
        """,
        type=float,
        # unit = 'eV', # arrays with units not yet supported
        shape=['*'],
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    stack_sequence = Quantity(
        description="""
        The stack sequence describing the cell.
        - If two materials, e.g. A and B, are mixed in one layer, list the materials in alphabetic order and separate them with semicolons, as in (A; B)
        - The perovskite layer is stated as “Perovskite”, regardless of composition, mixtures, dimensionality etc. There are plenty of other fields specifically targeting the perovskite.
        - If a material is doped, or have an additive, state the pure material here and specify the doping in the columns specifically targeting the doping of those layers.
        - There is no sharp well-defined boundary between a when a material is best considered as doped to when it is best considered as a mixture of two materials. When in doubt if your material is doped or a mixture, use the notation that best capture the metaphysical essence of the situation
        - Use common abbreviations when possible but spell it out when there is risk for confusion. For consistency, please pay attention to the abbreviation specified under the headline Abbreviations found tandem instructions v4.0 document.
                    """,
        type=str,
        shape=['*'],
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    area = Quantity(
        description='The total area of the device.',
        type=float,
        unit='cm^2',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='cm^2'),
    )

    area_measured = Quantity(
        description="""The effective area of the cell during IV and stability measurements under illumination. If measured with a mask, this corresponds to the area of the hole in the mask. Otherwise this area is the same as the total cell area.""",
        type=float,
        unit='cm^2',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='cm^2'),
    )

    flexibility = Quantity(
        description='TRUE if the device is flexible and bendable, FALSE if it is rigid.',
        type=bool,
        default=False,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    semitransparent = Quantity(
        description="""
        TRUE if the device is semitransparent which usually is the case when there are no thick completely covering metal electrodes.
        FALSE if it is opaque.""",
        type=bool,
        default=False,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    contains_textured_layers = Quantity(
        description='TRUE if the device contains textured layers with the purpose of light management.',
        type=bool,
        default=False,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    contains_antireflective_coating = Quantity(
        description='TRUE if the device contains one or more anti reflective coatings.',
        type=bool,
        default=False,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    subcells = SubSection(
        description='The sub cells in the device',
        section_def=SubCell,
        repeats=True,
    )
