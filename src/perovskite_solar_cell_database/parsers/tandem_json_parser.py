import json
import os
from typing import TYPE_CHECKING

from jmespath import search
from nomad.datamodel.datamodel import EntryArchive
from nomad.parsing.parser import MatchingParser

from perovskite_solar_cell_database.parsers.utils import create_archive
from perovskite_solar_cell_database.schema_packages.tandem.schema import (
    PerovskiteTandemSolarCell,
)
from perovskite_solar_cell_database.schema_packages.tandem.tandem import (
    Layer,
)

if TYPE_CHECKING:
    from structlog.stdlib import BoundLogger


class TandemJSONParser(MatchingParser):
    """
    Parser for tandem JSON files and creating instances of PerovskiteTandemSolarCell.
    """

    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
        child_archives: dict[str, 'EntryArchive'] = None,
    ) -> None:
        filename = os.path.basename(mainfile)
        logger.info(f'Parsing file {filename}')

        tandem = PerovskiteTandemSolarCell()

        with open(mainfile) as file:
            source_dict = json.load(file)

        update_dict = map_json_to_schema(source_dict)

        # Get ID from filename
        update_dict['reference']['ID'] = int(
            os.path.splitext(filename)[0].split('_')[-1]
        )

        tandem.m_update_from_dict(update_dict)
        archive.data = tandem


def map_json_to_schema(source: dict) -> dict:
    """
    Maps the JSON data to the PerovskiteTandemSolarCell schema.
    """

    data = {}

    # Reference
    data['reference'] = {
        'DOI_number': search('reference_data.doi', source),
        'name_of_person_entering_the_data': search(
            'reference_data.name_of_person_entering_the_data', source
        ),
        'data_entered_by_author': search(
            'reference_data.data_entered_by_author', source
        ),
    }

    # General
    data['general'] = {
        'architecture': search('device_classification.tandem_architecture', source),
        'number_of_terminals': search(
            'device_classification.number_of_terminals', source
        ),
        'number_of_junctions': search(
            'device_classification.number_of_junctions', source
        ),
        'number_of_cells': search(
            'device_classification.device_area.number_of_cells', source
        ),
        'photoabsorber': search(
            'device_classification.tandem_technology', source
        ).split(' | '),
        'photoabsorber_bandgaps': search('device_classification.band_gaps', source),
        'area_measured': search('device_classification.device_area.cell_area', source),
        'flexibility': search('device_classification.is_flexible', source),
        'semitransparent': search('device_classification.is_semitransparent', source),
        'contains_textured_layers': None,  # Not available in JSON.
        'contains_antireflectie_coating': None,  # Not available in JSON.
        'subcell': [],  # Not available in JSON.
    }

    # Layer Stack
    data['layer_stack'] = []
    layers_from_source = search('device_stack.layers', source) or []
    for layer_from_source in layers_from_source:
        # General layer properties
        layer = {}
        layer['properties'] = {
            'thickness': search('thickness', layer_from_source),
        }

        functionality = search('functionality', layer_from_source)
        if functionality:
            functionality = functionality.replace('_', ' ')
            if functionality in Layer.functionality.type:
                layer['functionality'] = functionality
                layer['name'] = (
                    functionality  # TODO: What should be the name of the layer?
                )
            else:
                functionality = None

        # Specify layer type
        if functionality == 'Photoabsorber':
            layer['properties'].update(
                {
                    'bandgap': search('band_gap.value', layer_from_source),
                    'bandgap_graded': search('band_gap.is_graded', layer_from_source),
                    'bandgap_estimation_basis': search(
                        'band_gap.estimated_from', layer_from_source
                    ),
                }
            )
            photoabsorber = search('photoabsorber_material', layer_from_source)
            if photoabsorber == 'Perovskite':
                layer = update_perovskite_layer(layer, layer_from_source)
            elif photoabsorber == 'CIGS':  # TODO: Check how this is called in the JSON.
                layer = update_CIGS_layer(layer, layer_from_source)
            elif photoabsorber == 'Silicon':
                layer = update_silicon_layer(layer, layer_from_source)
            else:
                layer = update_other_photoabsorber_layer(layer, layer_from_source)
        else:
            layer = update_nonabsorbing_layer(layer, layer_from_source)

        # Deposition and Synthesis
        layer = parse_synthesis(layer, layer_from_source)

        # Append layer to layer stack
        data['layer_stack'].append(layer)

    # Measurements
    data['measurements'] = {}

    # JV measurements
    JV_from_source = search('measurements.jv_measurements', source) or []
    for jv in JV_from_source:
        data = parse_jv_measurement(data, jv)

    # EQE measurements
    EQE_from_source = search('measurements.EQE', source) or []
    for eqe in EQE_from_source:
        data = parse_eqe_measurement(data, eqe)

    # Transmission measurements
    transmission_from_source = search('measurements.Transmission', source) or []
    for transmission in transmission_from_source:
        data = parse_transmission_measurement(data, transmission)

    return data


