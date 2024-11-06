from typing import (
    TYPE_CHECKING,
)

from nomad.datamodel.data import ArchiveSection
from nomad.datamodel.metainfo.basesections import PublicationReference
from nomad.datamodel.metainfo.eln import ELNAnnotation
from nomad.metainfo import JSON, Quantity, Section, SubSection
from nomad.metainfo.metainfo import MEnum

if TYPE_CHECKING:
    pass

from nomad.datamodel.data import Schema
from nomad.metainfo import SchemaPackage

m_package = SchemaPackage()


class Ion(ArchiveSection):
    m_def = Section(label='Ion')

    abbreviation = Quantity(
        type=str,
        description="The abbreviation used for the ion when writing the perovskite composition",
        a_eln=ELNAnnotation(label='Abbreviation', component='StringEditQuantity')
    )

    coefficient = Quantity(
        type=str,
        description="The stoichiometric coefficient of the ion",
        a_eln=ELNAnnotation(label='Coefficient', component='StringEditQuantity')
    )

class PerovskiteComposition(ArchiveSection):
    m_def = Section(label='Perovskite Composition')

    formula = Quantity(
        type=str,
        description="The perovskite composition according to IUPAC recommendations",
        a_eln=ELNAnnotation(label='Formula', component='StringEditQuantity')
    )

    dimensionality = Quantity(
        type=MEnum(['0D', '1D', '2D', '3D', '2D/3D']),
        description="Dimensionality of the perovskite structure",
        a_eln=ELNAnnotation(label='Dimensionality', component='EnumEditQuantity')
    )

    a_ions = SubSection(
        section_def=Ion,
        repeats=True,
        a_eln=ELNAnnotation(label='A-site Ions')
    )

    b_ions = SubSection(
        section_def=Ion,
        repeats=True,
        a_eln=ELNAnnotation(label='B-site Ions')
    )

    x_ions = SubSection(
        section_def=Ion,
        repeats=True,
        a_eln=ELNAnnotation(label='X-site Ions')
    )

# LightSource class
class LightSource(ArchiveSection):
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


class Solute(ArchiveSection):
    m_def = Section(label='Solute')

    name = Quantity(
        type=str,
        description='Name of the solute',
        a_eln=ELNAnnotation(label='Name', component='StringEditQuantity')
    )

    concentration = Quantity(
        type=float,
        description='Concentration value',
        a_eln=ELNAnnotation(label='Concentration', component='NumberEditQuantity')
    )

    concentration_unit = Quantity(
        type=MEnum(['mol/L', 'mmol/L', 'g/L', 'mg/L', 'wt%', 'vol%', 'M']),
        description='Unit of concentration',
        a_eln=ELNAnnotation(label='Concentration Unit', component='EnumEditQuantity')
    )

class GasQuenching(ArchiveSection):
    m_def = Section(label='Gas Quenching')

    gas_name = Quantity(
        type=str,
        description='Name of the gas used',
        a_eln=ELNAnnotation(label='Gas Name', component='StringEditQuantity')
    )

    time = Quantity(
        type=float,
        unit='s',
        description='Duration of gas quenching',
        a_eln=ELNAnnotation(label='Time', component='NumberEditQuantity')
    )

# Stability class
class Stability(ArchiveSection):
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
        description='Relative humidity during stability test',
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
        description='Time after which the cell performance has degraded by 20%',
        a_eln=ELNAnnotation(
            label='PCE T80', defaultDisplayUnit='hour', component='NumberEditQuantity'
        ),
    )

    PCE_at_start = Quantity(
        type=float,
        description='PCE at the start of the experiment',
        a_eln=ELNAnnotation(label='PCE at Start', component='NumberEditQuantity'),
    )

    PCE_after_1000_hours = Quantity(
        type=float,
        description='PCE after 1000 hours',
        a_eln=ELNAnnotation(
            label='PCE after 1000 Hours', component='NumberEditQuantity'
        ),
    )

    PCE_at_end = Quantity(
        type=float,
        description='PCE at the end of the experiment',
        a_eln=ELNAnnotation(label='PCE at End', component='NumberEditQuantity'),
    )


# ProcessingAtmosphere class
class ProcessingAtmosphere(ArchiveSection):
    m_def = Section(label='Processing Atmosphere')

    type = Quantity(
        type=str,
        description='Type of atmosphere',
        a_eln=ELNAnnotation(label='Atmosphere Type', component='StringEditQuantity'),
    )

    pressure = Quantity(
        type=float,
        unit='mbar',
        description='Pressure during processing',
        a_eln=ELNAnnotation(
            label='Pressure', defaultDisplayUnit='mbar', component='NumberEditQuantity'
        ),
    )

    relative_humidity = Quantity(
        type=float,
        description='Relative humidity during processing',
        a_eln=ELNAnnotation(
            label='Relative Humidity',
            component='NumberEditQuantity',
            props=dict(minValue=0, maxValue=100),
        ),
    )


