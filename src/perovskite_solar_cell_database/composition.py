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

import re
from typing import TYPE_CHECKING

from ase import Atoms
from nomad.atomutils import (
    Formula,
)
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
    elemental_composition_from_formula,
)
from nomad.datamodel.metainfo.common import (
    ProvenanceTracker,
)
from nomad.datamodel.results import (
    BandGap,
    ElectronicProperties,
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
from nomad.normalizing.topology import (
    add_system,
    add_system_info,
)
from structlog.stdlib import BoundLogger

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
        if self.smiles is None:
            return System(label=self.common_name)
        ase_atoms = optimize_molecule(self.smiles)
        atoms = nomad_atoms_from_ase_atoms(ase_atoms)
        structural_type = 'molecule'
        if len(ase_atoms) == 1:
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
                ],
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
        self.lab_id = 'perovskite_ion_' + self.abbreviation
        pure_substance = PubChemPureSubstanceSection(
            molecular_formula=self.molecular_formula,
            smile=self.smiles,
            iupac_name=self.iupac_name,
            cas_number=self.cas_number,
            name=self.common_name,
        )
        if isinstance(self.pure_substance, PubChemPureSubstanceSection):
            pure_substance.pub_chem_cid = self.pure_substance.pub_chem_cid
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
        formula = self.pure_substance.molecular_formula
        if isinstance(formula, str):
            self.pure_substance.molecular_formula = re.sub(
                r'(?<=[A-Za-z])\d*[+-]', '', formula
            )
        source_compound = PubChemPureSubstanceSection(
            molecular_formula=self.source_compound_molecular_formula,
            smile=self.source_compound_smiles,
            iupac_name=self.source_compound_iupac_name,
            cas_number=self.source_compound_cas_number,
        )
        if isinstance(self.source_compound, PubChemPureSubstanceSection):
            source_compound.pub_chem_cid = self.source_compound.pub_chem_cid
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

        system = self.to_topology_system()
        system.system_relation = Relation(type='root')
        topology = {}
        add_system(system, topology)
        add_system_info(system, topology)
        material = archive.m_setdefault('results.material')
        for system in topology.values():
            material.m_add_sub_section(Material.topology, system)


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
                ],
            )
        ),
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
                ],
            )
        ),
    )


class PerovskiteXIon(PerovskiteIon, EntryData):
    m_def = Section(
        categories=[PerovskiteCompositionCategory],
        label='Perovskite X Ion',
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
                ],
            )
        ),
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
                ],
            )
        )
    )
    coefficient = Quantity(
        type=str,
        description='The stoichiometric coefficient',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
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
            if self.abbreviation is None or archive.metadata.main_author is None:
                return
            from nomad.search import (
                MetadataPagination,
                search,
            )

            query = {
                'section_defs.definition_qualified_name:all': [
                    'perovskite_solar_cell_database.composition.PerovskiteIon'
                ],
                'results.eln.lab_ids': 'perovskite_ion_' + self.abbreviation,
            }  # TODO: Search also for smiles and molecular_formula
            search_result = search(
                owner='all',
                query=query,
                pagination=MetadataPagination(
                    page_size=1,
                    order_by='entry_create_time',
                    order='asc',
                ),
                user_id=archive.metadata.main_author.user_id,
            )
            if search_result.pagination.total > 0:
                entry_id = search_result.data[0]['entry_id']
                upload_id = search_result.data[0]['upload_id']
                self.system = f'../uploads/{upload_id}/archive/{entry_id}#data'
            else:
                logger.warn(f'Could not find system for ion {self.abbreviation}.')
                return  # TODO: Create ion
        if self.abbreviation is None:
            self.abbreviation = self.system.abbreviation
        if self.common_name is None:
            self.common_name = self.system.common_name
        if self.molecular_formula is None:
            self.molecular_formula = self.system.molecular_formula
        if self.smiles is None:
            self.smiles = self.system.smiles
        if self.iupac_name is None:
            self.iupac_name = self.system.iupac_name
        if self.cas_number is None:
            self.cas_number = self.system.cas_number
        if self.source_compound_molecular_formula is None:
            self.source_compound_molecular_formula = (
                self.system.source_compound_molecular_formula
            )
        if self.source_compound_smiles is None:
            self.source_compound_smiles = self.system.source_compound_smiles
        if self.source_compound_iupac_name is None:
            self.source_compound_iupac_name = self.system.source_compound_iupac_name
        if self.source_compound_cas_number is None:
            self.source_compound_cas_number = self.system.source_compound_cas_number


class PerovskiteAIonComponent(PerovskiteIonComponent):
    m_def = Section(
        label_quantity='abbreviation',
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
                ],
            )
        ),
    )
    system = Quantity(
        type=Reference(PerovskiteAIon.m_def),
        description='A reference to the component system.',
        a_eln=dict(component='ReferenceEditQuantity'),
    )

    def to_topology_system(self) -> System:
        system = super().to_topology_system()
        system.label = 'Perovskite A Ion: ' + self.abbreviation
        return system


class PerovskiteBIonComponent(PerovskiteIonComponent):
    m_def = Section(
        label_quantity='abbreviation',
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
                ],
            )
        ),
    )
    system = Quantity(
        type=Reference(PerovskiteBIon.m_def),
        description='A reference to the component system.',
        a_eln=dict(component='ReferenceEditQuantity'),
    )

    def to_topology_system(self) -> System:
        system = super().to_topology_system()
        system.label = 'Perovskite B Ion: ' + self.abbreviation
        return system


