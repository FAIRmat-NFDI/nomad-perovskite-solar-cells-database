#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from typing import TYPE_CHECKING

from ase import Atoms
from nomad.datamodel.data import (
    EntryData,
    EntryDataCategory,
)
from nomad.datamodel.datamodel import (
    ArchiveSection,
    EntryArchive,
)
from nomad.datamodel.metainfo.annotations import (
    ELNAnnotation,
    ELNComponentEnum,
    Filter,
    SectionProperties,
)
from nomad.datamodel.metainfo.basesections import (
    CompositeSystem,
    PubChemPureSubstanceSection,
    PureSubstance,
    PureSubstanceComponent,
    SystemComponent,
)
from nomad.datamodel.results import (
    Material,
    Properties,
    Relation,
    Results,
    System,
)
from nomad.metainfo.metainfo import (
    Category,
    MEnum,
    Package,
    Quantity,
    Reference,
    Section,
    SubSection,
)
from nomad.normalizing.common import nomad_atoms_from_ase_atoms
from nomad.normalizing.topology import add_system, add_system_info

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

m_package = Package()


def convert_rdkit_mol_to_ase_atoms(rdkit_mol):
    """
    Convert an RDKit molecule to an ASE atoms object.

    Args:
        rdkit_mol (rdkit.Chem.Mol): RDKit molecule object.

    Returns:
        ase.Atoms: ASE atoms object.
    """
    positions = rdkit_mol.GetConformer().GetPositions()
    atomic_numbers = [atom.GetAtomicNum() for atom in rdkit_mol.GetAtoms()]
    ase_atoms = Atoms(numbers=atomic_numbers, positions=positions)
    return ase_atoms


def optimize_molecule(smiles):
    from rdkit import Chem
    from rdkit.Chem import AllChem

    try:
        m = Chem.MolFromSmiles(smiles)
        m = Chem.AddHs(m)

        AllChem.EmbedMolecule(m)
        AllChem.MMFFOptimizeMolecule(m)

        ase_atoms = convert_rdkit_mol_to_ase_atoms(m)

        # Further processing
        # ...
        return ase_atoms
    except Exception as e:
        print(f'An error occurred: {e}')


class PerovskiteCompositionCategory(EntryDataCategory):
    m_def = Category(label='Perovskite Composition', categories=[EntryDataCategory])


class PerovskiteChemicalSection(ArchiveSection):
    common_name = Quantity(
        type=str,
        description='The common trade name',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        shape=[],
    )
    molecular_formula = Quantity(
        type=str,
        description='The molecular formula',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        shape=[],
    )
    smiles = Quantity(
        type=str,
        description='The canonical SMILE string',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        shape=[],
    )
    iupac_name = Quantity(
        type=str,
        description='The standard IUPAC name',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        shape=[],
    )
    cas_number = Quantity(
        type=str,
        description='The CAS number if available',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        shape=[],
    )

    def to_topology_system(self) -> System:
        """
        Convert the section to a system.

        Returns:
            System: The system object.
        """
        atoms=optimize_molecule(self.smiles)
        structural_type = 'molecule'
        if len(atoms) == 1:
            structural_type = 'atom'
        return System(
            label=self.common_name,
            method='parser',
            atoms=atoms,
            structural_type=structural_type,
        )


class PerovskiteIonSection(PerovskiteChemicalSection):
    abbreviation = Quantity(
        type=str,
        description='The standard abbreviation of the ion. If the abbreviation is in the archive, additional data is complemented automatically',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        shape=[],
    )
    source_compound_molecular_formula = Quantity(
        type=str,
        description='The molecular formula of the source compound',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        shape=[],
    )
    source_compound_smiles = Quantity(
        type=str,
        description='The canonical SMILE string of the source compound',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        shape=[],
    )
    source_compound_iupac_name = Quantity(
        type=str,
        description='The standard IUPAC name of the source compound',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        shape=[],
    )
    source_compound_cas_number = Quantity(
        type=str,
        description='The CAS number if available of the source compound',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        shape=[],
    )