#### Layer functions ####


def update_perovskite_layer(layer: dict, layer_from_source: dict) -> dict:
    """
    Maps the JSON data to the Perovskite layer schema.
    """

    layer.update(
        {
            'm_def': (
                'perovskite_solar_cell_database.schema_packages.tandem.tandem.PerovskiteLayer'
            ),
            'name': 'Perovskite',
        }
    )

    # Layer properties
    layer['properties'].update(
        {
            'inorganic': search('is_inorganic', layer_from_source),
            'lead_free': search('is_lead_free', layer_from_source),
        }
    )

    # Layer composition
    layer['composition'] = {
        'm_def': 'perovskite_solar_cell_database.composition.PerovskiteCompositionSection',
        'ions_a_site': [],
        'ions_b_site': [],
        'ions_x_site': [],
        # 'composition_estimate': search('composition_estimate', layer_from_source), # TODO: Check how this is called in the JSON
    }
    dim_map = {0: '0D', 1: '1D', 2: '2D', 2.5: '2D/3D', 3: '3D'}
    dimensionality = search('dimensionality', layer_from_source)
    if dimensionality:
        layer['properties']['dimensionality'] = dim_map.get(dimensionality, 'Other')
    # Ions
    for ion in search('composition.a_ions', layer_from_source):
        layer['composition']['ions_a_site'].append(
            {
                'm_def': 'perovskite_solar_cell_database.composition.PerovskiteAIonComponent',
                'abbreviation': search('ion', ion),
                'coefficient': search('coefficient', ion),
            }
        )
    for ion in search('composition.b_ions', layer_from_source):
        layer['composition']['ions_b_site'].append(
            {
                'm_def': 'perovskite_solar_cell_database.composition.PerovskiteBIonComponent',
                'abbreviation': search('ion', ion),
                'coefficient': search('coefficient', ion),
            }
        )
    for ion in search('composition.x_ions', layer_from_source):
        layer['composition']['ions_x_site'].append(
            {
                'm_def': 'perovskite_solar_cell_database.composition.PerovskiteXIonComponent',
                'abbreviation': search('ion', ion),
                'coefficient': search('coefficient', ion),
            }
        )

    return layer


def update_CIGS_layer(layer: dict, lay: dict) -> dict:
    """
    Maps the JSON data to the CIGS layer schema.
    """

    layer['m_def'] = (
        'perovskite_solar_cell_database.schema_packages.tandem.tandem.ChalcopyriteLayer'
    )
    layer['name'] = 'CIGS'

    return layer


def update_silicon_layer(layer: dict, lay: dict) -> dict:
    """
    Maps the JSON data to the Silicon layer schema.
    """

    layer['m_def'] = (
        'perovskite_solar_cell_database.schema_packages.tandem.tandem.SiliconLayer'
    )
    layer['name'] = 'Silicon'

    return layer


