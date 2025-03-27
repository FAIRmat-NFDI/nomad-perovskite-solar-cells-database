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

        # Append layer to layer stack
        data['layer_stack'].append(layer)

    # Measurements

    return data


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
