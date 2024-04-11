from nomad.datamodel.data import EntryData, UseCaseElnCategory

from perovskite_solar_cell_database.schema_sections import Ref
from nomad.metainfo import Package, Section, SubSection


m_package = Package(name='tandem_solar_cell_database')


class TandemSolarCell(EntryData):
    """
    This schema is designed to store data for tandem solar cells.
    """

    m_def = Section(
        label='Tandem Solar Cell',
        a_eln=dict(lane_width='400px'),
        categories=[UseCaseElnCategory],
    )

    reference = SubSection(section_def=Ref)


m_package.__init_metainfo__()
