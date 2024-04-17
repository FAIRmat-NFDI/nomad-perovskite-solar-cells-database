from nomad.datamodel.data import EntryData, UseCaseElnCategory
from nomad.metainfo import Package, Section, SubSection

from perovskite_solar_cell_database.schema_sections import Ref

from .schema_sections import Layer, Tandem

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
    tandem_device = SubSection(section_def=Tandem)
    layers = SubSection(section_def=Layer, repeats=True)


m_package.__init_metainfo__()