def update_other_photoabsorber_layer(layer: dict, lay: dict) -> dict:
    """
    Maps the JSON data to the Other Photoabsorber layer schema.
    """

    layer['m_def'] = (
        'perovskite_solar_cell_database.schema_packages.tandem.tandem.PhotoAbsorberLayer'
    )

    return layer


def update_nonabsorbing_layer(layer: dict, lay: dict) -> dict:
    """
    Maps the JSON data to the General layer schema.
    """

    layer['m_def'] = (
        'perovskite_solar_cell_database.schema_packages.tandem.tandem.NonAbsorbingLayer'
    )

    return layer


#### Synthesis functions ####

# Liquid-based processes
liquid_based_processes = [
    'Air brush spray',
    'Brush painting',
    'Centrifuge-casting',
    'Dip-coating',
    'Doctor blading',
    'Dropcasting',
    'Drop-infiltration',
    'Electrospinning',
    'Electrospraying',
    'Inkjet printing',
    'Lamination',
    'Langmuir-Blodgett deposition',
    'Meniscus-coating',
    'Painting',
    'Roller coating',
    'Sandwiching',
    'Screen printing',
    'Slot-die coating',
    'Spin-coating',
    'Spray-coating',
    'Spray-pyrolysis',
    'Sprinkling',
    'Substrate vibration assisted dropcasting',
    'Ultrasonic spray',
    'Ultrasonic spray pyrolysis',
]

# Gas-phase processes
gas_phase_processes = [
    'Aerosol-assisted CVD',
    'ALD',
    'Candle burning',
    'CBD',
    'Chemical etching',
    'Co-evaporation',
    'Condensation',
    'CVD',
    'DC Magnetron Sputtering',
    'DC Reactive Magnetron Sputtering',
    'DC Sputtering',
    'E-beam evaporation',
    'Evaporation',
    'Frequency Magnetron Sputtering',
    'Gelation',
    'Hydrolysis',
    'Hydrothermal',
    'Magnetron sputtering',
    'Oxidation',
    'Oxygen plasma treatment',
    'Pulsed laser deposition',
    'PVD',
    'Reactive sputtering',
    'RF Magnetron Sputtering',
    'RF plasma sputtering',
    'RF sputtering',
    'SILAR',
    'Solvothermal',
    'Sputtering',
    'Thermal oxidation',
]


def parse_synthesis(layer: dict, layer_from_source: dict) -> dict:
    """
    Maps the JSON data to the Synthesis schema.
    """

    layer['synthesis'] = {
        'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.tandem.Synthesis',
        'process_steps': [],
    }

    process_steps = search('deposition_procedure', layer_from_source) or []
    for step in process_steps:
        name = search('procedure', step)
        if name in liquid_based_processes:
            process = {
                'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.tandem.LiquidSynthesis',
                'name': name,
            }
        elif name in gas_phase_processes:
            process = {
                'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.tandem.GasPhaseSynthesis',
                'name': name,
            }
        else:
            process = None

        if process:
            layer['synthesis']['process_steps'].append(process)

    if len(layer['synthesis']['process_steps']) > 0:
        layer['synthesis']['origin'] = 'Lab made'

    return layer


#### Measurement functions ####


def map_source_of_measurement(measurement: dict) -> str:
    """
    Maps the source of the measurement to the correct value.
    """
    if (
        search('measurement_done_on', measurement) == 'Compleat_device'
        or search('is_identical_to_cell_in_tandem_stack', measurement) is True
    ):
        source = 'This device'
    elif search('is_identical_to_cell_in_tandem_stack', measurement) is False:
        source = 'Analogous free standing cell'
    else:
        source = 'Unknown'

    return source


