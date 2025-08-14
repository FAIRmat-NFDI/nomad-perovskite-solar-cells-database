import re

from ase.data import chemical_symbols
from nomad.datamodel.data import ArchiveSection
from nomad.datamodel.metainfo.annotations import (
    ELNAnnotation,
    Filter,
    SectionProperties,
)
from nomad.datamodel.metainfo.basesections import PubChemPureSubstanceSection
from nomad.metainfo import Datetime, MEnum, Quantity, Section, SubSection
from nomad.metainfo.metainfo import SchemaPackage

from perovskite_solar_cell_database.composition import PerovskiteCompositionSection

m_package = SchemaPackage()


### Chemicals and materials
class EnvironmentalConditionsDeposition(ArchiveSection):
    """
    Environmental conditions during the activity.
    """

    ambient_conditions = Quantity(
        description='TRUE if the activity is occurring in in uncontrolled ambient conditions. FALSE otherwise',
        type=bool,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    in_glove_box = Quantity(
        type=bool,
        shape=[],
        description="""True if the the activity was performed in a glove box, False otherwise.
            """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    atmosphere = Quantity(
        description='Atmosphere during the activity.',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'air',
                    'dry air',
                    'N2',
                    'Ar',
                    'He',
                    'O2',
                    'H2',
                    'vacuum',
                    'other',
                ]
            ),
        ),
    )

    relative_humidity = Quantity(
        description='Relative humidity during the activity. Given in %. i.e. number between 0 and 100',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    pressure = Quantity(
        description='The atmospheric pressure during the activity.',
        type=float,
        unit='Pa',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='Pa'),
    )

    ambient_temperature = Quantity(
        description='Ambient temperature during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    device_temperature = Quantity(
        description='The temperature of the device during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    oxygen_concentration = Quantity(
        description='The oxygen concentration during the activity. Given in %. i.e. number between 0 and 100',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )


class ChemicalComponentIdentity(PubChemPureSubstanceSection):
    """
    PubChem functionality for pure substances.
    """

    def normalize(self, archive, logger):
        # Fix for non-defined molecular_formula in PureSubstance v2.py
        # self.molecular_formula = self.formula
        super().normalize(archive, logger)


class ChemicalComponentAmount(ArchiveSection):
    """
    This is the section for the amount of a chemical component in a layer.
    """

    mass_fraction = Quantity(
        description='The mass fraction of the substance.',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    molar_fraction = Quantity(
        description='The molar fraction of the substance.',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    volume_fraction = Quantity(
        description='The volume fraction of the substance.',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
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

    mass = Quantity(
        description='The mass of the substance.',
        type=float,
        unit='g',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='g'),
    )

    volume = Quantity(
        description='The volume of the substance.',
        type=float,
        unit='ml',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='ml'),
    )

    amount = Quantity(
        description='The amount of the substance.',
        type=float,
        unit='mol',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mol'),
    )

    partial_pressure = Quantity(
        description='The partial pressure of the compound.',
        type=float,
        unit='Pa',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='Pa'),
    )


class NanostructureInformation(ArchiveSection):
    """
    This is the section for the nanostructure information of a chemical component.
    """

    shape = Quantity(
        description='The nanostructure of the compound',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'nanoparticle',
                    'quantum dot',
                    'nanorod',
                    'disc',
                    'sheet',
                    'other',
                ]
            ),
        ),
    )

    diameter = Quantity(
        description='diameter.',
        type=float,
        unit='nm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='nm'),
    )

    width = Quantity(
        description='width.',
        type=float,
        unit='nm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='nm'),
    )

    length = Quantity(
        description='length.',
        type=float,
        unit='nm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='nm'),
    )


class SupplierInformation(ArchiveSection):
    """
    This is the section for the supplier information of a chemical component.
    """

    supplier = Quantity(
        type=str,
        shape=[],
        description='The name of the supplier.',
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    product_number = Quantity(
        type=str,
        shape=[],
        description="The supplier's product number of the substance.",
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    batch_number = Quantity(
        type=str,
        shape=[],
        description='The suppliers batch number of the substance bought.',
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    purity = Quantity(
        description='The purity of the substance.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    delivery_date = Quantity(
        description='Date of delivery of the substance.',
        type=Datetime,
        a_eln=ELNAnnotation(component='DateTimeEditQuantity'),
    )


class SynthesisInformation(ArchiveSection):
    """
    Synthesis of substances not sourced from commercial suppliers.
    """

    synthesis_method = Quantity(
        type=str,
        shape=[],
        description='The synthesis method used to make the substance.',
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    synthesis_date = Quantity(
        description='Date of synthesis of the substance.',
        type=Datetime,
        a_eln=ELNAnnotation(component='DateTimeEditQuantity'),
    )

    free_text_comment = Quantity(
        type=str,
        shape=[],
        description="""
            Any additional description not captured by any other field.                    
            """,
        a_eln=dict(component='RichTextEditQuantity'),
    )


class Component(ArchiveSection):
    """
    This is the section for a chemical component in a layer.
    """

    ## Top level quantities
    name = Quantity(
        type=str,
        shape=[],
        description="""The common trade name of the material.
        examples: TiO2-mp, PEDOT:PSS, Spiro-MeOTAD, SLG, ITO""",
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    abbreviation = Quantity(
        type=str,
        shape=[],
        description="""Standard arreviation of the compound.""",
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    functionality = Quantity(
        description='The primary functionality of the compound in the layer',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'majority phase',
                    'secondary phase',
                    'additive',
                    'dopant',
                    'impurity',
                    'solvent',
                    'other',
                ]
            ),
        ),
    )

    aggregation_state = Quantity(
        description='The aggregation state of the compound',
        type=MEnum(
            [
                'solid',
                'liquid',
                'gas',
                'solution',
                'suspension',
                'other',
            ]
        ),
        a_eln=ELNAnnotation(component='EnumEditQuantity'),
    )

    origin = Quantity(
        description='The origin of the compound',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'commercial supplier',
                    'made in house',
                    'made by collaborator',
                    'collected in nature',
                    'other',
                ]
            ),
        ),
    )

    nanostructured = Quantity(
        description='TRUE if the compound is nanostructured, e.g. nanoparticles, nanorods etc.',
        type=bool,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    ## Subsections
    # PubChem pure substance section
    identity = SubSection(
        section_def=ChemicalComponentIdentity,
        description='The identity of the compound.',
    )

    # Amount of the compound in the layer
    amount = SubSection(
        section_def=ChemicalComponentAmount,
        description='The amount of the compound in the layer.',
    )

    # Supplier information
    supplier = SubSection(
        section_def=SupplierInformation,
        description='The supplier information of the compound.',
    )

    # Nanostructure information
    nanostructuration = SubSection(
        section_def=NanostructureInformation,
        description='The nanostructure information of the compound.',
    )

    # Synthesis information
    synthesis = SubSection(
        section_def=SynthesisInformation,
        description='Synthesis of substances not sourced from commercial suppliers.',
    )


class SputteringTarget(ArchiveSection):
    """
    Section for a sputtering target.
    """

    ## Top level quantities
    name = Quantity(
        type=str,
        shape=[],
        description="""The common trade name of the material.
        examples: Au, Ag, ITO, NiO""",
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    substrate_distance = Quantity(
        description='The distance between the substrate and the sputtering target.',
        type=float,
        unit='cm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='cm'),
    )

    origin = Quantity(
        description='The origin of the compound',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'commercial supplier',
                    'made in house',
                    'made by collaborator',
                    'other',
                ]
            ),
        ),
    )

    ## Subsections
    # PubChem pure substance section
    identity = SubSection(
        section_def=ChemicalComponentIdentity,
        description='The identity of the compound.',
    )

    # Supplier information
    supplier = SubSection(
        section_def=SupplierInformation,
        description='The supplier information of the compound.',
    )


