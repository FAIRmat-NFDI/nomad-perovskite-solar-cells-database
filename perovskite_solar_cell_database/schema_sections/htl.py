from perovskite_solar_cell_database.schema_sections.utils import add_solar_cell
from nomad.metainfo import Quantity
from nomad.datamodel.data import ArchiveSection

class HTL(ArchiveSection):
    """
    A section to describe information related to the Hole Transport Layer (**HTL**).
    """

    stack_sequence = Quantity(
        type=str,
        shape=[],
        description="""
    The stack sequence describing the hole transport layer. Use the following formatting guidelines
- With the HTL, we refer to any layer between the substrate and the perovskite in a pin-device, and any layer between the perovskite and the back contact in a nip-device.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- If two materials, e.g. A and B, are mixed in one layer, list the materials in alphabetic order and separate them with semicolons, as in (A; B)
- If no hole transport layer, state that as ‘non’
- Use common abbreviations when appropriate but spell it out if risk for confusion.
- If a material is doped, or have an additive, state the pure material here and specify the doping in the columns specifically targeting the doping of those layers.
- There is no sharp well-defined boundary between when a material is best considered as doped or as a mixture of two materials. When in doubt if your material is best described as doped or as a mixture, use the notation that best capture the metaphysical essence of the situation.
- There are a lot of stack sequences described in the literature. Try to find your one in the list. If it is not there (i.e. you may have done something new) define a new stack sequence according to the instructions.
Example:
Spiro-MeOTAD
PEDOT:PSS
none
NiO-c
PTAA
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['TAPC | MoO3; TAPC', '1‐adamantylamine hydrochloride | Spiro-MeOTAD', 'MDMO-PPV', 'TTPA-OMeTPA', 'NiO | Br-BA', 'P3CT-K', 'TPB', 'ZnBu4Pc', 'BuO-DATPA', 'FT-OMeTPA', 'BChl-2', 'Graphene oxide | CuBuPc', 'PTZDPP-2', 'Al2O3-mp | Me2N-DATPA', 'po-TPE-4DPA', 'TDAC', 'Au-np | NiO-c', 'B58', 'CuSCN-3D', 'HMDI', 'Me6-ZnPc', 'PMT', 'T103', 'Ag-np; NiO-c', 'NiO-np | TPI-4MEO', 'CsPbI3-QD | Spiro-MeOTAD', 'P(BDTT-SePPD)', 'PDBT-co-TT', 'GD; P3HT', 'KY7F22-np | Spiro-MeOTAD', 'PDBT-T1 | WOx', 'YT3', 'M116', 'CH3O-PEIA | Spiro-MeOTAD', 'HTM-2', 'TaTM | F6-TCNNQ; TaTm', 'PEDOT:PSS | Perylene', 'F6-TCNNQ | TaTm', 'V842', 'PEDOT:PSS | PSS-Na', 'NiO-c | PNP-BC', 'PEDOT:PSS | Au-np; VOx', '[BMPA-BTD]3-TPA', 'YKP06', 'DTBT', 'rGO-flakes | Spiro-MeOTAD', "9,9'-([1,2,5]thiadiazolo[3,4-c]pyridine-4,7-diylbis(4,1- phenylene))bis(N3,N3,N6,N6-tetrakis(4-methoxyphenyl)-9H-carbazole-3,6-diamine)", 'PFO | Al2O3-np', "4,4'-((2-Hexyl-2H-benzo[d][1,2,3]triazole-4,7-diyl)bis(thiophene5,2-diyl))bis(N,N-bis(4-(hexyloxy)phenyl)aniline)", 'TFB', 'V950', 'VOx | X-DVTPD', 'HB-Cz', 'C201', 'V1036', '2-MP | Spiro-MeOTAD', 'SWCNTs | PTAA', 'HTM4', 'H-2,3', 'MoS2', 'CON-10 | PEDOT:PSS', 'PEDOT:PSS | PTB7', 'YKP03', 'TPA-NAP-TPA', 'PTAA | TPFB', 'TTPA-DTP', 'CS05', 'SGT-407', 'CuPcNO2-OBFPh', 'EGO-PPV', 'RE-ZnBu4Pc', 'CdSe-QD | Spiro-MeOTAD', 'NiO-c | 1ab', 'MoOx | F4TCNQ', 'WS2', 'WO3', 'dly-2', '18-crown-6 ether | CuSCN', 'MoO3 | TBDI', 'BDTT:DPPD:TT', 'SY3', 'TTF1', 'PT', 'Tea Catachinrich biomolecules', 'PEH-9', 'NiO@C | Spiro-MeOTAD', 'ST1 (4-(4-(bis(4-(4-(dibutylamino)styryl)phenyl)amino)styryl)-N,N-dibutylaniline)', 'NiO-c | NBP-BC', 'CuPc-DMP', 'SGT-405', 'AL2O3-c | Spiro-MeOTAD', 'PTAA', 'di-TPA', '2-((5-(4-(2-ethylhexyl)-4H-dithieno[3,2-b:2′,3′-d]pyrrol-2-yl) thiophen-2-yl)methylene) malononitrile', 'PBDT(T)(2F)T', 'PPP', 'B[BMPDP]2', 'V873', '9,9’-di{6-[3-(2-(4-methylphenyl)vinyl)-9-carbazol9-yl]hexyl}-[3,3’]bicarbazole)', 'Caffeine | Spiro-MeOTAD', 'Poly-TBD', 'X60', 'HOFP | Spiro-MeOTAD', 'NP1', 'CuBuPc', 'PolyTPD | Spiro-MeOTAD', 'Al2O3-c | Ethyl acetate; I2; LiI; NMBI; Urea', 'PVBT-SO3', 'Spiro-MeOTAD | Cu1.75S', 'FBT-TH4 | CuxO', 'PTB1', 'Z34', 'PSS-g-PANI', 'MEAI | Spiro-MeOTAD', 'NiO-np | PMMA', 'M118', 'DPA-ANR-DPA', 'YR3', 'V997', 'DBT(QT-TPA)2', 'SO10', 'TaTm | TaTm:F6-TCNNQ', 'TBDI', 'PO-Spiro', 'TTPA-DSQT', 'Spiro-MeOTAD | PDPP4T', 'SnS-np; ZnS-np | NiO-np', '1b @ triphenylamine modified azobenzene dyes', 'THY-1', 'SP-11', 'Zeocoat | Graphene | P3HT', 'P3HT | Spiro-MeOTAD', 'H11', 'CuI | PEDOT:PSS', 'PTAA | PFN-P2', 'PTTh', 'TaTm | TPBi | MoO3', 'DEH', 'Perylene', 'PEDOT:PSS | pTPD', 'SDTCz2F', 'TCTA-BVP', 'EDT; PbS', 'PDCBT', 'NiO-c | Au-np', 'MeOAc-Spiro-OMeTAD', 'C102', '3,4-spiro', 'PTPD2', '3,3′,5,5′-tetrasubstituted 1,1′-biphenyl', 'X14', 'H101', 'POZ6-2', '1a @ triphenylamine modified azobenzene dyes', 'PEDOT:PSS | TPA-NPA-TPA', 'SubPc', 'Z10', 'OIPC-Br', '4b @ triphenylamine modified azobenzene dyes', 'X54', 'TPAC3M', '5,7-disubstituted azulene', 'CZTPA-1', 'NiO-np | TPI', 'P3HT | Ta:Wox-np', 'FT73', 'TDT-OMeTAD', 'AQ310 | Spiro-MeOTAD', 'Spiro-MeO-TPD', 'BL40', 'PEDOT:SAF', 'YC-3', 'TPA3C', 'V1056', 'SCPDT-BiT', 'NiO-np | 2,2’-BiPy', 'Fe3O4-np', 'Carbozole @ S14', 'PZn-DPPA', 'X2', 'SFD-Spiro', 'SWCNTs', 'HTB-Ome', 'CZTSSe; rGO', 'Q198', 'EVA; MWCNTs | Spiro-MeOTAD', 'BTPA', 'CsSnBr2I-QDs', 'MeoTPD', 'CuH', 'V2O5', 'HTM2', 'Graphene oxide | PTAA', "N2,N2,N3',N3',N6',N6',N7,N7-octakis(4-methoxyphenyl)spiro[fluorene-9,9'-xanthene]-2,3',6',7-tetraamine", 'M114', 'Benzylamine | Spiro-MeOTAD', 'pPh-2MODPACz', 'PMA | TaTm', 'DERDTS-TBDT', 'TTB3', 'BMIMBF4 | Spiro-MeOTAD', 'NBP-BC', 'TB-ZnPc', '(OctPhO)8CuPc1', 'PEDOT:PSS | V2O5', 'BTP-1', 'M4', 'Benxylamine | Spiro-MeOTAD', 'BDT-4D', 'oxo-Graphene', "4,4'-(5,10,11-Trihexyl-10,11-dihydro-5H-thieno[2′,3':4,5]pyrrolo [3,2-g]thieno[3,2-b][1,2,3]triazolo[4,5-e]indole-2,8-diyl)bis(N,N-bis(4- (hexyloxy)phenyl)aniline)", 'PEDOT:PSS; PEG', 'Spiro-MeOTAD | Al2O3-c', 'mm-SFX-2PA', 'Spiro-tBuBED', 'PTB-BO', 'V1004', 'CZTS0.5Se0.5; rGO', 'MPA', 'PTAA | PS', 'P-SC6-TiOPc', 'PBDT(2H)T', 'POZ2', 'PIF8-TAA', 'Spiro-PT-OMeTAD', 'BT', 'BTPA-TCNE', 'NiMgO', 'POZ9', 'Thiophene | Spiro-MeOTAD', 'HMe2Pc', 'TCPI | Spiro-MeOTAD', 'NiO-c | 1bb', 'PCDTBT; PFN', 'MoO2-np', 'Carbon-nt; PEDOT:PSS | PEDOT:PSS', 'Graphene oxide; PEDOT:PSS', '4-(4-phenyl-4-alfa-naphthylbutadienyl)-N,N-di(4-methoxyphenyl)-phenylamine', 'YC03', 'tetra-TPA', 'MHGO', 'P:ON', '1,3-disubstituted azulene', 'Ni | Au | Cu', 'M113', '2FBTA-2', 'NiO-c | NiO-np', 'DDOF', 'Trux-OMeTAD', 'PB2T-S', 'PEDOT:PSS | CuI', 'PEDOT:PSS | FrGO', 'PCE-10', 'HAB1', '2,7-BCz-OMeTAD', '2,5-bis (5-(5-(5-hexylthiophen-2-yl) thiophen2-yl) thiophen-2-yl) thiazolo[5,4-d]thiazole', 'BTF2', 'PEDOT:PSS | P3HT', 'CS04', 'PB(NAP-Th)TBT', '[BMPA-EDOT]3-TPA', '18-crown-6 ether | Spiro-MeOTAD', 'T30P', 'MoOx | TaTm', 'Z7', 'P(BDTT-ttPPD)', 'PEDOT:PSS | Porphyrin', 'Q221', 'SQ2 | Spiro-MeOTAD', 'Tetracene', 'TS-CuPc | PEDOT:PSS', 'D1', 'PTAA | Al2O3-mp', 'P3CT', 'MoO3', 'BTPA-5', 'P3HT', 'MoO3 | CuPc', 'V1012', 'EDOT-OMeTPA', 'CdTe@MAPbI3-QDs | Spiro-MeOTAD', 'NPD', 'Zn-Chl | H2-Chl', '3C', 'FBA2', '4-(2-(4-(Bis(4-(hexyloxy)phenyl)methyl)phenyl)-9-methyl-9H-naphtho[2,1-c]carbazol-12-yl)-N,N-bis(4-(hexyloxy)phenyl)aniline', 'ZnChl-3', '2TPA-3-DP', 'Spiro-MeOTAD | P3HT; SWCNTs | PEDOT:PSS', '2D-Sb', 'SY2', 'SFT-TPAM', 'Al2O3-np | CuBuPc', 'Th-PDI', 'TAA14', 'DPP-F', 'B74', 'Al-np; PEDOT:PSS', 'CuSCN | MoOx', 'I2; KI; Propylene carbonate; Polyethylene glycol', 'Z25', 'Black phosphorous 2D | CuSCN', 'Spiro-TTB | VOx', 'TPBC', 'POSS-SH | Spiro-MeOTAD', 'CZ-STA', 'PEDOT:PSS | 3-aminopropanoic acid-SAM', 'A-PDTON | PEDOT:PSS', 'T102', 'NO-Graphene-QDs', 'PTPD', 'Cu2MnSn4-np', 'PffBT4T-20D', 'M101', 'I2; LiI; Methoxypropionitrile', '3,6-di(2H-imidazol-2-ylidene)cyclohexa 1,4-diene-C12', 'TAE', '4-chlorothiophenol', 'X-DVTPD', 'HTM3', '1-(N,N-di-p-methoxyphenylamine)pyrene', 'MEH-PPV | Spiro-MeOTAD', 'pm-TPE-4DPA', 'MoOx', 'P3CT-N', 'TTh101', 'TP1', 'CZTS', 'CT2', 'PEH-1', 'KR355', 'Poly(3-bromothiophene)', 'rGO-4FPH | Spiro-MeOTAD', 'TZ3', 'PEDOT:PSS', 'FTA2', 'FrGO', 'CzPAF-TPA', 'MeO-DATPA', 'PEDOT:LS', 'MTA', 'PCPD2FBT:BCF', 'SO8', '4-F-br-4C', 'Polymer3', "3,3'-(2,7-bis(bis(4-methoxyphenyl)amino)-9H-fluorene-9,9-diyl)bis(N-ethyl-N,N- dimethylpropan-1-aminium) bis(trifluoromethanesulfonyl)imide", 'PTB7-th', 'BTT-5', 'CuInS2 | Al2O3-mp', 'BTF1', 'DCZ-OMeTAD', 'NiO-c | CuI', 'TPA-Pc', 'P', 'Spiro-MeOTAD-F', 'Cu:NiO', 'Graphene-QDs', 'F33', 'PCDTBT8', 'X59', 'NiO-c | BMIMBF4', 'rGO', 'P3DDT', 'X21', 'TPASBP', 'poly(DTSTPD-r-BThTPD)', 'PEDOT:PSS | Propionic acid', '1d @ triphenylamine modified azobenzene dyes', 'CuPc-Bu', 'MoS2; PEDOT:PSS', 'Al2O3-np | Spiro-MeOTAD', '3-Hexylthiophene | Spiro-MeOTAD', 'COTT-1', 'Graphene aerogel | Spiro-MeOTAD', 'PCP-Na', 'X19', 'IDF-SFXPh | MoO3', 'DPA-TPM', 'Co0.817Cu0.183O1.19', 'DBTMT', 'BTT-Me', 'Carbon-QDs', 'Polystyrene | Spiro-MeOTAD', 'PEDOT:MNSF', 'TOPO | TaTm', 'PEDOT:PSS | PEDOT:GSL', 'BTDTP', '9,9-bis(3-(dimethylamino)propyl)-N2,N2,N7,N7-tetrakis(4-methoxyphenyl)-9H-fluorene- 2,7-diamine', 'Spiro-MeOTAD; X60', 'CT1', 'PBDTT', 'PDO1', 'TTB1', 'JY7', '4,8-bis-(5-bromothiophene-2-yl)-benzo thiadiazole', 'TbT-3', 'BL51', 'NiO-c | N719 dye', 'Aniline | Spiro-MeOTAD', 'KM03', 'PF8-TAA', 'H66', 'ZnPcNO2-OBFPh', 'alfa-NPD', 'WO3-nw@PEDOT', 'NP-BC', 'COTT-2', 'PEG | Spiro-MeOTAD', 'PPDI | Spiro-MeOTAD', 'PFBT-Na', 'FePc-Cou', 'PVBT-SB', 'PAH 2', 'N1,N3,N5-tris(4-n-butylphenyl)-N1,N3,N5-triphenylbenzene-1,3,5-triamine', 'Au; NiO', 'IEICO; PBDTTT-E-T', 'HPB-Ome', 'V911', 'Bis-amide-TTF', 'Aminothiazolium iodide | P3HT', 'S5', 'NiO-c | NP-BC', 'TFB | P3HT', 'PEDOT:PSS | PTPAFSONa', 'M2', 'PVP | Spiro-MeOTAD', 'BTTP-CN', 'X36', 'TiS2-np', 'YK2', 'PEDOT:PSS | PEI', 'PEDOT:PSS | CrO3', 'ZnMe2Pc', 'NiO-c | PFN-P2', 'Poly(TA) | Spiro-MeOTAD', '2‐aminoterephthalic acid | Spiro-MeOTAD', 'Co0.39Cu0.61O', 'Ethyl acetate; I2; LiI; NMBI; Urea', 'H-Z2', 'MeO-2PACz', 'PEDOT:PSS; PEI | PEDOT:PSS', 'DTB', 'CuMePc', '3-hydroxypyridine | Spiro-MeOTAD', 'TPB(2-MeOTAD)', 'Mo(tfd-COCF3)3 | SWCNTs | Spiro-MeOTAD', 'Spiro-MeOTAD | Rubrene', 'CA-Br; TPA-PT-C6', 'PEDOT:PSS; V2O5', 'Z28', 'CISZ-QDs', 'PTB7', 'LiNiO-c', 'A101', 'PVBT-TMA', 'SAF-5', 'M117', 'PBDTTT-E-T | MoO3', 'PD-10-DTTE-7 | Spiro-MeOTAD', "4,4'-(1,3,4-Oxadiazole-2,5-diyl)bis(N,N-bis(4-methoxyphenyl)aniline)", 'WY-3', 'X55', 'BL25', 'pBDT-BODIPY | PFN', 'CuGaO2-np', 'NiO-np | PSS', 'pDPA-DBTP', 'BL52', 'CuCo2O4', 'PEDOT:PSS | PBDB-T:ITIC', 'HFB-OMeDPA', 'VOx | PEI', 'ATT-OHex', 'N-CuMe2Pc', 'PEDOT:PSS | Au-nw; VOx', 'CrO2', 'CoO', 'P5', 'M102', 'V1013', 'BX-OMeTAD', 'PEDOT:PSS; Graphene oxide', 'TAE4', 'TPADPP-2', '3-F-br-4C', 'MoS2-QDs; rGO-flakes | Spiro-MeOTAD', 'Polyacrylonitrile-grafted rGO', 'D101', 'V2Ox', 'TbT-2', 'PEDOT:PSS | NiO-c', 'IDT-TPA', 'NaYF4:Yb:Tm-np | Spiro-MeOTAD', 'PBDTTT-CT | Spiro-MeOTAD', 'CzPAF‐SBF', 'BTT(DPP-Th)3-EH', 'PTZ-TPA', 'PBDTT-FTTE', 'SGT-420', 'P2Z1', 'C6TBPH2', 'PMMA | DTPC8-ThTPA', 'PEDOT:PSS | X-QUPD', 'V1209', 'HBT-ZnPc', 'CuInS2@ZnS-QDs', 'PEDOT:PSS | Au-nanobipyramide; VOx', 'ZnPcNO2-OPh', 'Rubrene', 'tert-CuBuPc', 'PCBM-60', 'SM01', 'X51', 'P3HT; Spiro-MeOTAD', 'OMe-TATPyr', 'Azomethine', 'DCZ-OMeTPA', 'SWCNTs | P3HT', 'Co0.817Cu0.183O', 'Y3', 'N2,N,N8,N8-tetrakis[2,2-bis(4-methoxyphenyl)ethenyl]-4,10-dimethyl-6H,12H-5,11-methanodibenzo[b,f][1,5]diazocine2,8-diamine', 'PEDOT:PSS | AuAg@SiO2-np', 'PZn-TPA', 'TPD', 'Ph-TPA-4A', 'IDTT-TPA', 'TRUX1', 'Ta2O5 | Spiro-MeOTAD', '2mF-X59', 'YC-1', 'PMMA | Spiro-MeOTAD', 'LHTM-2', 'In2O3', 'TSHBC-CF3', 'PTAA | PFN', 'Spiro-TBB', 'HPPHT', 'Poly[4,8-bis(2-(4-(2-ethylhexyloxy)phenyl)-5-thienyl)benzo[1,2-b:4,5b’]dithiophene-alt-1,3-bis(4-octylthien-2-yl)-5-(2-ethylhexyl)thieno[3,4-c]pyrrole-4,6-dione', 'SFX-TPA', 'PEDOT; Graphene', '3,6-Cbz-EDOT', 'TPE-2,7-Carbazole W4', 'Choline chloride | Spiro-MeOTAD | SWCNTs', 'H-Z1', 'PEDOT:PSS | Dex-CB-MA', 'TTB2', 'COPV4', 'Cu0.8Cr0.2O2', 'Cz-OMeTAD', 'Cu3PS4-np', 'PDPPDBTE', 'NO2-PEIA | Spiro-MeOTAD', 'P3HT; SWCNTs; Spiro-MeOTAD', 'BL38', 'PEDOT:PSS | V2Ox', 'Co0.939Cu0.061O', 'Carbon-nt | PEDOT:PSS', 'DM2', 'CuI-np', 'PCz', 'H-3,4', 'TPA-ZnPc', 'TTz-1', 'Z1012', 'NH2-POSS | Spiro-MeOTAD', 'EP02', 'Triazine | Spiro-MeOTAD', 'Z7@MWCNTs', 'N3,N3,N9,N9‐tetrakis(4‐methoxyphenyl)xantheno[2,1,9,8‐klmna]xanthene‐3,9‐diamine', 'H65', 'ZnPc | Spiro-MeOTAD', 'AS44', '2FBTA-1', 'V886', 'PFB', 'IEICO; PBDB-T', 'NiO | CuSCN', 'PSQ1', 'M109', 'TRUX2', 'Spiro-MeOTAD | NaYF4', 'Poly-N-vinylcarbazole | Spiro-MeOTAD', 'Azu-Hex', 'p-DTS(FBTTh2)2', 'NiO-c | PCDTBT', 'TCP-OH', 'CuIn1.5Se3-QDs', '3,6-cbz-EDOT', 'SO9', 'DOR3T-TBDT; PCBM-70', 'TPD | HAT-CN', 'AZ2', 'CuPcNO2-OPh', 'TPAC-SAM', 'Yih-1', 'V885', 'NiS', 'IT-4F; PBDB-T-SF', 'CuO', 'HBZ-70', 'NiO-np | ME2', 'OCNR; PEDOT:PSS', 'M:ON', 'P1-2', 'WY-1', 'TZ1', 'pBBTa‐BDT2', 'mm-SFX-3PA', 'EHCz-2EtCz', 'VB-Me-FDPA', 'TPA1C', 'H6-ZnPc', 'Fluorene-dithiophene', 'quart-p-phenylene1', 'NiO-c | NiO-c', 'PDTSTTz', 'PDCBT | MoO3', 'Graphene oxide | PMMA', 'H-FL', 'none', 'BTF3', 'YC02', 'Carbon-nt; P3HT | PEDOT:PSS', 'Al2O3-c | Spiro-MeOTAD', 'PEDOT:PSS | PDPP-DTT', 'Spiro-MeOTAD | Al2O3', 'Tris(4-(5-hexylthiophen-2-yl)phenyl)amine', 'NBNDD', 'TAZ-[MeOTPA]2', 'TPB-2-MOTPA', 'N,N‐di‐p‐methylthiophenylamine', 'TPC', 'SrGO', 'PEH-8', '2PACz | MeO-2PACZ', 'PEDOT:PSS | PEI-HI', 'HL-1', 'Zn-Chl', 'POZ3', 'CZTS; rGO', 'PEDOT:PSS | Ethylene glycol', 'HT-ZnPc', 'LiMgNiO', 'BTTI-C8', 'X60(TFSI)2', 'CZTSe-QDs', 'RCP-BTT', 'NiO-c | YC-1', 'NiO-np | NaCl', 'PEO; KI; I2', 'rGO | PEDOT:PSS', 'KR133', 'Cz-N', 'CuI | Cu@CuI-nw', 'styryl-functionalized GO', 'H18', 'CuPc‐OTPAtBu', 'KR122', 'IDTC4-TPA', 'Vox | X-DVTPD', "N2,N2,N2',N2',N7,N7,N7',N7'-octakis(4-methoxyphenyl)spiro[fluorene-9,9'-xanthene]-2,2',7,7'-tetraamine", 'ZnPc-th-ZnPc', 'Tetrakis-Triphenylamine', 'CuPc-OBu', 'MeO-PPV | PFN-P2', 'J1', "5,5',5''-(5,5',5''-(nitrilotris(benzene-4,1-diyl))tris(furan-5,2-diyl))tris(2-octylisoindoline-1,3-dione)", "N2,N2,N7,N7-tetrakis(4-methoxyphenyl)spiro[fluorene-9,9'-xanthene]-2,7-diamine", 'ZPPHT', 'Y2A2', 'BL50', 'LiI; I2; Methoxyacetonitrile', 'TPP-OMeTAD', 'Cu(In0.5Ga0.5)S2-np', 'PBTTT', 'PEDOT:PSS | NiPcS4', 'NiMgLiO-c', 'S2', 'TTA', 'FT37', 'PASQ-IDT', '2D-PT', 'Graphene oxide | P3HT', 'PolyTPD | Al2O3-mp', 'PEDOT:PSS | PTPADCF3FSONa', 'CS03', 'MeO-PheDOT', '1c @ triphenylamine modified azobenzene dyes', 'XY1', 'mp-SFX-2PA', 'F4-TCNQ | CuPc', 'PEDOT:PSS | NaI', 'TTB-TTQ', 'Rubene | P3HT', 'TPA-CN', "4,4'-((2-Hexyl-2H-benzo[d][1,2,3]triazole-4,7-diyl)bis(thiophene5,2-diyl))bis(N,N-bis(4-methoxyphenyl)aniline)", 'M7-TFSI', 'DPA-ANT-DPA', 'CZTS-QDs', 'TAZ-[MeOTPATh]2', 'TPE-4DPA', 'LiCoO2', 'Graphene oxide; MoOx-np', 'TTA3', 'PTB9', 'iPrO-DATPA', 'PEH-2', 'EtO-DATPA', 'S,Si‐heteropentacene', 'XSln847', 'PFB | Al2O3-np', 'NiO-mp | Spiro-MeOTAD', 'PVCz-OMeDPD', 'MoO3 | TPTPA', 'CZTS0.75Se0.25; rGO', 'Graphene oxide | Spiro-MeOTAD', 'NiPcS4 | PEDOT:PSS', 'KR131', 'NiMgO | PVP', 'Adamantane | Spiro-MeOTAD', 'TAE3', 'PM-Spiro', 'PZn-3FTPA', 'TPBS', 'P3HT-MoS2', 'NiO-np | Graphene oxide', 'Al2O3 | CuPc(tBu)4', 'V1036:C2', 'Al2O3 | Sym-HTPcH', 'VO', 'Y4', 'Cu2O', 'GeO2', 'JY5', "N 4 ,N 4'-(4,10-dimethyl-6H,12H-5,11-methanodibenzo[b,f][1,5]diazocine-2,8-diyl)bis(N 4 ,N 4' ,N 4' - tris(4-methoxyphenyl)-[1,1'-biphenyl]-4,4'-diamine)", '2TPA-4-DP', 'Cu2O | PEDOT:PSS', 'TTBCPE', 'PEAI | Spiro-MeOTAD', 'CuO-nw | PEDOT:PSS', 'Cu0.5Cr0.5O2', 'Q216', 'M112', 'Co0.878Cu0.122O', 'Chl‐1', 'C8Br | Spiro-MeOTAD', 'Al2O3 | CuSCN', 'Zr(acac)4', 'THY-5', 'M104', '2,7-Ben', 'XMP', 'BTT-OMe', 'CuInSe2-QDs', '1,2-Bis[3,6-(4,4`-dimethoxydiphenylamino)-9H-carbazol-9-methyl]benzene', 'MC-43', 'CuPc(tBu)4', 'MoO3 | NPB', 'CW5', 'mGO | P3HT', 'PEDOT:PSS | PCDTBT', 'Cu2BaSnS4', 'CuFeO2-np', 'PPyra-ACD', 'P3CT-K | CuZnS', 'NiO-mp', 'P1Z2', 'X1', 'H-Tri', 'Hexakis[4-(N,N-di-p-methoxyphenylamino)phenyl]benzene', 'PMMA | DTPC13-ThTPA', 'CS02', 'BDTS-2DPP', 'XPP', 'CuMePy', 'CH3-PEIA | Spiro-MeOTAD', 'P:OO', 'Spiro-MeOTAD | Cu9S5-np', '2-(3,5-bis(5-(5-hexylthiophen-2-yl)thiophen-2-yl)thiophen-2-yl)-3,5-bis(5-(5-hexylthiophen-2-yl)thiophen-2-yl)thiophene', 'PZn-DPPA-O', 'MEH-PPV | PEDOT:PSS', '4-(5-(5-(5-(5-(5-hexylthiophen-2-yl) thiophen-2-yl) thiophene-2-yl) thiazolo[5,4-d]thiazol-2-yl) thiophene2-yl)-N,N-diphenyl-benzenamine', 'Graphene', 'V1091', '3,6-2,7-PCzTPA', 'PEDOT:PSS | Au@SiO2-np', "Poly[4,8-bis(2-(4-(2-ethylhexyloxy)3,5-fluorophenyl)-5-thienyl)benzo[1,2-b:4,5-b']dithiophenealt-1,3-bis(4-octylthien-2-yl)-5-(2-ethylhexyl)thieno[3,4-c]pyrrole-4,6-dione", 'FeS2', 'NiO | Spiro-MeOTAD', 'Ome-DPA-CuPc', 'PTPD | Spiro-MeOTAD', 'NiO-np | M2', 'Bi2Te3 | Spiro-MeOTAD', 'DPEDOT-B[BMPDP]2', 'Florinated polymer | Spiro-MeOTAD', 'DA-PEDOT:PSS', 'Poly(ethylene oxide)', 'BChl-3', 'H-Tetra', 'Graphene oxide | PTFTS', 'PbPc', 'benzo[1,2b:4,5b′]-dithiophene', 'SGT-410', 'P3HT | Carbon-nt', 'NiO-np | Glycerol', 'PEDOT:PSS | PTAA', 'HS-Ph-CN | Spiro-MeOTAD', 'Theobromine | Spiro-MeOTAD', 'NiMgLiO | 5-AVA', 'PTB7-TH; PFN', 'P6', '[BMMIm]Cl', 'NiO-np | CuSCN', 'M106', 'SM-1', 'VOx | APPA', 'PEDOT:PSS | PEG', 'CJ-01', 'sGO', 'C4Br | Spiro-MeOTAD', 'Graphene oxide | PEDOT:PSS', "(2Z,2'Z)-2,2'-((10-(2-ethylhexyl)-10H-phenothiazine-3,7-diyl) bis(4,1- phenylene)) bis(3-(4-(diphenylamino) phenyl) acrylonitrile", 'SWCNTs | Graphene oxide | PMMA', 'Z9', 'TAPC', 'V1102', 'Ph-TPA-6A', 'nPrO-DATPA', '2,5-bis (5-(5-(5-hexylthiophen-2-yl)thiophen-2-yl) furan-2-yl) thiazolo[5,4-d] thiazole', 'TBP', 'TSHBC-tBu', '(OctPhO)8ZnPc2', 'NiO-c | Al2O3-mp', 'TB(MA)', 'P2', 'ZnBChl', 'PEDOT:PSS | GeO2', 'PPN', 'OMeTP-SAM', 'PEO | Spiro-MeOTAD', 'PEDOT:PSS | PFI', 'TQ1d', 'NiO-np', 'V1021', 'CoOx', 'P3HT | SWCNTs | PMMA', '5,6,11,12-Tetraphenylnaphthacene', 'Spiro-MeOTAD | PEDOT:PSS', 'Black phosphorous nanosheets', 'MC6Cz-TPA', 'CsSnI3-QDs', 'CuPc | PEI', 'ETH44', 'O5H-OMeDPA', 'HTM-3', 'PTB7-Th | MoOx', 'r-GO-HBS', 'PHPT-py', 'TET', 'NO HTL', 'PTAA | PEDOT:PSS', 'NiO-c | PEDOT:PSS', '[Fe(bpyPY4)](OTf)2.5', 'Diketopyrrolopyrrole', 'F101', 'CPE-Na', 'ZnChl-2', '3-Dodecylthiophene | Spiro-MeOTAD', 'BL08', 'PBDB-T | Spiro-MeOTAD', 'CuGaO2-mp', 'CuInS | Spiro-MeOTAD', 'MEH-PPV', 'TAE1', 'CL1-2', 'PII2T8T', 'NiO-c | SY4', '3,8,13-tris[2,2-bis(4-methoxyphenyl)ethenyl]-5,10,15-triethyl-10,15-dihydro-5H-indolo-[3,2-a:3′,2′-c]carbazole', '5,7-bis(9-ethyl-9H-carbazol-3-yl)-2,3-dihydrothieno[3,4-b][1,4]dioxine', 'H-Z3', 'PZn-FTPA', 'Ni | NiMgO', 'CZTS0.25Se0.75; rGO', 'FA-MeOPh', 'PTEG', 'Me-QTPA', 'MeO-PPV', 'H112', 'MoOx | PEDOT:PSS', 'CzPAF‐SBFN', '4,4′-(9-Methyl-9H-naphtho[2,1-c]carbazole-2,12-diyl)bis(N,N-bis(4-methoxyphenyl)aniline)', 'NiO-np | M3', 'PEDOT:PSS | Carbon-nt', 'Au@SiO2-nw | Spiro-MeOTAD', 'Pyridine | Spiro-MeOTAD', 'PEDOT:PSS | PTPD', 'PARA1', 'PEDOT:PSS | PCP-Na', 'AgI-QDs', 'TTPA-BDT', 'M7-Br', 'PANI-PAMPSA', 'C13-FAS | Spiro-MeOTAD', 'B1', 'LD29', 'SM09', 'ZnPc-flu-ZnPc', 'BTT(DPP)3-C8', 'KR360', 'Si-PO-2CN', 'IEICO-4F | Spiro-MeOTAD', 'SWCNTs | PMMA', 'HfO2 | PTAA', 'BzTA', 'DR3TBDTT; PDMS', 'TPA-QA-TPA', 'Cu0.33Cr0.67O2', 'CuSCN | NPB', 'H1', 'P3HT | P3HT; PMMA', 'TPAC0M', 'CZ-TA', 'V2O5 | P3CT-K', 'KR353', 'Spiro-MeOTAD | CuI', 'X61', 'CuS-np', 'Z8', 'NiO-c | CuGaO2-mp', 'C12-carbazole', 'CA-Br', 'Carbon-nt; P3HT', 'ZnChl', 'PDPP-3T', 'pp-TPE-4DPA', 'Triazine-Ph-OMeTPA', 'TIPS-pentacene', 'V1000', 'NiO-np | ME1', 'PIDT-DFBT', 'PCT', 'NiPcS4', 'SiO2', 'CTAB | Spiro-MeOTAD', 'TPA-BP-TPA', 'PPyra-TXA', 'r-GO-BH', 'Crosslinked TCTA-BVP', 'Sym-HTPcH', 'VB-DAAF', 'Spiro-MeOTAD | V2O5', 'OMeTPA-TPA', 'TPA-OMeTPA', 'PCA-1', 'OMeTPA-FA', 'POZ10', 'CuInS2-QDs', 'PAF-86', 'DMFA-FA', 'TATCz3', 'Carbon; NiS', 'BDT2FMeDPA', 'c-TCTA', 'Spiro-MeOTAD-I', 'OMETPA-DPP', 'Z1', 'TFAP', 'NiO-np | PAS', 'Ethyl acetate; I2; LiI; TBP', "N3',N3',N6',N6'-tetrakis(4-methoxyphenyl)spiro[fluorene-9,9'-xanthene]-3',6'-diamine", 'H4', 'Carbon-QDs | Spiro-MeOTAD', 'M4; PCBM-60', 'X23', 'ITIC', 'HMPDI', 'Au-np; P3HT', 'Graphene | Spiro-MeOTAD', 'TPA-BP-OXD', 'PEDOT:PSS | MoS2', 'c-OTPD', 'Porphyrin-H1', "2,2'-[(4,5-Bis(2-ethylhexyl)-dithieno[2,3-d:2',3'-d']thieno[3,2-b:4,5-b']dipyrrole-2,7-diyl)-bis(3-hexylthien-5,5'-diyl)bis(methane-1-yl-1-ylidine)]dimalononitrile", 'CuHePc', 'CBP', 'S9', 'ACR-TPA', 'PBTTTV-h', 'PDVT-10', 'SGT-422', 'ZnPc-p-ZnPc', 'CI-GO | PTAA', 'NiO-c | Cysteine', 'DMFA-TPA', 'Alkoxy-PTEG', 'TATF8HBP', 'Ph-OMeTPA', 'Y1', 'FTA1', 'VOx | Cu phtalocyanine', 'TBASBP', 'V1061', 'Spiro-029', 'Cu12Sb4S13', 'PTB-DCB21', 'n-CuBuPc', 'DAHI | Spiro-MeOTAD', 'HTM-1', 'CuAlO2; CuO', 'PEDOT:PSS | Au@poly(4-styrenesulfonate)', 'Au@CuZnSnSe-np', 'M110', 'TFDIB | Spiro-MeOTAD', 'NaYF4:Yb:Er-np | Spiro-MeOTAD', 'Bp-OMe', 'PEDOT:PSS | 5,6,11,12-Tetraphenylnaphthacene', 'BP-DC', 'CuS', 'P3', 'C8-BTBT', 'Ome-TPA-CuPc', 'NiO-c | SY3', 'asy-PBTBDT', 'HS-Ph-SCH3 | Spiro-MeOTAD', 'Poly-N-vinylcarbazole | SP-11', 'PB2T-SO', 'SFX-TPAM', 'BTT(DPP)3-EH', 'V862', 'T40P', 'Z1011', '1,3,6,8-tetrakis-(N,N-di-p-methoxyphenylamine)pyrene', 'MPA-BTI', 'DTP-C6Th', 'CS01', 'M1', 'Poly(2-ethyl-2-oxazoline); PEDOT:PSS', 'TPA4C', 'M103', 'TbT-1', 'MFGO', 'c-OTPD; TPACA', 's-PANI:PSS', 'WT3', 'A102', 'Spiro-MeOTAD | ODA-FeS2-np', 'EHCz-MeFl', 'LD22', 'ZnPc', 'BTT-4', 'M115', 'Triazine-InT', 'Carbon-nt; Graphene oxide', 'MC6Cz-9-NPC', 'XDB', 'WOx', 'YN2', 'Bifluo', 'PEDOT:PSS | TS-CuPc', 'FH-3', 'Graphene oxide | Carbon-np', 'IDT2', 'PMAA; Spiro-MeOTAD | Spiro-MeOTAD', 'X50', 'NiO-np | Choline chloride', 'DEPT-SC', 'Spiro-MeOTAD | MoO3 | CuPc', 'ZnPc(tBu)4', 'BTPA-3', 'H16', 'TTPA-DBQT', 'PEDOT:PSS | PbI2', 'NiO-np | Al2O3-mp', 'L-f', 'Me-BPZTPA', 'Oleic-acid | P3HT', 'SP-01', "2,2'-[(4,5-Bis(2-ethylhexyl)-dithieno[2,3-d:2',3'-d']thieno[3,2-b:4,5-b']dipyrrole-2,7-diyl)-bis(4,3'-dihexyl-2,2'-bithien-5,5'-diyl)bis(methane-1-yl-1-ylidine)]dimalononitrile", 'NiCo2O4', 'Py-C', 'T101', 'BEDN', 'SO7', 'NP-SC6-TiOPc', 'PTT | Spiro-MeOTAD', 'CdZnSe@ZnSe-QDs', 'Py-COF | PTAA', 'Li-TFSI; TBP', 'XSln1453', '2,8-bis-[2,2-bis(4-methoxyphenyl)ethenyl]-5,11-diethyl-5,11-dihidroindolo[3,2-b]carbazole', 'Polymer4', 'PolyTPD | PFN', 'SM13', '2,5‐bis(4,4′‐bis(methoxyphenyl)aminophen‐4′′‐yl)‐3,4‐ethylenedioxythiophene', 'Z3', '2-((2-(4-(2-ethylhexyl)-4H-dithieno[3,2-b:2′,3′-d]pyrrol-2-yl) thiazol-5-yl)methylene) malononitrile', 'H7', 'Theophylline | Spiro-MeOTAD', 'BPAPF', 'Acetonitrile; B2; LiBr', 'OMETPA-BDT', 'CF-BTz-ThR', 'SDTFCz2', 'Si-OMeTPA', 'EGO-PPV | PFN-P2', 'PANI-PAMSA', 'SP-12', 'Ethyl acetate; I2; LiI; TBP; Urea', 'TPTPA | MoO3', 'MC8-TPA', 'CZTS-np', '1,4-di(1H-imidazol-2-yl)benzene-C6', 'PbS-QDs | Spiro-MeOTAD', 'Spiro p-xylene', 'PEDOT:PSS | 4-bromobenzenediazonium tetrafluoroborate', '3,6-Cz-TPA', 'TPTPA | TPTPA; MoO3', 'CuInS2 | ZnS-QDs', 'V1050', 'tri-TPA', 'H6', 'CzP', 'CuPc', 'F23', 'CsBiBr3-QDs', 'NiO-np | Spiro-MeOTAD', 'Triazine-Flu', 'PMMA; rGO', 'TB4-ZnPc', '2,7-Bis(4,4′-dimethoxydiphenylamine)-9- (bis(methylsulfanyl)methylene)fluorene', 'YT2', 'PhNa-1T', 'Ag:CuO-nanofibers | PEDOT:PSS', 'Chl‐2', 'cyclopenta[2,1-b; 3,4-b′]dithiophene', 'COPV6', 'PTAA | TFPPy-ETTA', 'DBFMT', 'Pt-np', 'BDT0FMeDPA', 'PtMePy', 'H-Bi', '3,6-di(2H-imidazol-2-ylidene)cyclohexa 1,4-diene-C6', 'Z2', 'PDPP3T', 'NiO-c | Sn2O3-qd', 'MC8-9-NPC', 'PTAA-1F', 'HTM5', 'NiO-np | TPI-2MEO', 'Spiro-MeOTAD | CANP | Spiro-MeOTAD', 'br-4C', 'Carbozole @ S12', 'IDF-DiDPA | MoO3', 'TPE-S', 'CsPbBr3-np | Spiro-MeOTAD', 'Rubrene | PEDOT:PSS', 'HA2', 'V2Ox | PEDOT:PSS', 'TP-FTzF-TP', 'SFT-TPA', '3,6-Ben', 'NH-2,6', 'FU7', 'MoS2-QDs | Spiro-MeOTAD', 'PCDTBT', 'NiO-c | MoOx', 'Polymer2', 'NiO-c | n-Butylamine', 'MoO3 | PTAA', 'TOPO', 'HBZ-71', 'DFBT(DTS-FBTTh2)2', 'Cobalt–porphyrin', 'TPA-ANR-TPA', 'Spiro-OEtTAD', 'TTE-2', 'NiO-c | NiO-nw', 'MEH-PPV-20', 'PEH-3', 'CsSnBr3-QDs', '3,6-PCzTPA', 'NiO-c | Mercaptoethylamine chlorate', 'HPB-OMeDPA', 'PTh; Graphene', 'SCZF-5', 'Titanylphthalocyanine', 'NiMgLiO', 'BTTP', 'Spiro-TAD', '3-Butylthiophene | Spiro-MeOTAD', 'Graphene oxide; NiO-c', 'BDT-PTZ', 'PMA', 'Cu3SbS4-np', 'Ni-acetate', 'TcTa', 'Ph-TPA-2A', 'P1', 'D205 | Spiro-MeOTAD', 'PDPPT-TT', 'ATT-ODec', 'Spiro-CPDT', 'P3HT; PFN', 'CuPcNO2-OMFPh', 'BChl-1', 'Spiro-OPrTAD', 'Al2O3-c', 'Carbon', 'PDTSTTz-4', 'Spiro-MeOTAD | MWCNTs; Spiro-MeOTAD', '2,7-triphenylamine-carbazole', 'NiO-c | Ni', 'V859', 'DPBTD-B[BMPDP]2', 'CuSCN | rGO', '2,2′-[(4,5-Bis(1-octylnonyl)-dithieno[2,3-d:2′3′-d]thieno[3,2-b:4,5-b′]dipyrrole-2,7-diyl)bis(thien-5,5′-diyl)bis(methane-1-yl-1-ylidine)]dimalononitrile', 'F4-TCNQ', 'PyThTPA', 'PSS-g-PANI:PFI', 'Spiro-TBB | Spiro-TBB', 'PDMS', 'NiO-np | TPI-6MEO', 'Lignosulfonate; PEDOT:PSS; PDA', 'TAPbI3 | Spiro-MeOTAD', 'Spiro-MeOTAD | WO3', 'DPPZnP-TSEH; PCBM-60 | BCP', 'BI25', 'PANI', 'T80P', 'CDTh 1', 'Au-np; PEDOT:PSS', '4-(4-Phenyl-4-alfa-naphthylbutadienyl)-N,N-di(4-tolyl)-phenylamine', 'FBA3', 'Spiro-MeOTAD | WOx', 'LCS01', 'MeO-FDPA', 'TiO2-np | NiO-np', 'BTT-TPA', 'Cu0.67Cr0.33O2', 'P(VDF-TrFE) | Spiro-MeOTAD', 'NPB', 'TQ2', 'alkylammonium bromide | Spiro-MeOTAD', 'TPE-2,7-Carbazole W1', 'H64', 'BTTI-C6', 'Z30', 'CZTPA-2', 'PCBM-60 | bis-C60', 'TPASB', 'NiO-np | PTAA', 'KTM3', 'S197', 'Au-np; Graphene oxide', 'JY6', 'NiO-c | CuGaO2-c', 'TCPBr | Spiro-MeOTAD', 'PET-OMeDPA', 'AIGS-QDs', 'Polyrotaxane', 'PSQ2', 'KM05', 'CPE-K', 'NiO-np | ME3', 'Unknown', 'TPL', 'pTPA-DBTP', 'OAI | DM', 'NPB; PTAA', 'PEDOT:PSS | Al2O3-mp', 'PO-Spiro-OMeTAD', 'Carbon-nt | Spiro-MeOTAD', 'CON-16 | PEDOT:PSS', 'LHTM-1', 'CuGaO2', 'COPV3', 'PFO', 'CIGS', 'NiMgO-c', 'P3TAA', 'Carbon-nt', 'PffBT4T-2OD | WOx', 'C12H10B2O4 | Spiro-MeOTAD', 'NTPA', 'PBT', 'Li4Ti5O12 | Spiro-MeOTAD', '2,2′-[(4,5-Bis(1-octylnonyl)-dithieno[2,3-d:2′3′-d]thieno[3,2-b:4,5-b′]dipyrrole-2,7-diyl)bis(2,3-dihydrothieno[3,4-b][1,4]dioxin-5,5′-diyl)bis(methane-1-yl-1-ylidine)]dimalononitrile', 'CuP', 'YN3', 'ZnChl-4', 'Carbon-np; PEDOT:PSS', '2PACz', 'Spiro-MeOTAD | PbS', 'BTT-1', 'BTF4', 'PTAA; Spiro-MeOTAD', 'Y2', 'DNA', 'NiO-c | SDBS', 'PTZ2', 'NP2', 'IEICO; PBDTTT-E-T | MoO3', 'OIPC-I', '2-F-br-4C', 'T1', 'B3', 'B63', 'COPV7', 'PCDTBT1', 'PBDTT-SeDPP; PCBM-70', 'Graphene oxide', 'DMZ', 'PMMA', 'Yih-2', 'ZnNc', 'PEDOT:PSS | PFN-P1', 'TTE-1', 'PbS', 'DH-MeO-FDPA', 'TPP-SMeTAD', 'DTS', 'SGT-409', 'S,N-heteropentacene', 'Poly-N-vinylcarbazole | SP-12', 'Spiro-MeOTAD | SWCNTs', '1F-SAM | PEDOT:PSS', 'CPEPh-Na', 'KR216', 'TaTm | MoO3', 'SFXDAnCBZ', 'Carbon-nt | PMMA', 'PTAA | Spiro-MeOTAD', 'CuCrO2', 'NiO-c | N749', 'NiO-c | PhNa-1T', 'TQ1', 'PbS-QDs', 'DM', 'DIPO-Ph4', 'DTh101', 'PPyra-XA', 'IDF-TeDPA | MoO3', 'NiPc | V2O5', 'HTM1', 'NiO-c | NiO-mp', 'CuSeCN', 'PTQ10 | PTAA', 'Th101', 'PolyTPD', 'PBDTT-SeDPP', 'EDOT-MPH', '2,7-Cbz-EDOT', 'DR3TBDTT', 'V1221', 'BTT-3', 'P3HT; SWCNTs | Spiro-MeOTAD', 'Ni | NiMgO | PVP', '2F-SAM | PEDOT:PSS', 'BDT:TT', 'AQ | Spiro-MeOTAD', 'Poly(1,4-phenylenevinylene)', 'PCPDTBT', 'PEDOT:PSS | Al2O3-np', '2,7-Pyr', 'JK-216D', 'BTSe-1', 'S:DIB', 'KR321', 'Spiro-TTB', 'PEDOT:P(SS-co-TFPMA)', 'X62', '(BMPA-EDOT)3-TPA', 'TPA-BPFN-TPA', 'CoTh-TTPA', 'THY-4', 'Fu-OMeTPA', 'PEDOT:PSS-NH2-OH', 'VOx', 'TPADPP-1', 'M6', 'WO3-nw@PEDOT | PEDOT:PSS', 'Al2O3-c | PEDOT:PSS', 'HfO2 | Acetonitrile; I2; LiI; TBP', 'T60P', 'Graphene oxide | PFNBr', 'Spiro-MeOTAD | rGO', 'Al2O3-mp | MeO-DATPA', 'NiO-c | BBA', 'YT1', 'BAI | DM', '3F-SAM | PEDOT:PSS', 'P3HT | Al2O3-mp', 'SY1', 'Triazine-Th-OMeTPA', 'Co3O4', 'SGT-411', 'NiO-c | FDA', 'BDT-POZ', 'J61-ITIC', 'SWCNTs | Graphene oxide', 'Spiro-MeOTAD | MoO3', 'CuInSe2-QDss', 'P3OT', 'T(EDOT-TPA)2', 'H5', 'apv-T', 'Graphene | PEDOT:PSS', 'FB-OMeTPA', 'TT80', 'BDT-4MeOTPA', 'CGS', '2,4-spiro', 'TSHBC', 'TCP-OC8', 'YC04', 'SGT-404', 'P1Z1', 'Nafion; PEDOT:PSS', 'T5H-OMeDPA', '(n-BuO)4ZnPc', 'SBFCz2', 'Polymer1', 'M3; PCBM-60', 'CzPF', 'PEDOT:PSS | SrGO', 'n-octylammonium iodide | Spiro-mF', 'CuSCN-nw', 'Py | Spiro-MeOTAD', 'PTAA | MoS2', 'B186', 'P3HT; SWCNTs | PEDOT:PSS', 'Al2O3 | Spiro-MeOTAD', 'ZnO-nw | PEDOT:PSS', 'NiO-c | Mg(AcO)2', 'HTM', 'Au-nw | Spiro-MeOTAD', 'NiO | PS', 'NiO-c | EPA', 'MeO-TPD', 'PTB7-Th', 'CuI | PbPc', 'Cu0.2Cr0.8O2', '1‐adamantylamine | Spiro-MeOTAD', 'NiO-c | DEA', 'Imidazolium iodide | P3HT', 'Graphene; TSHBC  @ 5:1', 'TFM', 'YC01', 'PEDOT:PSS | NPB', 'BTPA-6', 'S,N-Heteroacene 2', 'Ag-np; PEDOT:PSS', 'COTT-1 | COTT-2', 'S7', 'WO3-nw', 'PdMe2Pc', 'PDCBT | WOx', 'PPDT2FBT', 'SWCNTs | Spiro-MeOTAD', 'CAS', 'Graphene; P3HT', 'Pentacene', 'Q219', 'Polythiophene', 'S,N-Heteroacene 1', 'CT3', 'MnS', 'PTAA | LiF', 'NiCoO', 'CuSCN | Spiro-MeOTAD', 'PDI', "Tetrakis(4-methoxyphenyl)spiro[cyclopenta[1,2-b:5,4-b']dipyridine-5,9'-fluorene]-2',7'-diamine", 'V1207', 'Dispiro-OMeTAD', 'Au-np | Spiro-MeOTAD', 'PEDOT', 'SnS', 'NiO-np | Choline chloride; Glycerol', 'BEDCE | Spiro-MeOTAD', 'PZn-TPA-O', 'PTAA | PFN-Br', 'PP-Spiro', 'CuO2', 'MoO3 | TaTm', 'Phenethylamine | Spiro-MeOTAD', 'CdSe-QDs | Spiro-MeOTAD', 'PEDOT:PSS | MoO3', 'p-PFP-O | PTAA', 'PBTI-C', 'PTAA; TPFB', 'F6-TCNNQ; TaTm', 'NiO-c | SY1', 'TZ2', 'mDPA-DBTP', 'Montmorillonite | Spiro-MeOTAD', 'PCA-2', 'InP-np | Spiro-MeOTAD', 'TPA', 'H2', 'IEICO | MoO3', 'CsCuBr3-QDs', 'PolyTDP', 'NiPc-Cou', 'IDT1', 'TBC-1', 'PCPDTBT | PEDOT:PSS', 'Q197', 'P3HT | PEDOT:PSS', 'F16CuPc | Spiro-MeOTAD', 'TPB-4-MOTPA', 'TATSFHBP', 'ZnPc-p-ZnPc 1', 'HL-2', 'Tetracene | Spiro-MeOTAD', 'XOP', '2,7-PCzTPA', 'SY4', 'TPDI', 'C60', 'BTTI-C12', 'Q205', 'YK1', 'PTB7:Th', 'ZnChl-1', 'NiO-c | PTAA', 'iDM1', 'THY-2', 'mp-SFX-3PA', 'CZ-STA; CZ-TA', 'AS37', 'TaTm', 'CuInS2 | Al2O3-np', 'P3HT | WOx', 'Azu-Oct', 'Imidazonium iodide | Spiro-MeOTAD', 'PEDOT; Spiro-MeOTAD', 'Al2O3-np | TPA-ZnPc', 'P3HT; SWCNTs-PhOMe', 'ADAHI', 'JW8', 'COPV5', 'NiO-c | PEAI', 'PTAA-2F', 'Cu2CoSn4-np', 'PBDT(2F)T', 'PEDOT:PSS | Black phosphorous QDs', 'PEDOT:PSS | VOx', 'BTT-2', 'Pentafluorobenzenethiol | Spiro-MeOTAD', 'TFB | Al2O3-np', 'CMO', 'NiCo2O4-np | Spiro-MeOTAD', 'TBC-2', '1,3,6-tris-(N,N-di-p-methoxyphenylamine)pyrene', 'CuSCN | Graphene', 'C12-silane-SAM | Spiro-MeOTAD', 'Theophylline | PTAA', 'ZnPy', 'MPA-BTTI', 'Z1013', 'Ni | Au', 'P8TTT', 'CuSCN', 'P3OFHT', 'NH-2,7', 'NiO-c | CuGaO2', 'NiO-c | PMMA', 'PANI:PSS', 'P3HT | MoO3', 'CuAlO2 | PEDOT:PSS', 'CuSCN | Ta:Wox-np', 'No HTM', 'TPD-4EtCz', 'L-H', 'PT-DC', 'PDQT', 'DNA-CTMA', '2EGO-PPV', 'Co0.695Cu0.305O', 'PDMS | CuSCN', 'PB2T-O', 'NiO-c', 'GO-nanoribbons', 'CMP', 'Azu-Me', 'Ag-nw; PEDOT:PSS', 'Ppy', 'YC06', 'TPD-4MeTPA', 'LGC-D013', 'NiO-np | KCl', 'M108', 'SiTP-OMeTPA', 'TBC-3', 'Cz-Pyr', 'PEDOT:PSS | PEDOT:PSS', '10-butyl-3,7-diphenylphenoxazine', 'HTM-P1', 'apv-EC', 'Grafted rGO; Polyacrylonitrile', '4C', 'CuI; CuSCN', 'P3HT; SWCNTs', 'JK-217D', 'NiO', 'ATT-OBu', 'DFH', 'NiO-c | SY2', 'HfO2 | CuI', 'DFTAB', '0F', 'TAT-t BuSty', 'NiO-c | PTZ-1', 'DOR3T-TBDT', 'SWCNTs | PEDOT:PSS', 'PABA | Spiro-MeOTAD', 'BTBDT', 'PTAA | PMMA', 'PTZ1', 'M3', 'Cu2ZnSn4-np', 'KR374', 'P4', 'SGT-421', 'Al2O3-mp | Spiro-MeOTAD', 'V841', 'CuCrO2-np', 'BTX-OMeTAD', "N1,N1',N1'',N1'''-(ethene-1,1,2,2-tetrayltetrakis(benzene-4,1-diyl))tetrakis(N1-(4-(dimethylamino)phenyl)-N4,N4-dimethylbenzene-1,4-diamine)", 'H-Ca', 'PTAA | Car-ETTA', 'TPA-BPV-TPA', 'MWCNTs; Spiro-MeOTAD', 'M107', 'PEDOT:PSS | Rubrene', 'H111', 'OTPA-ZnPc', 'PTPD | PFN', 'Azu-Bu', 'PEDOT:PSS | VB-DAAF', 'TRUX-E-T', 'DR3T', 'PEDOT:GSL', "Fused-F (Tris[[4-[3,3'-dihexylsilylene-2,2'-bithiophene]-7-[5′′-n-hexyl-(2,2′; 5′,2′′-terthiophen\ne)-5-yl]-benzo[c]-[1,2,5]thiadiazole]-2,6,10-yl]-4,4,8,8,12,12-hexamethyl-4H,8H,12\nHbenzo[1,9]quinolizino [3,4,5,6,7,-defg]acridine )", 'PVDF-HFP | Spiro-MeOTAD', 'PEAI | PTAA', 'TS-CuPc', 'CsOAc | Spiro-MeOTAD', 'Ph-TPA-8A', 'ATT-OMe', 'PEDOT:PSS | PCPDTBT', 'PFN; PTPD', 'HPDI', 'PNP-BC', 'Oleylamine | Spiro-MeOTAD', 'CuOx', 'Z26', 'TPB(2-TPTZ)', 'P3CT-CH3NH2', 'CuMe2Pc', 'G2', 'KM07', 'JW6', 'MoO3 | TPA-2,7-FLTPA-TPA', 'HS-Ph-NO2 | Spiro-MeOTAD', 'DM1P', 'N2,N2,N12,N12-Tetrakis(4-methoxyphenyl)-9-methyl-9H-naphtho[2,1-c]carbazole-2,12-diamine', 'r-GO-NH', 'Ph-inv-OMeTPA', 'KR145', 'ZnP', '3,6-triphenylamine-carbazole', 'Co-Porphyrin', 'D102', 'H-PheDOT', 'P-OR', 'Z33', 'Polypseudorotaxane', 'TDAB', 'Z29', 'TPA‐ANT‐TPA', 'SYN1', 'G1', 'HfO2 | Spiro-MeOTAD', 'V2O5 | PEDOT:PSS', 'CrO3', 'BV-FNPD', 'V1036:C4', 'Si-QDs | Spiro-MeOTAD', 'pDPP5T-2 | WOx', "(2Z,2'Z)-2,2'-(((2,4-dimethylphenyl) azanediyl) bis([1,1'-biphenyl]-4',4-diyl)) bis(3-(4-(diphenylamino) phenyl) acrylonitrile", 'EH44', 'H2Pc-1', 'DPIE', 'DAI | DM', 'AZ1', 'D103', 'N-CuMe2Pc; P3HT', 'Cu2NiSn4-np', 'TT-3,6-TPA', 'Asy-PBTBDT', 'PTAA | PPNBr', 'PTA', 'CuPrPc', 'HA1', 'TPAC2M', 'M:OO', 'Cu:Ni acetate', 'YN1', 'ACE-QA-ACE', 'Spiro-OiPrTAD', 'PDCBT | Ta-Wox', "tetra{4-[N,N-(4,4'-dimethoxydiphenylamino)]phenyl}ethene", 'Q222', 'DPP-Ome', 'P3CT-Na', 'PFN; TT', 'Spiro-MeOTAD | MoOx', 'CdSe-Qd | CsPbI3-QD | Spiro-MeOTAD', 'CoPcNO2-OPh', 'CW4', 'Selenium', '3,6 ´-BCz-OMeTAD', 'SAF‐OMe', '2TPA-2-DP', 'LiF | PEDOT:PSS', 'NiO-c | PTZ-2', 'DM1', 'DPIO', 'PST1', 'PBDTP-DTDPP', 'BTPA-4', 'CsSnI2.95F0.05', 'P3TAA-co-P3HT', 'IDTC6-TPA', 'PBDTTT-C', '2TPA-1-DP', 'NiO-c | Al2O3-mp; Au@SnO2-nw', "4,4'-(5,10,11-Trihexyl-10,11-dihydro-5H-thieno[2′,3':4,5]pyrrolo [3,2-g]thieno[3,2-b][1,2,3]triazolo[4,5-e]indole-2,8-diyl)bis(N,N-bis(4- methoxyphenyl)aniline)", 'FT55', 'BAI | Spiro-MeOTAD', 'Poly TPD-NPD', 'pentaerythritol tetrakis(3-mercaptopropionate) | Spiro-MeOTAD', 'C6Br | Spiro-MeOTAD', 'Spiro-MeOTAD | TS-CuPc', 'TT-2,5-TPA', 'DBC-OMeDPA', 'DPA-QA-DPA', 'PTB7-TH', 'Co(II)P', 'P1C1', 'MTDATA', 'CW3', 'V1225', 'FBA1', 'Spiro-MeOTAD', 'DTS(IIThThHEX)2', 'KR378', 'P3HT | WO3', 'EtheneTTPA', 'M105', 'CT4', 'VB-MeO-FDPA', 'THY-3', 'NiPc', 'MoS2 | Spiro-MeOTAD', 'pBBTa‐BDT1', 'Py-OMe', 'Cu:NiO-np', 'HTM-M1', 'CuSCN-2D', 'TT0', 'P3CT-Na | PASP', 'Spiro-MeOTAD | Cu2O', 'Graphene | AuCl3 | PEDOT:PSS', 'PTAA | CuSCN', 'rGO | PTAA', 'J2', 'DTPC8-ThDTPA', 'CF-Sp-BTh', 'TaTm | F6-TCNNQ; TaTm', 'PEDOT:PSS | Au@SiO2-nw', 'NiCo2O4-np', 'FH-0', 'FEH', 'IrTiOx-c', 'm-MTDATA', 'TPA-TPM', 'Spiro-OBuTAD', 'MoOx | Spiro-MeOTAD', 'Co(II)P; Co(III)P', 'H2Pc', 'Co(III)P', 'NiO-c | UiO-66', 'PQT-12', 'N,N-bis-[7-(4,4′-dimethoxydiphenylamine)-9- (bis(methylsulfanyl)methylene)fluoren-2-yl]-4-methoxyaniline', 'CJ-02', 'M111', 'PVK', 'C202', 'MoO3 | TPA-3,6-FLTPA-TPA', 'P(BDTT-tPPD)', 'PTB7 | WOx', 'DIB; SeS2', 'Polyacrylonitrile', 'rGO | CuSCN', 'TT1', 'PTAA | NiO-c', 'MEH; PPV', 'PTAA | CuGaO2-mp', 'SnS-np | NiO-np', 'PEDOT:PSS | PFN', 'CuPc | PTAA', 'PBTTT-14', 'V1160', 'B2', 'PTB8', 'CuI', "5,5',5''-(5,5',5''-(nitrilotris(benzene-4,1-diyl))tris(furan-5,2-diyl))tris(2-octylisoindoline-1,3-dione", '1,6-di{3-[2-(4- methylphenyl)vinyl]carbazol-9-yl}hexane', 'RCP', 'PCBM-60 | BCP', 'Azu-EH', 'CuPs-TIPS', 'InP-np', 'Hexamethyl-substituted subphthalocyanine', "Poly[4,8-bis(2-(4-(2-ethylhexyloxy)3-fluorophenyl)-5-thienyl)benzo[1,2-b:4,5-b'] dithiophenealt-1,3-bis(4-octylthien-2-yl)-5-(2-ethylhexyl)thieno[3,4-c]pyrrole-4,6-dione", 'HfO2 | Acetonitrile; I2; LiI; PMII; Propylene glycol; TBP', 'BPZTPA', 'PDO2', 'CrOx', 'Z35', 'F6-TCNNQ; TaTm | TaTm', 'ZnPor', 'TPA-NADT-TPA', 'Black phosphorous nanosheets | Spiro-MeOTAD', 'SP-02', 'PCBM-60 | Carbon', 'Spiro-N', 'PEDOT:PSS | TPD', '3-Ethylthiophene | Spiro-MeOTAD', 'Spiro-E', 'CuAlO2', 'PdMePy', 'NDT', 'HS-Ph-OCH3 | Spiro-MeOTAD', 'TPE-2,7-Carbazole W2', 'CsSnBrI2-QDs', 'PEDOT:PSS | VB-MeO-FDPA', 'TTA2', 'TPA2C', 'BDT-2D', 'Vox', 'YC-2', 'Spiro-s', 'PII2T8TSi', 'PEDOT:PSS | CuSCN', 'SrCl2 | Spiro-MeOTAD', 'V852', '2H-MoS2 | Spiro-MeOTAD', 'V866', 'ZnPc-DPP-ZnPc', 'PEA2PBI4', 'PTPAANT', 'FA-CN', 'Diazo-OMeTPA', 'EVA; SWCNTs | Spiro-MeOTAD', 'H3', 'Red Phosphorous-QDs', '3EGO-PPV', 'Pyrmidine | Spiro-MeOTAD', 'WY-2', 'NiO-c | MOF-808', 'FDT', 'POSS-NH2 | Spiro-MeOTAD', 'MEH-PPV; PFN', 'dly-1', 'Spiro-MeOTAD | VOx', 'COPV2', 'ODA-FeS2-np', 'PEDOT:PSS | Pyrene', 'F8T2e', 'P3HT; PCBM-60', 'SM', "N2',N2',N7',N7'-tetrakis(4-methoxyphenyl)spiro[fluorene-9,9'-xanthene]-2',7'-diamine", 'PPV', '1-Donecyl Mercaptan | Spiro-MeOTAD', 'X25', 'PEDOT:PSS | Ca', 'F22', 'DPPS | Spiro-MeOTAD', 'TPA-MeOPh', 'BT41', 'NiO-nanowalls | Diethanolamine', 'S101', 'P3TI', '3-Methylthiophene | Spiro-MeOTAD', 'H-Di', 'X26', 'NiO-np | Br-BPA-SAM', 'COPV1', 'MeO-BPZTPA', 'PEDOT:PSS | PTMA-BP', 'C5PcH2 | MoOx', 'BL07', 'Porphyrin', 'JW7', 'PEDOT:PSS | Na3C6H5O7', 'tetra-substituted azulene', 'X18', 'P-R', 'BDT-C1', 'Phosphor-QDs', 'PCBZANT', 'TPD-4MeOTPA', 'MoO3 | TPBi | TaTm', 'Bifluo-OMeTAD | MoO3', 'ACE‐ANT‐ACE', 'Cu2ZnSnS4', 'CIGGSe-np', 'DMF; I2; PVA; TBAI', 'PAH 1', 'NiO-c | Al2O3-mp; Au@SnO2-np', 'DORDTS–TFBT', 'PEDOT:PSS | Graphene oxide; PEG', 'PEDOT:PSS | Graphene oxide', 'TPA-TVT-TPA', 'I2-electrolyte', 'PDBD-T', 'WO3 | Spiro-MeOTAD', 'TPA-AZO', 'YT4', 'Cs-oleate | Spiro-MeOTAD', 'TPDCN', 'YD2-o-C8 | Spiro-MeOTAD', 'Porphyrin-H2', 'PEDOT:PSS | PolyTPD', 'Th-OMeTPA', 'PDCBT | Ta:WOx', 'MoO3 | PEDOT:PSS', 'PVAc', 'Ph-TPM', 'CuPc | Spiro-MeOTAD', 'CuEtPc', 'TTA1', '3,6-Pyr', 'CuGaO2-np | CuSCN', 'TPFPB | Spiro-MeOTAD', 'PhCz-4MeOTPA', 'EtheneDTPA', 'CDTh-EtHex 2', 'PZn-2FTPA', 'X22', 'NiO-c | PS', '2F', 'PS | Spiro-MeOTAD', 'C101', 'NiO-nanowalls'])))

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
200
nan |250
100 | 5 | 8
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', '7.8', 'nan | 250.0', '2.5 | 30.0', '15.0 | 10.0', '89.0', '90.0', '2.0 | 50.0', '250.0 | 70.0', '100.0 | 10.0', '40.0 | nan', '325.0', '50.0', '220.0', '50.0 | 200.0', '137.0', '180.0', '45.0', '20.0 | 40.0', 'nan | 130.0', '167.0', 'nan | 33.0', '168.0', 'nan | 160.0', '803.0', '0.0', '10.0 | 6.0 | 1.0', '259.0', '10.0 | 160.0', '300.0 | 15.0', '15.0 | 150.0', '65.0 | 1400.0', '35.6', '60.0 | 10.0', '14.0 | 3.0', '300.0 | 5.0', '25.0 | 4.0', '95.0', 'nan | 44.0', '2.4', '5.0 | 2.0', '87.0', '10.0 | 90.0', '70.0', '41.0', '127.0', '193.0', '150.0 | 40.0', '11.0', '25.0 | 260.0', '5.7', '500.0', '5.0 | nan', '2000.0 | nan', '73.0', '184.0', '4.0 | nan', '76.0', 'True', '2000.0', '1.0', '54.0', '234.0', '10.0 | 5.0', '0.7 | nan', '260.0', '175.0', '267.0', '20.5', '2.0 | 400.0', '240.0', '50.0 | 50.0', '2.5 | 20.0', '9.0 | nan', '35.0 | 8.0', '600.0 | nan', '1.5 | 180.0', '330.0', '810.0', '21.0', '80.0 | 280.0', '26.0', '101.0', '809.0', '85.0', '250.0 | 40.0', '321.0', '30.0 | 40.0', '80.0 | 120.0', 'nan | 150.0', '9.0', '12.0 | 3.0', '5.0 | 40.0', '176.0', '136.0 | 5.0', '8.0', '10.0 | 7.0', 'nan | 8.0', 'nan | 3.0', '278.0', '13.0', '56.0', 'nan | 80.0', '35.0 | 10.0', 'nan | nan | nan', '650.0', '49.4', '20.0', '136.0', '20.0 | 10.0', '295.0', '52.0', '265.0', '165.0', '70.0 | nan', '40.4', '200.0 | nan', '82.0', 'nan | 6.5', '36.0', '6.5', '239.0', '14.0', '20.0 | 2.0', '1.5 | nan', 'nan | 100.0', '250.0', '2.0 | 60.0', '21.6 | nan', '10.0 | 10.0', '65.0', '9.2 | 10.0', '16.0 | 200.0', '150.0', '42.4 | nan', '100.0 | 7.0', '7.0 | 10.0', '47.35', '108.0', '9.0 | 200.0', '14.0 | 7.0', '110.0 | 7.0', '811.0', '25.0 | 15.0', 'nan | 140.0', '7.9', '12.0 | 7.0', 'nan | 20.0', 'nan | 150.3', '33.1', '15.0 | nan', '232.0', '2.5 | 40.0', '5.0 | 20.0', '10.0 | 2.0', '1.0 | 180.0', '33.5', '244.0', '50000.0', '40.0 | 10.0', '47.0', 'nan | 7.0', '35.0', '111.0', '750.0', '57.0', '135.0', '2.0 | nan', '805.0', '1.0 | nan', '30.0 | 10.0', '258.0', '33.0', 'nan | 2.0', '51.0', '2.5', '282.0', 'uknnown', '60.0 | nan', '807.0', '2.0 | 20.0', '160.0 | nan', '183.0', '80.0 | 350.0', '35.2 | nan', '20.0 | 20.0', '49.0', '200.0 | 10.0', '23.0', '59.0', '285.0', '90.0 | 80.0', '25.0', '2.8 | nan', '7.5', '40.0 | 350.0', '80.0 | 20.0', '40.0', '98.0', '35.0 | nan', 'nan | 150.1', '16.0 | 250.0', '230.0', '75.0', '20.0 | 5.0', '10.0 | nan', '37.5', '60.0 | 5.0', '40.0 | 200.0', '28.0', '480.0', '190.0', '50.0 | nan', 'nan | 180.0', 'nan | 300.0', '3.0 | nan', '8.0 | 4.0', '0.8 | 180.0', '15000.0', '10.0 | 325.0', '380.0', '700.0', '155.0', '211.0', '14.0 | 14.0', '22.0', '10.0 | 40.0', '145.0', '131.0', '63.0', '60.0 | 3.0', '34.0', '0.8', '1500.0', '37.0', '60.0 | 7.0', '280.0', '60.0', '5.0', '125.0', 'nan | 30.0', '7.0', '804.0', '160.0 | 8.0', '400.0', '143.0', '10.2', '25000.0', 'nan | 15.0', '71.0', '115.0', '2.0', '30.0 | 14.0', '20.0 | nan', '250.0 | 50.0', '130.0 | 10.0', '315.0', '4.0', '50.0 | 150.0', '253.0', '15.0 | 40.0', '34.4', '242.0', '40.9', '352.0', 'nan | 200.0', '12.0', '600.0', '300.0 | 8.0', '100.0', '105.0', '8.0 | nan', '485.0', '120.0 | 350.0', '252.0', '48.0', '96.0', '10.0 | 2.0 | 5.0', '200.0', '70.0 | 10.0', '150.0 | nan', '113.0', '80.0 | 8.0', '24.0 | 3.0', '1.2', '350.0', '290.0', '8.0 | 130.0', '3.0', '178.0', '10.0 | 30.0', '50.0 | 100.0', '10.0 | 120.0', '200.0 | 350.0', 'nan | nan', '48.3', '0.0 | 700.0', '806.0', '340.0', '35.0 | 210.0', '94.0', '181.0', '160.0', '38.0', 'nan | 15000.0', '100.0 | 8.0', 'nan | 50.0', 'nan | 14.0', '270.0', '170.0', '200.0 | 0.0', '7.0 | 115.0', '2.5 | 10.0', '15.0 | 45.0', 'nan | 170.0', '55.0', '0.4 | 180.0', '25.71', '7.0 | 2.0 | 10.0', '6.0', '80.0 | nan', '66.52', '20.0 | 100.0', '7.0 | nan', '60.0 | 1.0', '250.0 | 60.0', 'nan | 9.0', '200.0 | 700.0', '17.0', '44.0', '5.5 | 10.0', '293.0', '6.0 | 200.0', '12.0 | 200.0', '550.0', '15.0', '25.0 | 250.0', '215.0', '300.0', 'nan | 150.2', '245.0', '10.0 | 5.0 | 5.0', '185.0', '120.0', '180.0 | 160.0', '450.0', '18.0', '130.0', '153.0', '39.0', 'nan | 350.0', '110.0', '20.0 | 15.0', '310.0', '23.8', '808.0', '11000.0', '58.0', '345.0', '5.3', '3.0 | 10.0', '31.6', '1000.0', '25.0 | nan', '27.0', '188.0', '66.0', '225.0', '261.0', '46.2', '235.0', '60000.0', 'nan | 4.0', '802.0', '1200.0', '70.0 | 20.0', '390.0', '10.0', '43.0', '90.0 | 7.0', '0.2 | 180.0', '1.8 | 180.0', '30.0 | nan', '432.0', 'nan | 11.0', '173.0', '210.0', '397.0', '10.0 | 240.0', '2.5 | nan', '800.0', 'nan | 190.0', '198.0', '80.0 | 7.0', '271.0', '32.0', '5.0 | 10.0', '25.0 | 20.0', 'nan | 295.0', '163.0', '50.2', '24.0', '5.2', '40.0 | 20.0', '72.0', 'nan | 10.0', '99.0', '20.0 | 60.0', '200.0 | 5.0', '97.0', '196.0', '30.0', 'nan | 22.0', '18.3 | 10.0', '1.6', '2.0 | 180.0', '470.0', '680.0', '333.0', '35.0 | 348.0', '174.0', '158.0', '21.5', '24.0 | 7.0', '67.5', '35.0 | 475.0', '150.0 | 9.0', '116.0', '140.0', '100.0 | nan', '80.0', '801.0', 'nan | 5.0', '46.0', '320.0', '138.0', 'nan | 400.0', '45.6', '10.0 | 5.0 | 2.0', '70.0 | 7.0'])))

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
Example
Li-TFSI; TBP
FK209; Li-TFSI; TBP
F4-TCNQ
Undoped
Cu | Ag; Cu
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', 'Li-TFSI; PEG; TBP', 'Co2f; Li-TFSI; TBP', 'FK209; Li-TFSI; Rutin-Ag-np; TBP', 'AMH', 'AgNO3', 'D102; Li-TFSI; TBP', 'Cu | Ag; Cu', '2,6-ludidine; Li-TFSI', 'Graphene Oxide', 'TBA-PF6', 'Ag-TFSI; Li-TFSI; TNP', 'Poly(ethylene glycol) tridecyl ether', 'Tb', 'Li(CF3SO2)2N; TBP', 'Co1f; Li-TFSI; TBP', 'NDP9', 'PSS-Na', 'TBP; Triphenylamine', 'B', 'Pb', 'DMPS', 'Zn(TFSI)2', 'Diethylene glycol', 'TBP | Unknown', 'rGO-PhOHex', 'EMIC', 'Unknown | T4-TCNQ', 'Carbon-nano onions', 'Pyridine', 'Y', 'Undoped | Undoped', 'Ag-TFSI; Li-TFSI; TBP', 'Unknown | FK209; Li-TFSI; TBP', 'Ni', 'Ag', 'LiN(SO2CF3)2; t-BtPy', 'Cu-2Cl; Li-TFSI; TBP', 'Mg', 'Pd-PVP', 'AgI; Li-TFSI; TBP', 'Co-TFSI; TBP', 'FK209; Li-TFSI; TBP; POM@Cu-BTC', '2-6-lutidin; Li-TFSI', 'Unknown | Zn', 'Cs', 'Silane', 'MoS2', 'Li-TFSI; TPB', 'NH3', 'CSA', 'Mo(tfd-COCF3)3', 'NiOx', 'Undoped | Li-TFSI; TBP', 'Unknown | Li-TSFI; TBP', 'Li-bis; Li-TFSI; TBP', 'TFMS | Li-TFSI; TBP', 'Urea', 'BF4; TBP; TEMPO', 'Chlorobenzol; Li-TFSI; TBP', 'EDTA', 'K102; Li-TFSI', 'PTAA', 'Ethanolamine', 'FK209; Li-TFSI; TBP; CuPc', 'PEO', 'Ti', 'Unknown | 2-Py; Li-TFSI', 'BuPyIm-TFSI', 'FK269; Li-TFSI; nan; TBP', 'Sr', 'FK211', 'TBP; Li-TFSI; Co(III) TFSI', 'KMnO4; Li-TFSI; TBP', 'f-SWCNTs', 'acetylacetone', 'PSSH', 'GeO2-np', 'Co(PyPyz)3[TFSI]3; Li-TFSI; TBP', 'JQ3; Li-TFSI; TBP', 'Li-TFSI; PMo11V; TBP', 'aYF4:Yb,Er@NaYF4; Li-TFSI; TBP', 'PVA', 'Li-TFSI; Polystyrene; TBP', 'LiN(CF3SO2)2N; TBP', 'Li@C60-TFSI; TBP', 'CuSCN', 'Li-TFSI; TBP | Undoped | Li-TFSI; TBP', 'Nd', 'NaLuF4:Yb,Er@NaLuF4; Li-TFSI; TBP', 'FK212', 'TiO2@MoO3-np', 'ethanolamine', 'LiNO3', 'FK209; FN-Br; TBP', 'WOx', 'CMP', 'F8BT', 'nan | DPITPFB', 'Co-TFSI; Li-TFSI; TBP', 'TMAH', 'PFI', 'MoO3-np', 'Graphene; Li-TFSI; TBP', 'Co-TFSI', 'acetylacetonate', 'Co-TPTB; Li-TFSI; TBP', 'FK209; Li-TFIS; TBP', 'Rb', 'TCNQ | Unknown', 'Li-TFSI; TBP; FK102(II)PF6', 'Li', 'Ag-TFSI; TBP', 'Ag; Li', 'Tetrafluoro-tetracyanoquinodimethane', 'Li-TFSI; TBP', 'PZ0.020', 'F6-TCNNQ', 'Er; Yb | Li-TFSI; TBP', 'FK102', 'FK209; H3BTC; Li-TFSI; TBP; nan', 'Eu', 'PFN-P2', 'Li-TFSI; TBP; TEMPO', 'D2; Li-TFSI; TBP', 'Graphdiyne', 'NaYF4:Yb,Er; Li-TFSI; TBP', 'CNT', 'Li-TFSI; Ni-nanobelts; TBP', 'Li-TFSI; TPBA', 'AgOTf-doped GO', 'Cu(bpcm)2; Li-TFSI; TBP', 'TPFB', 'PMPS', 'TS-CuPc', 'Cu | Unknown', 'Yb', 'Li-TFSI; TBP; FK102', 'F-graphene', 'SrCl2', 'FK209; Li-TFSI; TBP | N', 'CZTS-np', 'C3-SAM', 'D-TBP; Li-TFSI', 'WO3-np', 'Li-TFSI', 'Li-TFSI; PTAA; TBP', 'ox-Carbon-nano onions', 'Thiourea', '4-Py', 'TBFB', 'HCl', 'Li-TFSI; SpiroTFSI2; TBP', 'BCF', 'PFPPY', 'Li-bisLi-TFSI; TBP', 'Li; Co', 'FK209; 3PO4; Li-TFSI; TBP', 'NE', 'CrO3', 'D1; Li-TFSI; TBP', 'Undoped; Unknown', 'Sc3N@C80', 'DIO', 'Co(II)(dpzpyr)2; Li-TFSI; TBP', 'NaCl', 'Glycerol', 'Benzoyl peroxide', 'Glucose; Graphene oxide', 'EDA', 'PDA', 'Butylamine', 'Co(III)(pztbpy)3; Li-TFSI; TBP', 'Unknown | TPFB', 'Li-TFSI; MoS2; TBP', 'LAD', 'I2; Li-TFSI; TBP', 'H-TFSI; TBP', 'Zn(TFSI)2; TBP', 'nan | Graphene oxide', 'Ag-np', 'Cu; Li', 'Cu(Oac)2', 'F4-TCNQ | Undoped', 'Fe', 'Cu', 'Zn', 'EHCz-2EtCz-ox', 'DOPA', 'Unknown | Ta', 'GeO2', 'WOx | Unknown', 'Undoped', 'FK209; Li-TFSI; rGO; TBP', 'BMPyTFSI', 'TPACA', 'D-sorbitol', 'FK209; Li-TFS; TBP', 'Li-TFSI; TBP; V2O5', 'FK209; Li-TFSI', 'F4-TCNQ', 'LiClO4', '2-amylpyridine; Li-TFSI', 'Ca', 'Unknown | Undoped', 'Glucose', 'MoO3', 'PDMS', 'Li; Mg', 'Cu9S5-np', 'DOBD', 'Polydopamine', 'Carbon-nt-G; Li-TFSI; TBP', 'FK209; Li-TFSI; TBP | Er3+; Yb3+', 'Co-LTFSI; Li-LTFSI; TBP', 'Ce', 'Diphenyliodonium-hexafluorophosphat', 'PEG', 'Li-TFSI; Li(Gd, Y)F4-Yb; TBP', 'Li-TFSI; TBA', 'Li; Pb', 'NPB', 'Pd', 'IrCp*Cl(PyPyz)[TFSI]; Li-TFSI; TBP', 'Unknown | AgSbF6', 'F4-TCNQ | Unknown', 'Li-TFSI; TBP; FK209', 'Co3f; Li-TFSI; TBP', 'Unknown | Li', 'CuH; Li-TFSI; TBP', 'Unknown | FK269; Li-TFSI; TBP', 'Unknown', 'FK209', 'Undoped | Cu', 'ClO4-', 'FK210', 'Undoped | glacial acetic acid', 'CuI; Li-TFSI', 'EHCz-MeFl-ox', 'CI', 'FK102; Li-TFS', 'K', 'Zonyl FS-300', 'GSL', 'Cu | Cu', 'Cu-2Cl; Li-TFSI', 'FK209; LiNO3', 'Graphene', 'F2-TCNQ | Unknown', 'FK209; Li-TFSI; TBP', 'EDT', 'Co; Li-TFSI; TBP', 'Mo(tfd-CO2Me)3', 'FK209; Zn(TFSI)2; TBP', 'EHCz-3EtCz-ox', 'Li-TFSI; TBP | D-sorbitol', 'Ba', 'Carbon-nt; Li-TFSI; TBP', 'Co(III)(pztbpy)3; LiNTf2; TBP', '4-isopropyl-4′-methyldiphenyliodonium tetrakis(pentafluorophenyl)borate', 'Au-np; Li-TFSI; TBP', 'JQ1; Li-TFSI; TBP', 'La', 'In10-2,4,6; Li-TFSI; TBP', 'FK102; Li-TFSI; TBP', 'CuPc; Li-TFSI; TBP', '2-Py', 'Li-TFSI; O2; TBP', 'n-Butylamine', 'sGO', 'nan | Li-TFSI; TBP', 'CuI', 'Li-TFSI; TBP; TeCA', 'PMMA', 'P3HT | Unknown', 'Fe(ttb)(TFSI)3; Li-TFSI; TBP', 'Co-TFSI; Li-TFSI', 'N', 'Lithium acetate', 'TAPC', 'Unknown | MoO3', 'Co', 'Li-TFSI; TBP | Undoped', 'TPE-NM3; Mo(tfdCOCF3)3', 'JQ2; Li-TFSI; TBP', 'TBP', 'Unknown | TBP', 'FK102; TBP', 'Unknown | Et4N-TFSI; H-TFSI', 'D4; Li-TFSI; TBP', 'Unknown | JQ1; Li-TFSI; TBP', 'FK209; Li-TFSI; TBP | Undoped', 'CuAlO2', 'FK209; H2SO4; Li-TFSI; TBP', 'Li-TFSI; TBP | Undoped | Unknown', 'rGO', 'FK269; Li-TFSI; TBP', 'Unknown | VOx', 'HA', 'Unknown | Unknown | TBP', 'CF3PA; FK209; Li-TFSI; TBP', 'Li-TFSI; TBP | Cu2O', 'O2', 'Li-TFSI; Si NPs', 'FN-Br', 'CsI', 'TBA-BF4', 'N2', 'Ethylene glycol | Unknown', 'PolyTPD', 'Triethanolamine', 'Unknown | FK209; Li-TSFI; TBP', 'Carbon-QDs', 'Alanine', '2-Py; Li-TFSI', 'Spiro-(TFSI)2; TBP', 'AuAg-np', 'Au-np', 'Li-TFSI; TBP; acetonitrile', 'Br-BA', 'NPh2O2C2H6', 'Unknown | FK102; Li-TFSI; TBP', 'DPITPFB', 'Cu-Bix; Li-TFSI; TBP', 'Amonia | Unknown', 'SrCl2 | Undoped', 'Li-TFSI; TBP | Li-TFSI; TBP', 'VOx', 'Spiro-(TFSI)2', 'Mo(tfd-COCF3)3; TBP', 'H2O2', 'Triton-X', 'Oleylamine | Li-TFSI; TBP', 'FK209; TBP', 'Sodium Citrate', 'PS', 'CTAB', 'RbCl', '[In2(phen)3Cl6]CH3CN; Li-TFSI; TBP', 'BCF; Li-TFSI; TBP', 'Ox-SWCNTs', 'PCBTBT', 'SiO-np', 'Carbon-nt@G; Li-TFSI; TBP', 'Cu9S5@SiO2-np', 'FK209; Li-TFSI; Pb(NO3)2; TBP', 'PCDSA', 'Li-TFSI; TBP; MWCNTs', 'Graphydine-QDs; Li-TFSI; TBP; nan', 'Sb', 'FK102; Li-TFSI', 'Li-TFSI; TBP | Unknown', 'Li-TFSI; P4VP; TBP', 'Cu(TFSI)2', 'TEMPOL', 'FK209; Li-TFSI; Pb-MOFs; TBP', 'D3; Li-TFSI; TBP', 'PZ0.025', 'Li-TFSI; TBP; V2O5 | Undoped', 'Unknown | TBA', 'AcOH; FK209; Li-TFSI; TBP', 'F6-TCNNQ | Unknown', 'Cu-2Cl', 'DIO; PCDTBT', 'I2', 'DMC; F4-TCNQ', 'TPFPB', 'DPPS', 'PZ0.030', 'NaLuF4:Yb,Er; Li-TFSI; TBP', 'DMSO', 'FeCl3; Li-TFSI; TBP', 'D-TBP', 'Unknown | Cu', 'NiPcS4', 'rGO-PhBiTh', 'ETH44-ox', 'Unknown | TBP | Unknown', 'Unknown | Li-TFSI; TBP', 'GD-QDs; Li-TFSI; TBP', 'TBA-TFSI'])))

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
            component='EnumEditQuantity', props=dict(suggestions=['', '0.1 %; nan', '2 mg/ml; 520 mg/ml; 0.036 vol%', '520 mg/ml; 0.036 mL', '9 uL(520mg/mLACN); 15 uL', '6.76 mg/ml; 0.5 vol%', '1 %; nan', '1.79 vol%; 2.5 vol%', '0.90 vol%; 2.07 vol%; 3.60 vol%', '11.4 mg/ml; 36 µl/ml', '35 uL(260mg/1mLACN); 30 uL/mL', '35 uL(260mg/mLACN); 30 uL', '3 %', 'nan | 2 uL/mL', '2.85 vol%; 1.75 vol% | nan', '520 mg/ml; 2.88 vol%', '11.7 mg/ml; 36 µl/ml', '520 mg/ml; 0.0338 vol%', '0.064 M; 0.198 M', '0.6 %', '8.7 mg/ml; 8.7 mg/ml; 2.88 vol%', '0.064; 0.198 M; nan', '50 vol%', 'nan | 1 vol%', '0.29 vol%; 1.75 vol%; 2.88 vol%', '0.2', '17.5 uL(300mg/1mLACN); 28.8 uL', '3 mol%; 50 mol%; 330 mol%', '9.1 mg/ml; 30 µl/ml', '67 vol%', '30 mM; 30 mM', '0.6 vol%', '5 mg/ml; 520 mg/ml; 0.036 vol%', '8 %', '0.03 M; 0.5 M; 3.3 M', '7 %', '10 %; nan', '32 mM; 28.5 µl/ml', '33 vol%', '0.029 vol%; 28.3 mg/ml; 0.0288 vol%', '1.75 vol%; 2.85 vol%', '6.24 mg/ml; 8 µl/ml', '6 mol%', '0.6 mg/ml', '30 mM; 200 mM', '0.32 mg/ml', '10.4 mg/ml; 0.03 ml/ml', '0.1', '0.5 %; nan', 'nan; nan; 1 mol%', '520 mg/ml; 0.036 vol%', '9.1 mg/ml; 0.029 ml/ml', '9.1 mg/ml; 28.8 µl/ml', '1.7 vol%; 2.0 vol%', 'nan; nan; 2 mol%', '5.2 mg/ml; 0.02 ml/ml', '15.08 mg/ml; 9.1 mg/ml; 28.8 µl/ml', '2.88 vol%', '5 wt%; 1 wt%', '0.32 mg/ml | nan', '0.5 vol%; 6.76 mg/ml; 0.5 vol%', '1.5 %', '0.035 M; 0.231 M', 'nan; 0.8 wt%; nan', '5.3 mol%', '30 mol%; 80 mol%', '7 %; nan', '2 vol%; nan; nan', '10 mol%', '9.1 mg/ml; 0.028 ml/ml', '54 uL(10mg/mLACN); 11.2 uL', '1 mg/ml; 520 mg/ml; 0.036 vol%', '0.05 M; 0.5 M; 3.3 M', '4 wt%', '9.1 mg/ml; 0.03 ml/ml', '17.5 uL(520mg/mLACN); 28.8 uL', '17.5 uL(520mg/mLACN); 29 uL', '0.05', '0.5 mg/ml', 'nan; 0.6 wt%; nan', '45 uL(2mg/mLACN); 10.2 uL', '12 µl/ml', '2 wt%', '30 mM.200mM', '0.075', 'nan; nan; nan', '0.05 wt%', '40 uL(40mg/mLACN); 23 uL(520mg/mLACN); 40 uL', '520 mg/ml; 2.85 vol%', 'nan; 0.4 wt%; nan', '0.025', '300 mg/ml; 520 mg/ml; 0.028 vol%', '2 mM; 2.88 vol%', '0.15', '0.015', '500 mg/ml; 0.03 vol%', '1 vol%; nan; nan', '0.01 %; nan; nan', '2.45 mM; 40 mM; 270 mM', 'nan | 1.75 vol%; 2.88 vol%', '520 mg/ml; 0.0288 vol%', '40 mol%', '7.8 mol%', '6 wt%', '3.38 mg/ml; 22.5 µl/ml', '7.5 mg/ml; 7.65 mg/ml; 0.01 ml/ml', '10 mg/ml', '10 wt%', '32 mM; 195 mM', '520 mg/ml; 334 mol%', '3.0 vol%; 3.6 vol%', '1.8 mM; 30 mM; 200 mM', '2.88 vol%; 1.75 vol%', '12.3 mol%', '0.01 %; nan', '17.5 uL(520mg/mlACN); 28.8 uL', '20 mol%', '50 %; nan', '170 mg/ml; nan', '5.6 mg/ml; 30 mg/ml', '35 mM; 210 mM', '0.4 %', '4 mM; 30 mM; 200 mM | nan', '0.3 wt%', '0.007', '18 uL(1MACN); 29 uL(1MCB)', '2.2 mg/ml', '12 %', '1.44 vol%; 2.88 vol%', '0.5 mg/ml; 0.5 vol%', '8.7 mg/ml; 9.8 mg/ml; 0.029 ml/ml', '11 %', '1 %', '10 uL(300mg/mLACN); 17.5 uL(520mg/mLACN); 28.8 uL', '4 %', '1.5 mM; 14 mM; 56 mM', '4 mM; 30 mM; 200 mM', '3.0 wt%', '29 uL(300mg/mL); 18 uL(520mg/mLACN); 29 uL', '0.0018', '9 mM; 55 mM', '11.4 mg/ml; 0.036 ml/ml', 'nan | nan', '20 uL(517mg/1mLACN); 36 uL; 8 uL(375mg/mLACN)', '6 %', '5.4 mg/ml; 9.36 mg/ml; 0.028 ml/ml', '18 uL(520mg/1mLACN); 30 uL; 29 uL(300mg/MLACN)', '11.34 mg/ml; 0.0176 ml/ml', '2.0 mg/ml', '0.0056 M; 0.031 M; 0.19 M', '30 mol%', '520 mg/ml; 0.285 vol%', '20 uL(517mg/mLACN); 36 uL; 8 uL(376mg/mLACN)', 'nan; nan; 4 mol%', '0.44 M', '170 mg/ml; 0.5 vol%', '31.5 uL(300mg/mLACN); 17.5 uL(520mg/mL/ACN); 28.8 uL', '8.7 mg/m; 9.1 mg/ml; 0.029 ml/ml', '7.5 uL(170mg/mLACN); 4 uL', '8.7 mg/ml; 9.1 mg/ml; 28.8 µl/ml', '9.1 mg/ml; 28.8 µl/ml | 9.1 mg/ml; 28.8 µl/ml', '1.6 vol%; 2.1 vol%; 3.6 vol%', '0.0175 mL/mL; 0.0285 mL/mL', '10.1 mol%', '0.1 wt%', '22.5 uL; 15 uL', '0.5 vol%; nan; nan', '9 %', '0.0175 vol%; 0.0288 vol%', 'nan | 17.5 uL(520mg/mLACN); 28.8 uL', '7.65 mg/ml; 1 vol%', '1.75 vol%; 3.1 vol%', '35 uL(520mg/mLACN); 60 uL', '1.7 mg/ml; 7 µl/ml', '0.0035', '170 mg/ml; 0.004 vol%', '2 %', '1.75 vol%; 2.88 vol%', '0.82 mg/ml; 2 µl/ml', '3 %; nan', '9.1 mg/ml; 0.0288 ml/ml', '0.15 wt%', '23 uL(90.9mg/mLACN); 39 uL', 'nan; nan; 3 mol%', '2.5 %', '17.5 uL(520mg/mLACN); 28.5 uL', '18.2 mg/ml; 8 µl/ml', '1.0 wt%', 'nan; 0.2 wt%; nan', 'nan | 2 vol%', '520 mg/ml; 1.4 vol%', '5 mol%', '0.5 wt%', '0.019 M; 0.007 M; 0.2 wt% | nan', '8.8 mg/ml; 0.028 vol%; 0.035 vol%', 'nan | 20 vol%', '30.2 uL(1756mg/mLACN); 9.7 uL', '1.5 wt%', '11.44 mg/ml; 36 µl/ml', '0.5 mg/ml; 520 mg/ml; 0.036 vol%', '1 wt%', '70 uL(170mg/1mLACN); 20 uL', '5.0 mg/ml', '10 uL(520mg/mLACN); 28 uL; 35 uL(18.8mg/50mLACN)', '17.5 uL(520mg/mLACN); 28.8 uK', '1.5 mg/ml', '30 uL(270mg/mLACN); 35 uL', '3 wt%', '5 at%', '5 %', '10 uL(170mg/mLACN); 5 uL', 'nan | 5 vol%', '9.14 uL(0.25MACN); 21.02 uL(1.8MACN); 35.65 uL', '5 wt%', '8.67 mg/ml; 9.1 mg/ml; 28.8 µl/ml', '6.8 vol%; 3.4 vol%', '0.0052', '0.03; 3.3; 0.5', '12 mol%', '5 %; nan', '0.8 %', 'nan | 10 vol%', '520 mg/ml'])))

    deposition_procedure = Quantity(
        type=str,
        shape=[],
        description="""
    The deposition procedures for the HTL-stack.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate them by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- Thermal annealing is generally not considered as an individual reaction step. The philosophy behind this is that every deposition step has a thermal history, which is specified in a separate filed. In exceptional cases with thermal annealing procedures clearly disconnected from other procedures, state ‘Thermal annealing’ as a separate reaction step.
- Please read the instructions under “Perovskite. Deposition. Procedure” for descriptions and distinctions between common deposition procedures and how they should be labelled for consistency in the database.
Example
Spin-coating
Spin-coating | Spin-coating
Evaporation
Spray-pyrolys
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['Spin-coating | Spin-coating >> Spin-coating', 'CBD | Dipp-coating', 'Spin-coating >> Spin-coating', 'Roller coating', 'Spin-coating >> Unknown', 'Spray-coating | Spray-coating', 'Electropolymerisation', 'Spin-coating | Spin-coating', 'Spray-pyrolys | Screen printing', 'Slot-die coating', 'Brush painting', 'Lamination | Spin-coating | Spin-coating', 'Spin-coating | Evaporation', 'Evaporation | Spin-coating', 'Ultrasonic spray', 'Sputtering', 'Spin-coating >> MeOH wash', 'Sputtering | Unknown', 'Spin-coating | Spray-coating | Spin-coating', 'Evaporation | Co-evaporation', 'CBD | Spin-coating', 'Doctor blading | Spin-coating', 'Dropcasting | Spin-coating', 'Spin-coating | Sputtering', 'Spin-coating | Unknown', 'Electrodeposition | Spin-coating', 'Evaporation | ALD', 'Magnetron sputtering >> Gas reaction', 'SILAR', 'Inkjet printing', 'Electrospinning | Spin-coating', 'Evaporation >> Oxidation', 'RF sputtering', 'Spin-coating >> Spin-coating >> Spin-coating', 'Spin-coating | Spin-coating >> Spin-coating >> Spin-coating', 'Evaoration | Spin-coating', 'Spin-coating | Lamination', 'Pulsed laser deposition | Sputtering', 'Evaporation | Evaporation', 'Spin-coating | RF sputtering', 'Electropolymerization', 'Spin-coating | Spin-coating | Lamination', 'Air brush spray', 'Spin-coating | Spray-coating', 'Spin-coating | Doctor blading', 'Sputtering | Sputtering', 'Sprinkling', 'Spray-coating | Spin-coating', 'Spin-coating | Spin-coating >> Spin-coating >> Spin-coating >> Spin-coating', 'Spin-coating | Spin-coating >> Lamination', 'Spin-coating | Spray-pyrolys', 'Spin-coating | Dipp-coating', 'Hydrothermal | Spin-coating', 'Spin-coating >> Blowing hot air', 'Lamination | Spin-coating', 'Spin-coating | Spin-coating | Spin-coating', 'Sputtering | Sputtering | Spin-coating', 'Magnetron sputtering | Spin-coating', 'Lamination', 'Evaporation >> Gas reaction', 'E-beam evaporation | Spin-coating', 'Evaporation | Evaporation | Evaporation', 'PVD', 'Press-transfer | Spin-coating | Spin-coating', 'Dipp-coating >> Spin-drying | Spin-coating', 'Dipp-coating', 'Cryo-controlled quasi-congealing spin-coating', 'Slot-die coating | Evaporation', 'Evaporation', 'Electrospraying', 'Spray-pyrolys', 'Unknown', 'CBD', 'DC Magnetron Sputtering | Spin-coating', 'Drop-infiltration', 'ALD | Spin-coating', 'CVD', 'Screen printing', 'Slot-die coating | Spin-coating', 'Centrifuge-casting', 'Doctor blading', 'Spin-coating | E-beam evaporation', 'Magnetron sputtering', 'Substrate vibration assisted dropcasting', 'Dropcasting | Lamination', 'Sputtering | Spin-coating', 'DC Sputtering >> Oxidation', 'E-beam evaporation', 'Spin-coating | Spin-coating >> Spin-coating >> Spin-coating >> Spin-coating >> Spin-coating', 'Unknown | Spin-coating', 'Spin-coating | Dropcasting', 'Spray-pyrolys | Dipp-coating', 'Dropcasting', 'Spin-coating >> Spin-coating >> Spin-coating >> Spin-coating', 'Pulsed laser deposition', 'DC Magnetron Sputtering', 'Evaporation >> Gas-reaction', 'Blow-drying', 'Hydrothermal', 'Electrodeposition', 'E-beam evaporation | E-beam evaporation', 'Spray-pyrolys | Spin-coating', 'Dipp-coating | Spin-coating', 'Evaporation >> Polymerisation', 'RF magnetron sputtering', 'Dipp-coating | Evaporation', 'Slot-die coating | Slot-die coating', 'Anti-solvent quenching | Spin-coating', 'Gelation', 'Spin-coating', 'Spin-coating | ALD', 'Doctor blading | Doctor blading', 'Spray-coating', 'Spin-coating | Evaporation | Evaporation', 'ALD', 'Co-evaporation | Evaporation', 'Spin-coating | Drop-infiltration', 'Reactive magnetron sputtering', 'Electrospraying | Spin-coating', 'Hydrolys | Drop-infiltration'])))

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
            component='EnumEditQuantity', props=dict(suggestions=['Solid', 'Liquid', 'Liquid | Liquid', 'Unknown', 'Liquid | Liquid | Liquid', 'Liquid | Liquid >> Liquid >> Liquid >> Liquid >> Liquid', 'Liquid >> Liquid', 'Gas', 'Gas >> Gas', 'Liquid | Liquid >> Liquid >> Liquid >> Liquid', 'Liquid | Liquid >> Liquid >> Liquid', 'Gas | Liquid', 'Gas | Gas', 'Liquid | Gas'])))

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
N2
Vacuum | N2
Air | Ar; H2O >> Ar
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['N2 | Vacuum', 'Vacuum >> Air', 'N2', 'Vacuum | Ar', 'Unknown', 'Air | N2', 'N2 >> methanol', 'N2 >> N2', 'N2 | N2', 'Ar | Ar', 'Air | Vacuum', 'Ambient', 'Air | Air', 'Dry air', 'Vacuum | Vacuum', 'Air', 'Vacuum', 'Ar; O2', 'Ar'])))

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
            component='EnumEditQuantity', props=dict(suggestions=['', '0.006 Torr', '0.002 Pa', '0.0001 Pa | nan', '1 atm | 0.00004 Torr', '0.000001 mbar | 0.000001 mbar', '1 atm | 0.00003 mbar', '1 atm | 1 atm', '6 Pa', '1 atm | 0.0001 Pa', '1 atm | 0.000001 atm', '1 atm | 0.000002 Torr', '0.0001 Pa', '1 atm', '4 Pa', '1 atm | 0.000001 Torr', ' N2', '2 Pa'])))

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
            component='EnumEditQuantity', props=dict(suggestions=['', '1 atm | 0.00004 Torr', '0.000001 mbar | 0.000001 mbar', '1 atm | 0.00003 mbar', '0.003 Torr; 0.003 Torr', '1 atm | 1 atm', '1 atm | 0.000001 atm', '1 atm | 0.000002 Torr', '1 atm', '1 atn', '1 atm | 0.000001 Torr', '1 atm | 0.0001 Pa'])))

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
            component='EnumEditQuantity', props=dict(suggestions=['', '30 | 30', '0.9', '25', '15', '30.0', '90.0', '20.0', '30', '0.35', '30 | 0', '50.0', '65.0', '10.0', '80.0', '0 | 0'])))

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
Chlorobenzene
Acetonitile; Ethanol | Chlorobenzene
none >> Ethanol; Methanol; H2O | DMF; DMSO
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['Ethanol; Water', 'Chloroform', 'Ethylene glycol', '2-methoxyethanol', 'Etyl cellulose; Terpineol', 'Diethyl sulfide', 'Dichlorobenzene', 'Unknown | Chlorobenzene', 'acetonitrile; Chlorobenzene', '2-methoxyethanol; monoethanolamine', 'IPA | Chlorobenzene', 'Unknown', 'Chlorobenzene | none', 'Ethanol | TMAOH solution', 'Chlorobenzene | Unknown', 'Toluene | Methanol', 'none', '2-methoxyethanol; ethanolamine | none', 'acetonitrile', 'Methanol', 'IPA; Water', 'Water | Chlorobenzene', 'Water; Methanol', 'IPA | Diethyl sulfide', 'Toluene | DMF', 'DMF', 'Water | 2-metoxyethanol', '1,2-dichlorobenzene', 'Chlorobenzene >> 2-Butanol', 'IPA | IPA', 'IPA | Unknown', 'Chlorobenzene', 'Chlorobenzene; acetonitrile', 'Hexanethiol', 'Ethyl acetate', '2-methoxyethanol; ethanolamine', 'Water; IPA', 'DMF | Chlorobenzene', 'Toluene', 'Water', 'Chlorobenzene | Chlorobenzene', 'Ethanol', 'none | 2-metoxyethanol', 'Ethylene glycol | Methanol', 'Water | IPA', 'none | Chlorobenzene', 'Water | Water', 'IPA', 'none | none', 'Hexane | Unknown', 'Chlorobenzene | IPA'])))

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
            component='EnumEditQuantity', props=dict(suggestions=['', '1; 8', '0.1; 51', '1 >> 1', '1; 0.006 | nan', '1 | nan', 'nan | 1', '1', '1; 0.006', '5; 1', '1 | 1', '1; 0.012', '1; 1', '1; 0.1', '1; 3'])))

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
            component='EnumEditQuantity', props=dict(suggestions=['Unknown | Sigma Aldrich', 'Fisher Chemical | ACROS Organic', 'Unknown', 'Fisher Scientific', 'Heraeus', 'Guangzhou Seaside Technology', 'Nacalai Tesque; Wako Pure Chemical', 'Aladdin', 'Unknown; Sigma Aldrich', 'J&K', 'Sigma Aldrich; Sigma Aldrich', 'Sigma Aldrich', "Xi'an Polymer Light Technology; Xi'an Polymer Light Technology"])))

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
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['anhydrous; 99%', 'Pro analysis', 'Unknown', 'Puris; Puris', '0.998', '99.8%; 99.8%', 'Puris'])))

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
FK209; Li-TFSI; Spiro-MeOTAD; TBP
NiO-np
PTAA | CuSCN
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', 'NiPc | Vanadium(V)\noxytriisopropoxide; IPA', 'FK209; Li-TFSI; CS03; TBP', 'Spiro-oF; Li-TFSI; Co-TFSI; TBP', 'FK209; Li-TFSI; CS01; TBP', '(NiAc)4H2O', 'Spiro-MeOTAD; nan', 'Ni(Ac)2·4H2O; SrCl2', 'P3CT-Na', 'Spiro-MeOTAD | MoOx', 'Clevios PVP Al 4083; Black phosphorous QDs', 'Li-TFSI; Spiro-MeOTAD', 'Ni; O2', 'NiO-np', 'Spiro-MeOTAD; Co(III)(pztbpy)3; Li-TFSI; TBP', 'P3HT; rGO-PhBiTh', 'NiO-np | PAS', 'FK209; Li-TFSI; LCS01; TBP', 'NaYF4:Yb,Er; Li-TFSI; TBP; PTAA', 'CuPc | PEI', 'Li-TFSI; H-Z3; TBP', 'FK209; Li-TFSI; H-Lin; TBP', 'Oleylamine | Li-TFSI; Spiro-MeOTAD; TBP', 'TRUX-E-T; Li-TFSI; TBP', 'PEDOT:PSS | TPA-NPA-TPA', 'P3HT; rGO-PhOHex', 'PTAA; Li-TFSI; TBP', 'aYF4:Yb,Er@NaYF4; Li-TFSI; TBP; PTAA', 'PTB7-Th | MoOx', 'PEDOT:PSS | MoO3', 'DIPO-Ph4', 'Nickel acetate tetrahydrate; ethanolamine', 'Spiro-MeOTAD; Li; Co', 'NiO Target', 'P3CT', 'Li-TFSI; NiPc; TBP', 'S; Oleylamine; 1-octadecane; diphenylphosphine; Indium acetate; CuI', 'Spiro-MeOTAD; Li-TFSI; TBP | MoO3', 'IEICO | MoO3', 'MoO3', 'FK209; Li-TFSI; B186; TBP', 'P3HT', 'H-Lin', 'PBTTTV-h', 'CuSO4; Lactic Acid; NaOH', 'Clevios PVP Al 4083', 'rGO-4FPH | Spiro-MeOTAD; Li-TFSI; TBP', 'Rubrene', 'M2; Li-TFSI; TBP', 'CF-BTz-ThR', 'Al(C2H5)3 | nan', 'MEH-PPV', 'Graphene oxide | Carbon dots', 'NiOx-np solution', 'Li-TFSI; H-Z2; TBP', 'Li-TFSI; Spiro-MeOTAD; TBP; Co-TFSI', 'Nickel acetate hexahydrate; ethanolamine | ethylphosphonic acid', 'NaLuF4:Yb,Er@NaLuF4; Li-TFSI; TBP; PTAA', 'Clevios PVP Al 4083 | PEI', 'Spiro-MeOTAD', 'Nickel Nitrate hexahydrate', 'CZ-TA; Li-TFSI; TBP', 'FK102; Li-TFSI; Spiro-MeOTAD; TBP', 'M1; Li-TFSI; TBP', 'Spiro-MeOTAD; Li-TFSI; TBP', 'Copper thiocyanate', 'Graphene oxide | PFNBr', 'Graphene oxide | PTAA', 'NiO-np | PTAA', 'CZTS-np', 'Li-TFSI; H-Z1; TBP', 'Spiro-MeOTAD; Li-TFSI; TBP | MoOx', 'Co(PyPz)3(TFSI)3; Li-TFSI; Spiro-MeOTAD; TBP', 'Li-TFSI; MWCNTs; Spiro-MeOTAD; TBP', 'PTAA | PFN', 'Nickel Chloride hexahydrate; HNO3', 'C102; FK209; Li-TFSI; TBP', 'Nickel acetate hexahydrate; ethanolamine', 'InP-np | Li-TFSI; Spiro-MeOTAD; TBP', 'C13-FAS | Spiro-MeOTAD', 'Li-TFSI; PTAA; TBP', 'TaTm | F6-TCNNQ; TaTm', 'FK209; iDM1; Li-TFSI; TBP', 'P3HT; Li-TFSI; TBP', 'H-Star', 'polyacrylonitrile; rGO', 'Ni(CH3COO)2·4H2O', 'Vanadium(V)\noxytriisopropoxide; IPA', 'PTAA', 'PBDT(T)(2F)T', 'CZTS-np; hexanethiol', 'FK209; Li-TFSI; Spiro-MeOTAD; TBP', 'PBDT(2F)T', 'PEDOT:PSS; PEG', 'Li-TFSI; Spiro-MeOTAD; TBP', 'Spiro-MeOTAD; Li-TFSI; Co-TFSI; TBP', 'FK209; Li-TFSI; H-Star; TBP', 'FK209; Li-TFSI; Spiro-MeOTAD; TBP | Vanadium(V)\noxytriisopropoxide; IPA', 'PBDT(2H)T', 'Ni(Ac)2·4H2O; SrCl2 | nan', '2PACz', 'B186', 'Li-TFSI; Spiro-MeOTAD; TBP; V2O3 | Clevios PVP Al 4083', 'Li-TFSI; P3HT; TBP', 'Carbon Paste', 'DTP-C6Th', 'Graphene oxide | PTFTS', 'Spiro-MeOTAD; TBP', 'IEICO; PBDTTT-E-T | MoO3', 'MeO-2PACz', 'nickel acetate tetrahydrate', 'PTAA >> Sb 2D-nanosheets', 'TPE-S', 'Rubrene | PEDOT:PSS', 'nickel acetylacetonate', 'HA2', 'Cu >> iodine', 'Nickel acetate tetrahydrate', 'Spiro-MeOTAD; Co(III)(pztbpy)3; LiNTf2; TBP', 'PEDOT:PSS', 'Graphene oxide', 'Li-TFSI; BTPA-3; TBP', 'HA1', 'Nickel acetate hexahydrate; ethanolamine | 4-Bromobenzoic acid', 'Li-TFSI; TBP; Spiro-MeOTAD; acetonitrile', 'Li-TFSI; Spiro-MeOTAD; TBP | Li-TFSI; MWCNTs; Spiro-MeOTAD; TBP', 'Cu-np; NiOx-np', 'C101; FK209; Li-TFSI; TBP', 'InP-np', 'Oleylamine', 'FK209; Li-TFSI; EP02; TBP', 'PBDTTT-E-T | MoO3', 'nickel (II) acetate tetrahydrate', 'ethanolamine; nickel acetate tetrahydrate', 'Nickel acetate; ethylene glycol; ethylenediamine', 'pentaerythritol tetrakis(3-mercaptopropionate) | Spiro-MeOTAD; Li-TFSI; TBP', 'PTAA | PFN-P2'])))

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
            component='EnumEditQuantity', props=dict(suggestions=['Heraeus | synthesized', 'Energy Chemical; Sigma Aldrich; Sigma Aldrich; Sigma Aldrich', 'Xi’an p-OLED; Sigma Adrich; Xi’an p-OLED; Sigma Adrich', 'Sigma Aldrich', 'Sigma Aldrich; Lumtec; Sigma Aldrich', 'Xi’an p-OLED', 'Unknown', 'Lumtec, Sigma Aldrich, Lumtec, Sigma Aldrich', 'Reike Metals', 'Unknown >> 0.1 mg/ml', 'Clevios PVP', "Xi'an Polymer Light Technology; Xi'an Polymer Light Technology; Xi'an Polymer Light Technology", 'Sigma Adrich; Shenzhen Feiming Science and Technology; Sigma Adrich; Dyesol', 'Dysole; Sigma Aldrich; Dyenamo; Sigma Aldrich', 'Unknown; Borun Chemical; Unknown', 'Clevious', 'Dyesol; Sigma Aldrich; Shenzen Feiminf Science and Technology; Sigma Aldrich', 'Sigma Aldrich; Merck; Sigma Aldrich', 'Sigma Aldrich; Sigma Aldrich; Dalian HeptaChroma SolarTech Co. Ltd.; Sigma Aldrich', 'Advanced Election Technology Co., Ltd; Unknown', 'Tokyo Chemical Industry; Wako Pure Chemical; Wako Pure Chemical', 'Sigma Adrich; Sigma Adrich; Sigma Adrich; Acros Organics', 'Aladdin; Aladdin; Aladdin', 'Alfa-Aesar', 'Unknown | Sigma Aldrich; Sigma Aldrich; Sigma Aldrich', 'Heraeus', '1-Material', 'Kojundo Chemical Lab. Co.', '1-Material, NICT-7', 'Sigma Adrich; Merck; Sigma Adrich', 'Showa Chemical | ACROS Organic', 'Dyesol; Sigma Aldrich; Shenzhen Feiming Science and Technology; Sigma Aldrich', 'Synthesized', 'Guangzhou Seaside Technology', 'Sigma Adrich; Sigma Adrich; Sigma Adrich', 'Dyesol; Aladdin; Merck; Aladdin', 'Tokyo Chemical Industry', 'Aladdin | Aladdin', 'Sigma Aldrich; Sigma Aldrich; Sigma Aldrich', 'Borun Chemicals; Sigma Aldrich; Unknown', 'Baytron', 'Clevios Heraeus', 'Ossila', 'Xi’an p-OLED | Aladdin', '1-Material >> synthesized', 'Synthesized; Synthesized', 'Shanghai Aladdin Bio-Chem. Technology; Shanghai Aladdin Bio-Chem. Technology; Shanghai Aladdin Bio-Chem. Technology; Sigma Aldrich; Sigma Aldrich', 'Sinopharm Chemical Reagent Co. Ltd.,', 'J&K Scientific; Merck; Sigma Aldrich', 'Derthon; Sigma Aldrich; Sigma Aldrich', 'Novaled GmbH | Novaled GmbH', '1-Material; Unknown; Nichem Chemicals; 1-Material'])))

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
            component='EnumEditQuantity', props=dict(suggestions=['Puris; Puris; Puris; Pro analysis', 'Unknown', 'Unknown; puris; puris', '99%; 99%', 'Unknown; 96%; Unknown; 99%', 'Puris; Puris; Technical', '99.5; 99.8; Unknown', '99.95%; Unknown; 96%', '0.98', 'Puris; Puris; Puris', '99.9; Pro analysis; Tecnical; Puris', 'Unknown; Pro analysis; Puris; Puris', '0.999'])))

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
            component='EnumEditQuantity', props=dict(suggestions=['', '35 mg/ml', '1.75 vol%; 80 mg/ml; 2.85 vol%', '1.55 wt%', '0.15 M; 1 M', '72 mg/ml; 1.7 vol%; 2.0 vol%', '30 mM; 50 mg/ml; 200 mM', '72.3 mg/ml; 2.85 vol%; 1.75 vol% | nan', '20 mg/ml | 1 mg/ml', '4 mM; 30 mM; 80 mg/ml; 200 mM', '5.4 mg/ml; 9.36 mg/ml; 72.3 mg/ml; 0.028 ml/ml', '30 mol%; 8 wt%; 80 mol%', '0.14 wt%; 2.24 wt%', '51.43 mg/ml; 1.79 vol%; 2.5 vol%', '1 M; 6 mL; 6 mL; 6 mL; 1 mL; 0.3 mmol; 0.3 mmol', '72.3 mg/ml; 6.76 mg/ml; 0.5 vol%', '9.1 mg/ml; 90 mg/ml; 0.029 ml/ml', '0.2 M', '72 mg/ml; 91 mg/ml; 2.85 vol% | nan', '1 mg/ml', '0.82 mg/ml; 10 mg/ml; 2 µl/ml', '15 mg/ml; 1.5 mg/ml', '9.1 mg/ml; 80 mg/ml; 0.0288 ml/ml', '18.2 mg/ml; 72.3 mg/ml; 8 µl/ml', '5 mg/ml', '25 mg/ml; 0.32 mg/ml | 2 mg/ml', '9.1 mg/ml; 72.3 mg/ml; 0.029 ml/ml', '1 mg/ml; 520 mg/ml; 0.036 vol%; 36 mg/ml', '0.15 M; nan', '9.1 mg/ml; 1 wt%; 72.3 mg/ml; 28.8 µl/ml', '90 mg/ml', '5.6 mg/ml; 56 mg/ml; 30 mg/ml', '90 mg/ml; 7.65 mg/ml; 1 vol%', '90 mg/ml; 0.0225 mL; 0.036 mL | nan', 'nan | 72.3 mg/ml; 1.75 vol%; 2.88 vol%', '2 wt% | nan', '70 mg/ml', '72.3 mg/ml; 2.88 vol%; 1.75 vol%', '520 mg/ml; 72.3 mg/ml; 0.0288 vol%', '9.1 mg/ml; 70 mg/ml; 28.8 µl/ml', '72.3 mg/ml; 520 mg/ml; 1', '182 mg/ml; 6 vol%', '11.44 mg/ml; 90 mg/ml; 36 µl/ml', '2 mg/ml | nan', '1.3 mg/ml', '1 mg/ml | 0.05 mg/ml', '17.5 mM', '4 mg/ml', '30 mg/ml; nan', '40 mg/ml; 10 mg/ml', '8.7 mg/ml; 9.1 mg/ml; 72.3 mg/ml; 0.029 ml/ml', '1.5 wt% | 2 mg/ml >> 2 mg/ml >> 2 mg/ml >> 2 mg/ml', '25 mg/ml; 0.32 mg/ml', '11.4 mg/ml; 90 mg/ml; 36 µl/ml', '520 mg/ml; 72.3 mg/ml; 2.88 vol%', '20 mg/ml', '5.2 mg/ml; 52.8 mg/ml; 0.02 ml/ml', '70 mM', '3.83 mg/ml; 50 mg/ml; 22.5 µl/ml', '0.5 vol%; 6.76 mg/ml; 30 mg/ml; 0.5 vol%', '12 µl/ml; 0.2 M', '73 mg/ml', '500 mg/ml; 80 mg/ml; 0.03 vol%', '60 mg/ml', '9.1 mg/ml; 72.3 mg/ml; 28.8 µl/ml | 9.1 mg/ml; 0.5 wt%; 72.3 mg/ml; 28.8 µl/ml', '32 mM; 75 mg/ml; 28.5 µl/ml', '8 mg/ml', '9.1 mg/ml; 72.3 mg/ml; 0.0288 ml/ml', '8.7 mg/ml; 9.8 mg/ml; 72.3 mg/ml; 0.029 ml/ml', '30 mg/ml | 0.005 vol%; 0.995 vol%', '0.5 vol%; 6.76 mg/ml; 10 mg/ml; 0.5 vol%', '12.5 mg/ml | nan', '73.2 mg/ml | 5 mg/ml', '9.1 mg/ml; 2 wt%; 72.3 mg/ml; 28.8 µl/ml', '1 mg/ml | 0.1 mg/ml', '5 mg/ml >> nan', '11.34 mg/ml; 72.3 mg/ml; 0.0176 ml/ml', '1.5 wt% | 2 mg/ml >> 2 mg/ml >> 2 mg/ml', '2.5 wt%', '1.2 mg/ml', 'nan; nan; 70 mg/ml; nan', '63 mg/ml; 170 mg/ml; 2 vol%', '80 mg/ml; 1.45 mg/ml; 2.85 mg/ml', '15 mg/ml; 0.75 vol%; 0.75 vol%', '72 mg/ml; 1.44 vol%; 2.88 vol%', '9.1 mg/ml; 80 mg/ml; 0.03 ml/ml', '1.7 mg/ml; 10 mg/ml; 7 µl/ml', '63 mg/ml', '0.035 M; 0.07 M; 0.231 M', '10 mg/ml', '2 mg/ml; 520 mg/ml; 0.036 vol%; 36 mg/ml', '0.3 M; 2 M; nan', '12.5 mg/ml; 10 mg/ml | nan', '0.2 M | 0.03 M', '30 mM; 85 mg/ml; 30 mM', '182 mg/ml; 6 vol% | 0.5 mg/ml', '9.1 mg/ml; 80 mg/ml; 0.028 ml/ml', '78 mM', '8.8 mg/ml; 0.028 vol%; 70 mg/ml; 0.035 vol%', '0.058 M; 0.0056 M; 0.031 M; 0.19 M', 'nan; 90 mg/ml; nan', '9.1 mg/ml; 60 mM; 0.029 ml/ml', '9.1 mg/ml; 72.3 mg/ml; 28.8 µl/ml', '520 mg/ml; 82 mg/ml; 1.4 vol%', '15 mg/ml; 0.5 mg/ml; 0.5 vol%', '80 mg/ml; 5 mg/ml', '25 mg/ml', '0.2 M | 0.01 M', '3 mol%; 50 mol%; 70 mM; 330 mol%', '0.2 M | 0.05 M', '10 mg/ml; 170 mg/ml; 0.004 vol%', '35 mM', '8.75 mM', '200 mg/ml', '72.3 mg/ml; 2.88 vol%', '1.8 mM; 30 mM; 60 mM; 200 mM', '72.5 mg/ml', '1.5 mg/ml | 0.5 mg/ml', '6.43 mg/ml', '80 mg/ml', '7.5 mg/ml; 7.65 mg/ml; 90 mg/ml; 0.01 ml/ml', '0.064 M; 0.17 M; 0.198 M', '8.7 mg/ml; 9.1 mg/ml; 72 mg/ml; 28.8 µl/ml', '0.1 M', '0.0175 vol%; 72.3 mg/ml; 0.0288 vol%', '2 mg/ml', '8.7 mg/ml; 8.7 mg/ml; 72.3 mg/ml; 2.88 vol%', '9.1 mg/ml; 72.3 mg/ml; 30 µl/ml', '0.3 mg/ml', '1.5 wt% | 2 mg/ml >> 2 mg/ml >> 2 mg/ml >> 2 mg/ml >> 2 mg/ml', '15 mM', '10.4 mg/ml; 60 mg/ml; 0.03 mg/ml', '102 mg/ml', '2.5 mg/ml', '10 mg/ml | nan', '30 mg/ml', '1 mg/ml | 0.025 mg/ml', '72.3 mg/ml; 520 mg/ml; 0.3 vol%', '0.44 M', '11.4 mg/ml; 90 mg/ml; 0.036 mg/ml', '0.90 vol%; 2.07 vol%; 0.091 mg/ml; 3.60 vol%', '72.3 mg/ml; 1.75 vol%; 2.88 vol%', '9.1 mg/ml; 72.3 mg/ml; 28.8 µl/ml | 9.1 mg/ml; 1 wt%; 72.3 mg/ml; 28.8 µl/ml', '10.4 mg/ml; 80 mg/ml; 0.03 ml/ml', '4 mM; 30 mM; 80 mg/ml; 200 mM | 0.005 vol%; 0.995 vol%', '35 mM; 35 mM; 210 mM', '72.3 mg/ml; 2 mM; 2.88 vol%', '80 mg/ml; 10 mg/ml', '68 mM; 9 mM; 55 mM', '1.6 vol%mM; 2.1 vol%; 91 mg/ml; 3.6 vol%', '2 mg/ml | 0.5 mg/ml', '0.2 M | 0.02 M', '0.2 M | 0.04 M', '100 mg/ml', '72.3 mg/ml; 0.029 vol%; 28.3 mg/ml; 0.0288 vol%', '2.45 mM; 40 mM; 81.6 mM; 270 mM', '72.3 mg/ml', '60 mM; 32 mM; 195 mM', '0.5 mg/ml; 520 mg/ml; 0.036 vol%; 36 mg/ml', '9.1 mg/ml; 72 mg/ml; 0.028 mg/ml', '0.170 M; 0.064 M; 0.198 M', '9.1 mg/ml; 0.5 wt%; 72.3 mg/ml; 28.8 µl/ml', '1.5 wt% | 2 mg/ml', '2.38 wt%', '300 mg/ml; 520 mg/ml; 72.3 mg/ml; 0.028 vol%', '0.5 wt%', '73.2 mg/ml', '1.5 wt%', '54 mol%; 30 mg/ml; 334 mol%', '72.3 mg/ml; 1.7 vol%; 2.8 vol%', '2.8 vol%mM; 1.85 vol%; 72.3 mg/ml; 2.9 vol%', '8.67 mg/ml; 9.1 mg/ml; 72.3 mg/ml; 28.8 µl/ml', '520 mg/ml; 83.2 mg/ml; 0.0338 vol%', '0.175 vol%; 80 mg/ml; 0.285 vol%', '1.5 wt% | 2 mg/ml >> 2 mg/ml', '9.1 mg/ml; 72.5 mg/ml; 0.028 mg/ml', '6 mg/ml', '15 mg/ml', '520 mg/ml; 36 mg/ml; 0.036 vol%', '1 mg/ml; 1 mg/ml', '9 mM; 68 mM; 55 mM', '1.5 mg/ml', '20 mg/ml; 170 mg/ml; 34.78 vol%', '50 mg/ml', '32 mM; 15 mg/ml; 28.5 µl/ml', '72.3 mg/ml; 1.75 vol%; 3.1 vol%', '72 mg/ml', '97 mg/ml', '30 mM; 72.3 mg/ml; 200 mM', '15.08 mg/ml; 9.1 mg/ml; 72.3 mg/ml; 28.8 µl/ml', '1 mM', '6.24 mg/ml; 72 mg/ml; 8 µl/ml', '0.005 vol%; 0.995 vol%', '5 mg/ml; 520 mg/ml; 0.036 vol%; 36 mg/ml', '9.1 mg/ml; 72.3 mg/ml; 28.8 µl/ml | 9.1 mg/ml; 2 wt%; 72.3 mg/ml; 28.8 µl/ml', '20 mg/ml; 6.8 vol%; 3.4 vol%'])))

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
            component='EnumEditQuantity', props=dict(suggestions=['0.02', '0.045', '33.0', '0.0175; 0.9537; 0.0288', '0.029; 0.0175; Unknown; 0.288', '0.03; 0.94; 0.03', '1.0; 0.015; 0.008', '0.0088; 0.0144', '0.05', 'Unknown', '0.065', '0.95; 0.0075; 0.004', '0.035', '0.018; 0.018; 0.936; 0.028', '1.3', '1.5', '0.006; 0.0175; 0.9485; 0.028', '1.7', '0.06', '19.0; 7.0; 8.0; 0.2 | 33.33', '0.0175; Unknown; 0.0285', '1.0', '0.0075; 0.47; 0.0169', '0.0175; 0.95; 0.0288', '0.018; 0.94; 0.028; 0.018', '0.018; Unknown; 0.028', '0.0175; 0.028', '0.92; 0.029; 0.0175; 0.0288'])))

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
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['48.0', 'Unknown', '0.33', '10.0', '0.0167', '4.0', '2.0', '4.0 | 0.0', '24.0', '3.0', '0.5'])))

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
            component='EnumEditQuantity', props=dict(suggestions=['70; 25', '25', 'Unknown', '70 | 25', '90', '60; 25', '50', '25 | Unknown', '70 | Unknown', '70', '60', '24', '25 | 25'])))

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
            component='EnumEditQuantity', props=dict(suggestions=['', '25', 'Unknown', '25 | 15', '120 | 25', '25 | 25 >> 25', '120', '25 >> 100', '25 | 25 >> 25 >> 25', '25 | 25 >> 25 >> 25 >> 25 >> 25', '25 | 25 >> 25 >> 25 >> 25', '25 | 25', '21'])))

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
            component='EnumEditQuantity', props=dict(suggestions=['25', '550', '25 >> 80', '300', '475', '13 | Unknown', '18 | Unknown', '160', '25 >> 550', '140 | 100', '5', '600', '140 | 100 >> 100 >> 100 >> 100', '650', '5 | 0', '25 >> 250', '70', '325', '75; 120; 300', '25 | 25', '400', '80', '200', '140 | 100 >> 100 >> 100 >> 100 >> 100', 'Unknown', '130 | 60', '100', '130', '120', '500', '150', '235 | 15', '165', '100 | 100', '110.0', '60', '25 | 55', '25 >> 650', '120 | 150', '150 | Unknown', '30 | Unknown', '90', '100 >> 100', '100 | 25', '25 >> 450', '12 | Unknown', '95', '235', '145', '450', '7 | Unknown', '125', '135', '140 | 100 >> 100', '235 | 25', '300 | 120', '140', '25; 100', '350', '140 | 100 >> 100 >> 100', '25 >> 100', '11 | Unknown', '50', '120 | 60', '9 | Unknown', '15 | Unknown', '130 | 25', '200.0'])))

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
            component='EnumEditQuantity', props=dict(suggestions=['40.0', '10.0 | 5.0 >> 5.0 >> 5.0', '10.0 | 5.0 >> 5.0 >> 5.0 >> 5.0 >> 5.0', '10.0', '5.0', '60.0', '45.0 | 0.0', '12.0', 'Unknown', '5.0 >> 2.0', '120.0', '45.0', '10.0 | 0.0', '15.0 | 25.0', '10.0 | 5.0', '30.0', '10.0 | 10.0', '0.0 >> 30.0', 'Unknown | 25.0', '30.0; 30.0', '10.0; 15.0; 60.0', '10.0 | Unknown', '60.0 | 15.0', '10.0 | 5.0 >> 5.0 >> 5.0 >> 5.0', '15.0 | 5.0', '1.0', '25.0', '20.0', '20.0 | 10.0', '10.0 | 5.0 >> 5.0', '2.0 | 2.0', '15.0'])))

    deposition_thermal_annealing_atmosphere = Quantity(
        type=str,
        shape=[],
        description="""
    The atmosphere during thermal annealing
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the atmospheres associated to each annealing step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
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
            component='EnumEditQuantity', props=dict(suggestions=['Dry air', 'Unknown', 'Air | Vacuum', 'Air | N2', 'Air', 'Ambient', 'N2', 'Ambient | Ar', 'O2', 'Vacuum', 'N2 >> N2', 'Air | Air', 'N2 | N2', 'Ar | Ar', 'Ar'])))

    storage_time_until_next_deposition_step = Quantity(
        type=str,
        shape=[],
        description="""
    The time between the HTL stack is finalised and the next layer is deposited
- If there are uncertainties, only state the best estimate, e.g. write 35 and not 20-50.
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['12.0', 'Unknown', '20.0', '24.0', '4.0', '15.0'])))

    storage_atmosphere = Quantity(
        type=str,
        shape=[],
        description="""
    The atmosphere in which the sample with the finalised HTL stack is stored until the next deposition step.
Example
Air
N2
Vacuum
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['Dry air', 'Unknown', 'Air', 'Ambient', 'Vacuum', 'N2', 'O2'])))

    storage_relative_humidity = Quantity(
        type=str,
        shape=[],
        description="""
    The relive humidity under which the sample with the finalised HTL stack is stored until next deposition step
- If there are uncertainties, only state the best estimate, e.g write 35 and not 20-50.
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', '20.0', '10.0'])))

    surface_treatment_before_next_deposition_step = Quantity(
        type=str,
        shape=[],
        description="""
    Description of any type of surface treatment or other treatment the sample with the finalised HTL stack undergoes before the next deposition step.
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
            component='EnumEditQuantity', props=dict(suggestions=['', 'Plasma', 'Ar plasma', 'Ozone', 'UV-Ozone', 'He plasma', 'Washed with methanol', 'IPA dipping', 'DMF'])))

    def normalize(self, archive, logger):
        add_solar_cell(archive)
        if self.stack_sequence:
            archive.results.properties.optoelectronic.solar_cell.hole_transport_layer = self.stack_sequence.split(' | ')


