import os.path

from nomad.client import normalize_all, parse


def test_schema():
    test_file = os.path.join(os.path.dirname(__file__), 'data', 'example.archive.json')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

    assert entry_archive.data.substrate.stack_sequence == 'SLG | ITO'
    assert entry_archive.data.perovskite.composition_inorganic is False
    assert entry_archive.metadata.entry_type == 'PerovskiteSolarCell'
    assert entry_archive.results.properties.optoelectronic.solar_cell.efficiency > -1
    assert len(entry_archive.data.jv.jv_curve[0].current_density) > -1
    assert len(entry_archive.results.material.chemical_formula_reduced) > 0
    assert entry_archive.results.properties.electronic.band_gap[0].value > 0
    # test for ion
    assert entry_archive.data.perovskite.composition_a_ions == 'MA'
    assert entry_archive.data.perovskite.composition_b_ions == 'Pb'
    assert entry_archive.data.perovskite.composition_c_ions == 'I'
    assert len(entry_archive.results.material.topology) == 4

    assert entry_archive.results.material.topology[0].label == 'absorber material'
    assert entry_archive.results.material.topology[0].structural_type == 'bulk'
    assert (
        entry_archive.results.material.topology[0].chemical_formula_iupac == 'PbCNH6I3'
    )
    assert (
        entry_archive.results.material.topology[0].chemical_formula_hill == 'CH6I3NPb'
    )
    assert len(entry_archive.results.material.topology[0].child_systems) == 3
    assert entry_archive.results.material.topology[1].label == 'A Cation: MA'
    assert (
        entry_archive.results.material.topology[1].structural_type
        == 'molecule / cluster'
    )
    assert entry_archive.results.material.topology[1].n_atoms == 8
    assert entry_archive.results.material.topology[1].chemical_formula_iupac == 'CNH6'

    assert entry_archive.results.material.topology[2].label == 'B Cation: Pb'
    assert entry_archive.results.material.topology[2].structural_type == 'atom'
    assert entry_archive.results.material.topology[2].n_atoms == 1
    assert entry_archive.results.material.topology[2].chemical_formula_iupac == 'Pb'

    assert entry_archive.results.material.topology[3].label == 'C Anion: I'
    assert entry_archive.results.material.topology[3].structural_type == 'atom'
    assert entry_archive.results.material.topology[3].n_atoms == 1
    assert entry_archive.results.material.topology[3].chemical_formula_iupac == 'I'
