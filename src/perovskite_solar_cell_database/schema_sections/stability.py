import numpy as np
from nomad.datamodel.data import ArchiveSection
from nomad.metainfo import Quantity


class Stability(ArchiveSection):
    """
    A section decsirbing the stability measurements performed in the device.
    """

    measured = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if some kind of stability measurement has been done.
- There is no sharp boundary between a stability measurement and a measurement of stabilised efficiency. Generally, a measurement under a few minutes is considered as a measurement of stabilised efficiency, whereas a stability measurement is sufficiently long for degradation to be seen (unless the device is really good)
                    """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    protocol = Quantity(
        type=str,
        shape=[],
        description="""
    The stability protocol used for the stability measurement.
- For a more detailed discussion on protocols and standard nomenclature for stability measurements, please see the following paper:
o Consensus statement for stability assessment and reporting for perovskite photovoltaics based on ISOS procedures byM. V. Khenkin et al. Nat. Energ. 2020. DOI10.1038/s41560-019-0529-5
Example:
ISOS-D-1
ISOS-D-1I
ISOS-L-2
ISOS-T-3
IEC 61215
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    'Indoor light',
                    'IEC 61646',
                    'ISOS-L-1',
                    'Bending test',
                    'Other',
                    'ISOS-LC-1',
                    'ISOS-T-1',
                    'ISOS-D-1I',
                    'ISOS-V-2',
                    'ISOS-L-2I',
                    'ISOS-D-1',
                    'IEC 61215',
                    'ISOS-L-C1I',
                    'ISOS‐L‐1',
                    'ISOS-L-3',
                    'ISOS-L-1I',
                    'ISOS-D-2',
                    'ISOS-V-1',
                    'ISOS-L-2',
                    'ISOS‐D‐3',
                    'ISOS-D-2I',
                    'ISOS-D-3',
                    'ISOS-V-1I',
                    'ISOS-O-1',
                    'UV-stability',
                    'ISOS-T-3',
                ]
            ),
        ),
    )

    average_over_n_number_of_cells = Quantity(
        type=np.dtype(np.int64),
        shape=[],
        description="""
    The number of cells the reported stability data is based on.
- The preferred way to enter data is to give every individual cell its own entry in the data template/data base. If that is done, the data is an average over 1 cell.
- If the reported stability data is not the data from one individual cell, but an average over N cells. Give the number of cells.
- If the reported value is an average, but it is unknown over how many cells the value has been averaged (and no good estimate is available), state the number of cells as 2, which is the smallest number of cells that qualifies for an averaging procedure.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    light_source_type = Quantity(
        type=str,
        shape=[],
        description="""
    The type of light source used during the stability measurement
- This category was included after the projects initial phase wherefor the list of reported categories is
short. Thus, be prepared to expand the given list of alternatives in the data template.
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
                    'Indoor light',
                    'Solar Simulator',
                    'UV lamp',
                    'Natural sunlight',
                    'LED',
                    'White Led',
                    'Synchrotron',
                    'Light',
                    'Mercury',
                    'Sulfur plasma',
                    'Halogen',
                    'Tungsten; Gamma rays',
                    'White LED',
                    'Dark',
                    'Solar simulator',
                    'solar simulator',
                    'Sun',
                    'Tungsten',
                    'Xenon',
                    'Fluorescent lamp',
                    'Metal halide',
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[''])),
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[''])),
    )

    light_intensity = Quantity(
        type=np.dtype(np.float64),
        unit=('mW/cm**2'),
        shape=[],
        description="""
    The light intensity during the stability measurement
- If there are uncertainties, only state the best estimate, e.g. write 100 and not 90-100.
- Standard AM 1.5 illumination correspond to 100 mW/cm2
- If you need to convert from illumination given in lux; at 550 nm, 1 mW/cm2 corresponds to 6830 lux
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    light_spectra = Quantity(
        type=str,
        shape=[],
        description="""
    The light spectrum used (or simulated as best as possible) during the stability measurement
- For an unspecified light spectra (that not is dark), state this as ‘Light’
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
                suggestions=[
                    '',
                    'Indoor light',
                    'X-ray, 17.998 keV',
                    'UV',
                    'AM 1.5',
                    'Monochromatic',
                    'Outdoor ligth',
                    'Yellow light',
                    'Am 1.5',
                ]
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
            props=dict(
                suggestions=[
                    'nan; nan',
                    '325; 325',
                    '300; 800',
                    '340.0; 340.0',
                    '365.0; 365.0',
                    '254.0; 254.0',
                    '267.0; 267.0',
                ]
            ),
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
            component='EnumEditQuantity', props=dict(suggestions=['', 'Substrate'])
        ),
    )

    light_load_condition = Quantity(
        type=str,
        shape=[],
        description="""
    The load situation of the illumination during the stability measurement.
- If the illumination is constant during the entire stability measurement, or if the cell is stored in the dark, state this as ‘Constant’.
- If the situation periodically is interrupted by IV-measurements, continue to consider the load condition as constant
- If there is a cycling between dark and light, state this as ‘Cycled’
- If the illumination varies in an uncontrolled way, state this as ‘Uncontrolled’
- This category was included after the projects initial phase wherefor the list of reported categories is
short. Thus, be prepared to expand the given list of alternatives in the data template.
Example:
Constant
Cycled
Day-Night cycle
Uncontrolled
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    'constant',
                    'Uncontrolled',
                    'Cycled',
                    'Day-Night cycle',
                    'Constant',
                ]
            ),
        ),
    )

    light_cycling_times = Quantity(
        type=str,
        shape=[],
        description="""
    If the illumination load is cycled during the stability measurement, state the time in low light followed by the time in high light for the cycling period.
- If not applicable, leave blank
Example
12; 12
6; 10
nan; nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=['Unknown', '0.16; 12.0', '12.0; 12.0', '10.0; 14.0', '0.6']
            ),
        ),
    )

    light_UV_filter = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if a UV-filter of any kind was placed between the illumination source and the device during the stability measurement.
                    """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    potential_bias_load_condition = Quantity(
        type=str,
        shape=[],
        description="""
    The Potentiostatic load condition during the stability measurement