class PerovskiteIon(PureSubstance, PerovskiteIonSection):
    """
    Abstract class for describing a general perovskite ion.
    """

    m_def = Section(
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(
                    exclude=[
                        'description',
                        'name',
                        'lab_id',
                        'pure_substance',
                        'source_compound',
                        'datetime',
                    ],
                ),
                order=[
                    'abbreviation',
                    'common_name',
                    'molecular_formula',
                    'smiles',
                    'iupac_name',
                    'cas_number',
                    'source_compound_molecular_formula',
                    'source_compound_smiles',
                    'source_compound_iupac_name',
                    'source_compound_cas_number',
                ]
            )
        )
    )
    abbreviation = Quantity(
        type=str,
        description='The standard abbreviation of the ion. If the abbreviation is in the archive, additional data is complemented automatically',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        shape=[],
    )
    pure_substance = SubSection(
        section_def=PubChemPureSubstanceSection,
        description="""
        Section with properties describing the substance.
        """,
    )
    source_compound = SubSection(
        section_def=PubChemPureSubstanceSection,
        description="""
        Section with properties describing the substance.
        """,
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        """
        The normalizer for the `PerovskiteIon` class.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        """
        pure_substance = PubChemPureSubstanceSection(
            molecular_formula=self.molecular_formula,
            smile=self.smiles,
            iupac_name=self.iupac_name,
            cas_number=self.cas_number,
            name=self.common_name,
        )
        pure_substance.normalize(archive, logger)
        if self.molecular_formula is None:
            self.molecular_formula = pure_substance.molecular_formula
        if self.smiles is None:
            self.smiles = pure_substance.smile
        if self.iupac_name is None:
            self.iupac_name = pure_substance.iupac_name
        if self.cas_number is None:
            self.cas_number = pure_substance.cas_number
        if self.common_name is None:
            self.common_name = pure_substance.name
        self.pure_substance = pure_substance
        source_compound = PubChemPureSubstanceSection(
            molecular_formula=self.source_compound_molecular_formula,
            smile=self.source_compound_smiles,
            iupac_name=self.source_compound_iupac_name,
            cas_number=self.source_compound_cas_number,
        )
        source_compound.normalize(archive, logger)
        if self.source_compound_molecular_formula is None:
            self.source_compound_molecular_formula = source_compound.molecular_formula
        if self.source_compound_smiles is None:
            self.source_compound_smiles = source_compound.smile
        if self.source_compound_iupac_name is None:
            self.source_compound_iupac_name = source_compound.iupac_name
        if self.source_compound_cas_number is None:
            self.source_compound_cas_number = source_compound.cas_number
        self.source_compound = source_compound
        super().normalize(archive, logger)
        # if self.smiles is not None:
        #     system = self.to_topology_system()



class PerovskiteAIon(PerovskiteIon, EntryData):
    m_def = Section(
        categories=[PerovskiteCompositionCategory],
        label='Perovskite A Ion',
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(
                    exclude=[
                        'description',
                        'name',
                        'lab_id',
                        'datetime',
                    ],
                ),
                editable=Filter(
                    exclude=[
                        'pure_substance',
                        'source_compound',
                        'elemental_composition',
                    ]
                ),
                order=[
                    'abbreviation',
                    'common_name',
                    'molecular_formula',
                    'smiles',
                    'iupac_name',
                    'cas_number',
                    'source_compound_molecular_formula',
                    'source_compound_smiles',
                    'source_compound_iupac_name',
                    'source_compound_cas_number',
                ]
            )
        )
    )


class PerovskiteBIon(PerovskiteIon, EntryData):
    m_def = Section(
        categories=[PerovskiteCompositionCategory],
        label='Perovskite B Ion',
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(
                    exclude=[
                        'description',
                        'name',
                        'lab_id',
                        'datetime',
                    ],
                ),
                editable=Filter(
                    exclude=[
                        'pure_substance',
                        'source_compound',
                        'elemental_composition',
                    ]
                ),
                order=[
                    'abbreviation',
                    'common_name',
                    'molecular_formula',
                    'smiles',
                    'iupac_name',
                    'cas_number',
                    'source_compound_molecular_formula',
                    'source_compound_smiles',
                    'source_compound_iupac_name',
                    'source_compound_cas_number',
                ]
            )
        )
    )


