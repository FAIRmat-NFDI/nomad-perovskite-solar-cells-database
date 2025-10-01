import json
from importlib.resources import files
from typing import (
    TYPE_CHECKING,
)

from nomad.datamodel.data import ArchiveSection, Schema
from nomad.datamodel.metainfo.annotations import ELNComponentEnum
from nomad.datamodel.metainfo.basesections import PublicationReference
from nomad.datamodel.metainfo.eln import ELNAnnotation
from nomad.metainfo import JSON, Quantity, SchemaPackage, Section, SubSection
from nomad.metainfo.metainfo import MEnum, Reference
from nomad.units import ureg

from perovskite_solar_cell_database.composition import (
    PerovskiteCompositionSection,
    PerovskiteIonComponent,
)
from perovskite_solar_cell_database.schema import PerovskiteSolarCell
from perovskite_solar_cell_database.schema_sections.add import Add
from perovskite_solar_cell_database.schema_sections.backcontact import Backcontact
from perovskite_solar_cell_database.schema_sections.cell import Cell
from perovskite_solar_cell_database.schema_sections.encapsulation import Encapsulation
from perovskite_solar_cell_database.schema_sections.etl import ETL
from perovskite_solar_cell_database.schema_sections.htl import HTL
from perovskite_solar_cell_database.schema_sections.jv import JV
from perovskite_solar_cell_database.schema_sections.perovskite import Perovskite
from perovskite_solar_cell_database.schema_sections.perovskite_deposition import (
    PerovskiteDeposition,
)
from perovskite_solar_cell_database.schema_sections.ref import Ref
from perovskite_solar_cell_database.schema_sections.stability import (
    Stability as OriginalStability,
)
from perovskite_solar_cell_database.schema_sections.substrate import Substrate

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive


m_package = SchemaPackage()


with (
    files('perovskite_solar_cell_database')
    .joinpath('synonym_map.json')
    .open('r', encoding='utf-8') as f
):
    SYNONYM_MAP: dict[str, str] = json.load(f)


class SectionRevision(ArchiveSection):
    review_completed = Quantity(
        type=bool,
        description='True if the review of the data is completed',
        default=False,
        a_eln=ELNAnnotation(label='Review Completed', component='BoolEditQuantity'),
    )


class Ion(SectionRevision):
    m_def = Section(label='Ion')

    abbreviation = Quantity(
        type=str,
        description="The abbreviation used for the ion when writing the perovskite composition such as: 'Cs', 'MA', 'FA', 'PEA'",
        a_eln=ELNAnnotation(label='Abbreviation', component='StringEditQuantity'),
    )

    coefficient = Quantity(
        type=str,
        description='The stoichiometric coefficient of the ion such as “0.75”, or “1-x”.',
        a_eln=ELNAnnotation(label='Coefficient', component='StringEditQuantity'),
    )


class PerovskiteComposition(SectionRevision, PerovskiteCompositionSection):
    m_def = Section(label='Perovskite Composition')
    pass


# LightSource class
class LightSource(SectionRevision):
    m_def = Section(label='Light Source')

    type = Quantity(
        type=MEnum(
            [
                'AM 1.5G',
                'AM 1.5D',
                'AM 0',
                'Monochromatic',
                'White LED',
                'Other',
                'Outdoor',
                'Unknown',
            ]
        ),
        description='Type of light source',
        a_eln=ELNAnnotation(label='Light Source Type', component='EnumEditQuantity'),
    )

    description = Quantity(
        type=str,
        description='Additional details about the light source. This is very important.',
        a_eln=ELNAnnotation(label='Description', component='StringEditQuantity'),
    )

    light_intensity = Quantity(
        type=float,
        unit='mW/cm**2',
        description='Light intensity value',
        a_eln=ELNAnnotation(
            label='Light Intensity',
            component='NumberEditQuantity',
            defaultDisplayUnit='mW/cm**2',
            props=dict(minValue=0),
        ),
    )

    lamp = Quantity(
        type=str,
        description='Type of lamp used to generate the spectrum',
        a_eln=ELNAnnotation(label='Lamp', component='StringEditQuantity'),
    )


