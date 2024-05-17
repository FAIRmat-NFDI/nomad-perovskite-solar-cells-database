import numpy as np
from nomad.datamodel.data import ArchiveSection
from nomad.datamodel.metainfo.plot import PlotSection
from nomad.metainfo import Quantity, Section, SubSection
from nomad.units import ureg

from .utils import add_solar_cell


class JVcurve(PlotSection, ArchiveSection):
    """
    Section describing a current density, voltage curve.
    """

    m_def = Section(
        label_quantity='cell_name',
        a_plotly_graph_object=[
            {'data': {'x': '#voltage', 'y': '#current_density'}},
            {'data': {'x': '#voltage', 'y': '#current_density'}},
        ],
    )

    def derive_n_values(self):
        if self.current_density is not None:
            return len(self.current_density)
        if self.voltage is not None:
            return len(self.voltage)
        else:
            return 0

    n_values = Quantity(type=int, derived=derive_n_values)

    cell_name = Quantity(
        type=str,
        shape=[],
        description='Cell identification name.',
        a_eln=dict(component='StringEditQuantity'),
    )

    current_density = Quantity(
        type=np.dtype(np.float64),
        shape=['n_values'],
        unit='mA/cm^2',
        description='Current density array of the *JV* curve.',
    )

    voltage = Quantity(
        type=np.dtype(np.float64),
        shape=['n_values'],
        unit='V',
        description='Voltage array of the of the *JV* curve.',
    )


class JV(ArchiveSection):
    """
    This section descirbes the current density *J* and voltage *V* characteristics
    of the solar cell. It includes the device parameters and information about how the
    measurements were performed.
    """

    data_file = Quantity(
        type=str,
        a_eln=dict(component='FileEditQuantity'),
        a_browser=dict(adaptor='RawFileAdaptor'),
    )

    measured = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if IV-data has been measured and is reported.
                    """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    average_over_n_number_of_cells = Quantity(
        type=np.dtype(np.int64),
        shape=[],
        description="""
    The number of cells the reported IV data is based on.
- The preferred way to enter data is to give every individual cell its own entry in the data template/data base. If that is done, the data is an average over 1 cell.
- If the reported IV data is not the data from one individual cell, but an average over N cells. Give the number of cells.
- If the reported value is an average, but it is unknown over how many cells the value has been averaged (and no good estimate is available), state the number of cells as 2, which is the smallest number of cells that qualifies for an averaging procedure.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    certified_values = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if the IV data is measured by an independent and certification institute. If your solar simulator is calibrated by a calibrated reference diode, that does not count as a certified result.
                    """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    certification_institute = Quantity(
        type=str,
        shape=[],
        description="""
    The name of the certification institute that has measured the certified device.
