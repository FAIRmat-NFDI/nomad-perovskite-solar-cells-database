import os
import shutil

import pytest
from nomad.client import normalize_all, parse

from perovskite_solar_cell_database.llm_extraction_schema import llm_to_classic_schema


@pytest.mark.usefixtures("tmp_path")
def test_conversion(tmp_path):
    # Locate source test file in repo
    source_file = os.path.join(
        os.path.dirname(__file__),
        "data",
        "10.1002--adfm.201904856-cell-1.archive.json"
    )

    tmp_file = tmp_path / "archive.json"
    shutil.copy(source_file, tmp_file)

    entry_archive = parse(tmp_file)[0]
    normalize_all(entry_archive)

    classic = llm_to_classic_schema(entry_archive.data)

    assert (
        classic.cell.stack_sequence
        == 'FTO | c-TiO2 | m-TiO2 | Perovskite | DTB(3%DEG) | Au'
    )
