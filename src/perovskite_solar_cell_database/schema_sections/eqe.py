import numpy as np
from nomad.datamodel.data import ArchiveSection
from nomad.datamodel.metainfo.plot import PlotSection
from nomad.metainfo import Quantity, Section
from nomad.units import ureg

from .perovskite import Perovskite


class EQE(PlotSection, ArchiveSection):
    """
    A section describing the External Quantum Efficiency **EQE** of the solar cell
    and additional parameteres derived from it. If used as an ELN, a file containing
    the EQE spectrum in columns can be uploaded in the quantity `data_file` to process
    automatic calculations of several parameteres like the `bandgap` or `Urbach energy`.
    """

    m_def = Section(
        a_eln=dict(lane_width='600px'),
        a_plotly_graph_object=[
            {
                'data': {'x': '#raw_wavelength_array', 'y': '#raw_eqe_array'},
                'layout': {'label': {'text': 'Raw EQE'}, 'yaxis': {'type': 'lin'}},
            },
            {
                'data': {'x': '#wavelength_array', 'y': '#eqe_array'},
                'layout': {
                    'label': {'text': 'Interpolated/extrapolated EQE log scale'},
                    'yaxis': {'type': 'log'},
                },
                'config': {'editable': 'true'},
            },
            {'data': {'x': '#photon_energy_array', 'y': '#raw_eqe_array'}},
            {'data': {'x': '#raw_photon_energy_array', 'y': '#raw_eqe_array'}},
            {'data': {'x': '#raw_wavelength_array', 'y': '#raw_eqe_array'}},
            {'data': {'x': '#photon_energy_array', 'y': '#eqe_array'}},
            {'data': {'x': '#wavelength_array', 'y': '#eqe_array'}},
            {'data': {'x': '#photon_energy_array', 'y': '#eqe_array'}},
        ],
    )

    eqe_data_file = Quantity(
        type=str,
        description="""
    eqe_array = Quantity(
        type=np.dtype(np.float64), shape=['n_values'],
                    Drop here your eqe file and click save for processing.
                    """,
        a_eln=dict(component='FileEditQuantity'),
        a_browser=dict(adaptor='RawFileAdaptor'),
    )

    header_lines = Quantity(
        type=np.dtype(np.int64),
        default=0,
        description="""
                    Number of header lines in the file.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    measured = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if the external quantum efficiency has been measured
                    """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    light_bias = Quantity(
        type=np.dtype(np.float64),
        unit=('mW/cm**2'),
        shape=[],
        description="""
    The light intensity of any bias light during the EQE measurement
- If there are uncertainties, only state the best estimate, e.g. write 100 and not 90-100.
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    bandgap_eqe = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='eV',
        description="""
    Bandgap derived form the eqe in eV.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    integrated_Jsc = Quantity(
        type=np.dtype(np.float64),
        unit='mA / cm**2',
        shape=[],
        description="""
    The integrated current from the EQE measurement
- Give Jsc in mA/cm2
- If there are uncertainties, only state the best estimate, e.g. write 20.5 and not 19-20
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    integrated_J0rad = Quantity(
        type=np.dtype(np.float64),
        unit='mA / cm**2',
        shape=[],
        description="""
    The integrated J<sub>{0, Rad}</sub> from the EQE measurement
- Give J<sub>{0, Rad}</sub> in mA/cm2
- If there are uncertainties, only state the best estimate, e.g. write 20.5 and not 19-20
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    voc_rad = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='V',
        description="""
    Radiative V<sub>oc</sub> derived from the eqe in V.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    urbach_energy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='eV',
        description="""
    Urbach energy fitted from the eqe in eV.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    def derive_n_values(self):
        if self.eqe_array is not None:
            return len(self.eqe_array)
        if self.photon_energy_array is not None:
            return len(self.photon_energy_array)
        else:
            return 0

    n_values = Quantity(type=int, derived=derive_n_values)

    def derive_n_raw_values(self):
        if self.raw_eqe_array is not None:
            return len(self.raw_eqe_array)
        if self.raw_photon_energy_array is not None:
            return len(self.raw_photon_energy_array)
        else:
            return 0

    n_raw_values = Quantity(type=int, derived=derive_n_raw_values)

    raw_eqe_array = Quantity(
        type=np.dtype(np.float64),
        shape=['n_raw_values'],
        description='EQE array of the spectrum',
    )

    raw_photon_energy_array = Quantity(
        type=np.dtype(np.float64),
        shape=['n_raw_values'],
        unit='eV',
        description='Raw Photon energy array of the eqe spectrum',
    )

    raw_wavelength_array = Quantity(
        type=np.dtype(np.float64),
        shape=['n_raw_values'],
        unit='nanometer',
        description='Raw wavelength array of the eqe spectrum',
    )

    eqe_array = Quantity(
        type=np.dtype(np.float64),
        shape=['n_values'],
        description='EQE array of the spectrum',
    )

    wavelength_array = Quantity(
        type=np.dtype(np.float64),
        shape=['n_values'],
        unit='nanometer',
        description='Interpolated/extrapolated wavelength array with *E<sub>u</sub>* of the eqe spectrum ',
    )

    photon_energy_array = Quantity(
        type=np.dtype(np.float64),
        shape=['n_values'],
        unit='eV',
        description='Interpolated/extrapolated photon energy array with a *E<sub>u</sub>*  of the eqe spectrum',
    )

    link_raw_data = Quantity(
        type=str,
        shape=[],
        description="""
    A link to where the data file for the EQE measurement is stored
- This is a beta feature. The plan is to create a file repository where the raw files for IV data can be stored and disseminated. With the link and associated protocols, it should be possible to programmatically access and analyse the raw IV-data.
                    """,
    )

    def normalize(self, archive, logger):
        from perovskite_solar_cell_database.data_tools import EQEAnalyzer

        if self.eqe_data_file:
            with archive.m_context.raw_file(self.eqe_data_file) as f:
                eqe_dict = EQEAnalyzer(
                    f.name, header_lines=self.header_lines
                ).eqe_dict()
                self.measured = True
                self.bandgap_eqe = eqe_dict['bandgap']
                self.integrated_Jsc = eqe_dict['jsc'] * ureg('A/m**2')
                self.integrated_J0rad = (
                    eqe_dict['j0rad'] * ureg('A/m**2')
                    if 'j0rad' in eqe_dict
                    else logger.warning('The j0rad could not be calculated.')
                )
                self.voc_rad = (
                    eqe_dict['voc_rad']
                    if 'voc_rad' in eqe_dict
                    else logger.warning('The voc_rad could not be calculated.')
                )
                self.urbach_energy = eqe_dict['urbach_e']
                self.photon_energy_array = np.array(
                    eqe_dict['interpolated_photon_energy']
                )
                self.raw_photon_energy_array = np.array(eqe_dict['photon_energy_raw'])
                self.eqe_array = np.array(eqe_dict['interpolated_eqe'])
                self.raw_eqe_array = np.array(eqe_dict['eqe_raw'])
                if archive.data.perovskite is None:
                    archive.data.perovskite = Perovskite()
                archive.data.perovskite.band_gap = str(self.bandgap_eqe.magnitude)
                archive.data.perovskite.band_gap_estimation_basis = 'EQE'

        if self.photon_energy_array is not None:
            self.wavelength_array = self.photon_energy_array.to('nm', 'sp')  # pylint: disable=E1101
            self.raw_wavelength_array = self.raw_photon_energy_array.to('nm', 'sp')  # pylint: disable=E1101
