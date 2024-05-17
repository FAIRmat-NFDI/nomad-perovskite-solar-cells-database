import os

import openpyxl
from ase import Atoms
from nomad.datamodel.metainfo.basesections import PureSubstanceSection
from nomad.metainfo import Quantity


class Ion(PureSubstanceSection):
    """
    A section describing the ions used in the solar cell.
    """

    ion_type = Quantity(
        type=str,
        shape=[],
        description='Type of the ion.',
        a_eln=dict(component='StringEditQuantity'),
    )

    common_name = Quantity(
        type=str,
        description='Common name.',
        a_eln=dict(component='StringEditQuantity'),
    )
    alternative_names = Quantity(
        type=str,
        shape=['*'],
        a_eln=dict(component='StringEditQuantity'),
    )

    common_source_compound = Quantity(
        type=str,
        shape=[],
        a_eln=dict(component='StringEditQuantity'),
    )
    source_compound_cas = Quantity(
        type=str,
        shape=[],
        a_eln=dict(component='StringEditQuantity'),
    )
    source_compound_formula = Quantity(
        type=str,
        shape=[],
        a_eln=dict(component='StringEditQuantity'),
    )

    coefficients = Quantity(
        type=float,
        shape=[],
        description='Coefficients for the ion.',
        a_eln=dict(component='NumberEditQuantity'),
    )

    def normalize(self, archive, logger: None) -> None:
        super().normalize(archive, logger)

        ions = read_ions_from_xlsx(self.ion_type)
        ion_match = find_ion_by_name(self.name, ions)
        if ion_match is not None:
            self.name = ion_match.name
            self.iupac_name = ion_match.iupac_name
            self.molecular_formula = ion_match.molecular_formula
            self.smile = ion_match.smile
            self.cas_number = ion_match.cas_number
            self.alternative_names = ion_match.alternative_names
            self.common_source_compound = ion_match.common_source_compound
            self.source_compound_cas = ion_match.source_compound_cas
            self.source_compound_formula = ion_match.source_compound_formula


def read_ions_from_xlsx(ion_type):
    ions_candidates = []
    file_name = f'{ion_type}-ion_data.xlsx'
    current_dir = os.path.dirname(os.path.realpath(__file__))

    workbook = openpyxl.load_workbook(os.path.join(current_dir, file_name))
    worksheet = workbook.active

    for row in worksheet.iter_rows(min_row=2, values_only=True):
        (
            _,
            abbreviation,
            alternative_abbreviations,
            molecular_formula,
            smile,
            common_name,
            iupac_name,
            cas,
            parent_iupac,
            parent_smile,
            parent_cas,
            common_source_compound,
            source_compound_cas,
            _,
            _,
        ) = row[:15]

        # todo: parent_* are not used.
        ion_candidate = Ion()
        ion_candidate.name = abbreviation
        if alternative_abbreviations is not None:
            ion_candidate.alternative_names = [
                el.strip() for el in alternative_abbreviations.split(',')
            ]
        else:
            ion_candidate.alternative_names = []
        ion_candidate.molecular_formula = molecular_formula
        ion_candidate.smile = smile
        ion_candidate.common_name = common_name
        ion_candidate.iupac_name = iupac_name
        ion_candidate.cas_number = cas
        ion_candidate.common_source_compound = common_source_compound
        ion_candidate.source_compound_cas = source_compound_cas

        ions_candidates.append(ion_candidate)

    return ions_candidates


def find_ion_by_name(ion_name, ions_candidates):
    if ion_name[0] == '(' and ion_name[-1] == ')':
        ion_name_clean = ion_name[1:-1]
    else:
        ion_name_clean = ion_name
    for ion in ions_candidates:
        if ion_name_clean == ion.name or ion_name_clean in ion.alternative_names:
            return ion
    return None


def get_all_ions_names(ions):
    ion_names = []
    for ion in ions:
        if ion.name is not None:
            ion_names.append(ion.name)
        if ion.alternative_names is not None:
            ion_names.extend(ion.alternative_names)

    return ion_names


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
