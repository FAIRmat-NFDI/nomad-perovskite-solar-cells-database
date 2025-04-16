from ase.data import chemical_symbols
from nomad.datamodel.data import ArchiveSection
from nomad.datamodel.metainfo.annotations import (
    ELNAnnotation,
    Filter,
    SectionProperties,
)
from nomad.datamodel.metainfo.basesections import PubChemPureSubstanceSection
from nomad.metainfo import MEnum, Quantity, Section, SubSection
from nomad.metainfo.metainfo import SchemaPackage

from perovskite_solar_cell_database.composition import PerovskiteCompositionSection

##### Chemicals and materials

m_package = SchemaPackage()


class PureSubstanceComponent(PubChemPureSubstanceSection):
    """
    A section describing a pure substance being a component in a mixture.
    """

    m_def = Section(
        label_quantity='name',
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(
                    exclude=['datetime', 'lab_id', 'description'],
                )
            )
        ),
    )

    supplier = Quantity(
        description='The supplier of the substance.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )
    purity = Quantity(
        description='The purity of the substance.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    molar_concentration = Quantity(
        description='The molarity of the substance.',
        type=float,
        unit='mol/l',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mol/l'),
    )
    mass_concentration = Quantity(
        description='The mass concentration of the substance.',
        type=float,
        unit='g/l',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mg/ml'),
    )
    molar_fraction = Quantity(
        description='The molar fraction of the substance.',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )
    mass_fraction = Quantity(
        description='The mass fraction of the substance.',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )
    volume_fraction = Quantity(
        description='The volume fraction of the substance.',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    def normalize(self, archive, logger):
        # Fix for non-defined molecular_formula in PureSubstance v2.py
        # self.molecular_formula = self.formula
        super().normalize(archive, logger)


class SolutionComponent(PureSubstanceComponent):
    """
    Extension of PureSubstanceComponent being a component in a solution.
    """

    role = Quantity(
        description='The role of this specific material in the solution.',
        type=MEnum(['Solvent', 'Solute', 'Quenching solvent']),
        a_eln=ELNAnnotation(component='EnumEditQuantity'),
    )
    volume = Quantity(
        description='The absolute volume of the substance.',
        type=float,
        unit='ml',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='ml'),
    )
    age = Quantity(
        description='The age of the substance.',
        type=float,
        unit='minute',  # days?
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='minute'
        ),
    )
    temperature = Quantity(
        description='The temperature of the substance.',
        type=float,
        unit='K',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )


class GasPhaseComponent(PureSubstanceComponent):
    """
    Extension of PureSubstanceComponent being a component in a gas phase process such as CVD or PVD.
    """

    role = Quantity(
        description='The role of this specific material in the reaction.',
        type=MEnum(['Reactant', 'Product']),
        a_eln=ELNAnnotation(component='EnumEditQuantity'),
    )
    pressure = Quantity(
        description='The partial pressure of the substance.',
        type=float,
        unit='mbar',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mbar'),
    )
    aggregation_state = Quantity(
        description='The aggregation state of the substance.',
        type=MEnum(['Solid', 'Liquid', 'Gas']),
        a_eln=ELNAnnotation(component='EnumEditQuantity'),
    )


class Solution(ArchiveSection):
    """
    A section describing a solution composed of several components.
    """

    components = SubSection(
        description='The components in the solution',
        section_def=SolutionComponent,
        repeats=True,
    )

    age = Quantity(
        description='The time between preparation nad use of the solution.',
        type=float,
        unit='minute',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='minute'
        ),
    )


##### Material layer properties


