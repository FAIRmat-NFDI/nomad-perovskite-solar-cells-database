import os.path

from nomad.client import normalize_all, parse
from nomad.metainfo import Quantity
from pint import UnitRegistry

# from perovskite_tandem_database.schema_packages.tandem import Ion

ureg = UnitRegistry()


def test_schema():
    test_file = os.path.join(os.path.dirname(__file__), 'data', 'test_tandem_schema.archive.json')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

    # test reference
    assert entry_archive.data.reference.DOI_number == '10.1002/advs.201700675'
    assert entry_archive.data.reference.data_entered_by_author is False

    # test general
    assert entry_archive.data.general.architecture == 'Stacked'
    assert entry_archive.data.general.number_of_terminals == 4
    assert entry_archive.data.general.number_of_junctions == 2
    assert entry_archive.data.general.number_of_cells == 1
    assert entry_archive.data.general.photoabsorber == ['CIGS', 'Perovskite']
    assert entry_archive.data.general.photoabsorber_bandgaps == [1.18, 1.62]
    assert entry_archive.data.general.area_measured == ureg.Quantity(
        0.213, 'centimeter ** 2'
    )

    # test layer stack
    assert len(entry_archive.data.layer_stack) == 18
    assert entry_archive.data.layer_stack[0].name == 'SLG'
    assert entry_archive.data.layer_stack[0].functionality == 'Substrate'
    assert entry_archive.data.layer_stack[0].origin == 'Commercial'

    assert entry_archive.data.layer_stack[1].name == 'Mo'
    assert entry_archive.data.layer_stack[1].functionality == 'Back contact'
    assert entry_archive.data.layer_stack[1].thickness == ureg.Quantity(
        700, 'nanometer'
    )
    assert entry_archive.data.layer_stack[1].origin == 'Lab made'
    assert (
        entry_archive.data.layer_stack[1].synthesis.steps[0].procedure == 'Sputtering'
    )

    assert entry_archive.data.layer_stack[2].name == 'CIGS'
    assert entry_archive.data.layer_stack[2].thickness == ureg.Quantity(3, 'micrometer')
    assert (
        entry_archive.data.layer_stack[2].synthesis.steps[0].procedure
        == 'Co-evaporation'
    )
    assert entry_archive.data.layer_stack[2].composition[0].name == 'Cu'
    assert entry_archive.data.layer_stack[2].composition[0].coefficient == 1
    # assert entry_archive.data.layer_stack[2].composition == [Ion('Cu', 1), Ion('In', 0.59), Ion('Ga', 0.41), Ion('Se', 2.0)]
