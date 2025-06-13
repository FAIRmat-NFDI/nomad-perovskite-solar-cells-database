import json
import os
from typing import TYPE_CHECKING, Optional

from jmespath import search
from nomad.datamodel.datamodel import EntryArchive
from nomad.parsing.parser import MatchingParser

from perovskite_solar_cell_database.parsers.utils import create_archive
from perovskite_solar_cell_database.schema_packages.tandem.device_stack import (
    BandGap,
    Layer,
)
from perovskite_solar_cell_database.schema_packages.tandem.schema import (
    PerovskiteTandemSolarCell,
    RawFileTandemJson,
)

if TYPE_CHECKING:
    from structlog.stdlib import BoundLogger


def get_id_from_mainfile(mainfile: str) -> str:
    """
    Extracts the ID from the mainfile name.
    The ID is expected to be the last part of the filename, separated by an underscore.
    """
    try:
        return os.path.splitext(mainfile)[0].split('_')[-1]
    except IndexError:
        raise ValueError(f'Invalid filename format: {mainfile}')


def get_eln_archive_name(mainfile: str) -> str:
    """
    Returns the name of the archive file for the ELN.
    The name is generated based on the mainfile name.
    """
    return f'tandem_{get_id_from_mainfile(mainfile)}.archive.json'


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
        with open(mainfile) as file:
            source_dict = json.load(file)

        update_dict = map_json_to_schema(source_dict)

        # Get ID from filename
        id = get_id_from_mainfile(mainfile)
        update_dict['reference']['ID'] = id

        tandem = PerovskiteTandemSolarCell()
        tandem.m_update_from_dict(update_dict)

        archive.data = RawFileTandemJson(
            tandem=create_archive(tandem, archive, get_eln_archive_name(mainfile)),
            data=source_dict,
        )
        archive.metadata.entry_name = f'Tandem {id} data file'


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
    photoabsorber = search('device_classification.tandem_technology', source)
    photoabsorber = photoabsorber.split(' | ') if photoabsorber else None
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
        'photoabsorber': photoabsorber,
        'photoabsorber_bandgaps': search('device_classification.band_gaps', source),
        'area_measured': search('device_classification.device_area.cell_area', source),
        'flexibility': search('device_classification.is_flexible', source),
        'semitransparent': search('device_classification.is_semitransparent', source),
        'contains_textured_layers': None,  # Not available in JSON.
        'contains_antireflective_coating': None,  # Not available in JSON.
        'subcell': [],  # Not available in JSON.
    }

    # Layer Stack
    data['layer_stack'] = []
    layers_from_source = search('device_stack.layers', source) or []
    for layer_from_source in layers_from_source:
        layer = {}
        layer['properties'] = parse_layer_properties(layer_from_source)
        layer['subcell_association'] = map_subcell_association(
            search('subcell_association', layer_from_source)
        )

        # Functionality
        functionality = search('functionality', layer_from_source)
        if functionality:
            functionality = functionality.replace('_', ' ')
            if functionality in Layer.functionality.type:
                layer['functionality'] = functionality
                layer['name'] = functionality
            else:
                functionality = None

        # Specify layer type
        if functionality == 'Photoabsorber':
            photoabsorber = search('photoabsorber_material', layer_from_source)
            if photoabsorber:
                layer['name'] = photoabsorber
            if photoabsorber == 'Perovskite':
                layer = parse_perovskite_layer(layer, layer_from_source)
            elif photoabsorber == 'CIGS':  # TODO: Check how this is called in the JSON.
                layer = parse_CIGS_layer(layer, layer_from_source)
            elif photoabsorber == 'Silicon':
                layer = parse_silicon_layer(layer, layer_from_source)
            else:
                layer = parse_other_photoabsorber_layer(layer, layer_from_source)
        else:
            layer = parse_other_layer(layer, layer_from_source)

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

    # Stability measurements
    stability_from_source = search('measurements.Stability', source) or []
    for stability in stability_from_source:
        data = parse_stability_measurement(data, stability)

    # EQE measurements
    EQE_from_source = search('measurements.EQE', source) or []
    for eqe in EQE_from_source:
        data = parse_eqe_measurement(data, eqe)

    # Transmission measurements
    transmission_from_source = search('measurements.Transmission', source) or []
    for transmission in transmission_from_source:
        data = parse_transmission_measurement(data, transmission)

    return data


