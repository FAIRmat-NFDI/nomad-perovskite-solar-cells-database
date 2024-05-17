import numpy as np
from nomad.datamodel.data import ArchiveSection
from nomad.datamodel.results import Properties
from nomad.metainfo import Quantity

from perovskite_solar_cell_database.schema_sections.utils import add_solar_cell

from .vars import cell_enum_edit_quantity_suggestions


class Cell(ArchiveSection):
    """
    General information about the solar cell. It includes information about the device area,
    the layer stack sequence and the device architecture.
    """

    stack_sequence = Quantity(
        type=str,
        shape=[],
        description="""
    The stack sequence describing the cell. Use the following formatting guidelines
- Start with the substrate to the left and list the materials in each layer of the device
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- If two materials, e.g. A and B, are mixed in one layer, list the materials in alphabetic order and separate them with  semicolons, as in (A; B)
- The perovskite layer is stated as “Perovskite”, regardless of composition, mixtures, dimensionality etc. There are plenty of other fields specifically targeting the perovskite.
- If a material is doped, or have an additive, state the pure material here and specify the doping in the columns specifically targeting the doping of those layers.
- There is no sharp well-defined boundary between a when a material is best considered as doped to when it is best considered as a mixture of two materials. When in doubt if your material is doped or a mixture, use the notation that best capture the metaphysical essence of the situation
- Use common abbreviations when possible but spell it out when there is risk for confusion. For consistency, please pay attention to the abbreviation specified under the headline Abbreviations found earlier in this document.
- There are several thousand stack sequences described in the literature. Try to find your one in the list of alternatives in the data template. If it is not there (i.e. you may have done something new) define a new stack sequence according to the instructions.
ExampleBelow are the 16 most common device stacks which represent close to half of all reported devices.
SLG | FTO | TiO2-c | TiO2-mp | Perovskite | Spiro-MeOTAD | Au
SLG | FTO | TiO2-c | Perovskite | Spiro-MeOTAD | Au
SLG | FTO | TiO2-c | TiO2-mp | Perovskite | Spiro-MeOTAD | Ag
SLG | FTO | TiO2-c | Perovskite | Spiro-MeOTAD | Ag
SLG | ITO | PEDOT:PSS | Perovskite | PCBM-60 | Al
SLG | ITO | PEDOT:PSS | Perovskite | PCBM-60 | BCP | Ag
SLG | ITO | PEDOT:PSS | Perovskite | PCBM-60 | Ag
SLG | FTO | TiO2-c | TiO2-mp | Perovskite | Carbon
SLG | FTO | TiO2-c | TiO2-mp | ZrO2-mp | Perovskite | Carbon
SLG | FTO | SnO2-c | Perovskite | Spiro-MeOTAD | Au
SLG | ITO | SnO2-np | Perovskite | Spiro-MeOTAD | Au
SLG | ITO | PEDOT:PSS | Perovskite | C60 | BCP | Ag
SLG | ITO | TiO2-c | Perovskite | Spiro-MeOTAD | Au
SLG | FTO | TiO2-c | TiO2-mp | Perovskite | PTAA | Au
SLG | FTO | SnO2-np | Perovskite | Spiro-MeOTAD | Au
SLG | ITO | NiO-c | Perovskite | PCBM-60 | BCP | Ag
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=sorted(cell_enum_edit_quantity_suggestions)),
        ),
    )
    area_total = Quantity(
        type=np.dtype(np.float64),
        unit=('cm**2'),
        shape=[],
        description="""
    The total cell area in cm2. The total area is defined as the area that would provide photovoltaic performance when illuminated without any shading, i.e. in practice the geometric overlap between the top and bottom contact.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    area_measured = Quantity(
        type=np.dtype(np.float64),
        unit=('cm**2'),
        shape=[],
        description="""
    The effective area of the cell during IV and stability measurements under illumination. If measured with a mask, this corresponds to the area of the hole in the mask. Otherwise this area is the same as the total cell area.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    number_of_cells_per_substrate = Quantity(
        type=np.dtype(np.int64),
        shape=[],
        description="""
    The number of individual solar cells, or pixels, on the substrate on which the reported cell is made
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    architecture = Quantity(
        type=str,
        shape=[],
        description="""
    The cell architecture with respect to the direction of current flow and the order in which layers are deposited. The two most common are nip (also referred to as normal) and pin (also referred to as inverted) but there are also a few others, e.g. Back contacted
- nip architecture means that the electrons are collected at the substrate side. The typical example is when a TiO2 electron selective contact is deposited between the perovskite and the substrate (e.g. SLG | FTO | TiO2-c |Perovskite | …)
- pin architecture means that it instead is the holes that are collected at the substrate side. The typical example is when a PEDOT:PSS hole selective contact is deposited between the perovskite and the substrate (e.g. SLG | FTO | PEDOT:PSS |Perovskite | …)
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'Unknown',
                    'Pn-Heterojunction',
                    'Front contacted',
                    'Back contacted',
                    'pin',
                    'nip',
                    'Schottky',
                ]
            ),
        ),
    )

    flexible = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if the cell flexible and bendable.
                    """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    flexible_min_bending_radius = Quantity(
        type=np.dtype(np.float64),
        unit=('cm'),
        shape=[],
        description="""
    The maximum bending radius possible without degrading the cells performance
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    semitransparent = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if the cell is semi-transparent, which usually is the case when there are no thick completely covering metal electrodes.
                    """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    semitransparent_AVT = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description="""
    The average visible transmittance in the wavelength range stated in the next field
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    semitransparent_wavelength_range = Quantity(
        type=str,
        shape=[],
        description="""
    the wavelength range under which the average visible transmittance is determined
Example:
400; 720
350; 770
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=['nan; nan', '800; 1200']),
        ),
    )

    semitransparent_raw_data = Quantity(
        type=str,
        shape=[],
        description="""
    A link to where the data file for the measurement is stored
- This is a beta feature. The plan is to create a file repository where the raw files for stability data can be stored and disseminated. With the link and associated protocols, it should be possible to programmatically access and analyse the raw data.
                    """,
    )

    def normalize(self, archive, logger):
        add_solar_cell(archive)
        if not archive.results.properties:
            archive.results.properties = Properties()
        if self.stack_sequence:
            archive.results.properties.optoelectronic.solar_cell.device_stack = (
                self.stack_sequence.split(' | ')
            )
        if self.architecture:
            archive.results.properties.optoelectronic.solar_cell.device_architecture = (
                self.architecture
            )
        if self.area_total or self.area_measured:
            if self.area_measured and not self.area_total:
                archive.results.properties.optoelectronic.solar_cell.device_area = (
                    self.area_measured
                )
            else:
                archive.results.properties.optoelectronic.solar_cell.device_area = (
                    self.area_total
                )