def parse_jv_measurement(data: dict, jv: dict) -> dict:
    """
    Maps the JSON data to the JV measurement schema.
    """

    # Map source
    source = map_source_of_measurement(jv)

    # Conditions
    conditions = {
        'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.measurements.JVConditions',
        'atmosphere': search('environmental_conditions.atmosphere', jv),
        # 'duration' : search('environmental_conditions.duration', jv), # TODO: Check how this is called in the JSON
        # 'temperature': search('environmental_conditions.temperature', jv), # TODO: Check how this is called in the JSON
        # 'humidity_relative': search('environmental_conditions.humidity', jv), # TODO: Check how this is called in the JSON
        'illumination': {
            'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.measurements.Illumination',
            'type': search('light_conditions.light_source', jv),
            'brand': search('light_conditions.light_source_brand_name', jv),
            'spectrum': search('light_conditions.light_spectra', jv),
            'intensity': search('light_conditions.light_intensity', jv),
            'mask': search('light_conditions.shadow_mask_is_used', jv),
        },
    }

    # JV measurement
    jv_measurement = {
        'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.measurements.JVMeasurement',
        'source': source,
        'conditions': conditions,
        'results': {
            'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.measurements.JVResults',
            'short_circuit_current_density': search('jv_metrics.j_sc', jv),
            'open_circuit_voltage': search('jv_metrics.voc', jv),
            'fill_factor': search('jv_metrics.ff', jv),
            'efficiency': round(float(search('jv_metrics.pce', jv)) / 100, 5)
            if search('jv_metrics.pce', jv)
            else None,
        },
    }

    # assign to the correct attribute
    if source == 'This device':
        if search('jv_metrics.scan_direction', jv) == 'Reversed':
            data['measurements']['jv_full_device_reverse'] = jv_measurement
        else:
            data['measurements']['jv_full_device_forward'] = jv_measurement
    elif source == 'Analogous free standing cell':
        if search('measurement_done_on', jv) == 'Top_cell':
            data['measurements']['jv_top_cell'] = jv_measurement
        elif search('measurement_done_on', jv) == 'Bottom_cell':
            data['measurements']['jv_bottom_cell'] = jv_measurement

    # TODO: Shaded cell

    return data


def parse_eqe_measurement(data: dict, eqe: dict) -> dict:
    """
    Maps the JSON data to the EQE measurement schema.
    """

    # Map source
    source = map_source_of_measurement(eqe)

    # Conditions
    conditions = {}

    # EQE measurement
    eqe_measurement = {
        'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.measurements.ExternalQuantumEfficiency',
        'source': source,
        'conditions': conditions,
        'results': {
            'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.measurements.EQEResults',
            'integrated_short_circuit_current_density': search(
                'EQE_metrics.integrated_current', eqe
            ),
        },
    }

    # assign to the correct attribute
    if source == 'This device':
        data['measurements']['eqe_full_device'] = eqe_measurement
    elif source == 'Analogous free standing cell':
        if search('measurement_done_on', eqe) == 'Top_cell':
            data['measurements']['eqe_top_cell'] = eqe_measurement
        elif search('measurement_done_on', eqe) == 'Bottom_cell':
            data['measurements']['eqe_bottom_cell'] = eqe_measurement

    return data


def parse_transmission_measurement(data: dict, transmission: dict) -> dict:
    """
    Maps the JSON data to the Transmission measurement schema.
    """

    # Map source
    # source = map_source_of_measurement(transmission)

    # Transmission measurement
    transmission_measurement = {
        'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.measurements.Transmission',
        'results': {
            'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.measurements.TransmissionResults',
            'integrated_transmission': search(
                'average_transmission_in_the_visible_range', transmission
            ),
        },
    }

    # assign to the correct attribute
    if search('measurement_done_on', transmission) == 'Top_cell':
        data['measurements']['transmission_top_cell'] = transmission_measurement
    elif search('measurement_done_on', transmission) == 'Bottom_cell':
        data['measurements']['transmission_bottom_cell'] = transmission_measurement

    return data
