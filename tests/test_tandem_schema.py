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
    reference = entry_archive.data.reference
    assert reference.data_entered_by_author is False
    assert reference.DOI_number == 'https://doi.org/10.1002/advs.201700675'

    # test general
    general = entry_archive.data.general
    assert general.architecture == 'Stacked'
    assert general.number_of_terminals == 4
    assert general.number_of_junctions == 2
    assert general.number_of_cells == 1
    assert general.photoabsorber == ['CIGS', 'Perovskite']
    assert general.photoabsorber_bandgaps == [1.18, 1.62]
    assert general.area_measured == ureg.Quantity(0.213, 'centimeter ** 2')

    # test layer stack
    stack = entry_archive.data.layer_stack
    assert len(stack) == 18

    # Layer 1: SLG
    layer = stack[0]
    assert layer.name == 'SLG'
    assert layer.functionality == 'Substrate'
    assert layer.synthesis.origin == 'Commercial'

    # Layer 2: Mo
    layer = stack[1]
    assert layer.name == 'Mo'
    assert layer.functionality == 'Back contact'
    assert layer.properties.thickness == ureg.Quantity(700, 'nanometer')
    assert layer.synthesis.origin == 'Lab made'
    assert layer.synthesis.process_steps[0].name == 'Sputtering'

    # Layer 3: CIGS
    layer = stack[2]
    assert layer.name == 'CIGS'
    assert layer.functionality == 'Photoabsorber'
    assert layer.properties.thickness == ureg.Quantity(3, 'micrometer')
    assert layer.properties.bandgap == ureg.Quantity(1.18, 'electron_volt')
    assert layer.synthesis.process_steps[0].name == 'Co-evaporation'
    assert layer.composition.ions[0].name == 'Cu'
    assert layer.composition.ions[0].coefficient == 1
    assert layer.composition.ions[1].name == 'In'
    assert layer.composition.ions[1].coefficient == 0.59

    # Layer 13: Perovskite
    layer = stack[12]
    assert layer.name == 'Perovskite'
    assert layer.functionality == 'Photoabsorber'
    assert layer.properties.thickness == ureg.Quantity(520, 'nanometer')
    assert layer.properties.bandgap == ureg.Quantity(1.62, 'electron_volt')
    assert layer.synthesis.process_steps[0].name == 'Evaporation'
    assert layer.synthesis.process_steps[0].atmosphere == 'Vacuum'
    assert layer.synthesis.process_steps[0].reactants[0].name == 'PbI2'
    assert layer.synthesis.process_steps[1].name == 'Spin-coating'
    assert layer.synthesis.process_steps[1].atmosphere == 'N2'
    assert layer.synthesis.process_steps[1].reactants[0].name == 'MAI'
    assert layer.synthesis.process_steps[1].solvent[0].name == 'IPA'
    assert layer.synthesis.process_steps[2].name == 'Thermal Annealing'
    assert layer.synthesis.process_steps[2].atmosphere == 'Unknown'
    assert layer.synthesis.process_steps[2].duration == ureg.Quantity(10, 'minute')
    assert layer.synthesis.process_steps[2].temperature == ureg.Quantity(100, 'celsius')
    assert layer.synthesis.process_steps[3].name == 'Spin-coating'
    assert layer.synthesis.process_steps[4].name == 'Thermal Annealing'
    assert layer.synthesis.process_steps[5].name == 'Solvent Annealing'
    assert layer.synthesis.process_steps[5].atmosphere == 'Chlorobenzene'
    assert layer.synthesis.process_steps[5].duration == ureg.Quantity(60, 'minute')

    ## test measurements

    # jv
    jv = entry_archive.data.measurements.jv_bottom_cell
    assert jv.method == 'JV'
    assert jv.results.fill_factor == 0.782
    assert jv.results.open_circuit_voltage == ureg.Quantity(0.682, 'volt')

    # stabilised performance
    performance = entry_archive.data.measurements.stabilised_performance_full_device
    assert performance.method == 'Stabilised performance'
    assert performance.conditions.procedure == 'MPPT'
    assert performance.results.power_conversion_efficiency == 0.227

    # eqe
    eqe = entry_archive.data.measurements.eqe_top_cell
    assert eqe.method == 'External quantum efficiency'
    assert eqe.results.integrated_short_circuit_current_density == ureg.Quantity(
        19.9, 'milliampere / centimeter ** 2'
    )
