from ase.data import chemical_symbols
from nomad.datamodel.data import ArchiveSection, EntryData
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.datamodel.metainfo.basesections import (
    Activity,
    ElementalComposition,
    Process,
)
from nomad.metainfo import Quantity, Section, SubSection
from nomad.metainfo.data_type import Enum
from nomad.metainfo.util import MEnum

# from perovskite_solar_cell_database.schema_sections.ions.ion import Ion
from .ref import Reference

# Chemicals and materials and their treatment


# TODO: Improve this section, check inheritence
class Ion(ArchiveSection):
    """
    A section describing a substance that is an element.
    """

    m_def = Section(label_quantity='element')

    ion_type = Quantity(
        type=str,
        shape=[],
        description='Type of the ion.',
        a_eln=dict(component='StringEditQuantity'),
    )

    element = Quantity(
        type=MEnum(chemical_symbols[1:]),
        description="""
        The symbol of the element, e.g. 'Pb'.
        """,
    )

    coefficient = Quantity(
        type=float,
        shape=[],
        description="""Coefficient for the element.
        - If a coefficient is unknown, leave the field empty.
        - If there are uncertainties in the coefficient, only state the best estimate, e.g. write 0.4 and not 0.3-0.5.
        - If the coefficients are not known precisely, a good guess is worth more than to state that we have absolutely no idea.
        """,
    )


# TODO : Check inheritance > material processing solution or basesections
class Substance(ArchiveSection):
    """
    A section describing a pure substance, i.e. a chemical compound or a material.
    """

    m_def = Section(label_quantity='name')

    name = Quantity(type=str, shape=[], description='The name of the substance.')
    supplier = Quantity(
        type=str, shape=[], description='The supplier of the substance.'
    )
    purity = Quantity(type=str, shape=[], description='The purity of the substance.')
    concentration = Quantity(
        type=str,  # TODO: Resolve this workaround for Parsing
        # type=float,
        shape=[],
        # unit='mg/ml',
        description='The concentration of the substance.',
    )
    volume = Quantity(
        type=float,
        shape=[],
        unit='ml',
        description='The volume of the substance.',
    )
    age = Quantity(
        type=float,
        shape=[],
        unit='minutes',  # days?
        description='The age of the substance.',
    )
    temperature = Quantity(
        type=float,
        shape=[],
        unit='K',
        a_eln=ELNAnnotation(defaultDisplayUnit='celsius'),
        description='The temperature of the substance.',
    )


class ReactionComponent(Substance):
    pass


class SolventAnnealing(ArchiveSection):
    """
    Section for a separate solvent annealing step, i.e. a step where the perovskite has been annealing in an atmosphere with a significant amount of solvents.
    This step should also be included deposition procedure sequence but is also stated separately here to simplify downstream filtering.
    """

    temperature = Quantity(
        type=float,
        shape=[],
        unit='K',
        a_eln=ELNAnnotation(defaultDisplayUnit='celsius'),
        description="""The temperature during the solvent annealing step.
        - The temperature refers to the temperature of the sample
        - If the temperature is not known, state that by ‘nan’""",
        repeating=True,
    )
    duration = Quantity(type=float, shape=[], unit='min')
    atmosphere = Quantity(
        type=str,
        shape=[],
        description='The solvents used in the solvent annealing step.',
        repeating=True,
    )
    point_in_time = Quantity(
        type=Enum(['After', 'Before', 'Under']),
        description="""
        The timing of the solvent annealing with respect to the thermal annealing step under which the perovskite is formed. There are three options.
        - The solvent annealing is conducted before the perovskite is formed.
        - The solvent annealing is conducted under the same annealing step in which the perovskite is formed
        - The solvent annealing is conducted after the perovskite has formed.""",
    )


class Solvent(Substance):
    """
    A section describing a solvent for a wetchemical synthesis process.
    """

    mixing_ratio = Quantity(
        type=float,
        shape=[],
        description='The mixing ratio of the solvent.',
    )

    annealing = SubSection(
        section_def=SolventAnnealing,
        description='Pre-deposition solvent annealing step.',
    )


class QuenchingSolvent(Solvent):
    """
    A section describing a quenching solvent.
    """

    # TODO: Check if this is correct
    additive_name = Quantity(
        type=str,
        shape=[],
        description='The name of the additive.',
    )
    additive_concentration = Quantity(
        type=float,
        shape=[],
        description='The concentration of the additive.',
    )


# Processing and deposition methods