- When the cell is not connected to anything, state this as ‘Open circuit’
Examples:
Constant current
Constant potential
MPPT
Open circuit
Passive resistance
Short circuit
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    'Short circuit',
                    'MPPT',
                    'Open circuit',
                    'Constant potential',
                    'Passive resistance',
                ]
            ),
        ),
    )

    potential_bias_range = Quantity(
        type=str,
        shape=[],
        description="""
    The potential range during the stability measurement
- Separate the lower and upper bound by a semicolon.
- For constant values, state only that value.
- For open circuit conditions, state this as ‘nan’
- If there are uncertainties, only state the best estimate, e.g. write 1 and not 0.90-1.1
- State unknown values as ‘nan’
Example:
0.9; 1.02
1.5
nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '0.9; 0.9',
                    '0.85; 0.85',
                    'nan; nan',
                    '0.8465; 0.8465',
                    '0.47; 0.47',
                    '0.7499; 0.7499',
                    '0.937; 0.937',
                    '1.2; 1.2',
                    '0.65; 0.65',
                    '0.95; 0.95',
                    '0.84; 0.84',
                    '0.71; 0.71',
                    '1.0; 1.0',
                    '0.86; 0.86',
                    '1.413; 1.413',
                    '0.76; 0.76',
                    '0.7; 0.7',
                    '0.908; 0.908',
                    '0.72; 0.72',
                    '0.8; 0.8',
                    '0.89; 0.89',
                ]
            ),
        ),
    )

    potential_bias_passive_resistance = Quantity(
        type=np.dtype(np.float64),
        unit=('ohm'),
        shape=[],
        description="""
    The passive resistance in the measurement circuit if a resistor was used
- Give the value in ohm
- If there are uncertainties, only state the best estimate, e.g. write 1.03 and not 1.01-1.05
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    temperature_load_condition = Quantity(
        type=str,
        shape=[],
        description="""
    The load situation of the temperature during the stability measurement.
- If the temperature is constant during the entire stability measurement, state this as ‘Constant’.
- If there is a cycling between colder and hotter conditions, state this as ‘Cycled’
- If the temperature varies in an uncontrolled way, state this as ‘Uncontrolled’
- This category was included after the projects initial phase wherefor the list of reported categories is
short. Thus, be prepared to expand the given list of alternatives in the data template.
Example:
Constant
Uncontrolled
Cycled
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    'constant',
                    'Uncontrolled',
                    'Cycled',
                    'uncontrolled',
                    'Constant',
                ]
            ),
        ),
    )

    temperature_range = Quantity(
        type=str,
        shape=[],
        description="""
    The temperature range during the stability measurement
- Separate the lower and upper bound by a semicolon.
- For constant values, state only that value.
- If there are uncertainties, only state the best estimate, e.g. write 1 and not 0.90-1.1
- State unknown values as ‘nan’
Example:
30
25; 85
nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '22.0; 22.0',
                    '70; 70',
                    '-10.0; -10.0',
                    '80; 80',
                    '55.0; 55.0',
                    '50.0; 50.0',
                    '10; 25',
                    'nan; nan',
                    '75.0; 75.0',
                    '20; 20',
                    '120.0; 120.0',
                    '-40.0; 85.0',
                    '85.0; 85.0',
                    '0.0; 0.0',
                    '26.0; 26.0',
                    '27.5; 27.5',
                    '28.0; 28.0',
                    '25; 85',
                    '25; 25',
                    '65; 65',
                    '22.3; 22.7',
                    '110.0; 110.0',
                    '25; 80',
                    '21.0; 21.0',
                    '14.0; 14.0',
                    '20; 25',
                    '23; 23',
                    '-22.0; 100',
                    '100.0; 100.0',
                    '95.0; 95.0',
                    '23.5; 23.5',
                    '15; 25',
                    '30; 30',
                    '25; 35',
                    '18; 22',
                    '42.0; 42.0',
                    '17.0; 17.0',
                    '22.5; 22.5',
                    '28; 32',
                    '25; 30',
                    '20; 30',
                    '60; 60',
                    '2; 70',
                    '75; 75',
                    '80.0; 80.0',
                    '45.0; 45.0',
                    '160.0; 160.0',
                    '90.0; 90.0',
                    '53.0; 53.0',
                    '30.0; 30.0',
                    '20; 40',
                    '45; 45',
                    '150.0; 150.0',
                    '40.0; 40.0',
                    '-20.0; -20.0',
                    '20.0; 20.0',
                    '25.0; 25.0',
                    '70.0; 70.0',
                    '41.0; 41.0',
                    '50; 50',
                    '40; 40',
                    '65.0; 65.0',
                    '35.0; 35.0',
                    '25.5; 25.5',
                    '24.0; 24.0',
                    '15.0; 15.0',
                    '82.0; 82.0',
                    '23.0; 23.0',
                    '28; 28',
                    '60.0; 60.0',
                    '85; 85',
                    '100; 100',
                    '23.1; 23.1',
                    'nan; 120',
                    '21.5; 21.5',
                    '27.0; 27.0',
                ]
            ),
        ),
    )

    temperature_cycling_times = Quantity(
        type=str,
        shape=[],
        description="""
    If the temperature is cycled during the stability measurement, state the time in low temperature followed by the time in high temperature for the cycling period.
- If not applicable, leave blank
- Separate the lower and upper bound by a semicolon.
- If there are uncertainties, only state the best estimate, e.g. write 1 and not 0.90-1.1
- State unknown values as ‘nan’
Example:
2; 2
0.5; 10
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'Unknown',
                    '15.0; 15.0',
                    '100.0; 100.0',
                    '25.0; 25.0',
                    '60.0; 120.0',
                ]
            ),
        ),
    )

    temperature_ramp_speed = Quantity(
        type=np.dtype(np.float64),
        unit=('celsius/minute'),
        shape=[],
        description="""
    The temperature ramp speed
- If there are uncertainties, only state the best estimate, e.g. write 1.03 and not 1.01-1.05
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    atmosphere = Quantity(
        type=str,
        shape=[],
        description="""
    The atmosphere in which the stability measurement is conducted
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
                    'Air. Desiccator',
                    'Ambient',
                    'N2',
                    'Vacuum',
                    'O2',
                    'N2; O2',
                    'Glovebox',
                    'Ar',
                    'Near-space',
                ]
            ),
        ),
    )

    atmosphere_oxygen_concentration = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description="""
    The oxygen concentration in the atmosphere
- If unknown, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    relative_humidity_load_conditions = Quantity(
        type=str,
        shape=[],
        description="""
    The load situation of the relative humidity during the stability measurement.
- If the relative humidity is constant during the entire stability measurement, state this as ‘Constant’.
- If there is a cycling between dryer and damper conditions, state this as ‘Cycled’
- If the relative humidity varies in an uncontrolled way, i.e. the cell is operated under ambient conditions, state this as ‘Ambient’
- This category was included after the projects initial phase wherefor the list of reported categories is
short. Thus, be prepared to expand the given list of alternatives in the data template.
Example
Ambient
Controlled
Cycled
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    'constant',
                    'Controlled',
                    'Ambient',
                    'ambient',
                    'Constant',
                ]
            ),
        ),
    )

    relative_humidity_range = Quantity(
        type=str,
        shape=[],
        description="""
    The relative humidity range during the stability measurement
- Separate the lower and upper bound by a semicolon.
- For constant values, state only that value.
- If there are uncertainties, only state the best estimate, e.g. write 1 and not 0.90-1.1
- State unknown values as ‘nan’
Example:
45
35; 65
nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '40; 50',
                    '61; 75',
                    '30; 80',
                    '80; 80',
                    '60; 70',
                    '25; 45',
                    'nan; nan',
                    '25; 50',
                    '20; 20',
                    '50; 70',
                    '30; 50',
                    '60; 80',
                    '35; 35',
                    '0; 0',
                    '55; 70',
                    '75; 85',
                    '65; 65',
                    '50; 60',
                    '50.60; 50.60',
                    '1; 50',
                    '25; 25',
                    '20; 70',
                    '25; 35',
                    '30; 30',
                    '10; 15',
                    '45; 55',
                    '15; 25',
                    '15; 15',
                    '15; 20',
                    '42.2; 54.4',
                    '35; 40',
                    '30; 70',
                    '25; 40',
                    '25; 30',
                    '20; 30',
                    '60; 60',
                    '20; 40',
                    '30; 35',
                    '45; 45',
                    '40; 80',
                    '5; 5',
                    '40; 60',
                    '90; 95',
                    '50; 50',
                    '40; 40',
                    '45; 60',
                    '12; 18',
                    '35; 45',
                    '10; 20',
                    '45; 50',
                    '40; 45',
                    '85; 85',
                    '10; 30',
                    '30; 40',
                    '100; 100',
                ]
            ),
        ),
    )

    relative_humidity_average_value = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description="""
    The average relative humidity during the stability measurement.
- If there are uncertainties, only state the best estimate, e.g. write 1 and not 0.90-1.1
- If unknown, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    time_total_exposure = Quantity(
        type=np.dtype(np.float64),
        unit=('hour'),
        shape=[],
        description="""
    The total duration of the stability measurement.