class PerovskiteCIon(PerovskiteIon, EntryData):
    m_def = Section(
        categories=[PerovskiteCompositionCategory],
        label='Perovskite C Ion',
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(
                    exclude=[
                        'description',
                        'name',
                        'lab_id',
                        'datetime',
                    ],
                ),
                editable=Filter(
                    exclude=[
                        'pure_substance',
                        'source_compound',
                        'elemental_composition',
                    ]
                ),
                order=[
                    'abbreviation',
                    'common_name',
                    'molecular_formula',
                    'smiles',
                    'iupac_name',
                    'cas_number',
                    'source_compound_molecular_formula',
                    'source_compound_smiles',
                    'source_compound_iupac_name',
                    'source_compound_cas_number',
                ]
            )
        )
    )


class PerovskiteIonComponent(SystemComponent, PerovskiteIonSection):
    m_def = Section(
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(
                    exclude=[
                        'name',
                        'mass',
                        'mass_fraction',
                    ],
                ),
                order=[
                    'system',
                    'coefficient',
                    'abbreviation',
                    'common_name',
                    'molecular_formula',
                    'smiles',
                    'iupac_name',
                    'cas_number',
                    'source_compound_molecular_formula',
                    'source_compound_smiles',
                    'source_compound_iupac_name',
                    'source_compound_cas_number',
                ]
            )
        )
    )
    coefficient = Quantity(
        type=float,
        description='The stoichiometric coefficient',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
        shape=[],
    )
    system = Quantity(
        type=Reference(PerovskiteIon.m_def),
        description='A reference to the component system.',
        a_eln=dict(component='ReferenceEditQuantity'),
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        """
        The normalizer for the `IonComponent` class.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        """
        super().normalize(archive, logger)
        if not isinstance(self.system, PerovskiteIon):
            return
        if self.abbreviation is None:
            self.abbreviation = self.system.abbreviation
        if self.molecular_formula is None:
            self.molecular_formula = self.system.molecular_formula
        if self.smiles is None:
            self.smiles = self.system.smiles
        if self.iupac_name is None:
            self.iupac_name = self.system.iupac_name
        if self.cas_number is None:
            self.cas_number = self.system.cas_number
        if self.source_compound_molecular_formula is None:
            self.source_compound_molecular_formula = self.system.source_compound_molecular_formula
        if self.source_compound_smiles is None:
            self.source_compound_smiles = self.system.source_compound_smiles
        if self.source_compound_iupac_name is None:
            self.source_compound_iupac_name = self.system.source_compound_iupac_name
        if self.source_compound_cas_number is None:
            self.source_compound_cas_number = self.system.source_compound_cas_number


class PerovskiteAIonComponent(PerovskiteIonComponent):
    m_def = Section(
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(
                    exclude=[
                        'name',
                        'mass',
                        'mass_fraction',
                    ],
                ),
                order=[
                    'system',
                    'coefficient',
                    'abbreviation',
                    'common_name',
                    'molecular_formula',
                    'smiles',
                    'iupac_name',
                    'cas_number',
                    'source_compound_molecular_formula',
                    'source_compound_smiles',
                    'source_compound_iupac_name',
                    'source_compound_cas_number',
                ]
            )
        )
    )
    system = Quantity(
        type=Reference(PerovskiteAIon.m_def),
        description='A reference to the component system.',
        a_eln=dict(component='ReferenceEditQuantity'),
    )


class PerovskiteBIonComponent(PerovskiteIonComponent):
    m_def = Section(
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(
                    exclude=[
                        'name',
                        'mass',
                        'mass_fraction',
                    ],
                ),
                order=[
                    'system',
                    'coefficient',
                    'abbreviation',
                    'common_name',
                    'molecular_formula',
                    'smiles',
                    'iupac_name',
                    'cas_number',
                    'source_compound_molecular_formula',
                    'source_compound_smiles',
                    'source_compound_iupac_name',
                    'source_compound_cas_number',
                ]
            )
        )
    )
    system = Quantity(
        type=Reference(PerovskiteBIon.m_def),
        description='A reference to the component system.',
        a_eln=dict(component='ReferenceEditQuantity'),
    )