class Storage(ArchiveSection):
    """
    A section describing the storage conditions of a sample before the next Sythesis step.
    """

    atmosphere = Quantity(
        type=Enum(['Air', 'Ambient', 'Ar', 'Dry Air', 'N2', 'Vacuum']),
        shape=[],
        description='The atmosphere in which the sample is stored.',
    )
    humidity_relative = Quantity(
        type=float,
        shape=[],
        unit='dimensionless',
        description='The relative humidity in the storage atmosphere.',
    )
    time_until_next_step = Quantity(
        type=float,
        shape=[],
        unit='hours',
        description='The time between the perovskite stack is finalised and the next layer is deposited.',
    )


class SynthesisStep(Activity, ArchiveSection):
    """
    A section describing a general synthesis step.
    More specific synthesis steps are inherited from this class.
    """

    # General
    procedure = Quantity(
        type=str,
        shape=[],
        default='Unknown',
        description='Name of the the synthesis step',
    )

    # TODO: make Enum?
    aggregation_state_of_reactants = Quantity(
        type=Enum(['Solid', 'Liquid', 'Gas', 'Unknown']),
        shape=[],
        default='Unknown',
        description="""The physical state of the reactants.
        - The three basic categories are Solid/Liquid/Gas
        - Most cases are clear cut, e.g. spin-coating involves species in solution and evaporation involves species in gas phase. For less clear-cut cases, consider where the reaction really is happening as in:
            - For a spray-coating procedure, it is droplets of liquid that enters the substrate (thus a liquid phase reaction)
            - For sputtering and thermal evaporation, it is species in gas phase that reaches the substrate (thus a gas phase reaction)
        """,
    )

    atmosphere = Quantity(
        type=Enum(['Air', 'Ar', 'Dry air', 'N2', 'O2', 'Vacuum']),
        shape=[],
        description='The atmosphere present during the synthesis step',
    )
    pressure_total = Quantity(
        type=float,
        shape=[],
        unit='mbar',
        description='The total pressure during each synthesis step',
    )
    humidity_relative = Quantity(
        type=float,
        shape=[],
        unit='dimensionless',
        description='The relative humidity in the storage atmosphere.',
    )
    temperature_substrate = Quantity(
        type=float,
        shape=[],
        unit='K',
        a_eln=ELNAnnotation(defaultDisplayUnit='celsius'),
        description='The temperature of the substrate during the synthesis step',
    )
    temperature_maximum = Quantity(
        type=float,
        shape=[],
        unit='K',
        a_eln=ELNAnnotation(defaultDisplayUnit='celsius'),
        description='The maximum temperature reached during the synthesis step',
    )


class Cleaning(Activity, ArchiveSection):
    """
    A section describing a cleaning step. Typically before a subsequent synthesis step.
    """

    # TODO: Make repeatable if possible
    procedure = Quantity(
        type=Enum(
            [
                'Soap',
                'Ultrasonic Bath',
                'Ethanol',
                'Acetone',
                'UV-ozone',
                'Piranha solutionion',
                'Unknown',
            ]
        ),
        description='',
        shape=[],
    )


class ThermalAnnealing(SynthesisStep):
    """
    A section describing a thermal annealing step.
    """

    temperature = Quantity(
        type=float,
        shape=[],
        unit='K',
        a_eln=ELNAnnotation(defaultDisplayUnit='celsius'),
        description='The temperature during the thermal annealing step',
    )
    duration = Quantity(
        type=float,
        shape=[],
        unit='min',
        description='The duration of the thermal annealing step',
    )
    atmosphere = Quantity(
        type=Enum(['Air', 'Ar', 'Dry air', 'N2', 'O2', 'Vacuum']),
        shape=[],
        description='The atmosphere present during the thermal annealing step',
    )


class LiquidSynthesis(SynthesisStep):
    """
    A section describing a wet chemical synthesis step such as spin-coating or dip-coating.
    """

    reactant = SubSection(
        section_def=ReactionComponent,
        description='The reactants used in the synthesis step',
        repeating=True,
    )
    solvent = SubSection(
        section_def=Solvent,
        description='The solvents used in the synthesis step',
        repeating=True,
    )
    quenching_solvent = SubSection(
        section_def=QuenchingSolvent,
        description='The quenching solvent used in the synthesis step',
        repeating=True,
    )


class GasPhaseSynthesis(SynthesisStep):
    """
    A section describing a gas phase synthesis step such as CVD or PVD.
    """

    pressure_partial = Quantity(
        type=float,
        shape=[],
        unit='mbar',
        description='The partial pressure of the gas phase reactants',
    )


class Synthesis(Process, ArchiveSection):
    steps = SubSection(section_def=SynthesisStep, repeating=True)


# Material layers and their properties