# ReactionSolution class
class ReactionSolution(ArchiveSection):
    m_def = Section(label='Reaction Solution')

    solutes = SubSection(
        section_def=Solute,
        repeats=True,
        a_eln=ELNAnnotation(label='Solutes')
    )

    volume = Quantity(
        type=float,
        unit='L',
        description='Volume of the solution',
        a_eln=ELNAnnotation(
            label='Volume',
            defaultDisplayUnit='L',
            component='NumberEditQuantity'
        ),
    )

    temperature = Quantity(
        type=float,
        unit='°C',
        description='Temperature of the solution',
        a_eln=ELNAnnotation(
            label='Temperature',
            defaultDisplayUnit='°C',
            component='NumberEditQuantity'
        ),
    )

    solvent = Quantity(
        type=str,
        description='Solvent used',
        a_eln=ELNAnnotation(label='Solvent', component='StringEditQuantity'),
    )


# ProcessingStep class
class ProcessingStep(ArchiveSection):
    m_def = Section(label='Processing Step')

    step_name = Quantity(
        type=str,
        description='Name of the processing step',
        a_eln=ELNAnnotation(label='Step Name', component='StringEditQuantity'),
    )

    method = Quantity(
        type=str,
        description='Method used in the processing step',
        a_eln=ELNAnnotation(label='Method', component='StringEditQuantity'),
    )

    atmosphere = SubSection(
        section_def=ProcessingAtmosphere,
        a_eln=ELNAnnotation(label='Atmosphere'),
    )

    temperature = Quantity(
        type=float,
        unit='°C',
        description='Temperature during the step',
        a_eln=ELNAnnotation(
            label='Temperature',
            defaultDisplayUnit='°C',
            component='NumberEditQuantity'
        ),
    )

    duration = Quantity(
        type=float,
        unit='s',
        description='Duration of the step',
        a_eln=ELNAnnotation(
            label='Duration',
            defaultDisplayUnit='s',
            component='NumberEditQuantity'
        ),
    )

    gas_quenching = SubSection(
        section_def=GasQuenching,
        a_eln=ELNAnnotation(label='Gas Quenching')
    )

    solution = SubSection(
        section_def=ReactionSolution,
        a_eln=ELNAnnotation(label='Solution')
    )

    additional_parameters = Quantity(
        type=JSON,
        description='Any additional parameters specific to this processing step',
        a_eln=ELNAnnotation(label='Additional Parameters'),
    )

# Deposition class
class Deposition(ArchiveSection):
    steps = SubSection(
        section_def=ProcessingStep,
        repeats=True,
        description='List of processing steps in order of execution. Only report conditions that have been explicitly reported.',
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
class Layer(ArchiveSection):
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
            ]
        ),
        description='Functionality of the layer',
        a_eln=ELNAnnotation(label='Functionality', component='EnumEditQuantity'),
    )

    deposition = SubSection(
        section_def=Deposition, a_eln=ELNAnnotation(label='Deposition')
    )

    additional_treatment = Quantity(
        type=str,
        description='Description of modifications applied to this layer beyond its basic composition',
        a_eln=ELNAnnotation(label='Additional Treatment', component='StringEditQuantity')
    )


# PerovskiteSolarCell class
class LLMExtractedPerovskiteSolarCell(PublicationReference, Schema):
    m_def = Section(label='LLM Extracted Perovskite Solar Cell')

    review_completed = Quantity(
        type=bool,
        description='True if the review of the data is completed',
        default=False,
        a_eln=ELNAnnotation(label='Review Completed', component='BoolEditQuantity'),
    )

    DOI_number = Quantity(
        type=str,
        description='DOI number of the publication',
        a_eln=ELNAnnotation(label='DOI Number', component='URLEditQuantity'),
    )

    cell_stack = Quantity(
        type=str,
        shape=['*'],
        description='The stack sequence of the cell.',
        a_eln=ELNAnnotation(label='Cell Stack', component='StringEditQuantity'),
    )

    perovskite_composition = SubSection(
        section_def=PerovskiteComposition,
        a_eln=ELNAnnotation(label='Perovskite Composition')
    )

    device_architecture = Quantity(
        type=MEnum(['pin', 'nip', 'back-contacted', 'front-contacted']),
        description='Device architecture',
        a_eln=ELNAnnotation(label='Device Architecture', component='EnumEditQuantity'),
    )

    pce = Quantity(
        type=float,
        description='Power Conversion Efficiency (PCE)',
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
        description='Fill Factor (FF)',
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

    bandgap = Quantity(
        type=float,
        unit='eV',
        description='Bandgap of the perovskite material in eV. Include this field only if the bandgap has been directly measured in the experiment.',
        a_eln=ELNAnnotation(
            label='Bandgap',
            component='NumberEditQuantity',
            props=dict(minValue=0.5, maxValue=4.0),
        ),
    )

    encapsulation = Quantity(
        type=str,
        description='Encapsulation method, if any',
        a_eln=ELNAnnotation(label='Encapsulation', component='StringEditQuantity'),
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


m_package.__init_metainfo__()