class EvaporationSource(ArchiveSection):
    """
    This is the section for a evaporation source.
    """

    ## Top level quantities
    name = Quantity(
        type=str,
        shape=[],
        description="""The common trade name of the material.
        examples: Au, Ag, C60, PCBM60, LiF, MoO3""",
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    amount = Quantity(
        description='The amount of the compound in the evaporation source.',
        type=float,
        unit='g',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='g'),
    )

    substrate_distance = Quantity(
        description='The distance between the substrate and the evaporation source.',
        type=float,
        unit='cm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='cm'),
    )

    aggregation_state = Quantity(
        description='The aggregation state of the compound',
        type=MEnum(
            [
                'solid',
                'liquid',
                'other',
            ]
        ),
        a_eln=ELNAnnotation(component='EnumEditQuantity'),
    )

    crucible_material = Quantity(
        description='The material of the evaporation boat/vessel',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    origin = Quantity(
        description='The origin of the compound',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'commercial supplier',
                    'made in house',
                    'made by collaborator',
                    'collected in nature',
                    'other',
                ]
            ),
        ),
    )

    ## Subsections
    # PubChem pure substance section
    identity = SubSection(
        section_def=ChemicalComponentIdentity,
        description='The identity of the compound.',
    )

    # Supplier information
    supplier = SubSection(
        section_def=SupplierInformation,
        description='The supplier information of the compound.',
    )

    # Synthesis information
    synthesis = SubSection(
        section_def=SynthesisInformation,
        description='Synthesis of substances not sourced from commercial suppliers.',
    )


class LigandsAndDyes(ArchiveSection):
    """
    This is the section for a ligands or dyes.
    """

    ## Top level quantities
    name = Quantity(
        type=str,
        shape=[],
        description="""The common trade name of the material.
        examples: TiO2-mp, PEDOT:PSS, Spiro-MeOTAD, SLG, ITO""",
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    abbreviation = Quantity(
        type=str,
        shape=[],
        description="""Standard arreviation of the compound.""",
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    origin = Quantity(
        description='The origin of the compound',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'commercial supplier',
                    'made in house',
                    'made by collaborator',
                    'collected in nature',
                    'other',
                ]
            ),
        ),
    )

    ## Subsections
    # PubChem pure substance section
    identity = SubSection(
        section_def=ChemicalComponentIdentity,
        description='The identity of the compound.',
    )

    # Supplier information
    supplier = SubSection(
        section_def=SupplierInformation,
        description='The supplier information of the compound.',
    )

    # Synthesis information
    synthesis = SubSection(
        section_def=SynthesisInformation,
        description='Synthesis of substances not sourced from commercial suppliers.',
    )


class GasComponent(ArchiveSection):
    """
    Section for a chemical component in gas phase.
    """

    ## Top level quantities
    name = Quantity(
        type=str,
        shape=[],
        description="""The common trade name of the substance.
        examples: methylamine, I2, H2O""",
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    functionality = Quantity(
        description='The role of this specific substance in the gas mixture.',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'reactant',
                    'product',
                    'carrier gas',
                    'none',
                    'other',
                ]
            ),
        ),
    )

    origin = Quantity(
        description='The origin of the substance.',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'reaction product',
                    'commercial supplier',
                    'made in house',
                    'made by collaborator',
                    'collected in nature',
                    'other',
                ]
            ),
        ),
    )

    partial_pressure = Quantity(
        description='The partial pressure of the gas.',
        type=float,
        unit='Pa',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='Pa'),
    )

    ## Subsections
    # PubChem pure substance section
    identity = SubSection(
        section_def=ChemicalComponentIdentity,
        description='The identity of the compound.',
    )

    # Supplier information
    supplier = SubSection(
        section_def=SupplierInformation,
        description='The supplier information of the compound.',
    )

    # Synthesis information
    synthesis = SubSection(
        section_def=SynthesisInformation,
        description='Synthesis of substances not sourced from commercial suppliers.',
    )


class SolutionComponent(ArchiveSection):
    """
    Section for a chemical component in a solution.
    """

    ## Top level quantities
    name = Quantity(
        type=str,
        shape=[],
        description="""The common trade name of the substance.
        examples: DMF, DMSO, TiO2-mp, PEDOT:PSS, Spiro-MeOTAD""",
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    functionality = Quantity(
        description='The role of this specific substance in the solution.',
        type=MEnum(['solvent', 'solute', 'other']),
        a_eln=ELNAnnotation(component='EnumEditQuantity'),
    )

    origin = Quantity(
        description='The origin of the substance.',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'commercial supplier',
                    'made in house',
                    'made by collaborator',
                    'collected in nature',
                    'other',
                ]
            ),
        ),
    )

    nanostructured = Quantity(
        description='TRUE if the compound is nanostructured, e.g. nanoparticles, nanorods etc.',
        type=bool,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    ## Subsections
    # PubChem pure substance section
    identity = SubSection(
        section_def=ChemicalComponentIdentity,
        description='The identity of the compound.',
    )

    # Amount of the compound in the layer
    amount = SubSection(
        section_def=ChemicalComponentAmount,
        description='The amount of the compound in the layer.',
    )

    # Supplier information
    supplier = SubSection(
        section_def=SupplierInformation,
        description='The supplier information of the compound.',
    )

    # Nanostructure information
    nanostructuration = SubSection(
        section_def=NanostructureInformation,
        description='The nanostructure information of the compound.',
    )

    # Synthesis information
    synthesis = SubSection(
        section_def=SynthesisInformation,
        description='Synthesis of substances not sourced from commercial suppliers.',
    )


class Solution(ArchiveSection):
    """
    Description of a solution
    """

    preparation_date = Quantity(
        description='Date of preparation of the solution.',
        type=Datetime,
        a_eln=ELNAnnotation(component='DateTimeEditQuantity'),
    )

    age = Quantity(
        description='The time between preparation and the use of the solution.',
        type=float,
        unit='hr',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='hr'),
    )

    volume = Quantity(
        description='The volume of the solution used.',
        type=float,
        unit='ml',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='ml'),
    )

    density = Quantity(
        description='The density of the solution.',
        type=float,
        unit='g/ml',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='g/ml'),
    )

    viscosity = Quantity(
        description='The viscosity of the solution.',
        type=float,
        unit='Pa*s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='Pa*s'),
    )

    temperature = Quantity(
        description='The temperature of the solution.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    temperature_max = Quantity(
        description='The maximum temperature the solution has experienced.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    colour = Quantity(
        description='The colour of the solution.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    stirred = Quantity(
        description="""True if the solution is stirred before use.""",
        type=bool,
        shape=[],
        a_eln=dict(component='BoolEditQuantity'),
    )

    filtered = Quantity(
        description="""TRUE if the if the solution is filtered before use.""",
        type=bool,
        shape=[],
        a_eln=dict(component='BoolEditQuantity'),
    )

    filter_pour_size = Quantity(
        description="""TRUE if the if the solution is filtered before use.""",
        type=float,
        unit='µm',
        shape=[],
        a_eln=dict(component='NumberEditQuantity', defaultDisplayUnit='µm'),
    )

    # Subsections
    # Compounds in the solution
    components = SubSection(
        section_def=SolutionComponent,
        description='The substances in the solution.',
        repeats=True,
    )

    # Environmental conditions
    environmental_conditions_during_preparation = SubSection(
        section_def=EnvironmentalConditionsDeposition,
        description='Environmental conditions during the activity.',
    )