class PerovskiteXIonComponent(PerovskiteIonComponent):
    m_def = Section(
        label_quantity='abbreviation',
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
                ],
            ),
        ),
    )
    system = Quantity(
        type=Reference(PerovskiteXIon.m_def),
        description='A reference to the component system.',
        a_eln=dict(component='ReferenceEditQuantity'),
    )

    def to_topology_system(self) -> System:
        system = super().to_topology_system()
        system.label = 'Perovskite C Ion: ' + self.abbreviation
        return system


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
                ],
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
            component=ELNComponentEnum.NumberEditQuantity, defaultDisplayUnit='cm^-3'
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
        if isinstance(self.pure_substance, PubChemPureSubstanceSection):
            pure_substance.pub_chem_cid = self.pure_substance.pub_chem_cid
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
        super().normalize(archive, logger)


class PerovskiteCompositionSection(ArchiveSection):
    short_form = Quantity(
        type=str,
    )
    long_form = Quantity(
        type=str,
    )
    formula = Quantity(
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
    ions_a_site = SubSection(
        section_def=PerovskiteAIonComponent,
        repeats=True,
    )
    ions_b_site = SubSection(
        section_def=PerovskiteBIonComponent,
        repeats=True,
    )
    ions_x_site = SubSection(
        section_def=PerovskiteXIonComponent,
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

    def to_topology_system(self, logger: 'BoundLogger') -> System:
        system = System(
            label='Perovskite Composition',
            description='A system describing the chemistry and components of the perovskite.',
        )
        formula_str = self.get_formula_str()
        if formula_str:
            formula = Formula(formula_str)
            formula.populate(system, overwrite=True)
        else:
            logger.warn('Could not find chemical formula for Perovskite.')

        if self.dimensionality == '3D':
            system.structural_type = 'bulk'
        elif self.dimensionality in ['1D', '2D']:
            system.structural_type = self.dimensionality

        system.chemical_formula_descriptive = self.long_form
        return system

    def get_formula_str(self) -> str:
        """
        Get the formula string for the perovskite composition.

        Returns:
            str: The formula string.
        """
        a_ions_sorted = sorted(self.ions_a_site, key=lambda ion: ion.abbreviation or '')
        b_ions_sorted = sorted(self.ions_b_site, key=lambda ion: ion.abbreviation or '')
        x_ions_sorted = sorted(self.ions_x_site, key=lambda ion: ion.abbreviation or '')
        ions: list[PerovskiteIonComponent] = (
            a_ions_sorted + b_ions_sorted + x_ions_sorted
        )
        self.short_form = ''
        self.long_form = ''
        formula_str = ''
        for ion in ions:
            if ion.abbreviation is None:
                break
            self.short_form += ion.abbreviation
            if ion.coefficient is None:
                break
            # Remove trailing zeros from the coefficient
            coefficient_str = re.sub(r'(\.\d*?)0+$', r'\1', ion.coefficient)
            # Remove trailing dot if it is the last character
            coefficient_str = re.sub(r'\.$', '', coefficient_str)
            if ion.coefficient == '1':
                coefficient_str = ''
            self.long_form += f'{ion.abbreviation}{coefficient_str}'
            if not isinstance(ion.molecular_formula, str):
                break
            cleaned_formula = re.sub(r'(?<=[A-Za-z])\d*[+-]', '', ion.molecular_formula)
            formula_str += f'({cleaned_formula}){coefficient_str}'
        return formula_str

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        """
        The normalizer for the `PerovskiteCompositionSection` class.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        """
        super().normalize(archive, logger)
        self.get_formula_str()


class PerovskiteComposition(PerovskiteCompositionSection, CompositeSystem, EntryData):
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
                ],
            )
        ),
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        """
        The normalizer for the `PerovskiteComposition` class.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        """
        super().normalize(archive, logger)
        if not archive.results:
            archive.results = Results()
        if not archive.results.material:
            archive.results.material = Material()
        if not archive.results.properties:
            archive.results.properties = Properties()

        self.components: list[PerovskiteIonComponent] = (
            self.ions_a_site + self.ions_b_site + self.ions_x_site
        )

        try:
            formula = Formula(self.get_formula_str())
            formula.populate(archive.results.material, overwrite=True)
        except Exception as e:
            logger.warn('Could not analyse chemical formula.', exc_info=e)
        archive.results.material.chemical_formula_descriptive = self.long_form

        if archive.results.material.chemical_formula_iupac is not None:
            self.elemental_composition = elemental_composition_from_formula(
                Formula(archive.results.material.chemical_formula_iupac)
            )

        if self.dimensionality in ['0D', '1D', '2D', '3D']:
            archive.results.properties.dimensionality = (
                self.dimensionality
            )  # TODO Check if this actually exists in the results
            if self.dimensionality == '3D':
                archive.results.material.structural_type = 'bulk'
            elif self.dimensionality != '0D':
                archive.results.material.structural_type = self.dimensionality

        if self.band_gap is not None:
            archive.results.properties.electronic = ElectronicProperties(
                band_gap=[
                    BandGap(
                        value=self.band_gap,
                        provenance=ProvenanceTracker(label='perovskite_composition'),
                    )
                ]
            )

        topology = {}
        parent_system = self.to_topology_system(logger=logger)
        parent_system.system_relation = Relation(type='root')
        add_system(parent_system, topology)
        add_system_info(parent_system, topology)

        for ion in self.components:
            child_system = ion.to_topology_system()
            add_system(child_system, topology, parent_system)
            add_system_info(child_system, topology)

        for system in topology.values():
            archive.results.material.m_add_sub_section(Material.topology, system)


m_package.__init_metainfo__()
