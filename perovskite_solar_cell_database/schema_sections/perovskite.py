from perovskite_solar_cell_database.schema_sections.utils import add_solar_cell, add_band_gap
from perovskite_solar_cell_database.schema_sections.ions.ion import Ion, optimize_molecule
from nomad.metainfo import Quantity, SubSection
from nomad.datamodel.data import ArchiveSection
from nomad.datamodel.results import Material
from nomad.datamodel.results import System
from ase.build import molecule


class Perovskite(ArchiveSection):
    """
    This section contains information about the properties of the absorber layer. It describes
    the `chemical formula`, the `dimensionality`, the `bandgap`,
    or the `list of dopants and additives` that are in the perovskite layer.
    """

    single_crystal = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if the cell is based on a perovskite single crystal
                    """,
        a_eln=dict(
            component='BoolEditQuantity'))

    dimension_0D = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if the cell is based on a perovskite quantum dots. Perovskite nanoparticle architectures can also be counted here unless they more have the characteristics of a standard polycrystalline cell
                    """,
        a_eln=dict(
            component='BoolEditQuantity'))

    dimension_2D = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if the cell is based on 2D perovskites, i.e. a layered perovskite with a large A-cation
                    """,
        a_eln=dict(
            component='BoolEditQuantity'))

    dimension_2D3D_mixture = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if the cell is based on a mixture of 2D and 3D perovskites. This is sometimes referred to as reduced dimensional perovskites (but not as reduced as to be a pure 2D perovskite)
                    """,
        a_eln=dict(
            component='BoolEditQuantity'))

    dimension_3D = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE for standard three-dimensional perovskites with ABC3 structures. TRUE also for the case where the bulk of the perovskite is 3D but where there exist a thin 2D-caping layer
                    """,
        a_eln=dict(
            component='BoolEditQuantity'))

    dimension_3D_with_2D_capping_layer = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if the bulk of the perovskite layer is 3D but there is a top layer with lower dimensionality.
                    """,
        a_eln=dict(
            component='BoolEditQuantity'))

    dimension_list_of_layers = Quantity(
        type=str,
        shape=[],
        description="""
    A list of the perovskite dimensionalities
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- In most cases, there will be only one layer
- For a perovskite that is a mixture of a 2D and a 3D phase, mark this is as2.5
Example
3
3 | 2
0
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(
                suggestions=['', '3.0 | 1.0', '3.0 | 0.0', '2.5', '0.0 | 0.0', '2.0 | 3.0 | 2.0',
                             '3.0 | 0.0 | 0.0 | 0.0', '3.0', '2.0 | 3.0', '3.0 | 3.0', '3.0 | 2.0', '3.0 | 0.0 | 0.0',
                             '1.5', '2.0', '3.0 | 2.0 | 0.0', '1.0', '0.0', '3.0 | 0.0 | 0.0 | 0.0 | 0.0',
                             '1.0 | 3.0'])))

    composition_perovskite_ABC3_structure = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if the photo-absorber has a perovskite structure
- The typical perovskite has an ABC3 structure and that is clearly a TRUE
- This category is inclusive in the sense that also 2D perovskite analogues should be labelled as TRUE
                    """,
        a_eln=dict(
            component='BoolEditQuantity'))

    composition_perovskite_inspired_structure = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if the photo absorber does not have a perovskite structure. In the literature we sometimes see cells based on non-perovskite photo absorbers, but which claims to be “perovskite inspired” regardless if the crystal structure has any resemblance to the perovskite ABC3 structure or not. This category is for enabling those cells to easily be identified and filtered.
                    """,
        a_eln=dict(
            component='BoolEditQuantity'))

    composition_a_ions = Quantity(
        type=str,
        shape=[],
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
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=sorted(
                ['', '(TFEA); Cs; FA; MA', '(PEA) | Cs; FA; MA | (PEA)', 'HA; MA', '(CHMA); MA', 'FA; HA',
                 'Cs | BA; Cs', 'MA | Cs | Cs | Cs | Cs', '(ALA); BA; MA', '(TEA); MA', '(PGA); BA; MA',
                 'BA; Cs; FA; MA', 'Cs; FA; MA | (PEA)', 'EA; MA; PEA', 'Cs; FA | Cs', '(BYA); MA', 'Cs; FA; K; MA',
                 'MA | Cs | Cs', '(PEI); MA', '(PEA); MA | MA', 'MA; PA', '(NMA); MA', '(BZA); (HAD); MA', 'Bi',
                 '(PDA); MA', 'Cu', '(BzDA); Cs; FA; MA', '(TBA); MA', 'Cs; (DMA); MA', '(CPEA); MA', 'FA; MA | (A43)',
                 '(Anyl)', 'BA; Cs; MA', '(HdA)', 'HA', 'FA; MA | DA', '(TMA)', '(CIEA); MA', 'MA | FA',
                 '(HEA); Cs; FA', '(BZA)', '(BdA)', 'BA; FA', '(OdA)', 'K; BA', 'Rb', '(5-AVA); MA', '(ALA); MA',
                 'Cs; FA; GU', 'DI; FA', '(iPA)', 'FA; MA | (MIC3)', '(5-AVAI); Cs; FA', 'FA; MA | (MIC2)',
                 'Cs; FA; PDA', 'Cs; FA | Cs; FA', 'Cs; MA', '(mF1PEA); MA', 'Cs; FA; MA | PA', '(PDMA)',
                 'Cs; FA; MA | (FPEA)', 'EA; FA', 'MA | (BEA)', 'FA | (ODA)', '(ImEA)', 'MA | BA', 'BA; MA',
                 'Cs; FA; MA | (mFPEA)', '(C6H4NH2)', 'MA | Cs | Cs | Cs', '(IEA); MA', 'FA; K; MA', '(PMA)',
                 'Cs; FA; MA | (pFPEA)', 'IM', 'Cs; HA', 'FA; PN', 'Cs; FA; GU; MA', '(ThMA); MA', 'FA',
                 '(DPA); MA; PA; PA', 'FA; MA | (C8H17NH3)', 'AN; FA; MA', '(DMA); MA', 'Cs; FA; MA | (oFPEA)',
                 '(3AMP); FA; MA', 'Bi; La', 'Cs; MA; FA | BA', 'AN; Cs; MA', '(BZA); MA', '(Ace); MA', 'MA | (PPEA)',
                 'FA; MA | (C4H9NH3)', '((CH3)3S)', 'MA | MA', '(4ApyH)', '(Br-PEA); MA', 'FA; GU', 'IA; MA', '(DMA)',
                 'BA; GA; MA', 'FA | Cs', '(PBA); MA', 'Aa; MA', 'Ag', '(PMA); MA', '(DAP)', '(MTEA); MA', 'MA | Cs',
                 'AN; MA', 'BU; FA', '(CHMA); Cs; MA', 'Cs | Cs', 'Cs', '(PDMA); MA', 'FA; MA | PEA', 'MA | (MIC1)',
                 '(PEA); FA; MA', '(3AMPY); MA', 'Cs; EA; FA', '(PTA); MA', '(PEA) | MA', 'MA | CA', '(PEA); Cs',
                 '(N-EtPy)', 'MA | (EU-pyP)', 'GU; MA', '(PEA); BA; FA', 'Cs; FA; MA | BA',
                 '(PEA); (F5PEA); Cs; FA; MA', 'Cs; FA; nan', '(n-C3H7NH3)', '(PGA); MA', 'FA; MA | (PEA)',
                 '(PEA); BA; MA', '(PEA); FA', '(F-PEA); MA', 'Ba; K', 'Cs; Rb', 'Cs; FA; MA | Cs', 'Ca; MA', 'BA',
                 'Cs; Li', '(iso-BA); MA', '(PyrEA)', 'Cs; FA; MA | (CH3)3S', 'Cs; FA; Rb', 'BA; Cs', '(BEA); MA',
                 'Cs; FA; MA | (EPA)', '(NEA); BA; MA', 'FA; MA | (HTAB); FA; MA', 'FA | EDA', '(1.3-Pr(NH3)2)',
                 'FA; MA | BA; FA', '(BEA); Cs; FA; MA', '(PEI)', 'MA | (BI)', 'MA | (PEA)', 'MA | (C4H9N2H6)', '(NH4)',
                 'K', '(ThFA); MA', 'Ag; Cs; Rb', 'EA', 'EDA; FA', 'FA; Rb', 'Cs; FA; MA | (FEA)', '(TBA); Cs; FA; MA',
                 'Cs; Ag', 'Cs | MA', '(NH4); FA; MA', '(Anyl); MA', '(PEA); MA', 'Cs; Na', 'IM; MA', '(4AMP); MA',
                 '(F3EA); BA; MA', 'BA; FA; MA; PMA', '(EDA); FA; MA', 'MA | (PPA)', 'HDA', 'Sr', '(pF1PEA); MA',
                 'MA | BA; MA', 'BE; FA', '(4AMPY); MA', 'FA; MA | (C6H13NH3)', 'Cs; FA | (PA)', 'Cs; FA | (PEA)',
                 'GA; MA', 'FA; MA | TA', '(oF1PEA); MA', 'EA; MA; NEA', '(BDA); MA', 'BA; Cs; FA', 'Cs; FA; MA',
                 '(H-PEA); MA', 'Cs; K', '(PEA); Cs; FA; MA', 'Cs; FA | (PMA)', 'GU', '(PBA); BA; MA', 'FA | (PEA)',
                 '(3AMP); MA', '(PEA); (F5PEA)', 'BA; FA; MA', '(ThMA); FA', 'BDA; Cs', '(BIM); MA', '(CH3ND3)',
                 '(GABA); MA', 'FA; MA | (FEA)', 'La', 'FA; OA', 'FA; MA | (NH4); FA', '(APMim)', '(F5PEA); Cs; FA; MA',
                 'Cs; FA; GA', 'FA; MA | (MIC1)', 'Cs; FA; MA | (A43)', 'Ag; Cs', 'Cs | FA', '(PDMA); FA', 'FA; MA',
                 'DA; FA', '(PEA); Cs; MA', 'FA; MA | OA', 'Cs; FA; MA | NMABr', 'MA', 'FA; TN', 'Cs; FA; MA | HA',
                 '(f-PEA)', 'Cs; FA; MA; Rb', 'Bn', '(Ada); FA', 'Ca; FA; MA', '(AVA) | MA | (BI)', '(PEA); Cs; FA',
                 'Cs; FA; MA | (PEI)', '(6-ACA); MA', '(DAT); MA', '(5-AVA); FA', '(PEA) | MA | (PEA)', '(BDA)',
                 '(PyEA); MA', '(F5PEA)', '(THM); MA', 'MA | (MIC3)', '(PDA); Cs; FA', '(5-AVA); Cs; MA', 'FA; GU; MA',
                 'FA; MA | BA', 'Cs; FA', '(Cl-PEA); MA', '(AVA); MA', '(PMA); FA', 'PA', 'EA; MA', 'FA; PR',
                 '(AVA) | MA', '(4FPEA); MA', '(PEA)', 'MA | (MIC2)', 'BA; GU; MA']))))

    composition_a_ions_coefficients = Quantity(
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
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['1', '0.2', '0.83; 0.17'])))

    composition_b_ions = Quantity(
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
            component='EnumEditQuantity', props=dict(
                suggestions=['', 'Pb; Sn | Pb; Sn', 'Ni; Pb', 'Al', 'Pb; Sm', 'Cu; Sb', 'Ag; Bi', 'Pb | Pb | Pb',
                             'Pb | Pb | Pb | Pb | Pb', 'Bi; Te', 'Mn; Pb', 'Pb; Zn', 'Y', 'Au', 'Pb; Sr', 'Fe', 'Sn',
                             'Cu', 'Bi', 'Hg; Pb', 'Ca; Pb', 'Sn | Sn', 'Cu; Pb; Sn', 'Ge; Pb', 'Pb | Pb', 'Ni',
                             'Bi; Pb', 'Cu; Pb', 'Sb', 'Mg; Pb', 'Hg', 'Co; Pb', 'Ge; Sn', 'Pb; Tb', 'Pb; Sn', 'Pb',
                             'Pb; Sb', 'Sb; Sn', 'Pb | Ba; Pb', 'Mn', 'Sn | Pb', 'Fe; Pb', 'Ti', 'In; Pb', 'La; Pb',
                             'Nb; Ni', 'Pb | Pb | Pb | Pb', 'Ge; Sb', 'Bi; Fe; Cr', 'Bi; Sb', 'Ge', 'Ba; Pb',
                             'Eu; Pb'])))

    composition_b_ions_coefficients = Quantity(
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
                suggestions=['', '7.8', '0.008; 0.992', '0.625; 0.375', '9', '0.6; 0.6', '0.1; 0.9', '0.875; 0.125',
                             '1', '0.05; 0.85; 0.1', '2', '0.85', '0.6', '0.85; 0.15', '0.93', '1.2; 0.8', '0.93; 0.07',
                             '41', '0.9999; 0.0001', '2.4; 1.8', '0.98', '0.5; 0.5', '0.45 | 9', '0.003; 0.997',
                             '0.97; 0.03', '0.07; 0.93', '11', '1 | 1; 1', '0.95; 0.1', '0.995', '2.6', '1 | 3',
                             '0.025; 0.975', '0.2; 0.8', '0.016; 0.984', '0.748; 0.252', '0; 0.19', '4.0',
                             '1 | 1 | 1 | 1', '0.0118; 0.9882', '4.8; 3.6', '0.99', '0.6; 0.4', '0.02; 0.98',
                             '0.031; 0.969', '0.4; 0.6', '0.875', '0.94; 0.06', '0.99; 0.01', '0.05',
                             '0.99999; 0.00001', '1.4; 0.6', '0.09; 0.91', '0.664; 0.336', '0.54', '100',
                             '0.999; 0.001', '0.075; 0.925', '7', '0.25; 0.75', '20', '0.96; 0.04', '8', '0.15; 0.85',
                             '0.5; 0.500', '0.05; 0.95', '0.063; 0.937', '0.57', '1 | 1 | 1', '1 | 2', '0.20; 0.80',
                             '1.0', '6.1', '0.05; 0.9; 0.05', '11.2', '1 | 1', '0.01; 0.99', '4', '0.05; 0.8; 0.15',
                             '10', '0.997; 0.003', '29', '3', '0.916; 0.084', '0.014; 0.986', '1.8; 0.2', '3.14',
                             '0.8; 0.2', '0.95; 0.05', '2.7', '6', '0.10; 0.90', '40', '0.50; 0.50', '1; 0.6',
                             '0.7; 0.3', '0.08; 0.92', '0.25', '0.4; 0.6 | 0.4; 0.6', '23', '0.84; 0.84',
                             '0.005; 0.995', '0.98; 0.02', '3; 2.4', '0.832; 0.168', '3; 1', '1.8; 1.2', '1; 3',
                             '0.995; 0.005', '61', '1.9; 0.1', '0.88; 0.12', '0.95', 'x', '2.2', '0.7; 0.255',
                             '2; 1; 1', '0.06; 0.94', '0.38; 0.62', '0.97', '0.03; 0.97', '5', '0.125; 0.875', '1; 1',
                             '0.9; 0.1', '0.66; 0.33', '80', '0.9', '0.375; 0.625', '0.58; 0.42', '12.9', '0.997',
                             '1.1', '60', '0.3; 0.7', '30', '0.04; 0.96', '0.92; 0.08', '1.6; 0.4', '9.5', '0.75; 0.25',
                             '0.45', '4 | 1', '0.0094; 0.9906', '0.37; 0.6255', '0.93; 0.03', '0.65; 0.35',
                             '1 | 1 | 1 | 1 | 1', '4.4'])))

    composition_c_ions = Quantity(
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
            component='EnumEditQuantity', props=dict(
                suggestions=['Br; I | Br; I', '', '(BF4); I', 'O', 'I | Br; I | I', 'S', 'Br | Br; I', 'Cl', 'Br',
                             'I | Br', 'I | I; Br', 'Br | I', 'Br; I | I', 'Br; F; I', 'Br; I', 'I | I | Br; I | Br; I',
                             '(PF6); PF6', '(SCN); I', 'I | I', 'F; I', 'Cl; I', 'I', 'I; (SCN)', 'I | I | I',
                             'Cl; I | Cl', 'Br; Cl', 'I; SCN', 'Br | Br', 'I | I | Br; I',
                             'I | I | Br; I | Br; I | Br; I', 'I | I; (PF6)', 'Br; Cl; I', 'Br | Br; Cl',
                             'I | Br; I'])))

    composition_c_ions_coefficients = Quantity(
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
            component='EnumEditQuantity', props=dict(suggestions=[''])))

    ions = SubSection(
        section_def=Ion,
        repeats=True,
    )

    composition_none_stoichiometry_components_in_excess = Quantity(
        type=str,
        shape=[],
        description="""
    Components that are in excess in the perovskite synthesis. E.g. to form stoichiometric MAPbI3, PbI2 and MAI are mixed in the proportions 1:1. If one of them are in excess compared to the other, then that component is considered to be in excess. This information can be inferred from data entered on the concentration for all reaction solutions but this gives a convenient shorthand filtering option.
