from typing import (
    TYPE_CHECKING,
)

from nomad.datamodel.data import ArchiveSection
from nomad.datamodel.metainfo.basesections import PublicationReference
from nomad.datamodel.metainfo.eln import ELNAnnotation
from nomad.metainfo import JSON, Quantity, Section, SubSection
from nomad.metainfo.metainfo import MEnum

from perovskite_solar_cell_database.composition import PerovskiteCompositionSection

if TYPE_CHECKING:
    pass

from nomad.datamodel.data import Schema
from nomad.metainfo import SchemaPackage

m_package = SchemaPackage()


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
        type=MEnum(['mol/L', 'mmol/L', 'g/L', 'mg/L', 'wt%', 'vol%', 'M', 'Unknown']),
        description='Unit of concentration',
        a_eln=ELNAnnotation(label='Concentration Unit', component='EnumEditQuantity'),
    )


# Stability class
class Stability(SectionRevision):
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
        description='Volume of the solution',
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
        description='This is the method for the processing of steps in the design of the cells. Some examples are: Spin-coating, Drop-infiltration, Co-evaporation, Doctor blading, Spray coating, Slot-die coating, Ultrasonic spray, Dropcasting, Inkjet printing, Electrospraying, Thermal-annealing, Antisolvent-quenching',
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

    additional_parameters = Quantity(
        type=JSON,
        description='Any additional parameters specific to this processing step',
        a_eln=ELNAnnotation(label='Additional Parameters'),
    )


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
        description='Order of the layers in the device stack. Use the layer names as they appear in the "Layers" section, separated by commas. If you want to add a missing layer, please add it first to the Layers section below. Then make sure to add the name of the layer, as you list it below, in this field in the right order. When you hit save on the top right, the correct order will be set on the layers in the Layers section below.',
        a_eln=ELNAnnotation(label='Layer Order', component='StringEditQuantity'),
    )

    # normalizer that reorderes the layers according to the layer_order
    def normalize(self, archive, logger):
        if not self.layer_order:
            return

        layer_dict = {layer.name: layer for layer in self.layers}
        ordered_names = [name.strip() for name in self.layer_order.split(',')]

        if set(ordered_names) != set(layer_dict.keys()):
            logger.warn('The names in layer_order does not match available layers')
            return

        # Reorder in single pass
        self.layers = [layer_dict[name] for name in ordered_names]
        super().normalize(archive, logger)


m_package.__init_metainfo__()
