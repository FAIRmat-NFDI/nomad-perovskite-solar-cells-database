import numpy as np
from nomad.datamodel.data import ArchiveSection
from nomad.metainfo import Quantity


class Outdoor(ArchiveSection):
    """A section describing measurements performed in outdoor conditions"""

    tested = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if the performance of the cell has been tested outdoors.
                    """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    protocol = Quantity(
        type=str,
        shape=[],
        description="""
    The protocol used for the outdoor testing.
- For a more detailed discussion on protocols and standard nomenclature for stability measurements, please see the following paper:
o Consensus statement for stability assessment and reporting for perovskite photovoltaics based on ISOS procedures byM. V. Khenkin et al. Nat. Energ. 2020. DOI10.1038/s41560-019-0529-5
Example:
IEC 61853-1
ISOS-O-1
ISOS-O-2
ISOS-O-3
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=['', 'ISOS-O-1', 'IEC 61853-1']),
        ),
    )

    average_over_n_number_of_cells = Quantity(
        type=np.dtype(np.int64),
        shape=[],
        description="""
    The number of cells the reported outdoor data is based on.
Example:
- The preferred way to enter data is to give every individual cell its own entry in the data template/data base. If that is done, the data is an average over 1 cell.
- If the reported data is not the data from one individual cell, but an average over N cells. Give the number of cells.
- If the reported value is an average, but it is unknown over how many cells the value has been averaged (and no good estimate is available), state the number of cells as 2, which is the smallest number of cells that qualifies for an averaging procedure.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    location_country = Quantity(
        type=str,
        shape=[],
        description="""
    The country where the outdoor testing was occurring
- For measurements conducted in space, state this as ’Space International’
Example:
Sweden
Switzerland
Space International
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    'Italy',
                    'Switzerland',
                    'Slovenia',
                    'China',
                    'Great Britain',
                    'Colombia',
                    'Spain',
                    'Israel',
                    'Space International',
                    'Saudi Arabia',
                ]
            ),
        ),
    )

    location_city = Quantity(
        type=str,
        shape=[],
        description="""
    The city where the outdoor testing was occurring
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=['', 'Ljubljana', 'Hong Kong']),
        ),
    )

    location_coordinates = Quantity(
        type=str,
        shape=[],
        description="""
    The coordinates fort the places where the outdoor testing was occurring.
- Use decimal degrees (DD) as the format.
Example:
59.839116; 17.647979
52.428150; 13.532134
                    """,
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['nan; nan'])),
    )

    location_climate_zone = Quantity(
        type=str,
        shape=[],
        description="""
    The climate zone for the places where the outdoor testing was occurring.
Example:
Cold
Desert
Subtropical
Teperate
Tropical
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=['', 'Subtropical', 'Cold', 'Desert', 'Temperate']),
        ),
    )

    installation_tilt = Quantity(
        type=np.dtype(np.float64),
        unit=('degree'),
        shape=[],
        description="""
    The tilt of the installed solar cell.
- A module lying flat on the ground have a tilt of 0
- A module standing straight up has a tilt of 90
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    installation_cardinal_direction = Quantity(
        type=np.dtype(np.float64),
        unit=('degree'),
        shape=[],
        description="""
    The cardinal direction of the installed solar cell.
- North is 0
- East is 90
- South is 180
- West is 270
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    installation_number_of_solar_tracking_axis = Quantity(
        type=np.dtype(np.int64),
        shape=[],
        description="""
    The number of tracking axis in the installation.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    time_season = Quantity(
        type=str,
        shape=[],
        description="""
    The time of year the outdoor testing was occurring.
- Order the seasons in alphabetic order and separate them with semicolons.
- For time periods longer than a year, state all four seasons once.
Example:
Autumn
Autumn; Summer
Autumn; Spring, Winter
Autumn; Spring; Summer; Winter
Spring; Winter
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    'Summer',
                    'Autumn; Spring; Summer; Winter',
                    'Autumn; Winter',
                    'Winter',
                    'Spring',
                    'Autumn; Summer',
                ]
            ),
        ),
    )

    time_start = Quantity(
        type=str,
        shape=[],
        description="""
    The starting time for the outdoor measurement.
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['0000:00:00:00:00'])
        ),
    )

    time_end = Quantity(
        type=str,
        shape=[],
        description="""
    The ending time for the outdoor measurement.
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=['0000:00:00:00:00', '0000:03:14:00:00']),
        ),
    )

    time_total_exposure = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description="""
    The total duration of the outdoor measurement in days.
- If there are uncertainties, only state the best estimate, e.g. write 1000 and not 950-1050
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    potential_bias_load_condition = Quantity(
        type=str,
        shape=[],
        description="""
    The Potentiostatic load condition during the outdoor measurement