### Material and layer properties
class Area(ArchiveSection):
    value = Quantity(
        description='The area of the layer',
        type=float,
        unit='cm^2',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='cm^2'),
    )


class BandGap(ArchiveSection):
    value = Quantity(
        description='The band gap of the layer',
        type=float,
        unit='eV',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='eV'),
    )

    graded = Quantity(
        description='TRUE if the band gap varies as a function of the vertical position in the layer',
        type=bool,
        a_eln=ELNAnnotation(component='BoolEditQuantity'),
    )

    determined_by = Quantity(
        description="""The method by which the band gap was estimated.
        The band gap can be estimated from absorption data, 
        EQE-data, UPS-data, or it can be estimated based on literature values 
        for the recipe, or it could be inferred from the composition and what 
        we know of similar but not identical compositions.""",
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'absorption',
                    'absorption Tauc-plot',
                    'composition',
                    'eqe',
                    'literature',
                    'ups',
                    'xps',
                    'other',
                ]
            ),
        ),
    )


class Conductivity(ArchiveSection):
    value = Quantity(
        description='The conductivity of the layer',
        type=float,
        unit='S/m',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='S/m'),
    )

    determined_by = Quantity(
        description='The measurement or estimation method used to determine the property.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )


class Crystallinity(ArchiveSection):
    value = Quantity(
        description='The crystallinity of the layer',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'amorphous',
                    'polycrystalline',
                    'single crystal',
                    'nanoparticles',
                    'nanorods',
                    'quantum dots',
                    'other',
                ]
            ),
        ),
    )

    average_grain_size = Quantity(
        description='The average grain size',
        type=float,
        unit='nm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='nm'),
    )

    determined_by = Quantity(
        description='The measurement or estimation method used to determine the property.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )


class ElectronMobility(ArchiveSection):
    value = Quantity(
        description='The electron mobility of the layer',
        type=float,
        unit='cm**2/(V*s)',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='cm**2/(V*s)'
        ),
    )

    determined_by = Quantity(
        description='The measurement or estimation method used to determine the property.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )


class HoleMobility(ArchiveSection):
    value = Quantity(
        description='The hole mobility of the layer',
        type=float,
        unit='cm**2/(V*s)',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='cm**2/(V*s)'
        ),
    )

    determined_by = Quantity(
        description='The measurement or estimation method used to determine the property.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )


class Photoluminesence(ArchiveSection):
    """
    This is the section for the photoluminesence of a layer.
    """

    pl_max = Quantity(
        description='The wavelength of the maximum PL intensity',
        type=float,
        unit='nm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='nm'),
    )

    determined_by = Quantity(
        description='The measurement or estimation method used to determine the property.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )


class RefractiveIndex(ArchiveSection):
    refractive_index = Quantity(
        description='The real part of the refractive index of the layer',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    extinction_coefficient = Quantity(
        description='The imaginary part of the refractive index of the layer',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    determined_by = Quantity(
        description='The measurement or estimation method used to determine the property.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )


class SheetResistance(ArchiveSection):
    value = Quantity(
        description='The sheet resistance of the layer',
        type=float,
        unit='ohm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='ohm'),
    )

    determined_by = Quantity(
        description='The measurement or estimation method used to determine the property.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )


class SurfaceRoughness(ArchiveSection):
    value = Quantity(
        description='The root mean square value of the surface roughness',
        type=float,
        unit='nm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='nm'),
    )

    determined_by = Quantity(
        description='The measurement or estimation method used to determine the property.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )


class Thickness(ArchiveSection):
    value = Quantity(
        description='The thickness of the layer',
        type=float,
        unit='nm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='nm'),
    )

    determined_by = Quantity(
        description='The measurement or estimation method used to determine the property.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )


class LayerProperties(ArchiveSection):
    """
    A section storing general properties of a layer.
    """

    area = SubSection(
        description='The area of the layer',
        section_def=Area,
    )

    band_gap = SubSection(
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

    electron_mobility = SubSection(
        description='The electron mobility of the layer',
        section_def=ElectronMobility,
    )

    hole_mobility = SubSection(
        description='The hole mobility of the layer',
        section_def=HoleMobility,
    )

    photoluminesence = SubSection(
        description='The photoluminesence of the layer',
        section_def=Photoluminesence,
    )

    refractive_index = SubSection(
        description='The refractive index of the layer',
        section_def=RefractiveIndex,
    )

    surface_roughness = SubSection(
        description='The surface roughness of the layer',
        section_def=SurfaceRoughness,
    )

    sheet_resistance = SubSection(
        description='The sheet resistance of the layer',
        section_def=SheetResistance,
    )

    thickness = SubSection(
        description='The thickness of the layer',
        section_def=Thickness,
    )


### Deposition procedures general sections
class DepositionStep(ArchiveSection):
    """
    This is a collection point for deposition procedures
    """

    duration = Quantity(
        description='The total time of the procedure.',
        type=float,
        unit='s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='s'),
    )

    equipment = Quantity(
        description='Brand name and model of the equipment used for the process.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    method = Quantity(
        type=str,
    )


### Synthetic procedures
class ALDStep(ArchiveSection):
    """
    ALD steps
    """

    time_of_step = Quantity(
        description='The length of the step.',
        type=float,
        unit='s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='s'),
    )

    chamber_pressure = Quantity(
        description='The pressure in the reaction chamber.',
        type=float,
        unit='Pa',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='Pa'),
    )

    gases = SubSection(
        section_def=GasComponent, description='The gases in the mixture', repeats=True
    )


class SpinCoatingSteps(ArchiveSection):
    """
    A spin-coating program can be composed of several different steps.
    This is a repeating section for describing all the spin-coating steps
    """

    duration = Quantity(
        description='The length of the step.',
        type=float,
        unit='s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='s'),
    )

    speed_start = Quantity(
        description='The spin speed of the start of the step.',
        type=float,
        unit='rpm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='rpm'),
    )

    speed_end = Quantity(
        description='The spin speed of the end of the step.',
        type=float,
        unit='rpm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='rpm'),
    )

    acceleration = Quantity(
        description='The acceleration of the rotations.',
        type=float,
        unit='rpm/s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='rpm/s'),
    )


class Dipping(ArchiveSection):
    """
    Details for a dipping treatment.
    """

    time_in_solution = Quantity(
        description='The time of the dipping.',
        type=float,
        unit='s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='s'),
    )

    drying_procedure = Quantity(
        description='The method by which the liquid is removed from the sample after dipping.',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'gas blowing',
                    'self drying',
                    'heating',
                    'tissue paper',
                    'none',
                    'other',
                ]
            ),
        ),
    )

    sample_temperature = Quantity(
        description='The temperature of the sample during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    solution_temperature = Quantity(
        description='The temperature of the solution during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    solution = SubSection(
        section_def=Solution,
        description='Details about the solution.',
    )


class TemperatureStep(ArchiveSection):
    """
    Details for heaating steps
    """

    time_of_step = Quantity(
        description='Time of the step.',
        type=float,
        unit='minute',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='minute'
        ),
    )

    temperature_start = Quantity(
        description='Temperature at the start of the step.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    temperature_end = Quantity(
        description='Temperature at the end of the step.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    temperature_acceleration = Quantity(
        description='Temperature acceleration',
        type=float,
        unit='C/min',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='C/min'),
    )


class SputteringStep(ArchiveSection):
    """
    Details for heaating steps
    """

    time_of_step = Quantity(
        description='Time of the step.',
        type=float,
        unit='minute',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='minute'
        ),
    )

    deposition_rate = Quantity(
        description='The rate of deposition.',
        type=float,
        unit='nm/s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='nm/s'),
    )

    target_power = Quantity(
        description='The power driving the target.',
        type=float,
        unit='J/s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='J/s'),
    )

    chamber_pressure = Quantity(
        description='The pressure in the reaction chamber.',
        type=float,
        unit='Pa',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='Pa'),
    )


class AntiSolventDetails(ArchiveSection):
    """
    Details for an antisolvent treatment.
    """

    volume = Quantity(
        description='The volume of the antisolvent.',
        type=float,
        unit='ml',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='ml'),
    )

    start_time = Quantity(
        description='Time of the start of the dispensing in seconds after the start of the spin-coating program.',
        type=float,
        unit='s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='s'),
    )

    dispense_speed = Quantity(
        description='The dispense speed of the precursor solution.',
        type=float,
        unit='ml/s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='ml/s'),
    )

    distance_between_tip_and_substrate = Quantity(
        description='Distance between the pipet tip and the substrate',
        type=float,
        unit='mm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mm'),
    )

    # Subsections
    solution = SubSection(
        section_def=Solution,
        description='Details about the solution.',
    )


