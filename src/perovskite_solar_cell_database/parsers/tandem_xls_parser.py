import re
from typing import TYPE_CHECKING
from unicodedata import numeric

import pandas as pd
from nomad.config import config
from nomad.datamodel.data import EntryData

# from nomad.parsing.tabular import create_archive
from nomad.datamodel.datamodel import EntryArchive
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.metainfo import Quantity
from nomad.parsing.parser import MatchingParser
from pint import UnitRegistry, errors

from perovskite_solar_cell_database.composition import (
    PerovskiteAIonComponent,
    PerovskiteBIonComponent,
    PerovskiteCompositionSection,
    PerovskiteXIonComponent,
)
from perovskite_solar_cell_database.parsers.utils import create_archive
from perovskite_solar_cell_database.schema_packages.tandem.measurements import (
    EQEResults,
    ExternalQuantumEfficiency,
    Illumination,
    JVConditions,
    JVMeasurement,
    JVResults,
    MeasurementConditions,
    PerformedMeasurements,
    Preconditioning,
    StabilisedPerformance,
    StabilisedPerformanceConditions,
)
from perovskite_solar_cell_database.schema_packages.tandem.schema import (
    PerovskiteTandemSolarCell,
)
from perovskite_solar_cell_database.schema_packages.tandem.tandem import (
    ChalcopyriteAlkaliAdditives,
    ChalcopyriteLayer,
    ChalcopyriteLayerComposition,
    Cleaning,
    DepositionStep,
    Elemental,
    GasPhaseSynthesis,
    General,
    Layer,
    LayerComposition,
    LayerProperties,
    LiquidSynthesis,
    NonAbsorbingLayer,
    PerovskiteLayer,
    PerovskiteLayerProperties,
    PhotoAbsorberLayer,
    PhotoAbsorberProperties,
    QuenchingSolvent,
    ReactionComponent,
    Reference,
    SiliconLayer,
    SiliconLayerProperties,
    Solvent,
    SolventAnnealing,
    Storage,
    SubCell,
    Substance,
    Substrate,
    SurfaceTreatment,
    Synthesis,
    ThermalAnnealing,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger


ureg = UnitRegistry()
ureg.define('% = 0.01 * [] = percent')
ureg.define('wt% = 0.01 * gram/gram = weight_percent')
ureg.define('vol% = 0.01* liter/liter = volume_percent')
ureg.define('mTorr = millitorr')
ureg.define('Torr = torr')

unit_pattern = re.compile(
    r'^(\d+(\.\d+)?|\.\d+)([eE][-+]?\d+)?\s*\w+([*/^]\w+)*(\s*[/()]\s*\w+)*$'
)  # Matches ".9kg", "10mA", "1.5 kg", "2 cm^2/(V*s)", "1e-6 m" etc.


class TandemXLSParser(MatchingParser):
    """
    Parser for matching tandem db files and creating instances of PerovskiteTandemSolarCell.
    """

    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
        child_archives: dict[str, 'EntryArchive'] = None,
    ) -> None:
        logger.info('TandemXLSParser.parse')
        data_frame = pd.read_excel(mainfile, index_col=0)

        # Process each column/device/publication separately
        for col in data_frame.columns:
            logger.info(f'Processing column: {col}')
            entry_archive = EntryArchive()

            # Clean the data frame
            # Set proper Boolean values and remove rows with all NaN values
            column_data = cleanup_dataframe(data_frame[col])

            # Extract the data
            layer_stack = extract_layer_stack(column_data)
            general = extract_general(column_data)
            reference = extract_reference(column_data)
            measurements = extract_measurements(column_data)

            tandem = PerovskiteTandemSolarCell(
                general=general,
                reference=reference,
                layer_stack=layer_stack,
                measurements=measurements,
            )

            entry_archive.data = tandem

            create_archive(
                entry_archive.m_to_dict(),
                archive.m_context,
                f'tandem_{col}.archive.json',
                'json',
                logger,
            )


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


def cleanup_dataframe(data_frame):
    """
    Cleans the data frame by setting proper Boolean values and
    removing rows with all NaN values. Returns the cleaned data frame.
    """
    bool_mask = data_frame.index.str.contains(r'\[TRUE/FALSE\]')
    data_frame.loc[bool_mask] = data_frame.loc[bool_mask].replace(
        {0: False, '0': False, 'FALSE': False, 1: True, '1': True, 'TRUE': True}
    )

    return data_frame.dropna(how='all')


def split_data(data, delimiter='|'):
    """
    Splits each column of a DataFrame or Series by a delimiter and expands the data frame to fit the longest list.
    Preserves the original index of the DataFrame.

    Parameters:
    data (pd.DataFrame or pd.Series): The data frame to split.
    delimiter (str): The delimiter to split the data frame by.

    Returns:
    pd.DataFrame: The expanded data frame with unique column names and preserved index.
    """

    # If it's a DataFrame, process each column
    if isinstance(data, pd.DataFrame):
        expanded_dfs = []
        for column in data.columns:
            # Split each column by the delimiter if it is a string
            split_data = data[column].apply(
                lambda x: str(x).split(delimiter) if isinstance(x, str) else [x]
            )
            # Expand the data frame to fit the longest list
            max_len = split_data.apply(len).max()
            if max_len > 1:
                expanded_data = split_data.apply(
                    lambda x: x + [x[-1]] * (max_len - len(x))
                )
                # Append the data frame with unique column names and preserved index
                expanded_df = pd.DataFrame(expanded_data.tolist(), index=data.index)
                expanded_df.columns = [f'{column}_{i}' for i in range(max_len)]
                expanded_dfs.append(expanded_df)
            else:
                expanded_dfs.append(data[column])

        return pd.concat(expanded_dfs, axis=1)

    elif isinstance(data, pd.Series):
        split_data = data.apply(
            lambda x: str(x).split(delimiter) if isinstance(x, str) else [x]
        )
        max_len = split_data.apply(len).max()
        if max_len > 1:
            expanded_data = split_data.apply(lambda x: x + [x[-1]] * (max_len - len(x)))
            expanded_df = pd.DataFrame(expanded_data.tolist(), index=data.index)
            expanded_df.columns = [f'{data.name}_{i}' for i in range(max_len)]
        else:
            expanded_df = pd.DataFrame(data)
        return expanded_df

    else:
        raise ValueError('Input data_frame must be a pandas DataFrame or Series')


