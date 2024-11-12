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

from perovskite_tandem_database.parsers.utils import create_archive
from perovskite_tandem_database.schema_packages.schema import PerovskiteTandemSolarCell
from perovskite_tandem_database.schema_packages.tandem import (
    ChalcopyriteAlkaliMetalDoping,
    ChalcopyriteLayer,
    Cleaning,
    CleaningStep,
    GasPhaseSynthesis,
    General,
    Ion,
    Layer,
    LiquidSynthesis,
    NonAbsorbingLayer,
    PerovskiteComposition,
    PerovskiteLayer,
    PhotoAbsorber,
    QuenchingSolvent,
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

            # Clean the data frame
            # Set proper Boolean values and remove rows with all NaN values
            column_data = cleanup_dataframe(data_frame[col])

            stack = extract_layer_stack(column_data)
            general = extract_general(column_data)
            reference = extract_reference(column_data)
            reference.normalize(archive, logger)

            tandem = PerovskiteTandemSolarCell(
                general=general, reference=reference, layer_stack=stack
            )

            entry_archive = EntryArchive(data=tandem)

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
    Cleans the data frame by setting proper Boolean values and removing rows with all NaN values.
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

    ureg = UnitRegistry()
    unit_pattern = re.compile(
        r'^(\d+(\.\d+)?|\.\d+)([eE][-+]?\d+)?\s*\w+([*/^]\w+)*(\s*[/()]\s*\w+)*$'
    )  # Matches ".9kg", "10mA", "1.5 kg", "2 cm^2/(V*s)", "1e-6 m" etc.

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


def extract_cleaning(data_frame):
    """
    Extracts the cleaning steps from the data subframe.
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
        return Cleaning(steps=cleaning_steps)


def extract_additives(data_frame):
    """
    Extracts the additives from the data subframe.
    """
    additives = []
    df_temp = data_frame[data_frame.index.str.contains('Additives.')]
    if not df_temp.empty:
        df_components = split_data(df_temp, delimiter=';')
        for component in df_components.columns:
            additives_properties = {
                'name': partial_get(df_components[component], 'Additives. Compounds'),
                'concentration': partial_get(
                    df_components[component], 'Additives. Concentrations'
                ),
            }
            additives.append(Substance(**additives_properties))
    if len(additives) == 0:
        return None
    else:
        return additives


def extract_solvents(data_frame):
    """
    Extracts the solvents from the data subframe.
    """
    solvents = []
    df_temp = data_frame[data_frame.index.str.contains('Solvents')]
    if not df_temp.empty:
        df_components = split_data(df_temp, delimiter=';')
        for component in df_components.columns:
            solvent_properties = {
                'name': partial_get(df_components[component], 'Solvents '),
                'mixing_ratio': partial_get(df_components[component], 'Mixing ratio'),
                'supplier': partial_get(df_components[component], 'Solvents. Supplier'),
                'purity': partial_get(df_components[component], 'Solvents. Purity'),
            }
            solvents.append(Solvent(**solvent_properties))
    if len(solvents) == 0:
        return None
    else:
        return solvents


def extract_reactants(data_frame):
    """
    Extracts the reactants from the data subframe.
    """
    reactants = []
    df_temp = data_frame[data_frame.index.str.contains('Reaction solutions.')]
    if not df_temp.empty:
        df_components = split_data(df_temp, delimiter=';')
        for component in df_components.columns:
            reactant_properties = {
                'name': partial_get(
                    df_components[component], 'Reaction solutions. Compounds '
                ),
                'supplier': partial_get(
                    df_components[component], 'Reaction solutions. Compounds. Supplier'
                ),
                'purity': partial_get(
                    df_components[component], 'Reaction solutions. Compounds. Purity'
                ),
                'concentration': partial_get(
                    df_components[component], 'Reaction solutions. Concentrations'
                ),
                'volume': partial_get(
                    df_components[component], 'Reaction solutions. Volumes'
                ),
                'age': partial_get(
                    df_components[component],
                    'Reaction solutions. Age',
                    default_unit='h',
                ),
                'temperature': partial_get(
                    df_components[component],
                    'Reaction solutions. Temperature',
                    default_unit='celsius',
                ),
            }

            reactants.append(Substance(**reactant_properties))
    if len(reactants) == 0:
        return None
    else:
        return reactants


def extract_quenching_solvents(data_frame):
    """
    Extracts the quenching solvents from the data subframe.
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
    Extracts the composition from the data subframe.
    """
    ions_a, ions_b, ions_c = [], [], []
    df_temp = data_frame[data_frame.index.str.contains('Perovskite. Composition')]
    if not df_temp.empty:
        df_components = split_data(
            df_temp[df_temp.index.str.contains('A-ions')], delimiter=';'
        )
        for component in df_components.columns:
            type = partial_get(df_components[component], '-ions ')
            coefficient = partial_get(df_components[component], '-ions. Coefficients ')
            if type:
                ions_a.append(Ion(ion_type=type, coefficient=coefficient))
        df_components = split_data(
            df_temp[df_temp.index.str.contains('B-ions')], delimiter=';'
        )
        for component in df_components.columns:
            type = partial_get(df_components[component], '-ions ')
            coefficient = partial_get(df_components[component], '-ions. Coefficients ')
            if type:
                ions_b.append(Ion(ion_type=type, coefficient=coefficient))
        df_components = split_data(
            df_temp[df_temp.index.str.contains('C-ions')], delimiter=';'
        )
        for component in df_components.columns:
            type = partial_get(df_components[component], '-ions ')
            coefficient = partial_get(df_components[component], '-ions. Coefficients ')
            if type:
                ions_c.append(Ion(ion_type=type, coefficient=coefficient))
    return PerovskiteComposition(ion_a=ions_a, ion_b=ions_b, ion_c=ions_c)


def extract_chalcopyrite_composition(data_frame):
    """
    Extracts the composition from the data subframe.
    """
    composition = []
    df_temp = data_frame[data_frame.index.str.contains('Chalcopyrite. Composition')]
    if not df_temp.empty:
        df_components = split_data(df_temp, delimiter=';')
        for component in df_components.columns:
            ion_type = partial_get(
                df_components[component], 'Chalcopyrite. Composition. Ions '
            )
            coefficient = partial_get(
                df_components[component],
                'Chalcopyrite. Composition. Ions. Coefficients',
            )
            composition.append(Ion(ion_type=ion_type, coefficient=coefficient))
    if len(composition) == 0:
        return None
    else:
        return composition


def extract_alkali_doping(data_frame):
    """
    Extracts the alkali doping from the data subframe.
    """
    alkali_doping = []
    df_temp = data_frame[data_frame.index.str.contains('lkali')]
    if not df_temp.empty:
        df_components = split_data(df_temp, delimiter=';')
        for component in df_components.columns:
            ion_type = partial_get(df_components[component], 'Alkali metal doping')
            source = partial_get(df_components[component], 'Sources of alkali doping')
            alkali_doping.append(
                ChalcopyriteAlkaliMetalDoping(ion_type=ion_type, source=source)
            )
    if len(alkali_doping) == 0:
        return None
    else:
        return alkali_doping


def extract_annealing(data_frame):
    """
    Extracts the annealing conditions from the data subframe.
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
                'temperature': partial_get(
                    df_temp[column], 'Temperature', default_unit='celsius'
                ),
                'duration': partial_get(df_temp[column], 'Time', default_unit='hour'),
                'atmosphere': atmosphere
                if atmosphere in ThermalAnnealing.atmosphere.type
                else None,
            }
            annealing.append(ThermalAnnealing(**annealing_conditions))
        return annealing