class PerovskiteCIonComponent(PerovskiteIonComponent):
    m_def = Section(
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(
                    exclude=[
                        'name',
                        'mass',
                        'mass_fraction',
                    ],
                ),
                order=[
                    'system',
                    'coefficient',
                    'abbreviation',
                    'common_name',
                    'molecular_formula',
                    'smiles',
                    'iupac_name',
                    'cas_number',
                    'source_compound_molecular_formula',
                    'source_compound_smiles',
                    'source_compound_iupac_name',
                    'source_compound_cas_number',
                ]
            )
        )
    )
    system = Quantity(
        type=Reference(PerovskiteCIon.m_def),
        description='A reference to the component system.',
        a_eln=dict(component='ReferenceEditQuantity'),
    )


class Impurity(PureSubstanceComponent, PerovskiteChemicalSection):
    m_def = Section(
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(
                    exclude=[
                        'name',
                        'mass',
                    ],
                ),
                order=[
                    'abbreviation',
                    'concentration',
                    'mass_fraction',
                    'common_name',
                    'molecular_formula',
                    'smiles',
                    'iupac_name',
                    'cas_number',
                ]
            )
        )
    )
    abbreviation = Quantity(
        type=str,
        description='The abbreviation used for the additive or impurity.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        shape=[],
    )
    concentration = Quantity(
        type=float,
        description='The concentration of the additive or impurity.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity, defaultDisplayUnit='mol%'
        ),
        unit='cm^-3',
        shape=[],
    )
    pure_substance = SubSection(
        section_def=PubChemPureSubstanceSection,
        description="""
        Section describing the pure substance that is the component.
        """,
    )
    
    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        """
        The normalizer for the `Impurity` class.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        """
        pure_substance = PubChemPureSubstanceSection(
            name=self.common_name,
            molecular_formula=self.molecular_formula,
            smile=self.smiles,
            iupac_name=self.iupac_name,
            cas_number=self.cas_number,
        )
        pure_substance.normalize(archive, logger)
        if self.molecular_formula is None:
            self.molecular_formula = pure_substance.molecular_formula
        if self.smiles is None:
            self.smiles = pure_substance.smile
        if self.iupac_name is None:
            self.iupac_name = pure_substance.iupac_name
        if self.cas_number is None:
            self.cas_number = pure_substance.cas_number
        if self.common_name is None:
            self.common_name = pure_substance.name
        super().normalize(archive, logger)