def convert_value(value, unit=None):  # noqa: PLR0911
    """
    Tries to convert the value to a Quantity object using the specified unit.

    Parameters:
    value (int, float, str): The value to be converted. Can be an integer, float, or string.
    unit (str, optional): The unit to convert the value to. Defaults to None.
    """

    if unit and isinstance(value, int | float) and not isinstance(value, bool):
        return ureg.Quantity(value, unit)

    if isinstance(value, str):
        value = value.strip()

        # Check for boolean values
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        elif value.lower() == 'nan':
            return None

        # Check for numerical values
        if value.isdigit() and not unit:
            return int(value)
        try:
            number = float(value)
            return ureg.Quantity(number, unit) if unit else number
        except ValueError:
            pass

        # Check for unit values
        if unit_pattern.match(value):
            try:
                quantity = ureg.Quantity(value)
                return quantity.to(unit) if unit else quantity
            except (errors.UndefinedUnitError, ValueError):
                pass

    return value


def partial_get(data, label, default=None, convert=False, unit=None):
    """
    Retrieve a value from a DataFrame or Series based on a partial match of the label.

    Parameters:
    data (pd.DataFrame or pd.Series): The data source to search within.
    label (str): The label to partially match against the index of the data.
    default (any, optional): The default value to return if no match is found. Defaults to None.
    convert (bool, optional): Whether to convert the retrieved value using the specified unit. Defaults to False.
    unit (str, optional): The unit to use for conversion if convert is True. Defaults to None.

    Returns:
    any: The matched value from the data, converted if specified, or the default value if no match is found.
    """

    df_matched = data[data.index.str.contains(label)]
    if df_matched.empty:
        return default

    if isinstance(data, pd.DataFrame):
        value = df_matched.iloc[0, 0]
    elif isinstance(data, pd.Series):
        value = df_matched.iloc[0]
    else:
        return default

    if convert or unit:
        return convert_value(value, unit)
    else:
        return value.strip() if isinstance(value, str) else value


def exact_get(data, label, default=None, convert=False, unit=None):
    """
    Retrieve a value from a DataFrame or Series based on an exact match of the label.

    Parameters:
    data (pd.DataFrame or pd.Series): The data source to search within.
    label (str): The label to match against the index of the data.
    default (any, optional): The default value to return if no match is found. Defaults to None.
    convert (bool, optional): Whether to convert the retrieved value using the specified unit. Defaults to False.
    unit (str, optional): The unit to use for conversion if convert is True. Defaults to None.

    Returns:
    any: The matched value from the data, converted if specified, or the default value if no match is found.
    """
    if label not in data.index:
        return default
    elif isinstance(data, pd.DataFrame):
        value = data.loc[label, data.columns[0]]
    elif isinstance(data, pd.Series):
        value = data.loc[label]
    return convert_value(value, unit) if convert or unit else value


def handle_concentration(concentration):
    """
    Converts the concentration string to a Quantity object and returns a dictionary with the appropriate concentration type.
    """

    result_dict = {}

    if isinstance(concentration, str):
        concentration = concentration.replace('wt%', 'weight_percent')
        concentration = concentration.replace('vol%', 'volume_percent')
        concentration = concentration.replace('%', 'percent')
        concentration = concentration.replace('dm3', 'liter')
        concentration = concentration.replace('cm3', 'ml')
        concentration = convert_value(concentration)
    if isinstance(concentration, ureg.Quantity):
        if concentration.dimensionality == '[mass]/[length]**3':
            result_dict['mass_concentration'] = concentration.to('g/l')
        elif concentration.dimensionality == '[substance]/[length]**3':
            result_dict['molar_concentration'] = concentration.to('mol/l')
        elif str(concentration.dimensionality) == str(
            ureg.dimensionless.dimensionality
        ):
            if 'gram' in str(concentration.units) or str(concentration.units) == 'wt%':
                result_dict['mass_fraction'] = concentration.to('g/g')
            elif (
                'liter' in str(concentration.units)
                or str(concentration.units) == 'vol%'
            ):
                result_dict['volume_fraction'] = concentration.to('l/l')

    return result_dict


def extract_cleaning(data_frame):
    """
    Extracts the cleaning steps from the data subframe and returns a list of CleaningStep objects.
    """

    df_cleaning = data_frame[data_frame.index.str.contains('Cleaning')]
    if df_cleaning.empty:
        return None

    df_cleaning = split_data(df_cleaning, delimiter='|')  # probably not necessary
    df_cleaning = split_data(df_cleaning, delimiter='>>')
    cleaning_steps = [
        partial_get(df_cleaning[column], 'procedure') for column in df_cleaning.columns
    ]
    return Cleaning(steps=cleaning_steps)


