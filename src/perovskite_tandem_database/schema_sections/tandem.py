from nomad.datamodel.data import ArchiveSection, EntryData
from nomad.datamodel.metainfo.basesections import (
    Activity,
    ElementalComposition,
    Process,
)
from nomad.metainfo import Quantity, SubSection
from nomad.metainfo.data_type import Enum

# Chemicals and materials and their treatment

class SolventAnnealing(ArchiveSection):
    temperature = Quantity()
    duration = Quantity()
    atmosphere = Quantity()
    point_in_time = Quantity()

class ChemicalCompound(ArchiveSection):
    name = Quantity()
    supplier = Quantity()
    purity = Quantity()
    concentration = Quantity()
    volume = Quantity()
    age = Quantity()
    temperature = Quantity()

class ReactionComponent(ChemicalCompound):
    pass

class Solvent(ChemicalCompound):
    annealing = SubSection(SolventAnnealing)

class QuenchingSolvent(ChemicalCompound):
    pass



# Processing and deposition methods

class Storage(ArchiveSection):
    atmosphere = Quantity()
    humidity_relative = Quantity()
    time_until_next_step = Quantity()

class SynthesisStep(Activity, ArchiveSection):
    
    # General
    procedure = Quantity()
    aggregation_state_of_reactants = Quantity()


    atmosphere = Quantity()
    pressure_total = Quantity()
    pressure_partial = Quantity()
    relative_humidity = Quantity()
    temperature_substrate = Quantity()
    temperature_maximum = Quantity()
    
class Cleaning(SynthesisStep):
    pass

class ThermalAnnealing(SynthesisStep):
    temperature = Quantity()
    duration = Quantity()
    atmosphere = Quantity()

class WetChemicalSynthesis(SynthesisStep):
    reaction_solution = SubSection(ReactionComponent, repeating=True)
    solvents = SubSection(Solvent, repeating=True)
    quenching_solvent = SubSection(QuenchingSolvent, repeating=True)

class GasPhaseSynthesis(SynthesisStep):
    pass

class Synthesis(Process, ArchiveSection):
    steps = SubSection(SynthesisStep, repeating=True)

# Material layers and their properties

class Layer(ArchiveSection):

    # Type
    functionality = Quantity()

    # Basic properties
    thickness = Quantity()
    area = Quantity()
    surface_roughness = Quantity()

    # Origin and manufacturing
    origin = Quantity()
    supplier = Quantity()
    supplier_brand = Quantity()
    synthesis = SubSection(Synthesis)

    # Storage
    storage = SubSection(Storage)
  

class NonAbsorbingLayer(Layer):
    additivies = Quantity(
        section_def=ElementalComposition,
    )

class PhotoAbsorber(Layer):
    bandgap = Quantity()
    bandgap_graded = Quantity()
    bandgap_estimation_basis = Quantity()
    PL_max = Quantity()

class PerovskiteLayer(PhotoAbsorber):
    pass

class SiliconLayer(PhotoAbsorber):
    pass

class ChalcopyriteLayer(PhotoAbsorber):
    pass

# Device architecture

class Tandem(EntryData):
    """
    This section stores general configuration information about a tandem solar cell.
    """

    architecture = Quantity(
        type=str,
        description='The general architecture of the tandem device. For 4-terminal devices and other configurations where there are two independent sub cells simply stacked on top of each other, define this as “stacked”',
        shape=[],
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=sorted(['stacked', 'monolithic', 'other'])
            )
        )
    )

    number_of_terminals = Quantity(
        type=int,
        description='The number of terminals in the device. The most common configurations are 2 and 4',
        shape=[],
        a_eln=dict(component='NumberEditQuantity')
    )

    number_of_junctions = Quantity(
        type=int,
        description='The number of junctions in the device.',
        shape=[],
        a_eln=dict(component='NumberEditQuantity')
    )

    photoabsorber = Quantity(
        type=Enum(['Silicon', 'Perovskite', 'CIGS', 'OPV', 'OSC', 'DSSC', 'BHJ']),
        description='''
            List of the photoabsorbers starting from the bottom of the device stack
            - Start with the bottom one, i.e. the one with the lowest band gap that is closest to the substrate and to the left in the defined device stack
            - Do not care about composition, e.g. write Perovskite or CIGS regardless of the composition of the perovskite and the CIGS. There are several fields that specifically deals with the composition.
        ''',
        shape=['*'],
        a_eln=dict(component='EnumEditQuantity')
    )
    
    photoabsorber_bandgaps = Quantity(
        type= float,
        #unit = 'eV',
        description='''
            List of the band gap values of the respective photo absorbers
            - Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
            - The layers must line up with the previous filed.
            - State band gaps in eV
            - If there are uncertainties, state the best estimate, e.g write 1.5 and not 1.45-1.55
            - Every photo absorber has a band gap. If it is unknown, state this as ‘nan’
        ''',
        shape=['*'],
        a_eln=dict(component='NumberEditQuantity')
    )