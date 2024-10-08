from nomad.datamodel.data import ArchiveSection, EntryData
from nomad.metainfo import Quantity, SubSection
from nomad.metainfo.data_type import Enum

# Processing and deposition methods

class Storage(ArchiveSection):
    atmosphere = Quantity()
    humidity_relative = Quantity()
    time_until_next_step = Quantity()

class ThermalAnnealing(ArchiveSection):
    temperature = Quantity()
    time = Quantity()
    atmosphere = Quantity()

class ReactionComponent(ArchiveSection):
    compound = Quantity()
    supplier = Quantity()
    purity = Quantity()
    concentration = Quantity()
    volume = Quantity()
    age = Quantity()
    temperature = Quantity()

class ReactionSolution(ArchiveSection):
    components = SubSection(ReactionComponent, repeating=True)
    temperature = Quantity()

class Deposition(ArchiveSection):
    procedure = Quantity()
    aggregation_state_of_reactants = Quantity()
    synthesis_atmosphere = Quantity()
    synthesis_atmosphere_pressure_total = Quantity()
    synthesis_atmosphere_pressure_partial = Quantity()
    synthesis_atmosphere_relative_humidity = Quantity()
    substrate_temperature = Quantity()
    max_temperature = Quantity()
    solvents = Quantity()
    solvents_mixing_ratios = Quantity()
    solvents_supplier = Quantity()
    solvents_purity = Quantity()

    thermal_annealing = SubSection(ThermalAnnealing)
    reaction_solution = SubSection(ReactionSolution)



# Materials and their properties

class Layer(ArchiveSection):
    thickness = Quantity()
    functionality = Quantity()
    surface_roughness = Quantity()

    storage = SubSection(Storage)
    deposition = SubSection(Deposition)

class NonAbsorbingLayer(Layer):
    pass

class PhotoAbsorber(Layer):
    bandgap = Quantity()
    bandgap_graded = Quantity()
    bandgap_estimation_basis = Quantity()
    PL_max = Quantity()


    

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