def extract_additives(data_frame):
    """
    Extracts the additives from the data subframe and returns a list of Substance objects.
    """
    df_temp = data_frame[data_frame.index.str.contains('Additives.')]
    if df_temp.empty:
        return None

    additives = []
    df_components = split_data(df_temp, delimiter=';')
    for component in df_components.columns:
        concentration = partial_get(
            df_components[component], 'Additives. Concentrations'
        )
        additives.append(
            Substance(
                name=partial_get(df_components[component], 'Additives. Compounds'),
                **handle_concentration(concentration),
            )
        )

    return additives if additives else None


def extract_solvents(data_frame):
    """
    Extracts the solvents from the data subframe and returns a list of Solvent objects.
    """
    df_temp = data_frame[data_frame.index.str.contains('Solvents')]
    if df_temp.empty:
        return None

    solvents = []
    df_components = split_data(df_temp, delimiter=';')
    for component in df_components.columns:
        solvent_properties = {
            'name': partial_get(df_components[component], 'Solvents '),
            'mixing_ratio': partial_get(
                df_components[component], 'Mixing ratio', convert=True
            ),
            'supplier': partial_get(df_components[component], 'Solvents. Supplier'),
            'purity': partial_get(df_components[component], 'Solvents. Purity'),
        }
        solvents.append(Solvent(**solvent_properties))

    return solvents if solvents else None


def extract_reactants(data_frame):
    """
    Extracts the reactants from the data subframe and returns a list of ReactionComponent objects.
    """
    df_temp = data_frame[data_frame.index.str.contains('Reaction solutions.')]
    if df_temp.empty:
        return None

    reactants = []
    df_components = split_data(df_temp, delimiter=';')
    for component in df_components.columns:
        properties = {
            'name': partial_get(
                df_components[component], 'Reaction solutions. Compounds '
            ),
            'supplier': partial_get(
                df_components[component], 'Reaction solutions. Compounds. Supplier'
            ),
            'purity': partial_get(
                df_components[component], 'Reaction solutions. Compounds. Purity'
            ),
            'volume': partial_get(
                df_components[component],
                'Reaction solutions. Volumes',
                unit='ml',
            ),
            'age': partial_get(
                df_components[component],
                'Reaction solutions. Age',
                unit='hour',
            ),
            'temperature': partial_get(
                df_components[component],
                'Reaction solutions. Temperature',
                unit='celsius',
            ),
        }
        # Handle destinction between mg/ml, mol/l, and wt%
        concentration = partial_get(
            df_components[component], 'Reaction solutions. Concentrations'
        )
        if concentration:
            properties.update(handle_concentration(concentration))

        reactants.append(ReactionComponent(**properties))

    return reactants if len(reactants) > 0 else None


def extract_quenching_solvents(data_frame):
    """
    Extracts the quenching solvents from the data subframe and returns a list of QuenchingSolvent objects.
    """
    df_temp = data_frame[
        data_frame.index.str.contains('Quenching media')
        & ~data_frame.index.str.contains('Additives')
    ]
    if df_temp.empty:
        return None

    quenching_solvents = []

    df_components = split_data(df_temp, delimiter=';')
    for component in df_components.columns:
        solvent_properties = {
            'name': partial_get(df_components[component], 'Quenching media '),
            'mixing_ratio': partial_get(
                df_components[component], 'Mixing media. Mixing ratios', convert=True
            ),
            'volume': partial_get(
                df_components[component], 'Quenching media. Volume', unit='microliter'
            ),
        }

        # Handle additives: untested, no data available
        df_temp = data_frame[
            data_frame.index.str.contains('Quenching media. Additives')
        ]
        if not df_temp.empty:
            df_additives = split_data(df_temp, delimiter=';')
            for additive in df_additives.columns:
                solvent_properties['additives'] = extract_additives(
                    df_additives[additive]
                )

        quenching_solvents.append(QuenchingSolvent(**solvent_properties))

    return quenching_solvents if quenching_solvents else None


def extract_perovskite_composition(data_frame):
    """
    Extracts the composition from the data subframe and returns a PerovskiteCompositionSection object.
    """

    df_temp = data_frame[data_frame.index.str.contains('Perovskite. Dimension')]
    if not df_temp.empty:
        if partial_get(df_temp, 'Dimension. 0D'):
            dimensionality = '0D'
        elif partial_get(df_temp, r'Dimension. 2D \['):
            dimensionality = '2D'
        elif partial_get(df_temp, 'Dimension. 2D/3D'):
            dimensionality = '2D/3D'
        elif partial_get(df_temp, r'Dimension. 3D \['):
            dimensionality = '3D'
        else:
            dimensionality = 'Other'

    ions_a, ions_b, ions_c = [], [], []
    df_temp = data_frame[data_frame.index.str.contains('Perovskite. Composition')]
    if not df_temp.empty:
        estimate_string = partial_get(df_temp, 'Assumption')
        if estimate_string:
            estimate_string = estimate_string.lower()
            if 'solution' in estimate_string:
                composition_estimate = 'Estimated from precursor solutions'
            elif 'literature' in estimate_string:
                composition_estimate = 'Literature value'
            elif 'xrd' in estimate_string:
                composition_estimate = 'Estimated from XRD data'
            elif 'spectroscop' in estimate_string:
                composition_estimate = 'Estimated from spectroscopic data'
            elif 'simulation' in estimate_string:
                composition_estimate = 'Theoretical simulation'
            elif 'hypothetical' in estimate_string:
                composition_estimate = 'Hypothetical compound'
            else:
                composition_estimate = 'Other'
        else:
            composition_estimate = 'Other'

        df_components = split_data(
            df_temp[df_temp.index.str.contains('A-ions')], delimiter=';'
        )
        for component in df_components.columns:
            abbreviation = partial_get(df_components[component], '-ions ')
            coefficient = partial_get(
                df_components[component], '-ions. Coefficients ', convert=True
            )
            if type:
                ions_a.append(
                    PerovskiteAIonComponent(
                        abbreviation=abbreviation, coefficient=coefficient
                    )
                )
        df_components = split_data(
            df_temp[df_temp.index.str.contains('B-ions')], delimiter=';'
        )
        for component in df_components.columns:
            abbreviation = partial_get(df_components[component], '-ions ')
            coefficient = partial_get(
                df_components[component], '-ions. Coefficients ', convert=True
            )
            if type:
                ions_b.append(
                    PerovskiteBIonComponent(
                        abbreviation=abbreviation, coefficient=coefficient
                    )
                )
        df_components = split_data(
            df_temp[df_temp.index.str.contains('C-ions')], delimiter=';'
        )
        for component in df_components.columns:
            abbreviation = partial_get(df_components[component], '-ions ')
            coefficient = partial_get(
                df_components[component], '-ions. Coefficients ', convert=True
            )
            if type:
                ions_c.append(
                    PerovskiteXIonComponent(
                        abbreviation=abbreviation, coefficient=coefficient
                    )
                )
    additives = extract_additives(data_frame)

    return PerovskiteCompositionSection(
        ions_a_site=ions_a,
        ions_b_site=ions_b,
        ions_x_site=ions_c,
        dimensionality=dimensionality,
        composition_estimate=composition_estimate,
        additives=additives,
    )