class GasQuenchingDetails(ArchiveSection):
    """
    Details for a gas quenching treatment.
    """

    gas = Quantity(
        description='The gas used for the quenching.',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'air',
                    'dry air',
                    'N2',
                    'Ar',
                    'He',
                    'O2',
                    'H2',
                    'other',
                ]
            ),
        ),
    )

    start_time = Quantity(
        description='Time of the start of the dispensing in seconds after the start of the spin-coating program.',
        type=float,
        unit='s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='s'),
    )

    duration = Quantity(
        description='The length of the qas quenching',
        type=float,
        unit='s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='s'),
    )

    pressure = Quantity(
        description='The pressure of the gas.',
        type=float,
        unit='Pa',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='Pa'),
    )

    temperature = Quantity(
        description='The temperature of the gas.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    distance_between_nozzle_and_substrate = Quantity(
        description='Distance between the nozzle and the substrate',
        type=float,
        unit='mm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mm'),
    )


class PostDepositionProcedure(DepositionStep):
    """
    Post deposition procedure.
    """

    # Top level sections
    time_stamp = Quantity(
        description='Date of the operation',
        type=Datetime,
        a_eln=ELNAnnotation(component='DateTimeEditQuantity'),
    )

    time_from_last_step = Quantity(
        description="""The time from the finalization of the last layer 
        and the start of the deposition of this.""",
        type=float,
        unit='hr',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='hr'),
    )

    # Subsections
    steps = SubSection(
        section_def=DepositionStep,
        description='The steps of the deposition procedure.',
        repeats=True,
    )

    # Environmental conditions
    environmental_conditions = SubSection(
        section_def=EnvironmentalConditionsDeposition,
        description='Environmental conditions during the activity.',
    )

    sample_history = SubSection(
        section_def=EnvironmentalConditionsDeposition,
        description="""A description of the conditions under which the sample have been stored between
        the finalization of the device and the described measurement.""",
    )


