import os.path
from nomad.client import parse, normalize_all

def test_schema():
    test_file = os.path.join(os.path.dirname(__file__), 'data', 'example.archive.json')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

   
    assert entry_archive.data.substrate.stack_sequence == "SLG | ITO"
    assert entry_archive.data.perovskite.composition_inorganic == False
    assert entry_archive.metadata.entry_type == 'PerovskiteSolarCell'
    assert entry_archive.results.properties.optoelectronic.solar_cell.efficiency > -1
    assert len(entry_archive.data.jv.jv_curve[0].current_density) > -1
    assert len(entry_archive.results.material.chemical_formula_reduced) > 0
    assert entry_archive.results.properties.electronic.band_gap[0].value > 0 