class Solute(SectionRevision):
    m_def = Section(label='Solute')

    name = Quantity(
        type=str,
        description='Name of the solute',
        a_eln=ELNAnnotation(label='Name', component='StringEditQuantity'),
    )

    concentration = Quantity(
        type=float,
        description='Concentration value',
        a_eln=ELNAnnotation(label='Concentration', component='NumberEditQuantity'),
    )

    concentration_unit = Quantity(
        type=MEnum(
            ['mol/L', 'mmol/L', 'g/L', 'mg/L', 'mg/mL', 'wt%', 'vol%', 'M', 'Unknown']
        ),
        description='Unit of concentration',
        a_eln=ELNAnnotation(label='Concentration Unit', component='EnumEditQuantity'),
    )


# Stability class
class Stability(LightSource):
    time = Quantity(
        type=float,
        unit='hour',
        description='Duration of the stability test',
        a_eln=ELNAnnotation(
            label='Time', defaultDisplayUnit='hour', component='NumberEditQuantity'
        ),
    )

    light_intensity = Quantity(
        type=float,
        unit='mW/cm**2',
        description='Light intensity during stability test',
        a_eln=ELNAnnotation(
            label='Light Intensity',
            component='NumberEditQuantity',
            defaultDisplayUnit='mW/cm**2',
            props=dict(minValue=0),
        ),
    )

    humidity = Quantity(
        type=float,
        description='The ambient humidity as a percentage without the % sign (i.e. a value between 0 and 100). When measurements are done in an inert atmosphere, this should be 0. If the humidity is fluctuating, use the average value.',
        a_eln=ELNAnnotation(
            label='Humidity',
            component='NumberEditQuantity',
            props=dict(minValue=0, maxValue=100),
        ),
    )

    temperature = Quantity(
        type=float,
        unit='°C',
        description='Temperature during stability test',
        a_eln=ELNAnnotation(
            label='Temperature', defaultDisplayUnit='°C', component='NumberEditQuantity'
        ),
    )

    PCE_T80 = Quantity(
        type=float,
        unit='hour',
        description='The time after which the cell performance has degraded by 20% with respect to the initial performance.',
        a_eln=ELNAnnotation(
            label='PCE T80', defaultDisplayUnit='hour', component='NumberEditQuantity'
        ),
    )

    PCE_at_start = Quantity(
        type=float,
        description='PCE at the start of the experiment as a percentage without the % sign.',
        a_eln=ELNAnnotation(label='PCE at Start', component='NumberEditQuantity'),
    )

    PCE_after_1000_hours = Quantity(
        type=float,
        description='PCE after 1000 hours as a percentage without the % sign.',
        a_eln=ELNAnnotation(
            label='PCE after 1000 Hours', component='NumberEditQuantity'
        ),
    )

    PCE_at_end = Quantity(
        type=float,
        description='PCE at the end of the experiment as a percentage without the % sign.',
        a_eln=ELNAnnotation(label='PCE at End', component='NumberEditQuantity'),
    )

    potential_bias = Quantity(
        type=MEnum(
            [
                'Open circuit',
                'MPPT',
                'Constant potential',
                'Constant current',
                'Constant resistance',
                'Unknown',
            ]
        ),
        description='Potential bias during stability test',
        a_eln=ELNAnnotation(label='Potential Bias', component='EnumEditQuantity'),
    )


class Solvent(SectionRevision):
    m_def = Section(label='Solvent')

    name = Quantity(
        type=str,
        description='Name of the solvent',
        a_eln=ELNAnnotation(label='Name', component='StringEditQuantity'),
    )

    volume_fraction = Quantity(
        type=float,
        description='The volume fraction of the solvent with respect to the other solvents in the solution',
        a_eln=ELNAnnotation(label='Volume Fraction', component='NumberEditQuantity'),
    )


# ReactionSolution class
class ReactionSolution(SectionRevision):
    m_def = Section(label='Reaction Solution')

    solutes = SubSection(
        section_def=Solute, repeats=True, a_eln=ELNAnnotation(label='Solutes')
    )

    volume = Quantity(
        type=float,
        unit='L',
        description='This volume is the volume of solution used in the experiment, e.g. the solvent volume that is spin-coated rather than the volume of the stock solution.',
        a_eln=ELNAnnotation(
            label='Volume', defaultDisplayUnit='L', component='NumberEditQuantity'
        ),
    )

    temperature = Quantity(
        type=float,
        unit='°C',
        description='Temperature of the solution',
        a_eln=ELNAnnotation(
            label='Temperature', defaultDisplayUnit='°C', component='NumberEditQuantity'
        ),
    )

    solvents = SubSection(
        section_def=Solvent, repeats=True, a_eln=ELNAnnotation(label='Solvents')
    )