class AtomicLayerDeposition(DepositionStep):
    """
    Details for an ALD process.
    """

    # Numerical qunatities

    substrate_temperature = Quantity(
        description='The temperature of the substrate during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    flow_rate = Quantity(
        description='The flow rate.',
        type=float,
        unit='cm^3/minute',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='cm^3/minute'
        ),
    )

    number_of_cycles = Quantity(
        description='The number of deposition cycles.',
        type=int,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    # Categorical qunatities
    carrier_gas = Quantity(
        description='The carrier gas.',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(suggestions=['air', 'dry air', 'N2', 'Ar', 'other']),
        ),
    )

    # Subsections
    steps = SubSection(
        section_def=ALDStep,
        description='Details about the four ALD steps.',
        repeats=True,
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'AtomicLayerDeposition'


class ChemicalBathDeposition(DepositionStep):
    """
    Details for a chemical bath deposition process.
    """

    # Numerical quantities
    time_in_solution = Quantity(
        description='The time of the dipping.',
        type=float,
        unit='s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='s'),
    )

    sample_temperature = Quantity(
        description='The temperature of the sample during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    solution_temperature = Quantity(
        description='The temperature of the solution during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    # Categorical quantities
    drying_procedure = Quantity(
        description='The method by which the liquid is removed from the sample after dipping.',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'gas blowing',
                    'self drying',
                    'heating',
                    'tissue paper',
                    'none',
                    'other',
                ]
            ),
        ),
    )

    # Subsection
    solution = SubSection(
        section_def=Solution,
        description='Details about the solution.',
    )

    environmental_conditions = SubSection(
        section_def=EnvironmentalConditionsDeposition,
        description='Environmental conditions during the activity.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'ChemicalBathDeposition'


class Cleaning(DepositionStep):
    """
    Cleaning procedures
    """

    # Categorical quantities

    free_text_comment = Quantity(
        type=str,
        shape=[],
        description="""
            Any additional description not captured by any other field.                    
            """,
        a_eln=dict(component='RichTextEditQuantity'),
    )

    # Subsections
    solution = SubSection(
        section_def=Solution,
        description='Details about the solution.',
    )

    environmental_conditions = SubSection(
        section_def=EnvironmentalConditionsDeposition,
        description='Environmental conditions during the activity.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'Cleaning'


class DipCoating(DepositionStep):
    """
    Details for a dip coating process.
    """

    # Numerical quantities
    time_in_solution = Quantity(
        description='The time of the dipping.',
        type=float,
        unit='s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='s'),
    )

    sample_temperature = Quantity(
        description='The temperature of the sample during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    solution_temperature = Quantity(
        description='The temperature of the solution during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    number_of_repetitions = Quantity(
        description='The number of repetitions (dippings).',
        type=int,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    time_between_repetitions = Quantity(
        description='The time between the repetitions.',
        type=float,
        unit='minute',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='minute'
        ),
    )

    # Categorical quantities
    drying_procedure = Quantity(
        description='The method by which the liquid is removed from the sample after dipping.',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'gas blowing',
                    'self drying',
                    'heating',
                    'tissue paper',
                    'none',
                    'other',
                ]
            ),
        ),
    )

    # Subsection
    solution = SubSection(
        section_def=Solution,
        description='Details about the solution.',
    )

    environmental_conditions = SubSection(
        section_def=EnvironmentalConditionsDeposition,
        description='Environmental conditions during the activity.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'DipCoating'


class DoctorBlading(DepositionStep):
    """
    Details for a doctor blading process.
    """

    # Numerical quantities

    blade_speed = Quantity(
        description='The speed of the blade.',
        type=float,
        unit='mm/s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mm/s'),
    )

    blade_angle = Quantity(
        description='The angle of the blade.',
        type=float,
        unit='degree',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='degree'
        ),
    )

    blade_height = Quantity(
        description='The height of the blade.',
        type=float,
        unit='mm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mm'),
    )

    ink_volume = Quantity(
        description='The volume of the ink used.',
        type=float,
        unit='ml',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='ml'),
    )

    sample_temperature = Quantity(
        description='The temperature of the sample during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    solution_temperature = Quantity(
        description='The temperature of the solution during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    # Subsections
    ink = SubSection(
        section_def=Solution,
        description='Details about the solution.',
    )

    environmental_conditions = SubSection(
        section_def=EnvironmentalConditionsDeposition,
        description='Environmental conditions during the activity.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'DoctorBlading'


class Evaporation(DepositionStep):
    """
    Details for a evaporation process.
    """

    # Numerical quantities
    number_of_sources = Quantity(
        description='The number of sources used for the evaporation.',
        type=int,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    substrate_temperature = Quantity(
        description='The temperature of the substrate during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    substrate_rotation_speed = Quantity(
        description='The rotation speed of the substrate during the activity.',
        type=float,
        unit='rpm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='rpm'),
    )

    deposition_rate = Quantity(
        description='The rate of deposition.',
        type=float,
        unit='nm/s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='nm/s'),
    )

    chamber_pressure = Quantity(
        description='The pressure in the reaction chamber.',
        type=float,
        unit='Pa',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='Pa'),
    )

    # Subsections
    sources = SubSection(
        section_def=EvaporationSource,
        description='Details about the evaporation sources.',
        repeats=True,
    )

    environmental_conditions = SubSection(
        section_def=EnvironmentalConditionsDeposition,
        description="""Environmental conditions during the activity. 
        Mostly relevant if the evaporation not is done in a vaccuum chamber""",
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'Evaporation'


class GeneralDepositionProcedure(DepositionStep):
    """
    A general deposition procedure.
    """

    # Numerical quantities

    sample_temperature = Quantity(
        description='The temperature of the sample during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    solution_temperature = Quantity(
        description='The temperature of the solution during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    # Subsections
    solution = SubSection(
        section_def=Solution,
        description='Details about the solution.',
    )

    gases = SubSection(
        section_def=GasComponent, description='The gases in the mixture', repeats=True
    )

    environmental_conditions = SubSection(
        section_def=EnvironmentalConditionsDeposition,
        description='Environmental conditions during the activity.',
    )


class Heating(DepositionStep):
    """
    Details for a heating process.
    """

    # categorical quantities
    heating_medium = Quantity(
        description='The way by which the temperature is controlled',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'hotplate',
                    'furnace',
                    'liquid bath',
                    'gas',
                    'other',
                ]
            ),
        ),
    )

    # Subsections
    temperature_steps = SubSection(
        section_def=TemperatureStep,
        description='Details about the temperature steps.',
        repeats=True,
    )

    environmental_conditions = SubSection(
        section_def=EnvironmentalConditionsDeposition,
        description='Environmental conditions during the activity.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'Heating'


class InkjetPrinting(DepositionStep):
    """
    Details for a inkjet printing process.
    """

    # Numerical qunatities
    drop_volume = Quantity(
        description='Drop volume.',
        type=float,
        unit='µl',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='µl'),
    )

    print_resolution = Quantity(
        description='The print resolution in dpi.',
        type=float,
        # unit='dpi',
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    print_speed = Quantity(
        description='The speed of the printer head.',
        type=float,
        unit='mm/s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mm/s'),
    )

    print_heigth = Quantity(
        description='The distance from the nozzle and the substrate.',
        type=float,
        unit='mm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mm'),
    )

    substrate_temperature = Quantity(
        description='The temperature of the substrate during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    ink_temperature = Quantity(
        description='The temperature of the solution during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    # Subsections
    ink = SubSection(
        section_def=Solution,
        description='Details about the solution.',
    )

    environmental_conditions = SubSection(
        section_def=EnvironmentalConditionsDeposition,
        description='Environmental conditions during the activity.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'InkjetPrinting'


class IonExchangeByDipping(DipCoating):
    """
    Details for a process where ions in a perovksite is exchanged by
    dipping it in a solution
    """

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'IonExchangeByDipping'


class IonExchangeByGasDiffusion(DepositionStep):
    """
    Details for a process where ions in a perovksite is exchanged by
    a gas diffusion process

    """

    # Numerical quantities

    substrate_temperature = Quantity(
        description='The temperature of the substrate during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    gas_temperature = Quantity(
        description='The temperature of the reaction gas during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    # Subsections
    gases = SubSection(
        section_def=GasComponent, description='The gases in the mixture', repeats=True
    )

    environmental_conditions = SubSection(
        section_def=EnvironmentalConditionsDeposition,
        description='Environmental conditions during the activity.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'IonExchangeByGasDiffusion'


class SlotDieCoating(DepositionStep):
    """
    Details for a slot dye coatig process
    """

    # Numerical qunatities

    blade_speed = Quantity(
        description='The speed of the blade.',
        type=float,
        unit='mm/s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mm/s'),
    )

    blade_angle = Quantity(
        description='The angle of the blade.',
        type=float,
        unit='degree',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='degree'
        ),
    )

    blade_height = Quantity(
        description='The height of the blade.',
        type=float,
        unit='mm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mm'),
    )

    ink_volume = Quantity(
        description='The volume of the ink used.',
        type=float,
        unit='ml',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='ml'),
    )

    sample_temperature = Quantity(
        description='The temperature of the sample during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    solution_temperature = Quantity(
        description='The temperature of the solution during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    # Subsectinos
    ink = SubSection(
        section_def=Solution,
        description='Details about the solution.',
    )

    environmental_conditions = SubSection(
        section_def=EnvironmentalConditionsDeposition,
        description='Environmental conditions during the activity.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'SlotDieCoating'


class SpinCoating(DepositionStep):
    """
    This is the section for a spin coating step of a layer.
    """

    # Boolean quantities
    dynamic_spin_coating = Quantity(
        description="""
            TRUE if the if the liquid is added on a spinning substrate. FALSE if the liquid is applied before the substrate starts spinning.',
            """,
        type=bool,
        shape=[],
        a_eln=dict(component='BoolEditQuantity'),
    )

    antisolvent = Quantity(
        description="""
            True if an antisolvent is used during spin-coating.',
            """,
        type=bool,
        shape=[],
        a_eln=dict(component='BoolEditQuantity'),
    )

    gas_quenching = Quantity(
        description="""
            True if an gas quenching is used during spin-coating.',
            """,
        type=bool,
        shape=[],
        a_eln=dict(component='BoolEditQuantity'),
    )

    # Numeric quantities
    substrate_temperature = Quantity(
        description='The temperature of the substrate during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    solvent_volume = Quantity(
        description='volume of the precursor solution used for spin coating.',
        type=float,
        unit='ml',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='ml'),
    )

    dispense_start_time = Quantity(
        description="""Time of the start of the dispensing in seconds after the start of the spin-coating program.
        For static spin-coating where the solution is added before the spinning starts, this is 0.""",
        type=float,
        unit='s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='s'),
    )

    dispense_speed = Quantity(
        description='The dispense speed of the precursor solution.',
        type=float,
        unit='ml/s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='ml/s'),
    )

    distance_between_tip_and_substrate = Quantity(
        description='Distance between the pipet tip and the substrate.',
        type=float,
        unit='mm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mm'),
    )

    # Subsections
    spin_coating_steps = SubSection(
        section_def=SpinCoatingSteps,
        description='Description of each spin-coating step.',
        repeats=True,
    )

    solution = SubSection(
        section_def=Solution,
        description='Details about the solution.',
    )

    environmental_conditions = SubSection(
        section_def=EnvironmentalConditionsDeposition,
        description='Environmental conditions during the activity.',
    )

    antisolvent_details = SubSection(
        section_def=AntiSolventDetails,
        description='Details about the antisolvent treatment.',
    )

    gas_quenching_details = SubSection(
        section_def=GasQuenchingDetails,
        description='Details about the gas quenching treatment.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'SpinCoating'


class SprayCoating(DepositionStep):
    """
    Details for a spray coating process
    """

    # Numerical qunatities

    nozzle_speed = Quantity(
        description='The speed of the nozzle.',
        type=float,
        unit='mm/s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mm/s'),
    )

    nozzle_angle = Quantity(
        description='The angle of the nozzle.',
        type=float,
        unit='degree',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='degree'
        ),
    )

    nozzle_height = Quantity(
        description='The distance between thesample and the nozzle.',
        type=float,
        unit='mm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mm'),
    )

    solution_volume = Quantity(
        description='The volume of the ink used.',
        type=float,
        unit='ml',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='ml'),
    )

    solution_temperature = Quantity(
        description='The temperature of the solution during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    sample_temperature = Quantity(
        description='The temperature of the sample during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    sample_area = Quantity(
        description='The area of the samples being sprayed.',
        type=float,
        unit='cm^2',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='cm^2'),
    )

    gas_pressure = Quantity(
        description='The gas pressure.',
        type=float,
        unit='Pa',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='Pa'),
    )

    # categorical qunatities
    carrier_gas = Quantity(
        description='The carrier gas.',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=['air', 'dry air', 'N2', 'Ar', 'He', 'O2', 'H2', 'other']
            ),
        ),
    )

    # Subsectinos
    solution = SubSection(
        section_def=Solution,
        description='Details about the solution.',
    )

    environmental_conditions = SubSection(
        section_def=EnvironmentalConditionsDeposition,
        description='Environmental conditions during the activity.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'SprayCoating'


class Sputtering(DepositionStep):
    """
    Details for a sputtering process
    """

    # Numerical qunatities

    substrate_temperature = Quantity(
        description='The temperature of the substrate during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    substrate_rotation_speed = Quantity(
        description='The rotation speed of the substrate during the activity.',
        type=float,
        unit='rpm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='rpm'),
    )

    # Categorical qunatities
    type_of_sputering = Quantity(
        description='The type of sputtering process',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'DC sputtering',
                    'RF sputtering',
                    'Magnetron sputtering',
                    'Reactive sputtering',
                    'Pulsed DC sputtering',
                    'other',
                ]
            ),
        ),
    )

    # Subsections
    steps = SubSection(
        section_def=SputteringStep,
        description='Details about the sputtering steps.',
        repeats=True,
    )

    target = SubSection(
        section_def=SputteringTarget,
        description='Details about the sputtering target.',
    )

    gases = SubSection(
        section_def=GasComponent,
        description='The gases in the mixture. For reactive sputtering',
        repeats=True,
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'Sputtering'


class Storage(DepositionStep):
    """
    Details for a storage process
    """

    # Subsections
    environmental_conditions = SubSection(
        section_def=EnvironmentalConditionsDeposition,
        description='Environmental conditions during the activity.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'Storage'


class UVOzonTreatment(DepositionStep):
    """
    UVOzon treatment
    """

    # Boolean qunatities
    uv_illuminated = Quantity(
        description="""
            TRUE if the if the samples is illuminated by UV-light. FALSE if samples only are treated with ozone.',
            """,
        type=bool,
        shape=[],
        a_eln=dict(component='BoolEditQuantity'),
    )

    # Numerical quantities

    substrate_temperature = Quantity(
        description='The temperature of the substrate during the activity.',
        type=float,
        unit='celsius',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='celsius'
        ),
    )

    uv_wavelength = Quantity(
        description='The wavelength of the UV light.',
        type=float,
        unit='nm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='nm'),
    )

    uv_intensity = Quantity(
        description='Intensity of the illumination.',
        type=float,
        unit='W/m^2',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='W/m^2'),
    )

    # Subsections
    environmental_conditions = SubSection(
        section_def=EnvironmentalConditionsDeposition,
        description='Environmental conditions during the activity.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.method = 'UVOzonTreatment'


### Deposition procedures top sections
class DepositionProcedure(ArchiveSection):
    """
    This is the section for the deposition procedure of a layer.
    """

    ## Top layer quantities
    substrate_layer = Quantity(
        description="""The layer on which the layer is deposited.
        The layer are ordered from bottom (furthest from the sun) to top (closest to the sun).
        Indicate if the layer was deposited on a layer that is below or above it in the device 
        (when the device is oriented with the top towards the sun)
        There are a few exceptions in that a layer can be a substrate, 
        it could be a layer that laminates two subcells, 
        and it could be a layer that is not deposited at all (like an air gap) 
        """,
        type=MEnum(
            [
                'is substrate',
                'on lower layer',
                'on upper layer',
                'laminate layers',
                'not-deposited',
            ]
        ),
        a_eln=ELNAnnotation(component='EnumEditQuantity'),
    )

    origin = Quantity(
        description='The place where the layer was deposited. i.e. was it deposited in the lab or was it bought. An example of a layer that often is bought is the ITO layer on glass substrates',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'commercial supplier',
                    'deposited in house',
                    'deposited by collaborator',
                ]
            ),
        ),
    )

    time_stamp = Quantity(
        description='Date the layer was deposited',
        type=Datetime,
        a_eln=ELNAnnotation(component='DateTimeEditQuantity'),
    )

    duration = Quantity(
        type=float,
        description='The time it takes to deposit the layer from start to finish.',
        unit='minute',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='minute'
        ),
    )

    time_from_last_step = Quantity(
        description="""The time from the finalization of the last layer 
        and the start of the deposition of this.""",
        type=float,
        unit='hr',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='hr'),
    )

    ## Subsections
    # Deposition steps
    steps = SubSection(
        section_def=DepositionStep,
        description='The steps of the deposition procedure.',
        repeats=True,
    )

    # Sample history
    sample_history = SubSection(
        section_def=EnvironmentalConditionsDeposition,
        description="""A description of the conditions under which the sample have been stored between
        the finalization of the last layer and the deposition of this layer.""",
    )