class Layer(ArchiveSection):
    name = Quantity(
        type=str,
        shape=[],
        description='The name of the layer',
    )
    # Type
    functionality = Quantity(
        type=Enum(
            [
                'Anti reflective coating',
                'Back contact',
                'Back reflector',
                'Beam splitter',
                'Buffer layer',
                'Down conversion',
                'Encapsulant',
                'ETL',
                'Front contact',
                'HTL',
                'Recombination layer',
                'Self assembled monolayer',
                'Subcell spacer',
                'Substrate',
                'Upconversion',
                'Window layer',
            ]
        ),
        description='The functionality of the layer',
    )

    # Basic properties
    thickness = Quantity(
        type=float,
        shape=[],
        unit='nm',
        description='The thickness of the layer',
    )
    area = Quantity(
        type=float,
        shape=[],
        unit='cm^2',
        description='The area of the layer',
    )
    surface_roughness = Quantity(
        type=float,
        shape=[],
        unit='nm',
        description='The root mean square value of the surface roughness',
    )

    # Origin and manufacturing
    origin = Quantity(
        type=Enum(['Commercial', 'Lab made', 'Unknown']),
        description='Origin of the layer',
    )
    supplier = Quantity(
        type=str,
        shape=[],
        description='The supplier of a commercially purchased layer',
    )
    supplier_brand = Quantity(
        type=str,
        shape=[],
        description='The specific brand name of a commercially purchased layer',
    )
    cleaning = SubSection(section_def=Cleaning, repeating=True)
    synthesis = SubSection(section_def=Synthesis)

    # Storage
    storage = SubSection(section_def=Storage)

    # Misc
    additives = SubSection(section_def=Substance, repeating=True)


class NonAbsorbingLayer(Layer):
    pass


class Substrate(NonAbsorbingLayer):
    pass


class PhotoAbsorber(Layer):
    bandgap = Quantity(
        type=float,
        shape=[],
        unit='eV',
        description='The band gap of the photoabsorber',
    )
    # TODO: See if joining these two fields makes sense
    bandgap_graded = Quantity(
        type=float,
        shape=[],
        unit='eV',
        description='The band gap if it varies as a function of the vertical position in the photoabsorber layer',
        repeating=True,
    )
    bandgap_estimation_basis = Quantity(
        type=Enum(
            [
                'Absorption',
                'Absorption Tauc-plot',
                'Composition',
                'EQE',
                'Literature',
                'UPS',
                'XPS',
                'Unknown',
            ]
        ),
        description="""The method by which the band gap was estimated.
        The band gap can be estimated from absorption data, EQE-data, UPS-data, or it can be estimated based on literature values for the recipe, or it could be inferred from the composition and what we know of similar but not identical compositions.""",
    )
    PL_max = Quantity(
        type=float,
        shape=[],
        unit='nm',
        description='The wavelength of the maximum PL intensity',
    )

    # Misc
    perovskite_inspired = Quantity(
        type=bool,
        default=False,
        description="""TRUE if the photoabsorber is perovskite inspired.
        In the literature we sometimes see cells based on non-perovskite photo absorbers, but which claims to be “perovskite inspired” regardless if the crystal structure has any resemblance to the perovskite ABC3 structure or not.
        This category is for enabling those cells to easily be identified and filtered.""",
    )


class PerovskiteComposition(ArchiveSection):
    # basis = Quantity()  # ???
    ion_a = SubSection(section_def=Ion, repeating=True)
    ion_b = SubSection(section_def=Ion, repeating=True)
    ion_c = SubSection(section_def=Ion, repeating=True)


class PerovskiteLayer(PhotoAbsorber):
    dimension = Quantity(
        type=Enum(
            [
                '0D (Quantum dot)',
                '2D',
                '2D/3D mixture',
                '3D',
                '3D with 2D capping layer',
            ]
        ),
        description="""
            The dimension of the perovskite layer.""",
        shape=[],
    )
    composition = SubSection(section_def=PerovskiteComposition)

    # General properties
    single_crystal = Quantity(
        type=bool,
        shape=[],
        default=False,
        description='TRUE if the perovskite layer is single crystal, FALSE if it is polycrystalline.',
    )
    # stoichiometry = Quantity()
    inorganic = Quantity(
        type=bool,
        shape=[],
        description='TRUE if the perovskite layer is inorganic, FALSE if it is organic.',
    )
    lead_free = Quantity(
        type=bool,
        shape=[],
        description='TRUE if the perovskite layer is lead-free, FALSE if it contains lead.',
    )


class SiliconLayer(PhotoAbsorber):
    cell_type = Quantity(
        type=str,
        shape=[],
        description="""The type of silicon cell.
        Examples: AL-BSF, c-type, HIT, Homojunction, n-type, PERC, PERC n-type c-Si bifacial SC/nFAB, PERL, Single heterojunction""",
    )
    silicon_type = Quantity(
        type=Enum(
            [
                'Amorphous',
                'CZ',
                'Float-zone',
                'Monocrystaline',
                'Polycrystaline',
                'Unknown',
            ]
        ),
        description='The type of silicon used in the layer',
    )
    doping_sequence = Quantity(
        type=Enum(['n-aSi', 'i-aSi', 'n-Si', 'p-aSi', 'n-SI', 'i-Si', 'p-Si']),
        description='The doping sequence of the silicon, starting from the bottom',
        repeating=True,
    )


