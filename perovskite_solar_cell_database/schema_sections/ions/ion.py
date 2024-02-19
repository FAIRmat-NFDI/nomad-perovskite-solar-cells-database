from nomad.datamodel.metainfo.basesections import PureSubstanceSection
from nomad.metainfo import Quantity, MEnum
import openpyxl
import os
from perovskite_solar_cell_database.schema_sections.ions.ion_vars import ion_a, ion_b, ion_c, ion_a_coefficients, ion_b_coefficients, ion_c_coefficients


class Ion(PureSubstanceSection):
    """
    A section describing the ions used in the solar cell.
    """
    name = Quantity(
        type=str,
        shape=[],
        a_eln=dict(
            component='EnumEditQuantity',
            # props=dict(
            #     suggestions=ion_a,
            # )
        ),
        description='Name of the ion.',
    )

    iupac_name = Quantity(
        type=str,
        description='IUPAC name.',
    )
    molecular_formula = Quantity(
        type=str,
        description='Molecular formula.',
    )
    smile = Quantity(
        type=str,
        description='Smile.',
    )
    common_name = Quantity(
        type=str,
        description='Common name.',
    )
    cas_number = Quantity(
        type=str,
        description='CAS number.',
    )
    alternative_names = Quantity(
        type=str,
        shape=['*'],
        # repeats=True,
      )

    common_source_compound = Quantity(
        type=str,
        shape=[],
    )
    source_compound_cas = Quantity(
        type=str,
        shape=[],
    )
    source_compound_formula = Quantity(
        type=str,
        shape=[],
    )

    coefficients = Quantity(
        type=float,
        shape=[],
        description='Coefficients for the ion.',
        a_eln=dict(
            component='NumberEditQuantity')
    )

    def normalize(self, archive, logger: None) -> None:
        super().normalize(archive, logger)
        ions = read_ions_from_xlsx(self.ion_type)
        ion = find_ion_by_name(self.name, ions)
        if ion is not None:
            self.name = ion.name
            self.iupac_name = ion.iupac_name
            self.molecular_formula = ion.molecular_formula
            self.smile = ion.smile
            self.cas_number = ion.cas_number
        if ion.alternative_names is not None:
            self.alternative_names = ion.alternative_names
            self.common_source_compound = ion.common_source_compound
            self.source_compound_cas = ion.source_compound_cas
            self.source_compound_formula = ion.source_compound_formula


class IonA(Ion):
    ion_type = 'A'

    name = Quantity(
        type=str,
        shape=[],
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=ion_a,
            )
        ),
        description="""
        List of the A-site ions in the perovskite structure
        - We have experimented with letting users write the perovskite structure and from that extract ions and coefficients. Due to the multitude of formatting variations, that has not worked out very well, wherefor we now define the perovskite ion by ion.
        - List all the A-site ions in alphabetic order and separate them by semicolons
        - For ions which labels are three characters or longer, enclose them in parenthesis. That improves readability and simplifies downstream data treatment.
        - In case of a layered perovskite structure, separate layers by a space, a vertical bar, and a space, i.e. (‘ | ‘)
        - Only include ions that go into the perovskite structure. Ions that only are found in secondary phases, or amorphous grain boundaries, or that disappears during synthesis, should instead be added as dopants/additives in the field dedicated to dopants and additives.
        o On example is Rb in MAFAPbBrI-perovskites. As far as we know, Rb does not go into the perovskite structure, even if that was believed to be the case in the beginning, but rather form secondary phases. For MAFAPbBrI-perovskites, Rb should thus not be considered as a A-site cation, but as a dopant/additive.
        Example:
        MA
        FA; MA
        Cs; FA; MA
        (5-AVA); MA
        Cs; FA; MA | (PEA)
        """,
    )

    coefficients = Quantity(
        type=str,
        shape=[],
        description="""
            A list of the perovskite coefficients for the A-site ions
        - The list of coefficients must line up with the list of the A-site ions
        - If a coefficient is unknown, state that with an ‘x’
        - If there are uncertainties in the coefficient, only state the best estimate, e.g. write 0.4 and not 0.3-0.5.
        - A common notation is ‘1-x’. Write that as x
        - If the coefficients are not known precisely, a good guess is worth more than to state that we have absolutely no idea.
        Examples:
        1
        0.83; 0.17
        0.05; 0.79; 0.16
        1.5; 0.5
        """,
        a_eln=dict(component='EnumEditQuantity',
                   props=dict(suggestions=ion_a_coefficients))
    )