def extract_chalcopyrite_additives(data_frame):
    """
    Extracts the additives from the data subframe and returns a list of Substance objects.
    """
    df_temp = data_frame[data_frame.index.str.contains('Additives.')]
    if df_temp.empty:
        return None

    additives = []
    df_components = split_data(df_temp, delimiter=';')
    for component in df_components.columns:
        concentration = partial_get(
            df_components[component], 'Additives. Concentrations'
        )
        additives.append(
            ChalcopyriteAlkaliAdditives(
                name=partial_get(df_components[component], 'Additives. Compounds'),
                source=partial_get(
                    df_components[component], 'Sources of alkali doping'
                ),
                **handle_concentration(concentration),
            )
        )

    return additives if additives else None


def extract_chalcopyrite_composition(data_frame):
    """
    Extracts the composition from the data subframe and returns a list of Ion objects.
    """

    def get_coefficient(component_data):
        coefficient = partial_get(
            component_data,
            'Chalcopyrite. Composition. Ions. Coefficients',
            convert=True,
        )
        return coefficient if isinstance(coefficient, float | int) else None

    df_temp = data_frame[data_frame.index.str.contains('Chalcopyrite. Composition')]
    if df_temp.empty:
        return None

    df_components = split_data(df_temp, delimiter=';')
    ions = [
        Elemental(
            name=partial_get(
                df_components[component], 'Chalcopyrite. Composition. Ions '
            ),
            coefficient=get_coefficient(df_components[component]),
        )
        for component in df_components.columns
    ]

    additives = extract_chalcopyrite_additives(df_temp)

    return ChalcopyriteLayerComposition(
        ions=ions,
        additives=additives,
    )


def extract_thermal_annealing(data_frame):
    """
    Extracts the annealing conditions from the data subframe and
    returns a list of ThermalAnnealing objects.
    """
    df_temp = data_frame[data_frame.index.str.contains('Thermal annealing.')]
    if df_temp.empty:
        return []

    annealing = []
    df_temp = split_data(df_temp, delimiter=';')
    for column in df_temp.columns:
        atmosphere = partial_get(df_temp[column], 'Atmosphere')
        annealing_conditions = {
            'temperature': partial_get(df_temp[column], 'Temperature', unit='celsius'),
            'duration': partial_get(df_temp[column], 'Time', unit='minute'),
            'atmosphere': atmosphere
            if atmosphere in ThermalAnnealing.atmosphere.type
            else None,
        }
        if annealing_conditions['temperature'] is not None:
            annealing.append(ThermalAnnealing(**annealing_conditions))

    return annealing


def extract_solvent_annealing(data_frame):
    """
    Extracts the annealing conditions from the data subframe and
    returns a list of SolventAnnealing objects.
    """
    df_temp = data_frame[data_frame.index.str.contains('Solvent annealing.')]
    if df_temp.empty:
        return []

    annealing = []
    df_temp = split_data(df_temp, delimiter=';')
    for column in df_temp.columns:
        annealing_conditions = {
            'point_in_time': partial_get(df_temp[column], 'Time vs thermal annealing'),
            'atmosphere': partial_get(df_temp[column], 'atmosphere'),
            'duration': partial_get(df_temp[column], r'Time \[', unit='minute'),
            'temperature': partial_get(df_temp[column], 'Temperature', unit='celsius'),
        }
        if annealing_conditions['temperature'] is not None:
            annealing.append(SolventAnnealing(**annealing_conditions))

    return annealing


def extract_storage(data_frame):
    """
    Extracts the storage condition from the dataframe and
    returns a Storage object.
    """
    df_temp = data_frame[data_frame.index.str.contains('Storage. ')]
    if df_temp.empty:
        return None

    atmosphere = partial_get(df_temp, 'Atmosphere')
    humidity = partial_get(df_temp, 'Relative humidity', convert=True)
    storage_conditions = {
        'atmosphere': atmosphere if atmosphere in Storage.atmosphere.type else None,
        'time_until_next_step': partial_get(df_temp, 'Time until', unit='hour'),
        'humidity_relative': round(humidity / 100, 5) if humidity else None,
    }
    return Storage(**storage_conditions)