class ChalcopyriteAlkaliMetalDoping(Ion):
    source = Quantity(
        type=str,
        shape=[],
        description="""The source of the alkali metal doping.
        Example: none, RbF, RbI, Substrate""",
    )


class ChalcopyriteLayer(PhotoAbsorber):
    # TODO: Reevaluate inheritance
    composition = SubSection(
        section_def=Ion,
        description='The composition of the chalcopyrite layer',
        repeating=True,
    )
    alkali_metal_doping = SubSection(
        section_def=ChalcopyriteAlkaliMetalDoping,
        description='The alkali metal doping of the chalcopyrite layer',
        repeating=True,
    )


# Device architecture


class General(EntryData):
    """
    This section stores general configuration information about a tandem solar cell.
    """

    architecture = Quantity(
        type=Enum(['stacked', 'monolithic', 'other']),
        description='The general architecture of the tandem device. For 4-terminal devices and other configurations where there are two independent sub cells simply stacked on top of each other, define this as “stacked”',
        shape=[],
        # a_eln=dict(
        #     component='EnumEditQuantity',
        #     props=dict(suggestions=sorted(['stacked', 'monolithic', 'other'])),
        # ),
    )

    number_of_terminals = Quantity(
        type=int,
        description='The number of terminals in the device. The most common configurations are 2 and 4',
        shape=[],
        # a_eln=dict(component='NumberEditQuantity')
    )

    number_of_junctions = Quantity(
        type=int,
        description='The number of junctions in the device.',
        shape=[],
        # a_eln=dict(component='NumberEditQuantity')
    )

    number_of_cells = Quantity(
        type=int,
        shape=[],
        default=0,
        description='The number of individual solar cells, or pixels, on the substrate on which the reported cell is made',
    )

    photoabsorber = Quantity(
        type=Enum(['Silicon', 'Perovskite', 'CIGS', 'OPV', 'OSC', 'DSSC', 'BHJ']),
        description="""
            List of the photoabsorbers starting from the bottom of the device stack.
                    """,
        shape=['*'],
        # a_eln=dict(component='EnumEditQuantity')
    )

    photoabsorber_bandgaps = Quantity(
        type=float,
        # unit = 'eV', # arrays with units not yet supported
        description="""
            List of the band gap values of the respective photo absorbers.
            - The layers must line up with the previous filed.
            - State band gaps in eV
            - If there are uncertainties, state the best estimate, e.g write 1.5 and not 1.45-1.55
            - Every photo absorber has a band gap. If it is unknown, state this as ‘nan’
        """,
        shape=['*'],
        # a_eln=dict(component='NumberEditQuantity'),
    )

    stack_sequence = Quantity(
        type=str,
        shape=['*'],
        description="""
        The stack sequence describing the cell.
        - If two materials, e.g. A and B, are mixed in one layer, list the materials in alphabetic order and separate them with semicolons, as in (A; B)
        - The perovskite layer is stated as “Perovskite”, regardless of composition, mixtures, dimensionality etc. There are plenty of other fields specifically targeting the perovskite.
        - If a material is doped, or have an additive, state the pure material here and specify the doping in the columns specifically targeting the doping of those layers.
        - There is no sharp well-defined boundary between a when a material is best considered as doped to when it is best considered as a mixture of two materials. When in doubt if your material is doped or a mixture, use the notation that best capture the metaphysical essence of the situation
        - Use common abbreviations when possible but spell it out when there is risk for confusion. For consistency, please pay attention to the abbreviation specified under the headline Abbreviations found tandem instructions v4.0 document.
                    """,
        # a_eln=dict(component='StringEditQuantity'),
    )

    area_measured = Quantity(
        type=float,
        shape=[],
        unit='cm^2',
        description="""The effective area of the cell during IV and stability measurements under illumination. If measured with a mask, this corresponds to the area of the hole in the mask. Otherwise this area is the same as the total cell area.""",
        # a_eln=dict(component='NumberEditQuantity'),
    )

    flexibility = Quantity(
        type=bool,
        shape=[],
        default=False,
        description='TRUE if the device is flexible and bendable, FALSE if it is rigid.',
        # a_eln=dict(component='BoolEditQuantity'),
    )

    semitransparent = Quantity(
        type=bool,
        shape=[],
        default=False,
        description="""
        TRUE if the device is semitransparent which usually is the case when there are no thick completely covering metal electrodes.
        FALSE if it is opaque.""",
        # a_eln=dict(component='BoolEditQuantity'),
    )
