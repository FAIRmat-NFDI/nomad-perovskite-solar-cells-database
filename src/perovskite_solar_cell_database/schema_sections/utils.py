import numpy as np
from nomad.datamodel.metainfo.common import ProvenanceTracker
from nomad.datamodel.results import (
    BandGap,
    BandGapDeprecated,
    BandStructureElectronic,
    ElectronicProperties,
    OptoelectronicProperties,
    Properties,
    Results,
    SolarCell,
)

# from nomad.datamodel.metainfo.plot import PlotSection
from nomad.units import ureg


def add_band_gap(archive, band_gap):
    """Adds a band gap value (in eV) with the additional section structure for solar
    cell data.eV=
    """
    if band_gap is not None:
        bg = BandGapDeprecated(value=np.float64(band_gap) * ureg('eV'))
        band_gap = BandGap(
            value=np.float64(band_gap) * ureg('eV'),
            provenance=ProvenanceTracker(label='solar_cell_database'),
        )  # TODO: check label
        band_structure = BandStructureElectronic(
            band_gap=[bg]
        )  # TODO: to be removed after reparsing
        electronic = ElectronicProperties(
            band_structure_electronic=[band_structure], band_gap=[band_gap]
        )
        archive.results.properties.electronic = electronic


def add_solar_cell(archive):
    """Adds metainfo structure for solar cell data."""
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