def extract_reference(data_frame):
    """
    Extracts the reference from the data subframe and
    returns a Reference object.
    """

    df_temp = data_frame[data_frame.index.str.contains('Ref. ')]

    reference_data = {
        'ID_temp': partial_get(df_temp, 'ID temp'),
        'DOI_number': partial_get(df_temp, 'DOI number'),
        'data_entered_by_author': partial_get(df_temp, 'Data entered by author'),
        'name_of_person_entering_the_data': partial_get(
            df_temp, 'Name of person entering the data'
        ),
        'free_text_comment': partial_get(df_temp, 'Free text comment'),
    }

    return Reference(**reference_data)


def extract_general(data_frame):
    """
    Extracts the general information from the data subframe and
    returns a General object.
    """
    # TODO: Can this used as quality check?
    df_temp = data_frame[data_frame.index.str.contains('Tandem.')]

    architecture = partial_get(df_temp, 'Tandem. Architecture')
    general_data = {
        'architecture': architecture
        if architecture in General.architecture.type
        else None,
        'number_of_terminals': partial_get(
            df_temp, 'Tandem. Number of terminals', convert=True
        ),
        'number_of_junctions': partial_get(
            df_temp, 'Tandem. Number of junctions', convert=True
        ),
        'number_of_cells': partial_get(
            df_temp, 'Tandem. Number of cells', convert=True
        ),
        'area': partial_get(df_temp, 'Tandem. Area. Total', unit='cm^2'),
        'area_measured': partial_get(df_temp, 'Tandem. Area. Measured', unit='cm^2'),
        'flexibility': partial_get(df_temp, 'Tandem. Flexible'),
        'semitransparent': partial_get(df_temp, 'Tandem. Semitransparent'),
        'contains_textured_layers': partial_get(df_temp, 'Textured layers'),
        'contains_antireflectie_coating': partial_get(
            df_temp, 'Antireflective coatings'
        ),
    }

    absorbers, bandgaps = [], []
    df_absorber = split_data(
        df_temp[df_temp.index.str.contains('Photoabsorbers')], delimiter='|'
    )
    for column in df_absorber.columns:
        absorber = partial_get(df_absorber[column], 'Photoabsorbers/tec')
        if absorber in General.photoabsorber.type:
            absorbers.append(absorber)
            bandgaps.append(
                partial_get(
                    df_absorber[column], 'Photoabsorbers. Band gaps', convert=True
                )
            )

    subcells = []
    df_subcells = split_data(
        df_temp[df_temp.index.str.contains('Subcells')], delimiter='|'
    )
    for column in df_subcells.columns:
        subcell_data = {
            'area': partial_get(df_subcells[column], 'Area', unit='cm^2'),
            'module': partial_get(df_subcells[column], 'Module', convert=True),
            'commercial_unit': partial_get(
                df_subcells[column], 'Comercial unit', convert=True
            ),
            'supplier': partial_get(df_subcells[column], 'Supplier'),
        }
        subcells.append(SubCell(**subcell_data))

    return General(
        **general_data,
        photoabsorber=absorbers,
        photoabsorber_bandgaps=bandgaps,
        subcell=subcells,
    )


