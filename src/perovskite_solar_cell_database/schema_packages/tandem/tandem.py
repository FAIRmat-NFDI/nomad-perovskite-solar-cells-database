from ase.data import chemical_symbols
from nomad.datamodel.data import ArchiveSection, EntryData
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.metainfo import Quantity, Section, SubSection
from nomad.metainfo.data_type import Enum
from nomad.metainfo.util import MEnum

from perovskite_solar_cell_database.composition import PerovskiteCompositionSection

# from perovskite_solar_cell_database.schema_sections.ions.ion import Ion
from .reference import Reference

##### Chemicals and materials and their treatment


class Elemental(ArchiveSection):
    """
    A section describing a substance that is an element.
    """

    m_def = Section()#label_quantity='ion_type')

    name = Quantity(
        type=str,
        description='Name of the ion.',
    )

    element = Quantity(
        type=MEnum(chemical_symbols[1:]),
        description="""
        The symbol of the element, e.g. 'Pb'.
        """,
    )

    coefficient = Quantity(
        type=float,
        description="""Coefficient for the element.
        - If a coefficient is unknown, leave the field empty.
        - If there are uncertainties in the coefficient, only state the best estimate, e.g. write 0.4 and not 0.3-0.5.
        - If the coefficients are not known precisely, a good guess is worth more than to state that we have absolutely no idea.
        """,
    )


