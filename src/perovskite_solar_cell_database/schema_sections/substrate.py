import numpy as np
from nomad.datamodel.data import ArchiveSection
from nomad.metainfo import Quantity

from .utils import add_solar_cell


class Substrate(ArchiveSection):
    """
    Information about the substrate used in the device. It describes the `substrate stack sequence`,
    the `substrate area`, the `substrate thickness`, and its provenance or fabrication method.
    """

    stack_sequence = Quantity(
        type=str,
        shape=[],
        description="""
    The stack sequence describing the substrate.
- With the substrate, we refer to any layer below the electron transport layer in a nip-device, and any layer below the hole transport layer in a pin-device.
- Every layer should be separ   ated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- If two materials, e.g. A and B, are mixed in one layer, list the materials in alphabetic order and separate them with semicolons, as in (A; B)
- Use common abbreviations when appropriate but spell it out if risk for confusion.
- There are a lot of stack sequences described in the literature. Try to find your one in the list. If it is not there (i.e. you may have done something new) define a new stack sequence according to the instructions.
ExampleBelow are some of the most common substrates
SLG | FTO
SLG | ITO
PET | ITO
PEN | ITO
SLG | AZO
PET | IZO
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=sorted(
                    [
                        'SLG | Ag-nw',
                        'Textile | PEN | ITO',
                        'PET | Ag',
                        'PEN | Graphene',
                        '42P2O5-22Li2O-22ZnO-12Sm2O3-2CeO2 | FTO',
                        'SLG | Cu-BHT',
                        'Mica | ITO',
                        'NOA88 | PEI | Au',
                        'Si | ITO',
                        'PEN | Graphene | MoO3',
                        'PET | Al2O3',
                        'PES | Ti | Graphene',
                        'SLG | Ag | Unknown',
                        'PEN | Ag-nw',
                        'Cu',
                        'Transparent wood | ITO',
                        'SLG | AZO',
                        'none',
                        'Ti-foil',
                        'Cellulose paper | Carbon black',
                        'SLG | FAZO',
                        'PDMS | PET | Au-grid',
                        'PEN | SWCNTs | MoO3',
                        'SrTiO3 | Sr2RuO4',
                        'SLG | In2O3:H',
                        'Epoxy | ITO',
                        'PES | ITO',
                        'Polyimide | ITO',
                        'Cellophane | TiO2 | Ag | TiO2',
                        'SiO2-mp | SLG | ITO',
                        'Polyimide | In2O3:H',
                        'Polyester-satin textile',
                        'NOA63 | Au',
                        'SLG | PEDOT:PSS',
                        'b-CNF | IZO',
                        'SLG',
                        'SLG | ITO:ATO',
                        'SLG | PET',
                        'Flexible | IZO',
                        'PET | TCE',
                        'SLG | AZO | Ag-nw | AZO',
                        'PET | PEDOT:PSS',
                        'Si',
                        'Pt',
                        'SLG | SU-8 | MoO3 | Au',
                        'SLG-HAMC-patterned | FTO',
                        'SLG | Cd2SnO4',
                        'PDMS | Graphene',
                        'PET | APTES; Graphene',
                        'PDMS | PET',
                        'SLG | Ni:Au-mesh',
                        'PEN | AZO',
                        'SLG | Ag-nw | Graphene oxide',
                        'SLG | Graphene | MoO3',
                        'Au | Ni | Al | Ti | GaN',
                        'Quartz | TaN',
                        'SLG | FTO | Au-grid',
                        'PDMS',
                        'PI | PEDOT:PSS',
                        'SLG | ITO | Au-grid | ITO',
                        'SLG | Au',
                        'SLG | PEDOT:PSS | Ag | PEI',
                        'Quartz | ITO',
                        'SLG | ITO | Au-grid | AZO',
                        'PEI | ITO',
                        'PES | FTO',
                        'PET | Ni-mesh:PH1000',
                        'PET | IWO',
                        'PI | Ag-np | PEDOT:PSS',
                        'PET | Ag-nw | FZO',
                        'SLG | WO3 | Ag | WO3',
                        'Willow glass | Graphene | Ag-nw',
                        'PAA-PEG | Ti',
                        'SLG | Au-np; Graphene; TFSA',
                        'PET | Ag-grid | PEDOT:PSS',
                        'PI',
                        'SLG | Ti',
                        'SLG | AZO:F',
                        'ITO | PET',
                        'SLG | MPTMS-SMA | Ag | MUTAB-SAM',
                        'PAA-PEG | Ti | PANI | Ti',
                        'SLG | Ag-nw; Graphene oxide',
                        'SLG | Graphene',
                        'SLG | ITO',
                        'Nb:SrTiO3',
                        'SLG | SWCNTs-HNO3',
                        'SiO2-hollow | SLG | ITO',
                        'PI | Cu-grid | Graphene',
                        'PEN | Graphene; MoO3',
                        'PET | Ag-grid',
                        'SLG | MSA-PEDOT:PSS',
                        'SLG | Ag-nw | AZO',
                        'NOA63 | MoO3 | Au',
                        'NOA63',
                        'PS',
                        'PES | PEDOT:PSS | Ag',
                        'Ag-nw; Graphene; Polycarbonate; Polystyrene',
                        'NOA63 | ITO',
                        'PET | ITO | Ag-nw',
                        'SLG | IZO',
                        'SLG | Graphene; TFSA',
                        'SLG | TiO2-c | SnO2-c | TiO2-c | SnO2-c | TiO2-c | SnO2-c | TiO2-c | SnO2-c | TiO2-c | ITO',
                        'SLNOA63 | CPI | Cr | Au-grid',
                        'SLG | APTES; Graphene',
                        'SLG | Au-np; Graphene',
                        'PET | AZO',
                        'Unknown',
                        'SLG | AZO | Cu-nw | AZO',
                        'Carbon-nt-yarn',
                        'PDMS | SLG | ITO',
                        'Cellophane | TiO2-c | Ag',
                        'SLG | ITO | ITO',
                        'PET | PEDOT:PSS | Ag-nw',
                        'PET | Ag-mesh:PH1000',
                        'PEN | Planarization | SiN | ITO',
                        'PET | AuCl3; Graphene',
                        'Silk | Ag-nw | PEDOT:PSS',
                        'PET | Graphene',
                        'PET | IZO',
                        'PET | Ag-nw; PEDOT:PSS',
                        'Quartz | Graphene',
                        'HCLaminate | IZO',
                        'Ti-wire',
                        'SLG | ITO-HMDS Scaffold',
                        'SLG | Cu-nw',
                        'PET | Ag-nw; Graphene oxide',
                        'PET | Ag-nw | Graphene',
                        'SLG | ZrO2 | MPTMS-SMA | Ag | MUTAB-SAM',
                        'PET | In2O3',
                        'Ti',
                        'PET',
                        'Carbon-nt-fiber',
                        'PEN | ITO',
                        'SLG | TiO2-c | Ag',
                        'Regenerated cellulose film | Ag-nw',
                        'SLG | Ag',
                        'PET | Graphene; TETA',
                        'Si | SiO2',
                        'SU-8 | Ca | Au',
                        'PET | FTO',
                        'PET | Ag-mesh | PH1000',
                        'PES | AZO | CuNW | AZO',
                        'Willow glas | Ti',
                        'PET | WO3 | Ag | WO3',
                        'SLG | Ni',
                        'Graphite',
                        'PET | Ag-nw',
                        'FPA-PDMS',
                        'Willow glass | ITO',
                        'SLG | SWCNTs',
                        'INVAR | ITO',
                        'SLG | SnO2 | SiO2 | FTO',
                        'PEG | ITO',
                        'PETUG',
                        'SLG | ZnO | ITO | Ag-nw | ITO',
                        'Ti-sheet',
                        'Unknown | ITO',
                        'SLG | FTO',
                        'PET | ITO',
                        'PES | AZO | Ag-nw | AZO',
                        'Willow glass | AZO',
                        'SLG | ITO | Ni',
                        'SLG | DWCNTs',
                        'PET | Au',
                        'Paper | Au',
                        'Steel',
                        'Nanopaper | TiO2 | Ag',
                        'PET | Au-np; Graphene; TFSA',
                        'PET | MSA-PEDOT:PSS',
                        'SU-8 | MoO3 | Au',
                        'SLG | PEI | Au',
                        'SLG | resist | ITO',
                        'PEN',
                        'SLG | SWCNTs | MoO3',
                        'SLG | WO3 | Ag',
                        'ITO | PEN',
                        'Ag-nw; GFRHybrimer; ITO',
                        'SLG | Ag-nw | Graphene',
                        'SLG | IWO',
                        'SLG | rGO',
                        'SLG | AZO | Au | AZO',
                        'Stainless steel',
                        'SLG | TCO',
                        'SLG | Au-grid | AZO',
                        'Willow glass | IZO',
                        'PET | SWCNTs',
                        'Cu-nw; GFRHybrimer; ITO',
                        'PEN | FTO',
                        'PEN | Ag-grid',
                        'SLG | Cu',
                        'SLG | FGZO',
                        'PET | APTES | AuCl3; Graphene',
                        'Foil | AZO',
                        'PET | AZO | Ag | AZO',
                    ]
                )
            ),
        ),
    )

    thickness = Quantity(
        type=str,
        shape=[],
        description="""
    A list of thicknesses of the individual layers in the stack. Use the following guidelines
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- The layers must line up with the previous filed.
- State thicknesses in nm
- Every layer in the stack have a thickness. If it is unknown, state this as ‘nan’
- If there are uncertainties, state the best estimate, e.g write 100 and not 90-110
- If you only know the total thickness, e.g. you have a 2 mm thick commercial FTO substrate and you do not know how thick the FTO layer is, state that as ‘2 | nan’
Example
2.2 | 0.1
2 | nan
nan | nan | nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    'nan | 140.0',
                    '2.0 | 0.0004',
                    'nan | 0.4',
                    '3.0',
                    '0.03 | 0.00015 | 2.0',
                    'nan | 332.0',
                    'nan | 35.0 | nan | 35.0',
                    '2.0 | 0.06',
                    'nan | 100.0',
                    '0.15',
                    '398.0',
                    'nan | 500.0',
                    'nan | 0.2',
                    'nan | 0.6',
                    'nan | 0.1',
                    '2.2 | nan',
                    'nan | 180.0',
                    'nan | nan',
                    '1.0 | 0.14',
                    '2.2 | 0.2',
                    '3.0 | nan',
                    '2.0',
                    'nan | 220.0',
                    'nan | 0.5',
                    'nan | 0.13',
                    'nan | 0.22',
                    '150.0',
                    'nan | 60.0',
                    '200.0',
                    'nan | 0.15',
                    'nan | 0.25',
                    '1.0 | 0.15',
                    'nan | 0.04',
                    '0.175 | 0.0025',
                    '2.2',
                    '1.0 | 0.13',
                    '2.0 | 0.6',
                    'nan | 40.0',
                ]
            ),
        ),
    )

    area = Quantity(
        type=np.dtype(np.float64),
        unit=('cm**2'),
        shape=[],
        description="""
    The total area in cm2 of the substrate over which the perovskite is deposited. This may be significantly larger than the cell area
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    supplier = Quantity(
        type=str,
        shape=[],
        description="""
    . The supplier of the substrate.
- Most substrates in the perovskite field are bought commercially, but if it is made in the lab, state this as “lab made”
- If the supplier is unknown, stat that as‘Unknown’
- This category was included after the projects initial phase wherefor the list of reported categories is short. Thus, be prepared to expand the given list of alternatives in the data template.
Example:
Lab made
NGO
Pilkington
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    'AimCore Technology',
                    'Lumtec',
                    'Yingkou OPV Tech New Energy Co.',
                    'Sigma Aldrich',
                    'Yingkou YouXuan',
                    'Unknown',
                    'Automatic Research GmbH',
                    'Xiang Science & Technology',
                    'Solaronix',
                    'OPV Technology Corp',
                    'Furuuchi Chemical',
                    'Thin Film Devices Inc.',
                    'Mekoprint OC50',
                    'Luminiscence Technology Corporation',
                    'Naranjo',
                    'Lab made',
                    'CSG Holding Co',
                    'Eastman Chemical Company',
                    'Naranjo substrates',
                    'Nippon Sheet Glass Co.',
                    'Pilkington',
                    'Advanced Election Technology',
                    'Kintec',
                    'Shen Zhen Hua Nan Xiang Cheng Factory',
                    'Hartford Glass Co.',
                    '3M',
                    'HeptaChroma',
                    'Merck',
                    'Delta Technologies',
                    'Ossila',
                    'AMG-Tech',
                    'Greatcell Solar',
                    'Xinyan Technology',
                    'Zhuhai Kaivo',
                ]
            ),
        ),
    )

    brand_name = Quantity(
        type=str,
        shape=[],
        description="""
    . The specific brand name of the substrate. e.g NGO11, TEC15, etc.
- This category was included after the projects initial phase wherefor the list of reported categories is short. Thus, be prepared to expand the given list of alternatives in the data template.
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    'TCO-XY15',
                    'Unknown',
                    'TEC15',
                    'TEC8',
                    'TEC14',
                    'Trizact 3000',
                    'FTO22-7',
                    'TEC7',
                    'TEC7.5',
                    'NSG10',
                    'DHS-FTO22-15N',
                    'TEC9',
                    'TCO22-7',
                    'TECS',
                ]
            ),
        ),
    )

    deposition_procedure = Quantity(
        type=str,
        shape=[],
        description="""
    . A list of the deposition procedures for the substrate
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- Make sure that you describe as many layers as there are layers in the stack. Otherwise it will be difficult to interpret which layer the deposition procedure is referring to. It should thus be as many vertical bars in this field as when describing the substrate stack.
- When more than one reaction step, separate them by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If the deposition procedure for a layer unknown, state that as‘Unknown’
- If a substrate is bought commercially and you do not know, indicate this by the label “Commercial”
- This category was included after the initial project release wherefor the list of reported purities are short, so be prepared to expand on the given list of alternatives in the extraction protocol.
Example
Commercial | Commercial
Commercial | Sputtered >> Sputtered
Commercial | ALD
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'Commercial | Commercial',
                    'Commercial | Electrodeposition >> Spin-coating',
                    'Commercial | Sputtering',
                    'Commercial | Electrospinning',
                    'Unknown',
                    'Commercial | Sputtering >> Sputtering',
                    'Commercial | commercial',
                    'Spin-coating | Commercial',
                    'Photolithography | Spin-coating | Lamination',
                    'Commercial | Laser patterning >> Spin-coating',
                    'Commercial | Spin-coating',
                    'CVD',
                    'Commercial | Magnetron sputtering',
                    'Commercial | ALD | Doctor blading | ALD',
                ]
            ),
        ),
    )

    surface_roughness_rms = Quantity(
        type=np.dtype(np.float64),
        unit=('nm'),
        shape=[],
        description="""
    The root mean square value (RMS) of the surface roughness expressed in nm
- If not known, leave this field blank
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    etching_procedure = Quantity(
        type=str,
        shape=[],
        description="""
    . For the most common substrates, i.e. FTO and ITO it is common that part of the conductive layer is removed before perovskite deposition. State the method by which it was removed
- If there is more than one cleaning step involved, separate the steps by a double forward angel bracket (‘ >> ‘)
- This category was included after the initial project release wherefor the list of reported purities are short, so be prepared to expand on the given list of alternatives in the extraction protocol.
Example
Zn-powder; HCl >> Mecanical scrubbing
Laser etching
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    'Unknown',
                    'Photolithography',
                    'Dipping in HCl',
                    'Laser etching',
                    'Zn-powder; HCl >> Mecanical scrubbing',
                ]
            ),
        ),
    )

    cleaning_procedure = Quantity(
        type=str,
        shape=[],
        description="""
    . The schematic cleaning sequence of the substrate. The Extraction protocol does not capture the fine details in the cleaning procedures, e.g. times, temperatures, etc. but state the general sequence. Refers to the cleaning of the entire substrate before the deposition of the rest of the cell stack starts.
- If there is more than one cleaning step involved, separate the steps by a double forward angel bracket (‘ >> ‘)
- If more than one procedure is occurring simultaneously, e.g. Soap washing an ultrasonic bath, separate simultaneously occurring steps with a semicolon.
- This category was included after the initial project release wherefor the list of reported purities are short, so be prepared to expand on the given list of alternatives in the extraction protocol.
Example
Helmanex >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> Acetone >> UV-ozone
Piranha solutionion
Piranha solutionion >> UV-ozone
Soap
Soap >> Ultrasonic bath
Soap >> Ultrasonic bath >> Ethanol; Ultrasonic bath >> Acetone >> UV-ozone
Soap >> Ultrasonic bath >> UV-ozone
Unknown
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=sorted(
                    [
                        'Water >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> heating >> UV-Ozone',
                        'Soap >> Ultrasonic bath >> Water >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> Ethanol >> Ultrasonic bath',
                        'Oxygen plasma',
                        'Soap >> Water >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> IPA >> O2-plasma',
                        'Soap >> Ultrasonic bath >> UV-Ozone',
                        'Water >> Acetone >> Ethanol >> UV-Ozone',
                        'De-ionized Water >> Ultrasonic bath >> Soap >> Ultrasonic bath >> IPA >> Ultrasonic bath',
                        'Soap >> Water >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> IPA >> UV-Ozone',
                        'Micro-90 detergent >> Ultrasonic bath >> DI Water >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> IPA >> Ultrasonic bath',
                        'Soap >> Water >> Ethanol',
                        'Helmanex >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> Acetone >> UV-Ozone',
                        'UV-Ozone',
                        'Soap >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> DI Water',
                        'Soap >> Water >> Ultrasonic bath >> IPA >> O2-plasma',
                        'Extran 300 >> Ultrasonic bath >> IPA',
                        'DI Water >> Ethyl alcohol >> Acetone',
                        'Soap >> Water >> Acetone >> IPA >> UV-Ozone',
                        'Toluene >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> Water >> Ultrasonic bath',
                        'Helmanex >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> IPA >> Ultrasonic bath',
                        'Soap >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> Ethanol',
                        'Soap >> Ultrasonic bath >> Water >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> UV-Ozone',
                        'Helmanex >> Ultrasonic bath >> DI Water >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> IPA >> Ultrasonic bath >> UV-Ozone',
                        'Water >> Acetone >> IPA',
                        'detergent >> deionized water >> isopropanol >> acetone >> UV-Ozone',
                        'Hellmanex >> solution >> DI >> water >> acetone >> IPA',
                        'Acetone >> Ultrasonic bath >> IPA >> Ultrasonic bath >> Ethanol >> UV-Ozone',
                        'Acetone >> Water >> IPA >> Nitrogen flow',
                        'Detergent >> Ultrasonic bath >> DI-Water >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> UV-Ozone',
                        'Helmanex >> Ultrasonic bath >> DI Water >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> IPA >> Ultrasonic bath >> O2 plasma',
                        'Helmanex >> Ultrasonic bath >> Water >> IPA >> Ultrasonic bath >> Acetone >> microwave plasma',
                        'Soap >> Ultrasonic bath >> Water >> Ultrasonic bath >> IPA >> UV-Ozone',
                        'Water >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> UV-Ozone',
                        'Water >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> Acetone',
                        'Soap >> Water >> Ultrasonic bath >> Ethanol >> O2-plasma',
                        'Soap >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> IPA >> Ultrasonic bath >> DI Water >> Ultrasonic bath >> Plasma',
                        'Soap >> Water >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> IPA',
                        'Soap >> Water >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> IPA >> UV-Ozone',
                        'Detergent >> Ultrasonic bath >> alkali liquor >> Ultrasonic bath >> DI Water >> Ultrasonic bath >> Ethanol >> Ultrasonic bath',
                        'Soap >> Water >> Ultrasonic bath >> Ethanol >> UV-Ozone',
                        'Acetone >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> Water >> Ultrasonic bath',
                        'Acetone >> Ultrasonic bath >> IPA >> Ultrasonic bath',
                        'Mucasol >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> Water >> Ultrasonic bath',
                        'Soap >> Water >> Ultrasonic bath >> Ethanol',
                        'Acetone >> Ultrasonic bath >> Abs Ethanol >> Ultrasonic bath >> DI Water',
                        'Soap >> Ultrasonic bath >> Water',
                        'Soap >> Water >> Acetone >> Water',
                        'Soap >> Water >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> Acetone >> UV-Ozone',
                        'Helmanex >> Ultrasonic bath >> Water >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> UV-Ozone',
                        'Acetone >> Ultrasonic bath >> IPA >> Ultrasonic bath >> Drying in oven >> UV-Ozone',
                        'Unknown >> O2 plasma',
                        'Water >> Ultrasonic bath >> IPA >> Ultrasonic bath >> O2-plasma',
                        'Detergent >> Ultrasonic bath >> DI Water >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> UV-Ozone',
                        'Water >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> IPA >> Ultrasonic bath >> UV-Ozone',
                        'H2O2/HCl/H2O = 1:1:5 >> acetone >> isopropyl alcohol',
                        'Soap >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> IPA >> Ultrasonic bath >> Water >> Ultrasonic bath >> O2-plasma',
                        'Soap >> Water >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> Ethanol >> IPA >> UV-Ozone',
                        'DI Water >> Ultrasonic bath >> Ethanol',
                        'DI Water >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> UV-Ozone',
                        'Unknown >> UV-Ozone',
                        'Helmanex >> Ultrasonic bath >> DI Water >> Ultrasonic bath',
                        'Mucasol >> Ultrasonic bath >> Water >> Ultrasonic bath >> Acetone >> IPA >> UV-Ozone',
                        'Acetone >> Water >> IPA >> Nitrogen flow >> Corona Treatment 0.74 kW',
                        'Soap >> Ultrasonic bath >> Water >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> Plasma',
                        'DI Water >> Ultrasonic bath >> Helmanex >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> Methanol >> Ultrasonic bath >> DI Water >> Ultrasonic bath >> UV-Ozone',
                        'Acetone >> Ultrasonic bath >> Methanol >> Ultrasonic bath',
                        'Soap >> Water >> Ultrasonic bath >> Acetone; IPA; Ethanol >> UV-Ozone',
                        'Soap >> Acetone >> Ultrasonic bath >> Water >> Ultrasonic bath >> Ethanol >> O2-plasma',
                        'Acetone >> Ultrasonic bath >> IPA >> Ultrasonic bath >> Ethanol >> Ultrasonic bath',
                        'Detergent >> Ultrasonic bath >> DI Water >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> Ethanol >> Ultrasonic bath',
                        'Acetone >> Ultrasonic bath >> Methanol >> Ultrasonic bath >> DI Water',
                        'Soap >> Ultrasonic bath >> Ethanol-HCl >> Ultrasonic bath >> Acetone >> Water >> Heating',
                        'Unknown',
                        'Water >> Ethanol >> IPA',
                        'Helmanex >> Ultrasonic bath >> IPA >> Ultrasonic bath >> Acetone >> UV-Ozone',
                        'Soap >> Ultrasonic bath >> Water >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> IPA >> Ultrasonic bath >> UV-Ozone',
                        'DI Water >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> IPA >> Ultrasonic bath',
                        'Helmanex >> Ultrasonic bath >> Ethanol >> Acetone',
                        'Soap >> Water >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> lPA;Acetone; Water >> Ultrasonic bath >> UV Ozone',
                        'Water >> Acetone >> IPA >> O2-plasma',
                        'Soap >> Ultrasonic bath >> Water >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> IPA >> Ultrasonic bath >> Plasma',
                        'Helmanex >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> Acetone >> DI Water',
                        'NaOH >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> DI Water >> Acetone',
                        'Acetone >> Ultrasonic bath >> IPA >> Ultrasonic bath >> O2-plasma',
                        'Soap >> Ultrasonic bath >> Water >> Ultrasonic bath >> Ethano >> Ultrasonic bath >> UV-Ozone',
                        'Soap >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> Acetone >> Plasma',
                        'Acetone >> Ultrasonic bath >> Isopropyl alcohol >> Ultrasonic bath >> de-ionized Water',
                        'Detergent >> Ultrasonic bath >> DI-Water >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> IPA >> Ultrasonic bath >> air plasma',
                        'Helmanex >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> DI Water >> Ultrasonic bath >> UV-Ozone',
                        'Soap >> peroxide/ammonia >> Ultrasonic bath >> Methanol >> Ultrasonic bath >> IPA >> UV-Ozone',
                        'Soap >> DIWater >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> IPA >> Ultrasonic bath >> N2 blowing >> UV-Ozone',
                        'Helmanex >> Ultrasonic bath >> Water >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> Acetone >> UV-Ozone',
                        'alconox-detergent >> Ultrasonic bath >> deionized water >> Ultrasonic bath  >> acetone >> Ultrasonic bath >> isopropanol >> Ultrasonic bath',
                        'Detergent >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >>  >> DI-Water >> Ultrasonic bath >> UV-Ozone',
                        'Water >> Acetone >> Ethanol >> IPA',
                        'Soap >> Water >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> Ethanol',
                        'Helmanex >> Acetone >> IPA >> O2-plasma',
                        'DIWater >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> IPA >> Ultrasonic bath >> UV-Ozone',
                        'Soap >> Ultrasonic bath >> Water >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> O2-plasma',
                        'Soap >> Water >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> lPA >>  >> Ethanol >> O2-plasma',
                        'Soap >> Water >> Toluene >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> IPA >> O2-plasma',
                        'detergent >> acetone >> isopropanol >> ethanol',
                        'Helmanex >> Acetone >> Ultrasonic bath >> IPA >> Ultrasonic bath >> O2 plasma',
                        'Acetone >> Ultrasonic bath >> Methanol >> Ultrasonic bath >> Water',
                        'Soap >> Water >> Acetone >> IPA >> Ethanol >> Water >> UV-Ozone',
                        'Soap >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> Acetone >> UV-Ozone',
                        'Mucasol >> Ultrasonic bath >> Acetone >> Utrasonic bath >> Acetone >> Ultrasonic bath >> IPA >> Ultrasonic bath >> Ozone',
                        'Acetone >> IPA >> O2 plasma',
                        'Soap >> Water >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> Ethanol >> O2-plasma',
                        'Soap >> Ultrasonic bath >> Water >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> IPA >> Ultrasonic bath >> O2-plasma',
                        'Soap >> Ultrasonic bath >> Water >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> Water >> Ultrasonic bath >> Ethanol >> Utrasonic bath >> UV-Ozone',
                        'Acetone >> Ultrasonic bath >> Methanol >> Ultrasonic bath >> Water >> Ultrasonic bath',
                        'Acetone >> IPA >> Water',
                        'Helmanex >> Ultrasonic bath >> DI Water >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> IPA >> Ultrasonic bath',
                        'Water >> Acetone >> IPA >> UV-Ozone',
                        'Helmanex >> Ultrasonic bath >> Water >> Ultrasonic bath >> Ethanol',
                        'Soap >> Ultrasonic bath >> Water >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> IPA >> Ultrasonic bath',
                        'Soap >> Acetone >> Ethanol >> Water >> UV-Ozone',
                        'NaOH Ethanolic solution >> Water >> detergent >> Water >> Dry air',
                        'Soap >> Ultrasonic bath >> Water >> Ultrasonic bath >> Ethanol >> UV-Ozone',
                        'Soap >> Ultrasonic bath >> de-ionized Water >> Ultrasonic bath >> Acetone >> UV-Ozone >> Ethanol >> UV-Ozone',
                        'Acetone >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> Water >> Ultrasonic bath >> UV-Ozone',
                        'DI Water >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> IPA >> Ultrasonic bath >> UV-Ozone',
                        '2.5 M NaOH >> Ultrasonic bath >> Water >> Detergent >> Milli-Q Water >> Annealed 30 min at 500℃',
                        'DIWater >> Ultrasonic bath >> Ethanol >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> Oven drying >> UV-Ozone',
                        'Helmanex >> Ultrasonic bath >> Water >> Ultrasonic bath >> Ethanol >> Ultrasonic bath',
                        'Soap >> Water >> Ultrasonic bath >> Acetone >> Ethanol >> Ultrasonic bath >> IPA >> UV-Ozone',
                        'Helmanex >> Ultrasonic bath >> DI Water >> Ethanol >> 2-propanol >> Ultrasonic bath',
                        'Soap >> Water >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> IPA >> O2-plasma',
                        'Soap >> Water >> Ultrasonic bath >> Acetone >> Ultrasonic bath >> IPA',
                    ]
                )
            ),
        ),
    )

    def normalize(self, archive, logger):
        add_solar_cell(archive)
        if self.stack_sequence:
            archive.results.properties.optoelectronic.solar_cell.substrate = (
                self.stack_sequence.split(' | ')
            )
