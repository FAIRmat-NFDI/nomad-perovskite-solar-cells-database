from typing import TYPE_CHECKING

import pandas as pd
from nomad.config import config
from nomad.datamodel.data import EntryData

# from nomad.parsing.tabular import create_archive
from nomad.datamodel.datamodel import EntryArchive
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.metainfo import Quantity
from nomad.parsing.parser import MatchingParser

from perovskite_tandem_database.parsers.utils import create_archive
from perovskite_tandem_database.schema_packages.schema import PerovskiteTandemSolarCell
from perovskite_tandem_database.schema_packages.tandem import (
    ChalcopyriteAlkaliMetalDoping,
    ChalcopyriteLayer,
    Cleaning,
    Element,
    GasPhaseSynthesis,
    General,
    Ion,
    LiquidSynthesis,
    NonAbsorbingLayer,
    PerovskiteComposition,
    PerovskiteLayer,
    PhotoAbsorber,
    QuenchingSolvent,
    Reference,
    SiliconLayer,
    Solvent,
    Substance,
    Substrate,
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
            column_data = cleanup(data_frame[col])

            stack = extract_layer_stack(column_data)
            general = General()
            reference = extract_reference(column_data)
            reference.normalize(archive, logger)

            tandem = PerovskiteTandemSolarCell(
                general=general, reference=reference, layer_stack=stack
            )

            entry_archive = EntryArchive(data=tandem)

            create_archive(
                entry_archive.m_to_dict(),
                archive.m_context,
                f'tandem.archive_{col}.json',
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


def cleanup(data_frame):
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
            expanded_data = split_data.apply(lambda x: x + [x[-1]] * (max_len - len(x)))
            # Append the data frame with unique column names and preserved index
            expanded_df = pd.DataFrame(expanded_data.tolist(), index=data.index)
            expanded_df.columns = [f'{column}_{i}' for i in range(max_len)]
            expanded_dfs.append(expanded_df)

        return pd.concat(expanded_dfs, axis=1)

    elif isinstance(data, pd.Series):
        split_data = data.apply(
            lambda x: str(x).split(delimiter) if isinstance(x, str) else [x]
        )
        max_len = split_data.apply(len).max()
        expanded_data = split_data.apply(lambda x: x + [x[-1]] * (max_len - len(x)))
        expanded_df = pd.DataFrame(expanded_data.tolist(), index=data.index)
        expanded_df.columns = [f'{data.name}_{i}' for i in range(max_len)]
        return expanded_df

    else:
        raise ValueError('Input data_frame must be a pandas DataFrame or Series')


def convert_value(value, default_unit=None):  # noqa: PLR0911
    """
    Attempts to convert the string value to its appropriate type (int, float, bool).
    Returns the original string if conversion is not possible.
    """
    import pint

    ureg = pint.UnitRegistry()
    if isinstance(value, str):
        value = value.strip()
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        try:
            number = int(value)
            return number * ureg(default_unit) if default_unit else number
        except ValueError:
            pass
        try:
            number = float(value)
            return number * ureg(default_unit) if default_unit else number
        except ValueError:
            pass
        try:
            quantity = ureg(value)
            if default_unit:
                return quantity.to(default_unit)
            return quantity
        except (pint.errors.UndefinedUnitError, ValueError):
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


def extract_additives(data_frame):
    """
    Extracts the additives from the data subframe.
    """
    additives = []
    df_temp = data_frame[data_frame.index.str.contains('Additives.')]
    if not df_temp.empty:
        df_components = split_data(df_temp, delimiter=';')
        for component in df_components.columns:
            additives_name = partial_get(
                df_components[component], 'Additives. Compounds'
            )
            additives_concentration = partial_get(
                df_components[component], 'Additives. Concentrations'
            )
            additives.append(
                Substance(name=additives_name, concentration=additives_concentration)
            )
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
            name = partial_get(df_components[component], 'Solvents ')
            mixing_ratio = partial_get(df_components[component], 'Mixing ratio')
            supplier = partial_get(df_components[component], 'Solvents. Supplier')
            purity = partial_get(df_components[component], 'Solvents. Purity')
            solvents.append(
                Solvent(
                    name=name,
                    mixing_ratio=mixing_ratio,
                    supplier=supplier,
                    purity=purity,
                )
            )
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
            name = partial_get(
                df_components[component], 'Reaction solutions. Compounds '
            )
            supplier = partial_get(
                df_components[component], 'Reaction solutions. Compounds. Supplier'
            )
            purity = partial_get(
                df_components[component], 'Reaction solutions. Compounds. Purity'
            )
            concentration = partial_get(
                df_components[component], 'Reaction solutions. Concentrations'
            )
            volume = partial_get(
                df_components[component], 'Reaction solutions. Volumes'
            )
            age = partial_get(df_components[component], 'Reaction solutions. Age')
            temperature = partial_get(
                df_components[component], 'Reaction solutions. Temperature'
            )
            reactants.append(
                Substance(
                    name=name,
                    supplier=supplier,
                    purity=purity,
                    concentration=concentration,
                    volume=volume,
                    age=age,
                    temperature=temperature,
                )
            )
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
            name = partial_get(df_components[component], 'Quenching media ')
            mixing_ratio = partial_get(
                df_components[component], 'Mixing media. Mixing ratios'
            )
            volume = partial_get(df_components[component], 'Quenching media. Volume')
            additive_name = partial_get(
                df_components[component], 'Quenching media. Additives'
            )
            additive_concentration = partial_get(
                df_components[component], 'Quenching media. Additives. Concentrations'
            )
            quenching_solvents.append(
                QuenchingSolvent(
                    name=name,
                    mixing_ratio=mixing_ratio,
                    volume=volume,
                    additive_name=additive_name,
                    additive_concentration=additive_concentration,
                )
            )
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
        df_components = split_data(df_temp, delimiter=';')
        for component in df_components.columns:
            ion_a_type = partial_get(
                df_components[component], 'Perovskite. Composition. Ion A type'
            )
            ion_a_coefficients = partial_get(
                df_components[component], 'Perovskite. Composition. Ion A concentration'
            )
            ion_b_type = partial_get(
                df_components[component], 'Perovskite. Composition. Ion B type'
            )
            ion_b_coefficients = partial_get(
                df_components[component], 'Perovskite. Composition. Ion B concentration'
            )
            ion_c_type = partial_get(
                df_components[component], 'Perovskite. Composition. Ion C type'
            )
            ion_c_coefficients = partial_get(
                df_components[component], 'Perovskite. Composition. Ion C concentration'
            )
            if ion_a_type:
                ions_a.append(Ion(ion_type=ion_a_type, coefficients=ion_a_coefficients))
            if ion_b_type:
                ions_b.append(Ion(ion_type=ion_b_type, coefficients=ion_b_coefficients))
            if ion_c_type:
                ions_c.append(Ion(ion_type=ion_c_type, coefficients=ion_c_coefficients))
    if len(ions_a) == 0 and len(ions_b) == 0 and len(ions_c) == 0:
        return None
    else:
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
            coefficients = partial_get(
                df_components[component],
                'Chalcopyrite. Composition. Ions. Coefficients',
            )
            composition.append(Ion(ion_type=ion_type, coefficients=coefficients))
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


def extract_reference(data_frame):
    """
    Extracts the reference from the data subframe.
    """
    df_temp = data_frame[data_frame.index.str.contains('Ref. ')]
    ID_temp = partial_get(df_temp, 'ID temp')
    DOI_number = partial_get(df_temp, 'DOI number')
    data_entered_by_author = partial_get(df_temp, 'Data entered by author')
    name_of_person_entering_the_data = partial_get(
        df_temp, 'Name of person entering the data'
    )
    free_text_comment = partial_get(df_temp, 'Free text comment')

    reference = Reference(
        ID_temp=ID_temp,
        DOI_number=DOI_number,
        data_entered_by_author=data_entered_by_author,
        name_of_person_entering_the_data=name_of_person_entering_the_data,
        free_text_comment=free_text_comment,
    )
    return reference


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
        cleaning_steps = []
        df_cleaning = df_layer[df_layer.index.str.contains('Cleaning')]
        if not df_cleaning.empty:
            df_cleaning = split_data(
                df_cleaning, delimiter='|'
            )  # probably not necessary
            df_cleaning = split_data(df_cleaning, delimiter='>>')
            for syn_step in df_cleaning.columns:
                cleaning_steps.append(
                    Cleaning(procedure=partial_get(df_cleaning[syn_step], 'Procedure'))
                )

        # Deposition
        df_sublayers = split_data(df_layer, delimiter='|')
        for sublayer in df_sublayers.columns:
            df_sublayer = df_sublayers[sublayer]

            # Sublayer information
            functionality = partial_get(df_sublayer, 'Functionality')
            thickness = partial_get(df_sublayer, 'Thickness')
            area = partial_get(df_sublayer, 'Area')
            surface_roughness = partial_get(df_sublayer, 'Surface roughness')
            bought_commercially = partial_get(df_sublayer, 'Bought commercially')
            if bought_commercially is None:
                origin = 'Unknown'
            elif bought_commercially is True:
                origin = 'Commercial'
            elif bought_commercially is False:
                origin = 'Lab made'
            supplier = exact_get(df_sublayer, 'Supplier')
            supplier_brand = partial_get(df_sublayer, 'Brand name')
            additives = extract_additives(df_sublayer)

            # Split synthesis into single steps
            synthesis = []
            df_processes = split_data(df_sublayer, delimiter='>>')
            for syn_step in df_processes.columns:
                df_process = df_processes[syn_step]
                name = partial_get(
                    df_process, 'Stack sequence '
                )  # TODO: check if this is correct

                # Synthesis process information
                procedure = partial_get(df_process, 'Deposition. Procedure')
                if procedure is not None:
                    aggr_state = partial_get(df_process, 'Aggregation state')
                    atmo = partial_get(df_process, 'Synthesis atmosphere ')
                    atmo_p_total = partial_get(
                        df_process, 'atmosphere. Pressure. Total', default_unit='mbar'
                    )
                    # atmo_p_partial = partial_get(df_process, "atmosphere. Pressure. Partial")
                    humidity_rel = partial_get(df_process, 'Relative humidity')

                    # Liquid based synthesis
                    if procedure in liquid_based_processes:
                        solvents = extract_solvents(df_process)
                        reactants = extract_reactants(df_process)
                        quenching_solvents = extract_quenching_solvents(df_process)
                        synthesis.append(
                            LiquidSynthesis(
                                aggregation_state_of_reactants=aggr_state,
                                atmosphere=atmo,
                                pressure_total=atmo_p_total,
                                humidity_relative=humidity_rel,
                                solvent=solvents,
                                reactant=reactants,
                                quenching_solvent=quenching_solvents,
                            )
                        )

                    # Physical vapour deposition & similar
                    elif procedure in gas_phase_processes:
                        synthesis.append(GasPhaseSynthesis())

            # Annealing etc!
            # Storage conditions
            storage = None

            # Differentiate between type of layers
            if 'NAlayer' in label:
                if functionality == 'Substrate':
                    layer_stack.append(
                        Substrate(
                            name=name,
                            functionality=functionality,
                            thickness=thickness,
                            area=area,
                            surface_roughness=surface_roughness,
                            origin=origin,
                            supplier=supplier,
                            supplier_brand=supplier_brand,
                            cleaning=cleaning_steps,
                        )
                    )
                else:
                    layer_stack.append(
                        NonAbsorbingLayer(
                            name=name,
                            functionality=functionality,
                            thickness=thickness,
                            area=area,
                            surface_roughness=surface_roughness,
                            origin=origin,
                            supplier=supplier,
                            supplier_brand=supplier_brand,
                            cleaning=cleaning_steps,
                            synthesis=synthesis,
                            storage=storage,
                            additives=additives,
                        )
                    )
            elif 'P' in label:
                absorber_type = partial_get(df_layer, 'Photoabsorber material')
                bandgap = partial_get(df_sublayer, 'Band gap ')
                bandgap_graded = partial_get(df_sublayer, 'Band gap. Graded')
                bandgap_estimation_basis = partial_get(
                    df_sublayer, 'Band gap. Estimation basis'
                )
                PL_max = partial_get(df_sublayer, 'Pl max')

                # Differentiate between absorber types
                if absorber_type == 'Perovskite':
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
                        dimension = dimension.split('Dimension. ')[1].split(' [')[0]

                    single_crystal = partial_get(df_sublayer, 'Single crystal')
                    inorganic = partial_get(df_sublayer, 'Inorganic Perovskite')
                    lead_free = partial_get(df_sublayer, 'Lead free')

                    composition = extract_perovskite_composition(df_sublayer)

                    layer_stack.append(
                        PerovskiteLayer(
                            name=name,
                            thickness=thickness,
                            area=area,
                            surface_roughness=surface_roughness,
                            bandgap=bandgap,
                            bandgap_graded=bandgap_graded,
                            bandgap_estimation_basis=bandgap_estimation_basis,
                            PL_max=PL_max,
                            dimension=dimension,
                            composition=composition,
                            single_crystal=single_crystal,
                            inorganic=inorganic,
                            lead_free=lead_free,
                            origin=origin,
                            supplier=supplier,
                            supplier_brand=supplier_brand,
                            cleaning=cleaning_steps,
                            synthesis=synthesis,
                            storage=storage,
                            additives=additives,
                        )
                    )
                elif absorber_type == 'Silicon':
                    cell_type = partial_get(df_sublayer, 'Type of cell')
                    silicon_type = partial_get(df_sublayer, 'Type of silicon')
                    doping_sequence = partial_get(df_sublayer, 'Doping sequence')

                    layer_stack.append(
                        SiliconLayer(
                            name=name,
                            thickness=thickness,
                            area=area,
                            surface_roughness=surface_roughness,
                            bandgap=bandgap,
                            bandgap_graded=bandgap_graded,
                            bandgap_estimation_basis=bandgap_estimation_basis,
                            PL_max=PL_max,
                            perovskite_inspired=None,
                            cell_type=cell_type,
                            silicon_type=silicon_type,
                            doping_sequence=doping_sequence,
                            origin=origin,
                            supplier=supplier,
                            supplier_brand=supplier_brand,
                            cleaning=cleaning_steps,
                            synthesis=synthesis,
                            storage=storage,
                            additives=additives,
                        )
                    )
                elif absorber_type == 'CIGS':
                    composition = extract_chalcopyrite_composition(df_sublayer)
                    alkali_metal_doping = extract_alkali_doping(df_sublayer)

                    layer_stack.append(
                        ChalcopyriteLayer(
                            name=name,
                            thickness=thickness,
                            area=area,
                            surface_roughness=surface_roughness,
                            bandgap=bandgap,
                            bandgap_graded=bandgap_graded,
                            bandgap_estimation_basis=bandgap_estimation_basis,
                            PL_max=PL_max,
                            composition=composition,
                            alkali_metal_doping=alkali_metal_doping,
                            perovskite_inspired=None,
                            origin=origin,
                            supplier=supplier,
                            supplier_brand=supplier_brand,
                            cleaning=cleaning_steps,
                            synthesis=synthesis,
                            storage=storage,
                            additives=additives,
                        )
                    )
                else:
                    layer_stack.append(
                        PhotoAbsorber(
                            name=name,
                            thickness=thickness,
                            area=area,
                            surface_roughness=surface_roughness,
                            bandgap=bandgap,
                            bandgap_graded=bandgap_graded,
                            bandgap_estimation_basis=bandgap_estimation_basis,
                            PL_max=PL_max,
                            perovskite_inspired=None,
                            origin=origin,
                            supplier=supplier,
                            supplier_brand=supplier_brand,
                            cleaning=cleaning_steps,
                            synthesis=synthesis,
                            storage=storage,
                            additives=additives,
                        )
                    )

    return layer_stack