### Layers
class Layer(ArchiveSection):
    """
    This is the section for a layer in the device stack.
    """

    # Top level quantities
    name = Quantity(
        type=str,
        shape=[],
        description=""" A sensible name for the layer. A good default is the trade 
        name of the material, possibly with an addition of the microstructure.
        examples: 
        * TiO2-mp
        * PEDOT:PSS
        * Spiro-MeOTAD
        * SLG
        * ITO
        """,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    device_subset = Quantity(
        type=int,
        shape=[],
        description="""
            If the device not is monolithic, this describes which individual subcell the layer belongs to.  

            - 0 = the layer belongs to a monolithic device 
            - 1 = the layer belongs to the bottom subcell, 
            - 2 = the layer belongs to the second subcell (top cell in a 2-junction device)
            - 3 = the layer belongs to the third subcell (top cell in a 3-junction device
            """,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    functionality = Quantity(
        type=str,
        shape=[],
        description='The primary functionality the layer has in the device stack.',
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'air gap',
                    'anti reflection',
                    'back contact',
                    'back reflector',
                    'buffer layer',
                    'down conversion',
                    'edge sealing',
                    'electrolyte',
                    'encapsulation',
                    'electron transport layer',
                    'front contact',
                    'hole transport layer',
                    'interface modifier',
                    'mesoporous scaffold',
                    'middle contact',
                    'optical spacer',
                    'organic dye',
                    'photoabsorber',
                    'recombination layer',
                    'refractive index matching',
                    'self assembled monolayer',
                    'spectral splitter',
                    'substrate',
                    'transparent conducting oxide',
                    'up conversion',
                    'window layer',
                ]
            ),
        ),
    )

    ### Subsections
    # Deposition procedure
    deposition_procedure = SubSection(
        section_def=DepositionProcedure,
        description='The deposition procedure of the layer.',
    )

    # Post deposition procedure
    post_deposition_procedure = SubSection(
        section_def=PostDepositionProcedure,
        description='Post deposition procedure.',
    )

    ## Properties of the layer
    properties = SubSection(
        section_def=LayerProperties,
        description='Properties of the layer.',
    )

    # Derived quantities
    layer_index = Quantity(
        type=int,
        shape=[],
        description="""The position in the device stack for the layer. Counted from the bottom. Can be populated automatically """,
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)


