import os.path
import shutil

import pytest
from nomad.client import normalize_all, parse

from perovskite_solar_cell_database.composition import (
    PerovskiteAIon,
    PerovskiteBIon,
    PerovskiteComposition,
    PerovskiteXIon,
)


@pytest.mark.usefixtures('tmp_path')
def test_composition(tmp_path):
    a_ion_file = os.path.join(
        os.path.dirname(__file__), 'data', 'MA_perovskite_ion.archive.json'
    )
    tmp_file = tmp_path / 'a_ion.archive.json'
    shutil.copy(a_ion_file, tmp_file)
    a_ion_archive = parse(tmp_file)[0]
    normalize_all(a_ion_archive)

    b_ion_file = os.path.join(
        os.path.dirname(__file__), 'data', 'Pb_perovskite_ion.archive.json'
    )
    tmp_file = tmp_path / 'b_ion.archive.json'
    shutil.copy(b_ion_file, tmp_file)
    b_ion_archive = parse(tmp_file)[0]
    normalize_all(b_ion_archive)

    x_ion_file_1 = os.path.join(
        os.path.dirname(__file__), 'data', 'I_perovskite_ion.archive.json'
    )
    tmp_file = tmp_path / 'x_ion.archive.json'
    shutil.copy(x_ion_file_1, tmp_file)
    x_ion_1_archive = parse(tmp_file)[0]
    normalize_all(x_ion_1_archive)

    x_ion_file_2 = os.path.join(
        os.path.dirname(__file__), 'data', 'Br_perovskite_ion.archive.json'
    )
    tmp_file = tmp_path / 'x_ion_2.archive.json'
    shutil.copy(x_ion_file_2, tmp_file)
    x_ion_2_archive = parse(tmp_file)[0]
    normalize_all(x_ion_2_archive)

    a_ion = a_ion_archive.data
    assert isinstance(a_ion, PerovskiteAIon)
    b_ion = b_ion_archive.data
    assert isinstance(b_ion, PerovskiteBIon)
    x_ion_1 = x_ion_1_archive.data
    assert isinstance(x_ion_1, PerovskiteXIon)
    x_ion_2 = x_ion_2_archive.data
    assert isinstance(x_ion_2, PerovskiteXIon)

    composition_file = os.path.join(
        os.path.dirname(__file__), 'data', 'composition.archive.yaml'
    )
    tmp_file = tmp_path / 'composition.archive.yaml'
    shutil.copy(composition_file, tmp_file)
    composition_archive = parse(tmp_file)[0]
    assert isinstance(composition_archive.data, PerovskiteComposition)
    composition_archive.data.ions_a_site[0].system = a_ion
    composition_archive.data.ions_b_site[0].system = b_ion
    composition_archive.data.ions_x_site[0].system = x_ion_1
    composition_archive.data.ions_x_site[1].system = x_ion_2
    normalize_all(composition_archive)

    # Check that short and long form are sorted correctly
    assert composition_archive.data.short_form == 'MAPbBrI'
    assert composition_archive.data.long_form == 'MAPbBr1.5I1.5'
