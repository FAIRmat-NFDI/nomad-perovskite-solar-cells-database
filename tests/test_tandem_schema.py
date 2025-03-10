import os.path

from nomad.client import normalize_all, parse
from nomad.metainfo import Quantity
from pint import UnitRegistry

# from perovskite_tandem_database.schema_packages.tandem import Ion

ureg = UnitRegistry()


def test_schema():
    test_file = os.path.join(
        os.path.dirname(__file__), 'data', 'test_tandem_schema.archive.json'
    )
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

    # test reference
    assert (
        entry_archive.data.reference.DOI_number
        == 'https://doi.org/10.1002/advs.201700675'
    )
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
    assert entry_archive.data.layer_stack[0].synthesis.origin == 'Commercial'

    assert entry_archive.data.layer_stack[1].name == 'Mo'
    assert entry_archive.data.layer_stack[1].functionality == 'Back contact'
    assert entry_archive.data.layer_stack[1].properties.thickness == ureg.Quantity(
        700, 'nanometer'
    )
    assert entry_archive.data.layer_stack[1].synthesis.origin == 'Lab made'
    assert entry_archive.data.layer_stack[1].synthesis.steps[0].name == 'Sputtering'

    # CIGS layer
    assert entry_archive.data.layer_stack[2].name == 'CIGS'
    assert entry_archive.data.layer_stack[2].properties.thickness == ureg.Quantity(
        3, 'micrometer'
    )
    assert entry_archive.data.layer_stack[2].properties.bandgap == ureg.Quantity(
        1.18, 'electron_volt'
    )
    assert entry_archive.data.layer_stack[2].synthesis.steps[0].name == 'Co-evaporation'
    assert entry_archive.data.layer_stack[2].composition[0].name == 'Cu'
    assert entry_archive.data.layer_stack[2].composition[0].coefficient == 1

    # Perovskite layer
    assert entry_archive.data.layer_stack[12].name == 'Perovskite'
    assert entry_archive.data.layer_stack[12].properties.bandgap == ureg.Quantity(
        1.62, 'electron_volt'
    )
    assert entry_archive.data.layer_stack[12].properties.thickness == ureg.Quantity(
        520, 'nanometer'
    )
    assert entry_archive.data.layer_stack[12].synthesis.steps[0].name == 'Evaporation'
    assert entry_archive.data.layer_stack[12].synthesis.steps[0].atmosphere == 'Vacuum'
    assert (
        entry_archive.data.layer_stack[12].synthesis.steps[0].reactants[0].name
        == 'PbI2'
    )
    assert entry_archive.data.layer_stack[12].synthesis.steps[1].name == 'Spin-coating'
    assert entry_archive.data.layer_stack[12].synthesis.steps[1].atmosphere == 'N2'
    assert (
        entry_archive.data.layer_stack[12].synthesis.steps[1].reactants[0].name == 'MAI'
    )
    assert (
        entry_archive.data.layer_stack[12].synthesis.steps[1].solvent[0].name == 'IPA'
    )
    assert (
        entry_archive.data.layer_stack[12].synthesis.steps[2].name
        == 'Thermal Annealing'
    )
    assert entry_archive.data.layer_stack[12].synthesis.steps[2].atmosphere == 'Unknown'
    assert entry_archive.data.layer_stack[12].synthesis.steps[
        2
    ].duration == ureg.Quantity(10, 'minute')
    assert entry_archive.data.layer_stack[12].synthesis.steps[
        2
    ].temperature == ureg.Quantity(100, 'celsius')

    ## test measurements

    # jv
    assert entry_archive.data.measurements.jv_bottom_cell.method == 'JV'
    assert entry_archive.data.measurements.jv_bottom_cell.results.fill_factor == 0.782
    assert (
        entry_archive.data.measurements.jv_bottom_cell.results.open_circuit_voltage
        == ureg.Quantity(0.682, 'volt')
    )

    # stabilised performance
    assert (
        entry_archive.data.measurements.stabilised_performance_full_device.method
        == 'Stabilised performance'
    )
    assert (
        entry_archive.data.measurements.stabilised_performance_full_device.conditions.procedure
        == 'MPPT'
    )
    assert (
        entry_archive.data.measurements.stabilised_performance_full_device.results.power_conversion_efficiency
        == 0.227
    )

    # eqe
    assert (
        entry_archive.data.measurements.eqe_top_cell.method
        == 'External quantum efficiency'
    )
    assert (
        entry_archive.data.measurements.eqe_top_cell.results.integrated_short_circuit_current_density
        == ureg.Quantity(19.9, 'milliampere / centimeter ** 2')
    )