- When the cell is not connected to anything, state this as ‘Open circuit’
Examples:
Constant current
Constant potential
MPPT
Open circuit
Passive resistance
Short circuit
                    """,
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['', 'MPPT'])),
    )

    potential_bias_range = Quantity(
        type=str,
        shape=[],
        description="""
    The potential range during the outdoor measurement
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['nan; nan'])),
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
    The load situation of the temperature during the outdoor measurement.
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
            component='EnumEditQuantity', props=dict(suggestions=['', 'Uncontrolled'])
        ),
    )

    temperature_range = Quantity(
        type=str,
        shape=[],
        description="""
    The temperature range during the outdoor measurement
- Separate the lower and upper bound by a semicolon.
- For constant values, state only that value.
- If there are uncertainties, only state the best estimate, e.g. write 1 and not 0.90-1.1
- State unknown values as ‘nan’
Example:
30
-10; 85
nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['nan; nan', '15; 60'])
        ),
    )

    temperature_tmodule = Quantity(
        type=np.dtype(np.float64),
        unit=('celsius'),
        shape=[],
        description="""
    The effective temperature of the module during peak hours.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    periodic_JV_measurements = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if the outdoor measurement periodically is interrupted for JV-measurements.
                    """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    periodic_JV_measurements_time_between_measurements = Quantity(
        type=np.dtype(np.float64),
        unit=('hour'),
        shape=[],
        description="""
    The average time between JV-measurement during the outdoor measurement.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    PCE_initial_value = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description="""
    The efficiency, PCE, of the cell before the measurement routine starts
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
                    """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    PCE_end_of_experiment = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description="""
    The efficiency, PCE, of the cell at the end of the experiment
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
    An estimated T80 for cells that was not measured sufficiently long for them to degrade by 20 %. with respect to the initial performance.
- This value will by definition have a significant uncertainty to it, as it is not measured but extrapolated under the assumption linearity but without a detailed and stabilised extrapolation protocol. This estimate is, however, not without value as it enables a ruff comparison between all cells for with the stability has been measured.
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

    power_generated = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description="""
    The yearly power generated during the measurement period in kWh/year/m^2.
- If there are uncertainties, only state the best estimate, e.g. write 20.5 and not 19-20
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    link_raw_data_for_outdoor_trace = Quantity(
        type=str,
        shape=[],
        description="""
    A link to where the data file for the measurement is stored
- This is a beta feature. The plan is to create a file repository where the raw files for stability data can be stored and disseminated. With the link and associated protocols, it should be possible to programmatically access and analyse the raw data.
                    """,
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[''])),
    )

    detaild_weather_data_available = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if detailed weather data is available for the measurement period
                    """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    link_detailed_weather_data = Quantity(
        type=str,
        shape=[],
        description="""
    A link to where the data file for the measurement is stored
- This is a beta feature. The plan is to create a file repository where the raw files for stability data can be stored and disseminated. With the link and associated protocols, it should be possible to programmatically access and analyse the raw data.
                    """,
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[''])),
    )

    spectral_data_available = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE measured spectral data are available for the measurement period
                    """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    link_spectral_data = Quantity(
        type=str,
        shape=[],
        description="""
    A link to where the data file for the measurement is stored
- This is a beta feature. The plan is to create a file repository where the raw files for stability data can be stored and disseminated. With the link and associated protocols, it should be possible to programmatically access and analyse the raw data.
                    """,
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[''])),
    )

    irradiance_measured = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE measured irradiance data are available for the measurement period
                    """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    link_irradiance_data = Quantity(
        type=str,
        shape=[],
        description="""
    A link to where the data file for the measurement is stored
- This is a beta feature. The plan is to create a file repository where the raw files for stability data can be stored and disseminated. With the link and associated protocols, it should be possible to programmatically access and analyse the raw data.
                    """,
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[''])),
    )