class PerovskiteComposition(CompositeSystem, EntryData):
    """
    Schema for describing a perovskite composition.
    """

    m_def = Section(
        categories=[PerovskiteCompositionCategory],
        label='Perovskite Composition',
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(
                    exclude=[
                        'datetime',
                        'description',
                        'name',
                        'lab_id', 
                    ],
                ),
                order=[
                    'short_form',
                    'long_form',
                    'composition_estimate',
                    'sample_type',
                    'dimensionality',
                    'band_gap',
                    'a_ions',
                    'b_ions',
                    'c_ions',
                    'impurities',
                    'additives',
                ]
            )
        )
    )
    short_form = Quantity(
        type=str,
    )
    long_form = Quantity(
        type=str,
    )
    composition_estimate = Quantity(
        type=MEnum(
            [
                'Estimated from precursor solutions',
                'Literature value',
                'Estimated from XRD data',
                'Estimated from spectroscopic data',
                'Theoretical simulation',
                'Hypothetical compound',
                'Other',
            ]
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.EnumEditQuantity),
    )
    sample_type = Quantity(
        type=MEnum(
            [
                'Polycrystalline film',
                'Single crystal',
                'Quantum dots',
                'Nano rods',
                'Colloidal solution',
                'Amorphous',
                'Other',
            ]
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.EnumEditQuantity),
    )
    dimensionality = Quantity(
        type=MEnum(['0D', '1D', '2D', '2D/3D', '3D', 'Other']),
        description='The dimensionality of the perovskite, i.e. 3D, 2D, 1D (nanorods), quantum dots (0D), etc.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.EnumEditQuantity),
    )
    band_gap = Quantity(
        type=float,
        description='Band gap of photoabsorber in eV.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity, defaultDisplayUnit='eV'
        ),
        unit='eV',
        shape=[],
    )
    a_ions = SubSection(
        section_def=PerovskiteAIonComponent,
        repeats=True,
    )
    b_ions = SubSection(
        section_def=PerovskiteBIonComponent,
        repeats=True,
    )
    c_ions = SubSection(
        section_def=PerovskiteCIonComponent,
        repeats=True,
    )
    impurities = SubSection(
        section_def=Impurity,
        repeats=True,
    )
    additives = SubSection(
        section_def=Impurity,
        repeats=True,
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        """
        The normalizer for the `PerovskiteComposition` class.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        """
        if not archive.results:
            archive.results = Results()
        if not archive.results.material:
            archive.results.material = Material()
        if not archive.results.properties:
            archive.results.properties = Properties()
        ions: list[PerovskiteIonComponent] = self.a_ions + self.b_ions + self.c_ions
        self.components = ions
        if not any(ion.coefficient is None for ion in ions):
            coefficient_sum = sum([ion.coefficient for ion in ions])
            for component in self.components:
                if (
                    not isinstance(component, PerovskiteIonComponent)
                    or not isinstance(component.system, PerovskiteIon)
                    or not isinstance(
                        component.system.pure_substance, PubChemPureSubstanceSection
                    )
                    or component.system.pure_substance.molecular_mass is None
                ):
                    continue
                component.mass_fraction = (
                    component.system.pure_substance.molecular_mass
                    * component.coefficient
                    / coefficient_sum
                )
        self.short_form = ''
        self.long_form = ''
        for ion in ions:
            if ion.abbreviation is None:
                continue
            self.short_form += ion.abbreviation
            if ion.coefficient is None:
                continue
            if ion.coefficient == 1:
                coefficient_str = ''
            elif ion.coefficient == int(ion.coefficient):
                coefficient_str = str(int(ion.coefficient))
            else:
                coefficient_str = f'{ion.coefficient:.2}'
            self.long_form += f'{ion.abbreviation}{coefficient_str}'

        if self.dimensionality in ['0D', '1D', '2D', '3D']:
            archive.results.properties.dimensionality = self.dimensionality
            if self.dimensionality == '3D':
                archive.results.material.structural_type = 'bulk'
            elif self.dimensionality != '0D':
                archive.results.material.structural_type = self.dimensionality
        super().normalize(archive, logger)

        topology = {}
        # Add original system
        parent_system = System(
            label='Perovskite Composition',
            description='A system describing the chemistry and components of the perovskite.',
            system_relation=Relation(type='root'),
        )

        parent_system.structural_type = archive.results.material.structural_type
        parent_system.chemical_formula_hill = (
            archive.results.material.chemical_formula_hill
        )
        parent_system.elements = archive.results.material.elements
        parent_system.chemical_formula_iupac = (
            archive.results.material.chemical_formula_iupac
        )

        add_system(parent_system, topology)
        add_system_info(parent_system, topology)

        sub_systems: list[PerovskiteChemicalSection] = ions + self.impurities + self.additives
        for sub_system in sub_systems:
            child_system = sub_system.to_topology_system()
            add_system(child_system, topology, parent_system)
            add_system_info(child_system, topology)

        material = archive.m_setdefault('results.material')
        for system in topology.values():
            material.m_add_sub_section(Material.topology, system)

        # topology contains an extra parent
        if len(sub_systems) == len(material.topology) - 1:
            for i in range(len(self.ions)):
                material.topology[i + 1].chemical_formula_descriptive = self.ions[
                    i
                ].name


m_package.__init_metainfo__()