def map_subcell_association(mention: str) -> int | None:
    """
    Maps the source of the measurement to the subcell association (int).
    """

    if not mention:
        return None

    association = None
    if mention.lower() in {'compleat_device', 'monolitic_device'}:
        association = 0
    if mention.lower() == 'bottom_cell':
        association = 1
    if mention.lower() == 'top_cell':
        association = 2

    return association


#### Layer functions ####


def parse_layer_properties(layer_from_source: dict) -> dict:
    """
    Maps the JSON data to LayerProperties and returns the properties dictionary.
    """

    properties = {}

    # General layer properties
    thickness = search('thickness', layer_from_source)
    if thickness:
        properties['thickness'] = {
            'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.layer_stack.Thickness',
            'value': thickness,
        }

    surface_roughness = search('surface_roughness', layer_from_source)
    if surface_roughness:
        properties['surface_roughness'] = {
            'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.layer_stack.SurfaceRoughness',
            'value': surface_roughness,
        }

    area = search('area', layer_from_source)
    if area:
        properties['area'] = {
            'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.layer_stack.Area',
            'value': area,
        }

    bandgap = search('band_gap.value', layer_from_source)
    if bandgap:
        determined_by = search('band_gap.estimated_from', layer_from_source)
        if determined_by and determined_by not in BandGap.determined_by.type:
            determined_by = None
        properties['bandgap'] = {
            'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.layer_stack.BandGap',
            'value': bandgap,
            'graded': search('band_gap.is_graded', layer_from_source),
            'determined_by': determined_by,
        }

    conductivity = search('conductivity', layer_from_source)
    if conductivity:
        properties['conductivity'] = {
            'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.layer_stack.Conductivity',
            'value': conductivity,
        }

    crystallinity = search('crystallinity', layer_from_source)
    if crystallinity:
        if crystallinity.lower()[:6] == 'amorph':
            crystallinity = 'Amorphous'
        elif crystallinity.lower()[:6] == 'polycr':
            crystallinity = 'Polycrystalline'
        elif crystallinity.lower()[:6] == 'single':
            crystallinity = 'Single Crystal'
        else:
            crystallinity = None
    if crystallinity:
        properties['crystallinity'] = {
            'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.layer_stack.Crystallinity',
            'value': crystallinity,
        }

    return properties


def parse_composition(layer: dict, layer_from_json: dict) -> dict:
    """
    Parses the composition of a layer from the JSON data and updates the layer dictionary.
    """

    materials = search('materials_in_layer', layer_from_json)

    if not materials:
        return None

    # Create composition section
    composition = {
        'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.layer_stack.LayerComposition',
        'components': [],
    }

    # Fill in the components
    for material in materials:
        component = {
            'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.layer_stack.LayerComponent',
            'name': search('name', material),
        }

        # Map the role of the component
        role_map = {
            'majority_phase': 'Majority Phase',
            'secondary_phase': 'Secondary Phase',
            'additive': 'Additive',
            'dopant': 'Dopant',
        }
        role = search('functionality_in_layer', material)
        if role in role_map:
            component['role'] = role_map[role]

        # Figure out fraction quantity
        if search('fraction_of_layer_content_metric', material) == 'mol_fraction':
            component['molar_fraction'] = search('fraction_of_layer_content', material)
        elif search('fraction_of_layer_content_metric', material) == 'mass_fraction':
            component['mass_fraction'] = search('fraction_of_layer_content', material)
        elif search('fraction_of_layer_content_metric', material) == 'volume_fraction':
            component['volume_fraction'] = search('fraction_of_layer_content', material)

        composition['components'].append(component)

    return composition


