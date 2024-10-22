from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    pass

from nomad.datamodel.data import Schema, UseCaseElnCategory
from nomad.metainfo import SchemaPackage, Section, SubSection

from perovskite_solar_cell_database.schema_sections import (
    EQE,
    ETL,
    HTL,
    JV,
    Add,
    Backcontact,
    Cell,
    Encapsulation,
    Module,
    Outdoor,
    Perovskite,
    PerovskiteDeposition,
    Ref,
    Stabilised,
    Stability,
    Substrate,
)

from .ref import Reference
from .tandem import (
    General,
    Layer,
)

m_package = SchemaPackage()


class PerovskiteTandemSolarCell(Schema):
    """
    This schema is adapted to map the data in the [Perovskite Solar Cell Database
    Project](https://www.perovskitedatabase.com/). The descriptions in the quantities
    represent the instructions given to the user who manually curated the data.
    """

    m_def = Section(
        label='Perovskite Tandem Solar Cell',
        a_eln=dict(lane_width='400px'),
        categories=[UseCaseElnCategory],
    )

    # General information
    general = SubSection(section_def=General, description='')

    # Reference
    reference = SubSection(
        section_def=Reference, description='The reference for the data in the entry.'
    )

    # Layer Stack as from tandem instructions v4.0
    layer_stack = SubSection(
        section_def=Layer,
        description='The stack of layers in the device starting from the bottom.',
        repeating=True,
    )

    # cell = SubSection(section_def=Cell)
    # module = SubSection(section_def=Module)
    # substrate = SubSection(section_def=Substrate)
    # backcontact = SubSection(section_def=Backcontact)
    # absorber_bottom = SubSection(section_def=Perovskite) # TODO: Change to CIGS related section
    # absorber_bottom_deposition = SubSection(section_def=PerovskiteDeposition) # TODO: Change to CIGS related section
    # buffer = SubSection(section_def=ETL) # TODO: Change to buffer related section
    # frontcontact_bottom = SubSection(section_def=Backcontact) # TODO: Change to front contact related section
    # htl = SubSection(section_def=HTL)
    # absorber_top = SubSection(section_def=Perovskite)
    # absorber_top_deposition = SubSection(section_def=PerovskiteDeposition)
    # etl = SubSection(section_def=ETL)
    # frontcontact = SubSection(section_def=Backcontact) # TODO: Change to front contact related section
    # add = SubSection(section_def=Add)

    # # Miscellaneous
    # encapsulation = SubSection(section_def=Encapsulation)
    # jv = SubSection(section_def=JV)
    # stabilised = SubSection(section_def=Stabilised)
    # eqe = SubSection(section_def=EQE)
    # stability = SubSection(section_def=Stability)
    # outdoor = SubSection(section_def=Outdoor)


m_package.__init_metainfo__()
