

import numpy as np
# from nomad.datamodel.metainfo.plot import PlotSection
from nomad.units import ureg
from nomad.datamodel.results import (BandGapDeprecated, BandGap, BandStructureElectronic,
                                     ElectronicProperties, OptoelectronicProperties,
                                     Properties, Results, SolarCell)
from nomad.datamodel.metainfo.common import ProvenanceTracker
from nomad.datamodel.metainfo.common import ProvenanceTracker

def add_band_gap(archive, band_gap):
    '''Adds a band gap value (in eV) with the additional section structure for solar
    cell data.eV=
    '''
    if band_gap is not None:
        bg = BandGapDeprecated(value=np.float64(band_gap) * ureg('eV'))
        band_gap = BandGap(value=np.float64(band_gap) * ureg('eV'),
                           provenance=ProvenanceTracker(label='solar_cell_database'))  # TODO: check label
        band_structure = BandStructureElectronic(band_gap=[bg])  # TODO: to be removed after reparsing
        electronic = ElectronicProperties(band_structure_electronic=[band_structure],
                                          band_gap=[band_gap])
        archive.results.properties.electronic = electronic


def add_solar_cell(archive):
    '''Adds metainfo structure for solar cell data.'''
    if not archive.results:
        archive.results = Results()
    if not archive.results.properties:
        archive.results.properties = Properties()
    if not archive.results.properties.optoelectronic:
        archive.results.properties.optoelectronic = OptoelectronicProperties()
    if not archive.results.properties.optoelectronic.solar_cell:
        archive.results.properties.optoelectronic.solar_cell = SolarCell()

# if __name__ == '__main__':
#     csv_database_path = 'perovskite_database.csv'
#     target_dir = 'perovskite_database'
#     perovskite_entry_writer = PerovskiteEntryWriter(csv_database_path)
#     perovskite_entry_writer.entry_writer(target_dir)


def get_reference(upload_id, entry_id):
    return f'../uploads/{upload_id}/archive/{entry_id}#data'


def get_entry_id_from_file_name(file_name, archive):
    from nomad.utils import hash
    return hash(archive.metadata.upload_id, file_name)


def create_archive(entity, archive, file_name) -> str:
    import json
    from nomad.datamodel.context import ClientContext
    if isinstance(archive.m_context, ClientContext):
        return None
    if not archive.m_context.raw_path_exists(file_name):
        entity_entry = entity.m_to_dict(with_root_def=True)
        with archive.m_context.raw_file(file_name, 'w') as outfile:
            json.dump({"data": entity_entry}, outfile)
        archive.m_context.process_updated_raw_file(file_name)
    return get_reference(
        archive.metadata.upload_id,
        get_entry_id_from_file_name(file_name, archive)
    )
