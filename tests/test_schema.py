import os.path
from nomad.client import parse, normalize_all
import perovskite
from nomad.metainfo import Quantity
def test_schema():
    test_file = os.path.join(os.path.dirname(__file__), 'data', 'example.archive.json')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

   
    assert entry_archive.data.substrate.stack_sequence == "SLG | ITO"
    assert entry_archive.data.perovskite.composition_inorganic == False
    # check more
    # assert entry_archive.data.cell.area_measured == 0.09
    # check m_def contains  section: nomad.datamodel.metainfo.eln.perovskite_solar_cell_database.PerovskiteSolarCell:Section