- If more than one component is in excess, order them in alphabetic order and separate them by semicolons.
- It there are no components that are in excess, write Stoichiometric
Examples:
PbI2
MAI
Stoichiometric
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(
                suggestions=['', 'SnI2', 'FA', 'Cl', 'SnF2; Sn', 'BiBr3', 'SnCl2', 'PbI2; SnI2', 'FAI', 'I2', 'Sn',
                             'MAI; PEAI; DMF', 'CH3ND3I', 'Stoichiometric | Stoichiometric', 'PbAc2', 'MAI; FAI',
                             'PbBr2; PbI2', 'MAI; PEAI', 'RbI', 'MA', 'FAI; MABr', 'MABr; PbI2', 'NH4Cl', 'HCl',
                             '5-AVAI', 'I', 'Pb', 'Stoichiometric', 'PbI2 | nan', 'SrI2', 'CsI', 'BiI3', 'MAI', 'AgI',
                             'CsBr', 'MABr', 'PbCl2', 'CsI; MACl', 'MACl', 'SbI3', 'PbI2; PbBr2',
                             'Stoichiometric | nan', 'PbI', 'SnBr2', 'PbBr2', 'PbI2'])))

    composition_short_form = Quantity(
        type=str,
        shape=[],
        description="""
    nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(
                suggestions=['FAMAPbBrI | (MIC3)PbI', 'CsBiPbI', 'BAFAMAPbI', 'FAPbI | (ODA)PbI', 'CsFAPbI | CsPbI',
                             '(PMA)FAPbI', 'CsRbSnI', 'MAPbI | (BEA)PbI', '(PEA)FAMAPbI', 'BAPbI', 'CsPbI | CsPbI',
                             'AgCsBiI', 'MAPbI | MABaPbI', 'MAPbI | (MIC1)PbI', 'CsPbBr | CsPbI', '(PEA)CsFAPbI',
                             'EAMAPEAPbI', 'nanBiI', 'GUPb(SCN)I', 'MAMnPbI', 'MAPbISCN', '(5-AVA)MAPbI', 'IMPbI',
                             '(mF1PEA)MAPbI', 'MAPb(SCN)I', 'FAGeSbCl', '(BEA)CsFAMAPbBrI', 'nanPbI', 'CsEAFAPbBrI',
                             'CsPbBrI | FAPbBrI', 'BAMASnI', 'CsCuPbBr', 'CsPbBr | MAPbI', '(1.3-Pr(NH3)2)PbI',
                             'FAMAPbBrI | (FEA)PbI', 'MAPbI | (PPEA)PbI', 'FAPbSnI', 'BACsFAMAPbI', 'CsMgPbBr',
                             'CsHAPbI', '(F-PEA)MAPbI', '(C6H4NH2)CuClI', 'CsPbBr | FAPbBr', '(DAT)MAPbI',
                             '(EDA)FAMAPbI', '(NH4)SbBrI', 'CsPbBrI | BACsPbBrI', 'MAMgPbI', 'CsNaBiI', '(IEA)MAPbI',
                             '(PGA)BAMAPbI', 'BACsFAPbSnI', 'FASnI', 'MASnBr', 'MAPbI | FAPbBrI', 'HAPbI',
                             'CsPbBrI | CsPbI', 'EAMANEAPbI', 'CsPbSrBr', 'CsFAMAPbI', '(PEA)CsFAMAPbBrI',
                             '(APMim)Pb(PF6)PF6', '(5-AVA)CsMAPbI', '(oF1PEA)MAPbI', 'SrTiO', 'EAMAPbI', '(PMA)MAPbI',
                             'FATNSnI', 'CuBiI', 'nanBiO', '(n-C3H7NH3)PbCl', '(PBA)BAMAPbI', 'CsFAPbSnI', '(NH4)SbI',
                             'CsFAPbBrI', 'HDABiI', 'CsRbPbBr', '(NH4)SbBr', 'AgCsBiBr', 'MAPbBr', '(PDA)CsFAPbI',
                             'CsFAPbBr', 'CsBaPbI', 'BACsPbI', 'MAPbSrI', 'HAMASnI', '(F5PEA)(PEA)CsFAMAPbBrI',
                             '(4AMPY)MAPbI', 'MAPbI | (MIC2)PbI', '(OdA)PbI', 'MAPbI | (C4H9N2H6)PbI', 'MAEuPbI',
                             'CsPbSnI', 'FAPbI | EDAPbI', 'RbPbI', 'BDACsPbBrI', '(Anyl)MAPbI', 'EAFASnI', '(4ApyH)SbI',
                             '(PEA)BAMAPbI', '(TMA)SnI', 'CsPbZnBr', 'AgBiI', 'CsPbSnBrI', '(ImEA)PbI', 'FAPbBrI',
                             'MAPbI | MAPbI', 'FAMAPbI | (A43)PbI', 'MANiPbI', 'BAKBiTeO', 'MASnI', '(BDA)PbI',
                             'FAMAPbBrI | OAPbI', 'MAHgI', '(F5PEA)CsFAMAPbBrI', '(4FPEA)MAPbI', 'MAPbI | (EU-pyP)PbI',
                             'CsMAPbSnBrI', 'CsFAPbBrI | (PEA)PbBrI', '(PEA)PbI | CsFAMAPbBrI | (PEA)PbI',
                             '(iso-BA)MAPbI', 'MAPbI | MAPbBrI', 'CsFAPbI | CsFAPbI(PF6)', 'MAPbBrCl',
                             'MAPbI | BAMAPbI', 'FAMAPbBrI | (C4H9NH3)PbI', 'EDAFASnI', 'CsNiPbBr', 'MAInPbI',
                             '((CH3)3S)SnClI', 'CsBaPbBrI', '(C6H4NH2)CuBrI', 'FAPbI | CsPbI', 'MACuPbBrI',
                             '(Br-PEA)MAPbBrI', 'CsFAMAPbBr', 'FAPbCl', 'MABaPbI', '(AVA)PbI | MAPbI | (BI)PbI',
                             'BAGAMAPbI', '(PEI)MAPbI', '(PEA)FAMASnI', 'MAPbI | MAPbBr', '(PDMA)MAPbI', 'FAMASnI',
                             'CsPb(SCN)I', 'CsFAMAPbBrI | (A43)PbI', 'CsFAPbBrI | (PA)PbBrI', 'EAMAPbBr', 'FASnBrI',
                             '(PEA)MAPbI', '(HEA)CsFAPbBrI', 'MACuPbSnBrI', 'IAMAPbI', '(ThMA)MAPbI',
                             'CsPbBr | FAPbBrCl', 'MAAuBr', 'BACsFAPbBrI', 'CsFAMAPbBrI | HAPbI', 'CsFARbPbI',
                             'CaMAPbBrI', 'CsMAPbI', 'FASnI | (PEA)SnI', 'FAPbBrCl', 'MACuBrCl', 'FAHAPbI',
                             '(PEA)MASnI', 'MACoPbI', '(3AMP)MAPbI', '(PBA)MAPbI', 'MAPbSnBr', 'CsFAMAPbBrI | CsPbI',
                             'FAMAPbI', 'FAMAPbSnI', '(F5PEA)(PEA)PbI', 'MAPbI | (BI)PbI', 'MAPAPbI', 'AgBi(SCN)I',
                             'FAPbBr', '(6-ACA)MAPbI', 'CsMAPbSnClI', '(PEI)PbI', 'FAMAPbSnBrI', 'MANiClI', 'MAGeBrI',
                             'MAPbClI', 'CsTiBr', 'CsSnI', 'MAPbBrI', '(CPEA)MAPbI', 'FAMAGeSnI', 'MAPbI | BAPbI',
                             'BiLaFeO', '(PEA)MAPbClI', 'BiFeO', 'FAMAPbBrI', '(PDMA)PbI', 'CsGeSnI', 'FAMAPbBr',
                             'FAKMAPbBrI', 'MASbSnI', 'FAMAGePbBrI', '(5-AVA)FASnI', 'CsFAMAPbI | (FEA)PbI',
                             'CsFAMAPbBrI | (pFPEA)PbI', 'FAMAPbBrI | DAPbI', '(4ApyH)BiSbI', '(DMA)MAPbI',
                             'CsFAMAPbBrI | (EPA)PbI', 'MASbI', 'IMMAPbI', '(BDA)MAPbI', '(F5PEA)PbI', 'BAFAPbI',
                             'MAGeI', 'LaYS', 'MAPbI | (PPA)PbI', 'CsPbBr | FAPbBrI', 'FAMAPbBrI | PEAPbI', 'nannannan',
                             'CsBiI', '(PEA)PbI', 'MACaPbI', 'nanSnI', 'CsFAMAPbBrI | CsPbBrI', 'FAMAPbBrI | BAFAPbI',
                             '(TEA)MAPbI', 'MAPbZnI', 'CsSbI', 'CsFAGAPbI', 'FAMAPbI | (NH4)FAPbI', 'BACsMAPbI',
                             'CsFASnI', 'BnSnI', 'HAMAPbI', 'FAPbI | (PEA)PbI', 'FAPbBrClI', 'CsPbBr | CsPbBrI',
                             '(NMA)MAPbI', 'CsGePbBrI', 'CsPbBrI', 'FAMAPbSnI | (PEA)PbSnI', '(3AMPY)MAPbI',
                             '(PGA)MAPbI', 'CsPbBr', 'BAFASnI', 'EAPbI', 'CsFAPDAPbI', '(N-EtPy)SbBr', '(PDMA)FAPbI',
                             'BAFAPbClI', 'MASnI | MAPbI', 'CsFAGAPbBrI', 'CsCaPbBr', 'MAPbI | CsPbBr', 'CsNaPbBr',
                             'AgCsSbI', 'CsLiPbBr', '(pF1PEA)MAPbI', '(NH4)FAMAPbBrI', 'BAMAPbI', 'MAPbI',
                             'MAPbI | CsPbI | CsPbBrI', '(PyEA)MAPbI', '(PEA)BAFASnI', '(BZA)PbI', 'CsFAPbI | CsFAPbI',
                             'MACuPbI', 'DIFAPbI', 'CsPbBr | CsPbBr', 'CsLaPbBrI', 'CsFAMAPbI | NMABrPbIBr',
                             'CsPbZnBrI', 'MASnBrI', 'CsPbBrI | CsPbBrI', '(ThMA)FAPbI', 'ANCsMAPbI', 'CsFAGUPbI',
                             '(PEA)FAMASnBrI', 'HASnI', 'CsSnBr', '(CHMA)MAPbI', '(TFEA)CsFAMAPbBrI',
                             'CsFAMAPbBrI | (FPEA)PbI', '(PEA)FASnI', 'CsFAMAPbBrI', 'CsFAKMAPbBrI', 'MAPb(BF4)I',
                             '(BZA)(HAD)MAPbI', '(BIM)MAPbI', '(ALA)MAPbI', 'CsPbSmBr', '(PEA)CsPbI',
                             'MAPbI | (MIC3)PbI', 'GUPbI', 'CsFAPbI', 'FABiPbI', '(BEA)MAPbI', '(PEA)CsMAPbI',
                             '((CH3)3S)SnBrI', '(TBA)MAPbI', '(Anyl)PbI', 'nanCuSbI', 'MAAlCl', 'CsBaPbBr', 'CsGeI',
                             '(GABA)MAPbI', '(Ada)FAPbI', '(CH3ND3)PbI', 'BACsFAMAPbBrI', 'MAHgPbI', 'CsMAPbBrI',
                             '(BdA)PbI', 'CsFAMAPbBrI | (mFPEA)PbI', 'BUFAPbI', 'CsPbBrFI', 'CsRbPbBrI', 'AgCsRbBiBr',
                             '(CHMA)CsMAPbI', '(BzDA)CsFAMAPbBrI', 'FAMAPbBrI | BAPbI', 'FAMAPbBrI | (HTAB)FAMAPbBrI',
                             'ANMAPbI', '(PEA)MAPbClI | MAPbCl', 'MAPbI | CAPbI', '(PEA)FAPbI', 'CsPbI', '(BYA)MAPbI',
                             'FAMAPbBrI | (MIC1)PbI', 'PAPbI', 'CsFAGUPbBrI', '(APMim)PbBrI', 'MAPbSnBrI',
                             'FAMAPbBrI | (C8H17NH3)PbI', 'MASnBrClI', '(Cl-PEA)MAPbClI', 'nanBiCrFeO',
                             '(5-AVAI)CsFAPbI', '(F3EA)BAMAPbI', '(BZA)MAPbI', 'FAPRPbI', '(f-PEA)PbI',
                             'MAPbI | CsPbI | CsPbBrI | CsPbBrI', 'FABiI', '(DMA)PbI', '(PEA)MAPbBrI', 'CsMAPb(SCN)I',
                             'CsFAMASnBrI', 'BAFAPbBrI', 'MAPbSbBrI', 'MAPbI | (PEA)PbI', 'FAMAPbBrI | (MIC2)PbI',
                             'CsMAPbSnI', '(H-PEA)MAPbI', 'CsFAMAPbBrI | BAPbBrI', 'CsFAMAPbBrI | BAPbI', 'RbSbI',
                             'BAGUMAPbI', 'FARbPbI', 'MAPbI | CsPbI | CsPbBrI | CsPbBrI | CsPbBrI', 'AaMAPbI',
                             'CsFAMAPbBrI | (PEI)PbI', 'CsFAKMAGePbBrI', 'CsFAMAPbBrI | (CH3)3SPbI', 'MASnCl', 'KSbI',
                             'BaKNbNiO', 'CsFAPbBrI | (PMA)PbBrI', '(CIEA)MAPbI', '(PEA)CsPbBrI', 'FAMAPbI | TAPbI',
                             'CsFAPbI | (PEA)PbI', '(iPA)PbI', '(4AMP)MAPbI', 'AgBiBr', 'CsSnBrI', 'CsEuPbBrI',
                             'AgCsBiSbBr', '(ThFA)MAPbI', 'FAOASnI', '(DMA)CsMAPbI', 'MAMnI', 'CsKPbBr', 'ANFAMAPbI',
                             'CsFAMAPbSnBrI', 'CsFAPbBrClI', 'CsFAMAPbBrI | PAPbI', '(HdA)PbI', 'CsFAMAPbSnI',
                             '(AVA)PbI | MAPbI', 'FAPbClI', '(ALA)BAMAPbI', 'CsAgBiBr', 'GUSnI', '(TBA)CsFAMAPbBrI',
                             'CsPbI | FAPbI', '(Ace)MAPbI', 'FAPbI', '(PDA)MAPbI', 'CsPbTbBr', '(PEA)PbI | MAPbI',
                             'FAMAPbBrI | (C6H13NH3)PbI', 'MAPbSbI', 'GAMAPbI', 'CsFAGUMAPbBrI', 'BEFAPbI',
                             'CsFAMAPbBrI | (PEA)PbI', '(3AMP)FAMAPbI', '(PEA)CsPbBr', '(AVA)MAPbI', '(PyrEA)PbI',
                             'FAGUSnI', '(Cl-PEA)MAPbI', '(PTA)MAPbI', '((CH3)3S)SnI', 'MAFePbI', 'DAFASnI',
                             'BAMAPbSnI', 'MAPbSnI', '(PEA)PbI | MAPbI | (PEA)PbI', 'MABiSbI', 'FAGUMAPbI',
                             '(MTEA)MAPbI', 'CsMASnI', 'CsFAMARbPbI', '(DPA)MAPAPAPbI', 'FAPNSnI', 'CsFAMARbPbBrI',
                             '(DAP)PbI', 'FASnBr', '(NEA)BAMAPbI', '(PEA)FAMAPbBrI', '(PMA)CuBr', 'GUMAPbI', 'MABiI',
                             'CaFAMAPbBrI', 'CsFAMAPbBrI | (oFPEA)PbI', 'MAPbI | CsPbI', '(THM)MAPbI', 'CsPbSrBrI',
                             'MASnFI', 'CsFAnanPbI', 'MAPbCl'])))

    composition_long_form = Quantity(
        type=str,
        shape=[],
        description="""
    nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(
                suggestions=['Cs0.2FA0.6MA0.2PbBr0.095I0.905', '(PEA)2FA0.5MA3.5Pb5I16', 'Cs0.2FA0.8Pb0.75Sn0.25I3',
                             '(THM)0.05MA0.95PbI3', 'FA0.026MA0.974PbI3', 'CsPbBrI2 | CsxPbBrI2',
                             '(PEA)0.2BA1.8MA3Pb4I13', 'Cs0.17FA0.83Pb0.995Sn0.005I3', '(PEA)2MA9Pb10I31',
                             'Cs0.05FA0.79MA0.16Pb0.58Sn0.42Br0.52I2.48', 'FA0.7MA0.3PbBr0.1I2.9',
                             'FA0.83MA0.13PbBr0.39I2.61', '(NH4)6.8FA0.15MA2.125Pb7.8Br0.45I23.97',
                             'FA0.75K0.1MA0.15PbBr0.55I2.55', 'Cs0.97Na0.03PbBr3', 'Cs0.2FA0.75MA0.05PbBr0.51I2.49',
                             'Cs0.09FA0.77MA0.14PbBr0.42I2.58', 'MASnI3', 'FASnI3 | (PEA)2SnI4',
                             'Cs0.10FA0.83MA0.07PbBr0.51I2.49', 'Cs0.07FA0.725MA0.115PbBr0.45I2.55',
                             'FA0.85MA0.15PbBr0.21I2.79', 'Ag3Bi1.0Br6', 'Cs0.2MA0.8PbI3', '(PDMA)FA2Pb3I10',
                             '(PEA)2MA59Pb60I181', 'GUPb(SCN)2.2I0.8', 'Cs0.05FA0.79MA0.16Pb0.5Sn0.5I3',
                             'MAPbI3 | MAPbBrI2', 'Cs0.9Ag3Bi2.6I9', 'MACu0.05Pb0.9Sn0.05Br0.1I2.9', 'FAPbCl3',
                             'Cs0.10FA0.75MA0.15PbBr0.45I2.55', 'Cs02FA0.8PbBr0.42I2.58', 'CsPbBr3 | FAPbBr2I',
                             'Cs0.3FA0.7PbBr0.256I0.744', 'Cs0.07FA0.9MA0.03PbBr0.24I2.76',
                             'Cs0.1MA0.9Pb0.9Sn0.1Br0.3I2.7', 'MAIn0.25Pb0.75I3', 'MAHg0.1Pb0.9I3',
                             'Cs0.05MA0.95Pb0.95Sn0.1Br0.15I2.85', 'Cs0.25FA0.75PbBr0.6I2.4',
                             'Cs0.1FA0.74MA0.1530PbBr0.51I2.49', 'Cs0.125FA0.875PbBr0.375I2.625', 'MAPb(SCN)I2',
                             'MAPb1.0BrI2', 'MAPbBr0.6I2.4', '(PGA)0.2BA1.8MA3Pb4I13', 'CsPbBr3 | CsPbBrI2',
                             'Cs0.1FA0.7MA0.2PbBr0.3I2.7', 'Cs0.10FA0.36MA0.54PbBr0.2I2.8', '(Ace)0.08MA0.92PbI3',
                             '(Anyl)2MA3Pb4I12', '(PBA)0.5BA1.5MA3Pb4I13', 'Cs0.05FA0.85MA0.15PbBr0.45I2.70',
                             'FA0.67MA0.33PbBr2I', 'FA0.5MA0.5PbBr0.3I2.7', 'Cs0.15FA0.85PbBr0.87I2.13',
                             '(PEA)2MA19Pb20I61', 'Cs0.05FA0.79MA0.16PbBr0.03I2.97', 'Cs0.1FA0.85Rb0.05PbI3',
                             '(Ace)0.03MA0.97PbI3', 'Cs0.1FA0.85MA0.05PbBr0.15I2.85', 'FA0.83MA0.17PbBr0.46I2.54',
                             'Cs0.02FA0.83MA0.17PbBr0.51I2.49', 'FA0.57MA0.43PbBr0.13I2.87', 'MAGeI3', 'HAMAPbI3',
                             'FA0.15MA0.85PbI3', 'CsSnBr2.5I0.5', 'HASnI3', 'Cs0.05FA0.93GU0.02PbI3',
                             'MACu0.01Pb0.99Br0.01I2.99', 'CsNi0.03Pb0.97Br3', 'Cs0.05FA0.78MA0.12PbBr0.51I2.49',
                             'MA3Bi2I10', 'FASnBr3', 'IM0.3MA0.30.7PbI3', 'Cs0.05FA0.76MA0.16PbBr0.48I2.52',
                             'EA0.15MA0.85PbI3', 'MASnI3 | MAPbI3', '(BZA)1.85(HAD)0.15MA2Pb3I10',
                             'Cs0.1FA0.9PbBr0.095I0.905', 'FA0.57MA0.43PbI3',
                             'Cs0.09FA0.77MA0.14PbBr0.42I2.58 | (FPEA)2PbI4', 'Cs0.05FA0.15MA0.85PbI3',
                             'CsEu0.07Pb0.93BrI2', 'Cs0.2FA0.8PbBr0.28I2.72', 'MACa0.01Pb0.99I3',
                             '(THM)0.075MA0.925PbI3', 'Cs0.40MA0.60PbI3', 'FA0.43MA0.57PbBr0.13I2.93',
                             '(Ada)2FA2Pb3I10', 'Cs0.17FA0.83Pb0.4Sn0.6I3', 'MAPbBr0.01I2.99', '(BIM)0.1MAPbI3.2',
                             'Cs0.96K0.04PbBr3', 'Cs0.17FA0.83PbBr0.3I2.7', 'FA0.85MA0.15PbBr3',
                             'Cs0.05MA0.95PbBr1.5I1.5', 'Cs0.2668FA0.666MA0.0664PbBr0.095I0.905',
                             'FA0.85MA0.15PbBr0.45I2.55 | BA0.5FA1.5PbI4', 'MAPbBr0.78I2.22',
                             'Cs0.05MA0.17FA0.76PbBrI2 | BA2PbBr3.2I0.8', 'FA0.95MA0.05PbBr0.15I2.75', 'Cs0.3FA0.7PbI3',
                             'Cs0.34MA0.66PbI3', '(PEA)0.03MA0.97PbI3', 'IM0.3MA0.7PbI3', 'nanPbI2',
                             '(5-AVA)0.05Cs0.05MA0.9PbI3', 'MAPbBr0.56I2.44', 'Cs0.17FA0.83PbBr0.51I2.5',
                             'FA0.93MA0.03PbBr0.09I2.91', 'MASnBr3', 'FA0.37MA0.63PbI3', 'MAPb0.75Sn0.25Br2.4I0.6',
                             'MAPb0.38Sn0.62I3', '(PEA)BAFA3Sn4I13', 'MAPb0.97Sb0.03Br2.94I0.09', 'EA2MA10Pb11I34',
                             'FA0.12MA0.8PbBr0.12I2.88', 'Cs0.05FA0.285MA0.665PbI3', 'BA2MAPb2I7',
                             'Cs0.025FA0.825MA0.15PbBr0.45I2.55', 'FA0.8MA0.2Pb1.0I3', 'MA3PbBr0.32I2.68',
                             'MAPbBr0.27I2.73', 'HAPbI4', 'FA0.15PN0.85SnI3', 'CsEu0.05Pb0.95BrI2',
                             'AN0.15FA0.5MA0.8PbI3', 'FA0.84MA0.16PbBr0.51I2.49', 'Cs0.2FA0.8PbBr0.12I2.88',
                             'Cs0.05FA0.81MA0.14PbI3', 'FA0.048MA0.952PbBrI2.91', 'BA2Cs0.6FA3.4Pb3Sn2.4I17',
                             'MA2CuBr2Cl2', 'Cs0.05FA0.8075MA0.1425PbBr0.45I2.55', 'MAPb0.75Sb0.25I3',
                             'Cs0.2FA0.66MA0.14Pb0.5Sn0.5Br0.5I2.5', 'Cs0.1FA0.75MA0.15PbBr0.35I2.65', 'FAPbBrI2',
                             'FA8PR2Pb9I28', '(DAT)MA2Pb3I10', 'Cs0.05FA0.79MA0.16PbBr0.51I2.49 | (pFPEA)PbI3',
                             '(PEA)2PbI4 | Cs0.1FA0.74MA0.13Pb1Br0.39I2.48 | (PEA)2PbI4',
                             'Cs0.065FA0.79MA0.145PbBr0.49I2.51', 'CsPbBr3', 'Cs0.1FA0.9PbBr0.1I2.9 | (PMA)PbBr0.1I2.9',
                             'Cs0.05FA0.95MAPbI3', 'Cs0.17FA0.83PbBr2.49I0.51', '((CH3)3S)2SnClI5', 'FA0.7GU0.3SnI3',
                             'CsBa0.1Pb0.9BrI2', 'Cs0.05FA0.8265MA0.1235PbBr0.51I2.49', 'BA2MA23Sn4I13',
                             'FA0.33PbBr1.5I1.5', 'CsPb0.88Zn0.12BrI2', 'FA0.57MA0.43PbBr0.13I2.91',
                             'FA0.85MA0.15Pb1.0Br0.45I2.55', '(MTEA)2MA4Pb5I16', 'FA0.8MA0.2PbBr0.6I2.40',
                             'FA0.17MA0.83PbBrI2', 'IM0.05MA0.95PbI3', '(4AMP)MA3Pb4I13', 'Cs0.15AgBi3I8.5',
                             'Cs0.8MA0.2PbI3', 'Cs0.2FA0.8PbBr0.9I2.1', 'FA0.85MA0.15PbBr0.45I2.55 | PEA2PbI4',
                             'Cs0.4FA0.2MA0.4PbI3', 'MAGeBrI2', 'MAPbBr0.045I2.955', 'FA0.75MA0.25PbBr0.45I2.55',
                             'MAIn0.10Pb0.90I3', 'Cs0.05FA0.79MA0.16Pb0.5Sn0.5Br0.5I2.5', 'FAPbI3 | (ODA)2PbI4',
                             '(PEA)2MA8Pb9Br11.2I16.8', 'Cs2FAnanPbI3', 'HA0.4MA0.6SnI3',
                             'Cs0.05FA0.79MA0.16PbBr0.15I0.85', 'FA0.97MA0.03PbBr0.09I2.91 | (MIC1)2PbI4',
                             'FAPb0.75Sn0.25I3', 'FA4GeSbCl12', 'Cs0.1FA0.1MA0.8Pb1.0I3', 'Cs0.1MA0.9PbBr1.2I1.8',
                             'MAPb0.4Sn0.6Br1.2I1.8', 'BA2FA2Pb3I10', 'MAPb0.75Sn0.25Br1.2I1.8', 'MAPbBr0.1I2.9',
                             'CsPbBr0.45I2.55', 'Cs0.1MA0.9Pb0.7Sn0.255I3', 'FA0.9MA0.1PbBr0.15I2.85',
                             'Cs0.2FA0.66MA0.14Pb0.25Sn0.75Br0.5I2.5', 'CsMAPbI3', 'MAIn0.05Pb0.95I3',
                             'Cs0.2FA0.66MA0.14SnBr0.5I2.5', 'Cs0.2FA0.8PbBr0.6I2.4', 'GUPb(SCN)3I',
                             'Cs0.1FA0.36MA0.54PbBr0.2I2.8', 'FA0.85MA0.15Pb1.0Br0.15I0.85',
                             'FA0.15MA0.85PbBr0.15I2.85', 'Cs0.05FA0.7885MA0.1615PbBr0.4845I2.4155', 'FA0.66MA0.34PbI3',
                             'Cs0.05FA0.79MA0.16Pb0.916Sn0.084Br0.52I2.48', 'CsSnBr0.3I2.7', 'GU0.25MA0.75PbI3',
                             '(TBA)0.03MA0.97PbI3', 'FA0.125MA0.875PbBrI2', 'IM0.25MA0.250.75PbI3',
                             'FA0.5MA0.5PbBr0.13I2.92', 'MAPb0.3Sn0.7I3', 'BAFA10Pb11I34', 'FA0.83MA0.17PbBr0.52I2.48',
                             'FA0.3MA0.7PbBr2.1I0.9', 'CsPbBrI2', 'IMPbI3', 'CsPbBr3 | CsPb2Br5',
                             'Cs0.15FA0.75MA0.1PbI3', 'CsNi0.003Pb0.997Br3', 'MASnBr0.42I2.58',
                             'Cs0.05FA0.79MA0.16PbBr0.51I2.49 | (mFPEA)PbI3', 'Cs0.05FA0.80MA0.15PbBr0.43I2.57',
                             'Cs0.88K0.12PbBr3', '(CIEA)0.03MA0.97PbI3', '(PyEA)2MA8Pb9I28', 'CsPbBrxIx',
                             'FA0.3MA0.7PbBr0.225I2.775', 'FA0.75MA0.75PbI3', 'AgCs2BiBr5.9', 'HA0.1MA0.9PbI3',
                             '(GABA)0.1MA0.9PbI3', 'FA0.83MA0.17PbBr0.03I2.97', 'Cs0.04FA0.96PbI3', '(PEA)2MAPb2I4',
                             'Cs0.1FA0.83MA0.17PbBr0.51I0.249', 'FA0.85MA0.15PbBr0.5I2.5', 'CsAgBiBr6',
                             'FA0.55MA0.45PbI3', 'FAPbBr2.43Cl0.57', '(F5PEA)2PbI4', 'FASn1.0I3',
                             'Cs0.25FA0.75PbBr0.51I2.49', 'MAMnI3', 'FA0.7MA0.3PbBr0.256I0.744',
                             'Cs0.05FA0.85MA0.1PbBr0.66I2.34', 'FAxMAxPbBrxIx', 'FA0.7MA0.3Pb0.7Sn0.3I3',
                             'FA0.3MA0.7PbBr0.3I2.7', 'Cs0.005Pb0.995Br3', 'Cs0.05FA0.7885MA0.1615PbBr0.34I2.66',
                             'AN0.06MA0.94PbI3', '(f-PEA)2PbI4', 'MAPbBrI', 'BA2Cs0.15FA0.57MA2.28Pb4I13',
                             'Cs0.17FA0.83PbI3', 'Cs0.4FA0.6PbBr0.256I0.744', 'CsPbBr3I', 'Ca0.2MA0.8PbBr0.6I2.4',
                             'CsBa0.3Pb0.7BrI2', 'Ag3Bi2I9', 'Cs0.15FA0.85PbBr2.1I0.9', 'IM0.4MA0.40.6PbI3',
                             'Cs0.1FA0.75MA0.15PbBr0.45I2.55', 'Cs0.2FA0.32MA0.48PbBr0.2I2.8', 'BA2MA3Pb4I13',
                             'Cs0.14FA0.65MA0.21PbBrI2', 'CsPbBr2.7I0.3', 'FA0.83MA0.17Ge0.03Pb0.97Br0.3I2.7',
                             'CsPbBr2.8I0.2', 'MAHg0.05Pb0.95I3', 'Cs0.4MA0.6PbI3', 'MAPbBr0.08I2.92',
                             'Cs0.08FA0.78MA0.14PbBr0.45I2.55', 'MAEu0.1Pb0.9I3', 'Cs0.005Pb0.995Br1.99I1.01',
                             'Cs0.05FA0.79MA0.16Pb0.25Sn0.75Br0.5I2.5', 'CsPbBr0.75I2.25', '(PEA)2PbI4 | MAPbI3',
                             '(HEA)2Cs0.9FA8.1Pb10Br3.3I29.7', 'Cs0.05FA0.7885MA0.16150PbBr0.51I2.49',
                             'Cs0.2FA0.8PbBr1.5I1.5', 'CsEu0.03Pb0.97BrI2', '(PEA)0.1MA0.9SnI3',
                             '(NH4)8.5FA0.15MA2.04Pb9.5Br0.45I29.24', 'Cs0.25FA0.75Pb0.37Sn0.6255I3',
                             'Cs0.2FA0.8PbBr0.15I2.85', 'Cs0.1MA0.9Pb0.9Sn0.1Br0.2I2.8',
                             'Cs0.05FA0.79MA0.16PbBr0.52I2.48', 'MAPbBr0.237I2.763', 'CsPbBr3 | CsPbI3',
                             'FAPbBr1.25Cl0.35I1.45', 'Cs0.03FA0.97PbI3', 'Cs0.06FA0.87MA0.07PbBr0.12I2.88',
                             'FAPb0.5Sn0.5I3', 'FA0.75MA0.25PbI3', 'Cs0.04FA0.71GU0.1MA0.15PbBr0.5I2.49',
                             'EA0.5MA0.5PbBr3', 'Cs0.03FA0.77MA0.2PbBr0.46I2.54', 'Cs0.5FA0.75MA0.1PbBr0.51I2.49',
                             'MAPbBr0.06I2.94', 'FA0.10MA0.9PbI3', 'Cs0.05FA0.78MA0.13PbBr0.45I2.55',
                             'MAPb0.75Sn0.25Br1.8I1.2', 'CsPb0.97Zn0.03Br3', 'Cs0.05FA83MA17PbBr0.51I2.49',
                             'Cs0.17FA0.83PbBr0.5I2.5', 'FA0.85MA0.15PbBr0.45I2.55 | BA1.5FA0.5PbI4', 'MAFe0.1Pb0.9I3',
                             'Cs0.12FA0.88PbBr0.36I2.54', 'FA0.5MA0.5PbBr3', 'FA0.85MA0.15PbBr0.45I2.55 | (FEA)2PbI4',
                             'Cs0.15(DMA)0.85MA0.15PbI3', 'Ca0.05FA0.8075MA0.1425PbBr0.45I2.55',
                             'BA2Cs0.15MA2.85Pb4I13', 'Cs0.05FA0.79MA0.16Pb0.75Sn0.25Br0.5I2.5', 'MAPbBr0.09I2.1',
                             'Cs0.06FA0.58MA0.36PbBr0.12I2.88', 'IM0.1MA0.9PbI3', 'Cs0.05FA0.79MA0.16PbBr0.3I2.7',
                             'Cs0.17FA0.83Pb0.3Sn0.7I3', 'Cs0.05FA0.85MA0.1PbBr0.45I2.55 | (PEA)2PbI4', 'MABi2I9',
                             'FA0.26MA0.74PbI3', 'FA0.85MA0.15PbBr0.3I2.7', 'FA0.85MA0.15PbBr0.50I2.50',
                             'FA0.17MA0.83PbBr0.5I2.5', 'MA3BiI2', 'FA0.83MA0.17PbBr0.39I2.61',
                             '(NH4)5.1FA0.15MA1.7Pb6.1Br0.45I18.7', 'Cs0.05FA0.7917MA0.1583PbBr0.5I2.5',
                             'Cs0.01FA0.94Rb0.05PbI3', 'MABiSbI9', '(NH4)3Sb2Br3I6', '(PEA)0.15FA0.85SnI3',
                             'FA3OA2Sn4I13', 'RbPbI3', 'Cs0.1MA0.9PbBr0.1I2.9', '(PEA)2Cs9Pb10I34',
                             'Cs0.1FA0.77MA0.13PbBr0.4I2.6', 'CsPbBr3 | FAPbBr3', 'CsSnBrI2', 'Cs0.2FA0.8Pb0.3Sn0.7I3',
                             '(NH4)11.9FA0.15MA1.7Pb12.9Br0.45I39.1',
                             'Cs0.05FA0.81MA0.14PbBr0.45I2.55 | CsPbBr1.85I1.15', 'FA0.8MA0.2PbBr0.2I2.8',
                             'Cs0.09FA0.77MA0.14PbBr0.42I2.58 | (PEA)2PbI4', 'BA2MA3Pb4I9', 'FAPbBr0.44I2.56',
                             '(PEA)2FA3Pb4I13', 'MAPb(BF4)2.85I0.15', '(CHMA)2MA39Pb40I121', 'MA3Bi2I11',
                             'FA0.5MA0.5SnI3', 'Cs0.21Ag3Bi3.14I9', '(oF1PEA)2MA4Pb4I13', 'HA2MA3Pb4I13',
                             'CsPbBr3 | FAPbBr1.5Cl1.5', 'CsFAMAPbBrI', '(PEA)2Cs1.77FA57.23Pb60I181',
                             'FA0.75MA0.25SnI3', 'Cs0.05FA0.7885MA0.1441PbBr0.3I2.7', 'MAPbBr1.5I1.5',
                             'Cs0.085FA0.915PbBr0.45I2.55', '(PEI)2MA6Pb7I22', 'MASnBr1.5Cl0.5I',
                             'Cs0.05FA0.79MA0.16PbBr0.47I2.53', 'Cs0.15FA0.75MA0.1PbBr0.5I2.5',
                             '(PEA)x(F5PEA)xCs0.15FA0.64MA0.2PbBr0.6I2.4', 'Cs0.2FA0.8PbBr1.2I1.8',
                             'CsPb0.99Sr0.01BrI2', 'Cs0.92K0.08PbBr3', 'MAHg0.075Pb0.925I3', 'FA0.9MA0.1PbBr0.03I2.91',
                             'Cs0.05FA0.79MA0.16PbBr2.51I2.49', 'FA0.95MA0.05PbBr0.1I2.9', 'CsBa0.1Pb0.9I3',
                             '(BYA)2MA3Pb4I13', 'Cs0.07FA0.93PbI3', 'MA2PA3Pb4I13', 'FAPbCl0.5I2.5',
                             'Cs0.0664FA0.8668MA0.0664PbBr0.095I0.905', '(Ace)0.2MA0.8PbI3', 'MAPb0.9Sr0.1I3',
                             'Cs0.75FA0.25PbI3', 'FA0.83MA0.17PbBr0.17I2.83', '(PEA)2Cs59Pb60I181', 'BA2MA2Pb3I9',
                             '(HEA)2Cs1.9FA17.1Pb20Br9.45I53.55', 'FA0.28MA0.72PbI3', '(iso-BA)0.5MA0.75PbI3.25',
                             'Cs0.15FA0.85PbBr0.12I2.88', 'FA0.88MA0.12PbBr0.15I2.85', 'Cs0.92Li0.08PbBr3',
                             'Cs0.175FA0.750MA0.075PbBr0.36I2.64', '(BZA)1.8(HAD)0.2MA2Pb3I10', '(3AMP)MA3Pb4I13',
                             'Cs0.06FA79MA0.15PbBr0.45I2.55', 'FAPb0.625Sn0.375I3', '(PMA)0.67FA0.33PbI3',
                             '(TBA)0.01MA0.99PbI3', 'Cs0.15MA0.85PbBr1.2I1.8', 'MAPbBr1.16I1.74',
                             'FA0.83MA0.17PbBr0.51I2.49', 'FA0.85MA0.15PbBr0.15I0.85', '(PEA)2Pb2I4', 'MASbSnI9',
                             'Cs2Pb(SCN)2I', 'FA0.85MA0.15PbBr0.45I0.85', 'Cs0.88Na0.12PbBr3', 'nanBi2O6',
                             'CsPbBrF0.12I1.88', '(PEA)2Cs0.45FA2.55Pb4I13', 'Cs0.25FA0.75PbBr0.60I2.40',
                             'EA0.92FA0.08SnI3', '(PDA)0.05Cs0.15FA0.8PbI3', '(APMim)PbBrI3', 'MASbI3',
                             '(PEA)1.4BA0.6MA3Pb4I13', 'FA0.95MA0.15PbBr0.45I2.5075', 'MAPbBr0.9I2.1',
                             'Cs0.05FA0.75MA0.15PbBr0.15I2.85', 'FA0.90TN0.10SnI3', 'MAMn0.1Pb0.9I3',
                             'Cs0.1FA0.9PbBr0.09I2.91', 'MA2Au2Br6', 'FA0.75MA0.25Pb0.75Sn0.25I3',
                             'FA0.85MA0.15PbBr0.55I2.55', 'Cs0.05FA0.38MA0.57PbBr0.2I2.8', 'MA2PA6Pb7I22',
                             'Cs0.04FA0.82MA0.14PbBr0.42I2.58', 'Cs0.05FA0.8K0.03MA0.12Ge0.03Pb0.97Br0.3I2.7',
                             'MAPbBr2.85I0.15', 'Cs0.05FA0.79MA0.16PbBr1.2I2.6', 'FA0.75MA0.25PbBr0.25I2.79', 'CsSnI3',
                             '(5-AVAI)0.02Cs0.05FA0.93PbI3', 'Cs0.05FA0.79MA0.16PbBr0.41I2.59', 'AN0.5MA0.5PbI3',
                             'MACo0.2Pb0.8I3', '(TBA)0.1Cs0.05FA0.71MA0.14PbBr0.51I2.49', 'MAEu0.04Pb0.96I3',
                             'Cs0.17FA0.83Pb0.6Sn0.4I3', 'Cs0.1FA0.75MA0.15PbBr0.46I2.54', 'MA2SnI6',
                             'FA0.75MA0.25PbBr0.75I2.25', 'MAPbBr0.19I2.81', '(5-AVA)0.05MA0.95PbI3', '((CH3)3S)2SnI6',
                             'Cs0.06FA0.94PbBr0.03I2.97', 'AN0.15Cs0.5MA0.8PbI3', 'MAPbI3 | CsPbI3', 'FA0.2PN0.8SnI3',
                             'BA2Cs0.2FA0.6MA3.2Pb5I16', 'Cs0.05FA0.81MA0.14PbBr0.42I2.58', 'Cs0.1FA0.9PbBr0.6I2.4',
                             '(3AMP)FA0.9MA2.1Pb4I13', 'Cs0.02MA0.98PbBr0.06I2.94', 'Cs0.07FA0.785MA0.145PbBr0.45I2.55',
                             'Cs0.01Pb0.99Br1.98I1.02', 'FAHA2Pb2I7', 'Cs0.5FA0.5PbI3', 'Cs0.5FA0.85PbI3',
                             'FA0.2MA0.8Pb1.0I3', 'Cs0.1FA0.1MA0.8PbI3', 'CsPbBr0.21I2.79', 'EA2MA8Pb9I28',
                             'Cs0.15FA0.71MA0.1PbBr0.39I2.61', 'MAPbI3 | MAPbBr1.2I1.8',
                             'Cs0.05FA0.82MA0.13PbBr0.13I2.87', 'Cs0.1FA0.76MA0.14PbBr0.51I2.49', 'Bn2SnI4',
                             'Cs0.14FA0.83MA0.17PbBr0.51I0.249', 'Cs0.05FA0.79MA0.16PbBr0.51I', 'MACa0.02Pb0.98I3',
                             'FA0.9MA0.1PbBr0.03I2.97', 'CsFAPbBrClI', 'Cs0.15FA0.26MA0.59PbI3', 'MAPb0.92Sb0.08I3',
                             '(mF1PEA)MA4Pb4I13', 'FA0.7MA0.3PbBr0.10I2.90', 'CsFA0.83MA0.17PbBr0.5I2.5',
                             'Cs0.04MA0.96PbI3', 'PA2PbI4', '(PEA)0.1FA0.15MA0.75SnI3', '(PDA)0.03Cs0.15FA0.82PbI3',
                             'CsCu0.003Pb0.997Br3', 'AgBiI4', 'FA0.17MA0.83PbBr2.5I0.5', 'Cs0.1FA0.9PbBr0.225I2.775',
                             '(Ace)0.1MA0.9PbI3', 'Cs0.05FA0.8MA0.15PbBr0.55I2.55', 'Cs0.17FA0.83Pb0.5Sn0.5I3',
                             'Cs0.07FA0.79MA0.14PbBr0.45I2.55', 'MAPb0.75Sn0.25I', '(PEA)2FA3Sn4I13',
                             'Cs0.17FA0.83Pb0.8Sn0.2I3', '(Cl-PEA)2MA2Pb3ClI10', 'Cs0.05MA095PbI3',
                             '(PEA)2Cs59Pb60Br120.67I60.33', 'MAPbBr0.7I2.3', '(ThFA)2MA2Pb2I7',
                             '(EDA)0.04FA0.29MA0.67Pb1.0I3', 'FA0.97MA0.03PbBr0.09I2.91', 'FA0.7MA0.3PbBr0.9I2.1',
                             'FA0.83MA0.17PbBr0.17I0.83', 'Cs0.1FA0.75MA0.15PbBr1.5I1.5',
                             'Cs0.16FA0.8MA0.04PbBr1.5I1.5', 'CsPb0.6Sn0.4I3', 'Cs0.05FA0.76MA0.16PbBr0.49I2.51',
                             'EA2MA19Pb20I61', 'MAPb0.375Sn0.625I3', '(F-PEA)2MA2Pb3I10',
                             'Cs0.05FA0.85MA0.1PbBr0.5I2.5', 'FA0.92MA0.08PbI3', 'FA0.7MA0.3PbBr0.095I0.905',
                             'AN0.3MA0.7PbI3', 'Cs0.05FA0.81MA0.14PbBr0.45I2.55', 'FA0.6MA0.4PbBr0.4I2.6',
                             'Cs0.05FA0.79MA0.16PbBr0.30I2.70', 'CsPbBr1.5I1.5', '(PEA)0.1FA0.9SnI3', 'Cs2NaBiI6',
                             'FA0.95MA0.05PbBr0.15I2.85 | BA2PbI4', 'MAPbI3 | MAPbBr0.9I2.1', 'MAPbBr2.5I0.5',
                             'Cs0.12MA0.88PbBr0.36I2.64', 'MA0.98PbI3', 'MAPbBr2.52I0.48', 'Cs0.17FA0.83PbBr0.17I0.83',
                             'FA0.1MA0.9PbI3', 'MAPbBr1.62I1.38', 'Cs0.1FA0.6MA0.3PbBr0.095I0.905',
                             'Cs0.05FAxMAxPbBrxIx', 'FA0.83MA0.17PbBr0.51I2.59', 'Cs0.025FA0.7MA0.25Rb0.025PbI3',
                             'MAPbI3-xClx', 'FA0.84MA0.16PbBr0.48I2.52', 'Cs0.25FA0.75PbBr0.9I2.1', 'IM0.2MA0.8PbI3',
                             'FA0.2MA0.8PbBr0.45I2.55', 'FA0.2MA0.8PbI3', 'MACu0.1Pb0.9I3', 'Cs0.08FA0.92PbBr3',
                             'FA0.83MA0.17PbBrI2', 'CsBi2I7', 'FA0.4MA0.6PbBr0.6I2.4', 'FAPbBr2.67Cl0.33',
                             'CsPb0.9Sn0.1Br2I', 'MAPbBr2.91I0.09', 'Cs0.15FA0.75MA0.1PbBr0.4I2.6',
                             '(EDA)0.04FA0.28MA0.68Pb1.0I3', '(CHMA)2MA2Pb3I10', 'MAPbBr0.4I2.6', 'Aa0.05MA0.95PbI3',
                             '(NH4)3Sb2Br6I3', 'GU0.1MA0.9PbI3', 'HA0.2MA0.8SnI3', 'Cs0.1FA0.9PbBr0.3I2.7',
                             'MAGeBr0.15I2.75', 'CsPbI3', 'Cs0.04FA0.8MA0.16PbBr0.49I2.51', 'MASnBr2I',
                             'Cs0.12FA0.83MA0.05PbBr1.2I1.8', 'Cs0.05FA0.88MA0.07PbBr0.24I2.76', 'Cs0.45FA0.55PbI3',
                             'MACo0.063Pb0.937I3', 'Cs0.05FA0.827MA0.123PbBr0.369I2.631', 'MAPb0.99Sr0.01I3',
                             'MAPbBr0.09I2.91', 'Cs0.05FA0.75MA0.2PbI3', 'MASb1.2Sn0.8I9', '(TBA)0.1MA0.9PbI3',
                             'Cs0.99Rb0.01PbBrI2', 'Cs0.02FA0.98PbI3 | Cs0.57FA0.43PbI3', '(PDA)MA3Pb4I13', 'MAPbISCN',
                             'Cs0.17FA0.83PbBr0.30I2.7', 'FAPbI3 | EDA22Pb3I10', '(CPEA)2MA5Pb6I19',
                             'MACu0.0118Pb0.9882Br0.2I2.8', '(DPA)2MA3PAPAPb4I13', 'FA0.85MA0.15PbBr0.27I2.73',
                             '(C6H4NH2)CuBr2I', 'Cs0.25FA0.75PbBr0.6I2.40', 'BA2MA2Pb3I10', '(3AMP)FA0.75MA2.25Pb4I13',
                             'MACo0.016Pb0.984I3', 'MAPbBr0.02I2.98', '(CIEA)0.05MA0.95PbI3',
                             'Cs0.07FA0.93PbBr0.06I2.94', 'nanCu3SbI6', 'Cs0.05MA0.95PbBr0.9I2.1',
                             'Cs0.11FA0.74MA0.15PbBr0.51I2.49', 'Cs0.15FA0.85PbBr0.81I2.19', 'Cs0.05Pb0.95Br1.9I1.1',
                             '(PBA)2MA3Pb4I13', 'CsGe0.3Pb0.7BrI2', 'MAPbBr1.26I1.74', 'Cs0.05FA0.93GA0.02PbI3',
                             'MACa0.10Pb0.90I3', 'MAPbI3 | MAPbI3', 'FA0.25MA0.75Pb0.75Sn0.25I3',
                             '(PEA)0.6BA1.4FA3Sn4I13', 'MAPbBr0.39I2.61', 'Cs0.97Rb0.03PbBr3', '(4ApyH)SbI4',
                             'Cs0.17FA0.83PbBr0.81I2.19', 'FA0.87MA0.13PbBr0.51I2.49', 'AgCs2Bi0.75Sb0.25Br6',
                             'FA0.84MA0.16PbBr0.5I1.5', 'Cs0.1FA0.75MA0.15Pb0.25Sn0.75Br0.5I2.5', 'MAPb0.93Sb0.07I3',
                             '(PEA)2Cs79Pb80I241', 'FA0.3MA0.67PbI3', 'CsPbBrF1.88I0.12', '(H-PEA)2MA2Pb3I10',
                             'Cs0.05FA0.75MA0.2PbBr0.3I2.7', '(BEA)2MA3Pb4I13', 'FAPbBr1.25Cl0.25I1.5',
                             'EA0.4MA0.6PbI3', 'Cs0.79FA0.16MA0.1PbBrI2', 'MAPb1.0Br0.6I2.4',
                             'Cs0.05FA0.78MA0.16PbBr0.5I2.5', 'FA0.8MA0.8PbBr0.06I2.96', 'Ca0.05MA0.95PbBr0.15I2.85',
                             'MAPbBr0.30I2.70', 'FA0.3MA0.7Pb1.0I3', 'FA0.7MA0.3Pb0.5Sn0.5I3', 'KBABiTeO6',
                             'CsPb0.97Tb0.03Br3', 'MAPbBr0.2I2.7', 'MA2PA4Pb5I16', 'Cs0.30FA0.70PbI3',
                             'Cs0.07FA0.81MA0.1146PbBrI2', 'FA0.8MA0.2PbBr0.45I2.55', 'MAPbI3 | (PEA)2PbI4',
                             'Cs0.05FA0.95PbBr0.15I2.85', '(PDA)0.04Cs0.15FA0.81PbI3', 'Cs0.05FA0.79MA0.17PbBr0.5I2.5',
                             'Cs0.3FA0.6MA0.1PbBr0.256I0.744', 'MA3Bi2I9', 'BAGUMA4Pb5I16', 'MAPb1.0Br0.3I2.7',
                             'Cs0.05FA0.65MA0.3PbBr0.15I2.85', 'CsPb0.98Sr0.02BrI2', 'MAPbBr0.075I2.95',
                             '(CPEA)2MA2Pb3I10', 'Cs0.15FA0.71MA0.14PbBr0.45I2.55', 'MAPbBr0.03I2.7', 'AN0.4MA0.6PbI3',
                             'Cs0.05MA0.95PbI3', 'Cs0.07FA0.78MA0.15PbBr0.45I2.55',
                             'Cs0.05FA0.79MA0.11Rb0.05PbBr0.39I2.61', '(APMim)PbBr2I3', 'Cs0.05FA0.80MA0.15PbI2.55',
                             'Cs0.1FA0.9PbI3 | (PEA)2PbI4', '(CPEA)2MA4Pb5I16', 'Cs0.05FA0.83MA0.17PbI3',
                             'Cs0.05FA0.81MA0.14PbBr0.57I2.43', '(TBA)0.3MA0.7PbI3',
                             'Cs0.1FA0.77MA0.13PbBr0.39I2.48 | (PEA)2PbI4', 'Cs0.05FA0.81MA0.14PbBr0.39I2.61',
                             'Cs0.07FA0.785MA0.115PbBr0.45I2.55', 'MAPbBr0.75I2.25', 'BA2Cs0.08MA3.92Pb5I16',
                             'Cs0.05FA0.92MA0.3PbBr0.09I2.91', 'FA0.57MA0.43PbBr0.04I2.96', 'BDACs4Pb5Br4.8I11.2',
                             'IM0.03MA0.97PbI3', '(PBA)BAMA3Pb4I13', 'MAPbBr0.15I2.85',
                             'Cs0.32FA0.58GA0.1PbBr0.81I2.19', 'FA0.6MA0.4Sn0.6I3', 'GU0.17MA0.83PbI3',
                             'Cs0.04FA0.80MA0.16PbBr0.51I2.49', 'FAxMAPbBrxI', 'BAMA3Pb4I13', 'Cs0.02MA0.98PbI3',
                             'AgCs2Bi0.5Sb0.5Br6', 'MAPbBr0.033I2.97', 'Cs0.05FA0.83MA0.17PbBr0.45I2.55',
                             'EA0.5MA0.5PbI3', 'FA0.83MA0.17PbBr2.5I0.5', '(BZA)1.9(HAD)0.1MA2Pb3I10',
                             'GUPb(SCN)2.6I0.4', 'MAPbI3 | MABaPbI3', 'FA0.9MA0.1PbBr0.256I0.744', 'FA3Bi2I9',
                             'Cs0.10FA0.75MA0.15PbBr0.51I2.49', 'Cs0.04FA0.92MA0.04PbI3 | (FEA)2PbI4',
                             'MAPbI3 | MAPbBr3', 'Cs0.1FA0.81MA0.09PbBr0.17I2.83', 'Cs0.1FA0.75MA0.15PbBrI2',
                             'CsPb0.5Sn0.5BrI2', '(EDA)0.01FA0.29MA0.7Pb1.0I3', 'Cs0.1MA0.9PbI3',
                             '(PEA)0.1FA0.15MA0.75SnBr0.24I2.76', 'Cs0.01FA0.99PbI3', 'CsPb1.0Br1.8I1.2',
                             'BAFA60Pb61Cl4I180', 'FA0.98MA0.02PbBr0.06I2.94', '(PEA)2MA39Pb40I121',
                             'FA0.85MA0.10PbBr0.3I2.7', 'MA0.1Mg0.1Pb0.9I3', 'MAPbBr0.60I2.40',
                             'Cs0.075FA0.75MA0.175PbBr0.33I2.67', 'Cs0.2FA0.8PbI3', 'Cs0.025FA0.475MA0.5Pb0.5Sn0.5I3',
                             'MA2CuBr3.5Cl0.5', 'FA0.95MA0.05PbBr0.15I2.85 | DA2PbI4', '(PDA)MAPb2I7',
                             'MAPb0.2Sn0.8Br0.4I2.6', 'CsPb1.0Br1.5I1.5', 'FA0.8MA0.2PbBr0.095I0.905', 'MASnF0.4I2.6',
                             'BU2FA8Pb9I28', 'MASnBr2.64I0.36', '(4AMP)MA2Pb3I10', 'Cs0.15FA0.85PbBr0.45I2.55',
                             'BA2MA3Pb4I12', 'Cs0.05FA0.07MA0.25PbI3', 'Cs0.04FA0.96PbBr3', 'Cs2Bi3I9',
                             'MABa0.01Pb0.99I3', 'Cs0.05FA0.79MA0.16Pb0.748Sn0.252Br0.52I2.48',
                             'Cs0.2FA0.8PbBr1.05I1.95', 'FA0.1MA0.9Pb1.0I3', 'FA0.78MA0.21PbBr0.21I2.79',
                             'BA2Cs0.3FA1.7Pb1.8Sn1.2I10', 'MA0.1Mn0.1Pb0.9I3', '(BEA)0.5MA3Pb3I10', 'FA0.38MA0.62PbI3',
                             'MAPbBr0.43I2.57', 'FA0.81MA0.19Pb0.57I2.33', 'FAPbI3', 'Cs0.05FA0.79MA0.16PbBr0.6I2.4',
                             'Cs0.2FA0.72MA0.08PbBr0.03I2.97', 'Cs0.133FA0.733MA0.133PbBr0.095I0.905',
                             'CsPbI3 | FAPbI3', 'MAPb0.9Sn0.1I3', '(ThMA)2MA2Pb3I10', 'Cs0.32FA0.58GU0.1PbBr0.81I2.19',
                             'Cs0.1FA0.75MA0.13PbBr0.45I2.55', 'GU0.50MA0.50PbI3', 'MA0.05Pb0.95I3', 'Cs0.06FA0.94PbI3',
                             '(HEA)2Cs2.9FA26.1Pb30Br9.3I83.7', 'Cs0.17FA0.83Pb0.9999Sn0.0001I3',
                             'Cs0.1FA0.135MA0.765PbBr0.45I2.55', 'MAPb0.50Sn0.50Br1.2I1.8', 'FA0.81MA0.15PbBr0.45I2.55',
                             'nanPb2I8', '(TBA)0.5Cs0.03FA0.4MA0.08PbBr0.51I2.49', 'Cs0.80K0.20PbBr3',
                             'MAPbCl0.06I2.94', 'Cs0.05FA0.85MA0.1PbBr0.03I2.97', '(Anyl)2MA2Pb3I9',
                             'Cs0.1FA0.54MA0.36PbI3', 'CsBi0.06Pb0.94I3', 'Cs0.67FA0.33PbBr0.75I2.25', 'CsFASnI3',
                             'Cs0.1FA0.65MA0.25PbI3', 'Cs0.05FA0.77MA0.16PbBr0.48I2.52', 'MAPb0.85Sn0.15I3',
                             'FAPbBr0.45I2.55', '(N-EtPy)SbBr6', 'MAPbBr3', 'MAPbBr0.33I2.67', 'MAPb0.25Sn0.75I3',
                             'Cs0.14FA0.83MA0.03PbBr0.51I2.49', 'Cs0.05FA0.89MA0.06PbBr0.18I2.82',
                             'FA0.2MA0.8PbBr0.15I2.85', 'Cs0.15FA0.8GA0.05PbBr0.45I2.55', '(THM)0.1MA0.9PbI3',
                             '(BZA)1.95(HAD)0.05MA2Pb3I10', 'FAMAPbBr3I', 'Cs0.05MAPbBr0.45I2.55',
                             'Cs0.05FA0.6MA0.35PbBr0.3I2.7', 'Cs0.20FA0.80PbBr1.2I1.8', 'Cs0.4FA0.6PbBr0.9I2.1',
                             'FAPbI3 | (PEA)2PbI4', 'Cs0.5Rb0.5SnI3', 'Cs0.1MA0.9SnI3',
                             'Cs0.05FA0.79MA0.12PbBr0.39I2.61', 'CsCa0.03Pb0.97Br3', 'Cs0.05FA0.79MA0.15PbBr0.45I2.55',
                             'Cs0.15FA0.85PbI3', 'MASbI2', 'MA0.125Pb0.875I3', 'MACu0.05Pb0.95Br0.05I2.95', '(DAP)PbI4',
                             'Cs0.05FA0.7885MA0.1615PbBr0.51I2.49', 'AN0.09MA0.91PbI3',
                             'Cs0.07FA0.81MA0.12PbBr0.38I2.62', 'MASb1.6Sn0.4I9', '(NMA)2MA39Pb40I121',
                             'MAPbI3 | (EU-pyP)2PbI4', 'Cs0.15FA0.85PbBr0.3I2.7', 'FASnBr0.24I2.76', 'FA0.5MA0.5PbI3',
                             'FAMAPbBrI', 'MAGeBr0.3I2.9', 'Cs0.091FA0.758MA0.152PbI3', 'Cs0.17FA0.83PbBr1.8I1.2',
                             'BDACs2Pb3Br3I7', 'FA0.85GU0.15SnI3', 'MAPb0.95Sn0.05Br0.1I2.9', 'Cs0.2FA0.2MA0.6PbI3',
                             'Cs0.05FA0.95SnI3', 'MAPb0.8Sr0.2I3', 'Ag2BiI5', 'Cs0.05FA0.85MA0.10PbBr0.45I2.55',
                             'Cs0.05FA0.81MA0.14PbBr0.4I2.6', 'Cs0.07FA0.7MA0.23PbBr0.69I2.31', 'FA0.65MA0.35PbI3',
                             '(TMA)SnI3', '(PEI)2MA2Pb2I10', '(AVA)2PbI4 | MA1Pb1I3 | (BI)2PbI4',
                             'Cs0.05FA0.79MA0.16PbBr0.51I2.49 | BAPbI4', 'CsPbBr3 | FAPbBr1.5I1.5',
                             'MAPbI3 | (BI)2PbI2', 'GU0.14MA0.86PbI3', 'Cs0.05FA0.79MA0.16PbBr0.51I2.49 | CsPbI3',
                             'GU0.125MA0.875PbI3', 'Cs0.05FA0.79MA0.16PbBr1.5I1.5', 'CsSn0.05I2.95', 'MAPbBr0.25I2.75',
                             'Cs0.2FA0.8PbBr0.3I2.7', 'Cs0.3FA0.7Pb0.7Sn0.3I3', 'Cs0.25FA0.75Pb0.6Sn0.4I3',
                             'Cs0.04FA0.82MA0.14PbBr0.45I2.55', 'Cs0.0664FA0.666MA0.2668PbBr0.256I0.744',
                             'Cs0.05FA0.79MA0.16PbBr0.75I2.25', 'FA0.1MA0.9PbI3 | TAPbI3',
                             'Cs0.05FA0.79MA0.16PbBr0.45I2.55', 'Cs0.05FA0.87MA0.0782PbBrI2', 'MAPbI3 | (C4H9N2H6)PbI4',
                             'Cs0.6MA0.4PbI3', 'BA2MA4Pb5I16', '((CH3)3S)2SnBr2I4', 'Cs0.05FA0.05MA0.9PbBr0.05I2.95',
                             'MAPbBr0.2I2.8', 'MAPb0.5Sn0.5Br0.6I2.4', '(Ace)0.15MA0.85PbI3', 'CsPbBr', 'EA2MA2Pb3I10',
                             'Cs0.05FA0.788MA0.162PbBr0.5I2.5', 'DI2FA8Pb9I28', 'MAPbI3 | CsPbBr3',
                             'Ca0.1MA0.9PbBr0.3I2.7', '(PEA)1.8BA0.2MA3Pb4I13', 'Cs0.09FA0.58MA0.33PbBr0.65I2.35',
                             'CsPbBrF1.78I0.22', 'FA0.9MA0.1PbI3', 'CsSnBr0.5I2.5', 'FAPbBr0.15I2.85',
                             'Cs0.30MA0.70PbI3', '(NH4)10.2FA0.15MA1.7Pb11.2Br0.45I34', 'FA0.96MA0.04PbBr0.12I2.88',
                             'Cs0.05FA0.79MA0.16Pb0.54I2.46', 'CsLa0.02Pb0.98BrI2', 'MAPbBr0.04I2.96',
                             'MAPb0.4Sn0.6Br0.9I2.1', 'IM0.025MA0.0250.975PbI3', 'AN0.2MA0.8PbI3', 'Cs0.02FA0.98PbI3',
                             'FA0.6MA0.4PbBr1.2I1.8', '(DMA)0.05MA0.95PbI3', 'BA2MA2Sn3I10', 'Cs0.94Na0.06PbBr3',
                             'FA0.75MA0.25Ge0.2Sn0.8I3', 'MAPb0.75Sn0.25I3', '(PEA)2Cs3Pb4I13', 'FA0.125MA0.875PbI3',
                             '(CHMA)2MA3Pb4I13', 'FA0.6MA0.4Pb0.4Sn0.6Br0.48I2.52', 'Cs0.05FA0.49MA0.16PbBr0.51I2.49',
                             'Cs0.05FA0.83MA0.12PbBr0.36I2.64', 'Ag2Bi3I11', '(PEA)FASnI3', 'Cs0.05FA0.79MA0.16PbI3',
                             'Cs0.15FA0.75MA0.1PbBr0.1I2.9', 'Cs0.15FA0.71MA0.14PbBr0.75I2.25', 'MAGeBr0.3I2.7',
                             'Cs0.05FA0.81MA0.14PbBr0.45', 'MAPb0.5Sb0.5I3', '(PEA)2MA5Pb4Cl2I10 | MA3PbCl2',
                             'FA0.38MA0.57PbI3', 'Cs0.025FA0.81MA0.15PbBr0.45I2.5', 'BA2Cs4MA35Pb40I121',
                             'Cs0.05FA0.79MA0.16PbBr0.39I2.61', 'AgCs1.7Rb0.3BiBr6', 'Cs0.09MA0.91PbI3',
                             '(NH4)1.7FA0.15MA1.7Pb2.7Br0.45I8.5', 'GU0.05MA0.95PbI3', 'Cs0.13FA0.87PbBrI2', 'MAPbI3',
                             'Cs0.05FA0.8MA0.15PbBr0.75I1.25', 'MAPbBr2.25I0.75', '(ThMA)2FA4Pb5I16',
                             'Cs0.21FA0.56MA0.23PbBr0.06I2.94', '(BDA)MA3Pb4I13', 'Cs0.15FA0.8Rb0.05PbI3',
                             'MABa0.1Pb0.9I3', '(PEA)xCs0.15FA0.64MA0.2PbBr0.6I2.4',
                             'Cs0.05MA0.95Pb0.95Sn0.05Cl0.1I2.9', 'Cs0.08FA0.81MA0.12PbBr0.35I2.65',
                             'Cs0.3FA0.6MA0.1PbBr0.095I0.905', 'GU0.2MA0.8PbI3', 'FA0.5MA0.5PbI4',
                             'FA0.67MA0.33PbBr0.5I2.5', 'Cs0.05FA0.7885MA0.1615PbBr0.1I0.9', 'FA0.9MA0.1PbBr0.3I2.7',
                             '(NH4)6.8FA0.15MA2.04Pb7.8Br0.45I24.14', 'FA0.65K0.2MA0.15PbBr0.55I2.55',
                             'FA0.625MA0.935PbI', '(HEA)2Cs1.9FA17.1Pb20Br6.3I56.7', 'FA0.975MA0.025PbI3',
                             'Cs0.02Pb0.98Br1.96I1.04', 'FA0.95MA0.05PbBr0.15I2.85 | OA2PbI4',
                             'FA0.95MA0.05PbBr0.15I2.85', 'CsLa0.03Pb0.97BrI2', 'FA0.75MA0.15PbBr0.45I',
                             'Cs0.05FA0.79MA0.160Pb1.0Br0.3I2.7', '(PEA)2MAPbI4', 'Cs0.25FA0.75PbBrI2',
                             'Cs0.94Rb0.06PbBr3', 'Cs0.05FA0.15MA0.8PbI3', '(NH4)3.4FA0.15MA2.04Pb4.4Br0.45I13.94',
                             'CsPb0.997Zn0.003Br3', 'CsBi3I10', 'Cs0.15FA0.75MA0.1PbBr0.3I2.7', 'CsPb0.3Sn0.7I3',
                             'Cs0.15FA0.85SnI3', 'Cs0.06FA0.79MA0.15PbBr0.45I2.55', 'CsCu0.01Pb0.99Br3',
                             'FA0.17MA0.83PbBr1.5I1.5', 'Cs0.15FA0.85PbBr0.25I2.75', 'CsPb0.75Sn0.25Br2I', 'MAPbCl3',
                             'FA0.14MA0.86PbBr0.42I2.58', 'MAHgI3', 'Cs0.23MA0.77PbI3', 'GUPb(SCN)1.8I1.2',
                             '(DMA)0.075MA0.925PbI3', '(PEA)2Cs39Pb40Br40.33I80.67',
                             '(TFEA)2Cs0.225FA7.425MA1.35Pb10Br4.65I26.35', 'FA0.9GU0.1SnI3', 'MA3Bi2I13', 'Cs3Bi2I9',
                             'BA2PbI4', 'FA0.7MA0.3PbI3', 'Cs0.1FA0.9PbBr0.9I2.1', 'FASnBrI2', 'FAPb0.375Sn0.625I3',
                             'Cs0.2FA0.8PbBr0.32I2.68', 'Cs0.2FA0.6MA0.2PbBr0.256I0.744',
                             'Cs0.05FA0.79MA0.16PbBr0.51I2.49 | PA2PbI4', 'MAPb0.98Zn0.02I3', '(n-C3H7NH3)PbCl3',
                             '(PTA)2MA3Pb4I13', 'Cs0.2FA0.8PbBr0.256I0.744', 'Cs0.1MA0.9Pb0.25Sn0.75I3',
                             '((CH3)3S)2SnBrI5', 'MAPbI3 | FAPbBrI2', 'FA0.83MA0.17PbBr0.51', 'FA0.1MA0.9PbBr0.3I2.9',
                             'BA2CsPb2I7', 'MAPbI3 | (BEA)PbI4', 'Cs0.10MA0.90PbI3', 'CsPb0.97Sr0.03Br3',
                             'FA0.67MA0.33PbBr0.33I2.67', 'Cs0.05FA0.83MA0.12PbBr0.5I2.5', 'CsBi0.04Pb0.96I3',
                             '(TBA)0.3Cs0.04FA0.55MA0.11PbBr0.51I2.49', 'MAPbI3 | (MIC1)2PbI4', 'Ag3BiI3(SCN)3',
                             'FAPbBr0.6I2.4', 'Cs0.003Pb0.997Br3', 'CsNi0.005Pb0.995Br3',
                             'Cs0.05FA0.788GU0.032MA0.129PbBr0.51I2.49', 'Cs0.07FA0.73MA0.20PbBr0.47I2.53',
                             'FA0.02MA0.98PbI3', 'FA0.975MA0.025PbBr0.075I2.925', 'Cs0.17FA0.83Pb0.98Sn0.02I3',
                             'MAPb0.95Sn0.05I3', 'Cs0.10FA0.81MA0.09PbBr0.03I2.97',
                             '(NH4)6.8FA0.15MA1.7Pb7.8Br0.45I23.8', 'FAPbBr0.25I2.75', 'MAPb0.2Sn0.8I3',
                             'Cs0.05FA0.79MA0.16PbBr0.51I2.49 | (oFPEA)PbI3', 'MAPb1.0Br0.66I2.33', 'BA2FA3Sn4I13',
                             'MAPbBr0.11I2.89', 'Cs0.10MA0.90Pb(SCN)0.15I2.85', '(PEA)2Cs99Pb100I301',
                             'MAPbBr0.51I2.49', 'FA0.85MA0.15PbBr0.45I2.45', 'FA0.88MA0.12PbI3',
                             'Cs0.05FA0.79MA0.16Pb1.0Br0.51I2.49', 'MAPbI3 | (MIC3)2PbI4', 'FAPbBr0.095I0.905',
                             'FAPb0.4Sn0.6I3', 'MAPb0.8Sn0.2I3', 'MAPb0.75Sn0.25Br0.9I2.1', 'Ag2CsSb2I3',
                             'Cs0.17FA0.83PbBr1.5I1.5', 'Cs0.08MA0.92PbBr0.24I2.76', 'Cs0.05FA0.70MA0.25PbI3',
                             'MAPb0.4Sn0.6I3', 'MAPb0.97Zn0.03I3', 'MACu0.05Pb0.95Br0.1I2.9',
                             'FA0.85MA0.15Pb0.45I2.55 | (NH4)8FA2.4Pb9I28.4',
                             'Cs0.05FA0.79MA0.16PbBr0.51I2.49 | (PEI)2PbI4', 'Cs0.02FA0.82MA0.16PbBr0.51I0.249',
                             'Cs0.88FA0.12PbI3 | Cs0.88FA0.12PbIx(PF6)x', 'FA0.97MA0.03PbBr2.91I0.09',
                             'FA0.976MA0.024PbBr0.075I2.925', 'CsPbBr0.6I2.4', 'FA0.94MA0.6PbBr0.06I2.94',
                             '(PEA)0.5MA0.5PbI3', 'FA0.67MA0.33PbI3', 'Cs0.17FA0.83PbBr0.45I2.55',
                             'FA0.94MA0.06PbBr0.06I', 'FA0.9MA0.1PbBr0.1I2.9', 'Cs0.05FA0.81GU0.025MA0.11PbBr0.39I2.61',
                             '(PEA)2Cs59Pb60Br181', 'FA0.85MA0.15PbBr0.03I2.97', 'HDABiI5', 'CsPb0.93I3', 'FA0.33PbBr3',
                             'MAPbBr0.075I2.925', 'Cs0.05FA0.79MA0.16PbBr0.51I2.49 | (PEA)PbI3', 'CsCu0.03Pb0.97Br3',
                             '(HEA)2Cs1.9FA17.1Pb20Br0I63', 'FA0.6MA0.4Pb0.4Sn0.6Br0.18I2.82', '(PyrEA)PbI4',
                             'BA2MA3Pb4.0I13', 'FA0.1MA0.9Pb0.9Sn0.1I3', '(TBA)0.2Cs0.04FA0.63MA0.13PbBr0.51I2.49',
                             'BA2Cs1.5MA2.85Pb4I13', '(NH4)3.4FA0.15MA1.7Pb4.4Br0.45I13.6', '(PEA)0.4MA0.6PbI3',
                             'FA0.58MA0.42PbI3', 'Cs0.05FA0.7MA0.25PbI3', 'Cs0.05FA0.85MA0.15PbBr0.75I2.25',
                             'FA0.6MA0.4PbSn0.6I0.4', 'CsGe0.5Sn0.5I3', 'CsPbBrF0.22I1.78', 'GAMA4Pb4I13',
                             'BA2MA10Pb11I34', 'EA3MA2NEAPb4I13', 'MA2PbI4', 'Cs0.15FA0.85PbBr0.15I2.85',
                             'MASb1.8Sn0.2I9', 'FA0.75MA0.25Ge0.05Sn0.95I3', 'CsPb0.25Sn0.75Br2I',
                             'Cs0.2FA0.66MA0.14PbBr0.5I2.5', 'Cs0.0664FA0.666MA0.2668PbBr0.095I0.905',
                             'FA0.83MA0.17PbI3', 'MAPb1.0Br0.45I2.55', 'Cs0.05FA0.80MA0.15PbI3',
                             'Cs0.1MA0.90PbBr0.3I2.70', 'FA0.85MA0.15PbI5', 'Cs0.06FA0.78MA0.16PbI3',
                             '(PEA)0.1MA0.9PbI3', 'Cs0.84K0.16PbBr3', 'Cs0.17FA0.83Pb0.99999Sn0.00001I3',
                             '(BDA)MAPb2I7', 'FA0.2MA0.8PbBr0.3I2.9', 'BDACs3Pb4Br3.9I9.1',
                             'Cs0.1FA0.747MA0.153PbBr0.17I0.83', 'FAPbBr1.5I1.5', 'MA0.03Mg0.03Pb0.97I3',
                             '(1.3-Pr(NH3)2)0.5Pb1.0I3', 'FA0.83MA0.17PbBr0.6I2.4', 'Cs0.20MA0.80PbI3',
                             'FA0.1MA0.9PbBrI2.8', 'MAPb0.75Sn0.25Br0.6I2.4', 'Cs0.15MA0.85PbI3',
                             '(NH4)6.8FA0.15MA1.275Pb7.8Br0.45I23.375', 'CsPbBr0.3I2.7', 'FA0.84MA0.16PbBr0.50I2.50',
                             'Cs0.07FA0.775MA0.145PbBr0.45I2.55', 'FA0.7MA0.3PbBr0.3I2.9', '(pF1PEA)2MA4Pb4I13',
                             '(ALA)2MA3Pb4I13', 'FA0.9MA0.1PbBr0.095I0.905', 'CsHA2Pb2I7',
                             'Cs0.175FA0.75MA0.075PbBr0.33I2.67', 'MA2PA8Pb9I28', '(IEA)2MA2Pb2I7', 'FAMAPbI3',
                             'FA0.3MA0.7PbBr0.45I2.55', 'MAPb0.97Sn0.03Br0.06I2.94', 'MAPb0.6Sn0.4Br0.4I2.6',
                             'MAPb0.4Sn0.6Br2.1I0.9', 'Cs0.25FA0.75PbBr0.3I2.7', 'Cs0.25FA0.75PbI3 | CsPbI3',
                             'Cs0.1FA0.9PbBr3', '(TEA)2MA3Pb4I14', 'Cs0.06FA0.77MA0.17PbBr0.17I0.83',
                             'Cs0.05FA0.79MA0.16Pb0.84Sn0.84Br0.52I2.48', 'FA0.85MA0.15PbBr0.15I2.85',
                             'Cs0.08FA0.92SnI3', 'Cs0.05FA0.5MA0.45Pb0.5Sn0.5I3', 'CsPbBr0.2I2.8', 'HA2MAPb2I7',
                             'CsPbBr1.5I1.5 | FAPbBr1.5I1.5', 'Cs0.05FA0.788GU0.129MA0.032PbBr0.51I2.49',
                             'Cs0.15MA0.85PbBr0.45I2.55', '(Anyl)2PbI3', 'MAPb0.93Sb0.03I3', 'MAPb0.25Sb0.75I3',
                             'Cs0.5FA0.5PbBr0.51I2.49', 'MA0.75Sn0.25I3', 'Cs0.07FA0.81MA0.12PbBr0.39I2.61',
                             '(Cl-PEA)2MA3Pb4I13', 'MAPbBr0.06I2.24', 'Cs0.05FA0.83MA0.12PbBr0.49I2.51',
                             'Cs0.05FA0.8MA0.15PbBr0.15I0.85', 'MAPb0.75Sn0.25Br0.3I2.7', 'Cs0.45FA0.55PbBr0.15I2.85',
                             'MAHg0.2Pb0.8I3', 'CsBa0.4Pb0.6BrI2', 'Cs0.05MA0.95PbBr1.2I1.8', 'Cs0.05FA0.28MA0.67PbI3',
                             'FA0.8MA0.15PbBr0.45I2.55', 'Ag4Bi7I25', 'FA0.82MA0.18PbBr0.53I2.47', 'FA0.95GU0.05SnI3',
                             'Cs0.17FA0.83MAPbBr2.59I0.51', 'FA0.8MA0.2PbBr0.6I2.4', 'FA0.81MA0.19PbBr0.5I2.5',
                             'AgCs1.9Rb0.1BiBr6', 'FA0.5MA0.5PbBr0.45I2.55', 'FA0.5MA0.5Pb0.5Sn0.5I3', 'AgCs2BiBr5.5',
                             'CsPbBr0.15I2.85', 'Cs0.1MAPbBr0.45I2.55', 'FA0.4MA0.6PbBr0.1I2.9', 'MAPb0.96Sb0.04I3',
                             'FA0.85MA0.15Pb0.6Sn0.4Br0.45I2.55', 'FABi3I10', 'FA0.285GU0.05MA0.665PbI3',
                             'Cs0.96Li0.04PbBr3', 'CsPb0.995Zn0.005Br3', 'Cs0.1FA0.2MA0.7PbI3', 'MASnCl3',
                             'MAPb0.9Sb0.1I3', 'FA0.25MA0.75PbI', 'FA0.5MA0.5PbBr0.25I2.75', 'MAPbBr1.2I1.8',
                             '(GABA)0.5MA0.5PbI3', 'MAPb(BF4)2.80I0.2', 'EA0.3MA0.7PbI3',
                             'Cs0.05FA0.80MA0.15PbBr0.51I2.49', 'Cs0.07FA0.78MA0.15PbBr0.51I2.49',
                             'Cs0.225FA0.75MA0.025PbBr0.33I2.67', 'FA0.3MA0.7PbI3', 'MAPbBr0.6Cl2.4', 'HA2PbI4',
                             'Cs0.05FA0.8MA0.15PbBr0.5I2.5', 'FA0.5MA0.5PbBr1.5I1.5', 'Cs0.05FA0.8MA0.15PbI3',
                             'Cs0.05FA0.19MA0.76PbI3', 'Cs0.24FA0.76PbI3', 'FA0.83MA0.17PbBr2I',
                             'Cs0.05FA0.788GU0.065MA0.097PbBr0.51I2.49', 'Cs0.1FA0.75MA0.15PbBr0.5I2.5',
                             '((CH3)3S)2SnCl2I4', 'Cs0.06FA0.67MA0.27PbBr0.3I2.7', 'Cs0.1FA0.7MA0.2Pb0.5Sn0.5I3',
                             '(5-AVA)2FA4Sn5I16', 'FA0.81MA0.15PbBr0.45I2.51', 'FA0.6MA0.4Pb0.6Sn0.6I3',
                             'MAPbBr2.1I0.9', 'Cs0.05FA0.875MA0.075PbBr0.225I2.775', 'FA0.75MA0.25PbBr0.25I2.75',
                             'MAPb(BF4)2.90I0.1', 'Cs0.02FA0.37MA0.61PbBr0.04I2.96', 'Cs0.06FA0.78MA0.16PbBr0.54I2.46',
                             'GUMA3Pb3I10', 'FAPb0.2Sn0.8I3', 'Cs0.05FA0.79MA0.16PbBr0.51I2.49 | (CH3)3SPbI3',
                             'MACu0.05Pb0.8Sn0.15Br0.1I2.9', 'Cs0.2FA0.8PbBr0.095I0.905',
                             'Cs0.05FA0.79MA0.16Pb0.832Sn0.168Br0.52I2.48', 'Cs0.15FA0.85PbBr0.9I2.1',
                             'Cs0.04FA0.81MA0.14PbBr0.43I2.57', 'CsGe0.1Pb0.9BrI2', 'Cs0.05FA0.81MA0.14PbBr0.43I2.57',
                             'FA0.5MA0.5PbBr2I', 'FABi0.05Pb0.95I3', 'FAPbBr0.05I2.95', 'Cs0.05MA0.95PbBr0.3I2.7',
                             'Cs0.05FA0.7885MA0.1615PbI3', 'Cs0.75MA0.25PbI3', 'MAPbBr0.36I2.64',
                             'Cs0.15FA0.76MA0.09PbBr0.03I2.97', 'Cs0.12FA0.5MA0.38PbBr0.96I2.04',
                             'FA0.83MA0.17PbBr0.0I2.51', 'Cs0.3FA0.2MA0.5PbI3', '(GABA)0.05MA0.95PbI3', 'MABiI2',
                             'Cs0.17MA0.83PbI3', 'MASnBr1.2I1.8', 'MAPbIx', 'MAPb1.0ClI2', 'BA2MA34Pb5I15',
                             'Cs0.05MA0.95Pb0.95Sn0.05Br0.1I2.9', 'Cs0.05FA0.85MA0.15PbBr0.45I2.55', '(3AMP)MA2Pb3I10',
                             'CsGe0.2Pb0.8BrI2', '(NEA)0.2BA1.8MA3Pb4I13', 'Cs0.05FA0.86MA0.09PbBr0.3I2.7',
                             'CsCu0.005Pb0.995Br3', 'MAPbBr0.12I2.88', 'FA0.93MA0.07PbBr0.21I2.79',
                             '(NMA)2MA59Pb60I181', '(PEA)2MA5Pb4Cl2I10', 'FA0.4MA0.6PbBr0.2I2.8',
                             '(PBA)1.5BA0.5MA3Pb4I13', 'MAPb1.0Br1.5I1.5', 'AgBiI7', 'FA0.75MA0.25Ge0.1Sn0.9I3',
                             'CsPb0.97Sm0.03Br3', 'Cs0.05FA0.83MA0.17PbBr0.51I2.49', 'FA0.83MA0.17PbBr0.22I2.78',
                             'FA0.75MA0.25PbBr0.51I2.49', 'FA0.33PbI3', 'FA0.85MA0.15PbBr0.6I2.4',
                             'Cs0.05FA0.83MA0.17PbBr0.36I2.64', 'FAPbBr3', 'FA0.3MA0.7PbBr0.15I2.85',
                             'FA0.33MA0.66Pb0.66Sn0.33I3', 'BAFA60Pb61Br4I180', 'MABiI3', 'AgCs2BiBr5.4',
                             'FA0.95MA0.05PbBr0.15I2.85 | (HTAB)0.03FA0.95MA0.05PbBr0.15I2.85',
                             'Cs0.05FA0.75MA0.11PbBr0.39I2.61', 'Cs0.1MA0.9PbBrI2', '(PGA)2MA3Pb4I13',
                             'Cs0.3FA0.7PbBr3', 'MAPbBr1.74I1.26', 'Cs0.05FA0.7885MA0.1615PbBr0.3I2.7',
                             'Cs0.05FA0.788GU0.162PbBr0.51I2.49', 'MAPbBr1.77I1.23', 'AgCs2BiBr5.8',
                             'Cs0.05FA0.83MA0.17PbBr0.17I0.83', 'Cs0.1MA0.9Pb0.5Sn0.5I3', 'Cs0.3Ag3Bi2.2I9',
                             'CsPbBr0.31I2.69', 'Cs0.15FA0.72MA0.13PbBr0.45I2.55', 'MAPbBr1.7I1.3', 'FAPbBr0.3I2.7',
                             'FA0.33PbBrI2', 'Cs0.1FA0.27MA0.63PbI3', 'Cs0.15FA0.75MA0.1PbBr0.7I2.3',
                             'CsPb0.5Sn0.5Br2I', 'Cs0.98Li0.02PbBr3', 'MAPbBr1.8I1.2', 'MAPb0.95Zn0.05I3', 'GUPbI3',
                             'Cs0.1FA0.79MA0.16PbBr0.51I2.49', 'Cs0.05FA0.8075MA0.1425PbBr0.51I2.49', 'FA0.8TN0.2SnI3',
                             'FA0.45MA0.55PbI3', 'Cs0.05FA0.79MA0.16PbBr0.54I2.46', 'FA0.83MA0.17PbBr3',
                             'Cs0.1FA0.765MA0.135PbBr0.45I2.55', 'Cs0.08FA0.76MA0.16PbBr0.51I2.49', 'BA2PbI3',
                             'IM0.2MA0.20.8PbI3', 'Cs0.1FA0.75MA0.15PbBr0.55I2.55', 'MAPb1.0Br0.15I2.85', 'nanBiI3',
                             'MACu0.014Pb0.986I3', 'CsBa0.03Pb0.97Br3', '(3AMP)FA0.6MA2.4Pb4I13', 'MAGeBr0.6I2.4',
                             'MAPb0.95Sb0.05I3', 'Cs0.04FA0.80MA0.16PbBr0.50I2.50', 'MAAlCl4', 'AgCs2BiBr5.7',
                             'GU0.075MA0.925PbI3', 'Cs0.02FA0.84MA0.14PbBr0.05I2.95', '(5-AVA)0.1MA0.9PbI3',
                             'Cs0.2FA0.6MA0.2PbBr0.33I2.67', 'FA0.5MA0.5PbBr0.5I2.5', 'Cs0.1MA0.9Pb0.75Sn0.25I3',
                             'Cs0.05FA0.81MA0.14Pb0.95Br0.43I2.42', 'AgCs2BiBr6', '(PEA)2MA29Pb30I91', 'MAPb0.7Sn0.3I3',
                             'FA0.07MA0.93PbI3', 'Cs0.05FA0.80MA0.15PbBr0.25I2.75', 'MAPb1.0I3', 'MAPb0.6Sn0.4I3',
                             'Cs0.15FA0.85PbBr0.6I2.4', 'Cs0.1FA0.9PbBr0.1I2.9 | (PEA)PbBr0.1I2.9', 'EA2MA4Pb5I16',
                             'MA0.01Pb0.99I3', 'IM0.05MA0.050.95PbI3', 'FA0.67MA0.33PbBr1.5I1.5',
                             'Cs0.05FA0.81MA14PbBr2.55I0.45', 'FA0.83MA0.17PbBr0.5I2.5', 'Cs0.1FA0.7MA0.2PbBr0.2I2.8',
                             'FAPbCl0.45I2.55', 'FA0.29MA0.71PbBr0.3I2.7', 'FAPbBr', 'BA2MA3Pb3SnI13', '(PDA)MA2Pb3I10',
                             '(PEA)2Cs39Pb40I121', 'FA0.6MA0.4PbI3', 'Cs0.16FA0.8MA0.04PbBr1.83I1.17', 'SrTiO3',
                             'FA0.66MA0.33PbBr0.45I2.55', '(GABA)0.025MA0.975PbI3', 'Cs0.06FA0.8MA0.14PbBr0.45I2.55',
                             'FA0.15MA0.85PbBr2.55I0.45', 'FA0.85MA0.15PbBr0.451I2.55', '(BZA)2MA2Pb3I10',
                             'MAPbI3 | Cs1Pb1I3 | Cs1Pb1Br0.3I2.7 | Cs1Pb1Br0.7I2.3 | CsPbBrI2',
                             '(PEA)2Cs9Pb10Br10.33I20.67', 'FAPbBr0.1I2.9', 'Cs0.2FA0.24MA0.56PbI3',
                             'CsPbBrI2 | CsPbBrI2', 'MAPb0.5Sn0.5I3', '(3AMPY)MA3Pb4I13', 'Cs0.05FA0.5MA0.5PbBr1.5I1.5',
                             'Cs0.5FA0.5PbI3 | CsPbI3', 'MAPbI3 | FAPbBr1.5I1.5', '(THM)0.025MA0.975PbI3',
                             'Cs0.17FA0.75MA0.08PbBr0.39I2.61', '(6-ACA)0.038MA0.962PbI3', '(PEA)2PbI4',
                             'FA0.83MA0.17PbBr0.47I2.53', 'Cs0.15Ag3Bi3I9', 'MAPbBr1.6I1.4', 'MAPb0.97Sr0.03I3',
                             '(BDA)MA2Pb3I10', 'FA0.6MA0.4Pb0.4Sn0.6Br0.12I2.88', 'Cs0.05FA0.83MA0.12PbBr0.51I2.49',
                             '(PEI)2PbI4', 'Cs0.17FA0.83Pb0.999Sn0.001I3', 'Cs0.08FA0.09PbBr3',
                             'Cs0.05FA0.7885MA0.1615PbBr0.4845I2.5155', 'Cs0.05FA0.85MA0.5PbBr0.25I2.75',
                             'MAPbI3 | CA2PbI4', 'Ag4Bi5I19', 'MAPb0.8Sn0.2Br0.4I2.6',
                             'FA0.92MA0.08PbBr0.24I2.76 | (C8H17NH3)2PbI4', 'MAPb0.75Sn0.25Br1.5I1.5',
                             'FA0.4MA0.6PbBr0.3I2.7', 'CsSnBr2.7I0.3', 'MACo0.008Pb0.992I3', '(OdA)PbI4',
                             'Cs0.1FA0.9PbBr0.135I2.865', '(PEA)2MA4Pb5I16', 'CsPb0.94Zn0.06BrI2', 'FA0.05PN0.95SnI3',
                             'FA0.97MA0.03PbBr0.09I2.91 | (MIC3)2PbI4', 'CsPb0.97Sr0.03BrI2', 'MAPbBrI2',
                             '(CPEA)2MA3Pb4I13', 'Cs0.02FA0.15PDA0.82PbI3', '(NH4)6.8FA0.15MA0.85Pb7.8Br0.45I22.95',
                             'MA4PbI6', 'Cs0.05FA0.8075MA0.1425PbBr0.3I2.7', '(PEA)0.4BA1.6MA3Pb4I13',
                             'MAEu0.06Pb0.94I3', '(NH4)6.8FA0.15MA2.21Pb7.8Br0.45I24.31', 'MAPb0.4Sn0.6Br1.5I1.5',
                             'BA0.15FA0.85SnI3', 'FA0.95MA0.05PbBr01.51I2.85', 'Cs0.05FA0.85MA0.1PbBr0.1I2.9',
                             'MAPbBr2I', 'Cs0.06FA0.79MA0.15PbBr0.51I2.49', 'Cs0.08FA0.92PbI3',
                             'Cs0.75FA0.25PbI3 | CsPbI3', 'FA0.83MA0.17PbBr0.49I2.51', 'MAPbBr0.5I2.5',
                             'Cs0.1665FA0.667MA0.1665PbBr0.33I2.67', '(EDA)0.005FA0.3MA0.695Pb1.0I3',
                             'GU0.025MA0.975PbI3', 'Cs0.08FA0.78MA0.14PbBr0.42I2.38', '(CHMA)2MAPb2I7',
                             '(NH4)5.1FA0.15MA2.04Pb6.1Br0.45I19.04', 'Cs0.1FA0.6MA0.3PbBr0.256I0.744',
                             'FA0.85MA0.15Pb0.45I2.55', 'FA0.75MA0.25PbBr0.25I2.77', 'Cs0.05FA0.81MA0.15PbBr0.45I2.55',
                             'Cs0.15FA0.85Pb0.375Sn0.625I3', '(NH4)8.5FA0.15MA1.7Pb9.5Br0.45I28.9',
                             'Cs0.2FA0.8PbBr0.16I2.84', 'Cs0.05FA0.89MA0.6PbBr0.06I2.94', '(BZA)2PbI4', '(PEA)2CsPb2I7',
                             'Cs0.05FA0.28MA0.67PbBr0.54I2.46', '(PEA)2Cs7Pb8I25', 'MAPb0.75Sn0.25Br2.1I0.9',
                             '(NH4)3Sb2I9', 'EA2MA6Pb7I22', 'CsSnBr0.6I2.4', 'MAPb0.995Sb0.005I3', 'EA2MA5Pb6I19',
                             'MA3PbCl2', 'Cs0.88Rb0.12PbBr3', 'Cs0.133FA0.733MA0.133PbBr0.256I0.744',
                             'FA0.67MA0.33PbBr3', 'MAPbBr1.41I1.59', 'MAPb0.7Sn0.255I3', 'Cs0.1FA0.7MA0.2PbBr0.5I2.5',
                             '(PEA)2Cs9Pb10I31', '(PEA)MAPbI3', 'Cs0.05FA0.75MA0.2PbBr0.51I2.49',
                             'FA0.6MA0.4Pb0.4Sn0.6I3 | (PEA)2Pb0.4Sn0.6I4', '(PDMA)FA2Pb23I7', '(Br-PEA)2MA2Pb3BrI10',
                             'CsBi9I28', 'Cs0.05FA0.788MA0.162PbBr0.51I2.49', 'BA2FA0.6MA2.4Pb4I13',
                             'FA0.83MA0.17PbBr0.3I2.7', 'Cs0.2MA0.8Pb0.5Sn0.5I3', '(DMA)PbI3', 'AN0.015MA0.985PbI3',
                             'Cs0.91Na0.09PbBr3', 'BA2MA2Pb4I13', '(Anyl)2MAPb2I6', 'FA0.75MA0.25PbBr0.24I2.76',
                             'FA0.83MA0.17PbBr0.37I2.63', 'Cs0.05FA0.79MA0.16PbBr0.48I2.52',
                             'Cs0.07FA0.93PbBr0.15I2.85', 'Cs0.05FA0.84MA0.11PbBr0.1I2.9', 'Cs0.01MA0.99PbBr0.03I2.97',
                             'FAPbBr0.5I2.5', 'MAPbBr0.45I2.55', 'Cs0.17FA0.83Pb0.7Sn0.3I3',
                             'Cs0.1FA0.75MA0.13PbBr0.45I2.55 | (A43)2PbI4', 'Cs0.8FA0.69MA0.23PbBr0.9I2.1',
                             'MAPb(Br0.7I0.3)xCl3-x', 'MAPb0.75Sn0.25Br2.7I0.3',
                             'Cs0.1FA0.76MA0.14PbBr0.51I2.49 | (EPA)2PbI4', 'CsSnBr1.5I1.5',
                             'Cs0.17FA0.83Pb0.99Sn0.01I3', 'Cs0.05FA0.788MA0.162PbBr0.3I2.7', 'MAPbBr0.84I2.16',
                             'Cs0.05FA0.46MA0.49PbBr0.12I2.88', 'GU0.15MA0.85PbI3', '(CH3ND3)PbI3',
                             '(F3EA)0.12BA1.88MA3Pb4I13', '(PEA)2MA5Pb6I19', 'MAPb0.99Sb0.01I3', 'Cs0.14FA0.86PbI3',
                             'MAPbBr0.48I2.52', '(CHMA)2Cs4MA35Pb40I121', 'MAPb1.0Br3', 'FA0.11MA0.89PbI3',
                             'CsPbBr3 | FAPbBr2Cl', 'MAPbI3 | Cs1Pb1I3 | CsPbBr0.3I2.7', 'FA0.35MA0.65PbBr0.13I2.94',
                             'FA0.8MA0.2PbBr0.2I0.8', 'CsPbI3 | CsPbI3', 'MAPbI3 | BAPbI4', 'MASb1.9Sn0.1I9',
                             'Cs0.05FA0.57MA0.38PbI3', 'MAPbBr0.18I2.82', 'MA3PbI3', 'Cs0.02FA0.79MA0.16PbBr0.551I2.49',
                             'FA0.9MA0.1PbBr0.2I2.7', 'CsPbBrF1.72I0.28', '(PDA)MAPbI4',
                             'Cs0.1FA0.75MA0.15Pb0.75Sn0.25Br0.5I2.5', 'FAMAPbBr0.45I2.55', 'MAPbBr0.21I2.79',
                             'K3Sb2I9', 'CsPbBr0.09I2.91', 'FA0.75MA0.25PbBr0.25I2.80', 'AgBi2I7',
                             'Cs0.05FA0.9Rb0.05PbI3', 'FA0.84MA0.16PbBr0.4I2.6', 'Cs0.07FA0.89GU0.02PbI3',
                             '(HEA)2Cs1.9FA17.1Pb20Br3.15I59.85', 'Cs0.05FA0.79MA0.16PbBr0.65I2.35', 'FA0.85MA0.85PbI3',
                             'Cs0.05FA0.79MA0.16PbBr0.51I2.49 | HAPbI4', 'Cs0.17FA0.83PbBr0.6I2.4', 'FAPb0.7Sn0.3I3',
                             '(BDA)PbI4', 'Cs0.05FA0.76MA0.16PbBr1.5I1.5', 'Cs0.15FA0.75MA0.1PbBr0.2I2.8',
                             'FA0.85TN0.15SnI3', 'MAPb0.625Sn0.375I3', 'MAPb0.99Zn0.01I3', 'LaYS3',
                             'FA0.8K0.05MA0.15PbBr0.55I2.55', '(5-AVA)0.03MA0.97PbI3', 'MAPbBr0.225I2.775',
                             'Cs0.85Rb0.15PbBr3', 'FA0.5MA0.5PbBrI2', '(CIEA)0.1MA0.9PbI3', '(ThMA)MA4Pb5I16',
                             'FABiPbI3', 'Cs0.2FA0.8Pb0.25Sn0.75I3', 'FAPb0.875Sn0.125I3', 'FA0.46MA0.64PbBr0.24I0.76',
                             '(TFEA)2Cs0.475FA15.675MA2.85Pb20Br9.15I51.85', '(TBA)0.15Cs0.04FA0.67MA0.14PbBr0.51I2.49',
                             '(PEA)2Cs79Pb80Ix', 'FA0.97MA0.03PbBr0.09I2.91 | (MIC2)2PbI4',
                             'Cs0.09FA0.83MA0.08PbBr0.15I2.85', 'FA0.87MA0.13PbI3', 'MAIn0.20Pb0.80I3', 'nanSnI6',
                             'CsEu0.09Pb0.91BrI2', '(PMA)2MAPbI3', 'Ag4Bi9I31', 'Cs0.13FA0.72MA0.16PbBr0.51I2.49',
                             'MAPb0.4Sn0.6Br1.8I1.2', 'FA0.83MA0.17PbBr0.02I2.98', 'MACa0.03Pb0.97I3',
                             'Cs0.05FA0.85MA0.1PbBr3.0', 'FA0.15MA0.85PbBr0.45I2.55', 'MAPbBr1.14I1.86',
                             'Cs0.05FA0.79MA0.16PbBr0.5I2.5', 'MAMg0.09Pb0.91I3', 'MAHg0.15Pb0.85I3',
                             '(APMim)Pb(PF6)PF63', 'FAPb0.125Sn0.875I3', 'CsLa0.01Pb0.99BrI2', 'CsPb1.0Br3',
                             '(CHMA)2MAPbI4', 'CsPb0.98I3', 'FA0.79MA0.16PbBr0.51I2.49', 'MAPbBr2.97I0.03',
                             'MAPbBr0.3I2.7', 'Cs0.05FA0.8MA0.15PbBr0.4I2.6', '(PMA)2MA3Pb4I13', 'GUMA4Pb4I13',
                             'Cs0.03FA0.37MA0.6PbBr0.025I2.975', 'FA0.83MA0.17PbBr1.2I1.8', 'Cs0.2FA0.8PbBr0.2I2.8',
                             'MAPbBr0.87I2.13', 'FAPb0.9Sn0.1I3', 'MAGeBr0.45I2.55', 'FA0.75Sn0.25I3', 'FAPb0.5Sn0.5I',
                             'CsSnBr2I', 'MAPbBr0.14I2.86', 'Cs0.1FA0.75MA0.15PbBr0.51I2.49',
                             'Cs0.05FA0.85MA0.10PbBr0.39I2.61', 'Cs0.15FA0.71MA0.14PbBr0.9I2.1', 'FA0.4MA0.6PbI3',
                             '(PEA)0.8MA0.5PbI3.2', 'MASnBr1.8Cl0.2I', 'MABi3I10', 'MAPbBr0.083I2.92',
                             'FA0.67MA0.33PbBrI2', 'Cs0.05FA0.54MA0.41PbBr0.06I2.94', 'Cs0.17FA0.83PbBrI2',
                             'Cs0.05FA0.8MA0.15PbBr0.47I2.53', 'FA0.87MA0.13PbBr0.13I2.83', '(AVA)2PbI4 | MAPbI3',
                             'Cs0.05FA0.76GU0.075MA0.11PbBr0.39I2.61', 'Cs0.1FA0.7MA0.2PbI3',
                             'FA0.8MA0.2PbBr0.256I0.744', 'CsPb0.95I3', 'Cs0.1FA0.81MA0.09PbBr0.1I2.9', 'Cs2SnI6',
                             'FA0.85MA0.15PbBr0.46I2.54', 'FA0.75MA0.25Sn1.0I3', 'Cs0.1FA0.9SnI3', 'GU0.75MA0.25PbI3',
                             '(3AMP)FA0.45MA2.55Pb4I13', 'EA2MA3PEAPb4I13', '(DMA)0.025MA0.975PbI3',
                             'Cs0.05FA0.76MA0.19PbBr0.6I2.4', '(BDA)MAPbI4', 'Cs0.04FA0.8MA0.16PbBr0.45I2.55',
                             'Cs0.1FA0.75MA0.15Pb0.5Sn0.5Br0.5I2.5', 'FA0.5MA0.5PbI',
                             '(TBA)0.5Cs0.05FA0.75MA0.15PbBr0.51I2.49', 'Cs0.05FA0.79MA0.16PbBr0.49I2.51',
                             'FA0.59MA0.41PbI3', 'BAFA40Pb41I124', 'MASb2I9', 'Cs0.02FA0.98SnI3',
                             'Cs0.05FA0.68MA0.26Pb0.75Sn0.25Br0.4I2.6', 'FA0.79MA0.21PbI3', 'FA0.10PN0.90SnI3',
                             'FA0.2MA0.8PbBr2.4I0.6', 'CsPb0.1Sn0.9I3', 'MACu0.03Pb0.97Br0.03I2.97',
                             'Cs0.08FA0.78MA0.14PbBr0.42I2.58', 'Cs0.15FA0.71MA0.14PbBr0.6I2.4',
                             'Cs0.06FA0.78MA0.16PbBr0.18I2.82', 'FAPbBr2.25Cl0.75', 'MAPb0.95I3', 'BE2FA9Pb9I28',
                             'MAPb0.4Sn0.6Br0.4I2.6', 'FA0.83MA0.17PbBr1.5I1.5', 'Cs0.04FA0.8MA0.16PbBr0.15I0.85',
                             '(PEA)0.67MA0.33PbI3', 'Ag0.152Bi3I9.5', 'HA0.1MA0.9SnI3', 'FA0.25MA0.75SnI3',
                             '(Ace)0.02MA0.98PbI3', 'FA0.0MA0.13PbBr0.13I2.87', 'FA0.5MA0.5PbBr2.5I0.5',
                             'FA0.072MA0.928PbBrI2.86', 'Cs0.05FA0.79MA0.16PbBrI2', 'Cs0.03Pb0.97Br3',
                             'BA0.5MA0.75PbI3.25', 'FA0.4MA0.6PbBr0.025I2.975', 'Cs0.05FA0.55MA0.4PbBr2.88I0.12',
                             'FA0.7Rb0.3PbI3', 'FA0.88MA0.12PbBr0.36I2.64', 'FA0.4MA0.6PbI4', 'FAPbBr2.1Cl0.9',
                             'MA3Sb1.4Sn0.6I9', 'Cs0.0125FA0.4875MA0.5Pb0.5Sn0.5I3', '(PDMA)MA5Pb6I19', 'BA2MAPb2I6',
                             'MA0.01Mg0.01Pb0.99I3', 'Cs0.1FA0.9PbBr0.1I2.9', 'Cs0.05FA0.8MA0.15PbBr0.15I2.85',
                             'CuBiI4', 'CsPb0.9I3', 'GUMA3Pb3I12', 'Cs0.05FA0.79MA0.16SnBr0.5I2.5', 'MAPb0.97Sb0.03I3',
                             '(CHMA)2MA4Pb5I16', 'BA2MA39Pb40I121', '(PDA)0.01Cs0.15FA0.84PbI3', 'MAPb(BF4)2.95I0.05',
                             'MA3PA2Pb4I13', 'Cs0.05MA0.95PbBr0.6I2.4', 'Cs0.01Pb0.99Br3', 'EA2PbI4', 'MAPb0.97I3',
                             'MAPbBr0.07I2.97', '(F3EA)0.04BA1.96MA3Pb4I13', 'Cs0.19FA0.81PbBr0.54I2.46',
                             'FA0.6MA0.4Pb0.4Sn0.6I3', 'MANi0.1Pb0.9I3', 'CsMg0.03Pb0.97Br3', 'BA2MA3Sn4I13',
                             'Cs0.05MA0.79PbBr0.3I2.7', 'Cs0.17FA083PbBr0.6I0.24', 'MAPbI3 | (PPA)PbI4',
                             'CsPb1.0Br1.2I1.8', 'Cs0.05FA0.83MA0.12PbBr0.45I2.55', 'FA0.83MA0.17PbBr0.33I2.67',
                             'MAPb0.4Sn0.6Br0.6I2.4', 'FA0.71MA0.29PbBr0.42I2.58', 'CsEu0.01Pb0.99BrI2',
                             'BA0.52GA0.15MA0.67PbI3.33', 'Cs0.3MA0.7PbI3', 'DA2FA3Sn4I13', 'FA0.024MA0.976PbBrI2.955',
                             'MABa0.03Pb0.97I3', 'BA2Cs0.1FA2.36MA0.48Pb3Br1.7I0.83', 'Cs0.05FA0.94MA0.01PbBr0.03I2.97',
                             '(F3EA)0.2BA1.8MA3Pb4I13', 'Cs0.1FA0.9PbI3', 'BA2Cs0.08FA1.36MA2.56Pb5I16',
                             'FA0.62MA0.38PbBr0.13I2.90', 'MA2PA10Pb11I34', 'Cs0.2FA0.8SnI3', 'MAPb0.4Sn0.6Br2.4I0.6',
                             'FA0.8MA0.2PbI3', '(4ApyH)Bi0.2Sb0.8I4', 'Cs0.05FA0.75MA0.1PbBr0.3I2.9',
                             'FA0.75MA0.25PbBr0.25I2.76', 'Rb3Sb2I9', 'FA0.86MA0.15PbBr0.45I2.55',
                             'FA0.8MA0.2Pb0.5Sn0.5I3', '(iPA)3PbI5', 'Cs0.12FA0.88PbBr0.36I2.64',
                             'FA0.3MA0.7PbBr0.6I2.4', 'CsPbBr3 | MAPbI3', 'MAPb0.4Sn0.6BrI3', 'CsFAPbBrI',
                             'BA2FA2.4MA0.6PMAPbI13', 'FAPbBr2I', 'MAEu0.08Pb0.92I3', 'FA0.87MA0.13PbBr0.51I2.61',
                             'FA0.4MA0.6Pb1.0I3', 'FAPb1.0I3', 'FA0.92MA0.08PbBr0.24I2.76 | (C4H9NH3)2PbI4',
                             'FA0.73MA0.23PbBr0.13I2.89', 'FA0.6MA0.4PbBr0.256I0.744', 'FA0.8GU0.2SnI3',
                             'Cs0.005FA0.81MA0.14PbBr0.45I2.55', 'Ag0.15Bi4I11.5', '(HEA)2Cs3.9FA35.1Pb40Br12.3I110.7',
                             'CsFAPbBr0.2I2.8', '(C6H4NH2)CuCl2I', 'CsPbBr3 | CsPbBr3', 'Cs0.08FA0.76MA15PbBr0.51I2.49',
                             'Cs0.05FA0.8MA0.15PbBr0.42I2.58', 'CsPb0.99Zn0.01Br3', 'MAEu0.02Pb0.98I3', '(DMA)2PbI4',
                             'Cs0.04FA0.80MA0.16PbBr0.5I2.5', 'CsBi0.05Pb0.95I3',
                             'Cs0.05FA0.75GU0.075MA0.10PbBr0.39I2.61', 'MA2PA4Pb3I10', 'FA0.17MA0.83PbBr3', 'Cs2TiBr6',
                             'FA0.85MA0.85PbBr0.45I2.55', '(F5PEA)xCs0.15FA0.64MA0.2PbBr0.6I2.4',
                             'CsPbBrI2 | BA2CsPb2BrI6', 'Cs0.5MA0.5PbI3', 'Cs0.05FA0.79GU0.05MA0.11PbBr0.39I2.61',
                             'GUSnI3', 'FA0.3MA0.7PbBr0.3I2.9', 'Cs0.25FA0.75PbI3', 'Cs0.1FA0.85MA0.15PbBr0.45I2.55',
                             'MAPbBr0.81I2.19', 'EA2MA9Pb10I31', 'Cs0.13FA0.87PbBr0.39I2.61', 'Ba0.1K0.9Nb0.95Ni0.05O3',
                             '(AVA)0.05MA0.95PbI3', '(DMA)0.1MA0.9PbI3', 'MA3Sb2I9', 'FAPb0.6Sn0.4I3', 'BA2FAPb2I7',
                             'FA0.17MA0.83PbBr2I', 'FA0.83MA0.17PbBr0.4I2.6', 'BDACsPb2Br2.1I4.9',
                             'FA0.5MA0.5PbBr0.12I2.88', '(PMA)2CuBr4', 'FA0.3MA0.7PbBr0.48I2.52',
                             'MAPb0.25Sn0.75Br1.2I1.8', 'MAPb0.99I3', '(PEA)2MA2Pb3I10', 'Cs0.8Rb0.2SnI3',
                             'MAPb0.65Sn0.35I3', 'FAPbBr3I', '(PEA)0.8BA1.2MA3Pb4I13',
                             'FA0.85MA0.15PbBr0.45I2.55 | BAFAPbI4', '(4AMPY)MA3Pb4I13', 'CsNi0.01Pb0.99Br3',
                             '(HdA)PbI4', 'FA0.5MA0.5Pb0.75Sn0.25I3', 'FA0.6MA0.4PbBr0.3I2.9', 'MAPb1.0Cl3',
                             '(PEA)2Cs59Pb60Br60.33I120.67', 'FA0.54MA0.46PbI3', 'Cs0.05FA0.855MA0.095PbBr0.285I2.565',
                             '(BDA)MA4Pb5I16', 'CsPbBr1.9I1.1', '(PEA)2PbI4 | MA1Pb1I3 | (PEA)2PbI4',
                             'Cs0.11MA0.89PbI3', 'Cs0.06FA0.94PbBr3', 'MA2Pb(SCN)2I2', 'AgCs2BiBr5.6',
                             'MAPbI3 | BA2MA2Pb3I310', 'Cs0.06MA0.94PbI3', 'BiFeO3', 'Cs0.09FA0.91PbBr0.12I2.88',
                             'Cs0.05FA0.84MA0.11PbBr0.2I2.8', 'FA0.87MA0.13PbBr0.39I2.61',
                             'Cs0.1FA0.9PbBr0.1I2.9 | (PA)PbBr0.1I2.9', 'MAIn0.15Pb0.85I3',
                             'Cs0.05FA0.788GU0.097MA0.065PbBr0.51I2.49', 'FA0.6MA0.4Pb0.4Sn0.6Br0.3I2.7',
                             'FA0.05MA0.95PbI3', 'CsPbBr3 | CsPbBr2I', 'Cs0.35FA0.65PbI3',
                             'Cs0.05FA0.79MA0.16PbBr0.51I2.51', 'FA0.2MA0.8PbBr0.6I2.4',
                             'Cs0.06FA0.78MA0.16PbBr0.51I2.49', 'Cs0.02FA0.95MA0.03PbBr0.09I2.91',
                             'Cs0.15FA0.65MA0.20PbBr0.6I2.4', 'CsPbBr2I | CsPbI3', 'FA0.81MA0.19PbBr0.54I2.46',
                             'Cs0.1FA0.76MA0.14PbBr0.45I2.55', 'CsxFAxPbI3', 'Cs0.17FA0.83Pb0.9Sn0.1I3',
                             'MAPb0.75Sn0.25Br3', '(ImEA)PbI4', 'Cs0.01FA0.76MA0.14PbBr0.45I2.55',
                             'FA0.8MA0.2PbBr0.22I', 'Cs0.06FA0.79MA0.15PbBr1.8I1.2', 'Cs0.05FA0.5MA0.45PbBr0.04I2.96',
                             'IM0.005MA99.5PbI3', 'EA0.2MA0.8PbI3', 'Cs0.05FA0.76MA0.19PbBr0.57I2.32',
                             'CsPbBrF0.28I1.72', 'Cs0.10FA0.75MA0.15PbBr0.50I2.50',
                             'Cs0.05FA0.7885MA0.1625PbBr0.45I2.55', '(Anyl)2MA34Pb5I15', 'Cs0.5FA0.4MA0.1PbBr0.51I2.49',
                             '(BdA)PbI4', 'FASnI3', 'IM0.5MA0.50.5PbI3', 'Cs0.05FA0.81MA0.14PbBr0.51I2.49',
                             '(PEA)2FA0.85MA0.15Pb2Br1.05I5.95', 'FAPbBr0.35I2.65', 'Cs0.1FA0.75MA0.15SnBr0.5I2.5',
                             'Cs0.15FA0.255MA0.595PbI3', 'Cs3Sb2I9', 'MACo0.1Pb0.9I3', 'MASnBr0.6I2.4',
                             'FA0.33PbBr2.5I0.5', 'Cs0.80MA0.20PbI3', 'CsBa0.2Pb0.8BrI2',
                             'Cs0.16FA0.8MA0.04PbBr1.71I1.29', 'Cs0.3FA0.7PbBr0.095I0.905', 'FA0.75GU0.25SnI3',
                             'MAPb0.93I3', 'MASnBrI2', 'PAPbI3', 'MACu0.0094Pb0.9906I3', 'BA2Cs1.2FA7.65Pb4.8Sn3.6I28',
                             'Cs0.05FA0.76MA0.19PbI3', 'FAPbBrxIx', '(GABA)0.2MA0.8PbI3',
                             'Cs0.05FA0.81MA0.11PbBr0.45I2.55', '(Ace)0.05MA0.95PbI3', 'FAPbBr2Cl', 'MAPbBr0.3I2.9',
                             'Cs0.1FA0.78MA0.13PbI3', 'GU2PbI4', '(ALA)0.2BA1.8MA3Pb4I13', 'Ag3BiI6',
                             'Cs0.05FA0.83MA0.12PbBr0.39I2.61', 'FAPbBr2.5I0.5', 'BA2Cs0.15FA0.85Pb1.2Sn0.8I7',
                             'Cs0.05FA0.95PbI3', '(EDA)0.015FA0.29MA0.695Pb1.0I3', '(PEA)1.6BA0.4MA3Pb4I13',
                             'nannannan', '(PEA)2FA8Sn9I28', 'CsPb0.9Zn0.1Br2I', 'Cs0.05FA0.79MA0.16Pb1.1Br0.51I2.49',
                             'FAPb3Br6I', 'MAPbBr0.8I2.2', 'FA0.125MA0.875PbI', 'Cs0.1FA0.83MA0.17PbBr0.51I2.49',
                             'MAPb0.95Sr0.05I3', 'MAPbBr0.015I2.985', 'FA0.3MA0.7PbBr0.54I2.46',
                             'FA0.84MA0.16PbBr0.45I2.55', 'Cs0.2FA0.664MA0.336PbBr1.05I1.95', 'MAPbI3 | (PPEA)PbI4',
                             'MAPb0.9Zn0.1I3', 'Cs0.4FA0.6PbBr0.095I0.905', 'CsGeI3', 'FA0.85MA0.15PbBr0.55I2.45',
                             'FA0.83MA0.17PbBr0.50I2.50', 'MACo0.4Pb0.6I3', 'Ag0.153Bi3I10.5',
                             'MAPbI3 | Cs1Pb1I3 | Cs1Pb1Br0.3I2.7 | CsPbBr0.7I2.3', 'Cs0.05FA0.45MA0.5Pb0.5Sn0.5I3',
                             'Cs0.08FA0.8MA0.12PbBr0.36I2.64', 'CsPbBrI', 'Cs0.05FA0.85MA0.1PbBr0.45I2.45',
                             'Cs0.15FA0.51MA0.34PbI3', 'Cs0.1FA0.9PbBr0.51I2.49', 'FA0.4MA0.6PbBr1.8I1.2',
                             'IM0.01MA0.99PbI3', '(PDMA)PbI4', 'MACu0.05Pb0.85Sn0.1Br0.1I2.9', 'FA0.6MA0.4PbBr0.1I2.9',
                             'MA3Bi2I12', 'FA0.85PbBr0.08I2.92', 'FA0.5MA0.5PbSnI3', 'MAPb0.5Sn0.500I3',
                             '(PEA)1.4BA0.6FA3Sn4I13', 'FA0.25MA0.75PbBr0.12I2.88', 'EA0.1MA0.9PbI3', 'BAPbI4',
                             'Cs0.94Li0.06PbBr3', 'Cs0.05FA0.79MA0.16PbBr0.51I2.49', 'MAPbBr0.05I2.95',
                             'Cs0.17FA0.83PbBr0.8I2.2', 'Cs0.07FA0.77MA0.16PbBr0.50I2.50', 'MAPb0.9Sn0.1Br0.2I2.8',
                             'MANiCl2I', 'Cs0.2668FA0.666MA0.0664PbBr0.256I0.744', 'Cs0.17FA0.83PbBr0.75I2.25',
                             'Cs0.70FA0.30PbI3', 'Cs0.05FA0.79MA0.16PbBr1.2I1.8',
                             'Cs0.0664FA0.8668MA0.0664PbBr0.256I0.744', 'FA0.5MA0.5PbBr0.13I2.87',
                             'FA0.85MA0.15PbBr0.51I2.49', 'Cs0.2FA0.8PbBr0.36I2.64', '(PEA)0.33MA0.67PbI3',
                             'Cs0.1FA0.74MA0.13PbBr0.39I2.48', 'Cs0.05FA0.7885MA0.1615PbBr1.2I1.8',
                             'Cs0.05FA0.38MA0.57PbI3', 'Cs0.03MA0.97PbBr0.09I2.91', 'CsPbBr2I', 'FA0.1MA0.9PbBr2.7I0.3',
                             'MAPb0.85Sb0.15I3', 'Cs0.05FA0.80MA0.15PbBr0.45I2.55', '(PEA)2MA3Pb4I13',
                             'MACo0.031Pb0.969I3', 'Cs0.03FA0.91Rb0.05PbI3', 'FA0.85MA0.15PbBr0.45I2.55',
                             'FA0.3MA0.7PbBr0.9I2.1', 'MASnBr1.5I1.5', 'FA0.75MA0.25PbBr0.25I2.78', 'MAPbBr2.13I0.87',
                             'Cs0.05FA0.93MA0.11PbBr0.40I2.6', 'Cs0.17FA0.83PbBr0.51I2.49', 'Cs0.24FA0.76PbBrI',
                             'CsBi0.01Pb0.99I3', 'MAHg0.3Pb0.7I3', '(PEA)0.05MA0.95PbBr1.2I1.8',
                             'FA0.6MA0.4Pb0.4Sn0.6Br0.24I2.76', 'FA0.6MA0.4Pb1.0I3', 'FA0.75MA0.25PbBr0.5I2.5',
                             'Cs0.05FA0.79MA016PbBr0.5I2.5', 'BA2FAMA2.64Pb5I16',
                             'Cs0.2FA0.66MA0.14Pb0.75Sn0.25Br0.5I2.5', 'Cs0.15FA0.25MA0.6PbI3', 'BA2MA6Pb7I22',
                             'Cs0.05FA0.79MA0.16PbBr0.31I2.7', 'Cs0.88FA0.12PbI3', 'Cs0.17FA0.83PbBr1.2I1.8',
                             'Cs0.05FA0.79MA0.16PbBr0.50I2.5', 'FA0.85MA0.15PbBr0.45I2.55 | BA2FAPbI4',
                             'Cs0.1FA0.77MA0.13PbBr0.39I2.48', '(HEA)2Cs1.9FA17.1Pb20Br12.6I57.54', '(4FPEA)2MA4Pb5I16',
                             'Cs0.05FA0.80MA0.15PbBr0.33I2.67', 'CsPbBr2.9I0.1', 'BAMA2Pb2I7', 'FA0.33MA0.67PbI3',
                             'MAHg0.025Pb0.975I3', 'Cs0.1FAxMAxPbBrxIx', 'Cs0.03FA0.945MA0.025PbBr0.075I2.925',
                             'MAPbBr2.16I0.84', 'BAFA60Pb61I184', 'FA0.67MA0.33PbBr2.5I0.5', '(PEA)0.12BA0.9MA3Pb4I13',
                             'Cs0.05FA0.7885MA0.1615PbBr0.4845I2.51555', 'MAPbBr0.226I2.774', 'FA0.48MA0.52PbI3',
                             'FASnBr0.75I2.25', 'MAPb(BF4)0.05I2.95', '(THM)0.2MA0.8PbI3', 'CsPb0.95Sr0.05BrI2',
                             '(BEA)0.5Cs0.15FA2.36MA0.48Pb3Br1.7I0.83', 'Cs0.125FA0.75MA0.125PbBr0.33I2.67',
                             'BA2MA3PbI4', 'Cs0.17FA0.83Pb0.95Sn0.05I3', 'Cs0.3FA0.7PbBr0.15I2.85', 'FA0.33PbBr2I',
                             'MAPb0Sn0.19I3', 'IM0.6MA0.60.4PbI3', 'FA0.76MA0.15PbBr0.48I2.42',
                             'Cs0.05FA0.85MA0.1PbBr0.3I2.7', 'Cs0.04FA0.92MA0.04PbI3', 'Cs0.1FA0.9PbBr0.256I0.744',
                             'Cs0.02FA0.98PbBr3', 'FAPb0.25Sn0.75I3', 'MAPb0.98Sb0.02I3',
                             'FA0.92MA0.08PbBr0.24I2.76 | (C6H13NH3)2PbI4', 'MACa0.1Pb0.9I3', '(CIEA)0.01MA0.99PbI3',
                             'MAPbBrxIx', 'MAPbBr0.9I', 'MAPb0.125Sn0.875I3', 'Cs0.05FAPbI3', 'FA0.25MA0.75PbI3',
                             'Cs0.05FA0.16MA0.79PbBr0.51I2.49', 'Cs0.17FA0.83PbBr0.15I2.85',
                             'FA0.66MA0.34PbBr0.42I2.58', 'Cs0.05FA0.795MA0.16PbBr0.51I2.5',
                             'Cs0.05FA0.79MA0.16PbBr0.16I0.84', 'FA0.44MA0.56PbBr0.33I2.67', 'HA0.3MA0.7SnI3',
                             'AgCs1.8Rb0.2BiBr6', 'Cs0.02FA0.38MA0.6PbBr0.025I2.975', 'Cs0.3MA0.7Pb0.5Sn0.5I3',
                             'MAPbBr0.066I2.93', 'MAPb0.875Sn0.125I3', 'Cs0.06FA0.84MA0.10PbBr0.41I2.59',
                             'Cs0.17FA0.83PbBr0.4I2.6', 'FA0.8MA0.2PbBr0.13I2.88', 'nanBi2FeCrO6',
                             'Cs0.05FA0.79MA0.16Pb0.664Sn0.336Br0.52I2.48', 'Cs0.05FA0.747K0.05MA0.153PbBr0.51I2.49',
                             '(NH4)3Sb2Br9', '(PDA)0.02Cs0.15FA0.83PbI3', 'CsSnBr3', 'CsBiI4', 'FA0.2MA0.8PbBr0.3I2.7',
                             '(TBA)0.05MA0.95PbI3', 'MAPbBr0.03I2.97', 'CsBi0.025Pb0.975I3', 'Cs0.91Rb0.09PbBr3',
                             'Cs0.4FA0.6PbBr1.05I1.95', 'MAPb0.999Sb0.001I3', 'Cs0.08FA0.69MA0.23PbBr0.63I2.37',
                             'Bi0.95La0.05FeO3', '(PEA)0.25(F5PEA)0.75PbI4', 'Cs0.2FA0.65MA0.15PbBr0.55I2.55',
                             'FA0.57MA0.43PbBr0.39I2.61', 'Cs0.05FA0.79MA0.17PbBr0.51I2.49', 'MAPbI3 | BA2PbI4',
                             'BA2FA60Pb61Br4I180', '(PDA)2MA3Pb4I13', 'CsFAPbI3', 'CsFAPbBr3I',
                             'Cs0.08FA0.55MA0.37PbI3', 'Cs0.05FA0.8MA0.15PbBr0.45I2.55', 'Cs0.05FA0.7885MA0.1615PbBrI2',
                             'Cs0.08MA0.92PbI3', '(BzDA)Cs0.45FA7.2MA1.35Pb10Br2.17I28.83', 'FA0.95TN0.05SnI3',
                             'FA0.17MA0.83PbI3', '(PEA)0.05MA0.95PbI3', 'Cs0.05FA0.82MA0.13PbBr0.45I2.55',
                             'EDA0.01FA0.99SnI3', 'Cs0.05FA0.90MA0.05PbBr0.15I2.85', 'Cs0.1FA0.76MA0.14PbBr0.55I2.55',
                             'Cs0.2FA0.75MA0.05PbBr0.33I2.67', '(PEI)2MA4Pb5I16', 'Cs0.05FA0.8265MA0.1235PbBr0.39I2.61',
                             'Cs0.06FA0.83MA0.17PbBr0.51I0.249', 'AN0.03MA0.97PbI3', 'BA2MA8Pb9I28',
                             'Cs0.05FA0.79MA0.16PbI3 | NMABrPbIBr', 'Cs0.17FA0.83PbBr1.2I2.8', 'CsPb2Br5',
                             'MAPbBr1.25I75', 'Cs0.1FA0.9PbBr0.315I2.685', 'HA2MA2Pb3I10', 'IM0.15MA0.150.85PbI3',
                             'Cs0.14FA0.86PbBr0.27I2.29', 'FA0.85MA0.15PbI3', 'Cs0.05FA0.09MA0.05PbBr0.15I2.85',
                             'BA0.67MA0.67PbI3.33', 'FA0.87MA0.13PbBr0.5I2.5', 'FA0.33PbBr0.5I2.5', 'MAPb3I3',
                             'MA0.05Mg0.05Pb0.95I3', '(NH4)1.7FA0.15MA2.04Pb2.7Br0.45I8.84', 'CsxMAxPbxBrxIx',
                             'FAPbBr0.256I0.744', 'FASnBr0.5I2.5', 'Cs0.1FA0.75MA0.24PbBr0.51I2.49', 'MABa0.05Pb0.95I3',
                             'MAPbI3 | (MIC2)2PbI4', 'Cs0.17FA0.87PbBr0.36I2.64', 'Cs0.2FA0.8PbBr0.75I2.25',
                             '(PEA)2Cs4MA35Pb40I121', 'Cs0.03FA0.81MA0.16PbBr0.50I2.50',
                             'Cs0.1FA0.747MA0.153PbBr0.51I2.49', 'AN0.1MA0.9PbI3', 'MA0.5PA0.5PbI3',
                             'Cs0.05FA0.83MA0.17PbBr0.39I2.61', 'FA0.6MA0.4PbBr0.095I0.905',
                             '(TFEA)2Cs0.725FA23.925MA4.35Pb29Br13.65I77.35', 'FA0.12MA0.88PbBr0.25I2.75',
                             '(PEA)2MA4Pb4I13', 'Cs2AgBiBr6', 'CsPb1.0BrI2', 'Cs0.60MA0.40PbI3', '(PDMA)FA3Pb4I13',
                             '(EDA)0.02FA0.29MA0.69Pb1.0I3', 'BA2Cs0.45FA2.55Pb2.4Sn1.8I14', 'Cs0.1FA0.9MAPbI3',
                             '(PEA)0.4FA0.6PbI3', '(TFEA)2Cs0.975FA32.175MA5.85Pb40Br18.15I102.85',
                             'Cs0.01FA0.39MA0.6PbBr0.025I2.975', 'IA0.05MA0.95PbI3', 'Cs0.15EA0.75FA0.1PbBr0.3I2.7',
                             'Cs0.05FA0.75MA0.15Rb0.05PbI3', 'FA0.25MA0.75PbBr0.25I2.75',
                             'Cs0.017FA0.83MA0.15PbBr0.51I2.49', 'FA0.1MA0.9PbI3 | (A43)2PbI4',
                             'Cs0.11FA0.89PbBr0.18I2.82', 'Cs0.05FA0.79MA0.15PbBr0.51I2.49', 'Cs0.25FA0.75Pb0.5Sn0.5I3',
                             'CsPb0.85I3', 'BA0.1Cs0.15FA0.75PbBr0.3I2.7', 'FA0.92MA0.08PbBr0.24I2.76',
                             'CsFAPbBr0.3I2.7', 'IM0.1MA0.10.9PbI3', 'MAPb1.0Br0.33I2.66', 'Cs0.2FA0.8Pb0.5Sn0.5I3',
                             'MACa0.05Pb0.95I3', 'FAPbI3 | CsPbI3', 'Cs0.05FA0.7885MA0.1615PbBr0.45I2.55'])))

    composition_assumption = Quantity(
        type=str,
        shape=[],
        description="""
    The knowledge base from which the perovskite composition is inferred. Is the assumed perovskite composition based on the composition of the precursor solutions and the assumption that the final perovskite will have the same composition (i.e. Solution composition), or is it based on literature claims (i.e. Literature) or has it been experimentally verified with some technique, e.g. XRD, EDX, XRF, etc.?
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(
                suggestions=['', 'Literature', 'Solution composition | XRD', 'TEM', 'XPS', 'Solution composition',
                             'Solution composition | Solution composition', 'EDX', 'Experimental verification',
                             'XRD'])))

    composition_inorganic = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if the perovskite does not contain any organic ions.
                    """,
        a_eln=dict(
            component='BoolEditQuantity'))

    composition_leadfree = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if the perovskite is completely lead free.
                    """,
        a_eln=dict(
            component='BoolEditQuantity'))

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
            component='EnumEditQuantity', props=dict(
                suggestions=['', '4-Aminophenyl Boronic acrid; Cl', 'FABr', 'BMImI; LiI; L-iTFSI',
                             'Cl; Phosphatidylcholine', 'PLMF', 'Cl | ZnCl2', 'DACl', 'CH3CONH2', 'rGO-g-Ptet',
                             '(PEY)2PbI4', 'oxo-G/DA', 'MEH-PPV; TBP', 'PbI2-bipyridine', '1,10-diiododecane; Cl',
                             'AA; Cl', 'NiI2', 'Benzenamine hydrochloride', 'BrPh-Thr; bis-PCBM', 'HCOOH', 'OctAm',
                             'CsPbI3', 'CH2CHCH2 (CC2)-ionic liquid', 'Polyethylenimines (PEIs), MW 600', 'EP-PDI',
                             'EtOH; MA', 'EDACl2', 'Cl; PTAI', 'bis-DMEC60', 'DMF', 'CuBr', 'Cl; PEO', 'Tb', 'ILPF6',
                             'KIPIG-500', 'Cl; K; Sn', '1‐methyl‐3‐(1H,1H,2H,2H‐tridecafluorooctyl)‐imidazolium iodide',
                             'SCN; SnF2', 'Cl; PbS-np', 'NbF5', 'PbF2', 'PEI', 'n-butyl amine', 'Cl; MDACl2', 'NaI',
                             'PF-0', 'Cl; DPE', 'methylammonium hypophosphite; L-α-phosphatidylcholine; PEABr', 'PVDF',
                             'SrI2', 'Starch', 'P(VDF-TrFE)', 'C8Br; Cl', 'GU(SCN)', 'PCBB-OEG', 'C4H10INO2; Cl',
                             'ITIC', 'NH4I', 'Carbazole-C4', 'Polystyrene', 'CsAc', 'BMIm', 'SCN', 'FACl; SnF2',
                             'BaAc2', 'PMM', '1‐butyl‐3‐methylimidazolium bromide', 'RbBr', 'PVAm.HI', 'C16H36BrN',
                             'PPC', 'organicD‐pi‐A', 'p-phenylenediamine', 'Pyrrole', 'TPA', 'Cl; CNT-NH2', 'Cl; CuI',
                             'Cl; CuPc(tBU)4', 'HPbI3 | Cl', 'Undoped | Undoped', '1,4-dibromobutane; Cl', 'CuBr2; RbI',
                             'PABA∙HI', 'PPAI', 'In; Br', 'Cl; Spiro', 'Rubrene', 'PbAc2; H2O', 'PCBM-60', 'Ni', 'Ag',
                             'CuBr2; CsI', 'EDA; SnF2', 'ASCl; Cl', 'Cl; SrCl2', 'Mg',
                             '1,8- Diazabicyclo[5.4.0]undec-7-ene', 'Melanin', 'HoNH3Cl', 'MACl, NMP | Undoped',
                             'AsI3 | NH4Cl', 'Cs', 'Isatin-Cl', 'KSCN', 'TPE-DPP4', 'Phenylammonium; HI', 'DCL97',
                             'MoS2', 'PPS', 'P25', 'MABr; MACl', '1‐butyl‐3‐methylimidazolium iodide', 'Caprolactam',
                             'Cl; Urea', 'BAOAc', 'AgI', 'TEP', 'Cl; EAI', 'CSA', 'HPA; Pb(AcO)2', 'InCl3', 'DMA',
                             'C60', 'HI; HBr', 'Cl; PNVF–NVE', 'Phosphonic acid', 'BAI', 'Aminobenzonitrile', 'C3N5',
                             'MAPbBr3-QDs', 'Cl; Cu(Tiurea)I', 'Cl; Hypophosphorous acid', 'MPTS; Cl', 'Imidazole',
                             'Cl; I2', 'C60; PMMA', '(adamantan‐1‐yl)methanammonium; HI', 'Hl', 'UiO', 'ABA',
                             'Cl; PCBM', 'PEG-[60]fullerenes', 'p-Si-np', '5-AVAI; CuSCN', 'Cl; Formamidineacetate',
                             'HMTA', 'Cl; NH4Cl; CuBr2', 'Acetate; HPA', 'Pb(OAC)2', 'Urea', 'Cl; Thiourea', 'MgI',
                             'FeOOH-QDs', 'ZnI', 'C3H7NH3I; Cl', 'FAAc', 'TBA', 'L-alfa-phosphatidylcholine', 'NaOAc',
                             'Co(Ac)2', 'CPTS; Cl', '(SnF2(DMSO))2', 'PEA2PbI4', 'RbI',
                             'Polyethylenimines (PEIs), MW 70000', 'PTAA',
                             '2‐(6‐bromo‐1,3‐dioxo‐1H ‐benzo[de ]isoquinolin‐2(3H )‐yl)ethan‐1‐ammonium iodide',
                             'Hexamethylphosphoramide', 'CsPbBr3-np', 'Cl; PEG-NH2', 'DRCN5T', 'Carbonnanowalls',
                             'HaHc', 'Diethylamine hydrochloride', 'PEO', 'Mn', 'Hexylamine hydrochlorid', 'C6Br; Cl',
                             'NMP', 'poly(ethyleneimine); Carbon-nt', 'b-PEI; Cl', 'Ti', 'Sr', 'PbCl2; KCl', 'MACl',
                             '1,4-diiodobutane; Cl', 'BYK333', 'BP-QDs', 'C6H14INO2; Cl', 'exMMT', 'Spiro',
                             'Lead acetate', 'CEA', 'Cl; Au-CZTS', 'PbI2', 'Methylpyrrolidone', 'H2P2O6', 'C-PCBOD',
                             'IEICO-4F', 'GaAA3', 'beta-cyclodextrin', 'n-butyl amine; Cl', 'P123',
                             'tetra-tert-butyl-metal free phthalocyanine', 'PEG; Cl', 'HMImCl', 'Pb(DDTC)2',
                             'EDAl2; SnF2', 'Anilinium Iodide', 'MA(SCN)', 'PS; PMMA', '5-AVAI; PCBM-60', 'E-g-C3N4-np',
                             'D-alanine', 'Acetate', 'YD2-o-C8', '4-ABPACl', 'PDMAI', 'PVA', 'FIm',
                             '3-Aminophenyl Boronic acrid; Cl', 'Polyethyleneglycol; Polyvinylpyrrolidone',
                             'EtOH; H20; Pb(SCN)2', 'Polyurethane', '1-butyl-4-amino-1,2,4-triazoliumiodine', 'CuSCN',
                             'DPSI', 'Glycine', 'GUBr', 'p-CH3OC6H4; p-t-BuC6H4', 'MA', 'Nd', 'Cl; TPPI', 'MACl, NMP',
                             'GAI', 'Er', 'ZnPc', 'Pb(CH3CH2COO)2', 'Tetracyanoquinodimethane', 'PPA', 'KIPIG-600',
                             'PTS | Cl', 'Piperazin; SnF2', 'CH2I2', 'Cl; Liquid crystals', 'MOF', 'CuBr2; NaI',
                             'YbAc3', 'NiCl2', 'Butylammonium iodide', 'Cl; INIC2', 'TTABr', 'HI; PEAI',
                             'Melaminium iodine', 'Lysine', 'Yttrium', 'MAPbI3-QDs', 'DMBI-2-Th',
                             '1,3:2,4-di-O-dimethylbenzylidene-d-sorbitol', 'Ag@SiO2-nw', 'Poly(styrene-co-butadiene)',
                             'E2CA', 'Cl; MAH2PO2', 'KIPIG-550', 'Benzoic acid hydroiodide', 'Cl; DRCN5T',
                             'Guanidinium', '5-AVAI; Formamide', 'Guanidinium-SCN', 'SA-2',
                             '1-ethyl-4-amino-1,2,4-triazoliumiodine', 'SnCl2', '1,6-diaminohexane dihydrochloride',
                             'DOI', 'CaI2', 'Cl; DIO', 'CNDs@K', 'Cl; CsF', 'PCBPEG-4k', 'CdI2', 'CsPbBr3', 'TPPCl',
                             'Cl; DMF', 'APSA', '1‐butyl‐3‐methylimidazolium chloride', 'Cl; PEI', 'pyr-fullerene',
                             'tetrabutylammonium chloride', 'DMBI-2-Th-I', 'Sm(acac)3', 'CH3I; Cl', 'Rb', 'PAI',
                             'SrCl2 | MACl', 'ZnO-np', 'NiO',
                             'MACl; poly[9,9-bis(3′-(N,N-dimethylamino)-\npropyl)-2,7-fluorene)-alt-2,7-(9,9-dioctylfluorene)]) (PFN-P1) in chlorobenzene; PFN-P2 (in ethanol',
                             'OTG1', 'DF-C60; SnF2', 'PF-1', 'Undoped | Mn', 'BiI3', 'Li', 'MABr', 'PbCl2', 'MACSN',
                             'TBAI3', 'HATNA', 'IBr', 'MXene', 'AuAg@SiO-np', 'Cl; H2O', 'P(EO/EP)',
                             'Protic ionic liquid', 'Cl; HI', 'Cl; InCl3', '5-AVAI; HBF4', 'Formamide; PEA',
                             'Li-TFSI; TBP', 'AVAI', 'Cl; Cu:NiO-np; Graphite', 'MOF-525', 'Rb; Thiourea',
                             'Li-TFSI; LiF; TBP', 'DMAI', 'NMA', 'SQ63', 'Cl', 'NH4Ac', '1,8-octanedithiol',
                             'Hydrazinium chloride; SnF2', 'Butylamineiodide', 'FAI',
                             'tetra-tert-butyl‑silicon phthalocyanine bis(trihexylsilyloxide)', 'S-Carbon-nt', 'HPbI3',
                             'NaF', 'BCP', 'DETAI3', 'H2O; Pb(SCN)2', 'Cl; TBAB', 'C6H5C2H4NH3',
                             'Diphenylidonium hexafluoroarsenate; PCBOD', 'NO3', 'Eu', 'Butanediaminedihydroiodide',
                             'PEACl', 'PbAc', 'FU11', 'Phenylethylammonium iodide', 'rGO-g-PDDT', 'Ag-nw', 'Graphdiyne',
                             'Chitosan', 'H2O; KI', 'C4F8I2', '1-ethylpyridinium chloride', 'SWCNTs', 'CNT', 'DMEC60',
                             'J71', 'MACl; PbBr2', '2Ph-ox', 'NEP', 'LiBr', '4-fluorophenylethylammine',
                             '1-octyl-4-amino-1,2,4-triazoliumiodine', 'PCBM-70', 'PMPS', 'DMI', 'Diiodomethane',
                             'PEOXA', 'InCl2', 'Yb', 'PDAI', 'CuI2', 'MAAc', 'SrCl2',
                             'Side-chain liquid crystalline polymer (SCLCP)', 'SnF2; TMA', 'Cl; I3', 'A43', 'K; Rb',
                             'Al; Cl', 'OTG2',
                             'methylammonium hypophosphite (MHP); L-α-phosphatidylcholine (LP); 1,3-diaminopropane (DAP)',
                             'BEA', 'TiO2-np', 'Acetic acid; HCl; n-propylamin; Pb(Ac)2', 'C4Br; Cl', 'C60-PYP',
                             'Ethane\xad1,2\xaddiammonium', 'Pb(NO3)2', 'ASA', 'CB', 'Li-TFSI', 'BiFeO3-np',
                             'Carbon-np; Urea', 'PE10', 'GA', 'BTA; SnF2',
                             'methylammonium hypophosphite; L-α-phosphatidylcholine; PEACl', 'TMA', 'SnF2',
                             'CuCl; PbCl2', 'Poly(amicacid)', 'Cl; RbBr', 'PbC2O4', 'Thiourea', 'LiI', 'Graphdiyne-QDs',
                             'terephthalonitile', 'As; NH4; Cl', 'FACl', 'NH4Cl; DMSO', 'Cl | nan', 'Acetonitrile',
                             '2-(1H-pyrazol-1-yl)pyridine', 'GITC', 'TDZT', 'HCl',
                             'N-methyl-2-(3,5-bis(perfluorooctyl)phenyl)-3,4-fulleropyrrolidine', 'MAPbBr3',
                             'SmI2; SnF2', 'HI; Mercapto-tetrazolium', 'TiI2', 'GuaI', 'Cl; PEG', 'Carbon-nt-g-P3HT',
                             'Cl; Fe(acac)3', 'NaYF4:Yb:Er-np', '5-AVAI; Cl', 'CsBr',
                             'Hydrophosphoric acid; rGO; PbAc2', 'N-Carbon-QDs', 'MAH2PO2', 'PTMA-H; Rb', 'F127',
                             'Black Phophorous', 'GeI2', 'PCBM-60; PbF4', 'GuCl', 'L-α- phosphatidylcholine',
                             'CsPbBrCl2-QDs', 'Ag-NPs', '2-pyridylthiourea', 'EtOH', '1-Donecyl Mercaptan',
                             'Au@Ag@SiO2-np', 'PFPA', 'PbS-QDs-AI-ligand', 'DIO', 'H2PO3', 'Cl; ZnO-np', 'Polyimide',
                             'EDAI2 | SnF2', 'NaCl', 'CsPbr3', 'I3', 'EDA', 'CH3SH', 'Cl; IPFB', 'Ti3C2Tx',
                             'Methylammonium formate', 'MACl; PFN-P2 (in ethanol', 'Cl; NH4Cl', 'Cl; NH4Br',
                             'HPbI3; PTABr', 'tetra-tert-butyl‑germanium naphthalocyanine bis(trihexylsilyloxide)',
                             'PE', 'NH4SCN', 'Phenylethyl-ammonium iodide', 'Acetamidine hydrochloride',
                             'Polythiocyanogen', 'Cl; Guanidinium', '3,4-dihydroxybenzhydrazide; MACl', 'KCl', 'Sm',
                             'CH2CCH (CC3)-ionic liquid', 'GASCN', 'TBAI; Cl', 'Cl; HCOOH', 'Octoxynol', 'PEA5',
                             'Cl; Formamide; Guadinium', 'n-BAI; Rb', '5F-PCDM-60', 'CuI; PbCl2', 'Au@TiO2 NPs', 'TOPO',
                             'Cl; Cu(thiourea)Cl', 'PbF4', 'M13 bacteriophage', 'OAc', 'PVC', 'EAPP', 'CH2O2; SnF2',
                             'SbCl3', 'n-Si-np', 'Trimesic acid', 'CsCl', 'Acetate; SrI2', 'N-cyclohexyl-2-pyrrolidone',
                             'DPP-DTT', 'Hydrazine', 'KHQSA', 'Butylated hydroxytoluene', 'RbI; KI', 'Acetate; HAc',
                             'Ethyl cellulose; Cl', 'Cl; TBAC', 'C2H6INO2; Cl', 'FeI2', '4-MSA', 't-BAI', 'Cu',
                             '1,2,4-triazole', 'Zn', 'KBr', '3F-PCBM-60', 'Cl; Eu(acac)3', 'Cl; Cu(thiourea)I', 'TDZDT',
                             'Acetate; Cl', 'Polyvinylalkolhol', 'Agarose', 'Cl; KI', 'PMA', '3BBAI; Cl',
                             'Thenolytrifluoroacetone', 'Cl; PCBM-60', 'Cl; PCBM-60; PEG', 'HBr', 'MLAI', '5-AVAI',
                             'PVDF-HFP', 'Cl; HI; KOH', 'D3', 'Cl; KBr', 'Cl; PNVF-NVEE Microgels', 'PVA; SnF2',
                             'Undoped', 'C6F5I', 'PTAI', 'Cl; EA۰HCl', 'Rb; SrI2', 'g-C3N4', 'Carbon', 'DEACl', 'MAI',
                             'EACl', 'C3A; PEA', 'THTO', 'Acetate; H2O; Hypophosphorous acid', 'Adipic acid; Cl',
                             '3-aminopropyl (3-oxobutanoic acid) functionalized silica nanoparticles; Cl',
                             'OA; ODE; OLA', 'D1', 'CHP', 'SA-1', 'Ethylene‐diammonium; SnF2', '1,8-dibromooctane; Cl',
                             'GN-GQDs', 'BMImI; LiI', 'ZnI2', 'h-TAc', 'F4-TCNQ', 'A10C60', 'Ca', 'Ag; Cl; rGO',
                             'Cl; HBr', 'PEABr', 'MQW', 'Cl; NO3', 'Mn; Cl', 'PDMS', 'H2O; KCl', 'Cl; MAAc', 'BMIMBF4',
                             'C60(QM)2', 'PMMA; PbCl2', 'H3PO2; Acetate', 'PANI', 'Acetic acid', 'Al2O3-np', 'PC', 'Ce',
                             'PEG', 'Caffeine', 'SQ45', '3-phenyl-2-propen-1-amine iodide', 'HBr; Hi', 'SQ81', 'MnCl2',
                             'Monoammonium zinc porphyrin', '1,8-diiodooctane', 'BMImI', 'Cl; DMSO',
                             'Cl; DL-tartaricacid', 'CDTA; SnF2', 'ThMAI', 'I', 'TPPi', 'Imidazolium', 'FEAI',
                             '1-hexyl-3-methylimidazoliumchloride; HMImCl', 'EuCl3', 'Octylammonium iodide', 'CHCl',
                             'Dithizone', '4-vinylbenzylammonium', 'H2O; TEOS', 'Cl; Formic acid', 'iPAI',
                             '1,3-diaminopropane', 'p-phtalic acid', 'Cl; NH3SO3', 'Lu', 'H2O; Ti3C2Tx', 'Cl; TBPI',
                             'Cl; NiO-np', 'Rhodanina', 'CH3COCHCOCH3', 'MAOAc', 'Cl; SDS', 'Cu:NiO-np', 'SP-3D-COF 2',
                             'CU(SCN)', 'Cl; ITIC', 'Cl; PEDOT:PSS', 'PbAc2; PbCl2', 'PAA', 'Carbon-np',
                             'alfa-cyclodextrin', 'Eu-pyP', 'MWCNTs', 'TSC', 'Cl; Diiodooctan', 'CsBr; Cl', 'BHT',
                             'Unknown', 'SbBr', 'Cl; HCl', 'PbS-QDs-MAI-ligand', 'N2H5Cl', 'Si-nc', 'Octylammonium',
                             '1-hexyl-3-methylimidazoliumchloride', 'PMMA; Rb', 'CH3NH2',
                             '4-(1H-imidazol-3-ium-3-yl) butane-1-sulfonate', 'ligands', 'N-methylimidazole', 'DIFA',
                             'Formamide', 'Styrene', 'YbCl3', 'K', 'MeO-PEAI', 'BrPh-ThR', 'OA; OLA', 'SnF2; Uric Acid',
                             'SnCl', 'Cl; TBP', 'tetra-ammonium zinc porphyrin', 'Ho', 'Graphene', 'Carbon-nt-g-PDDT',
                             'PFPAI', 'Graphitic carbin nitride (g-C3N4)', 'Cl; PAA', 'TEOS', 'Cl; KCl', 'Carbon-nt',
                             'F-PEAI', 'J61', 'Ethyl cellulose', 'Ethyleneglycol', 'Citric acid; Cl',
                             'Cl; Pb(SCN)2; SnF2', 'D2', 'pyP', 'In', 'dimethyl itaconate', 'GdF3', 'BAI; PEG',
                             'Formic acid', 'Cl; PCDTBT', 'Nb', 'GABr; Pb(SCN)2', 'APPA', 'H2O', 'Ag@SiO2', 'NH4Br',
                             'gamma-cyclodextrin', 'Ba', 'PEAI', 'J51', 'N2200', 'DNA', 'TiO2-nw', 'A@SiO2-np-nw; Cl',
                             'Graphene-nanofibers', 'Methylamine', 'G-NH2', 'BaCl2; Cl', 'GASCN; MACl', 'SnF2; TFEACl',
                             'Polyacrylonitrile', 'Acetic acid; Cl', 'La', 'LFA', '[BMMIm]Cl', 'PCBPEG-20k',
                             'B-alanine', 'NH2CONH2', 'P(VDF-TrFE-CTFE)', 'Polyvinylbutyral', 'Graphene oxide', 'EAI',
                             'C70', 'C4H8I2', 'Cesium phenethyl xanthate', 'NH4Ac2', 'Benzylamine hydroiodide', 'LiCl',
                             'FPEAI', 'GuaSCN; SnF2', 'PbS-np', 'Hydroquinone', 'CuI', 'enI2; SnF2', 'Cl; PbS', 'PMMA',
                             'H2O; KBr', 'HC(NH2)2I–NaI', 'PbC2N2S2', 'g-CN', '1,8-octanedithiol; Cl', 'Cellulose-CDHC',
                             'HMPA', 'rGO-g-P3HT', 'Cellulose-HEC', 'Gd', 'NaSCN', 'NH4Cl; NH4SCN', 'PA', 'TACl',
                             'I2; Thiourea', 'CsPbBr3-nw', 'Benzene‐1,4‐diboronic acid; Cl',
                             'methylammonium hypophosphite; L-α-phosphatidylcholine', 'MABF4', 'Co', 'BA; HI; HBr',
                             'Cl; PVP', 'IPA HCl', 'CaCl2', 'F-N2200', 'CuCl2', 'Ag; Cl', 'TCA', 'TBP', 'CuBr2; KI',
                             'Cl; CuSCN', 'Benzoquinone', 'KI', 'Al2O3-np; Cl', 'Isobutylamine hydroiodide',
                             'Graphene-QDs', 'MAPbCl3', '2,9,16,23-tetra-tert-butyl-29H,31H-phthalocyanine',
                             'Formamide; Guadinium', 'Bi', 'Cl; Y', 'NiO-np', 'GuI', '1,8-diiodooctane; Cl',
                             'SP-3D-COF 1', 'Cl; Cu', 'rGO', 'HBr; HI', 'HA', 'OAm', 'Cl; Graphene', 'Nano-carbon',
                             'HAc', 'PEA20', 'ACN', 'Hypophosphorous acid', 'Cl; TPPCl', 'IPFB; PbCl2', 'CsPbBr-np',
                             'MgAc', 'PEA0', 'In2-6', 'FPEAI; Mn', 'Cl; Y(acac)3', 'Cl; NH4I', 'ZnCl2', 'CsI', 'TiO2',
                             'Polyethylenimines (PEIs), MW 10000', 'Diiodooctane', 'PbS-QDs',
                             'Phenylethyl ammonium iodide', '3-(5-Mercapto-1H-tetrazol-1-yl)benzenaminium iodide; HI',
                             'CdS; Cd(SCN2H4)2Cl2', 'PbAc tri-hydrate; H3PO2', 'MA3Bi2Br9', 'BmPyPhB', 'Ag-rGO; Cl',
                             'CdS', 'Cl; DMA', 'Methimazole', '2-Phenylethylamine Hydroiodide', 'Ba; Cl', 'BAI; GAI',
                             'Az', 'Cl; C-PCBSD', 'Diethylammoniumchloride; PCBM-60', 'hypophosphorous acid',
                             'CH2CN (CN)-ionic liquid', 'ITIC-Th', 'PbCl2; Phenol', 'False', 'Br',
                             'Cl; NAP 1-(3-aminopropylpyrrolidine)', 'Cd', 'Carbon-QDs', 'PTMA; Rb', 'Cl; DTA', 'g-CNI',
                             'Sn', 'PCBM-nw', '5-AVAI; Acetamide', 'Cl; CZTS', 'MnCl2; ZnCl2', 'Cl; MA', 'Cl; SCN',
                             'ITIC; PCBM-60', 'NH4OAc', 'NH4Cl; SnF2', 'Au-np', 'TMS', 'PVP', 'Cl; MoOx-np', 'NaAc',
                             'Benzoicacid', 'FAOAc', 'Tea Polyphenol', 'Cl; Sr', 'Carbon-nt; PDDT', 'DOI; PbCl2',
                             'Nickel phtalocyanine', 'OAI', '5-AVAI; Urea', 'n-butylammoniumbromide', 'en; SnF2',
                             'PbCl2; Phosphatidylcholine', 'NH4Cl', 'CQD', 'Pb(OAc)2', 'Levulinic acid', 'EC', 'PbSCN2',
                             'KI; I2', 'In2-4', 'NH4BF4', 'EDEA', 'Hydrophosphoric acid; PbAc2', 'Graphdyine', 'TOAB',
                             'OTAB', 'Pb(SCN)2; SnF2', 'Diethylammoniumchloride', 'Tetraethylorthosilicate',
                             'trihydrazine dihydriodide (THDH)', 'DA2PbI4', 'Cl; DL-lacticacid',
                             'l-alfa-phosphatidylcholine; Methylammoniumhypophosphite; NH4Cl', 'HI | Undoped',
                             'Graphdiyne QDs', 'Lead acetate trihydrate', 'PEAI; SnF2', 'BE2PbI4', 'Cl; FAH', 'ABS',
                             'PbCl2; TBP', 'PS', 'CsI; OIH', 'J50', 'NH4F', 'acac; Cl', '3DHG', 'BA', 'PEA; SnF2',
                             'Pb(Ac)2', 'OTG3', 'NH4H2PO2', 'PEA', 'Eu(Ac)3', 'Acetate; H2O',
                             '1-allyl-3-methylimidazolium chloride', 'H3PO2', 'EE', 'NO3-C3N4', 'Cl; MWCNTs', 'BCP; Cl',
                             'Zr(AC)4', 'Terephthalic acid', 'SnS-QDs', '1-benzyl-3-methylimidazolium chloride', 'Sb',
                             'Cl; TPPBr', 'di-iodomethane', 'NH4', 'ZnAc2', 'Ethylenediammonium', 'Cl; DL-malicacid',
                             'Thiosemicarbazide', 'Guanidinium; HI', 'ETI',
                             'Phosphonic acid; Aluminium acetylacetonate', '1,3:2,4-di-O-methylbenzylidene-d-sorbitol',
                             'CH3CH2COO', 'SbI3', 'SnBr2', 'xDMAI', 'Cl; SrAl2O4:Eu2+:Dy3+', 'CuBr; PbCl2', 'MACL',
                             'Cl; SnF2', 'PTN-Br; SnF2', 'SnI2', 'bis-PCBM', 'HI', 'BMII', 'HPA', 'In2-2',
                             'Poly(diallyldimethylammoniumchloride)', 'Cl; K', 'I2', 'ME', 'Pyrazine; SnF2', 'DPPS',
                             'Ascorbic acid', 'PbAc2', 'CuBr2', 'IDTBR', 'PbCl2; PbAc2', 'Cl; ICBA', 'Carbon-nt; P3HT',
                             'P(VDF-TrFE-CFE)', 'BaI2', 'ALAI; Cl', 'TMTA',
                             'Formamidinium chloride; formamidinium hypophosphite; Phenylethylammonium chloride',
                             'DMSO', 'NaYF4:Tb:Er-np', 'Cl; NH4Cl; CuBr', 'PTB7', 'SnF2; PMMA', 'Pb(SCN)2',
                             'l-alfa-phosphatidylcholine; Methylammoniumhypophosphite', 'DAGCl',
                             '1-chloronaphthalene; Cl', 'Acetate; HCl', 'CdCl2', 'Cl; V2Ox', 'Cl; IEICO-4F',
                             '1-chloronaphthalene', 'C70; Cl', 'a-Ge; Cl; H-np',
                             'methylammonium hypophosphite; L-α-phosphatidylcholine; PEAI', 'C4H9NH3I; Cl', 'C-PANI',
                             'MAI; FACl', 'PU', 'TFBA'])))

    additives_concentrations = Quantity(
        type=str,
        shape=[],
        description="""
    The concentration of the dopants/additives.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- If more than one dopant/additive in the layer, e.g. A and B, separate the concentration for each dopant/additive with semicolons, as in (A; B)