class Substance(ArchiveSection):
    """
    A section describing a pure substance, i.e. a chemical compound or a material.
    """

    m_def = Section(label_quantity='name')

    name = Quantity(type=str, description='The name of the substance.')
    supplier = Quantity(type=str, description='The supplier of the substance.')
    purity = Quantity(type=str, shape=[], description='The purity of the substance.')
    molar_concentration = Quantity(
        type=float,
        description='The molarity of the substance.',
        unit='mol/l',
    )
    mass_concentration = Quantity(
        type=float,
        description='The mass concentration of the substance.',
        unit='g/l',
        a_eln=ELNAnnotation(defaultDisplayUnit='mg/ml'),
    )
    mass_fraction = Quantity(
        type=float,
        description='The mass fraction of the substance.',
    )
    volume_fraction = Quantity(
        type=float,
        description='The volume fraction of the substance.',
    )
    volume = Quantity(
        type=float,
        unit='ml',
        a_eln=ELNAnnotation(defaultDisplayUnit='ml'),
        description='The volume of the substance.',
    )
    age = Quantity(
        type=float,
        unit='minute',  # days?
        description='The age of the substance.',
        a_eln=ELNAnnotation(defaultDisplayUnit='minute'),
    )
    temperature = Quantity(
        type=float,
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
        unit='K',
        a_eln=ELNAnnotation(defaultDisplayUnit='celsius'),
        description="""The temperature during the solvent annealing step.
        - The temperature refers to the temperature of the sample
        - If the temperature is not known, state that by ‘nan’""",
        repeats=True,
    )
    duration = Quantity(
        type=float,
        unit='minute',
        a_eln=ELNAnnotation(defaultDisplayUnit='minute'),
    )
    atmosphere = Quantity(
        type=str,
        description='The solvents used in the solvent annealing step.',
        repeats=True,
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

    additives = SubSection(section_def=Substance, repeats=True)


##### Processing and deposition methods

class SynthesisStep(ArchiveSection):
    """
    A section describing a general synthesis step.
    """

    name = Quantity(
        type=str,
        description='The name of the process step.',
    )


class DepositionStep(SynthesisStep):
    """
    A section describing a general deposition step.
    More specific deposition steps are inherited from this class.
    """

    m_def = Section()

    # General
    name = Quantity(
        type=str,
        description='Name of the the synthesis step',
    )

    aggregation_state_of_reactants = Quantity(
        type=Enum(['Solid', 'Liquid', 'Gas', 'Unknown']),
        description="""The physical state of the reactants.
        - The three basic categories are Solid/Liquid/Gas
        - Most cases are clear cut, e.g. spin-coating involves species in solution and evaporation involves species in gas phase. For less clear-cut cases, consider where the reaction really is happening as in:
            - For a spray-coating procedure, it is droplets of liquid that enters the substrate (thus a liquid phase reaction)
            - For sputtering and thermal evaporation, it is species in gas phase that reaches the substrate (thus a gas phase reaction)
        """,
    )

    atmosphere = Quantity(
        type=Enum(['Air', 'Ar', 'Dry air', 'N2', 'O2', 'Vacuum', 'Unknown']),
        default='Unknown',
        description='The atmosphere present during the synthesis step',
    )
    pressure_total = Quantity(
        type=float,
        unit='mbar',
        a_eln=ELNAnnotation(defaultDisplayUnit='mbar'),
        description='The total pressure during each synthesis step',
    )
    humidity_relative = Quantity(
        type=float,
        unit='dimensionless',
        description='The relative humidity in the storage atmosphere.',
    )
    temperature_substrate = Quantity(
        type=float,
        unit='K',
        a_eln=ELNAnnotation(defaultDisplayUnit='celsius'),
        description='The temperature of the substrate during the synthesis step',
    )
    temperature_maximum = Quantity(
        type=float,
        unit='K',
        a_eln=ELNAnnotation(defaultDisplayUnit='celsius'),
        description='The maximum temperature reached during the synthesis step',
    )

    reactants = SubSection(
        section_def=ReactionComponent,
        description='The reactants used in the synthesis step',
        repeats=True,
    )


class LiquidSynthesis(DepositionStep):
    """
    A section describing a wet chemical synthesis step such as spin-coating or dip-coating.
    """

    solvent = SubSection(
        section_def=Solvent,
        description='The solvents used in the synthesis step',
        repeats=True,
    )
    quenching_solvent = SubSection(
        section_def=QuenchingSolvent,
        description='The quenching solvent used in the synthesis step',
        repeats=True,
    )


class GasPhaseSynthesis(DepositionStep):
    """
    A section describing a gas phase synthesis step such as CVD or PVD.
    """

    pressure_partial = Quantity(
        type=float,
        unit='mbar',
        description='The partial pressure of the gas phase reactants',
    )


class Cleaning(SynthesisStep):
    """
    A cleaning procedure as a synthesis step.
    """

    steps = Quantity(
        type=str,
        description='The steps in the cleaning procedure',
        shape=['*'],
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.name = 'Cleaning'


class ThermalAnnealing(SynthesisStep):
    """
    A section describing a thermal annealing step.
    """

    temperature = Quantity(
        type=float,
        unit='K',
        a_eln=ELNAnnotation(defaultDisplayUnit='celsius'),
        description='The temperature during the thermal annealing step',
    )
    duration = Quantity(
        type=float,
        unit='minute',
        a_eln=ELNAnnotation(defaultDisplayUnit='minute'),
        description='The duration of the thermal annealing step',
    )
    atmosphere = Quantity(
        type=Enum(['Air', 'Ar', 'Dry air', 'N2', 'O2', 'Vacuum', 'Unknown']),
        default='Unknown',
        description='The atmosphere present during the synthesis step',
    )
    pressure_total = Quantity(
        type=float,
        unit='mbar',
        a_eln=ELNAnnotation(defaultDisplayUnit='mbar'),
        description='The total pressure during each synthesis step',
    )
    humidity_relative = Quantity(
        type=float,
        unit='dimensionless',
        description='The relative humidity in the storage atmosphere.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.name = 'Thermal Annealing'


class Synthesis(ArchiveSection):
    """ """

    # Origin and manufacturing
    origin = Quantity(
        type=Enum(['Commercial', 'Lab made', 'Unknown']),
        description='Origin of the layer',
    )
    supplier = Quantity(
        type=str,
        description='The supplier of a commercially purchased layer',
    )
    supplier_brand = Quantity(
        type=str,
        description='The specific brand name of a commercially purchased layer',
    )

    steps = SubSection(section_def=SynthesisStep, repeats=True)


class Storage(ArchiveSection):
    """
    A section describing the storage conditions of a sample before the next layer is deposited.
    """

    atmosphere = Quantity(
        type=Enum(['Air', 'Ambient', 'Ar', 'Dry Air', 'N2', 'Vacuum']),
        description='The atmosphere in which the sample is stored.',
    )
    humidity_relative = Quantity(
        type=float,
        unit='dimensionless',
        description='The relative humidity in the storage atmosphere.',
    )
    time_until_next_step = Quantity(
        type=float,
        unit='hour',
        a_eln=ELNAnnotation(defaultDisplayUnit='hour'),
        description='The time between the perovskite stack is finalised and the next layer is deposited.',
    )


##### Material layers and their properties


class LayerProperties(ArchiveSection):
    """
    A section storing general properties of a layer.
    """

    thickness = Quantity(
        type=float,
        unit='nm',
        a_eln=ELNAnnotation(defaultDisplayUnit='nm'),
        description='The thickness of the layer',
    )
    area = Quantity(
        type=float,
        unit='cm^2',
        a_eln=ELNAnnotation(defaultDisplayUnit='cm^2'),
        description='The area of the layer',
    )
    surface_roughness = Quantity(
        type=float,
        unit='nm',
        a_eln=ELNAnnotation(defaultDisplayUnit='nm'),
        description='The root mean square value of the surface roughness',
    )


class Layer(ArchiveSection):
    """
    General layer class for inheriting specific layer types.
    """

    name = Quantity(
        type=str,
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
                'Photoabsorber',
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
    properties = SubSection(section_def=LayerProperties)

    # Synthesis
    synthesis = SubSection(section_def=Synthesis)

    # Storage
    storage = SubSection(section_def=Storage)

    # Misc
    additives = SubSection(section_def=Substance, repeats=True)


class NonAbsorbingLayer(Layer):
    pass


class Substrate(NonAbsorbingLayer):
    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.functionality = 'Substrate'


class PhotoAbsorberProperties(LayerProperties):
    """
    A section storing general properties of a photoabsorber layer.
    """

    bandgap = Quantity(
        type=float,
        unit='eV',
        description='The band gap of the photoabsorber',
    )
    bandgap_graded = Quantity(
        type=bool,
        description='TRUE if the band gap varies as a function of the vertical position in the photoabsorber layer',
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


class PhotoAbsorber(Layer):
    """
    A section describing a photoabsorber layer.
    """

    properties = SubSection(section_def=PhotoAbsorberProperties)

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.functionality = 'Photoabsorber'


class PerovskiteLayerProperties(PhotoAbsorberProperties):
    """
    A section storing general properties of a perovskite layer.
    """

    single_crystal = Quantity(
        type=bool,
        default=False,
        description='TRUE if the perovskite layer is single crystal, FALSE if it is polycrystalline.',
    )
    inorganic = Quantity(
        type=bool,
        description='TRUE if the perovskite layer is inorganic, FALSE if it is organic.',
    )
    lead_free = Quantity(
        type=bool,
        description='TRUE if the perovskite layer is lead-free, FALSE if it contains lead.',
    )
    # non_stoichiometry = Quantity(
    #     type=str,
    #     description='Excess components in the perovskite layer.',
    # )


class PerovskiteLayer(PhotoAbsorber):
    """
    A section describing a perovskite layer.
    """

    composition = SubSection(section_def=PerovskiteCompositionSection)
    properties = SubSection(section_def=PerovskiteLayerProperties)


class SiliconLayerProperties(PhotoAbsorberProperties):
    """
    A section storing general properties of a silicon layer.
    """

    cell_type = Quantity(
        type=str,
        description="""The type of silicon cell.
        Examples: AL-BSF, c-type, HIT, Homojunction, n-type, PERC, PERC n-type c-Si bifacial
        SC/nFAB, PERL, Single heterojunction""",
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
        repeats=True,
    )


class SiliconLayer(PhotoAbsorber):
    """
    A section describing a silicon layer.
    """

    properties = SubSection(section_def=SiliconLayerProperties)

    cell_type = Quantity(
        type=str,
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
        repeats=True,
    )


class ChalcopyriteAlkaliMetalDoping(Elemental):
    source = Quantity(
        type=str,
        description="""The source of the alkali metal doping.
        Example: none, RbF, RbI, Substrate""",
    )


class ChalcopyriteLayer(PhotoAbsorber):
    # TODO: Reevaluate inheritance
    composition = SubSection(
        section_def=Elemental,
        description='The composition of the chalcopyrite layer',
        repeats=True,
    )
    alkali_metal_doping = SubSection(
        section_def=ChalcopyriteAlkaliMetalDoping,
        description='The alkali metal doping of the chalcopyrite layer',
        repeats=True,
    )


# Device architecture


class SubCell(ArchiveSection):
    """
    A section describing a sub cell in a tandem solar cell.
    """

    area = Quantity(
        type=float,
        unit='cm^2',
        a_eln=ELNAnnotation(defaultDisplayUnit='cm^2'),
        description='The area of the sub cell',
    )

    module = Quantity(
        type=bool,
        description="""
        TRUE if a sub cell is in the form of a module, FALSE if it is a single cell
        It is for example possible to have a silicon bottom cell and a perovskite module as a top cell. In that case this would be marked as FALSE | TRUE
        """,
    )

    commercial_unit = Quantity(
        type=bool,
        description='TRUE if the sub cell was bought commercially, FALSE if it is a lab-made unit',
    )

    supplier = Quantity(
        type=str,
        description='Origin of the subcell. This will most often be a company or the lab of a research group',
    )


class General(EntryData):
    """
    This section stores general configuration information about a tandem solar cell.
    """

    architecture = Quantity(
        type=Enum(['Stacked', 'Monolithic', 'Other']),
        default='Other',
        description='The general architecture of the tandem device. For 4-terminal devices and other configurations where there are two independent sub cells simply stacked on top of each other, define this as “stacked”',
    )

    number_of_terminals = Quantity(
        type=int,
        description='The number of terminals in the device. The most common configurations are 2 and 4',
    )

    number_of_junctions = Quantity(
        type=int,
        description='The number of junctions in the device.',
    )

    number_of_cells = Quantity(
        type=int,
        default=0,
        description='The number of individual solar cells, or pixels, on the substrate on which the reported cell is made',
    )

    photoabsorber = Quantity(
        type=Enum(['Silicon', 'Perovskite', 'CIGS', 'OPV', 'OSC', 'DSSC', 'BHJ']),
        description="""
            List of the photoabsorbers starting from the bottom of the device stack.
                    """,
        shape=['*'],
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
    )

    area = Quantity(
        type=float,
        unit='cm^2',
        a_eln=ELNAnnotation(defaultDisplayUnit='cm^2'),
        description='The total area of the device.',
    )

    area_measured = Quantity(
        type=float,
        unit='cm^2',
        a_eln=ELNAnnotation(defaultDisplayUnit='cm^2'),
        description="""The effective area of the cell during IV and stability measurements under illumination. If measured with a mask, this corresponds to the area of the hole in the mask. Otherwise this area is the same as the total cell area.""",
    )

    flexibility = Quantity(
        type=bool,
        default=False,
        description='TRUE if the device is flexible and bendable, FALSE if it is rigid.',
    )

    semitransparent = Quantity(
        type=bool,
        default=False,
        description="""
        TRUE if the device is semitransparent which usually is the case when there are no thick completely covering metal electrodes.
        FALSE if it is opaque.""",
    )

    contains_textured_layers = Quantity(
        type=bool,
        default=False,
        description='TRUE if the device contains textured layers with the purpose of light management.',
    )

    contains_antireflectie_coating = Quantity(
        type=bool,
        default=False,
        description='TRUE if the device contains one or more anti reflective coatings.',
    )

    subcell = SubSection(
        section_def=SubCell,
        description='The sub cells in the device',
        repeats=True,
    )