def extract_storage(data_frame):
    """
    Extracts the storage condition from the dataframe.
    """

    df_temp = data_frame[data_frame.index.str.contains('Storage. ')]
    if df_temp.empty:
        return None
    else:
        atmosphere = partial_get(df_temp, 'Atmosphere')
        storage_conditions = {
            'atmosphere': atmosphere if atmosphere in Storage.atmosphere.type else None,
            'time_until_next_step': partial_get(
                df_temp, 'Time until', default_unit='h'
            ),
            'humidity_relative': partial_get(df_temp, 'Relative humidity'),
        }
        return Storage(**storage_conditions)


def extract_reference(data_frame):
    """
    Extracts the reference from the data subframe.
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
    Extracts the general information from the data subframe.
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
    layer_labels = [idx.split('Exist')[0] for idx in filtered_df.index]

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
            synthesis = []
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
                    'humidity_relative': partial_get(
                        df_process, 'atmosphere. Relative humidity'
                    ),
                }

                # Liquid based synthesis
                if process_conditions['procedure'] in liquid_based_processes:
                    synthesis.append(
                        LiquidSynthesis(
                            **process_conditions,
                            solvent=extract_solvents(df_process),
                            reactant=extract_reactants(df_process),
                            quenching_solvent=extract_quenching_solvents(df_process),
                        )
                    )

                # Physical vapour deposition & similar
                elif process_conditions['procedure'] in gas_phase_processes:
                    synthesis.append(
                        GasPhaseSynthesis(
                            **process_conditions,
                            reactant=extract_reactants(df_process),
                        )
                    )

                # Annealing
                annealing = extract_annealing(df_process)
                if annealing:
                    synthesis.extend(annealing)

            # Storage conditions
            storage = extract_storage(df_sublayer)

            # Differentiate between type of layers
            if 'NAlayer' in label:
                if sublayer_properties['functionality'] == 'Substrate':
                    layer_stack.append(
                        Substrate(
                            **sublayer_properties,
                            cleaning=cleaning,
                            synthesis=synthesis,
                            storage=storage,
                        )
                    )
                else:
                    layer_stack.append(
                        NonAbsorbingLayer(
                            **sublayer_properties,
                            cleaning=cleaning,
                            synthesis=synthesis,
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

                    dimension = next(
                        (
                            idx
                            for idx in df_sublayer.index
                            if 'Dimension. ' in idx
                            and 'Dimension. List of layers' not in idx
                            and df_layer[idx]
                        ),
                        None,
                    )
                    if dimension:
                        perovskite_properties['dimension'] = dimension.split(
                            'Dimension. '
                        )[1].split(' [')[0]

                    layer_stack.append(
                        PerovskiteLayer(
                            **sublayer_properties,
                            **perovskite_properties,
                            composition=extract_perovskite_composition(df_sublayer),
                            cleaning=cleaning,
                            synthesis=synthesis,
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
                            synthesis=synthesis,
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
                            synthesis=synthesis,
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
                            synthesis=synthesis,
                            storage=storage,
                            additives=additives,
                        )
                    )

    return layer_stack
