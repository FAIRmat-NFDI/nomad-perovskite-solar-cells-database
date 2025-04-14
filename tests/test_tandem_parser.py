import os.path
from datetime import UTC, datetime

from nomad.client import normalize_all, parse
from nomad.metainfo import Quantity
from nomad.units import ureg


def test_schema():
    test_file = os.path.join(
        os.path.dirname(__file__), 'data', 'Json_data_tandem_cell_initialdata_0.json'
    )
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

    # test reference
    reference = entry_archive.data.reference
    assert reference.DOI_number == 'https://doi.org/10.1039/d0ta12286f'
    assert reference.ID == 0
    assert reference.publication_date == datetime.fromisoformat(
        '2021-03-18T12:44:28'
    ).replace(tzinfo=UTC)
    assert reference.journal == 'Journal of Materials Chemistry A'
    assert reference.publication_authors[0] == 'Xin Wu'
    assert reference.name_of_person_entering_the_data == 'Adam Hultqvist'
    assert reference.data_entered_by_author is False

    # test general
    general = entry_archive.data.general
    assert general.architecture == 'Monolithic'
    assert general.number_of_terminals == 2
    assert general.number_of_junctions == 2
    assert general.number_of_cells == 0  # default value
    assert general.photoabsorber == ['OPV', 'Perovskite']
    assert general.photoabsorber_bandgaps == [1.3, 1.79]
    assert general.flexibility is False
    assert general.semitransparent is False
    assert general.contains_textured_layers is False  # default value
    assert general.contains_antireflective_coating is False  # default value

    ## tests for layer stack
    stack = entry_archive.data.layer_stack
    assert len(stack) == 11

    # Layer 1: Back contact
    layer = stack[0]
    assert layer.name == 'Back contact'
    assert layer.functionality == 'Back contact'
    assert layer.properties.thickness.value == ureg('100 nm')
    assert layer.composition.components[0].name == 'Ag'
    assert layer.composition.components[0].role == 'Majority Phase'
    assert layer.synthesis.origin == 'Lab made'
    assert layer.synthesis.steps[0].name == 'Evaporation'

    # Layer 2: HTL
    layer = stack[1]
    assert layer.name == 'HTL'
    assert layer.functionality == 'HTL'
    assert layer.properties.thickness.value == ureg('10 nm')
    assert layer.composition.components[0].name == 'MoO3'
    assert layer.composition.components[0].role == 'Majority Phase'
    assert layer.synthesis.origin == 'Lab made'
    assert layer.synthesis.steps[0].name == 'Evaporation'

    # Layer 3: OPV
    layer = stack[2]
    assert layer.name == 'OPV'
    assert layer.functionality == 'Photoabsorber'
    assert layer.properties.thickness.value == ureg('110 nm')
    assert layer.properties.bandgap.value == ureg('1.3 eV')
    assert layer.properties.bandgap.determined_by == 'EQE'
    assert layer.properties.bandgap.graded is False
    assert layer.composition.components[0].name == 'PM6'
    assert layer.composition.components[0].role == 'Majority Phase'
    assert layer.composition.components[0].molar_fraction == 0.45
    # assert layer.composition.components[0].pub_chem_cid == ...
    assert layer.composition.components[1].name == 'Y6'
    assert layer.composition.components[1].role == 'Majority Phase'
    assert layer.composition.components[1].molar_fraction == 0.55
    assert layer.composition.components[1].pub_chem_cid == 145705715
    assert layer.synthesis.origin == 'Lab made'
    assert layer.synthesis.steps[0].name == 'Spin-coating'

    # Layer 4: ETL
    layer = stack[3]
    assert layer.name == 'ETL'
    assert layer.functionality == 'ETL'
    assert layer.properties.thickness.value == ureg('50 nm')
    assert layer.composition.components[0].name == 'ZnO'
    assert layer.composition.components[0].role == 'Majority Phase'
    # assert layer.composition.components[0].pub_chem_cid == ...
    assert layer.synthesis.origin == 'Lab made'
    assert layer.synthesis.steps[0].name == 'Spin-coating'

    # Layer 5: Recombination layer
    layer = stack[4]
    assert layer.name == 'Recombination layer'
    assert layer.functionality == 'Recombination layer'
    assert layer.properties.thickness.value == ureg('1 nm')
    assert layer.composition.components[0].name == 'Ag'
    assert layer.composition.components[0].role == 'Majority Phase'
    assert layer.composition.components[0].pub_chem_cid == 23954
    assert layer.synthesis.origin == 'Lab made'
    assert layer.synthesis.steps[0].name == 'Evaporation'

    # Layer 6: HTL
    layer = stack[5]
    assert layer.name == 'HTL'
    assert layer.functionality == 'HTL'
    assert layer.properties.thickness.value == ureg('6 nm')
    assert layer.composition.components[0].name == 'MoO3'
    assert layer.composition.components[0].role == 'Majority Phase'
    assert layer.composition.components[0].pub_chem_cid == 14802
    assert layer.synthesis.origin == 'Lab made'
    assert layer.synthesis.steps[0].name == 'Evaporation'

    # Layer 7: HTL
    layer = stack[6]
    assert layer.name == 'HTL'
    assert layer.functionality == 'HTL'
    assert layer.properties.thickness.value == ureg('25 nm')
    assert layer.composition.components[0].name == 'PBDB-T'
    assert layer.composition.components[0].role == 'Majority Phase'
    assert layer.composition.components[0].pub_chem_cid == 164608287
    assert layer.synthesis.origin == 'Lab made'
    assert layer.synthesis.steps[0].name == 'Spin-coating'

    # Layer 8: Perovskite
    layer = stack[7]
    assert layer.name == 'Perovskite'
    assert layer.functionality == 'Photoabsorber'
    assert layer.properties.thickness.value == ureg('180 nm')
    assert layer.properties.crystallinity.value == 'Polycrystalline'
    assert layer.properties.bandgap.value == ureg('1.79 eV')
    assert layer.properties.bandgap.determined_by == 'Absorption Tauc-plot'
    assert layer.properties.bandgap.graded is False
    assert layer.properties.inorganic is True
    assert layer.properties.lead_free is False
    assert layer.composition.long_form == 'Cs1.0Pb1.0Br0.9I2.1'

    # TODO: add remaining layers...

    ## tests for measurements

    # jv
    jv = entry_archive.data.measurements.jv_measurements
    assert len(jv) == 3
    for measurement in jv:
        assert measurement.method == 'JV'
        assert measurement.certified is False
        assert measurement.conditions.illumination.type == 'Solar simulator'
        assert measurement.conditions.illumination.brand == 'Enlitech SS-F5'
        assert measurement.conditions.illumination.spectrum == 'AM 1.5'
        assert measurement.conditions.illumination.intensity == ureg('100 W/m^2')

    assert jv[0].component_association == 0
    assert jv[0].results.short_circuit_current_density == ureg('12.67 mA/cm^2')
    assert jv[0].results.open_circuit_voltage == ureg('1.89 V')
    assert jv[0].results.fill_factor == 12.67
    assert jv[0].results.power_conversion_efficiency == 0.1717

    assert jv[1].component_association == 1
    assert jv[1].results.short_circuit_current_density == ureg('15.46 mA/cm^2')
    assert jv[1].results.open_circuit_voltage == ureg('1.15 V')
    assert jv[1].results.fill_factor == 0.812
    assert jv[1].results.power_conversion_efficiency == 0.1443

    assert jv[2].component_association == 2
    assert jv[2].results.short_circuit_current_density == ureg('24.75 mA/cm^2')
    assert jv[2].results.open_circuit_voltage == ureg('0.83 V')
    assert jv[2].results.fill_factor == 0.682
    assert jv[2].results.power_conversion_efficiency == 0.1401

    # eqe
    results = [ureg('12 mA/cm^2'), ureg('14.87 mA/cm^2'), ureg('23.57 mA/cm^2')]
    eqe = entry_archive.data.measurements.eqe_measurements
    for measurement in eqe:
        assert measurement.method == 'External quantum efficiency'
        assert measurement.certified is False
        assert (
            measurement.results.integrated_short_circuit_current_density
            == results[measurement.component_association]
        )