def extract_layer_stack(data_frame):
    """
    Extracts the layer stack from the data subframe.
    """

    layer_stack = []

    # Filter out layers
    filtered_df = data_frame[data_frame.index.str.contains('Exist')]
    layer_labels = [
        idx.split('Exist')[0].strip() for idx, val in filtered_df.items() if val
    ]

    for label in layer_labels:
        # Filter dataframes by label
        df_layer = data_frame[data_frame.index.str.contains(label)]
        if df_layer.empty:
            continue

        # Cleaning
        cleaning = extract_cleaning(df_layer)

        # Deposition
        df_sublayers = split_data(df_layer, delimiter='|')
        for sublayer in df_sublayers.columns:
            df_sublayer = df_sublayers[sublayer]

            # Sublayer information
            functionality = partial_get(df_sublayer, 'Functionality')
            general_properties = {
                'functionality': functionality
                if functionality in Layer.functionality.type
                else None,
            }
            properties = {
                'thickness': partial_get(df_sublayer, 'Thickness', unit='nm'),
                'area': partial_get(df_sublayer, 'Area', unit='cm^2'),
                'surface_roughness': partial_get(
                    df_sublayer, 'Surface roughness', unit='nm'
                ),
            }

            additives = extract_additives(df_sublayer)

            # Split synthesis into single steps
            synthesis_steps = []
            if cleaning:
                synthesis_steps.append(cleaning)
            df_processes = split_data(df_sublayer, delimiter='>>')
            for syn_step in df_processes.columns:
                df_process = df_processes[syn_step]

                # Sublayer name
                general_properties['name'] = partial_get(df_process, 'Stack sequence ')

                # Synthesis process information
                aggregation_state_of_reactants = partial_get(
                    df_process, 'Aggregation state'
                )
                atmosphere = partial_get(df_process, 'Synthesis atmosphere ')
                humidity = partial_get(
                    df_process, 'atmosphere. Relative humidity', convert=True
                )
                # TODO: implement partial gas pressure
                process_conditions = {
                    'name': partial_get(df_process, 'Deposition. Procedure'),
                    'atmosphere': atmosphere
                    if atmosphere in DepositionStep.atmosphere.type
                    else None,
                    'aggregation_state_of_reactants': aggregation_state_of_reactants
                    if aggregation_state_of_reactants
                    in DepositionStep.aggregation_state_of_reactants.type
                    else None,
                    'pressure_total': partial_get(
                        df_process,
                        'atmosphere. Pressure. Total',
                        unit='mbar',
                    ),
                    'humidity_relative': round(humidity / 100, 5) if humidity else None,
                }

                # Liquid based synthesis
                if process_conditions['name'] in liquid_based_processes:
                    synthesis_steps.append(
                        LiquidSynthesis(
                            **process_conditions,
                            solvent=extract_solvents(df_process),
                            reactants=extract_reactants(df_process),
                            quenching_solvent=extract_quenching_solvents(df_process),
                        )
                    )

                # Physical vapour deposition & similar
                elif process_conditions['name'] in gas_phase_processes:
                    synthesis_steps.append(
                        GasPhaseSynthesis(
                            **process_conditions,
                            reactants=extract_reactants(df_process),
                        )
                    )

                # Thermal Annealing
                synthesis_steps.extend(extract_thermal_annealing(df_process))

            # Solvent Annealing (not part of the >> process scheme)
            # TODO: respect point_in_time quantity
            synthesis_steps.extend(extract_solvent_annealing(df_process))

            ## Synthesis
            treatment = partial_get(df_sublayer, 'Surface treatment')
            if (
                treatment
                and isinstance(treatment, str)
                and treatment.lower() not in ['none', 'nan']
            ):
                synthesis_steps.append(SurfaceTreatment(method=treatment))
            synthesis_properties = {
                'supplier': exact_get(df_sublayer, label + ' Supplier'),
                'supplier_brand': exact_get(df_sublayer, label + ' Brand name'),
            }
            bought_commercially = partial_get(df_sublayer, 'Bought commercially')
            if bought_commercially is True:
                synthesis_properties['origin'] = 'Commercial'
            elif bought_commercially is False or len(synthesis_steps) > 0:
                synthesis_properties['origin'] = 'Lab made'
            else:
                synthesis_properties['origin'] = 'Unknown'
            synthesis = Synthesis(**synthesis_properties, process_steps=synthesis_steps)

            # Storage conditions
            storage = extract_storage(df_sublayer)

            # Create composition for general layer types
            if additives:
                composition = LayerComposition(additives=additives)
            else:
                composition = None

            # Differentiate between type of layers
            if 'NAlayer' in label:
                if general_properties['functionality'] == 'Substrate':
                    layer_stack.append(
                        Substrate(
                            **general_properties,
                            properties=LayerProperties(**properties),
                            composition=composition,
                            synthesis=synthesis,
                            storage=storage,
                        )
                    )
                else:
                    layer_stack.append(
                        NonAbsorbingLayer(
                            **general_properties,
                            properties=LayerProperties(**properties),
                            composition=composition,
                            synthesis=synthesis,
                            storage=storage,
                        )
                    )
            elif 'P' in label:
                general_properties.update(
                    {
                        'name': partial_get(df_sublayer, 'Photoabsorber material'),
                    }
                )

                properties.update(
                    {
                        'bandgap': partial_get(df_sublayer, 'Band gap ', unit='eV'),
                        'bandgap_graded': partial_get(
                            df_sublayer, 'Band gap. Graded', convert=True
                        ),
                        'bandgap_estimation_basis': partial_get(
                            df_sublayer, 'Band gap. Estimation basis'
                        ),
                        'PL_max': partial_get(df_sublayer, 'Pl max', unit='nm'),
                    }
                )

                # Differentiate between absorber types
                if general_properties['name'] == 'Perovskite':
                    properties.update(
                        {
                            'single_crystal': partial_get(
                                df_sublayer, 'Single crystal'
                            ),
                            'inorganic': partial_get(
                                df_sublayer, 'Inorganic Perovskite'
                            ),
                            'lead_free': partial_get(df_sublayer, 'Lead free'),
                        }
                    )

                    layer_stack.append(
                        PerovskiteLayer(
                            **general_properties,
                            properties=PerovskiteLayerProperties(**properties),
                            composition=extract_perovskite_composition(df_sublayer),
                            synthesis=synthesis,
                            storage=storage,
                        )
                    )
                elif general_properties['name'] == 'Silicon':
                    properties.update(
                        {
                            'cell_type': partial_get(df_sublayer, 'Type of cell'),
                            'silicon_type': partial_get(df_sublayer, 'Type of silicon'),
                            'doping_sequence': partial_get(
                                df_sublayer, 'Doping sequence'
                            ),
                            'perovskite_inspired': None,
                        }
                    )
                    layer_stack.append(
                        SiliconLayer(
                            **general_properties,
                            properties=SiliconLayerProperties(**properties),
                            composition=composition,
                            synthesis=synthesis,
                            storage=storage,
                        )
                    )
                elif general_properties['name'] == 'CIGS':
                    layer_stack.append(
                        ChalcopyriteLayer(
                            **general_properties,
                            properties=PhotoAbsorberProperties(**properties),
                            composition=extract_chalcopyrite_composition(df_sublayer),
                            synthesis=synthesis,
                            storage=storage,
                        )
                    )
                else:
                    layer_stack.append(
                        PhotoAbsorberLayer(
                            **general_properties,
                            properties=PhotoAbsorberProperties(**properties),
                            composition=composition,
                            synthesis=synthesis,
                            storage=storage,
                        )
                    )

    return layer_stack


### Measurement extraction functions


