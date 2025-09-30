import os
import shutil

import pytest
from nomad.client import normalize_all, parse

from perovskite_solar_cell_database.llm_extraction_schema import (
    LLMExtractedPerovskiteSolarCell,
    llm_to_classic_schema,
)
from perovskite_solar_cell_database.schema_sections.cell import Cell
from perovskite_solar_cell_database.schema_sections.etl import ETL
from perovskite_solar_cell_database.schema_sections.htl import HTL
from perovskite_solar_cell_database.schema_sections.perovskite_deposition import (
    PerovskiteDeposition,
)


@pytest.mark.usefixtures('tmp_path')
def test_conversion(tmp_path):
    # Locate source test file in repo
    source_file = os.path.join(
        os.path.dirname(__file__), 'data', '10.1002--adfm.201904856-cell-1.archive.json'
    )

    tmp_file = tmp_path / 'archive.json'
    shutil.copy(source_file, tmp_file)

    entry_archive = parse(tmp_file)[0]
    normalize_all(entry_archive)

    llm_cell = entry_archive.data
    assert isinstance(llm_cell, LLMExtractedPerovskiteSolarCell)
    assert llm_cell.layers[1].name == 'TiO2-c'

    classic = llm_to_classic_schema(entry_archive.data)
    cell = classic.cell
    assert isinstance(cell, Cell)
    assert (
        cell.stack_sequence == 'FTO | TiO2-c | TiO2-mp | Perovskite | DTB(3%DEG) | Au'
    )

    etl = classic.etl
    assert isinstance(etl, ETL)
    assert etl.stack_sequence == 'TiO2-c | TiO2-mp'
    assert etl.deposition_procedure == 'Spin-coating | Spin-coating'
    assert etl.deposition_synthesis_atmosphere == 'Ambient air | Ambient air'
    assert etl.deposition_solvents == '1-butanol | ethanol'
    assert (
        etl.deposition_reaction_solutions_compounds
        == 'titanium diisopropoxide bis(acetylacetonate) | TiO2 paste'
    )
    assert etl.deposition_reaction_solutions_concentrations == '0.15 mol/L | 14.3 wt%'
    assert etl.deposition_thermal_annealing_temperature == '125 >> 450 | 500'
    assert etl.deposition_thermal_annealing_time == '300 >> 1800 | 1800'
    assert (
        etl.deposition_thermal_annealing_atmosphere
        == 'Ambient air >> Ambient air | Ambient air'
    )

    htl = classic.htl
    assert isinstance(htl, HTL)
    assert htl.deposition_reaction_solutions_temperature == '60'

    perovskite_deposition = classic.perovskite_deposition
    assert isinstance(perovskite_deposition, PerovskiteDeposition)
    assert perovskite_deposition.procedure == 'Spin-coating'
    assert perovskite_deposition.synthesis_atmosphere == 'Ambient air'
    assert perovskite_deposition.quenching_induced_crystallisation
    assert perovskite_deposition.quenching_media == 'Chlorobenzene'
    assert perovskite_deposition.thermal_annealing_temperature == '100'
    assert perovskite_deposition.thermal_annealing_time == '7200'
    assert perovskite_deposition.thermal_annealing_atmosphere == 'Ambient air'
    assert perovskite_deposition.solvents == 'DMF; DMSO'
    assert perovskite_deposition.solvents_mixing_ratios == '0.9; 0.1'
    assert (
        perovskite_deposition.reaction_solutions_compounds
        == 'FAI; PbI2; MABr; PbBr2; CsI'
    )
    assert (
        perovskite_deposition.reaction_solutions_concentrations
        == '172 mg/mL; 507 mg/mL; 22.4 mg/mL; 73.4 mg/mL; 1.5 mol/L'
    )