class PhysicalProperty(ArchiveSection):
    """
    A section describing a property of a layer.
    """

    name = Quantity(
        description='The name of the property.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    value = Quantity(
        description='The value of the property.',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    determined_by = Quantity(
        description='The measurement or estimation method used to determine the property.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )


class Thickness(PhysicalProperty):
    value = Quantity(
        description='The thickness of the layer',
        type=float,
        unit='nm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='nm'),
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        if not self.name:
            self.name = 'Thickness'


class Area(PhysicalProperty):
    value = Quantity(
        description='The area of the layer',
        type=float,
        unit='cm^2',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='cm^2'),
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        if not self.name:
            self.name = 'Area'


class SurfaceRoughness(PhysicalProperty):
    value = Quantity(
        description='The root mean square value of the surface roughness',
        type=float,
        unit='nm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='nm'),
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        if not self.name:
            self.name = 'Surface Roughness'


class BandGap(PhysicalProperty):
    value = Quantity(
        description='The band gap of the layer',
        type=float,
        unit='eV',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='eV'),
    )
    graded = Quantity(
        description='TRUE if the band gap varies as a function of the vertical position in the photoabsorber layer',
        type=bool,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )
    determined_by = Quantity(
        description="""The method by which the band gap was estimated.
        The band gap can be estimated from absorption data, EQE-data, UPS-data, or it can be estimated based on literature values for the recipe, or it could be inferred from the composition and what we know of similar but not identical compositions.""",
        type=MEnum(
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
        a_eln=ELNAnnotation(component='EnumEditQuantity'),
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        if not self.name:
            self.name = 'Band Gap'


class Conductivity(PhysicalProperty):
    value = Quantity(
        description='The conductivity of the layer',
        type=float,
        unit='S/m',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='S/m'),
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        if not self.name:
            self.name = 'Conductivity'


class Crystallinity(PhysicalProperty):
    value = Quantity(
        description='The crystallinity of the layer',
        type=MEnum(['Amorphous', 'Polycrystalline', 'Single crystal', 'Unknown']),
        a_eln=ELNAnnotation(component='EnumEditQuantity'),
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        if not self.name:
            self.name = 'Crystallinity'


class LayerProperties(ArchiveSection):
    """
    A section storing general properties of a layer.
    """

    thickness = SubSection(
        description='The thickness of the layer',
        section_def=Thickness,
    )

    surface_roughness = SubSection(
        description='The surface roughness of the layer',
        section_def=SurfaceRoughness,
    )

    area = SubSection(
        description='The area of the layer',
        section_def=Area,
    )

    bandgap = SubSection(
        description='The band gap of the layer',
        section_def=BandGap,
    )

    conductivity = SubSection(
        description='The conductivity of the layer',
        section_def=Conductivity,
    )

    crystallinity = SubSection(
        description='The crystallinity of the layer',
        section_def=Crystallinity,
    )


class PhotoAbsorberProperties(LayerProperties):
    """
    A section storing general properties of a photoabsorber layer.
    """

    PL_max = Quantity(
        description='The wavelength of the maximum PL intensity',
        type=float,
        unit='nm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='nm'),
    )

    # Misc
    perovskite_inspired = Quantity(
        description="""TRUE if the photoabsorber is perovskite inspired.
        In the literature we sometimes see cells based on non-perovskite photo absorbers, but which claims to be “perovskite inspired” regardless if the crystal structure has any resemblance to the perovskite ABC3 structure or not.
        This category is for enabling those cells to easily be identified and filtered.""",
        type=bool,
        default=False,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )


class PerovskiteLayerProperties(PhotoAbsorberProperties):
    """
    A section storing general properties of a perovskite layer.
    """

    inorganic = Quantity(
        description='TRUE if the perovskite layer is inorganic, FALSE if it is organic.',
        type=bool,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )
    lead_free = Quantity(
        description='TRUE if the perovskite layer is lead-free, FALSE if it contains lead.',
        type=bool,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )
    # non_stoichiometry = Quantity(
    #     type=str,
    #     description='Excess components in the perovskite layer.',
    # )


class SiliconLayerProperties(PhotoAbsorberProperties):
    """
    A section storing general properties of a silicon layer.
    """

    cell_type = Quantity(
        description="""The type of silicon cell.
        Examples: AL-BSF, c-type, HIT, Homojunction, n-type, PERC, PERC n-type c-Si bifacial
        SC/nFAB, PERL, Single heterojunction""",
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    doping_sequence = Quantity(
        description='The doping sequence of the silicon, starting from the bottom',
        type=str,
        shape=['*'],
        a_eln=ELNAnnotation(
            component='StringEditQuantity',
            suggestions=['n-aSi', 'i-aSi', 'p-aSi', 'n-Si', 'i-Si', 'p-Si'],
        ),
    )


##### Material layer compositions


class LayerComponent(PureSubstanceComponent):
    """
    A section describing a component in a layer.
    """

    m_def = Section(
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(
                    exclude=['datetime', 'lab_id', 'description'],
                )
            )
        )
    )

    role = Quantity(
        description='The role of this specific material in the film.',
        type=MEnum(
            [
                'Majority Phase',
                'Secondary Phase',
                'Additive',
                'Impurity',
                'Dopant',
            ]
        ),
        a_eln=ELNAnnotation(component='EnumEditQuantity'),
    )


class LayerComposition(ArchiveSection):
    """
    A section describing the composition of a layer.
    """

    components = SubSection(
        description='The components in the layer',
        section_def=LayerComponent,
        repeats=True,
    )


class ChalcopyriteLayerComposition(LayerComposition):
    """
    A section describing the composition of a chalcopyrite layer.
    """

    GGI = Quantity(
        description='The ratio of gallium to the sum of gallium and indium in the chalcopyrite layer.',
        type=float,
    )
    CGI = Quantity(
        description='The ratio of copper to the sum of gallium and indium in the chalcopyrite layer.',
        type=float,
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        # TODO: calculate GGI and CGI from the composition
        if self.components:
            Cu, Ga, In = None, None, None
            for component in self.components:
                if component.iupac_name == 'copper':
                    Cu = component.molar_concentration
                elif component.iupac_name == 'gallium':
                    Ga = component.molar_concentration
                elif component.iupac_name == 'indium':
                    In = component.molar_concentration
            if Ga and In:
                self.GGI = Ga / (Ga + In)
            if Cu and Ga and In:
                self.CGI = Cu / (Ga + In)


##### Processing and deposition methods


class SynthesisStep(ArchiveSection):
    """
    A section describing a general synthesis step.
    """

    name = Quantity(
        description='The name of the process step.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )


class DepositionStep(SynthesisStep):
    """
    A section describing a general deposition step.
    More specific deposition steps are inherited from this class.
    """

    # General
    name = Quantity(
        description='Name of the the synthesis step',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    aggregation_state_of_reactants = Quantity(
        description="""The physical state of the reactants.
        - The three basic categories are Solid/Liquid/Gas
        - Most cases are clear cut, e.g. spin-coating involves species in solution and evaporation involves species in gas phase. For less clear-cut cases, consider where the reaction really is happening as in:
            - For a spray-coating procedure, it is droplets of liquid that enters the substrate (thus a liquid phase reaction)
            - For sputtering and thermal evaporation, it is species in gas phase that reaches the substrate (thus a gas phase reaction)
        """,
        type=MEnum(['Solid', 'Liquid', 'Gas', 'Unknown']),
        a_eln=ELNAnnotation(component='EnumEditQuantity'),
    )

    atmosphere = Quantity(
        description='The atmosphere present during the synthesis step',
        type=MEnum(['Air', 'Ar', 'Dry air', 'N2', 'O2', 'Vacuum', 'Unknown']),
        default='Unknown',
        a_eln=ELNAnnotation(component='EnumEditQuantity'),
    )
    pressure_total = Quantity(
        description='The total pressure during each synthesis step',
        type=float,
        unit='mbar',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mbar'),
    )
    humidity_relative = Quantity(
        description='The relative humidity in the storage atmosphere.',
        type=float,
        unit='dimensionless',
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )
    temperature_substrate = Quantity(
        description='The temperature of the substrate during the synthesis step',
        type=float,
        unit='K',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )
    temperature_maximum = Quantity(
        description='The maximum temperature reached during the synthesis step',
        type=float,
        unit='K',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )


class LiquidSynthesis(DepositionStep):
    """
    A section describing a wet chemical synthesis step such as spin-coating or dip-coating.
    """

    solution = SubSection(
        description='The solution used in the synthesis step',
        section_def=Solution,
    )


class GasPhaseSynthesis(DepositionStep):
    """
    A section describing a gas phase synthesis step such as CVD or PVD.
    """

    reactants = SubSection(
        description='The reactants used in the synthesis step',
        section_def=GasPhaseComponent,
        repeats=True,
    )


class Cleaning(SynthesisStep):
    """
    A cleaning procedure as a synthesis step.
    """

    steps = Quantity(
        description='The steps in the cleaning procedure',
        type=str,
        shape=['*'],
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        if not self.name:
            self.name = 'Cleaning'


class ThermalAnnealing(SynthesisStep):
    """
    A section describing a thermal annealing step.
    """

    temperature = Quantity(
        description='The temperature during the thermal annealing step',
        type=float,
        unit='K',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )
    duration = Quantity(
        description='The duration of the thermal annealing step',
        type=float,
        unit='minute',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='minute'
        ),
    )
    atmosphere = Quantity(
        description='The atmosphere present during the synthesis step',
        type=MEnum(['Air', 'Ar', 'Dry air', 'N2', 'O2', 'Vacuum', 'Unknown']),
        default='Unknown',
        a_eln=ELNAnnotation(component='EnumEditQuantity'),
    )
    pressure_total = Quantity(
        description='The total pressure during each synthesis step',
        type=float,
        unit='mbar',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mbar'),
    )
    humidity_relative = Quantity(
        description='The relative humidity in the storage atmosphere.',
        type=float,
        unit='dimensionless',
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        if not self.name:
            self.name = 'Thermal Annealing'


class SolventAnnealing(ThermalAnnealing):
    """
    A section describing a solvent annealing step.
    """

    atmosphere = Quantity(
        description='The solvent used in this annealing step.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    point_in_time = Quantity(
        description="""
        The timing of the solvent annealing with respect to the thermal annealing step under which the perovskite is formed. There are three options.
        - The solvent annealing is conducted before the perovskite is formed.
        - The solvent annealing is conducted under the same annealing step in which the perovskite is formed
        - The solvent annealing is conducted after the perovskite has formed.""",
        type=MEnum(['After', 'Before', 'Under']),
        a_eln=ELNAnnotation(component='EnumEditQuantity'),
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        if not self.name:
            self.name = 'Solvent Annealing'


class SurfaceTreatment(SynthesisStep):
    """
    A section describing a surface treatment step.
    """

    method = Quantity(
        description='The method used for the surface treatment.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        if not self.name:
            self.name = 'Surface Treatment'


class Storage(ArchiveSection):
    """
    A section describing the storage conditions of a sample,
    e.g. before the next layer is deposited or a measurement is performed.
    """

    atmosphere = Quantity(
        description='The atmosphere in which the sample is stored.',
        type=MEnum(['Air', 'Ambient', 'Ar', 'Dry Air', 'N2', 'Vacuum']),
        a_eln=ELNAnnotation(component='EnumEditQuantity'),
    )
    humidity_relative = Quantity(
        description='The relative humidity in the storage atmosphere.',
        type=float,
        unit='dimensionless',
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )
    time_until_next_step = Quantity(
        description='The time between the perovskite stack is finalised and the next layer is deposited.',
        type=float,
        unit='hour',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='hour'),
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        if not self.name:
            self.name = 'Storage'


class Synthesis(ArchiveSection):
    """
    A section describing the synthesis of a layer.
    """

    # Origin and manufacturing
    origin = Quantity(
        description='Origin of the layer',
        type=MEnum(['Commercial', 'Lab made', 'Unknown']),
        a_eln=ELNAnnotation(component='EnumEditQuantity'),
    )
    supplier = Quantity(
        description='The supplier of a commercially purchased layer',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )
    supplier_brand = Quantity(
        description='The specific brand name of a commercially purchased layer',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    steps = SubSection(section_def=SynthesisStep, repeats=True)


##### Material layers


class Layer(ArchiveSection):
    """
    General layer class for inheriting specific layer types.
    """

    name = Quantity(
        description='The name of the layer',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )
    # Type
    functionality = Quantity(
        description='The functionality of the layer',
        type=MEnum(
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
        a_eln=ELNAnnotation(component='EnumEditQuantity'),
    )

    subcell_association = Quantity(
        description='Indicates the association of the layer with a subcell. A value of 0 signifies that the entire device is monolithic. Any value greater than 0 associates the layer with a specific subcell, numbered sequentially from the bottom.',
        type=int,
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
            minValue=0,
        ),
    )

    # Basic properties
    properties = SubSection(section_def=LayerProperties)

    # Composition
    composition = SubSection(section_def=LayerComposition)

    # Synthesis
    synthesis = SubSection(section_def=Synthesis)


class Substrate(Layer):
    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.functionality = 'Substrate'


class PhotoAbsorberLayer(Layer):
    """
    A section describing a photoabsorber layer.
    """

    properties = SubSection(section_def=PhotoAbsorberProperties)

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        if not self.functionality:
            self.functionality = 'Photoabsorber'


class PerovskiteLayer(PhotoAbsorberLayer):
    """
    A section describing a perovskite layer.
    """

    composition = SubSection(section_def=PerovskiteCompositionSection)
    properties = SubSection(section_def=PerovskiteLayerProperties)


class SiliconLayer(PhotoAbsorberLayer):
    """
    A section describing a silicon layer.
    """

    properties = SubSection(section_def=SiliconLayerProperties)


class ChalcopyriteLayer(PhotoAbsorberLayer):
    """
    A section describing a chalcopyrite layer.
    """

    composition = SubSection(section_def=ChalcopyriteLayerComposition)


m_package.__init_metainfo__()