Example:
Newport
NIM, National Institute of Metrology of China
KIER, Korea Institute of Energy Research
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    'National Institute ofMetrology, China',
                    'Quality supervision＆Testing Center of Chemical＆Physical Power Sources of Information Industry',
                    'CREST, Photovoltaic Meaasurement and calibration Laboratory at Universit of Loughborough',
                    'Photovoltaic and Wind Power Systems Quality Test Center, Chinese Academy of Sciences',
                    'NREL',
                    'Institute of Metrology (NIM) of China',
                    'PVEVL, National Central University, Taiwan',
                    'NIM, National Institute of Metrology of China',
                    'Fraunhofer ISE',
                    'SIMIT, Shanghai Institute of Microsystem and Information Technology',
                    'Newport',
                    'CSIRO, PV Performance Lab at Monash University',
                    'AIST, National Institute of Advanced Industrial Science and Technology',
                    'CPVT, National Center of Supervision and Inspection on Solar Photovoltaic Products Quality of China',
                    'KIER, Korea Institute of Energy Research',
                    'Newport Corporation',
                    'Solar Power Lab at Arizona State University',
                ]
            ),
        ),
    )

    storage_age_of_cell = Quantity(
        type=str,
        shape=[],
        description="""
    The age of the cell with respect to when the last deposition step was finalised.
- If there are uncertainties, only state the best estimate, e.g. write 3 and not 1-5.
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '1.0',
                    'Unknown',
                    '7.0',
                    '4.0',
                    '2.0',
                    '28.0',
                    '58.0',
                    '8.0',
                    '0.01',
                    '0.5',
                    '5.0',
                    '6.0',
                ]
            ),
        ),
    )

    storage_atmosphere = Quantity(
        type=str,
        shape=[],
        description="""
    The atmosphere in which the sample was stored between the device finalisation and the IV measurement.
- If the atmosphere is a mixture of different gases, e.g. A and B, list the gases in alphabetic order and separate them with semicolons, as in (A; B)
- “Dry air” represent air with low relative humidity but where the relative humidity is not known
- “Ambient” represent air where the relative humidity is not known. For ambient conditions where the relative humidity is known, state this as “Air”
- “Vacuum” (of unspecified pressure) is for this purpose considered as an atmospheric gas
- If the atmosphere has changed during the storing time, separate the different atmospheres by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- This category was included after the projects initial phase wherefor the list of reported categories is
short. Thus, be prepared to expand the given list of alternatives in the data template.
Example
N2
Air
N2 >> Air
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=['Dry air', 'Unknown', 'Air', 'Ambient', 'N2', 'Vacuum']
            ),
        ),
    )

    storage_relative_humidity = Quantity(
        type=str,
        shape=[],
        description="""
    The relative humidity in the atmosphere in which the sample was stored between the device finalisation and the IV measurement.
- If the relative humidity has changed during the storing time, separate the different relative humidity by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If the relative humidity is not known, stat that as ‘nan’
- For values with uncertainties, state the best estimate, e.g. write 35 and not 30-40.
Example
35
0
0 >> 25
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=['', '0.9', '65.0', '5.0']),
        ),
    )

    test_atmosphere = Quantity(
        type=str,
        shape=[],
        description="""
    The atmosphere in which the IV measurement is conducted
- If the atmosphere is a mixture of different gases, e.g. A and B, list the gases in alphabetic order and separate them with semicolons, as in (A; B)
- “Dry air” represent air with low relative humidity but where the relative humidity is not known
- “Ambient” represent air where the relative humidity is not known. For ambient conditions where the relative humidity is known, state this as “Air”
- “Vacuum” (of unspecified pressure) is for this purpose considered as an atmospheric gas
Example
Air
N2
Vacuum
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'Water',
                    'Dry air',
                    'Unknown',
                    'Air',
                    'Ambient',
                    'Outdoor',
                    'N2',
                    'Vacuum',
                    'Ar',
                    'Near-space',
                ]
            ),
        ),
    )

    test_relative_humidity = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description="""
    The relive humidity in which the IV measurement is conducted
- If there are uncertainties, only state the best estimate, e.g write 35 and not 20-50.
- If the relative humidity is not known, stat that as ‘nan’
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    test_temperature = Quantity(
        type=np.dtype(np.float64),
        unit=('celsius'),
        shape=[],
        description="""
    The temperature of the device during the IV-measurement
