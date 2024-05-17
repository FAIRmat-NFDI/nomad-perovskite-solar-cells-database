from nomad.datamodel.data import ArchiveSection
from nomad.metainfo import Quantity

from perovskite_solar_cell_database.schema_sections.utils import add_solar_cell


class Backcontact(ArchiveSection):
    """
    A section to describe information related to the back contact of the solar cell.
    """

    stack_sequence = Quantity(
        type=str,
        shape=[],
        description="""
    The stack sequence describing the back contact.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- If two materials, e.g. A and B, are mixed in one layer, list the materials in alphabetic order and separate them with semicolons, as in (A; B)
- If no back contact, state that as ‘non’
- Use common abbreviations when appropriate but spell it out if risk for confusion.
- If a material is doped, or have an additive, state the pure material here and specify the doping in the columns specifically targeting the doping of those layers.
- There is no sharp well-defined boundary between when a material is best considered as doped or as a mixture of two materials. When in doubt if your material is best described as doped or as a mixture, use the notation that best capture the metaphysical essence of the situation.
- There are a lot of stack sequences described in the literature. Try to find your one in the list. If it is not there (i.e. you may have done something new) define a new stack sequence according to the instructions.
Example:
Au
Ag
Al
Carbon
MoO3 | Ag
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'Au | ITO',
                    'rGO | Au',
                    'MoO3 | Ag | WO3',
                    'Carbon; WO3-np',
                    'ITO | MgF2',
                    'Al | Al2O3',
                    'Ag | Alq3',
                    'AgAu',
                    'MoOx | Ag',
                    'Carbon-nt; PCBM-60',
                    'ITO',
                    'AgAl',
                    'Cr | Cu',
                    'AgZn | Al',
                    'Mo | Ag',
                    'Cu-CFN',
                    "Field's metal",
                    'Al | Ag',
                    'Ag-nw | ZnO-np',
                    'Carbon; NiS',
                    'PEDOT:PSS | PDMS',
                    'Carbon; Graphite; PANI',
                    'MoOx | Au',
                    'Ni-grid',
                    'GaIn',
                    'Cu',
                    'Ag | MoO3',
                    'CNTs',
                    'none',
                    'MoOx | Al',
                    'MWCNTs; ONC1',
                    'Cu | Au',
                    'Cr | Au',
                    'MoOx | Au | Cu | MoOx',
                    'Pt-sheet',
                    'MoO3 | Ag',
                    'Carbon | IPA',
                    'KIPIG',
                    'T-MWCNTs',
                    'AZO',
                    'CSCNT@SnO2',
                    'B-MWCNTs',
                    'Carbon black | Carbon',
                    'Ag | SiO2 | ZnS | Ag | ZnS',
                    'Carbon-nt | PMMA',
                    'MoO3 | Ag | MoO3',
                    'PEDOT:PSS | Graphene',
                    'Pb',
                    'ITO | SLG',
                    'Carbon; NiO:rGO',
                    'Carbon; NiO',
                    'NiO',
                    'Cu; Cu2O',
                    'Graphene | PDMS',
                    'Carbon black; Graphite',
                    'N-Graphene',
                    'CuPc | Carbon',
                    'Carbon',
                    'Carbon-paper',
                    'Au | Al',
                    'Carbon; WO2-np',
                    'FTO',
                    'CNTs | Mxene',
                    'Graphite | Cu-tape',
                    'H2PtCl6',
                    'PTAA | FTO | SLG',
                    'PEI | PEDOT:PSS | PDMS',
                    'Bi2Te3',
                    'Pt',
                    'Carbon-nw',
                    'Cu | Ag | MoO3',
                    'MoO2 | ITO',
                    'Ca | Al',
                    'AZO | Ni | Al | Ni',
                    'MoOx | Cu',
                    'Carbon-tape',
                    'Carbon | Au',
                    'Carbon | CuSCN',
                    'PEDOT:PSS | Al',
                    'TFSA-Graphene | PET | Ag',
                    'ITO | Ag-grid',
                    'Ca',
                    'Mo2O3 | Ag',
                    'SnO2-c | Ag | SnO2-c',
                    'Candle soot | FTO | SLG',
                    'MoOx | IZO',
                    'Au | Ag-nw',
                    'Au',
                    'TETA-Graphene | PET',
                    'W',
                    'Transparent Conductive Adhesive | PET:Ni mesh',
                    'Graphene | PMMA | PDMS',
                    'MoO3 | Au | MoO3',
                    'Au | LiF',
                    'MoO3 ∣ ITO',
                    'Au-np',
                    'Mg | Al',
                    'Carbon | Ag',
                    'TETA-Graphene | PET | Ag',
                    'Graphite | Cu',
                    'Ag-nw',
                    'Ni',
                    'Na@Carbon-nanowalls',
                    'Carbon black',
                    'Au | Organosilicate',
                    'AZO-c',
                    'Carbon; NiO-np',
                    'Ag',
                    'Ag | FTO',
                    'IZTO',
                    'ITO | MWCNTs',
                    'Ag-nw | PCBM-60',
                    'PEDOT:PSS | PEDOT:PSS | PDMS',
                    'Carbon | FTO | SLG',
                    'SWCNTs',
                    'Cr',
                    'IZO | Ag',
                    'FTO | SLG',
                    'Graphite | FTO',
                    'AZO | Ni | Al',
                    'Pd',
                    'Carbon | FAAc',
                    'Carbon black; Carbon-nt; Graphite',
                    'Carbon black; Graphite | MWCNTs',
                    'TeO2 | Ag',
                    'Au | MoO3',
                    'AZO | NiAl',
                    'Bi | Au',
                    'Carbon; MAI | Carbon',
                    'NiO | Ag | NiO',
                    'MoO3 | ITO | MgF2',
                    'PH 1000',
                    'Ag | ITO | Ag',
                    'ITO | LiF',
                    'Ag | IZO',
                    'LiF | Al',
                    'H:MoO3-nanobelts',
                    'Carbon | CNTs',
                    'Ti | Au',
                    'Carbon | Al',
                    'MoOx | Au | MoOx',
                    'Ag-sheet',
                    'TFSA-Graphene | PET',
                    'Graphene | PET',
                    'Graphene | PEDOT',
                    'MoOx | Ag | MoOx',
                    'MoO3 | AuAg | MoO3',
                    'Carbon | Carbon-fibre',
                    'MoO3 | Au | Ag',
                    'Ba | Ag',
                    'Graphen',
                    'Mg | Ag',
                    'Carbon | MAAc',
                    'MoO3 | Au',
                    'MoOx | ITO',
                    'Graphite | Pt',
                    'MWCNTs; ONC2',
                    'IZO',
                    'Ag | Ni',
                    'PANI | FTO | SLG',
                    'Al | Au',
                    'MoO3 ∣ Au ∣ Ag ∣ MoO3 | Alq3',
                    'PEDOT:PSS | Ag-nw | PDMS',
                    'MWCNTs',
                    'Cr | Pt | FTO',
                    'SnO2-c | Ag',
                    'Carbon | Sn',
                    'Unknown',
                    'Carbon; PEMA',
                    'Carbon | Graphite',
                    'MoP3 | Ag',
                    'Ag | Ta2O3',
                    'Cr2O3:Cr',
                    'Graphene | Au',
                    'PEDOT:PSS | FTO | SLG',
                    'Carbon | CNTs | Mxene',
                    'AlAg',
                    'AZO | Au',
                    'AV-Carbon; MAI',
                    'Graphite; Carbon black@5:1',
                    'NiO | Ag | NiO | NaYF4 | Ag',
                    'AV-carbon; MAI',
                    'SWCNTs | PMMA',
                    'Ba | Al',
                    'Pt-Carbon-nt',
                    'Sb',
                    'Carbon-epoxy | Ag',
                    'ITO | Ni | Al',
                    'Ni | Al',
                    'Ag | V2O5',
                    'Pt | FTO | SLG',
                    'PEDOT:PSS | ITO | SLG',
                    'Graphene',
                    'Cu | Au | BCP',
                    'IZO | Au',
                    'Au | Ni',
                    'Au | ITO | Au',
                    'MoO3 | AZO | AlNi-grid',
                    'WO3 | Ag',
                    'Au | Ag',
                    'SnO2-c | Cu | SnO2-c',
                    'Carbon | FTO',
                    'CSCNT@Al2O3-c | CSCNT@SnO2',
                    'Ti',
                    'Carbon-nt',
                    'AZO-np | Ag',
                    'Carbon; NiPt-nw',
                    'D-Sorbito; PEDOT:PSSl | Ag-nw | PET',
                    'Carbon; LPP',
                    'MoOx | Cu | MoOx',
                    'PEDOT:PSS | ITO | PET',
                    'In',
                    'Carbon-nanowalls',
                    'NiS | Cr | Pt | FTO | SLG',
                    'Ag | ITO',
                    'Ca | Ag',
                    'Ag-nw | C60',
                    'MoOx | Ag | ZnS',
                    'Au | FTO',
                    'Pt | Si',
                    'Al',
                    'Ag@Au-np',
                    'Graphite',
                    'PEDOT:PSS:PSA',
                    'MnO3 | Ag',
                    'AgAu-mp',
                    'ITO | Al',
                    'Ag | SnO2-c',
                    'ICO',
                    'Ti-grid',
                    'ITO | Au',
                    'MoO3 | Au | Ag | MoO3 | Alq3',
                    'Au-np; NiO',
                    'Carbon-nt | Carbon',
                    'MoOx | ITO | Au',
                    'PEDOT:PSS; Sorbitol | Ag-grid | PET',
                    'MoO3 | ITO',
                    'Pt | FTO',
                    'MoOx | IO | ITO | Au',
                    'Carbon | Galinstan',
                    'P3HT | FTO | SLG',
                    'ITO | Ag',
                    'Ni | Au',
                    'Ag | Au',
                    'SWCNTs | Ag',
                    'Ag | Al',
                    'MoOx | IAI',
                    'Cu | Ag',
                    'Perovskite | PEDOT:PSS | ITO | SLG',
                    'Graphene oxide | Carbon',
                    'Ag-nanocubes | Ag | MoO3',
                    'MoO3 | IZO',
                    'Carbon-mp',
                    'MoOx | ITO | MgF2',
                    'NbS2',
                    'MoO3 | Al',
                    'Ti3C2',
                    'MWCNTs; ONC3',
                    'Carbon | PEDOT:PSS | FTO | SLG',
                    'MoOx | IZO | Au',
                    'LiF | Ag',
                    'ITO | Au-grid',
                    'PEDOT:PSS',
                    '3D potassium-ion preintercalated graphene (KIPIG)',
                    'PEI | PH 1000',
                    "Filed's metal",
                    'Ti | Cu',
                    'Au | Au-wire',
                    'AlNi-grid',
                    'Carbon-nt | PMMA | Au',
                    'ITO | PEN',
                    'Carbon black; MWCNTs',
                    'Carbon | Silica gel electrolyte | Carbon',
                    'CSCNT@Al2O3-c | CSCNT',
                    'Ag-np | ITO',
                    'Carbon; MAI',
                    'PTCBI | Ag | WO3 | PTCBI | Ag',
                    'Carbon | KAc',
                    'Ag | CsF',
                    'Liq | Al',
                    'Graphite | FTO | SLG',
                    'Cu-ribbon',
                    'ITO | Cu',
                    'Mo',
                    'Metal',
                    'AZO | Ag | AZO',
                    'Graphite ribbon',
                    'Pt-np | FTO | SLG',
                    'Carbon | CsAc',
                ]
            ),
        ),
    )

    thickness_list = Quantity(
        type=str,
        shape=[],
        description="""
    A list of thicknesses of the individual layers in the stack.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- The layers must line up with the previous filed.
- State thicknesses in nm
- Every layer in the stack have a thickness. If it is unknown, state this as ‘nan’
- If there are uncertainties, state the best estimate, e.g write 100 and not 90-110
Example
100
10 | 80
nan | 100
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    '89.0',
                    '90.0',
                    '40.0 | 11.0',
                    '5.0 | 130.0',
                    '50.0',
                    '70.0 | 10.0 | 10.0',
                    '220.0',
                    '230.0 | 100.0',
                    '81.0',
                    '180.0',
                    '45.0',
                    '15.0 | 80.0',
                    '14000.0',
                    '50.0 | 4000.0',
                    '7.0 | 80.0',
                    '24.0 | 15.0 | 20.0 | 480.0 | 8.0',
                    '10.0 | 100.0 | 200.0',
                    '203.0',
                    '10.0 | 120.0 | 70.0',
                    '11.0 | 30.0',
                    '1.0 | 200.0',
                    '30.0 | 120.0 | nan',
                    '60.9',
                    '11000.0 | nan',
                    '1.3 | 100.0',
                    '300.0 | 250.0',
                    '2.0 | 1.0 | 7.0 | 5.0 | 50.0',
                    '15.0 | 150.0',
                    '60.4',
                    '35.0 | 103.0 | 35.0',
                    '2.5 | 154.0',
                    '6.0 | 11.0 | 20.0',
                    '1800.0',
                    '22000.0',
                    '11.0 | 50.0',
                    '60.5',
                    '95.0',
                    '20.0 | 10.0 | 20.0',
                    '10.0 | 110.0',
                    '20.0 | 14.0',
                    '87.0',
                    '10.0 | 90.0',
                    '70.0',
                    '12.0 | 40.0',
                    '21.0 | 250.0',
                    '11.0',
                    '500.0',
                    '2000.0 | nan',
                    '5.0 | nan',
                    '53150.0',
                    '2000.0',
                    '20.0 | 15.0 | 20.0 | 480.0 | 8.0',
                    '10.0 | 80.0',
                    '1.0 | 7.0 | 40.0',
                    '21.0 | 15.0 | 20.0 | 480.0 | 8.0',
                    '8.0 | 120.0',
                    '5.0 | 150.0',
                    'nan | 6.0 | nan',
                    '61210.0',
                    '260.0',
                    '201.0',
                    '3.0 | 1.0 | 7.0 | 5.0 | 50.0',
                    '2.0 | 100.0',
                    '7.0 | 60.0',
                    '100.0 | 1000.0',
                    '16500.0 | nan',
                    '10.0 | 15.0 | 30.0',
                    '240.0',
                    '7.2 | 70.0',
                    '50.0 | 50.0',
                    '11.0 | nan',
                    '9.0 | nan',
                    '35.0 | 95.0 | 35.0',
                    '330.0',
                    '10.0 | 30000.0',
                    '60.3',
                    '85.0',
                    '60.1',
                    '130.0 | 100.0',
                    '2.5 | 154.0 | 50.0',
                    'nan | 150.0',
                    '15.0 | 12.0',
                    '10.0 | 70.0',
                    '9.0',
                    '15.0 | 12.0 | 60.0',
                    '150.0 | 500.0',
                    '8.0',
                    '0.5 | 60.0',
                    '10.0 | 200.0',
                    '13.0',
                    '7.0 | 12.0 | 30.0',
                    '820.0',
                    '1.0 | 6.0',
                    'nan | 80.0',
                    '13.0 | 80.0',
                    '25.0 | 15.0 | 20.0 | 480.0 | 8.0',
                    '2.0 | 250.0',
                    '93.2',
                    '500.0 | 150.0',
                    '5000.0',
                    '20.0',
                    '52.0',
                    '7.0 | 18.0 | 30.0',
                    '21.0 | 7.0 | 20.0',
                    '60.11',
                    '82.0',
                    '15.0 | 12.0 | 20.0',
                    '6.0 | 1.5 | 9.5 | 20.0',
                    '7870.0',
                    '8.0 | 20.0 | 115.0 | 8.0 | 20.0',
                    '30.0 | 120.0',
                    '30.0 | 80.0',
                    '10.0 | 20.0',
                    '14.0',
                    '8.0 | 20.0 | 65.0 | 8.0 | 20.0',
                    '80.0 | 10.0',
                    '2001.0 | nan',
                    'nan | 100.0',
                    '250.0',
                    '10.0 | 10.0',
                    'nan | 220.0',
                    '65.0',
                    '150.0',
                    '15.0 | 50.0',
                    '4000000000.0',
                    '15.0 | 200.0',
                    '46530.0',
                    'nan | 70.0',
                    '23.0 | 15.0 | 20.0 | 480.0 | 8.0',
                    '35.0 | 10.0 | 35.0',
                    '100000.0 | nan',
                    '88.0 | 700.0',
                    '5.0 | 12.0 | 40.0',
                    '1.0 | 250.0',
                    '8000.0 | nan',
                    '60.8',
                    '12000.0',
                    '15.0 | nan',
                    '60.7',
                    'nan | 25000.0',
                    '1.0 | 100.0',
                    '30.0 | 70.0',
                    '50000.0',
                    '30.0 | 135.0',
                    '8.0 | 200.0',
                    '35.0',
                    '180.0 | 50.0',
                    '30.0 | 7.0 | 80.0',
                    '750.0',
                    '32000.0',
                    '1.0 | nan',
                    '5.0 | 90.0',
                    '8.0 | 80.0',
                    '150.0 | 4900.0',
                    '90.0 | 200.0',
                    '51.0',
                    '22.0 | 15.0 | 20.0 | 480.0 | 8.0',
                    '4500.0',
                    '16000.0',
                    '24000.0',
                    '30000.0',
                    '10.0 | 60.0',
                    '12.0 | 100.0',
                    '7.0 | 120.0',
                    '9.0 | 100.0',
                    '6.7 | 100.0',
                    '154.0 | 50.0',
                    '25.0',
                    '10.0 | 202.0',
                    '20.0 | 10.0 | 35.0',
                    '80.0 | 20.0',
                    '40.0',
                    '65.0 | nan',
                    '83.0',
                    '11200.0',
                    '8.0 | 90.0',
                    '20.0 | 7.0 | 20.0',
                    '230.0',
                    '75.0',
                    '8.0 | 60.0',
                    '190.0',
                    '6.0 | 100.0',
                    '7.0 | 1.0',
                    '3.0 | nan',
                    '15000.0',
                    '35.0 | 84.0 | 35.0',
                    '60.6',
                    '9.0 | 80.0',
                    'nan | 400.0 | 500.0',
                    '10.0 | 40.0',
                    '145.0',
                    'nan | 50.0 | 4000.0',
                    '1500.0',
                    '100.0 | 125.0',
                    '2.0 | 200.0',
                    '28.0 | 15.0 | 20.0 | 480.0 | 8.0',
                    '7.0 | 70.0',
                    '60.0',
                    '125.0',
                    '5.0',
                    '40000.0',
                    '45.0 | nan',
                    '35.0 | 76.0 | 35.0',
                    '900.0',
                    '400.0',
                    '105.0 | 90.0',
                    '25000.0',
                    '8.0 | 30.0 | 100.0',
                    '180.0 | 100.0',
                    '2.0',
                    '20.0 | nan',
                    '80.0 | 150.0',
                    '30.0 | 100.0',
                    '11.0 | 10.0',
                    '5.0 | 120.0',
                    '4.0',
                    '1.0 | 10.0 | 20.0',
                    '14.0 | 20.0',
                    '15.0 | 40.0',
                    '40.0 | 120.0',
                    '20.0 | 250.0',
                    '600.0',
                    'nan | 200.0',
                    '12.0',
                    '12000.0 | nan',
                    '6.0 | nan',
                    '100.0',
                    '105.0',
                    '8.0 | 110.0',
                    '15.0 | 120.0',
                    '37500.0',
                    '23000.0 | nan',
                    '5.0 | 10.0 | 35.0',
                    '10.0 | 40.0 | nan',
                    '80.0 | 50.0',
                    '10000.0 | nan',
                    '8.0 | 20.0 | 85.0 | 8.0 | 20.0',
                    '28000.0',
                    '21000.0',
                    '48.0',
                    '9.0 | 25.0',
                    '4.0 | 80.0',
                    '15.0 | 100.0',
                    '96.0',
                    '3.0 | 80.0',
                    '200.0',
                    '70.0 | 10.0',
                    '4000.0 | nan',
                    '150.0 | nan',
                    '80.0 | 8.0',
                    '350.0',
                    '110.0 | 120.0',
                    '1.0 | 10.0 | 35.0',
                    '90.0 | 100.0',
                    '50.0 | 100.0',
                    '80000.0',
                    '10.0 | 120.0',
                    '202.0',
                    '200000.0',
                    '8000.0',
                    '35.0 | 120.0 | 70.0',
                    '160.0',
                    '10.0 | 55.0',
                    '3.5 | 100.0',
                    '2000.0 | 100.0 | nan',
                    '10.0 | 150.0',
                    '25.0 | 100.0',
                    '12.0 | 80.0',
                    '5.0 | 10.0 | 40.0',
                    '170.0',
                    '35.0 | 64.0 | 35.0',
                    '1500-2000',
                    '55.0',
                    '9000.0',
                    '6.0',
                    '4900.0',
                    '10.0 | 100.0 | 10.0 | 100.0',
                    '100.0 | 20.0',
                    '20.0 | 100.0',
                    '7.0 | nan',
                    '34.0 | 20.0 | 25.0 | nan | 8.0',
                    '3333.0',
                    '2.5 | 80.0',
                    '20.0 | 80.0',
                    '18.0 | 10.0 | 19.0',
                    '150.0 | 100.0',
                    '5.0 | 60.0',
                    '6.0 | 10.0 | 35.0',
                    '3500.0',
                    '550.0',
                    '15.0',
                    '12500.0',
                    '35.0 | 120.0',
                    '8.0 | 100.0',
                    '7.0 | 24.0 | 30.0',
                    '300.0',
                    '11.0 | 80.0',
                    '50.0 | 101.0',
                    '185.0',
                    '71600.0',
                    '77.0 | nan',
                    '5.0 | 100.0',
                    '120.0',
                    '88.0',
                    '130.0',
                    '3000.0',
                    '110.0',
                    '20.0 | 15.0',
                    '120000.0',
                    '300000.0',
                    '10.0 | 100.0',
                    '26.0 | 15.0 | 20.0 | 480.0 | 8.0',
                    '11000.0',
                    '6500.0',
                    '1000.0',
                    '5.0 | 10.0 | 5.0',
                    '10.0 | 1.0 | 10.0 | 40.0',
                    '34.0 | 20.0 | 55.0 | nan | 15.0',
                    '6.3 | 70.0',
                    '60000.0',
                    '100.0 | 100.0',
                    '10.0 | 35.0',
                    '1200.0',
                    '60.2',
                    '390.0',
                    '10.0',
                    '11.0 | 20.0',
                    '25800.0',
                    '35.0 | 160.0',
                    '35.0 | 53.0 | 35.0',
                    '30.0 | nan',
                    '1.0 | 120.0',
                    '120.0 | 70.0',
                    '20000.0',
                    '5.0 | 20.0 | 35.0',
                    '210.0',
                    '2500.0',
                    '5.0 | 300.0',
                    '5.0 | 80.0',
                    '10.0 | 10.0 | 35.0',
                    '800.0',
                    '1.9 | 70.0',
                    '1.45 | nan',
                    '9.0 | 110.0',
                    '40.0 | 4000.0',
                    '3.0 | 100.0',
                    '20.0 | 14.0 | 20.0',
                    '15.0 | 350.0',
                    '53.0',
                    '70.0 | 30.0',
                    '250.0 | 50.0 | 1000.0',
                    '86.0',
                    '1600.0',
                    '3.0 | 200.0',
                    '7000.0',
                    '97.0',
                    '30.0',
                    '6.0 | 60.0',
                    '7.0 | 100.0',
                    '3.0 | 150.0',
                    '10.0 | nan | nan',
                    '10.0 | 75.0',
                    '10.0 | 50.0',
                    '70000.0',
                    '9600.0',
                    '140.0',
                    '50.0 | 120.0',
                    '100.0 | nan',
                    '80.0',
                    'nan | 5.0',
                    '27.0 | 15.0 | 20.0 | 480.0 | 8.0',
                    '80.0 | 80.0',
                    '6.0 | 80.0',
                    '13000.0',
                    '35.0 | 88.0 | 35.0',
                    '4000.0',
                    '100000.0',
                    '60.0 | 40.0',
                    '84.0',
                    '16.0',
                    '10.0 | 201.0',
                    '10000.0',
                    '34.0 | 20.0 | 75.0 | nan | 35.0',
                    '10.0 | 8.5 | 10.0',
                ]
            ),
        ),
    )

    additives_compounds = Quantity(
        type=str,
        shape=[],
        description="""
    List of the dopants and additives that are in each layer of the HTL-stack
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- The layers must line up with the previous fields.
- If several dopants/additives, e.g. A and B, are present in one layer, list the dopants/additives in alphabetic order and separate them with semicolons, as in (A; B)
- If no dopants/additives, state that as “Undoped”
- If the doping situation is unknown, stat that as‘Unknown’
- This category was included after the projects initial phase wherefor the list of reported categories is
short. Thus, be prepared to expand the given list of alternatives in the data template, even if to most common back contacts is undoped metals
Example
CuS
B; P
Au-np | Undoped
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    'Undoped | Undoped',
                    'TiO2-np',
                    'Undoped | Undoped | Undoped | Undoped | Undoped',
                    'B; P',
                    'C; NiO',
                    'B4C',
                    'WO3-np',
                    'P',
                    'B',
                    'Undoped',
                    'CuS',
                ]
            ),
        ),
    )

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
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    '4; 1',
                    '10 wt%',
                    '2 wt%',
                    '7; 3',
                    '5 wt%',
                    '0.1 wt%',
                    '9; 1',
                    '3.5 wt%',
                    '7.5 wt%',
                    '8 wt%',
                    '6.5 wt%',
                    '0.5 wt%',
                ]
            ),
        ),
    )

    deposition_procedure = Quantity(
        type=str,
        shape=[],
        description="""
    The deposition procedures for the HTL-stack.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate them by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- Thermal annealing is generally not considered as an individual reaction step. The philosophy behind this is that every deposition step has a thermal history, which is specified in a separate filed. In exceptional cases with thermal annealing procedures clearly disconnected from other procedures, state ‘Thermal annealing’ as a separate reaction step.
- Please read the instructions under “Perovskite. Deposition. Procedure” for descriptions and distinctions between common deposition procedures and how they should be labelled for consistency in the database.
- A few additional clarifications:
- Lamination
o A readymade film is transferred directly to the device stack. A rather broad concept. An everyday kitchen related example of lamination would eb to place a thin plastic film over a slice of pie.
- Sandwiching
o When a readymade top stack simply is placed on top of the device stack. Could be held together with clams. The typical example is a when a “Carbon | FTO | SLG” is placed on top of the device stack. Standard procedure in the DSSC filed.
Example
Evaporation
Evaporation | Evaporation
Doctor blading
Screen printing
Sputtering
Lamination
E-beam evaporation
Sandwiching
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'Evaporation | Evaporation | Evaporation | Evaporation',
                    'Doctor blading | Doctor blading | Doctor blading',
                    'Pressed',
                    'Spray-coating | Spray-coating',
                    'Spin-coating | Spin-coating',
                    'Electropolymerisation | Sandwiching',
                    'Brush painting',
                    'Evaporation | DC Sputtering',
                    'Screen printing | Lamination',
                    'Spin-coating | Evaporation',
                    'Sputtering | Sputtering | Sputtering',
                    'Evaporation | Spin-coating',
                    'Sputtering',
                    'Screen printing | Spray-coating',
                    'DC Sputtering',
                    'Evaporation | Sputtering | Sputtering',
                    'Evaporation | RF sputtering | E-beam evaporation',
                    'Doctor blading | Spin-coating',
                    'Dropp casting',
                    'Lamination | Lamination',
                    'RF sputtering | Evaporation | Evaporation',
                    'Evaporation | ALD',
                    'Inkjet printing',
                    'RF sputtering',
                    'E-beam evaporation | E-beam evaporation | E-beam evaporation | PVD | Evaporation',
                    'Sputtering | Spray-coating',
                    'Candle burning | Sandwiching',
                    'Brush painting | Brush painting',
                    'Evaporation | Evaporation',
                    'E-beam evaporation | E-beam evaporation | E-beam evaporation',
                    'CVD | Spin-coating >> reactive ion etching',
                    'Evaporation | Activated reactive evaporation',
                    'Spin-coating | Doctor blading',
                    'Sputtering | Sputtering',
                    'Drop coated',
                    'Sandwithcing',
                    'CVD >> Lamination',
                    'Unknown | Ultrasonic  welding',
                    'Sputtering | Evaporation | Evaporation | Evaporation',
                    'Evaporation | Magnetron sputtering',
                    'Candel burning >> Sandwiching | Unknown | Unknown',
                    'Evaporation | RF magnetron sputtering',
                    'Candle burning | Lamination',
                    'ALD | Evaporation | ALD',
                    'Spray-pyrolys | Sandwiching',
                    'Spin-coating | Screen printing',
                    'Lamination | Spin-coating',
                    'Evaporation | DC Magnetron Sputtering',
                    'Lamination | Painting',
                    'Lamination',
                    'Doctor blading | Ultrasonic  welding',
                    'Evaporation | Evaporation | Evaporation',
                    'Brush painting | Unknown',
                    'Evaporation | Sputtering',
                    'PVD',
                    'Dipp-coating',
                    'Screen printing >> Lamination',
                    'Springkling | Sandwiching',
                    'Magnetron sputtering | Magnetron sputtering',
                    'Sputtering | Lamination',
                    'Spin-coating | Sandwiching',
                    'Evaporation',
                    'Unknown',
                    'Unknown | Doctor blading',
                    'Evaporation | Magnetron sputtering | E-beam evaporation',
                    'Lamination | Evaporation',
                    'CVD',
                    'Lamination >> Isostatic pressing',
                    'ALD | Evaporation',
                    'Screen printing',
                    'Evaporation | Sputtering | Evaporation',
                    'Unknown | Evaporation',
                    'Evaporation | Sputtering | Sputtering | Evaporation',
                    'Doctor blading',
                    'Magnetron sputtering',
                    'Evaporation | Evaporation | Evaporation | Evaporation | Evaporation',
                    'RF Magnetron Sputtering',
                    'DC Sputtering | Evaporation',
                    'Candle burning >> Sandwiching',
                    'Dropcasting | Lamination',
                    'Lamination | Dropcasting',
                    'Electrospinning',
                    'Suttering',
                    'E-beam evaporation',
                    'Candle burning >> Lamination',
                    'Screen printing | Painting',
                    'Evaporation >> Evaporation >> Oxidation',
                    'Evaporation | E-beam evaporation | E-beam evaporation | E-beam evaporation | E-beam evaporation',
                    'DC Magnetron Sputtering | Evaporation',
                    'Sputtering >> Lamination',
                    'Evaporation | Sandwiching',
                    'Dropcasting',
                    'Pulsed laser deposition',
                    'DC Magnetron Sputtering',
                    'Screen printing | Unknown',
                    'E-beam evaporation | E-beam evaporation',
                    'Sputtering | Evaporation',
                    'Lamination | Spin-coating | Evaporation',
                    'Brush painting | Sandwiching',
                    'Spin-coating',
                    'Sputtering | E-beam evaporation | E-beam evaporation',
                    'Doctor blading | Doctor blading',
                    'Spray-coating',
                    'Spin-coating | Evaporation | Evaporation',
                    'Doctor blading | Sandwhiching',
                    'Sandwiching',
                    'Painting',
                    'Mechanical clipping',
                    'Evaporation | Spray-coating',
                    'Candel burning | Sandwiching',
                    'Doctor blading | Lamination',
                    'Screen printing | Screen printing',
                    'Evaporation | DC Magnetron Sputtering | E-beam evaporation',
                ]
            ),
        ),
    )

    deposition_aggregation_state_of_reactants = Quantity(
        type=str,
        shape=[],
        description="""
    The physical state of the reactants.
- The three basic categories are Solid/Liquid/Gas
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the aggregation state associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- Most cases are clear cut, e.g. spin-coating involves species in solution and evaporation involves species in gas phase. For less clear-cut cases, consider where the reaction really is happening as in:
o For a spray-coating procedure, it is droplets of liquid that enters the substrate (thus a liquid phase reaction)
o For sputtering and thermal evaporation, it is species in gas phase that reaches the substrate (thus a gas phase reaction)
- This category was included after the projects initial phase wherefor the list of reported categories is short. Thus, be prepared to expand the given list of alternatives in the data template.
Example
Liquid
Gas | Liquid
Liquid | Liquid >> Liquid
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'Solid',
                    'Liquid',
                    'Unknown',
                    'Gas | Gas | Gas | Gas | Gas',
                    'Solid | Gas',
                    'Solid | Solid | Solid',
                    'Liquid | Gas | Gas',
                    'Liquid | Solid',
                    'Gas',
                    'Liquid >> Solid',
                    'Gas | Gas',
                    'Liquid | Gas',
                ]
            ),
        ),
    )

    deposition_synthesis_atmosphere = Quantity(
        type=str,
        shape=[],
        description="""
    The synthesis atmosphere.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the atmospheres associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- The number and order of layers and deposition steps must line up with the previous columns.
- If the synthesis atmosphere is a mixture of different gases, e.g. A and B, list the gases in alphabetic order and separate them with semicolons, as in (A; B)
- “Dry air” represent air with low relative humidity but where the relative humidity is not known
- “Ambient” represent air where the relative humidity is not known. For ambient conditions where the relative humidity is known, state this as “Air”
- “Vacuum” (of unspecified pressure) is for this purpose considered as an atmospheric gas
- This category was included after the projects initial phase wherefor the list of reported categories is short. Thus, be prepared to expand the given list of alternatives in the data template.
Example
Vacuum
Vacuum | N2
Air | Ar; H2O >> Ar
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'N2 | Vacuum',
                    'Vacuum | Vacuum',
                    'Unknown',
                    'Air',
                    'Vacuum',
                    'Vacuum | Vacuum | Vacuum | Vacuum | Vacuum',
                    'Air | Vacuum | Vacuum',
                    'Air >> Air',
                    'Ar',
                    'Ar | O2',
                ]
            ),
        ),
    )

    deposition_synthesis_atmosphere_pressure_total = Quantity(
        type=str,
        shape=[],
        description="""
    The total gas pressure during each reaction step
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the pressures associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- The number and order of layers and deposition steps must line up with the previous columns.
- Pressures can be stated in different units suited for different situations. Therefore, specify the unit. The preferred units are:
o atm, bar, mbar, mmHg, Pa, torr, psi
- If a pressure is not known, stat that as ‘nan’
- For values with uncertainties, state the best estimate, e.g. write 100 pa and not 80-120 pa.
Example
1 atm
0.002 torr | 10000 Pa
nan >> 1 atm | 1 atm
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    '0.0006 Pa',
                    '0.000009 mbar',
                    '0.0001 Torr',
                    '0.01 Torr',
                    '0.0000002 Torr',
                    '0.000005 mbar',
                    '0.000002 bar',
                    '0.0001 mbar',
                    '0.0001 Pa | 0.0001 Pa',
                    '0.0005 Pa',
                    '0.00001 mbar',
                    '0.0004 Pa',
                    '0.00005 Torr',
                    '0.0003 bar',
                    '0.0000019 Torr',
                    '0.1 Torr',
                    '0.000001 mbar',
                    '1 atm >> 0.2 MPa',
                    '0.0000001 Torr',
                    '0.00001 Pa',
                    '0.000001 bar',
                    '0.000000001 bar',
                    '0.000006 Torr',
                    '0.000007 Torr',
                    '1.2 mTorr',
                    '0.006 Torr',
                    '0.000004 Torr',
                    '10 E-7Torr',
                    '0.00005 mbar',
                    '0.00001 Torr',
                    '2 e-05',
                    '2 E-10Torr',
                    '0.00005 Pa',
                    '0.000008 bar',
                    '0.00000003 Torr',
                    '0.0001 Pa',
                    '0.000001 Torr',
                    '0.0002 Pa',
                    '0.0000048 Torr',
                    '0.000002 Torr',
                    '0.0003 Pa',
                    '0.00003 mbar',
                    '0.0000001 mbar',
                    '0.000002 mbar',
                    '1 atm',
                    '0.000005 Torr',
                ]
            ),
        ),
    )

    deposition_synthesis_atmosphere_pressure_partial = Quantity(
        type=str,
        shape=[],
        description="""
    The partial pressures for the gases present during each reaction step.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the pressures associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- The number and order of layers and deposition steps must line up with the previous columns.
- If the synthesis atmosphere is a mixture of different gases, e.g. A and B, list the partial pressures and separate them with semicolons, as in (A; B). The list of partial pressures must line up with the gases they describe.
- In cases where no gas mixtures are used, this field will be the same as the previous filed.
Example
1 atm
0.002 torr | 10000 Pa
nan >> 0.99 atm; 0.01 atm | 1 atm
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    '0.0001 mbar',
                    '0.0001 Pa | 0.0001 Pa',
                    '0.00001 mbar',
                    '0.0004 Pa',
                    '0.0003 bar',
                    '0.000001 mbar',
                    '1 atm >> 0.2 MPa',
                    '0.00001 Pa',
                    '0.000006 Torr',
                    '0.000007 Torr',
                    '0.006 Torr',
                    '0.000004 Torr',
                    '0.00001 Torr',
                    '0.000001 Torr',
                    '0.000002 Torr',
                    '0.00003 mbar',
                    '0.0003 Pa',
                    '0.0000001 mbar',
                    '0.000002 mbar',
                    '1 atm',
                    '0.000005 Torr',
                ]
            ),
        ),
    )

    deposition_synthesis_atmosphere_relative_humidity = Quantity(
        type=str,
        shape=[],
        description="""
    The relative humidity during each deposition step
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the relative humidity associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- The number and order of layers and deposition steps must line up with the previous columns
- If the relative humidity for a step is not known, stat that as ‘nan’
- For values with uncertainties, state the best estimate, e.g. write 35 and not 30-40.
Example
35
0 | 20
nan >> 25 | 0
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=['', '25.0', '30 >> 30', '30.0', '50 | nan | nan', '50.0']
            ),
        ),
    )

    deposition_solvents = Quantity(
        type=str,
        shape=[],
        description="""
    The solvents used in each deposition procedure for each layer in the stack
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the solvents associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If a solvent is a mixture of different solvents, e.g. A and B, list the solvents in alphabetic order and separate them with semicolons, as in (A; B)
- The number and order of layers and deposition steps must line up with the previous columns.
- For non-liquid processes with no solvents, state the solvent as ‘none’
- If the solvent is not known, state this as ‘Unknown’
- Use common abbreviations when appropriate but spell it out when risk for confusion
- This category was included after the projects initial phase wherefor the list of reported categories is short. Thus, be prepared to expand the given list of alternatives in the data template.
Example
none
Acetonitile; Ethanol | Chlorobenzene
none >> Ethanol; Methanol; H2O | DMF; DMSO
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'Unknown',
                    'none',
                    'Methanol | none | none',
                    'Ethyl cellulose; Terpineol',
                    'IPA | none',
                    'Ethyl cellulose; Terpineol | Unknown',
                ]
            ),
        ),
    )

    deposition_solvents_mixing_ratios = Quantity(
        type=str,
        shape=[],
        description="""
    The mixing ratios for mixed solvents
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the solvent mixing ratios associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- The number and order of layers and deposition steps must line up with the previous columns.
- For pure solvents, state the mixing ratio as 1
- For non-solvent processes, state the mixing ratio as 1
- For unknown mixing ratios, state the mixing ratio as ‘nan’
- For solvent mixtures, i.e. A and B, state the mixing ratios by using semicolons, as in (VA; VB)
- The preferred metrics is the volume ratios. If that is not available, mass or mol ratios can be used instead, but it the analysis the mixing ratios will be assumed to be based on volumes.
Example
1
4; 1 | 1
1 >> 5; 2; 0.3 | 2; 1
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=['', '1', '1 | 1', '1 | nan | nan']),
        ),
    )

    deposition_solvents_supplier = Quantity(
        type=str,
        shape=[],
        description="""
    The suppliers of all the solvents.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the solvent suppliers associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If a solvent is a mixture of different solvents, e.g. A and B, list the associated suppliers and separate them with semicolons, as in (A; B)
- The number and order of layers, reaction steps, and solvents must line up with the previous columns.
- For non-liquid processes with no solvents, mark the supplier as ‘none’
- If the supplier for a solvent is unknown, state this as ‘Unknown’
- This category was included after the projects initial phase wherefor the list of reported categories is short. Thus, be prepared to expand the given list of alternatives in the data template.
Example
Sigma Aldrich
Sigma Aldrich; Fisher | Acros
none >> Sigma Aldrich; Sigma Aldrich | Unknown
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'Shanghai MaterWin New Material',
                    'Guangzhou Seaside Technology',
                    'Unknown',
                ]
            ),
        ),
    )

    deposition_solvents_purity = Quantity(
        type=str,
        shape=[],
        description="""
    The purity of the solvents used.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the solvent purities associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If a solvent is a mixture of different solvents, e.g. A and B, list the associated purities and separate them with semicolons, as in (A; B)
- The number and order of layers, reaction steps, and solvents must line up with the previous columns.
- Use standard nomenclature for purities, e.g. pro analysis, puris, extra dry, etc.
- For non-liquid processes with no solvents, state the purity as ‘none’
- If the purity for a solvent is not known, state this as ‘Unknown’
- This category was included after the projects initial phase wherefor the list of reported categories is short. Thus, be prepared to expand the given list of alternatives in the data template.
Example
Pro analysis
Puris; Puris| Tecnical
none >> Pro analysis; Pro analysis | Unknown
                    """,
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    deposition_reaction_solutions_compounds = Quantity(
        type=str,
        shape=[],
        description="""
    The non-solvent precursor chemicals used in each reaction step
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the non-solvent chemicals associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If a solution contains several compounds, e.g. A and B, list the associated compounds in alphabetic order and separate them with semicolons, as in (A; B)
- Note that also dopants/additives should be included
- When several precursor solutions are made and mixed before the reaction step, it is the properties of the final mixture used in the reaction we here describe.
- The number and order of layers and reaction steps must line up with the previous columns.
- For gas phase reactions, state the reaction gases as if they were in solution.
- For solid-state reactions, state the compounds as if they were in solution.
- For reaction steps involving only pure solvents, state this as ‘none’
- If the compounds for a deposition step is not known, state this as ‘Unknown’
- This category was included after the projects initial phase wherefor the list of reported categories is short. Thus, be prepared to expand the given list of alternatives in the data template.
Example
Au
CuI
Ag
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    'Al',
                    'Graphite',
                    'Mg | Ag',
                    'Carbon Paste',
                    'ITO',
                    'AgAl',
                    'Carbon | nan | nan',
                    'IZO',
                    'Au',
                    'Ag | Au',
                    'Cu',
                    'Ag | MoO3',
                    'Cu | Ag',
                    'Cr | Au',
                    'Ag-nanocubes | Ag | MoO3',
                    'Carbon | Ag',
                    'MoO3 | Al',
                    'Ag',
                    'IZTO',
                    'PEDOT:PSS',
                    'AZO',
                    'Adhesive; PEDOT:PSS | PET; Ni-mesh',
                    'PTCBI | Ag | WO3 | PTCBI | Ag',
                    'AZO-np | Ag',
                    'Carbon',
                    'PEDOT:PSS | Al',
                ]
            ),
        ),
    )

    deposition_reaction_solutions_compounds_supplier = Quantity(
        type=str,
        shape=[],
        description="""
    The suppliers of the non-solvent chemicals.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the non-solvent chemical suppliers associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If a solution contains several dissolved compounds, e.g. A and B, list the associated suppliers and separate them with semicolons, as in (A; B)
- The number and order of layers, reaction steps, and solvents must line up with the previous columns.
- For gas phase reactions, state the suppliers for the gases or the targets/evaporation sources that are evaporated/sputtered/etc.
- For solid state reactions, state the suppliers for the compounds in the same way.
- For reaction steps involving only pure solvents, state the supplier as ‘none’ (as that that is entered in a separate filed)
- For chemicals that are lab made, state that as “Lab made” or “Lab made (name of lab)”
- If the supplier for a compound is unknown, state this as ‘Unknown’
- This category was included after the projects initial phase wherefor the list of reported categories is short. Thus, be prepared to expand the given list of alternatives in the data template.
Example
Dysole; Sigma Aldrich; Dyenamo; Sigma Aldrich
Sigma Aldrich; Fisher | Acros
Lab made (EPFL) | Sigma Aldrich >> none
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'DongDaLai company',
                    'Unknown',
                    'Solaronix',
                    'Styccobond; Agfa | Epigem',
                    'Heraeus',
                    'Guangzhou Seaside Technology',
                    'Sigma Aldrich | Unknown',
                    'Sigma Aldrich',
                    'Ulet',
                    'Shanghai MaterWin New Materials Co., Ltd',
                ]
            ),
        ),
    )

    deposition_reaction_solutions_compounds_purity = Quantity(
        type=str,
        shape=[],
        description="""
    The purity of the non-solvent chemicals.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the compound purities associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If a solution contains several dissolved compounds, i.e. A and B, list the associated purities and separate them with semicolons, as in (A; B)
- The number and order of layers, reaction steps, and solvents must line up with the previous columns.
- Use standard nomenclature for purities, e.g. pro analysis, puris, extra dry, etc.
- For reaction steps involving only pure solvents, state this as ‘none’ (as that is stated in another field)
- If the purity for a compound is not known, state this as ‘Unknown’
- This category was included after the projects initial phase wherefor the list of reported categories is short. Thus, be prepared to expand the given list of alternatives in the data template.
Example
Pro analysis
99.999; Puris| Tecnical
Unknown >> Pro analysis; Pro analysis | none
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['Unknown', '99.99'])
        ),
    )

    deposition_reaction_solutions_concentrations = Quantity(
        type=str,
        shape=[],
        description="""
    The concentration of the non-solvent precursor chemicals.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the concentrations associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If a solution contains several dissolved compounds, e.g. A and B, list the associated concentrations and separate them with semicolons, as in (A; B)
- The order of the compounds must be the same as in the previous filed.
- For reaction steps involving only pure solvents, state this as ‘none’
- When concentrations are unknown, state that as ‘nan’
- Concentrations can be stated in different units suited for different situations. Therefore, specify the unit used. When possible, use one of the preferred units
o M, mM, molal; g/ml, mg/ml, µg/ml, wt%, mol%, vol%, ppt, ppm, ppb
- For values with uncertainties, state the best estimate, e.g write 4 wt% and not 3-5 wt%.
Example
4 wt%
0.2 M; 0.15 M| 10 mg/ml
0.3 mol% | 2 mol%; 0.2 wt% | nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=['', '57.2 wt%; 42.8 wt% | nan', '8 mg/ml | nan']),
        ),
    )

    deposition_reaction_solutions_volumes = Quantity(
        type=str,
        shape=[],
        description="""
    The volume of the reaction solutions
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the volumes associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- The volumes refer the volumes used, not the volume of the stock solutions. Thus if 0.15 ml of a solution is spin-coated, the volume is 0.15 ml
- For reaction steps without solvents, state the volume as ‘nan’
- When volumes are unknown, state that as ‘nan’
Example
0.1
0.1 >> 0.05 | 0.05
nan | 0.15
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=['15.0 | Unknown | Unknown', 'Unknown']),
        ),
    )

    deposition_reaction_solutions_age = Quantity(
        type=str,
        shape=[],
        description="""
    The age of the solutions
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the age of the solutions associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- As a general guideline, the age refers to the time from the preparation of the final precursor mixture to the reaction procedure.
- When the age of a solution is not known, state that as ‘nan’
- For reaction steps where no solvents are involved, state this as ‘nan’
- For solutions that is stored a long time, an order of magnitude estimate is adequate.
Example
2
0.25 |1000 >> 10000
nan | nan
                    """,
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    deposition_reaction_solutions_temperature = Quantity(
        type=str,
        shape=[],
        description="""
    The temperature of the reaction solutions.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the temperatures of the solutions associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If a reaction solution undergoes a temperature program, list the temperatures (e.g. start, end, and other important points) and separate them with semicolons, e.g. 25; 100
- When the temperature of a solution is unknown, state that as ‘nan’
- For reaction steps where no solvents are involved, state the temperature of the gas or the solid if that make sense. Otherwise state this as ‘nan’
- For values with uncertainties, state the best estimate, e.g. write 120 and not 110-130.
- Assume an undetermined room temperature to be 25
Example
25
100; 50 | 25
nan | 25 >> 25
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=['25', 'Unknown', '25 | 25']),
        ),
    )

    deposition_substrate_temperature = Quantity(
        type=str,
        shape=[],
        description="""
    The temperature of the substrate.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the temperatures of the substrates (i.e. the last deposited layer) associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- The temperature of the substrate refers to the temperature when the deposition of the layer is occurring.
- If a substrate undergoes a temperature program before the deposition, list the temperatures (e.g. start, end, and other important points) and separate them with semicolons (e.g. 25; 100)
- When the temperature of a substrate is not known, state that as ‘nan’
- For values with uncertainties, state the best estimate, e.g. write 120 and not 110-130.
- Assume that an undetermined room temperature is 25
Example
25
nan
125; 325; 375; 450 | 25 >> 25
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '25',
                    'Unknown',
                    '15',
                    '100',
                    '100 | 25',
                    '60',
                    '40',
                    '22',
                    '25 | 25',
                    '80',
                ]
            ),
        ),
    )

    deposition_thermal_annealing_temperature = Quantity(
        type=str,
        shape=[],
        description="""
    The temperatures of the thermal annealing program associated with depositing the layers
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the annealing temperatures associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If the thermal annealing involves a temperature program with multiple temperature stages, list the temperatures (e.g. start, end, and other important points) and separate them with semicolons (e.g. 25; 100)
- For values with uncertainties, state the best estimate, e.g. write 120 and not 110-130.
- If no thermal annealing is occurring after the deposition of a layer, state that by stating the room temperature (assumed to 25°C if not further specified)
- If the thermal annealing program is not known, state that by ‘nan’
Example
25
50 | nan
450 | 125; 325; 375; 450 >> 125; 325; 375; 450
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    '25',
                    '350.0',
                    '85',
                    '120 >> 120',
                    '400',
                    '80',
                    'Unknown',
                    '450.0',
                    '100',
                    '120',
                    '450 | 25',
                    '60',
                    '250.0',
                    '60; 120',
                    '450',
                    '150.0',
                    '25; 100',
                    '100 | Unknown',
                    '550.0',
                ]
            ),
        ),
    )

    deposition_thermal_annealing_time = Quantity(
        type=str,
        shape=[],
        description="""
    The time program associated to the thermal annealing program.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the annealing times associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If the thermal annealing involves a temperature program with multiple temperature stages, list the associated times at those temperatures and separate them with semicolons.
- The annealing times must align in terms of layers¸ reaction steps and annealing temperatures in the previous filed.
- If a time is not known, state that by ‘nan’
- If no thermal annealing is occurring after the deposition of a layer, state that by ‘nan’
- For values with uncertainties, state the best estimate, e.g. write 20 and not 10-30.
Example
nan
60 | 1000
30 | 5; 5; 5; 30 >> 5; 5; 5; 30
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '40.0',
                    'Unknown',
                    '30.0',
                    '20.0',
                    '15.0; 5.0',
                    '100.0',
                    '30.0; 30.0',
                    '60.0',
                    '15.0 >> 5.0',
                    '10.0',
                    '10.0 | Unknown',
                    '15.0',
                    '30.0 | Unknown',
                ]
            ),
        ),
    )

    deposition_thermal_annealing_atmosphere = Quantity(
        type=str,
        shape=[],
        description="""
    The atmosphere during thermal annealing
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the atmospheres associated to each annelaing step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- The number and order of layers and deposition steps must line up with the previous columns.
- If the atmosphere is a mixture of different gases, i.e. A and B, list the gases in alphabetic order and separate them with semicolons, as in (A; B)
- “Dry air” represent air with low relative humidity but where the relative humidity is not known
- “Ambient” represent air where the relative humidity is not known. For ambient conditions where the relative humidity is known, state this as “Air”
- “Vacuum” (of unspecified pressure) is for this purpose considered as an atmospheric gas.
- This is often the same as the atmosphere under which the deposition is occurring, but not always.
- This category was included after the projects initial phase wherefor the list of reported categories is
short. Thus, be prepared to expand the given list of alternatives in the data template.
Example
N2
Vacuum | N2
Air | Ar >> Ar
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=['Unknown', 'Air', 'Vacuum', 'N2', 'Air >> Air']),
        ),
    )

    storage_time_until_next_deposition_step = Quantity(
        type=str,
        shape=[],
        description="""
    The time between the back contact is finalised and the next layer is deposited
- If there are uncertainties, only state the best estimate, e.g. write 35 and not 20-50.
- If this is the last layer in the stack, state this as ‘nan’
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['Unknown', '24.0'])
        ),
    )

    storage_atmosphere = Quantity(
        type=str,
        shape=[],
        description="""
    The atmosphere in which the sample with the finalised back contact is stored until the next deposition step or device performance measurement
Example
Air
N2
Vacuum
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=['Dry air', 'N2', 'Unknown', 'Air']),
        ),
    )

    storage_relative_humidity = Quantity(
        type=str,
        shape=[],
        description="""
    The relive humidity under which the sample with the finalised back contact is stored until the next deposition step or device performance measurement
- If there are uncertainties, only state the best estimate, e.g write 35 and not 20-50.
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=['', '5.0', '10', '10.0']),
        ),
    )

    surface_treatment_before_next_deposition_step = Quantity(
        type=str,
        shape=[],
        description="""
    Description of any type of surface treatment or other treatment the sample with the finalised back contact is stored until the next deposition step or device performance measurement
- If more than one treatment, list the treatments and separate them by a double forward angel bracket (‘ >> ‘)
- If no special treatment, state that as ‘none’
- This category was included after the projects initial phase wherefor the list of reported categories is
short. Thus, be prepared to expand the given list of alternatives in the data template.
Example:
none
Ar plasma
UV-ozone
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    'EDA gas',
                    'DEDA gas',
                    'MEA immersion >> 125C 20 min',
                    'TETA gas',
                ]
            ),
        ),
    )

    def normalize(self, archive, logger):
        add_solar_cell(archive)
        if self.stack_sequence:
            archive.results.properties.optoelectronic.solar_cell.back_contact = (
                self.stack_sequence.split(' | ')
            )
