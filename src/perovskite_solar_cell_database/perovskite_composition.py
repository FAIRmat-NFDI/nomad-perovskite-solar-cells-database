from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    pass

from nomad.datamodel.data import ArchiveSection, Schema, UseCaseElnCategory
from nomad.datamodel.results import Material, System
from nomad.metainfo import Quantity, SchemaPackage, Section, SubSection

from perovskite_solar_cell_database.schema_sections.ions.ion import (
    Ion,
    optimize_molecule,
)
from perovskite_solar_cell_database.schema_sections.utils import (
    add_band_gap,
    add_solar_cell,
)

m_package = SchemaPackage()


class PerovskiteComposition(Schema):
    """
    A section describing the composition of the perovskite.
    """

    single_crystal = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if the cell is based on a perovskite single crystal
                    """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    composition_short_form = Quantity(
        type=str,
        shape=[],
        description="""
    nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=[]),
        ),
    )

    composition_long_form = Quantity(
        type=str,
        shape=[],
        description="""
    nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=[]),
        ),
    )

    additives_compounds = Quantity(
        type=str,
        shape=[],
        description="""
    List of the dopants and additives that are in the perovskite
- If the perovskite is layered (e.g. 3D perovskite with a 2D caping layer), separate the layers by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- If several dopants/additives, e.g. A and B, are present in one layer, list the dopants/additives in alphabetic order and separate them with semicolonsas in (A; B)
- If no dopants/additives, state that as “Undoped”
- If the doping situation is unknown, stat that as‘Unknown’
- Include any non-solvent that does not go into the perovskite structure. This includes compounds that are found in secondary phases, or amorphous grain boundaries, or that disappears during synthesis.
o One example is Rb in MAFAPbBrI-perovskites. As far as we know, Rb does not go into the perovskite structure, even if that was believed to be the case in the beginning, but rather form secondary phases. For MAFAPbBrI-perovskites, Rb should thus not be considered as a A-site cation, but as a dopant/additive.
o One other example is chloride in MAPbI3. As far as we know, Cl does not go into the perovskite structure even if that was believed to be the case in the beginning. For MAPbI3 Cl should thus not be considered as a C-site cation, but as a dopant/additive.
Example
Cl
Undoped
5-AVAI
SnF2
Ag; Cl; rGO
Rb
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    'Undoped',
                    'Cl',
                    '5-AVAI',
                    'SnF2',
                    'Ag; Cl; rGO',
                    'Rb',
                ]
            ),
        ),
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)

        from nomad.atomutils import Formula
        from nomad.datamodel.results import Symmetry

        from .formula_normalizer import PerovskiteFormulaNormalizer

        add_solar_cell(archive)
        add_band_gap(archive, self.band_gap)

        if self.composition_short_form:
            archive.results.properties.optoelectronic.solar_cell.absorber = (
                self.composition_short_form.split(' | ')
            )

        if self.composition_long_form:
            if not archive.results.material:
                archive.results.material = Material()

            if self.dimension_3D or self.dimension_2D:
                if archive.results.material.structural_type is None:
                    archive.results.material.structural_type = 'not processed'
                elif self.dimension_3D:
                    archive.results.material.structural_type = 'bulk'
                    archive.results.material.dimensionality = '3D'
                elif self.dimension_2D and self.dimension_3D is False:
                    archive.results.material.structural_type = '2D'
                    archive.results.material.dimensionality = '2D'

            if self.composition_perovskite_ABC3_structure:
                if not archive.results.material.symmetry:
                    archive.results.material.symmetry = Symmetry()
                    if archive.results.material.symmetry.structure_name is None:
                        archive.results.material.symmetry.structure_name = 'perovskite'
                    # remove archive.results.material.material_name if == 'perovskite'
                    if archive.results.material.material_name == 'perovskite':
                        archive.results.material.material_name = None

            if archive.results.material.functional_type is None:
                archive.results.material.functional_type = [
                    'semiconductor',
                    'solar cell',
                ]

            formula_cleaner = PerovskiteFormulaNormalizer(self.composition_long_form)
            final_formula = formula_cleaner.clean_formula()
            try:
                formula = Formula(final_formula[0])
                formula.populate(archive.results.material)
                archive.results.material.chemical_formula_descriptive = (
                    formula_cleaner.pre_process_formula()
                )
            except Exception as e:
                logger.warn('could not analyse chemical formula', exc_info=e)
            archive.results.material.elements = final_formula[1]

        ions = []
        a_ions_names = []
        a_ions_coefficients = []
        if self.composition_a_ions is not None:
            a_ions_names = self.composition_a_ions.split('; ')
        if self.composition_a_ions_coefficients is not None:
            a_ions_coefficients = [
                float(c) for c in self.composition_a_ions_coefficients.split('; ')
            ]

        if len(a_ions_names) != 0 and len(a_ions_names) == len(a_ions_coefficients):
            for i in range(len(a_ions_names)):
                ion_a = Ion(
                    name=a_ions_names[i],
                    coefficients=a_ions_coefficients[i],
                    ion_type='A',
                )
                ion_a.normalize(self, archive)
                ions.append(ion_a)

        b_ions_names = []
        b_ions_coefficients = []
        if self.composition_b_ions is not None:
            b_ions_names = self.composition_b_ions.split('; ')
        if self.composition_b_ions_coefficients is not None:
            b_ions_coefficients = [
                float(c) for c in self.composition_b_ions_coefficients.split('; ')
            ]

        if len(b_ions_names) != 0 and len(b_ions_names) == len(b_ions_coefficients):
            for i in range(len(b_ions_names)):
                ion_b = Ion(
                    name=b_ions_names[i],
                    coefficients=b_ions_coefficients[i],
                    ion_type='B',
                )
                ion_b.normalize(self, archive)
                ions.append(ion_b)

        c_ions_names = []
        c_ions_coefficients = []
        if self.composition_c_ions is not None:
            c_ions_names = self.composition_c_ions.split('; ')
        if self.composition_c_ions_coefficients is not None:
            c_ions_coefficients = [
                float(c) for c in self.composition_c_ions_coefficients.split('; ')
            ]
        if len(c_ions_names) != 0 and len(c_ions_names) == len(c_ions_coefficients):
            for i in range(len(c_ions_names)):
                ion_c = Ion(
                    name=c_ions_names[i],
                    coefficients=c_ions_coefficients[i],
                    ion_type='C',
                )
                ion_c.normalize(self, archive)
                ions.append(ion_c)

        self.ions = ions

        from nomad.datamodel.results import Relation
        from nomad.normalizing.common import nomad_atoms_from_ase_atoms
        from nomad.normalizing.topology import add_system, add_system_info

        topology = {}
        # Add original system
        parent_system = System(
            label='absorber material',
            description='A system describing the chemistry and components of the absorber material.',
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

        for ion in self.ions:
            ase_atoms = optimize_molecule(ion.smile)
            atoms = nomad_atoms_from_ase_atoms(ase_atoms)
            if ion.ion_type != 'C':
                label = f'{ion.ion_type} Cation: {ion.name}'
            else:
                label = f'{ion.ion_type} Anion: {ion.name}'
            child_system = System(
                label=label,
                method='parser',
                atoms=atoms,
            )

            if len(ase_atoms) == 1:
                child_system.structural_type = 'atom'
            elif len(ase_atoms) > 1:
                child_system.structural_type = 'molecule / cluster'

            add_system(child_system, topology, parent_system)
            add_system_info(child_system, topology)

        material = archive.m_setdefault('results.material')
        for system in topology.values():
            material.m_add_sub_section(Material.topology, system)

        # topology contains an extra parent
        if len(self.ions) == len(material.topology) - 1:
            for i in range(len(self.ions)):
                material.topology[i + 1].chemical_formula_descriptive = self.ions[
                    i
                ].name