def parse_perovskite_layer(layer: dict, layer_from_json: dict) -> dict:
    """
    Maps the JSON data to the Perovskite layer schema.
    Returns the layer dictionary with the updated values.
    """

    # Assign specific layer type
    layer['m_def'] = (
        'perovskite_solar_cell_database.schema_packages.tandem.layer_stack.PerovskiteLayer'
    )

    # Layer properties
    layer['properties'].update(
        {
            'm_def': (
                'perovskite_solar_cell_database.schema_packages.tandem.layer_stack.PerovskiteLayerProperties'
            ),
            'inorganic': search('is_inorganic', layer_from_json),
            'lead_free': search('is_lead_free', layer_from_json),
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
    dimensionality = search('dimensionality', layer_from_json)
    if dimensionality:
        layer['properties']['dimensionality'] = dim_map.get(dimensionality, 'Other')
    # Ions
    for ion in search('composition.a_ions', layer_from_json) or []:
        layer['composition']['ions_a_site'].append(
            {
                'm_def': 'perovskite_solar_cell_database.composition.PerovskiteAIonComponent',
                'abbreviation': search('ion', ion),
                'coefficient': search('coefficient', ion),
            }
        )
    for ion in search('composition.b_ions', layer_from_json) or []:
        layer['composition']['ions_b_site'].append(
            {
                'm_def': 'perovskite_solar_cell_database.composition.PerovskiteBIonComponent',
                'abbreviation': search('ion', ion),
                'coefficient': search('coefficient', ion),
            }
        )
    for ion in search('composition.x_ions', layer_from_json) or []:
        layer['composition']['ions_x_site'].append(
            {
                'm_def': 'perovskite_solar_cell_database.composition.PerovskiteXIonComponent',
                'abbreviation': search('ion', ion),
                'coefficient': search('coefficient', ion),
            }
        )

    return layer


def parse_CIGS_layer(layer: dict, layer_from_json: dict) -> dict:
    """
    Maps the JSON data to the CIGS layer schema.
    """

    # Assign specific layer type
    layer['m_def'] = (
        'perovskite_solar_cell_database.schema_packages.tandem.layer_stack.ChalcopyriteLayer'
    )

    # Layer composition
    layer['composition'] = parse_composition(layer, layer_from_json)
    layer['composition'].update(
        {
            'm_def': 'perovskite_solar_cell_database.composition.ChalcopyriteLayerComposition',
        }
    )

    # TODO : Parse composition

    return layer


def parse_silicon_layer(layer: dict, layer_from_json: dict) -> dict:
    """
    Maps the JSON data to the Silicon layer schema.
    """

    # Assign specific layer type
    layer['m_def'] = (
        'perovskite_solar_cell_database.schema_packages.tandem.layer_stack.SiliconLayer'
    )

    # Layer composition
    layer['composition'] = parse_composition(layer, layer_from_json)

    # Layer properties
    layer['properties'].update(
        {
            'm_def': (
                'perovskite_solar_cell_database.schema_packages.tandem.layer_stack.SiliconLayerProperties'
            ),
        }
    )

    return layer


def parse_other_photoabsorber_layer(layer: dict, layer_from_json: dict) -> dict:
    """
    Maps the JSON data to the Other Photoabsorber layer schema.
    """

    # Assign specific layer type
    layer['m_def'] = (
        'perovskite_solar_cell_database.schema_packages.tandem.layer_stack.PhotoAbsorberLayer'
    )

    # Layer composition
    layer['composition'] = parse_composition(layer, layer_from_json)

    return layer


def parse_other_layer(layer: dict, layer_from_json: dict) -> dict:
    """
    Maps the JSON data to the General layer schema.
    """

    # Assign specific layer type
    layer['m_def'] = (
        'perovskite_solar_cell_database.schema_packages.tandem.layer_stack.Layer'
    )

    # Layer composition
    layer['composition'] = parse_composition(layer, layer_from_json)

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
        'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.layer_stack.Synthesis',
        'steps': [],
    }

    process_steps = search('deposition_procedure', layer_from_source) or []
    for step in process_steps:
        name = search('procedure', step)
        if name in liquid_based_processes:
            process = {
                'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.layer_stack.LiquidSynthesis',
                'name': name,
            }
        elif name in gas_phase_processes:
            process = {
                'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.layer_stack.GasPhaseSynthesis',
                'name': name,
            }
        else:
            process = None

        if process:
            layer['synthesis']['steps'].append(process)

    if len(layer['synthesis']['steps']) > 0:
        layer['synthesis']['origin'] = 'Lab made'

    return layer


#### Measurement functions ####


def convert_to_fraction(value: float | None) -> float | None:
    """
    Converts a percentage string to a fraction.
    """
    if value and value > 2:
        return value * 0.01
    return value


def parse_jv_measurement(data: dict, jv: dict) -> dict:
    """
    Maps the JSON data to the JV measurement schema.
    """

    # Check if list of JV measurements exists
    if 'jv_measurements' not in data['measurements']:
        data['measurements']['jv_measurements'] = []

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
    data['measurements']['jv_measurements'].append(
        {
            'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.measurements.JVMeasurement',
            'certified': search('is_certified', jv),
            'subcell_association': map_subcell_association(
                search('measurement_done_on', jv)
            ),
            'conditions': conditions,
            'results': {
                'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.measurements.JVResults',
                'short_circuit_current_density': search('jv_metrics.j_sc', jv),
                'open_circuit_voltage': search('jv_metrics.voc', jv),
                'fill_factor': convert_to_fraction(search('jv_metrics.ff', jv)),
                'power_conversion_efficiency': convert_to_fraction(
                    search('jv_metrics.pce', jv)
                ),
            },
        }
    )

    return data


def parse_eqe_measurement(data: dict, eqe: dict) -> dict:
    """
    Maps the JSON data to the EQE measurement schema.
    """

    # Check if list of EQE measurements exists
    if 'eqe_measurements' not in data['measurements']:
        data['measurements']['eqe_measurements'] = []

    # Conditions
    conditions = None  # TODO: Check if this can be extracted from the JSON

    # EQE measurement
    data['measurements']['eqe_measurements'].append(
        {
            'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.measurements.ExternalQuantumEfficiency',
            'certified': search('is_certified', eqe),
            'subcell_association': map_subcell_association(
                search('measurement_done_on', eqe)
            ),
            'conditions': conditions,
            'results': {
                'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.measurements.EQEResults',
                'integrated_short_circuit_current_density': search(
                    'EQE_metrics.integrated_current', eqe
                ),
            },
        }
    )

    return data


def parse_transmission_measurement(data: dict, transmission: dict) -> dict:
    """
    Maps the JSON data to the Transmission measurement schema.
    """

    # Check if list of transmission measurements exists
    if 'transmission' not in data['measurements']:
        data['measurements']['transmission'] = []

    # Conditions
    conditions = None  # TODO: Check if this can be extracted from the JSON

    # Transmission measurement
    avg_transmission = convert_to_fraction(
        search('average_transmission_in_the_visible_range', transmission)
    )
    if avg_transmission:
        data['measurements']['transmission'].append(
            {
                'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.measurements.Transmission',
                'certified': search('is_certified', transmission),
                'subcell_association': map_subcell_association(
                    search('measurement_done_on', transmission)
                ),
                'conditions': conditions,
                'results': {
                    'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.measurements.TransmissionResults',
                    'integrated_transmission': avg_transmission,
                },
            }
        )

    return data


def parse_stability_measurement(data: dict, stability: dict) -> dict:
    """
    Maps the JSON data to the Stability measurement schema.
    """

    # Check if list of stability measurements exists
    if 'stability_measurements' not in data['measurements']:
        data['measurements']['stability_measurements'] = []

    # Conditions
    conditions = None  # TODO: Check if this can be extracted from the JSON

    # Stability measurement
    data['measurements']['stability_measurements'].append(
        {
            'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.measurements.StabilityMeasurement',
            'certified': search('is_certified', stability),
            'subcell_association': map_subcell_association(
                search('measurement_done_on', stability)
            )
            or 0,
            'conditions': conditions,
            'results': {
                'm_def': 'perovskite_solar_cell_database.schema_packages.tandem.measurements.StabilityResults',
                'power_conversion_efficiency_initial': convert_to_fraction(
                    search('PCE_at_start', stability)
                ),
                'power_conversion_efficiency_final': convert_to_fraction(
                    search('PCE_at_end', stability)
                ),
                'burn_in_observed': search('burn_in_period_observed', stability),
                'time_until_pce_95': search('T95', stability),
                'time_after_burn_in_until_pce_95': search('T95s', stability),
                'time_until_pce_80': search('T80', stability),
                'time_after_burn_in_until_pce_80': search('T80s', stability),
                'power_conversion_efficiency_after_1000h': convert_to_fraction(
                    search('PCE_1000h', stability)
                ),
            },
        }
    )

    return data
