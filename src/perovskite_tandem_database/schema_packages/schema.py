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

from .measurements import PerformedMeasurements
from .reference import Reference
from .tandem import (
    General,
    Layer,
)

m_package = SchemaPackage()


class PerovskiteTandemSolarCell(Schema):
    """
    This is schema for representing Perovskite Tandem Solar Cells.
    The descriptions in the quantities represent the instructions given to the user
    who manually curated the data.
    """

    m_def = Section(
        label='Perovskite Tandem Solar Cell',
        a_eln=dict(lane_width='400px'),
        categories=[UseCaseElnCategory],
    )

    # General information
    general = SubSection(
        section_def=General, description='General information about the device.'
    )

    # Reference
    reference = SubSection(
        section_def=Reference, description='The reference for the data in the entry.'
    )

    # Layer Stack as from tandem instructions v4.0
    layer_stack = SubSection(
        section_def=Layer,
        description='The stack of layers in the device starting from the bottom.',
        repeats=True,
    )

    # Measurements
    measurements = SubSection(
        section_def=PerformedMeasurements,
        description='The measurements performed on the device.',
    )


m_package.__init_metainfo__()
