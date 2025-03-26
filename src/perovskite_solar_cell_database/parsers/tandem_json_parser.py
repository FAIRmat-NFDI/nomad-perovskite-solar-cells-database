import os
from typing import TYPE_CHECKING

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

import json


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

        # entry_archive = EntryArchive()
        # entry_archive.data = tandem

        # create_archive(
        #     entry_archive.m_to_dict(),
        #     archive.m_context,
        #     'tandem' + '.archive.json',
        #     # os.path.splitext(filename)[0] + '.archive.json',
        #     'json',
        #     logger,
        # )


def map_json_to_schema(source: dict) -> dict:
    """
    Maps the JSON data to the PerovskiteTandemSolarCell schema.
    """

    from jmespath import search

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


def update_perovskite_layer(layer: dict, lay: dict) -> dict:
    """
    Maps the JSON data to the Perovskite layer schema.
    """

    layer['m_def'] = (
        'perovskite_solar_cell_database.schema_packages.tandem.tandem.PerovskiteLayer'
    )

    return layer


def update_CIGS_layer(layer: dict, lay: dict) -> dict:
    """
    Maps the JSON data to the CIGS layer schema.
    """

    layer['m_def'] = (
        'perovskite_solar_cell_database.schema_packages.tandem.tandem.ChalcopyriteLayer'
    )

    return layer


def update_silicon_layer(layer: dict, lay: dict) -> dict:
    """
    Maps the JSON data to the Silicon layer schema.
    """

    layer['m_def'] = (
        'perovskite_solar_cell_database.schema_packages.tandem.tandem.SiliconLayer'
    )

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