# ProcessingStep class
class ProcessingStep(SectionRevision):
    m_def = Section(label='Processing Step', label_quantity='method')

    step_name = Quantity(
        type=str,
        description='Name of the processing step',
        a_eln=ELNAnnotation(label='Step Name', component='StringEditQuantity'),
    )

    method = Quantity(
        type=str,
        description='This is the method for the processing of steps in the design of the cells. Some examples are: Spin-coating, Drop-infiltration, Evaporation, Co-evaporation, Doctor blading, Spray coating, Slot-die coating, Ultrasonic spray, Dropcasting, Inkjet printing, Electrospraying, Thermal-annealing, Antisolvent-quenching',
        a_eln=ELNAnnotation(label='Method', component='StringEditQuantity'),
    )

    atmosphere = Quantity(
        type=MEnum(
            [
                'Ambient air',
                'Dry air',
                'Air',
                'N2',
                'Ar',
                'He',
                'H2',
                'Vacuum',
                'Other',
                'Unknown',
            ]
        ),
        description='Atmosphere during the step',
        a_eln=ELNAnnotation(label='Atmosphere', component='EnumEditQuantity'),
    )

    temperature = Quantity(
        type=float,
        unit='°C',
        description='The temperature during the deposition step. Depending on the circumstances the most relevant temperature could be either the ambient temperature, the substrate temperature, or the solution temperature.',
        a_eln=ELNAnnotation(
            label='Temperature', defaultDisplayUnit='°C', component='NumberEditQuantity'
        ),
    )

    duration = Quantity(
        type=float,
        unit='s',
        description='Duration of the step',
        a_eln=ELNAnnotation(
            label='Duration', defaultDisplayUnit='s', component='NumberEditQuantity'
        ),
    )

    solution = SubSection(
        section_def=ReactionSolution, a_eln=ELNAnnotation(label='Solution')
    )

    antisolvent = Quantity(
        type=str,
        description='Any antisolvent(s) used in the processing step. Separate multiple antisolvents with a semicolon (;).',
        a_eln=ELNAnnotation(label='Antisolvent', component='StringEditQuantity'),
    )

    additional_parameters = Quantity(
        type=JSON,
        description='Any additional parameters specific to this processing step',
        a_eln=ELNAnnotation(label='Additional Parameters'),
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = SYNONYM_MAP.get(self.method, self.method)


# Deposition class
class Deposition(SectionRevision):
    steps = SubSection(
        section_def=ProcessingStep,
        repeats=True,
        description='List of processing steps in order of execution. Only report conditions that have reported in the paper.',
    )

    reviewer_additional_notes = Quantity(
        type=str,
        description='Any additional comments or observations',
        a_eln=ELNAnnotation(label='Additional Notes', component='RichTextEditQuantity'),
    )

    additional_notes = Quantity(
        type=str, description='Any additional comments or observations'
    )


# Layer class
class Layer(SectionRevision):
    name = Quantity(
        type=str,
        description='Name of the layer',
        a_eln=ELNAnnotation(label='Layer Name', component='StringEditQuantity'),
    )

    thickness = Quantity(
        type=float,
        unit='nm',
        description='Thickness of the layer',
        a_eln=ELNAnnotation(
            label='Thickness',
            component='NumberEditQuantity',
            defaultDisplayUnit='nm',
            props=dict(minValue=0),
        ),
    )

    functionality = Quantity(
        type=MEnum(
            [
                'Hole-transport',
                'Electron-transport',
                'Contact',
                'Absorber',
                'Other',
                'Substrate',
                'Unknown',
            ]
        ),
        description='Functionality of the layer',
        a_eln=ELNAnnotation(label='Functionality', component='EnumEditQuantity'),
    )

    deposition = SubSection(
        section_def=ProcessingStep,
        a_eln=ELNAnnotation(label='Deposition'),
        repeats=True,
    )

    additional_treatment = Quantity(
        type=str,
        description="""Description of modifications applied to this layer beyond its basic composition, including:

- Self-assembled monolayers (SAMs)
- Surface passivation treatments
- Interface engineering (e.g., Lewis base/acid treatments)
- Additives or dopants
- Post-deposition treatments

Use established terminology: "SAM" for self-organized molecular layers, "surface passivation", "doping" where applicable.""",
        a_eln=ELNAnnotation(
            label='Additional Treatment', component='StringEditQuantity'
        ),
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.name = SYNONYM_MAP.get(self.name, self.name)


class ExtractionMetadata(SectionRevision):
    git_commit = Quantity(
        type=str,
        description='Link to git commit of the extraction code',
        a_eln=ELNAnnotation(component=ELNComponentEnum.URLEditQuantity),
    )

    model = Quantity(
        type=str,
        description='Model used for extraction',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
    )

    model_version = Quantity(
        type=str,
        description='Version of the model used for extraction',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
    )


# PerovskiteSolarCell class
class LLMExtractedPerovskiteSolarCell(PublicationReference, SectionRevision, Schema):
    m_def = Section(label='LLM Extracted Perovskite Solar Cell')

    DOI_number = Quantity(
        type=str,
        description='DOI number of the publication',
        a_eln=ELNAnnotation(label='DOI Number', component='URLEditQuantity'),
    )

    perovskite_composition = SubSection(
        section_def=PerovskiteComposition,
        a_eln=ELNAnnotation(label='Perovskite Composition'),
    )

    device_architecture = Quantity(
        type=MEnum(
            ['pin', 'nip', 'Back contacted', 'Front contacted', 'Other', 'Unknown']
        ),
        description='Device architecture',
        a_eln=ELNAnnotation(label='Device Architecture', component='EnumEditQuantity'),
    )

    pce = Quantity(
        type=float,
        description="""This is the device efficiency in %. Make sure to convert it to a percentage if it's given as a fraction before reporting.
Sometimes several different PCE values are presented for the same device. It could be a stabilized efficiency, a value extracted from a reversed JV scan, a value extracted from a forward JV scan. Only state one value. If several values are present for the device The priority is: Stabilized values is preferred before JV data from the reverse scan which is preferred before JV values from the forward scan.""",
        a_eln=ELNAnnotation(
            label='PCE',
            component='NumberEditQuantity',
            props=dict(minValue=0, maxValue=40),
        ),
    )

    jsc = Quantity(
        type=float,
        unit='mA/cm**2',
        description='Short-circuit current density (JSC)',
        a_eln=ELNAnnotation(
            label='JSC', defaultDisplayUnit='mA/cm**2', component='NumberEditQuantity'
        ),
    )

    voc = Quantity(
        type=float,
        unit='V',
        description='Open-circuit voltage (VOC)',
        a_eln=ELNAnnotation(
            label='VOC', component='NumberEditQuantity', props=dict(minValue=0)
        ),
    )

    ff = Quantity(
        type=float,
        description='This field requires the fill factor as a percentage without the % sign. If the fill factor is given as a fraction, e.g. 0.2, convert it to and write it as 20 without any percentage sign (%).',
        a_eln=ELNAnnotation(
            label='Fill Factor',
            component='NumberEditQuantity',
            props=dict(minValue=0, maxValue=100),
        ),
    )

    active_area = Quantity(
        type=float,
        unit='cm**2',
        description='Reported active area of the solar cell.',
        a_eln=ELNAnnotation(
            label='Active Area',
            component='NumberEditQuantity',
            defaultDisplayUnit='cm**2',
            props=dict(minValue=0),
        ),
    )

    number_devices = Quantity(
        type=int,
        description='Number of devices over which the metrics have been averaged',
        a_eln=ELNAnnotation(label='Number of Devices', component='NumberEditQuantity'),
    )

    averaged_quantities = Quantity(
        type=bool,
        description='True if metrics are averaged over multiple devices',
        a_eln=ELNAnnotation(label='Averaged Quantities', component='BoolEditQuantity'),
    )

    light_source = SubSection(
        section_def=LightSource, a_eln=ELNAnnotation(label='Light Source')
    )

    encapsulated = Quantity(
        type=bool,
        description='True if the device is encapsulated',
        a_eln=ELNAnnotation(label='Encapsulated', component='BoolEditQuantity'),
    )

    reviewer_additional_notes = Quantity(
        type=str,
        description='Any additional comments or observations',
        a_eln=ELNAnnotation(label='Additional Notes', component='RichTextEditQuantity'),
    )

    additional_notes = Quantity(
        type=str, description='Any additional comments or observations'
    )

    stability = SubSection(
        section_def=Stability, a_eln=ELNAnnotation(label='Stability')
    )

    layers = SubSection(
        section_def=Layer, repeats=True, a_eln=ELNAnnotation(label='Layers')
    )

    layer_order = Quantity(
        type=str,
        description='Order of the layers in the device stack. Use the layer names as they appear in the "Layers" section, separated by "|". If you want to add a missing layer, please add it first to the Layers section below. Then make sure to add the name of the layer, as you list it below, in this field in the right order. When you hit save on the top right, the correct order will be set on the layers in the Layers section below.',
        a_eln=ELNAnnotation(label='Layer Order', component='StringEditQuantity'),
    )

    classic_entry = Quantity(
        type=Reference(PerovskiteSolarCell.m_def),
        description='This is the classic schema entry that is generated from this LLM extracted entry. It is generated when the entry is normalized and saved and does not need to be filled.',
    )

    extraction_metadata = SubSection(
        section_def=ExtractionMetadata,
    )

    def normalize(self, archive: 'EntryArchive', logger):
        super().normalize(archive, logger)
        layer_dict = {
            SYNONYM_MAP.get(layer.name, layer.name): layer for layer in self.layers
        }
        if self.layer_order:
            ordered_names = [
                SYNONYM_MAP.get(name.strip(), name.strip())
                for name in self.layer_order.split('|')
            ]
            self.layer_order = ' | '.join(ordered_names)

            if set(ordered_names) != set(layer_dict.keys()):
                logger.warn('The names in layer_order does not match available layers')
                self.layer_order = ' | '.join(layer_dict.keys())
            else:
                self.layers = [layer_dict[name] for name in ordered_names]
        else:
            self.layer_order = ' | '.join(layer_dict.keys())
        # Generate the classic schema entry
        mainfile_list = archive.metadata.mainfile.split('.')
        mainfile_list[-3] += '_classic'
        mainfile = '.'.join(mainfile_list)
        if (
            isinstance(self.extraction_metadata, ExtractionMetadata)
            and self.extraction_metadata.model
        ):
            llm_extraction_name = f'LLM Extraction by {self.extraction_metadata.model}'
        else:
            llm_extraction_name = 'LLM Extraction'
        with archive.m_context.update_entry(
            mainfile, write=True, process=True
        ) as entry:
            entry['data'] = llm_to_classic_schema(
                self, llm_extraction_name=llm_extraction_name
            ).m_to_dict(with_root_def=True)
            entry['results'] = dict(material={})
        self.classic_entry = get_reference(
            upload_id=archive.metadata.upload_id, mainfile=mainfile
        )


def get_reference(upload_id: str, mainfile: str) -> str:
    from nomad.utils import hash

    entry_id = hash(upload_id, mainfile)
    return f'../uploads/{upload_id}/archive/{entry_id}#data'


def quantity_to_str(quantity):
    if isinstance(quantity, ureg.Quantity):
        return format(quantity.magnitude, '.10g')
    elif isinstance(quantity, int | float):
        return format(quantity, '.10g')
    return 'nan'


def add_to_pipe_separated_list(existing: str | None, addition: str | None) -> str:
    if not addition:
        return existing or 'Unknown'
    if existing:
        return existing + ' | ' + addition
    else:
        return addition or 'Unknown'


def set_layer_properties(
    layer: ETL | HTL | Backcontact | Substrate | Perovskite | PerovskiteDeposition,
    llm_layer: Layer,
):
    """
    Set the properties of the classic layer based on the LLM extracted layer.
    """
    depositions: list[ProcessingStep] = llm_layer.deposition
    thermal_annealing_steps = [
        step for step in depositions if step.method == 'Thermal-annealing'
    ]
    depositions = [step for step in depositions if step.method != 'Thermal-annealing']
    if isinstance(layer, PerovskiteDeposition):
        layer.procedure = ' >> '.join(
            deposition.method if deposition.method is not None else 'Unknown'
            for deposition in depositions
        )
        layer.number_of_deposition_steps = len(depositions)
    elif not isinstance(layer, Perovskite):
        layer.stack_sequence = add_to_pipe_separated_list(
            layer.stack_sequence, llm_layer.name
        )
        layer.deposition_procedure = add_to_pipe_separated_list(
            layer.deposition_procedure,
            ' >> '.join(
                deposition.method if deposition.method is not None else 'Unknown'
                for deposition in depositions
            ),
        )
    if isinstance(layer, HTL | Backcontact):
        layer.thickness_list = add_to_pipe_separated_list(
            layer.thickness_list, quantity_to_str(llm_layer.thickness)
        )
    elif not isinstance(layer, PerovskiteDeposition):
        layer.thickness = add_to_pipe_separated_list(
            layer.thickness, quantity_to_str(llm_layer.thickness)
        )
    if isinstance(layer, Substrate):
        layer.cleaning_procedure = llm_layer.additional_treatment
    elif not isinstance(layer, PerovskiteDeposition):
        layer.surface_treatment_before_next_deposition_step = (
            add_to_pipe_separated_list(
                layer.surface_treatment_before_next_deposition_step,
                llm_layer.additional_treatment,
            )
        )
    if isinstance(layer, Perovskite | Substrate):
        return
    atmospheres = []
    temperatures = []
    quenched = False
    antisolvents = []
    solvents = []
    solvent_fractions = []
    solutes = []
    solute_concentrations = []
    solution_temperatures = []
    volumes = []
    annealing_temperatures = []
    annealing_durations = []
    annealing_atmospheres = []
    for deposition in depositions:
        atmospheres.append(
            deposition.atmosphere if deposition.atmosphere else 'Unknown'
        )
        temperatures.append(
            quantity_to_str(deposition.temperature)
            if deposition.temperature is not None
            else 'nan'
        )
        if deposition.antisolvent:
            antisolvents.append(deposition.antisolvent)
            quenched = True
        if isinstance(deposition.solution, ReactionSolution):
            solution_temperatures.append(
                quantity_to_str(deposition.solution.temperature)
                if deposition.solution.temperature is not None
                else 'nan'
            )
            volumes.append(
                quantity_to_str(deposition.solution.volume)
                if deposition.solution.volume is not None
                else 'nan'
            )
            if deposition.solution.solvents:
                step_solvents = []
                step_solvent_fractions = []
                solvent: Solvent
                for solvent in deposition.solution.solvents:
                    step_solvents.append(solvent.name)
                    step_solvent_fractions.append(
                        quantity_to_str(solvent.volume_fraction)
                        if solvent.volume_fraction is not None
                        else 'nan'
                    )
                solvents.append('; '.join(step_solvents))
                solvent_fractions.append('; '.join(step_solvent_fractions))
            else:
                solvents.append('Unknown')
                solvent_fractions.append('nan')
            if deposition.solution.solutes:
                step_solutes = []
                step_solute_concentrations = []
                solute: Solute
                for solute in deposition.solution.solutes:
                    step_solutes.append(solute.name)
                    step_solute_concentrations.append(
                        f'{quantity_to_str(solute.concentration)} {solute.concentration_unit}'
                    )
                solutes.append('; '.join(step_solutes))
                solute_concentrations.append('; '.join(step_solute_concentrations))
            else:
                solutes.append('Unknown')
                solute_concentrations.append('nan')
    if thermal_annealing_steps:
        for step in thermal_annealing_steps:
            annealing_temperatures.append(
                quantity_to_str(step.temperature)
                if step.temperature is not None
                else 'nan'
            )
            annealing_durations.append(
                quantity_to_str(step.duration) if step.duration is not None else 'nan'
            )
            annealing_atmospheres.append(
                step.atmosphere if step.atmosphere else 'Unknown'
            )
    if isinstance(layer, ETL | HTL | Backcontact):
        layer.deposition_synthesis_atmosphere = add_to_pipe_separated_list(
            layer.deposition_synthesis_atmosphere, ' >> '.join(atmospheres)
        )
        layer.deposition_substrate_temperature = add_to_pipe_separated_list(
            layer.deposition_substrate_temperature, ' >> '.join(temperatures)
        )
        layer.deposition_solvents = add_to_pipe_separated_list(
            layer.deposition_solvents, ' >> '.join(solvents)
        )
        layer.deposition_reaction_solutions_compounds = add_to_pipe_separated_list(
            layer.deposition_reaction_solutions_compounds, ' >> '.join(solutes)
        )
        layer.deposition_reaction_solutions_concentrations = add_to_pipe_separated_list(
            layer.deposition_reaction_solutions_concentrations,
            ' >> '.join(solute_concentrations),
        )
        layer.deposition_reaction_solutions_temperature = add_to_pipe_separated_list(
            layer.deposition_reaction_solutions_temperature,
            ' >> '.join(solution_temperatures),
        )
        layer.deposition_thermal_annealing_temperature = add_to_pipe_separated_list(
            layer.deposition_thermal_annealing_temperature,
            ' >> '.join(annealing_temperatures),
        )
        layer.deposition_thermal_annealing_time = add_to_pipe_separated_list(
            layer.deposition_thermal_annealing_time, ' >> '.join(annealing_durations)
        )
        layer.deposition_thermal_annealing_atmosphere = add_to_pipe_separated_list(
            layer.deposition_thermal_annealing_atmosphere,
            ' >> '.join(annealing_atmospheres),
        )
        layer.deposition_reaction_solutions_volumes = add_to_pipe_separated_list(
            layer.deposition_reaction_solutions_volumes, ' >> '.join(volumes)
        )
    elif isinstance(layer, PerovskiteDeposition):
        layer.synthesis_atmosphere = ' >> '.join(atmospheres)
        layer.substrate_temperature = ' >> '.join(temperatures)
        layer.reaction_solutions_compounds = ' >> '.join(solutes)
        layer.reaction_solutions_concentrations = ' >> '.join(solute_concentrations)
        layer.reaction_solutions_temperature = ' >> '.join(solution_temperatures)
        layer.solvents = ' >> '.join(solvents)
        layer.solvents_mixing_ratios = ' >> '.join(solvent_fractions)
        layer.quenching_induced_crystallisation = quenched
        layer.quenching_media = ' >> '.join(antisolvents)
        layer.reaction_solutions_volumes = ' >> '.join(volumes)
        if thermal_annealing_steps:
            layer.thermal_annealing_temperature = ' >> '.join(annealing_temperatures)
            layer.thermal_annealing_time = ' >> '.join(annealing_durations)
            layer.thermal_annealing_atmosphere = ' >> '.join(annealing_atmospheres)


def llm_to_classic_schema(
    llm_cell: LLMExtractedPerovskiteSolarCell,
    llm_extraction_name: str = 'LLM Extraction',
) -> PerovskiteSolarCell:
    """
    Convert an LLM extracted PerovskiteSolarCell to the classic schema format.
    """
    classic_cell = PerovskiteSolarCell()

    ref = Ref()
    ref.extraction_method = 'LLM'
    ref.name_of_person_entering_the_data = llm_extraction_name
    ref.DOI_number = llm_cell.DOI_number
    # Assumes first author is lead author
    if llm_cell.publication_authors:
        ref.lead_author = llm_cell.publication_authors[0]
    ref.publication_date = llm_cell.publication_date
    ref.journal = llm_cell.journal
    ref.free_text_comment = f"""
    Publication title: {llm_cell.publication_title},
    Additional notes: {llm_cell.additional_notes},
    Additional notes from reviewer: {llm_cell.reviewer_additional_notes}
    """

    cell = Cell()
    cell.architecture = llm_cell.device_architecture
    cell.area_total = llm_cell.active_area
    # cell.stack_sequence = ' | '.join(llm_cell.layer_order.split(','))
    cell.stack_sequence = ' | '.join(
        'Perovskite' if layer.functionality == 'Absorber' else layer.name
        for layer in llm_cell.layers
    )

    jv = JV()
    jv.default_PCE = llm_cell.pce
    jv.default_Jsc = llm_cell.jsc
    jv.default_Voc = llm_cell.voc
    ff = llm_cell.ff
    if ff is not None and ff > 1:
        ff /= 100  # Convert percentage to fraction if needed
    jv.default_FF = ff
    # Use number of devices if reported
    if llm_cell.number_devices:
        jv.average_over_n_number_of_cells = llm_cell.number_devices
    # If it's only reported that it is averaged we write 2 as per original instructions
    elif llm_cell.averaged_quantities:
        jv.average_over_n_number_of_cells = 2

    encapsulation = Encapsulation()
    encapsulation.Encapsulation = llm_cell.encapsulated

    perovskite = Perovskite()
    llm_composition = PerovskiteComposition()
    if llm_cell.perovskite_composition:
        llm_composition = llm_cell.perovskite_composition
    perovskite.composition_long_form = llm_composition.long_form
    perovskite.composition_short_form = llm_composition.short_form
    a_ions: list[PerovskiteIonComponent] = sorted(
        llm_composition.ions_a_site, key=lambda ion: ion.abbreviation
    )
    b_ions: list[PerovskiteIonComponent] = sorted(
        llm_composition.ions_b_site, key=lambda ion: ion.abbreviation
    )
    x_ions: list[PerovskiteIonComponent] = sorted(
        llm_composition.ions_x_site, key=lambda ion: ion.abbreviation
    )
    perovskite.composition_a_ions = '; '.join(
        ion.abbreviation if ion.abbreviation is not None else 'Unknown'
        for ion in a_ions
    )
    perovskite.composition_b_ions = '; '.join(
        ion.abbreviation if ion.abbreviation is not None else 'Unknown'
        for ion in b_ions
    )
    perovskite.composition_c_ions = '; '.join(
        ion.abbreviation if ion.abbreviation is not None else 'Unknown'
        for ion in x_ions
    )
    if a_ions:
        perovskite.composition_a_ions_coefficients = '; '.join(
            ion.coefficient if ion.coefficient is not None else 'Unknown'
            for ion in a_ions
        )
    if b_ions:
        perovskite.composition_b_ions_coefficients = '; '.join(
            ion.coefficient if ion.coefficient is not None else 'Unknown'
            for ion in b_ions
        )
    if x_ions:
        perovskite.composition_c_ions_coefficients = '; '.join(
            ion.coefficient if ion.coefficient is not None else 'Unknown'
            for ion in x_ions
        )
    perovskite.band_gap = llm_composition.band_gap
    # Still needs to be read:
    # llm_composition.impurities
    # llm_composition.additives
    # llm_composition.formula
    # llm_composition.sample_type
    perovskite.dimension_list_of_layers = llm_composition.dimensionality
    match llm_composition.dimensionality:
        case '0D':
            perovskite.dimension_0D = True
        case '1D':
            pass
        case '2D':
            perovskite.dimension_2D = True
        case '2D/3D':
            perovskite.dimension_2D3D_mixture = True
        case '3D':
            perovskite.dimension_3D = True
        case 'Other':
            pass
        case _:
            pass

    llm_light_source = LightSource()
    if llm_cell.light_source:
        llm_light_source = llm_cell.light_source
    jv.light_spectra = llm_light_source.type
    jv.light_intensity = llm_light_source.light_intensity
    jv.light_source_type = llm_light_source.lamp
    # Still needs to be read:
    # llm_light_source.description

    stability = OriginalStability()
    llm_stability = Stability()
    if llm_cell.stability:
        llm_stability = llm_cell.stability
    stability.light_spectra = llm_stability.type
    stability.light_intensity = llm_stability.light_intensity
    stability.light_spectra = llm_stability.lamp
    stability.time_total_exposure = llm_stability.time
    stability.relative_humidity_average_value = llm_stability.humidity
    stability.temperature_range = llm_stability.temperature
    stability.PCE_T80 = llm_stability.PCE_T80
    stability.PCE_initial_value = llm_stability.PCE_at_start
    stability.PCE_after_1000_h = llm_stability.PCE_after_1000_hours
    stability.PCE_end_of_experiment = llm_stability.PCE_at_end
    stability.potential_bias_range = llm_stability.potential_bias
    # Still needs to be read:
    # llm_stability.description

    etl = ETL()
    htl = HTL()
    backcontact = Backcontact()
    substrate = Substrate()
    add = Add()
    perovskite_deposition = PerovskiteDeposition()
    llm_layer: Layer
    for llm_layer in llm_cell.layers:
        # Still needs to be read:
        # llm_cell.layers[:].additional_treatment
        # llm_cell.layers[:].deposition[:].step_name
        # llm_cell.layers[:].deposition[:].additional_parameters
        match llm_layer.functionality:
            case 'Absorber':
                set_layer_properties(perovskite, llm_layer)
                set_layer_properties(perovskite_deposition, llm_layer)
            case 'Electron-transport':
                set_layer_properties(etl, llm_layer)
            case 'Hole-transport':
                set_layer_properties(htl, llm_layer)
            case 'Contact':
                set_layer_properties(backcontact, llm_layer)
            case 'Substrate':
                set_layer_properties(substrate, llm_layer)
            case _:
                pass

    classic_cell.ref = ref
    classic_cell.cell = cell
    classic_cell.jv = jv
    classic_cell.encapsulation = encapsulation
    classic_cell.perovskite = perovskite
    classic_cell.perovskite_deposition = perovskite_deposition
    classic_cell.stability = stability
    classic_cell.etl = etl
    classic_cell.htl = htl
    classic_cell.backcontact = backcontact
    classic_cell.substrate = substrate
    classic_cell.add = add
    return classic_cell


m_package.__init_metainfo__()