### Specialised layers
class GeneralLayer(Layer):
    """
    This is the section for a general layer in the device stack.
    """

    ### Subsections
    # Compounds in the layer
    components = SubSection(
        section_def=Component,
        description='The components in the layer.',
        repeats=True,
    )


class Photoabsorber(Layer):
    """
    This is the section for a photoabsorber layer in the device stack.
    """

    # Compounds in the layer
    components = SubSection(
        section_def=Component,
        description='The components in the layer.',
        repeats=True,
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)


## Photoabsorbers
class CIGSComposition(ArchiveSection):
    """
    This is the section for the composition of a CIGS photoabsorber.
    """

    # Numerical quantities
    Cu = Quantity(
        description='The stoichiometric coefficient for Cu',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    In = Quantity(
        description='The stoichiometric coefficient for In',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    Ga = Quantity(
        description='The stoichiometric coefficient for Ga',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    Se = Quantity(
        description='The stoichiometric coefficient for Se',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )


class CZTSComposition(ArchiveSection):
    """
    This is the section for the composition of a CIGS photoabsorber.
    """

    # Numerical quantities
    Cu = Quantity(
        description='The stoichiometric coefficient for Cu',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    Zn = Quantity(
        description='The stoichiometric coefficient for Zn',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    Sn = Quantity(
        description='The stoichiometric coefficient for Sn',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    S = Quantity(
        description='The stoichiometric coefficient for S',
        type=float,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )


class Photoabsorber_Perovskite(Photoabsorber):
    """
    This is the section for a perovskite photoabsorber.
    """

    lead_free = Quantity(
        description="""True if the perovskite does not contain any lead.""",
        type=bool,
        shape=[],
        a_eln=dict(component='BoolEditQuantity'),
    )

    inorganic = Quantity(
        description="""True if the perovskite is inorganic.""",
        type=bool,
        shape=[],
        a_eln=dict(component='BoolEditQuantity'),
    )

    double_perovskite = Quantity(
        description="""True if it is a double perovskite structure. 
        A double perovksite is strictly not a perovskite, but as if 
        in terms of PV development often is treated as a perovskite, 
        it is worth including it but with a flag indicating the structure.""",
        type=bool,
        shape=[],
        a_eln=dict(component='BoolEditQuantity'),
    )

    has_a_2D_perovskite_capping_layer = Quantity(
        description="""True if the perovskite has a thin capping layer of a 2D perovskite.""",
        type=bool,
        shape=[],
        a_eln=dict(component='BoolEditQuantity'),
    )

    # Subsections
    composition = SubSection(
        section_def=PerovskiteCompositionSection,
        description='The composition of the perovskite.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)

        if not self.name:
            self.name = 'Perovskite'


class Photoabsorber_Silicon(Photoabsorber):
    """
    This is the section for a silicon photoabsorber.
    """

    cell_type = Quantity(
        description='The type of silicon cell.',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'Amorphous',
                    'Al-BSF',
                    'c-type',
                    'HIT',
                    'HJT',
                    'Heterojunction',
                    'Homojunction',
                    'IBC',
                    'n-type',
                    'p-type',
                    'PERC',
                    'PERL',
                    'SC/nFAB',
                    'TOPCon',
                    'other',
                ]
            ),
        ),
    )

    type_of_silicon = Quantity(
        description='The type of silicon.',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'Amorphous',
                    'Monocrystalline',
                    'Polycrystalline',
                    'CZ',
                    'Float-zone',
                    'other',
                ]
            ),
        ),
    )

    doping_sequence = Quantity(
        description='Description of the doping sequence.',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)

        if not self.name:
            self.name = 'Silicon'


class Photoabsorber_CIGS(Photoabsorber):
    """
    This is the section for a CIGS photoabsorber.
    """

    # Derived quantities
    molecular_formula = Quantity(
        description='The molecular formula. Can be derived automatically based on the stoichiometric coefficients',
        type=str,
    )

    # Subsections
    composition = SubSection(
        section_def=CIGSComposition,
        description='The composition of the CIGS.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)

        # Generate molecular formula
        formula_str = ''
        if self.composition:
            for key in self.composition.__dict__.keys():
                if re.fullmatch(r'^[A-Z][a-z]?$', key):
                    coef = getattr(self.composition, key)
                    coef_str = f'{coef:.2f}'
                    if coef_str == '0.00':
                        pass
                    elif coef_str == '1.00':
                        formula_str += key
                    else:
                        coef_str = re.sub(
                            r'(\.\d*?[1-9])0+$', r'\1', re.sub(r'\.0+$', '', coef_str)
                        )
                        formula_str += f'{key}{coef_str}'
        self.molecular_formula = formula_str

        # Set layer name if not set
        if not self.name:
            self.name = 'CIGS'


class Photoabsorber_CZTS(Photoabsorber):
    """
    This is the section for a CZTS photoabsorber.
    """

    # Derived quantities
    molecular_formula = Quantity(
        description='The molecular formula. Can be derived automatically based on the stoichiometric coefficients',
        type=str,
    )

    # Subsections
    composition = SubSection(
        section_def=CZTSComposition,
        description='The composition of the CZTS.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)

        # Generate molecular formula
        formula_str = ''
        if self.composition:
            for key in self.composition.__dict__.keys():
                if re.fullmatch(r'^[A-Z][a-z]?$', key):
                    coef = getattr(self.composition, key)
                    coef_str = f'{coef:.2f}'
                    if coef_str == '0.00':
                        pass
                    elif coef_str == '1.00':
                        formula_str += key
                    else:
                        coef_str = re.sub(
                            r'(\.\d*?[1-9])0+$', r'\1', re.sub(r'\.0+$', '', coef_str)
                        )
                        formula_str += f'{key}{coef_str}'
        self.molecular_formula = formula_str

        # Set layer name if not set
        if not self.name:
            self.name = 'CZTS'


class Photoabsorber_GaAs(Photoabsorber):
    """
    This is the section for a CIGS photoabsorber.
    """

    # Derived quantities
    molecular_formula = Quantity(
        description='The molecular formula. Can be derived automatically based on the stoichiometric coefficients',
        type=str,
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.molecular_formula = 'GaAs'

        # Set layer name if not set
        if not self.name:
            self.name = 'GaAs'


class Photoabsorber_OPV(Photoabsorber):
    """
    This is the section for a organic photoabsorber.
    """

    blend = Quantity(
        description='The name of the OPV blend. Often in the form - "name of acceptor:"name of donor"',
        type=str,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    cell_type = Quantity(
        description='The type of opv cell',
        type=str,
        a_eln=ELNAnnotation(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'single layer',
                    'bilayer',
                    'polymer',
                    'heterojunction',
                    'bulk heterojunction',
                    'polymer bulk heterojunction',
                    'homojunction',
                ]
            ),
        ),
    )

    peak_absorption_wavelength = Quantity(
        description='The wavelength at maximum absorption',
        type=float,
        unit='nm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='nm'),
    )

    molar_extinction_coefficient = Quantity(
        description='The molar extinction coefficient',
        type=float,
        unit='L*mol^1*cm^-1',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='L*mol^1*cm^-1'
        ),
    )

    homo_level = Quantity(
        description='The energy of the HOMO level',
        type=float,
        unit='eV',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='eV'),
    )

    lumo_level = Quantity(
        description='The energy of the LUMO level',
        type=float,
        unit='eV',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='eV'),
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)

        # Set layer name if not set
        if not self.name:
            self.name = 'OPV'


