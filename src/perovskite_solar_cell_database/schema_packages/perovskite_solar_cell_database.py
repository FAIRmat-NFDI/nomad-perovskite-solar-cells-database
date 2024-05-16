from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

from nomad.datamodel.data import UseCaseElnCategory
from nomad.config import config
from nomad.datamodel.data import Schema
from .schema_sections import (
    Ref,
    Cell,
    Module,
    Substrate,
    ETL,
    Perovskite,
    PerovskiteDeposition,
    HTL,
    Backcontact,
    Add,
    Encapsulation,
    JV,
    Stabilised,
    EQE,
    Stability,
    Outdoor,
)
from nomad.metainfo import Package, Section, SubSection, SchemaPackage

configuration = config.get_plugin_entry_point(
    'perovskite_solar_cell_database.schema_packages:perovskite_solar_cell_database'
)

m_package = SchemaPackage()


class PerovskiteSolarCell(Schema):
    """
    This schema is adapted to map the data in the [Perovskite Solar Cell Database
    Project](https://www.perovskitedatabase.com/). The descriptions in the quantities
    represent the instructions given to the user who manually curated the data.
    """

    m_def = Section(
        label='Perovskite Solar Cell',
        a_eln=dict(lane_width='400px'),
        categories=[UseCaseElnCategory],
    )

    ref = SubSection(section_def=Ref)
    cell = SubSection(section_def=Cell)
    module = SubSection(section_def=Module)
    substrate = SubSection(section_def=Substrate)
    etl = SubSection(section_def=ETL)
    perovskite = SubSection(section_def=Perovskite)
    perovskite_deposition = SubSection(section_def=PerovskiteDeposition)
    htl = SubSection(section_def=HTL)
    backcontact = SubSection(section_def=Backcontact)
    add = SubSection(section_def=Add)
    encapsulation = SubSection(section_def=Encapsulation)
    jv = SubSection(section_def=JV)
    stabilised = SubSection(section_def=Stabilised)
    eqe = SubSection(section_def=EQE)
    stability = SubSection(section_def=Stability)
    outdoor = SubSection(section_def=Outdoor)


m_package.__init_metainfo__()