- If there are uncertainties, only state the best estimate, e.g. write 1000 and not 950-1050
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    periodic_JV_measurements = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if the stability measurement periodically is interrupted for JV-measurements. A typical example is a cell that is stored in the dark and once in a wile is take out from storage for an IV-measurement.
                    """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    periodic_JV_measurements_time_between_jv = Quantity(
        type=str,
        shape=[],
        description="""
    The average time between JV-measurement during the stability measurement.
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '40.0',
                    '85.0',
                    '90.0',
                    '50.0',
                    '24.0',
                    '1440.0',
                    '10.0',
                    '3.0',
                    '3.2',
                    '220.0',
                    '60.0',
                    '5.0',
                    '125.0',
                    '9.0',
                    '120.0',
                    'Unknown',
                    '72.0',
                    '7.0',
                    '180.0',
                    '75.0',
                    '100.0',
                    '400.0',
                    '240.0',
                    '80.0',
                    '6.0',
                    '0.067',
                    '480.0',
                    '30.0',
                    '0.3',
                    '0.167',
                    '2.0',
                    '0.016',
                    '0.5',
                    '168.0',
                    '48.0',
                    '25.0',
                    '0.1',
                    '52.0',
                    '20.0',
                    '360.0',
                    '160.0',
                    '34.0',
                    '1680.0',
                    '15.0',
                    '200.0',
                ]
            ),
        ),
    )

    PCE_initial_value = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description="""
    The efficiency, PCE, of the cell before the stability measurement routine starts
- Give the efficiency in %
- If there are uncertainties, only state the best estimate, e.g. write 20.5 and not 19-20
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    PCE_burn_in_observed = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if the performance has a relatively fast initial decay after which the decay rate stabilises at a lower level.
- There are no sharp boundary between an initial burn in phase an a catastrophic failure, but if the performance of the cell quickly degrade by more than half, it is stretching it a bit to label this as an initial burn in phase.
                    """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    PCE_end_of_experiment = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description="""
    The efficiency, PCE, of the cell at the end of the stability routine
- Give the efficiency in %
- If there are uncertainties, only state the best estimate, e.g. write 20.5 and not 19-20
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    PCE_T95 = Quantity(
        type=np.dtype(np.float64),
        unit=('hour'),
        shape=[],
        description="""
    The time after which the cell performance has degraded by 5 % with respect to the initial performance.