class Photoabsorber_DSSC(Photoabsorber):
    """
    This is the section for a organic photoabsorber.
    """

    peak_absorption_wavelength = Quantity(
        description='The wavelength at maximum absorption',
        type=float,
        unit='nm',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='nm'),
    )

    molar_extinction_coefficient = Quantity(
        description='The molar extinction coefficient',
        type=float,
        unit='L*mol^1*cm^-1',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='L*mol^1*cm^-1'
        ),
    )

    homo_level = Quantity(
        description='The energy of the HOMO level',
        type=float,
        unit='eV',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='eV'),
    )

    lumo_level = Quantity(
        description='The energy of the LUMO level',
        type=float,
        unit='eV',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='eV'),
    )

    oxidation_potential = Quantity(
        description='The oxidation potential vs the normal hydrogen electrode',
        type=float,
        unit='V',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='V'),
    )

    # subsections
    dye = SubSection(
        section_def=LigandsAndDyes,
        description='The components.',
        repeats=True,
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)

        # Set layer name if not set
        if not self.name:
            self.name = 'DSSC'


class Photoabsorber_QuantumDot(Photoabsorber):
    """
    This is the section for a quantum dot photoabsorbers.
    """

    # subsections
    # Nanostructure information
    nanostructuration = SubSection(
        section_def=NanostructureInformation,
        description='The nanostructure information of the compound.',
    )

    ligands = SubSection(
        section_def=LigandsAndDyes,
        description='The components.',
        repeats=True,
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)

        # Set layer name if not set
        if not self.name:
            self.name = 'QD-absorber'


class PhotoabsorberOther(Photoabsorber):
    """
    This is the section for a photoabsorber layer not described by a dedicated class.
    """

    def normalize(self, archive, logger):
        super().normalize(archive, logger)

        # Set layer name if not set
        if not self.name:
            self.name = 'Other Photoabsorber'


m_package.__init_metainfo__()