def extract_jv_results(data_frame):
    """
    Extracts the JV results from the data subframe and returns a JVResults object.
    """
    pce = partial_get(data_frame, 'PCE', convert=True)
    return JVResults(
        short_circuit_current_density=partial_get(data_frame, 'Jsc', unit='mA/cm^2'),
        open_circuit_voltage=partial_get(data_frame, 'Voc', unit='V'),
        fill_factor=partial_get(data_frame, 'FF'),
        power_conversion_efficiency=round(pce / 100, 5) if pce else None,
        maximum_power_point_voltage=partial_get(data_frame, 'Vmp', unit='V'),
        maximum_power_point_current_density=partial_get(
            data_frame, 'Jmp', unit='mA/cm^2'
        ),
        resistance_series=partial_get(data_frame, 'Series resistance', unit='ohm*cm^2'),
        resistance_shunt=partial_get(data_frame, 'Shunt resistance', unit='ohm*cm^2'),
    )


def extract_jv(data_frame):
    """
    Extracts the JV measurements from the data subframe and returns a dictionary of JVMeasurement objects.
    """
    jv_dict = {}

    # Full device
    df_temp = data_frame[~data_frame.index.str.contains('Subcell')]
    if not df_temp.empty:
        component = 'Whole Device'
        source = 'This device'

        # Storage Information
        df_storage = df_temp[df_temp.index.str.contains('Storage.')]
        if not df_storage.empty:
            humidity = partial_get(df_storage, 'Relative humidity', convert=True)
            storage = Storage(
                atmosphere=partial_get(df_storage, 'Atmosphere'),
                time_until_next_step=partial_get(df_storage, 'Age of cell', unit='day'),
                humidity_relative=round(humidity / 100, 5) if humidity else None,
            )
        else:
            storage = None

        # Preconditioning Information
        df_preconditioning = df_temp[df_temp.index.str.contains('Preconditioning.')]
        if (
            not df_preconditioning.empty
            and partial_get(df_preconditioning, 'Procotol') is not None
        ):
            preconditioning = Preconditioning(
                protocol=partial_get(df_preconditioning, 'Procotol'),
                duration=partial_get(
                    df_preconditioning, 'Preconditioning. Time', unit='hour'
                ),
                potential=partial_get(
                    df_preconditioning, 'Preconditioning. Potential', unit='V'
                ),
                light_intensity=partial_get(
                    df_preconditioning,
                    'Preconditioning. Light intensity',
                    unit='mW/cm^2',
                ),
            )
        else:
            preconditioning = None

        # Illumination Information
        df_illumination = df_temp[df_temp.index.str.contains('Light')]
        if not df_illumination.empty:
            illumination = Illumination(
                type=partial_get(df_illumination, 'Type'),
                brand=partial_get(df_illumination, 'Brand name'),
                simulator_class=partial_get(df_illumination, 'Simulator class'),
                intensity=partial_get(df_illumination, 'Intensity', unit='mW/cm^2'),
                spectrum=partial_get(df_illumination, 'Spectra'),
                wavelength=partial_get(
                    df_illumination, 'Wavelength', unit='nm'
                ),  # TODO: check if this is correct
                direction=partial_get(df_illumination, 'Illumination direction')
                if partial_get(df_illumination, 'Illumination direction')
                in Illumination.direction.type
                else None,
                mask=partial_get(df_illumination, 'Masked cell'),
                mask_area=partial_get(df_illumination, 'Mask area', unit='cm^2'),
            )
        else:
            illumination = None

        # JV Conditions
        humidity = partial_get(df_temp, 'Test. Relative humidity', convert=True)
        conditions = JVConditions(
            atmosphere=partial_get(df_temp, 'Test. Atmosphere'),
            humidity_relative=round(humidity / 100, 5) if humidity else None,
            temperature=partial_get(df_temp, 'Test. Temperature', unit='celsius'),
            speed=partial_get(df_temp, 'Scan. Speed', unit='mV/s'),
            delay_time=partial_get(df_temp, 'Scan. Delay time', unit='ms'),
            integration_time=partial_get(df_temp, 'Scan. Integration time', unit='ms'),
            voltage_step=partial_get(df_temp, 'Scan. Voltage step', unit='mV'),
            illumination=illumination,
        )

        # JV Results
        # forward scan
        df_forward = df_temp[df_temp.index.str.contains('Forward scan.')]
        if not df_forward.empty:
            results = extract_jv_results(df_forward)
            jv_dict['jv_full_device_forward'] = JVMeasurement(
                component=component,
                source=source,
                results=results,
                storage=storage,
                preconditioning=preconditioning,
                conditions=conditions,
            )
        # reverse scan
        df_reverse = df_temp[df_temp.index.str.contains('Reverse scan.')]
        if not df_reverse.empty:
            results = extract_jv_results(df_reverse)
            jv_dict['jv_full_device_reverse'] = JVMeasurement(
                component=component,
                source=source,
                results=results,
                storage=storage,
                preconditioning=preconditioning,
                conditions=conditions,
            )

    # Subcell 1, Bottom Cell
    df_temp = data_frame[data_frame.index.str.contains('Subcell 1.')]
    if not df_temp.empty:
        component = 'Bottom Cell'
        if partial_get(df_temp, 'Cell is identical to cell') and not partial_get(
            df_temp, 'JV data is a best estimate based'
        ):
            source = 'This device'
        elif not partial_get(df_temp, 'Cell is identical to cell') and partial_get(
            df_temp, 'JV data is a best estimate based'
        ):
            source = 'Analogous free standing cell'
        else:
            source = 'Unknown'

        # not shaded
        df_subcell = df_temp[~df_temp.index.str.contains('Shaded by top cell')]
        if not df_subcell.empty:
            results = extract_jv_results(df_subcell)
            jv_dict['jv_bottom_cell'] = JVMeasurement(
                component=component, source=source, results=results
            )

        # shaded
        df_subcell = df_temp[df_temp.index.str.contains('Shaded by top cell')]
        if not df_subcell.empty:
            results = extract_jv_results(df_subcell)
            jv_dict['jv_bottom_cell_shaded'] = JVMeasurement(
                component=component, source=source, results=results
            )

    # Subcell 2, Top Cell
    df_temp = data_frame[data_frame.index.str.contains('Subcell 2.')]
    if not df_temp.empty:
        component = 'Top Cell'
        if partial_get(df_temp, 'Cell is identical to cell') and not partial_get(
            df_temp, 'JV data is a best estimate based'
        ):
            source = 'This device'
        elif not partial_get(df_temp, 'Cell is identical to cell') and partial_get(
            df_temp, 'JV data is a best estimate based'
        ):
            source = 'Analogous free standing cell'
        else:
            source = 'Unknown'

        # not shaded
        df_subcell = df_temp[~df_temp.index.str.contains('Shaded by top cell')]
        if not df_subcell.empty:
            results = extract_jv_results(df_subcell)
            jv_dict['jv_top_cell'] = JVMeasurement(
                component=component, source=source, results=results
            )

    return jv_dict


