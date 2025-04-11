from nomad.datamodel.data import ArchiveSection, EntryData
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.metainfo import Quantity, Section, SubSection
from nomad.metainfo.data_type import MEnum


class SubCell(ArchiveSection):
    """
    A section describing a sub cell in a tandem solar cell.
    """

    area = Quantity(
        type=float,
        unit='cm^2',
        a_eln=ELNAnnotation(defaultDisplayUnit='cm^2'),
        description='The area of the sub cell',
    )

    module = Quantity(
        type=bool,
        description="""
        TRUE if a sub cell is in the form of a module, FALSE if it is a single cell
        It is for example possible to have a silicon bottom cell and a perovskite module as a top cell. In that case this would be marked as FALSE | TRUE
        """,
    )

    commercial_unit = Quantity(
        type=bool,
        description='TRUE if the sub cell was bought commercially, FALSE if it is a lab-made unit',
    )

    supplier = Quantity(
        type=str,
        description='Origin of the subcell. This will most often be a company or the lab of a research group',
    )


class General(ArchiveSection):
    """
    This section stores general configuration information about a tandem solar cell.
    """

    architecture = Quantity(
        type=MEnum(['Stacked', 'Monolithic', 'Other']),
        default='Other',
        description='The general architecture of the tandem device. For 4-terminal devices and other configurations where there are two independent sub cells simply stacked on top of each other, define this as “stacked”',
    )

    number_of_terminals = Quantity(
        type=int,
        description='The number of terminals in the device. The most common configurations are 2 and 4',
    )

    number_of_junctions = Quantity(
        type=int,
        description='The number of junctions in the device.',
    )

    number_of_cells = Quantity(
        type=int,
        default=0,
        description='The number of individual solar cells, or pixels, on the substrate on which the reported cell is made',
    )

    photoabsorber = Quantity(
        type=MEnum(['Silicon', 'Perovskite', 'CIGS', 'OPV', 'OSC', 'DSSC', 'BHJ']),
        description="""
            List of the photoabsorbers starting from the bottom of the device stack.
                    """,
        shape=['*'],
    )

    photoabsorber_bandgaps = Quantity(
        type=float,
        # unit = 'eV', # arrays with units not yet supported
        description="""
            List of the band gap values of the respective photo absorbers.
            - The layers must line up with the previous filed.
            - State band gaps in eV
            - If there are uncertainties, state the best estimate, e.g write 1.5 and not 1.45-1.55
            - Every photo absorber has a band gap. If it is unknown, state this as ‘nan’
        """,
        shape=['*'],
    )

    stack_sequence = Quantity(
        type=str,
        shape=['*'],
        description="""
        The stack sequence describing the cell.
        - If two materials, e.g. A and B, are mixed in one layer, list the materials in alphabetic order and separate them with semicolons, as in (A; B)
        - The perovskite layer is stated as “Perovskite”, regardless of composition, mixtures, dimensionality etc. There are plenty of other fields specifically targeting the perovskite.
        - If a material is doped, or have an additive, state the pure material here and specify the doping in the columns specifically targeting the doping of those layers.
        - There is no sharp well-defined boundary between a when a material is best considered as doped to when it is best considered as a mixture of two materials. When in doubt if your material is doped or a mixture, use the notation that best capture the metaphysical essence of the situation
        - Use common abbreviations when possible but spell it out when there is risk for confusion. For consistency, please pay attention to the abbreviation specified under the headline Abbreviations found tandem instructions v4.0 document.
                    """,
    )

    area = Quantity(
        type=float,
        unit='cm^2',
        a_eln=ELNAnnotation(defaultDisplayUnit='cm^2'),
        description='The total area of the device.',
    )

    area_measured = Quantity(
        type=float,
        unit='cm^2',
        a_eln=ELNAnnotation(defaultDisplayUnit='cm^2'),
        description="""The effective area of the cell during IV and stability measurements under illumination. If measured with a mask, this corresponds to the area of the hole in the mask. Otherwise this area is the same as the total cell area.""",
    )

    flexibility = Quantity(
        type=bool,
        default=False,
        description='TRUE if the device is flexible and bendable, FALSE if it is rigid.',
    )

    semitransparent = Quantity(
        type=bool,
        default=False,
        description="""
        TRUE if the device is semitransparent which usually is the case when there are no thick completely covering metal electrodes.
        FALSE if it is opaque.""",
    )

    contains_textured_layers = Quantity(
        type=bool,
        default=False,
        description='TRUE if the device contains textured layers with the purpose of light management.',
    )

    contains_antireflectie_coating = Quantity(
        type=bool,
        default=False,
        description='TRUE if the device contains one or more anti reflective coatings.',
    )

    subcells = SubSection(
        section_def=SubCell,
        description='The sub cells in the device',
        repeats=True,
    )
