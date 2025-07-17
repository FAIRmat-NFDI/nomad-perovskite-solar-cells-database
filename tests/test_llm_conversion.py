import os.path

from nomad.client import normalize_all, parse

from perovskite_solar_cell_database.llm_extraction_schema import llm_to_classic_schema


def test_conversion():
    test_file = os.path.join(
        os.path.dirname(__file__), 'data', '10.1002--adfm.201904856-cell-1.archive.json'
    )
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

    classic = llm_to_classic_schema(entry_archive.data)

    assert (
        classic.cell.stack_sequence
        == 'FTO | c-TiO2 | m-TiO2 | Perovskite | DTB(3%DEG) | Au'
    )