def extract_stabilised_performance(data_frame):
    """ """

    performance_dict = {}

    # Full device
    if partial_get(data_frame, 'Stabilised performance. Measured'):
        df_temp = data_frame[~data_frame.index.str.contains('Stacked cell')]

        # metric_value = partial_get(df_temp, 'Value')
        conditions = StabilisedPerformanceConditions(
            procedure=partial_get(df_temp, 'Procedure '),
            duration=partial_get(df_temp, 'Measurement time', unit='min'),
        )

        pce = partial_get(df_temp, 'PCE', convert=True)
        results = JVResults(
            power_conversion_efficiency=round(pce / 100, 5) if pce else None,
            maximum_power_point_voltage=partial_get(df_temp, 'Vmp', unit='V'),
            maximum_power_point_current_density=partial_get(
                df_temp, 'Jmp', unit='mA/cm^2'
            ),
        )

        performance_dict['stabilised_performance_full_device'] = StabilisedPerformance(
            component='Whole Device',
            conditions=conditions,
            results=results,
        )

    return performance_dict


def construct_eqe(intensity, jsc, component):
    """
    Constructs an ExternalQuantumEfficiency object from the given parameters.
    Helper function for extract_eqe.
    """

    if intensity is not None:
        illumination = Illumination(intensity=intensity)
        conditions = MeasurementConditions(illumination=illumination)
    else:
        conditions = None

    results = EQEResults(integrated_short_circuit_current_density=jsc)
    return ExternalQuantumEfficiency(
        component=component,
        results=results,
        conditions=conditions,
    )


def extract_eqe(data_frame):
    """
    Extracts the EQE measurements from the data subframe
    and returns a dictionary of ExternalQuantumEfficiency objects.
    """

    eqe_dict = {}

    # Full device
    df_temp = data_frame[data_frame.index.str.contains('Full cell')]
    if not df_temp.empty and partial_get(df_temp, 'Measured'):
        intensity = partial_get(df_temp, 'Light bias', unit='mW/cm^2')
        jsc = partial_get(df_temp, 'Full cell. Integrated Jsc', unit='mA/cm^2')
        if jsc is not None:
            eqe_dict['eqe_full_device'] = construct_eqe(intensity, jsc, 'Whole Device')

    # Subcell 1, Bottom Cell
    df_temp = data_frame[data_frame.index.str.contains('Subcell 1.')]
    if not df_temp.empty and partial_get(df_temp, 'Measured'):
        intensity = partial_get(df_temp, 'Light bias', unit='mW/cm^2')
        jsc = partial_get(df_temp, 'Subcell 1. Integrated Jsc', unit='mA/cm^2')
        jsc_shaded = partial_get(df_temp, 'Shaded. Integrated Jsc', unit='mA/cm^2')
        if jsc is not None:
            eqe_dict['eqe_bottom_cell'] = construct_eqe(intensity, jsc, 'Bottom Cell')
        if jsc_shaded is not None:
            eqe_dict['eqe_bottom_cell_shaded'] = construct_eqe(
                intensity, jsc_shaded, 'Bottom Cell'
            )

    # Subcell 2, Top Cell
    df_temp = data_frame[data_frame.index.str.contains('Subcell 2.')]
    if not df_temp.empty and partial_get(df_temp, 'Measured'):
        intensity = partial_get(df_temp, 'Light bias', unit='mW/cm^2')
        jsc = partial_get(df_temp, 'Subcell 2. Integrated Jsc', unit='mA/cm^2')
        if jsc is not None:
            eqe_dict['eqe_top_cell'] = construct_eqe(intensity, jsc, 'Top Cell')

    # TODO: Add more subcells and shaded measurements

    return eqe_dict


def extract_measurements(data_frame):
    """
    Extracts the measurements from the data subframe and returns a PerformedMeasurements object.
    """

    performed_measurements = {}

    # extract JV measurements
    df_temp = data_frame[data_frame.index.str.contains('JV.')]
    if not df_temp.empty:
        performed_measurements.update(extract_jv(df_temp))

    # extract stabilised performance measurements
    df_temp = data_frame[data_frame.index.str.contains('Stabilised performance.')]
    if not df_temp.empty:
        performed_measurements.update(extract_stabilised_performance(df_temp))

    # extract EQE measurements
    df_temp = data_frame[data_frame.index.str.contains('EQE.')]
    if not df_temp.empty:
        performed_measurements.update(extract_eqe(df_temp))

    return PerformedMeasurements(**performed_measurements)
