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
    ChalcopyriteAlkaliMetalDoping,
    ChalcopyriteLayer,
    CleaningStep,
    GasPhaseSynthesis,
    General,
    Ion,
    Layer,
    LiquidSynthesis,
    NonAbsorbingLayer,
    # PerovskiteComposition,
    PerovskiteLayer,
    PhotoAbsorber,
    QuenchingSolvent,
    ReactionComponent,
    Reference,
    SiliconLayer,
    Solvent,
    Storage,
    SubCell,
    Substance,
    Substrate,
    SynthesisStep,
    ThermalAnnealing,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger


ureg = UnitRegistry()
ureg.define('% = 0.01 * [] = percent')
ureg.define('wt% = 0.01* [] = weight_percent')
ureg.define('vol% = 0.01* [] = volume_percent')

unit_pattern = re.compile(
    r'^(\d+(\.\d+)?|\.\d+)([eE][-+]?\d+)?\s*\w+([*/^]\w+)*(\s*[/()]\s*\w+)*$'
)  # Matches ".9kg", "10mA", "1.5 kg", "2 cm^2/(V*s)", "1e-6 m" etc.


class TandemParser(MatchingParser):
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
        logger.info('TandemParser.parse')
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
    Attempts to convert the string value to its appropriate type (int, float, bool).
    Returns the original string if conversion is not possible.
    """

    if unit and isinstance(value, (int, float)) and not isinstance(value, bool):
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


def partial_get(data, label, default=None, default_unit=None):
    """
    Extracts the first entry from a DataFrame or Series whose index partially matches a label.
    """
    df_matched = data[data.index.str.contains(label)]
    if df_matched.empty:
        return default
    else:
        if isinstance(data, pd.DataFrame):
            value = df_matched.iloc[0, 0]
        elif isinstance(data, pd.Series):
            value = df_matched.iloc[0]
        else:
            return default
        return convert_value(value, default_unit)


def exact_get(data, label, default=None, default_unit=None):
    """
    Extracts the first entry from a DataFrame or Series whose index exactly matches a label.
    """
    if label in data.index:
        if isinstance(data, pd.DataFrame):
            value = data.loc[label, data.columns[0]]
        elif isinstance(data, pd.Series):
            value = data.loc[label]
        return convert_value(value, default_unit)
    else:
        return default


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
            if 'gram' in str(concentration.units) or 'wt%' == str(concentration.units):
                result_dict['mass_fraction'] = concentration.to('g/g')
            elif 'liter' in str(concentration.units) or 'vol%' == str(
                concentration.units
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
    else:
        df_cleaning = split_data(df_cleaning, delimiter='|')  # probably not necessary
        df_cleaning = split_data(df_cleaning, delimiter='>>')
        cleaning_steps = []
        for syn_step in df_cleaning.columns:
            cleaning_steps.append(
                CleaningStep(name=partial_get(df_cleaning[syn_step], 'procedure'))
            )
        return cleaning_steps


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

    return additives if len(additives) > 0 else None


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
            'mixing_ratio': partial_get(df_components[component], 'Mixing ratio'),
            'supplier': partial_get(df_components[component], 'Solvents. Supplier'),
            'purity': partial_get(df_components[component], 'Solvents. Purity'),
        }
        solvents.append(Solvent(**solvent_properties))

    return solvents if len(solvents) > 0 else None


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
                default_unit='ml',
            ),
            'age': partial_get(
                df_components[component],
                'Reaction solutions. Age',
                default_unit='hour',
            ),
            'temperature': partial_get(
                df_components[component],
                'Reaction solutions. Temperature',
                default_unit='celsius',
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
    quenching_solvents = []
    df_temp = data_frame[data_frame.index.str.contains('Quenching media')]
    if not df_temp.empty:
        df_components = split_data(df_temp, delimiter=';')
        for component in df_components.columns:
            solvent_properties = {
                'name': partial_get(df_components[component], 'Quenching media '),
                'mixing_ratio': partial_get(
                    df_components[component], 'Mixing media. Mixing ratios'
                ),
                'volume': partial_get(
                    df_components[component], 'Quenching media. Volume'
                ),
                'additive_name': partial_get(
                    df_components[component], 'Quenching media. Additives'
                ),
                'additive_concentration': partial_get(
                    df_components[component],
                    'Quenching media. Additives. Concentrations',
                ),
            }
            quenching_solvents.append(QuenchingSolvent(**solvent_properties))

    if len(quenching_solvents) == 0:
        return None
    else:
        return quenching_solvents


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
        assumption = partial_get(df_temp, 'Assumption')
        if assumption:
            assumption = assumption.lower()
            if 'solution' in assumption:
                composition_estimate = 'Estimated from precursor solutions'
            elif 'literature' in assumption:
                composition_estimate = 'Literature value'
            elif 'xrd' in assumption:
                composition_estimate = 'Estimated from XRD data'
            elif 'spectroscop' in assumption:
                composition_estimate = 'Estimated from spectroscopic data'
            elif 'simulation' in assumption:
                composition_estimate = 'Theoretical simulation'
            elif 'hypothetical' in assumption:
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
            coefficient = partial_get(df_components[component], '-ions. Coefficients ')
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
            coefficient = partial_get(df_components[component], '-ions. Coefficients ')
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
            coefficient = partial_get(df_components[component], '-ions. Coefficients ')
            if type:
                ions_c.append(
                    PerovskiteXIonComponent(
                        abbreviation=abbreviation, coefficient=coefficient
                    )
                )
    return PerovskiteCompositionSection(
        ions_a_site=ions_a,
        ions_b_site=ions_b,
        ions_x_site=ions_c,
        dimensionality=dimensionality,
        composition_estimate=composition_estimate,
    )


def extract_chalcopyrite_composition(data_frame):
    """
    Extracts the composition from the data subframe and returns a list of Ion objects.
    """
    composition = []
    df_temp = data_frame[data_frame.index.str.contains('Chalcopyrite. Composition')]
    if not df_temp.empty:
        df_components = split_data(df_temp, delimiter=';')
        for component in df_components.columns:
            name = partial_get(
                df_components[component], 'Chalcopyrite. Composition. Ions '
            )
            coefficient = partial_get(
                df_components[component],
                'Chalcopyrite. Composition. Ions. Coefficients',
            )
            composition.append(Ion(name=name, coefficient=coefficient))
    if len(composition) == 0:
        return None
    else:
        return composition


def extract_alkali_doping(data_frame):
    """
    Extracts the alkali doping from the data subframe and
    returns a list of ChalcopyriteAlkaliMetalDoping objects.
    """
    alkali_doping = []
    df_temp = data_frame[data_frame.index.str.contains('lkali')]
    if not df_temp.empty:
        df_components = split_data(df_temp, delimiter=';')
        for component in df_components.columns:
            name = partial_get(df_components[component], 'Alkali metal doping')
            source = partial_get(df_components[component], 'Sources of alkali doping')
            alkali_doping.append(
                ChalcopyriteAlkaliMetalDoping(name=name, source=source)
            )
    if len(alkali_doping) == 0:
        return None
    else:
        return alkali_doping


def extract_annealing(data_frame):
    """
    Extracts the annealing conditions from the data subframe and
    returns a list of ThermalAnnealing objects.
    """
    df_temp = data_frame[data_frame.index.str.contains('Thermal annealing.')]

    if df_temp.empty:
        return None
    else:
        annealing = []
        df_temp = split_data(df_temp, delimiter=';')
        for column in df_temp.columns:
            atmosphere = partial_get(df_temp[column], 'Atmosphere')
            annealing_conditions = {
                'procedure': 'Thermal annealing',
                'temperature': partial_get(
                    df_temp[column], 'Temperature', default_unit='celsius'
                ),
                'duration': partial_get(df_temp[column], 'Time', default_unit='minute'),
                'atmosphere': atmosphere
                if atmosphere in ThermalAnnealing.atmosphere.type
                else None,
            }
            if annealing_conditions['temperature'] is not None:
                annealing.append(ThermalAnnealing(**annealing_conditions))
        return annealing


def extract_storage(data_frame):
    """
    Extracts the storage condition from the dataframe and
    returns a Storage object.
    """

    df_temp = data_frame[data_frame.index.str.contains('Storage. ')]
    if df_temp.empty:
        return None
    else:
        atmosphere = partial_get(df_temp, 'Atmosphere')
        humidity = partial_get(df_temp, 'Relative humidity')
        storage_conditions = {
            'atmosphere': atmosphere if atmosphere in Storage.atmosphere.type else None,
            'time_until_next_step': partial_get(
                df_temp, 'Time until', default_unit='hour'
            ),
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
        'number_of_terminals': partial_get(df_temp, 'Tandem. Number of terminals'),
        'number_of_junctions': partial_get(df_temp, 'Tandem. Number of junctions'),
        'number_of_cells': partial_get(df_temp, 'Tandem. Number of cells'),
        'area': partial_get(df_temp, 'Tandem. Area. Total', default_unit='cm^2'),
        'area_measured': partial_get(
            df_temp, 'Tandem. Area. Measured', default_unit='cm^2'
        ),
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
                partial_get(df_absorber[column], 'Photoabsorbers. Band gaps')
            )

    subcells = []
    df_subcells = split_data(
        df_temp[df_temp.index.str.contains('Subcells')], delimiter='|'
    )
    for column in df_subcells.columns:
        subcell_data = {
            'area': partial_get(df_subcells[column], 'Area', default_unit='cm^2'),
            'module': partial_get(df_subcells[column], 'Module'),
            'commercial_unit': partial_get(df_subcells[column], 'Comercial unit'),
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
            sublayer_properties = {
                'functionality': functionality
                if functionality in Layer.functionality.type
                else None,
                'thickness': partial_get(df_sublayer, 'Thickness', default_unit='nm'),
                'area': partial_get(df_sublayer, 'Area', default_unit='cm^2'),
                'surface_roughness': partial_get(
                    df_sublayer, 'Surface roughness', default_unit='nm'
                ),
                'supplier': partial_get(df_sublayer, 'Supplier'),
                'supplier_brand': partial_get(df_sublayer, 'Brand name'),
            }

            bought_commercially = partial_get(df_sublayer, 'Bought commercially')
            if bought_commercially is True:
                sublayer_properties['origin'] = 'Commercial'
            elif bought_commercially is False:
                sublayer_properties['origin'] = 'Lab made'
            else:
                sublayer_properties['origin'] = 'Unknown'

            additives = extract_additives(df_sublayer)

            # Split synthesis into single steps
            synthesis_steps = []
            df_processes = split_data(df_sublayer, delimiter='>>')
            for syn_step in df_processes.columns:
                df_process = df_processes[syn_step]

                # Sublayer name
                # TODO: check if this is correct
                sublayer_properties['name'] = partial_get(df_process, 'Stack sequence ')

                # Synthesis process information
                # atmo_p_partial = partial_get(df_process, "atmosphere. Pressure. Partial")
                aggregation_state_of_reactants = partial_get(
                    df_process, 'Aggregation state'
                )
                atmosphere = partial_get(df_process, 'Synthesis atmosphere ')
                humidity = partial_get(df_process, 'atmosphere. Relative humidity')
                process_conditions = {
                    'procedure': partial_get(df_process, 'Deposition. Procedure'),
                    'atmosphere': atmosphere
                    if atmosphere in SynthesisStep.atmosphere.type
                    else None,
                    'aggregation_state_of_reactants': aggregation_state_of_reactants
                    if aggregation_state_of_reactants
                    in SynthesisStep.aggregation_state_of_reactants.type
                    else None,
                    'pressure_total': partial_get(
                        df_process,
                        'atmosphere. Pressure. Total',
                        default_unit='mbar',
                    ),
                    'humidity_relative': round(humidity / 100, 5) if humidity else None,
                }

                # Liquid based synthesis
                if process_conditions['procedure'] in liquid_based_processes:
                    synthesis_steps.append(
                        LiquidSynthesis(
                            **process_conditions,
                            solvent=extract_solvents(df_process),
                            reactants=extract_reactants(df_process),
                            quenching_solvent=extract_quenching_solvents(df_process),
                        )
                    )

                # Physical vapour deposition & similar
                elif process_conditions['procedure'] in gas_phase_processes:
                    synthesis_steps.append(
                        GasPhaseSynthesis(
                            **process_conditions,
                            reactants=extract_reactants(df_process),
                        )
                    )

                # Annealing
                annealing = extract_annealing(df_process)
                if annealing:
                    synthesis_steps.extend(annealing)

            # Storage conditions
            storage = extract_storage(df_sublayer)

            # Differentiate between type of layers
            if 'NAlayer' in label:
                if sublayer_properties['functionality'] == 'Substrate':
                    layer_stack.append(
                        Substrate(
                            **sublayer_properties,
                            cleaning=cleaning,
                            synthesis=synthesis_steps,
                            storage=storage,
                        )
                    )
                else:
                    layer_stack.append(
                        NonAbsorbingLayer(
                            **sublayer_properties,
                            cleaning=cleaning,
                            synthesis=synthesis_steps,
                            storage=storage,
                            additives=additives,
                        )
                    )
            elif 'P' in label:
                sublayer_properties.update(
                    {
                        'name': partial_get(df_sublayer, 'Photoabsorber material'),
                        'bandgap': partial_get(df_sublayer, 'Band gap '),
                        'bandgap_graded': partial_get(df_sublayer, 'Band gap. Graded'),
                        'bandgap_estimation_basis': partial_get(
                            df_sublayer, 'Band gap. Estimation basis'
                        ),
                        'PL_max': partial_get(df_sublayer, 'Pl max'),
                    }
                )

                # Differentiate between absorber types
                if sublayer_properties['name'] == 'Perovskite':
                    perovskite_properties = {
                        'single_crystal': partial_get(df_sublayer, 'Single crystal'),
                        'inorganic': partial_get(df_sublayer, 'Inorganic Perovskite'),
                        'lead_free': partial_get(df_sublayer, 'Lead free'),
                    }

                    layer_stack.append(
                        PerovskiteLayer(
                            **sublayer_properties,
                            **perovskite_properties,
                            composition=extract_perovskite_composition(df_sublayer),
                            cleaning=cleaning,
                            synthesis=synthesis_steps,
                            storage=storage,
                            additives=additives,
                        )
                    )
                elif sublayer_properties['name'] == 'Silicon':
                    silicon_properties = {
                        'cell_type': partial_get(df_sublayer, 'Type of cell'),
                        'silicon_type': partial_get(df_sublayer, 'Type of silicon'),
                        'doping_sequence': partial_get(df_sublayer, 'Doping sequence'),
                    }

                    layer_stack.append(
                        SiliconLayer(
                            **sublayer_properties,
                            **silicon_properties,
                            perovskite_inspired=None,
                            cleaning=cleaning,
                            synthesis=synthesis_steps,
                            storage=storage,
                            additives=additives,
                        )
                    )
                elif sublayer_properties['name'] == 'CIGS':
                    layer_stack.append(
                        ChalcopyriteLayer(
                            **sublayer_properties,
                            composition=extract_chalcopyrite_composition(df_sublayer),
                            alkali_metal_doping=extract_alkali_doping(df_sublayer),
                            perovskite_inspired=None,
                            cleaning=cleaning,
                            synthesis=synthesis_steps,
                            storage=storage,
                            additives=additives,
                        )
                    )
                else:
                    layer_stack.append(
                        PhotoAbsorber(
                            **sublayer_properties,
                            perovskite_inspired=None,
                            cleaning=cleaning,
                            synthesis=synthesis_steps,
                            storage=storage,
                            additives=additives,
                        )
                    )

    return layer_stack


def extract_jv_results(data_frame):
    """
    Extracts the JV results from the data subframe and returns a JVResults object.
    """
    pce = partial_get(data_frame, 'PCE')
    return JVResults(
        short_circuit_current_density=partial_get(
            data_frame, 'Jsc', default_unit='mA/cm^2'
        ),
        open_circuit_voltage=partial_get(data_frame, 'Voc', default_unit='V'),
        fill_factor=partial_get(data_frame, 'FF'),
        power_conversion_efficiency=round(pce / 100, 5) if pce else None,
        maximum_power_point_voltage=partial_get(data_frame, 'Vmp', default_unit='V'),
        maximum_power_point_current_density=partial_get(
            data_frame, 'Jmp', default_unit='mA/cm^2'
        ),
        resistance_series=partial_get(
            data_frame, 'Series resistance', default_unit='ohm*cm^2'
        ),
        resistance_shunt=partial_get(
            data_frame, 'Shunt resistance', default_unit='ohm*cm^2'
        ),
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
            humidity = partial_get(df_storage, 'Relative humidity')
            storage = Storage(
                atmosphere=partial_get(df_storage, 'Atmosphere'),
                time_until_next_step=partial_get(
                    df_storage, 'Age of cell', default_unit='day'
                ),
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
                    df_preconditioning, 'Preconditioning. Time', default_unit='hour'
                ),
                potential=partial_get(
                    df_preconditioning, 'Preconditioning. Potential', default_unit='V'
                ),
                light_intensity=partial_get(
                    df_preconditioning,
                    'Preconditioning. Light intensity',
                    default_unit='mW/cm^2',
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
                intensity=partial_get(
                    df_illumination, 'Intensity', default_unit='mW/cm^2'
                ),
                spectrum=partial_get(df_illumination, 'Spectra'),
                wavelength=partial_get(
                    df_illumination, 'Wavelength', default_unit='nm'
                ),  # TODO: check if this is correct
                direction=partial_get(df_illumination, 'Illumination direction')
                if partial_get(df_illumination, 'Illumination direction')
                in Illumination.direction.type
                else None,
                mask=partial_get(df_illumination, 'Masked cell'),
                mask_area=partial_get(
                    df_illumination, 'Mask area', default_unit='cm^2'
                ),
            )
        else:
            illumination = None

        # JV Conditions
        humidity = partial_get(df_temp, 'Test. Relative humidity')
        conditions = JVConditions(
            atmosphere=partial_get(df_temp, 'Test. Atmosphere'),
            humidity_relative=round(humidity / 100, 5) if humidity else None,
            temperature=partial_get(
                df_temp, 'Test. Temperature', default_unit='celsius'
            ),
            speed=partial_get(df_temp, 'Scan. Speed', default_unit='mV/s'),
            delay_time=partial_get(df_temp, 'Scan. Delay time', default_unit='ms'),
            integration_time=partial_get(
                df_temp, 'Scan. Integration time', default_unit='ms'
            ),
            voltage_step=partial_get(df_temp, 'Scan. Voltage step', default_unit='mV'),
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
            duration=partial_get(df_temp, 'Measurement time', default_unit='min'),
        )

        pce = partial_get(df_temp, 'PCE')
        results = JVResults(
            power_conversion_efficiency=round(pce / 100, 5) if pce else None,
            maximum_power_point_voltage=partial_get(df_temp, 'Vmp', default_unit='V'),
            maximum_power_point_current_density=partial_get(
                df_temp, 'Jmp', default_unit='mA/cm^2'
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
        intensity = partial_get(df_temp, 'Light bias', default_unit='mW/cm^2')
        jsc = partial_get(df_temp, 'Full cell. Integrated Jsc', default_unit='mA/cm^2')
        if jsc is not None:
            eqe_dict['eqe_full_device'] = construct_eqe(intensity, jsc, 'Whole Device')

    # Subcell 1, Bottom Cell
    df_temp = data_frame[data_frame.index.str.contains('Subcell 1.')]
    if not df_temp.empty and partial_get(df_temp, 'Measured'):
        intensity = partial_get(df_temp, 'Light bias', default_unit='mW/cm^2')
        jsc = partial_get(df_temp, 'Subcell 1. Integrated Jsc', default_unit='mA/cm^2')
        jsc_shaded = partial_get(
            df_temp, 'Shaded. Integrated Jsc', default_unit='mA/cm^2'
        )
        if jsc is not None:
            eqe_dict['eqe_bottom_cell'] = construct_eqe(intensity, jsc, 'Bottom Cell')
        if jsc_shaded is not None:
            eqe_dict['eqe_bottom_cell_shaded'] = construct_eqe(
                intensity, jsc_shaded, 'Bottom Cell'
            )

    # Subcell 2, Top Cell
    df_temp = data_frame[data_frame.index.str.contains('Subcell 2.')]
    if not df_temp.empty and partial_get(df_temp, 'Measured'):
        intensity = partial_get(df_temp, 'Light bias', default_unit='mW/cm^2')
        jsc = partial_get(df_temp, 'Subcell 2. Integrated Jsc', default_unit='mA/cm^2')
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