- If there are uncertainties, only state the best estimate, e.g. write 1000 and not 950-1050
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    PCE_Ts95 = Quantity(
        type=np.dtype(np.float64),
        unit=('hour'),
        shape=[],
        description="""
    The time after which the cell performance has degraded by 5 % with respect to the performance after any initial burn in phase.
- If there are uncertainties, only state the best estimate, e.g. write 1000 and not 950-1050
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    PCE_T80 = Quantity(
        type=np.dtype(np.float64),
        unit=('hour'),
        shape=[],
        description="""
    The time after which the cell performance has degraded by 20 % with respect to the initial performance.
- If there are uncertainties, only state the best estimate, e.g. write 1000 and not 950-1050
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    PCE_Ts80 = Quantity(
        type=np.dtype(np.float64),
        unit=('hour'),
        shape=[],
        description="""
    The time after which the cell performance has degraded by 20 % with respect to the performance after any initial burn in phase.
- If there are uncertainties, only state the best estimate, e.g. write 1000 and not 950-1050
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    PCE_Te80 = Quantity(
        type=np.dtype(np.float64),
        unit=('hour'),
        shape=[],
        description="""
    An estimated T80 for cells that were not measured sufficiently long for them to degrade by 20 %. with respect to the initial performance.
- This value will by definition have a significant uncertainty to it, as it is not measured but extrapolated under the assumption linearity but without a detailed and stabilised extrapolation protocol. This estimate is, however, not without value as it enables a rough comparison between all cells for with the stability has been measured.
- If there is an experimental T80, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    PCE_Tse80 = Quantity(
        type=np.dtype(np.float64),
        unit=('hour'),
        shape=[],
        description="""
    An estimated T80s for cells that was not measured sufficiently long for them to degrade by 20 %. with respect to the performance after any initial burn in phase.
- This value will by definition have a significant uncertainty to it, as it is not measured but extrapolated under the assumption linearity but without a detailed and stabilised extrapolation protocol. This estimate is, however, not without value as it enables a ruff comparison between all cells for with the stability has been measured.
- If there is an experimental T80s, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    PCE_after_1000_h = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description="""
    The efficiency, PCE, of the cell after 1000 hours
- Give the efficiency in %
- If there are uncertainties, only state the best estimate, e.g. write 20.5 and not 19-20
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    lifetime_energy_yield = Quantity(
        type=np.dtype(np.float64),
        unit=('kW*hour/m^2'),
        shape=[],
        description="""
    The lifetime energy yield
- If there are uncertainties, only state the best estimate, e.g. write 20.5 and not 19-20
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    flexible_cell_number_of_bending_cycles = Quantity(
        type=np.dtype(np.int64),
        shape=[],
        description="""
    Number of bending cycles for a flexible cell in a mechanical stability test
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    flexible_cell_bending_radius = Quantity(
        type=np.dtype(np.float64),
        unit=('degree'),
        shape=[],
        description="""
    The bending radius of the flexible cell during the mechanical stability test
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    flexible_cell_PCE_initial_value = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description="""
    The efficiency, PCE, of the cell before the mechanical stability measurement routine starts
- Give the efficiency in %
- If there are uncertainties, only state the best estimate, e.g. write 20.5 and not 19-20
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    flexible_cell_PCE_end_of_experiment = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description="""
    The efficiency, PCE, of the cell after the mechanical stability measurement routine
- Give the efficiency in %
- If there are uncertainties, only state the best estimate, e.g. write 20.5 and not 19-20
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    link_raw_data_for_stability_trace = Quantity(
        type=str,
        shape=[],
        description="""
    A link to where the data file for the stability data is stored
- This is a beta feature. The plan is to create a file repository where the raw files for stability data can be stored and disseminated. With the link and associated protocols, it should be possible to programmatically access and analyse the raw stability data.
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', 'www.testsite…'])
        ),
    )