class IonB(Ion):
    ion_type = 'B'
    name = Quantity(
        type=str,
        shape=[],
        description="""
        List of the B-site ions in the perovskite structure
        - We have experimented with letting users write the perovskite structure and from that extract ions and coefficients. Due to the multitude of formatting variations, that has not worked out very well, wherefor we now define the perovskite ion by ion.
        - List all the B-site ions in alphabetic order and separate them by semicolons
        - In case of a layered perovskite structure, separate layers by a space, a vertical bar, and a space, i.e. (‘ | ‘)
        - Only include ions that go into the perovskite structure. Ions that only are found in secondary phases, or amorphous grain boundaries, or that disappears during synthesis, should instead be added as dopants/additives in the field dedicated to dopants and additives.
        Example:
        Pb
        Sn
        Pb; Sn
        Bi
        Pb | Pb
        """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=ion_b,
            )
        ),
    )
    coefficients = Quantity(
        type=str,
        shape=[],
        description="""
            A list of the perovskite coefficients for the B-site ions
        - The list of coefficients must line up with the list of the B-site ions
        - If a coefficient is unknown, mark that with an ‘x’
        - If there are uncertainties in the coefficient, only state the best estimate, e.g. write 0.4 and not 0.3-0.5.
        - A common notation is ‘1-x’. Write that as x
        - If the coefficients are not known precisely, a good guess is worth more than to state that we have absolutely no idea.
        Examples:
        1
        0.83; 0.17
        x; x
        0.5; 0.5 | 1
        """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(
                suggestions=ion_b_coefficients
            ),
        )
    )


class IonC(Ion):
    ion_type = 'C'
    name = Quantity(
        type=str,
        shape=[],
        description="""
        List of the C-site ions in the perovskite structure
        - We have experimented with letting users write the perovskite structure and from that extract ions and coefficients. Due to the multitude of formatting variations, that has not worked out very well, wherefor we now define the perovskite ion by ion.
        - List all the A-site ions in alphabetic order and separate them by semicolons
        - For ions which labels are three characters or longer, enclose them in parenthesis. That improves readability and simplifies downstream data treatment.
        - In case of a layered perovskite structure, separate layers by a space, a vertical bar, and a space, i.e. (‘ | ‘)
        - Only include ions that go into the perovskite structure. Ions that only are found in secondary phases, or amorphous grain boundaries, or that disappears during synthesis, should instead be added as dopants/additives in the field dedicated to dopants and additives.
        o One example is chloride in MAPbI3. As far as we know, Cl does not go into the perovskite structure even if that was believed to be the case in the beginning. For MAPbI3 Cl should thus not be considered as a C-site cation, but as a dopant/additive.
        Example:
        I
        Br; I
        Br
        Br; I| I
        """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=ion_c,
            )
        ),
    )
    coefficients = Quantity(
        type=str,
        shape=[],
        description="""
        A list of the perovskite coefficients for the C-site ions
        - The list of coefficients must line up with the list of the C-site ions
        - If a coefficient is unknown, mark that with an ‘x’
        - If there are uncertainties in the coefficient, only state the best estimate, e.g. write 0.4 and not 0.3-0.5.
        - A common notation is ‘1-x’. Write that as x
        - If the coefficients are not known precisely, a good guess is worth more than to state that we have absolutely no idea.
        Examples:
        3
        0.51; 2.49
        0.51; 2.49 | x
        """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=ion_c_coefficients,
            )
        ),
    )


def read_ions_from_xlsx(ion_type):
    ions = []
    file_name = f'{ion_type}-ion_data.xlsx'
    current_dir = os.path.dirname(os.path.realpath(__file__))

    workbook = openpyxl.load_workbook(os.path.join(current_dir, file_name))
    worksheet = workbook.active

    for row in worksheet.iter_rows(min_row=2, values_only=True):

        (_, abbreviation, alternative_abbreviations, molecular_formula,
         smile, common_name, iupac_name, cas, parent_iupac, parent_smile,
         parent_cas, common_source_compound, source_compound_cas,
         _, _) = row[:15]

        # todo: parent_* are not used.
        ion = Ion()
        ion.name = abbreviation
        if alternative_abbreviations is not None:
            ion.alternative_names = [el.strip() for el in alternative_abbreviations.split(',')]
        else:
            ion.alternative_names = []
        ion.molecular_formula = molecular_formula
        ion.smile = smile
        ion.common_name = common_name
        ion.iupac_name = iupac_name
        ion.cas_number = cas
        ion.common_source_compound = common_source_compound
        ion.source_compound_cas = source_compound_cas

        ions.append(ion)

    return ions


def find_ion_by_name(ion_name, ions):
    for ion in ions:
        if (ion.name == ion_name or ion_name in ion.alternative_names):
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
# #
# ic = get_all_ions_names(read_ions_from_xlsx('A'))
# print(len(ic))
# print(len(set(ion_a)))
# print(len(ion_a))
# print(set(ion_a))