- If the temperature is not controlled and not is known, assume a standard room temperature of 25°C.
- If there are uncertainties, only state the best estimate, e.g write 35 and not 20-50.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    light_source_type = Quantity(
        type=str,
        shape=[],
        description="""
    The type of light source used during the IV-measurement
- This category was included after the projects initial phase wherefor the list of reported categories is
short. Thus, be prepared to expand the given list of alternatives in the data template.
- The category Solar simulator should only be used when you do not really know which type of light source you have in your solar simulator.
Example:
Laser
Metal halide
Outdoor
Solar simulator
Sulfur plasma
White LED
Xenon plasma
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    'Unknown',
                    'White LED',
                    'Solar Simulator',
                    'Fluorescent lamp',
                    'Solar simulator',
                    'solar simulator',
                    'Laser',
                    'Xenon',
                ]
            ),
        ),
    )

    light_source_brand_name = Quantity(
        type=str,
        shape=[],
        description="""
    The brand name and model number of the light source/solar simulator used
- This category was included after the projects initial phase wherefor the list of reported categories is
short. Thus, be prepared to expand the given list of alternatives in the data template.
Example:
Newport model 91192
Newport AAA
Atlas suntest
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    'EC-lab T-5A',
                    'ABET 11000',
                    'Wavelabs',
                    'ABET Technologies 10500',
                    'Newport model 94023A-U',
                    'McScience K3000',
                    'BOS-X-1000G',
                    'Solar light 16S-300',
                    'Enlitech',
                    'Newport, model 94063A',
                    'Wacom Denso model WXS-155S-10',
                    'Sciencetech Inc. SS-150',
                    'WAVELABS SINUS-70 LED',
                    'Oriel Sol2ATM',
                    'Newport model 91195A',
                    'Newport ORIEL LCS100',
                    'Oriel 91160',
                    'Newport Verasol',
                    'Solar IV-150A, Zolix',
                    'WAVELABS SINUS-220',
                    'Newport 91195A',
                    'San-ei Electric XES-301S',
                    'Newport model 94043A',
                    'Cree XML T6',
                    'Bunkoukeiki CEP-2000SRR',
                    'Peccell Technologies PEC-L01',
                    'XES-70S1',
                    'Sciencetech',
                    'Oriel 91160A',
                    'Oriel VeraSol-2',
                    'CEP-2000SRR, Bunkou-Keiki Inc',
                    'Zolix SS150A',
                    'SANEI',
                    'PET Photo Emission Tech Inc. Model SS',
                    'Enlitech SS-F7-3A',
                    'Newport 91160',
                    'ABET Technology Sun 2000',
                    'Oriel 9119',
                    'Peccell PEC-L01',
                    'Bunkoukeiki BSS-150T',
                    'Enlitech SS-F5',
                    'Global (G)',
                    'Wacom WXs-156s-l2',
                    'Photo Emission Tech Inc SS150',
                    'Newport Oriel LCS-100',
                    'Oriel 92251A',
                    'Newport 94123A',
                    'Oriel 94023 A',
                    'Newport model 94023A',
                    'Newport Oriel 92192',
                    'Newport model 94022',
                    'Bunkoukeiki KHP-1',
                    'YAMASHITA DENSO model YSS-150A',
                    'Oriel 300',
                    'Newport AAA',
                    'KHP-1, Bunko-Keiki, Japan',
                    'Spectra-Nova',
                    'Sol3A, Oriel Instruments',
                    'Abet Technologies Sun 3000',
                    'IV5, PV Measurements, Inc., USA',
                    'Newport Oriel PVIV-201 V',
                    'Photo Emission Tech.',
                    'Newport model 91192',
                    'XES-40S1, SAN-E1',
                    'San-ei Electric',
                    'Oriel 92251A-1000',
                    'Newport Oriel 94043A',
                    'So13A',
                    'Newport Oriel Sol3A',
                    'ABET Sun 3000',
                    'KHS Steuernagel',
                    'Zolix Sirius-SS',
                    'Oriel 81172',
                    'PV Measurements Inc.',
                    'Oriel',
                    'XEF-300',
                    'Oriel Sol3A',
                    'Peceell PEC-L01',
                    'Ushio Optical ModuleX',
                    'Newport Oriel 96000',
                    'Oriel 94023A',
                    'McScience K401',
                    'Newport Oriel 3A',
                    '94011A-ES Sol',
                    'Bunkoukeiki CEP-25ML',
                    'Newport 6279 NS',
                    'Sharif Solar 10–2',
                    'SAN-EI (XES-50S1)',
                    'Enlitech SS-F5-3A',
                    'ScienceTech model SF-150',
                    'Newport Oriel',
                    'Newport Oriel Sol2A',
                    'Batsol PEC-L01',
                ]
            ),
        ),
    )

    light_source_simulator_class = Quantity(
        type=str,
        shape=[],
        description="""
    The class of the solar simulator
- A three-letter code of As, Bs, and Cs. The order of the letters represents the quality ofspectral match, spatial non-uniformity, and temporal instability
Example
AAA
ABB
CAB
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=['', 'ABB', 'A', 'AAA', 'ABA', 'AAB']),
        ),
    )

    light_intensity = Quantity(
        type=np.dtype(np.float64),
        unit=('mW/cm**2'),
        shape=[],
        description="""
    The light intensity during the IV measurement
- If there are uncertainties, only state the best estimate, e.g. write 100 and not 90-100.
- Standard AM 1.5 illumination correspond to 100 mW/cm2
- If you need to convert from illumination given in lux; at 550 nm, 1 mW/cm2 corresponds to 6830 lux. Be aware that the conversion change with the spectrum used. As a rule of thumb for general fluorescent/LED light sources, around 0.31mW corresponded to 1000 lux. If your light intensity is measured in lux, it probably means that your light spectra deviates quite a lot from AM 1.5, wherefore it is very important that you also specify the light spectra in the next column.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    light_spectra = Quantity(
        type=str,
        shape=[],
        description="""
    The light spectrum used (or simulated as best as possible) during the IV measurement
Example
AM 1.0
AM 1.5
Indoor light
Monochromatic
Outdoor
UV
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=['', 'Indoor light', 'AM 1.5', 'Monochromatic', 'Am 1.5']
            ),
        ),
    )

    light_wavelength_range = Quantity(
        type=str,
        shape=[],
        description="""
    The wavelength range of the light source
- Separate the lower and upper bound by a semicolon.
- For monochromatic light sources, only give the constant value.
- If there are uncertainties, only state the best estimate, e.g. write 100 and not 90-100.
- State unknown values as ‘nan’
Example:
330; 1000
400; nan
550
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=['nan; nan', '250; 1200']),
        ),
    )

    light_illumination_direction = Quantity(
        type=str,
        shape=[],
        description="""
    The direction of the illumination with respect to the device stack
- If the cell is illuminated trough the substrate, state this as ‘Substrate’
- If the cell is illuminated trough the top contact, state this as ‘Superstrate’
- For back contacted cells illuminated from the non-contacted side, state this as ‘Superstrate’
Example
Substrate
Superstrate
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=['', 'Superstrate', 'Substrate']),
        ),
    )

    light_masked_cell = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if the cell is illuminated trough a mask with an opening that is smaller than the total cell area.
                    """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    light_mask_area = Quantity(
        type=np.dtype(np.float64),
        unit=('cm**2'),
        shape=[],
        description="""
    The area of the opening in the mask trough with the cell is illuminated (if there is a mask)
- If there are uncertainties, only state the best estimate, e.g. write 100 and not 90-100.
- If there is no light mask, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    scan_speed = Quantity(
        type=np.dtype(np.float64),
        unit=('mV/s'),
        shape=[],
        description="""
    The speed of the potential sweep during the IV measurement
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    scan_delay_time = Quantity(
        type=np.dtype(np.float64),
        unit=('ms'),
        shape=[],
        description="""
    The time at each potential value before integration in the potential sweep.
- For some potentiostats you need to specify this value, whereas for others it is set automatically and is not directly accessible.
- If there are uncertainties, only state the best estimate, e.g. write 100 and not 90-100.
- If unknown, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    scan_integration_time = Quantity(
        type=np.dtype(np.float64),
        unit=('ms'),
        shape=[],
        description="""
    The integration time at each potential value in the potential sweep.
- For some potentiostats you need to specify this value, whereas for others it is set automatically and is not directly accessible.
- If there are uncertainties, only state the best estimate, e.g. write 100 and not 90-100.
- If unknown, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    scan_voltage_step = Quantity(
        type=np.dtype(np.float64),
        unit=('mV'),
        shape=[],
        description="""
    The distance between the measurement point in the potential sweep
- If unknown, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    preconditioning_protocol = Quantity(
        type=str,
        shape=[],
        description="""
    Any preconditioning protocol done immediately before the IV measurement
- If no preconditioning was done, state this as ‘none’
- If more than one preconditioning protocol was conducted in parallel, separate them with semicolons
- If more than one preconditioning protocol was conducted in sequence, separate them by a double forward angel bracket (‘ >> ‘)
Example
Cooling
Heeting
Light soaking
Light soaking; Potential biasing
Potential biasing
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    'Light soaking',
                    'Potential biasing',
                    'Heating',
                    'Unknown',
                    'MPPT',
                    'Voc stabilization',
                    'Bending',
                    'Light Soaking',
                    'Light Soaking; Potential biasing',
                    'Electroluminescence measurement',
                    'Light soaking; Potential biasing',
                    'Heating; Light soaking',
                    'Light soaking; Potential cykling',
                    'Cooling',
                ]
            ),
        ),
    )

    preconditioning_time = Quantity(
        type=np.dtype(np.float64),
        unit=('s'),
        shape=[],
        description="""
    The duration of the preconditioning protocol
- If there are uncertainties, only state the best estimate, e.g. write 100 and not 90-100.
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    preconditioning_potential = Quantity(
        type=np.dtype(np.float64),
        unit=('V'),
        shape=[],
        description="""
    The potential at any potential biasing step
- If there are uncertainties, only state the best estimate, e.g. write 100 and not 90-100.
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    preconditioning_light_intensity = Quantity(
        type=np.dtype(np.float64),
        unit=('mW/cm**2'),
        shape=[],
        description="""
    The light intensity at any light soaking step
- If there are uncertainties, only state the best estimate, e.g. write 100 and not 90-100.
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    reverse_scan_Voc = Quantity(
        type=np.dtype(np.float64),
        unit='V',
        shape=[],
        description="""
    The open circuit potential, Voc, at the reverse voltage sweep (when U scanned from Voc to 0)
- Give Voc in volts [V]
- If there are uncertainties, only state the best estimate, e.g. write 1.03 and not 1.01-1.05
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    reverse_scan_Jsc = Quantity(
        type=np.dtype(np.float64),
        unit='mA / cm**2',
        shape=[],
        description="""
    The short circuit current, Jsc, at the reverse voltage sweep (when U scanned from Voc to 0)
- Give Jsc in mA/cm2
- If there are uncertainties, only state the best estimate, e.g. write 20.5 and not 19-20
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    reverse_scan_FF = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description="""
    The fill factor, FF, at the reverse voltage sweep (when U scanned from Voc to 0)
- Give FF as the ratio between Vmp*Jmp/(Voc*Jsc) which gives it a value between 0 and 1
- If there are uncertainties, only state the best estimate, e.g. write 0.73 and not 0.7-0.76
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    reverse_scan_PCE = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description="""
    The efficiency, PCE, at the reverse voltage sweep (when U scanned from Voc to 0)
- Give the efficiency in %
- If there are uncertainties, only state the best estimate, e.g. write 20.5 and not 19-20
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    reverse_scan_Vmp = Quantity(
        type=np.dtype(np.float64),
        unit='V',
        shape=[],
        description="""
    The potential at the maximum power point, Vmp, at the reverse voltage sweep (when U scanned from Voc to 0)
- Give Vmp in volts [V]
- If there are uncertainties, only state the best estimate, e.g. write 1.03 and not 1.01-1.05
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    reverse_scan_Jmp = Quantity(
        type=np.dtype(np.float64),
        unit='mA / cm**2',
        shape=[],
        description="""
    The current density at the maximum power point, Jmp, at the reverse voltage sweep (when U scanned from Voc to 0)
- Give Jmp in mA/cm2
- If there are uncertainties, only state the best estimate, e.g. write 20.5 and not 19-20
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    reverse_scan_series_resistance = Quantity(
        type=np.dtype(np.float64),
        unit='ohm*cm**2',
        shape=[],
        description="""
    The series resistance as extracted from the reverse voltage sweep (when U scanned from Voc to 0)
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    reverse_scan_shunt_resistance = Quantity(
        type=np.dtype(np.float64),
        unit='ohm*cm**2',
        shape=[],
        description="""
    The shunt resistance as extracted from the reverse voltage sweep (when U scanned from Voc to 0)
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    forward_scan_Voc = Quantity(
        type=np.dtype(np.float64),
        unit='V',
        shape=[],
        description="""
    The open circuit potential, Voc, at the forward voltage sweep (when U scanned from 0 to Voc)
- Give Voc in volts [V]
- If there are uncertainties, only state the best estimate, e.g. write 1.03 and not 1.01-1.05
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    forward_scan_Jsc = Quantity(
        type=np.dtype(np.float64),
        unit='mA / cm**2',
        shape=[],
        description="""
    The short circuit current, Jsc, at the forward voltage sweep (when U scanned from 0 to Voc)
- Give Jsc in mA/cm2
- If there are uncertainties, only state the best estimate, e.g. write 20.5 and not 19-20
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    forward_scan_FF = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description="""
    The fill factor, FF, at the forward voltage sweep (when U scanned from 0 to Voc)
- Give FF as the ratio between Vmp*Jmp/(Voc*Jsc) which gives it a value between 0 and 1
- If there are uncertainties, only state the best estimate, e.g. write 0.73 and not 0.7-0.76
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    forward_scan_PCE = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description="""
    The efficiency, PCE, at the forward voltage sweep (when U scanned from 0 to Voc)
- Give the efficiency in %
- If there are uncertainties, only state the best estimate, e.g. write 20.5 and not 19-20
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    forward_scan_Vmp = Quantity(
        type=np.dtype(np.float64),
        unit='V',
        shape=[],
        description="""
    The potential at the maximum power point, Vmp, at the forward voltage sweep (when U scanned from 0 to Voc)
- Give Vmp in volts [V]
- If there are uncertainties, only state the best estimate, e.g. write 1.03 and not 1.01-1.05
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    forward_scan_Jmp = Quantity(
        type=np.dtype(np.float64),
        unit='mA / cm**2',
        shape=[],
        description="""
    The current density at the maximum power point, Jmp, at the forward voltage sweep (when U scanned from 0 to Voc)
- Give Jmp in mA/cm2
- If there are uncertainties, only state the best estimate, e.g. write 20.5 and not 19-20
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    forward_scan_series_resistance = Quantity(
        type=np.dtype(np.float64),
        unit='ohm*cm**2',
        shape=[],
        description="""
    The series resistance as extracted from the forward voltage sweep (when U scanned from 0 to Voc)
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    forward_scan_shunt_resistance = Quantity(
        type=np.dtype(np.float64),
        unit='ohm*cm**2',
        shape=[],
        description="""
    The shunt resistance as extracted from the forward voltage sweep (when U scanned from 0 to Voc)
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    link_raw_data = Quantity(
        type=str,
        shape=[],
        description="""
    A link to where the data file for the IV-data is stored
- This is a beta feature. The plan is to create a file repository where the raw files for IV data can be stored and disseminated. With the link and associated protocols, it should be possible to programmatically access and analyse the raw IV-data.
                    """,
    )

    default_Voc = Quantity(
        type=np.dtype(np.float64),
        unit='V',
        shape=[],
        description="""
    Open circuit voltage.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    default_Jsc = Quantity(
        type=np.dtype(np.float64),
        unit='mA / cm**2',
        shape=[],
        description="""
    Short circuit current density.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    default_FF = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description="""
    Fill factor.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    default_PCE = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description="""
    Power conversion efficiency.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    default_Voc_scan_direction = Quantity(
        type=str,
        shape=[],
        description="""
    nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=['Reversed', '', 'Forward']),
        ),
    )

    default_Jsc_scan_direction = Quantity(
        type=str,
        shape=[],
        description="""
    nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=['Reversed', '', 'Forward']),
        ),
    )

    default_FF_scan_direction = Quantity(
        type=str,
        shape=[],
        description="""
    nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=['Reversed', '', 'Forward']),
        ),
    )

    default_PCE_scan_direction = Quantity(
        type=str,
        shape=[],
        description="""
    nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=['Reversed', '', 'Stabilised', 'Forward']),
        ),
    )

    hysteresis_index = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description="""
    nan
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    jv_curve = SubSection(section_def=JVcurve, repeats=True)

    def normalize(self, archive, logger):
        from perovskite_solar_cell_database.data_tools import jv_dict_generator

        if self.data_file:
            with archive.m_context.raw_file(self.data_file) as f:
                jv_dict = jv_dict_generator(f.name)
                self.measured = True
                self.average_over_n_number_of_cells = jv_dict['no_cells']
                self.light_mask_area = jv_dict['active_area']
                self.light_intensity = jv_dict['intensity']
                self.scan_integration_time = jv_dict['integration_time']
                self.preconditioning_time = jv_dict['settling_time']

                self.reverse_scan_Jsc = round(jv_dict['reverse_scan_Jsc'], 2) * ureg(
                    'mA / cm^2'
                )
                self.reverse_scan_Voc = round(jv_dict['reverse_scan_Voc'], 2) * ureg(
                    'V'
                )
                self.reverse_scan_FF = round(jv_dict['reverse_scan_FF'], 2) * 0.01
                self.reverse_scan_PCE = round(jv_dict['reverse_scan_PCE'], 2)
                self.reverse_scan_Vmp = round(jv_dict['reverse_scan_Vmp'], 2) * ureg(
                    'V'
                )
                self.reverse_scan_Jmp = round(jv_dict['reverse_scan_Jmp'], 2) * ureg(
                    'mA / cm^2'
                )
                self.reverse_scan_series_resistance = round(
                    jv_dict['reverse_scan_series_resistance'], 2
                ) * ureg('ohm * cm^2')
                self.reverse_scan_shunt_resistance = round(
                    jv_dict['reverse_scan_shunt_resistance'], 2
                ) * ureg('ohm * cm^2')

                self.forward_scan_Jsc = round(jv_dict['forward_scan_Jsc'], 2) * ureg(
                    'mA / cm^2'
                )
                self.forward_scan_Voc = round(jv_dict['forward_scan_Voc'], 3) * ureg(
                    'V'
                )
                self.forward_scan_FF = round(jv_dict['forward_scan_FF'], 2) * 0.01
                self.forward_scan_PCE = round(jv_dict['forward_scan_PCE'], 2)
                self.forward_scan_Vmp = round(jv_dict['forward_scan_Vmp'], 3) * ureg(
                    'V'
                )
                self.forward_scan_Jmp = round(jv_dict['forward_scan_Jmp'], 2) * ureg(
                    'mA / cm^2'
                )
                self.forward_scan_series_resistance = round(
                    jv_dict['forward_scan_series_resistance'], 3
                ) * ureg('ohm * cm^2')
                self.forward_scan_shunt_resistance = round(
                    jv_dict['forward_scan_shunt_resistance'], 3
                ) * ureg('ohm * cm^2')

                self.default_Jsc = round(
                    jv_dict['default_Jsc'], 2
                )  # * ureg('milliampere / centimeter ** 2')
                self.default_Voc = round(jv_dict['default_Voc'], 2) * ureg('V')
                self.default_FF = round(jv_dict['default_FF'], 2) * 0.01
                self.default_PCE = round(jv_dict['default_PCE'], 2)
                self.default_Voc_scan_direction = jv_dict['default_Voc_scan_direction']
                self.default_Jsc_scan_direction = jv_dict['default_Jsc_scan_direction']
                self.default_FF_scan_direction = jv_dict['default_FF_scan_direction']
                self.default_PCE_scan_direction = jv_dict['default_PCE_scan_direction']

                self.jv_curve = []
                for curve in range(len(jv_dict['jv_curve'])):
                    jv_set = JVcurve(
                        cell_name=jv_dict['jv_curve'][curve]['name'],
                        voltage=jv_dict['jv_curve'][curve]['voltage'],
                        current_density=jv_dict['jv_curve'][curve]['current_density'],
                    )
                    self.jv_curve.append(jv_set)

        add_solar_cell(archive)
        if self.default_Voc is not None:
            archive.results.properties.optoelectronic.solar_cell.open_circuit_voltage = self.default_Voc
        if self.default_Jsc is not None:
            archive.results.properties.optoelectronic.solar_cell.short_circuit_current_density = self.default_Jsc
        if self.default_FF is not None:
            archive.results.properties.optoelectronic.solar_cell.fill_factor = (
                self.default_FF
            )
        if self.default_PCE is not None:
            archive.results.properties.optoelectronic.solar_cell.efficiency = (
                self.default_PCE
            )
        if self.light_intensity is not None:
            archive.results.properties.optoelectronic.solar_cell.illumination_intensity = self.light_intensity