- For each dopant/additive in the layer, state the concentration.
- The order of the dopants/additives must be the same as in the previous filed.
- For layers with no dopants/additives, state this as ‘none’
- When concentrations are unknown, state that as ‘nan’
- Concentrations can be stated in different units suited for different situations. Therefore, specify the unit used.
- The preferred way to state the concentration of a dopant/additive is to refer to the amount in the final product, i.e. the material in the layer. When possible, use on the preferred units
o wt%, mol%, vol%, ppt, ppm, ppb
- When the concentration of the dopant/additive in the final product is unknown, but where the concentration of the dopant/additive in the solution is known, state that concentration instead. When possible, use on the preferred units
o M, mM, molal; g/ml, mg/ml, µg/ml
- For values with uncertainties, state the best estimate, e.g write 4 wt% and not 3-5 wt%.
Example
4 wt%
5 vol%; nan | 10 mg/ml
0.3 mol% | 2 mol%; 0.2 wt% | 0.3 M
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(
                suggestions=['', '0.25 wt%', '0.125', '0.225', '24 mg/ml', '0.025; nan', '0.35', '2 %; 0.1 %',
                             '0.66; 0.0875', '2', '0.0775', '0.005', '0.0207', '0.05 %', '0.1 M; 10 wt%', '5 vol%',
                             '0.1 mol', '0.005 M', '0.057', '0.003; nan', '6 mol%; 10 mol%', '0.22', '0.6 mg/ml; nan',
                             'nan; 1', '3.7 wt%', '0.36', '0.099', 'nan; 8 mol%', '0.6 vol%', '0.03 M', '5.6 vol%; nan',
                             '2.6', ' PEG', '2.5 wt%; 0.5 wt%', '0.1666666666666667', '0.03125', '0.035; 1.5 vol%',
                             '0.002 mg/ml', '8 %; 4 %33%', '0.0003 mmol/ml', '0.3 vol%', '3.3 %; nan', '2.5 vol%',
                             '0.2 mol%; 10 mol%', '0.18', '0.0001 mol%', '0.01 mol%', '0.515 M', '0.07', '20 µmol/ml',
                             '2.5 wt%; 1.5 wt%', '0.9 wt%', '0.006', '0.5 mg/perovskite_mmol', '30 mmolL-1', '0.000525',
                             '2.5 wt%; 0.25 wt%', '0.321; 0.009', '0.05', '2.4', '0.00167', 'nan; 5 %', '0.4 wt.%',
                             '0.05 wt%', '6.4', '1.05', '0.04; 0.17', '0.0125', '0.3 mg/perovskite_mmol',
                             '2.5 wt%; 0.35 wt%', '8', '0.084', '10 vol%', '0.05 %; nan', '0.0001 mmol/ml',
                             '0.035; 3 mg/ml', '0.0007', '0.03; 0.02', '0.0625 \u202c', '1.0', '0.14', '10 wt%',
                             '0.16; 0.5', '60 mol%', 'nan | 20 mg/ml', '0.00068', 'nan | 13 mg/ml', 'nan; 4 mol%',
                             '0.02', '1.2 mg/ml; 20 mg/ml', 'nan | 27 mg/ml', '0.0003', '0.333; 0.009', '3.9 vol%',
                             '0.4; 0.01', '0.7', '0.9 mg/ml; 15 mg/ml', '6 mol%; 20 mol%', '0.05; nan', '0.66; 1',
                             '0.04; 0.0015', 'nan; 0.66 %', '0.034; 0.034', '3 mg/ml; nan', '15; 10',
                             '50 mg/ml; 1 mg/ml', '0.3 mg/ml', '6.8 e-05', '0.03 mM; 0.09 mM', '0.048', '1.2 M',
                             '0.312; 0.018', '3 mg/ml', '0.0005 mmol/ml', '0.005 wt%', '4.5', '0.1 vol%', 'nan; 0.0125',
                             '60 mol% | 6 mg/ml', 'nan; 0.0166 %', '0.336', '150 mol%', '12 wt%', '10 %; 7.5 %',
                             'nan | 5 mg/ml', '4 mg/ml; nan', '3 %; nan', '0.9 mM', '30 mM', '0.03 vol%', '12.8',
                             '10 ppm', '0.089 mg/ml', '0.5 wt%', '10 g/ml', '0.06 mg/ml', '0.13 wt%', '0.028; nan',
                             '2.5 %; 10 %', 'nan; 1.0', '0.1; 0.15', '15 %; 7.5 %', '8.0', 'nan; 1 wt%', '23 mol%',
                             '0.006; 0.05', '6 mg/ml', 'nan; 1 mg/ml', '15 mg/ml', '0.262 M', '0.02 M', 'nan; 20 %',
                             '0.09', '0.45', '0.016', '1 ppm', '7 mol%', '0.333', '5 mg/ml; nan', '0.0085', '0.5 wt.%',
                             '0.09375', '0.15 wt%; 0.05 wt%; 0.42 mol%', '5 mol%; 20 mg/ml', '2.0 wt%', '50 mol%',
                             '5 wt%', '50', '5 %; nan', '2 wt.%', '4 mg/ml; 4 mg/ml; 4 mg/ml', '2.3', '0.05 M', '0.03',
                             '0.0034', '16 vol%', '15 wt%', '0.01 ug/ml', '2.5 wt%; 0.3 wt%', 'nan; 0.02', '0.10 wt%',
                             'nan | 0.05 mol%', '6 mM', '50 vol%', '8 mol%', '0.66; 0.08', '0.1 mol%', '1.3',
                             '0.035; 30 mg/ml', '1.2 wt%', '0.5; 0.5', '12 mM', '0.00075', '3.5 m%', '12 mg/ml',
                             '0.0175', '4 µmol/ml', '5- AVAI', '12.5 wt%', '0.042', '18 mM', '5 %; 0.1 %', '0.6 mg/ml',
                             '3.3 vol%', '0.6 wt%', '0.097 mol%', '0.5 %; nan', '0.66; 0.075', '0.0026344676180021956',
                             'nan; 10 mg/ml', '0.05 vol%', '4 mg/ml', 'nan; 9 mM', '0.5 M', '0.0004', 'nan; 114 mM',
                             '0.05; 0.15', '1.5 %; 6 %', '0.3 M', '20 mg/ml', '0.04; 0.003', '100 ppm', '7 mg/ml',
                             'nan; 1 %', 'nan; 0.1 mg/ml', 'nan | 0.1 mol%', '2.5 wt%; 0.2 wt%', '6 µmol/ml',
                             '7.5 mol%', '0.018; nan', '0.5 vol%', '0.08', '2 wt%', '0.04 %', '0.025',
                             '10 mmg/perovskite_mmol', 'nan; 0.033 %', 'nan; 0.2 mg/ml', '0.014 mol%', '0.3', '12.5',
                             '0.59 uM', '0.12', '0.0285 vol% | nan', '0.0076', '0.015 M', '0.06', '10 %; 20 %',
                             'nan; 0.015', '1 e-05', '6 wt%', '0.10; 0.01', '75 vol%', '10 mg/ml', '0.4 mg/ml',
                             'nan; 0.15 %', '0.25 mM', '5.69 vol%', '3.5 vol%', '0.75; nan', '0.66; 1; 0.0075',
                             'nan; 2 mg/ml', 'nan; 0.33 %', 'nan; 0.00166 %', '0.0125; 0.05', '1.35', '8 %; nan',
                             '1000 ppm', '16.67 %; nan', '2.5 wt%; 0.1 wt%', '0.08 mg/ml', '0.125; 20 mg/ml',
                             'nan; 0.0075', '2.5', '90 mol%', 'nan; 2 wt%', '1.5 mol%', '2 mg/mlantisolvent',
                             '25 mg/ml', '0.0011', '0.15; 0.15', '0.0015', '20 vol%', 'nan; 4 %', '15 mol%; 10 mol%',
                             '0.075; nan', '6', '1.25; nan', 'nan; 2', '0.35; 0.019', '0.02; 0.03', '0.4 mM',
                             '50 mg/ml; nan', '8 vol%', '5 %; 7.5 %', '0.3 mol', '0.006; nan', '0.25', 'nan; 18 mM',
                             '2.5 mg/ml', '0.09; nan; nan', '1 wt%; nan', '2 vol%', '0.01 | 0.1', 'nan; 1.5',
                             'nan | 0.2 mol%', '0.017', '0.01 vol%', '7.5', '0.009', '13.7 mg/ml', '0.027',
                             '0.25; 0.04', '0.15; 0.15; 0.004', '6.67', '30 wt%', 'nan; 0.005', '1.0 wt%', '1 %; 0.1 %',
                             '0.48 mg/ml; nan', '5 mol%', '0.067 mol%', 'nan; 36 mM', '0.9', 'nan; 0.5', '0.011',
                             '0.035', '0.4 wt%', '0.004', '0.33; 0.33', '6 %; nan', '0.04; 0.0001875', 'nan; 0.025',
                             'nan; 0.05', '100 mol%', 'nan; 5 mol%', '0.75; 0.25', '20 uL', '0.0375', '1.67 mol%',
                             '0.14 M', '3 wt%', '0.01; 0.05', '4 %; nan', '0.0028', '0.15; 0.075', '0.07 wt%', '1; nan',
                             'nan | 0.5 mol%', '0.35; 0.057', '0.0002', 'nan; 2 %', '0.8 M', '3.5 mol%; 10 mol%',
                             '25 vol%', '0.04; 0.000375', '10 µmol/ml', '0.15; 0.025', '0.5 mg/m', '0.8', '25', '9',
                             '16 mg/ml', '6 e-05', '0.5; nan', '2 mol%; 2 mol%', '1', '0.33; 0.003', '0.064',
                             '0.6 wt.%', '5.0', '0.1; 0.02', 'nan; 3 %', '0.6', '0.66; 0.0625', '0.84 vol%; nan',
                             '1.25 mg/ml', '76 mg/ml', '15 µmol/ml', '0.20; 0.15', 'nan | 2.5 mol%', 'nan; 0.54 %',
                             '0.1 mg/perovskite_mmol', '12 mg/ml; 12 mg/ml; 12 mg/ml', '0.2', '0.24 mg/ml; nan',
                             'nan; 1.66 %', '5 mg/ml', '1 mol%', '2 mg/ml; nan', '100 vol%', '1.5', '0.33', '0.00035',
                             '0.167', '0.284', '2.0', 'nan; 9', '1 mg/ml; nan', 'nan; 1.5 mg/ml', '0.00067', '1 e-06',
                             '5 mol%; 10 mol%', 'nan; 10 mol%', '0.003', '0.66; 0.016', '0.66', 'nan; 72 mM',
                             '3.5 mol%', '0.05 | nan', '0.018', '12 mg/ml; 12 mg/ml', '0.0010537870472008782', '0.4',
                             '0.0112', '0.012', '0.1 mg/ml', '0.5; 0.16', '0.26', '4 wt%', '0.02 mg/ml',
                             'nan; 0.54 %; 0.11 %', '0.034; 0.05', '2.8 mol%', '8 mg/ml', '100', '0.075', '0.077',
                             '0.0615; 0.0185', '0.764 M', 'nan; 1.5 %', '8 µmol/ml', '0.6 mol%', '0.25; 0.75', '0.15',
                             '0.032', '2.5 wt%', 'nan; 7 %', '0.3 mM', '0.5 mg/mlantisolvent', '0.014; nan', '40 mol%',
                             'nan; 0.25 %', '0.125 mol%', '3.6 vol%', '42.9', '0.05; 0.1', '0.5', '0.46', '20; 10',
                             '5.268935236004391 e-05', '4 mol%', 'nan; 0.03', '0.0008', '0.00026344676180021956',
                             '0.00027', '3 mol%; 10 mol%', '0.66; 0.1', 'nan; 0.125 %', 'nan; 3 wt%', 'nan; 0.5 mg/ml',
                             '0.0075', '0.3 wt%', '0.04', '3', '3.0', '3.2', '2.5 wt%; 0.4 wt%', 'nan; 0.01',
                             '0.39999999999999997', '0.3 mg/ml; 5 mg/ml', '1.009 M', '3 vol%', '0.034 mol%',
                             '0.16666666666666666', '0.023', '0.6 M', '0.333; 0.003', '0.25 mg/ml', '0.07 mol%',
                             '0.03 wt%', '0.003; 0.05', '50 mM', '5; 10', 'nan; 2.5 %', '0.126', '2 mg/ml', '9.6',
                             'nan; 0.2', '0.001', '0.063', '2.0 mg/ml', '0.15; 0.05', '30 mg/ml', '30 mol%', '0.21',
                             '0.05 mg/ml', '0.05; nan; nan', '0.5 mol%', '0.031', '0.2 mg/ml', '0.0035', '0.75.0.01',
                             '0.01 M', '0.75 M', '0.8 mg/ml', '1 mol%; 10 mol%', 'nan; 4 wt%', '0.11', '0.1 mM',
                             '29 wt%', '16.67', '0.66; 0.05', 'nan; 0.75', '40 wt%', '0.5 mmol', '0.01; nan', '1.4 %5%',
                             '0.04; 0.00075', '4.2 vol%', '1 wt%', '6.0', '0.008', '2 %; nan', '0.23', 'nan; 0.048 %',
                             'nan; 0.1 %', '0.66; 0.04', 'nan; 0.3 mg/ml', 'nan; 4 mg/ml', '1.5 mg/ml', '50 mg/ml',
                             '15 mol%', '0.67', '12.5 mM', '2 wt%; nan', '5 g/ml', '2.5 wt%; 3 wt%', '0.0005', '1 mM',
                             '33.3', '750 vol%', 'nan | 0.0003', '0.0056', '1 M', '15.0', '6.6 mol%', '1.00 wt%',
                             '1 %; nan', '0.66; 0.01', '0.000285 mol%', '25 mol%', '0.1; 0.005', 'nan; 3 mol%',
                             '0.17500000000000002', '0.002', '0.15000000000000002', '1.4 vol%; nan', '2 µmol/ml',
                             '2.5 mol%', '0.10; 0.15', '0.9 M', '0.034', '3 mol%', '0.1; 0.075', '33 ul.57wt%',
                             '1 mg/ml', '4 vol%', '0.0005268935236004391', '0.17', '0.068', '75', 'nan; 0.5 %',
                             '2.21 wt%', '1.3 %; nan', '2 e-05', '0.15 wt%; 0.05 wt%', '1.4 %; 6 %', '0.1; 0.1',
                             '10; 10', '0.01', '0.25; nan', '6 mol%', '0.028; 0.0003', '20 wt%', '0.014', '0.1',
                             '5 mol%; 10 mg/ml', '0.079', 'nan; 4', '1.5 wt%; 1.0 wt%; 0.15 wt%; nan', '8 wt%', '0.28',
                             '0.13', '0.033', '0.8 vol%', '1.2 wt.%', '9 mg/ml', '0.1; nan', '0.075 wt%', '8 %; 33 %',
                             '3 mM', '10 mol%', 'nan; 2 %; 6 %', 'nan; 10 %', '0.1; 0.01', '10.0', '0.125; 40 mg/ml',
                             '0.024', '2.5 wt%; 0.15 wt%', '0.5 mg/ml', '2 mol%', '20', '0.14 mg/ml', '0.75 mol%',
                             '0.00010537870472008782', '0.1; 0.03', '0.015', '1.2 mg/ml', '0.57', '7.5 g/ml',
                             '0.01 wt%', '9 mol%', '0.19', 'nan; 0.4 mg/ml', '0.071', '350', '0.35; 0.038', '200 mol%',
                             '2.5 mol%; 10 mol%', '0.14 mol%', '0.15 wt%; 0.05 wt%; 0.83 mol%', '4', '0.1; 0.04',
                             '0.0068', '10', '0.25 mol%', '0.045', '20 mol%', '150 vol%', '0.15 M', '0.66; 0.16',
                             '0.2 wt%', '0.1; 0.05', 'nan; 5', '2 %; 2 %', '1 vol%', '2.8 vol%; nan', '0.66; 0.008',
                             '0.6 mg/ml; 10 mg/ml', '2.5 g/ml', 'nan; 2.0', '0.2 mol', '0.01; 0.04', '0.375',
                             '0.001; 0.05', '12', '0.055', 'nan | 1 mol%', '0.1 M', '0.03; nan', '1 mg/perovskite_mmol',
                             '0.03; 0.003', '0.8 wt.%', '0.029', '0.142', 'nan; 0.4', '0.04 M', '0.07500000000000001',
                             'nan; 7', '0.000175', '1.6', '0.0001', '0.1 wt%', '0.02; nan', '7.8 mg/ml',
                             '10 mol%; 10 mol%', '1.75 mM', '1 %; 10 %', '5', '0.333; 0.018', '0.005; nan', '1.5 wt%',
                             '0.15 wt%; 0.05 wt%; 1.67 mol%', '0.15; 0.1', '0.021', '0.1 w%', '60', '0.005 vol%',
                             'nan; 0.3', '0.12 mg/ml; nan', '0.04; 0.01', 'nan; 0.1', '0.4; 0.7', '1.61 e-05',
                             '3 %; 3 %', '70 mol%', '0.02 wt%', '7.5 W%', '0.75', '0.009; nan', '0.04 mg/ml', '0.0025',
                             '2.4 mol%', '33 mol%', '1.8 mg/ml', '0.77'])))

    thickness = Quantity(
        type=str,
        shape=[],
        description="""
    The thickness of the perovskite layer
- If the perovskite contains more than one layer, separate those by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- State thicknesses in nm
- Every layer in the stack have a thickness. If it is unknown, state this as ‘nan’
- If there are uncertainties, state the best estimate, e.g write 100 and not 90-110
- For cells where the perovskite infiltrates a mesoporous scaffold, state the thickness as starting from the bottom of the infiltrated mesoporous layer to the top of the perovskite layer (i.e. include the thickness of the infiltrated mesoporous layer)
Example
200
500 |20
600 | nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', '90.0', '446.0', '325.0', '50.0', '220.0', '520.0', '137.0', '180.0', '45.0', '167.0', '668.0', '387.0', '191.0', '540.0', '353.0', '515.0', '233.0', '601.0', '354.9', '560.0', '461.0', '1020.0', '391.0', '297.0', '6000.0', '385.0', '1800.0', '107.0', '212.0', '95.0', '0.05', '760.0', '551.0', '274.0', '70.0', '447.0', '573.0', '500.0', '306.0', '275.0', '1300.0', '524.0', '2000.0', '788.0', '665.6', '54.0', '507.0', '484.0', '266.1', '291.0', '260.0', '175.0', '630.0', '1410.0', '267.0', '283.0', '455.0', '240.0', '615.0', '303.0', '150.0 | 200.0', '3600.0', '330.0', '810.0', '89.8', '775.0', '334.0', '408.0', '420.0', '26.0', '5500000.0', '85.0', '321.0', '1015.0', '463.0', '505.0', '150.0 | 500.0', '895.0', '354.0', '620.0', '709.0', '278.0', '56.0', '269.4', '650.0', '500.0 | nan', '126.0', '52.0', '20.0', '295.0', '165.0', '135.7', '265.0', '1400.0', '287.0', '372.0', '685.0', '1100.0', '359.0', '150.0 | 300.0', '602.3', '314.0', '238.0', '250.0', '229.0', '375.0', '142.0', '2130.0', '65.0', '399.0', '317.0', '875.0', '150.0', '435.0', '464.0', '379.7', '769.0', '273.0', '12000.0', '610.0', '363.0', '965.0', '880.0', '247.0', '244.0', '50000.0', '302.2', '35.0', '750.0', '468.0', '135.0', '600.0 | 20.0', '730.0', '339.0', '870.0', '258.0', '324.0', '309.4', '183.0', '481.0', '660.0', '457.0', '407.0', '342.0', '336.0', '285.0', '401.0', '25.0', '294.0', '983.0', '3100.0', '172.5', '405.0', '40.0', '67.0', '230.0', '522.0', '75.0', '334.2', '272.0', '288.0', '577.0', '331.0', '150.0 | 400.0', '480.0', '298.0', '190.0', '604.0', '365.0', '301.0', '223.0', '380.0', '700.0', '93.0', '575.0', '155.0', '529.0', '780.0', '217.0', '314.8', '599.8', '280.0', '60.0', '125.0', '465.0', '3370.0', '40000.0', '440.0', '900.0', '122.0', '400.0', '950.0', '572.0', '538.0', '510.0', '296.0', '840.0', '315.0', '498.0', '121.0', '242.0', '425.0', '512.0', '213.0', '600.0', '850.0', '100.0', '105.0', '740.0', '720.0', '485.0', '1150.0', '252.0', '417.0', '607.0', '459.3', '526.0', '511.4', '338.0', '690.0', '200.0', '453.0', '350.0', '104.0', '290.0', '195.0', '311.0', '890.0', '585.0', 'nan | nan', '547.0', '340.0', '202.0', '596.0', '160.0', '209.0', '38.0', '584.0', '653.0', '270.0', '170.0', '390.0 | 10.0', '337.0', '670.0', '151.0', '326.0', '24500.0', '386.0', '1205.0', '725.0', '171.0', '413.0', '445.0', '248.0', '640.0', '2080.0', '355.0', '150.0 | 100.0', '394.0', '765.0', '293.0', '478.0', '1130.0', '563.0', '550.0', '531.0', '215.0', '542.0', '300.0', '513.6', '245.0', '430.0', '1010.0', '395.0', '185.0', '308.0', '289.0', '530.0', '120.0', '450.0', '501.0', '218.0', '153.0', '130.0', '110.0', '310.0', '150.0 | 600.0', '141.0', '199.0', '11000.0', '490.0', '345.0', '580.0', '1000.0', '232.6', '188.0', '66.0', '225.0', '235.0', '60000.0', '528.0', '590.0', '770.0', '1200.0', '444.0', '845.0', '473.0', '1070.0', '390.0', '10.0', '43.0', '1650.0', '1393.0', '236.0', '266.0', '742.6', '412.0', '20000.0', '210.0', '397.0', '357.0', '424.0', '2200.0', '567.0', '800.0', '586.0', '525.0', '388.0', '378.0', '370.0', '129.0', '348.0', '960.0', '149.0', '477.0', '570.0', '487.0', '454.0', '7000.0', '97.0', '410.0', '30.0', '462.0', '510.2', '792.0', '360.0', '470.0', '335.0', '680.0', '438.0', '460.0', '224.0', '400.0 | 2.0', '147.0', '474.0', '1510.0', '140.0', '578.0', '492.0', '80.0', '404.0', '320.0', '4000.0', '138.0', '448.0', '10000.0', '226.0', '276.0'])))

    band_gap = Quantity(
        type=str,
        shape=[],
        description="""
    The band gap of the perovskite
- If the perovskite contains more than one layer, separate the band gaps for the respective layer by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- If there are uncertainties, state the best estimate, e.g. write 1.62 and not 1.6-1.64
Example
1.62
1.57 | 2.3
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', '1.764', '1.189', '1.516', '2', '1.578', '1.645', '1.583', '2.115', '1.715', '1.621', '2.44', '1.533', '1.486', '1.481', '2.6', '1.555', '1.73', '1.63 | nan', '1.633', '1.61', '2.04', '1.595', '2.78', '1.617', '1.526', '2.296', '1.626', '2.4', '1.72', '1.46', '1.613', '1.47', '1.91 | 1.8', '1.79', '1.623', '2.37', '1.17', '2.27', '2.42', '1.608', '1.515', '1.855', '1.525', '1.8', '1.56', '2.2', '1.605', '1.632', '1.523', '1.671', '1.503', '1.27', '2.13', '1.569', '1.684', '1.881', '1.635', '1.597', '1.627', '1.652', '2.43', '2.28', '1.775', '2.277', '1.588', '1.88', '3.04', '2.09', '1.655', '2.9', '2.3', '2.07', '2.31', '1.58', '2.38', '1.57', '1.3', '2.49', '1.901', '1.641', '1.55', '1.89', '1.66', '1.556', '1.546', '1.94', '1.498', '1.49', '1.77', '2.92', '2.12', '1.64', '1.45', '1.919', '1.549', '1.76', '1.33', '1.41', '2.39', '1.584', '1.579', '1.638', '1.592', '1.624', '1.965', '1.65', '1.26', '1.656', '1.644', '1.596', '1.906', '1.598', '1.54', '1.35', '1.21', '1.96', '2.5', '1.51', '2.268', '2.01', '2.273', '2.278', '1.674', '2.161', '1.865', '2.154', '1.99', '1.71', '1.683', '1.739', '1.78', '1.36', '1.848', '2.23', '2.19', '1.924', '1.92', '1.599', '1.872', '1.564', '1.582', '1.791', '1.612', '2.66', '2.153', '1.69', '1.565', '1.651', '2.46', '1.839', '2.14', '1.895', '1.589', '2.26', '2.36', '2.15', '1.812', '1.87', '1.548', '1.4', '1.5', '2.25', '2.027', '2.0', '1.594', '1.9', '1.581', '1.591', '1.28', '2.287', '2.48', '1.614', '1.39', '1.58 | 2.08', '1.86', '1.68', '1.25', '1.576', '1.575', '1.629', '1.375', '1.74', '1.16', '1.38', '1.957', '1.667', '1.609', '1.7', '1.557', '1.604', '2.139', '2.033', '1.602', '1.97', '2.34', '1.896', '1.634', '1.586', '1.2', '1.85', '1.535', '2.05', '1.18', '1.553', '2.21', '2.7', '1.607', '2.47', '1.606', '1.529', '1.639', '1.611', '1.752', '1.688', '1.32', '1.93', '2.22', '1.75', '1.616', '1.574', '2.308', '1.524', '1.23', '1.976', '1.845', '1.59', '2.105', '2.03', '1.725', '1.676', '2.18', '1.672', '1.34', '1.682', '2.1', '1.662', '2.54', '2.536', '2.8', '1.53', '2.113', '1.531', '1.505', '1.858', '1.67', '1.528', '2.35', '1.585', '1.751', '1.63', '1.52', '1.615', '2.02', '1.571', '1.866', '1.42', '1.619', '1.272', '1.573', '1.777', '1.893', '1.746', '1.517', '1.84', '1.509', '1.889', '1.31', '1.636', '1.628', '1.48', '1.62', '1.29', '1.82', '1.95', '1.668', '1.969', '1.91', '1.512', '1.593', '2.83', '2.141', '1.6 | 1.68', '2.29', '2.24', '2.08', '1.22', '2.288', '1.6', '1.587', '2.58', '1.757', '2.52', '1.98', '2.55', '1.37', '1.974', '1.989', '1.43', '1.24', '1.625', '1.701', '1.554', '1.637', '1.44', '2.17', '1.81', '2.32', '1.558', '2.33', '1.83'])))

    band_gap_graded = Quantity(
        type=str,
        shape=[],
        description="""
    TRUE if the band gap varies as a function of the vertical position in the perovskite layer.
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['true', 'false'])))

    band_gap_estimation_basis = Quantity(
        type=str,
        shape=[],
        description="""
    The method by which the band gap was estimated. The band gap can be estimated from absorption data, EQE-data, UPS-data, or it can be estimated based on literature values for the recipe, or it could be inferred from the composition and what we know of similar but not identical compositions.
Example
Absorption Tauc-plot
Literature
Composition
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(
                suggestions=['', 'Composition', 'Literature', 'EQE', 'Absorption', 'Absorption Tauc-plot', 'UPS',
                             'Absorption Tauc-plot | UPS'])))

    pl_max = Quantity(
        type=str,
        shape=[],
        description="""
    The maximum from steady-state PL measurements
- If more than one PL-max, separate those by a semicolon
Example
780
550; 770
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(
                suggestions=['', '779.8', '795', '520.0', '761.0', '632.6', '779.0', '695', '828.0', '728', '782.0',
                             '582.1', '589', '772', '952', '553', '540.0', '774.5', '825', '610', '1.61', '560.0',
                             '731', '767', '722.0', '640', '729', '746', '659.5', '781.5', '760.0', '819', '544', '716',
                             '786.7', '590.4', '824', '683', '708.5', '758.5', '746.0', '788.0', '538', 'nan | 740',
                             '795.0', '757.0', '793', '602', '518', '543.8', '626', '673', '794.8', '790', '813', '770',
                             '805.5', '763.5', '934.0', '819.5', '595', '663.1', '830', '715.4', '762', '884', '744',
                             '540', '810.0', '775.0', '762.5', '761', '724.0', '800.8', '766', '765.4', '777.0', '719',
                             '570', '727', '918.0', '815.8', '890', '774.0', '780.3', '825.0', '806', '817', '580',
                             '620.0', '820.0', '910.0', '625', '650.0', '803', '538.2', '781.3', '760.4', '775.4',
                             '799', '882', '754.0', '965', '932', '538.6', '584.9', '755.6', '770.1', '531', '573',
                             '976', '644.0', '632', '667', '810', '718', '755', '654', '767.1', '794', '692', '828',
                             '636.0', '798', '636', '729.4', '777', '752.0', '778.8', '769.0', '539.1', '870', '723.0',
                             '715', '639.1', '465', '741', '587.6', '685', '778', '880.0', '769.9', '764.8', '784',
                             '716.0', '751', '728.0', '614', '780', '804', '751.0', '723', '736.0', '838', '722',
                             '750.0', '776.2', '805.0', '730.0', '801.8', '529', '870.0', '764', '549', '833', '771.2',
                             '769.4', '832', '743.5', '946.0', '915', '900', '639', '768.8', '807.0', '767.0', '551',
                             '630', '984.0', '691', '635', '595.0', '843.5', '525', '735', '638', '635.8', '913',
                             '657.0', '778.0', '757.5', '786', '637', '804.3', '759.0', '731.0', '783', '746.9', '661',
                             '799.0', '300', '624', '943', '704.5', '807', '1005', '642', '677.5', '537.3', '732',
                             '877', '672.0', '800', '894', '692.0', '713', '700.0', '537.4', '686', '22.3', '748',
                             '780.0', '712', '558.0', '772.0', '552', '766.0', '797', '750', '645', '1200', '0',
                             '533.0', '805', '756.6', '996.4', '726.0', '440.0', '605', '670.2', '750 | nan', '868',
                             '526', '725', '720.9', '771.8', '743', '541', '771', '530', '796', '761.4', '680', '802',
                             '682', '575', '754', '832.2', '690', '550', '657', '722.1', '515', '512.0', '985.7',
                             '600.0', '699', '740.0', '740', '822', '753.0', '633', '720.0', '977', '785', '765', '959',
                             '880', '811', '527.0', '769', '975', '961', '775.6', '655', '840', '600', '912', '650',
                             '752', '790.0', '873', '725.1', '535', '583', '896', '539', '806.0', '950', '704', '546',
                             '812', '787', '755.0', '620', '820', '962', '774', '768.0', '670.0', '643', '200', '759',
                             '920', '778; 710', '543.0', '77', '708', '789', '964', '545', '768.3', '725.0', '769.1',
                             '1025', '843', '982', '615', '532', '506', '710.0', '764.0', '664.0', '445.0', '756',
                             '765.0', '865', '785.3', '647.0', '21.4', '675', '649.4', '550.0', '531.0', '834', '763',
                             '781', '726', '756.7', '596', '490', '707', '530.0', '805.1', '779', '527', '1058', '960',
                             '714', '719.0', '969', '889', '792', '420', '666.6', '520', '541.4', '758.0', '576.7',
                             '751.5', '946', '955', '757', '809', '730', '1020', '815', '528.0', '770.0', '802.0',
                             '781.1', '894.0', '651', '753', '724', '652', '767.9', '627', '788', '543', '821', '967',
                             '768', '742', '646', '800.0', '816', '748.0', '922', '525.0', '1016', '660', '665',
                             '727.0', '745', '705', '768.4', '781.0', '663', '534', '785.7', '779.9', '700', '791',
                             '522', '784.0', '696', '710', '782', '776', '775', '968.8', '659', '792.0', '814', '777.6',
                             '537', '717', '763.0', '720', '745.0', '980', '756.8', '680.0', '729.0', '749', '773',
                             '538.7', '547', '800 | 620', '860', '653', '796.0', '670', '762.0', '519', '776.0', '485',
                             '524', '738.0', '808', '658', '794.0', '629.4', '655.0', '758', '895', '528', '760',
                             '779.2', '738', '733', '700.5', '776.5', '712.7', '773.0', '801'])))

    storage_time_until_next_deposition_step = Quantity(
        type=str,
        shape=[],
        description="""
    The time between the perovskite stack is finalised and the next layer is deposited
- If there are uncertainties, state the best estimate, e.g. write 35 and not 20-50.
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(
                suggestions=['1200.0', '144.0', '300.0', '1440.0', '24.0', '2400.0', '3120.0', '2160.0', '960.0',
                             '120.0', 'Unknown', '12.0', '72.0', '240.0', '720.0', '1920.0', '432.0', '480.0', '168.0',
                             '48.0', '2880.0', '1680.0', '192.0', '4.0'])))

    storage_atmosphere = Quantity(
        type=str,
        shape=[],
        description="""
    The atmosphere in which the sample with the finalised perovskite stack is stored until the next deposition step.
Example
Air
N2
Vacuum
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=['Unknown', 'Air', 'Ambient', 'Vacuum', 'N2', 'O2', 'Ar'])))

    storage_relative_humidity = Quantity(
        type=str,
        shape=[],
        description="""
    The time between the perovskite stack is finalised and the next layer is deposited
- If there are uncertainties, state the best estimate, e.g write 35 and not 20-50.
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(
                suggestions=['', '40.0', '30.0', '20.0', '75.0', '45.0', '90.0', '24.0', '60.0', '50.0', '10.0', '70.0',
                             '80.0', '35.0'])))

    surface_treatment_before_next_deposition_step = Quantity(
        type=str,
        shape=[],
        description="""
    Description of any type of surface treatment or other treatment the sample with the finalised perovskite stack undergoes before the next deposition step.
- If more than one treatment, list the treatments and separate them by a double forward angel bracket (‘ >> ‘)
- If no special treatment, state that as ‘none’
- This category was included after the projects initial phase wherefor the list of reported categories is
short. Thus, be prepared to expand the given list of alternatives in the data template.
Examples:
none
UV
Ozone
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', 'UV', 'Ar plasma'])))

    def normalize(self, archive, logger):
        super().normalize(archive, logger)

        from .formula_normalizer import PerovskiteFormulaNormalizer
        from nomad.atomutils import Formula
        from nomad.datamodel.results import Symmetry

        add_solar_cell(archive)
        add_band_gap(archive, self.band_gap)

        if self.composition_short_form:
            archive.results.properties.optoelectronic.solar_cell.absorber = self.composition_short_form.split(' | ')

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
                archive.results.material.functional_type = ['semiconductor', 'solar cell']

            formula_cleaner = PerovskiteFormulaNormalizer(self.composition_long_form)
            final_formula = formula_cleaner.clean_formula()
            try:
                formula = Formula(final_formula[0])
                formula.populate(archive.results.material)
                archive.results.material.chemical_formula_descriptive = formula_cleaner.pre_process_formula()
            except Exception as e:
                logger.warn('could not analyse chemical formula', exc_info=e)
            archive.results.material.elements = final_formula[1]

        ions = []
        a_ions_names = []
        a_ions_coefficients = []
        if self.composition_a_ions is not None:
            a_ions_names = self.composition_a_ions.split("; ")
        if self.composition_a_ions_coefficients is not None:
            a_ions_coefficients = [float(c) for c in self.composition_a_ions_coefficients.split("; ")]

        if len(a_ions_names) != 0 and len(a_ions_names) == len(a_ions_coefficients):
            for i in range(len(a_ions_names)):
                ion_a = Ion(name=a_ions_names[i], coefficients=a_ions_coefficients[i], ion_type='A')
                ion_a.normalize(self, archive)
                ions.append(ion_a)

        b_ions_names = []
        b_ions_coefficients = []
        if self.composition_b_ions is not None:
            b_ions_names = self.composition_b_ions.split("; ")
        if self.composition_b_ions_coefficients is not None:
            b_ions_coefficients = [float(c) for c in self.composition_b_ions_coefficients.split("; ")]

        if len(b_ions_names) != 0 and len(b_ions_names) == len(b_ions_coefficients):
            for i in range(len(b_ions_names)):
                ion_b = Ion(name=b_ions_names[i], coefficients=b_ions_coefficients[i], ion_type='B')
                ion_b.normalize(self, archive)
                ions.append(ion_b)

        c_ions_names = []
        c_ions_coefficients = []
        if self.composition_c_ions is not None:
            c_ions_names = self.composition_c_ions.split("; ")
        if self.composition_c_ions_coefficients is not None:
            c_ions_coefficients = [float(c) for c in self.composition_c_ions_coefficients.split("; ")]
        if len(c_ions_names) != 0 and len(c_ions_names) == len(c_ions_coefficients):
            for i in range(len(c_ions_names)):
                ion_c = Ion(name=c_ions_names[i], coefficients=c_ions_coefficients[i], ion_type='C')
                ion_c.normalize(self, archive)
                ions.append(ion_c)

        self.ions = ions

        from nomad.normalizing.topology import add_system_info, add_system
        from nomad.datamodel.results import Relation
        from nomad.normalizing.common import nomad_atoms_from_ase_atoms

        topology = {}
        # Add original system
        parent_system = System(
            method='parser',
            label='absorber material',
            description='A system describing the chemistry and components of the absorber material.',
            system_relation=Relation(type='root'),
        )

        parent_system.structural_type = archive.results.material.structural_type
        parent_system.chemical_formula_hill = archive.results.material.chemical_formula_hill
        parent_system.elements = archive.results.material.elements
        parent_system.chemical_formula_iupac = archive.results.material.chemical_formula_iupac

        add_system(parent_system, topology)
        add_system_info(parent_system, topology)

        for ion in self.ions:
            ase_atoms = optimize_molecule(ion.smile)
            atoms = nomad_atoms_from_ase_atoms(ase_atoms)
            if ion.ion_type != 'C':
                label = f'{ion.ion_type} Cation: {ion.molecular_formula}'
            else:
                label = f'{ion.ion_type} Anion: {ion.molecular_formula}'
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
