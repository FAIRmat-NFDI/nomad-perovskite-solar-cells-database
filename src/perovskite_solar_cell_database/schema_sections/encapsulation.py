import numpy as np
from nomad.datamodel.data import ArchiveSection
from nomad.metainfo import Quantity


class Encapsulation(ArchiveSection):
    """A section to describe information about the encapsulation of the device."""

    Encapsulation = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if the cell is encapsulated
                    """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    stack_sequence = Quantity(
        type=str,
        shape=[],
        description="""
    The stack sequence of the encapsulation
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- If two materials, e.g. A and B, are mixed in one layer, list the materials in alphabetic order and separate them with semicolons, as in (A; B)
- Use common abbreviations when appropriate but spell it out if risk for confusion.
- There are now separate filed for doping. Indicate doping with colons. E.g. wither aluminium doped NiO-np as Al:NiO-np
Example:
SLG
Epoxy
Cover glass
PMMA
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'Parylene | SLG',
                    'Plastic tape',
                    'Parylene-C',
                    'UV-curated glue | SLG',
                    'SLG | Ossila E131 epoxy resin',
                    "Field's metal",
                    'Scribbling UV-glue',
                    'Kapton tape | Glue',
                    'UV-curable epoxy',
                    'UV-glue | SLG',
                    'Surlyn | SLG',
                    'Epoxy',
                    'Eu(TTA)2(Phen)MAA',
                    'Cover glass-QDs; Epoxy',
                    'Al2O3 | SLG',
                    'Pattex silicon',
                    'UV-glue (NOA 68, Norland products)',
                    'Kapton PI tape with Silicone adhesive',
                    'Polymer | SLG',
                    'Ossila E131 Epoxy Resin',
                    'Viewbarrier (mitsibushi plastic, inc)',
                    'Cavity glass',
                    'Epoxy (3124L(MS), Three Bond)',
                    'Polymer',
                    'SLG',
                    'FTO',
                    'UV curable glue',
                    'Surlyn',
                    'UV-glue (ThreeBond)',
                    'Epoxy | SLG',
                    'Cyanoacrylate',
                    'UV-curated epoxy | SLG',
                    'Parylene-film',
                    'UV-curable epoxy | Cover glass-QDs',
                    'EVOH | S5 | UV | G1',
                    'Face-sealing adhesive sheets',
                    'Polystyrene microgel particles',
                    'Cover glass-QDs | UV-curable epoxy',
                    'Polyolefin',
                    'Paraffin',
                    'PDMS',
                    'SiO2 | Desiccant | SLG',
                    'UV-glue',
                    'Barrier foil',
                    'EVA',
                    'Polyisobutylene',
                    'SiO2 | AB epoxy glue (Super Glue Corp.) | Desiccant | SLG',
                    'UVCA (3035B)',
                    'SLG; UV-selant',
                    'UV epoxy',
                    'SLG | Epoxy',
                    'Glass cyclindrical tube',
                    'Norland Optical Adhesive (NOA) layers on (PET) | micropatterned NOA',
                    'LDPE | PP',
                    'Thermoplastic sealant',
                    'PVP | UV-Epoxy | SLG',
                    'Fluoropolymeric layer',
                    '3M acrylic elastomer (3M VHB 4905)',
                    'SLG | LT-U001',
                    'Cover glass-QDs',
                    'UV curing epoxy',
                    'UV-cured epoxy; Cavity glass',
                    'UHPBF',
                    'UV filter glass and light curable epoxy',
                    'Polyvinyl pyrrolidone | Epoxy resin | SLG',
                    'SnO2-c',
                    'UV Epoxy',
                    'Surlyn | Gover glass',
                    'Unknown',
                    'SL; Unknown:UV cured adhesive',
                    'UV epoxy | SLG',
                    'Glass (Ossila E131)',
                    'UV-glue (ThreeBond, 3052)',
                    'UV-curable epoxy | SLG',
                    'PCL',
                    'Graphene',
                    'Al2O3 | PET',
                    'PDMS-nanocone',
                    'Hot melt polymer foil (Oxford PV) | Cover glass-QDs',
                    'Norland Optical Adhesive (NOA) layers on (PET)',
                    'Carbon-nt',
                    'PET',
                    'Cover glass-QDs; Water-absorbent sealant (HD-S051414W-40, Dynic)',
                    'Desiccant | SLG',
                    'Graphene oxide | Desiccant | SLG',
                    'Ossila E132 resin',
                    'Kapton tape',
                    'Kapton tape | SLG',
                    'UV curable resin',
                    'UV-glue (3035B, ThreeBond Holdings)',
                    'Al2O3 | pV3D3',
                    'Surlyn | FTO',
                    'Cover glass with ultraviolet-curable adhesive',
                    'Polyisobutene',
                    'Cover glass-QDs; Expoxy',
                    'SLG | FTO',
                    'polyisobutylene | SLG',
                    'PMMA; PU',
                    'UVCA (3035B) | Paraffin',
                    'Ag; Carbon-epoxy',
                    'UV sealant | Surlyn | SLG',
                    'PEN',
                    'Self-mixing epoxy',
                    'Teflon',
                    'Al2O3',
                    'UV glue',
                    'Kapton | Ligh-curated glue | SLG',
                    'Adhesive glue 3025 B (Three Bond Holding Co. Ltd)',
                    'ITO | PEN',
                    'Ethylene-vinyl acetate',
                    'EVA | SLG',
                    'PCPD2FBT:BCF',
                    'PMMA',
                    'Desiccant',
                    'SiO2',
                    'Scotch tape',
                    'Meltronix',
                    'Al2O3 | O-Al-CH3 | Al2O3',
                ]
            ),
        ),
    )

    edge_sealing_materials = Quantity(
        type=str,
        shape=[],
        description="""
    Edge sealing materials
- If two materials, e.g. A and Bare used, list the materials in alphabetic order and separate them with semicolons, as in (A; B)
Example:
Epoxy
Surlyn
UV-glue
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'Epoxy  (Pacer  Technology,  SY-QS )',
                    'Thermoplastic',
                    'Araldite 2011',
                    'Kapton tape | Light-curable glue',
                    'NOA 89',
                    'Epoxy; Silicone',
                    'Hot-melting polymer',
                    'UV-glue (3035B, ThreeBond Holdings)',
                    'Ossila Epoxy E131',
                    '467 MP 3M Adhesive Transfer Tape',
                    'PDMS',
                    'polyisobutylene',
                    'Unknown',
                    'UV-curable epoxy',
                    'NOA 88',
                    'UV-curable epoxy (ThreeBond)',
                    'Polymer foil',
                    'Clamp',
                    'Epoxy',
                    'none',
                    'Glue',
                    'UV-glue',
                    'Epoxy adhesive',
                    'Polyurathene',
                    'Epoxy (XNR 5516Z-B1, Nagase ChemteX Corporation)',
                    'NOA 63',
                    'Polyisobutylene',
                    'Epoxy sealant Ossila E131',
                    'UV-glue (NOA 68, Norland products)',
                    'Kapton tape | UV-curable Glue',
                    'Threebond glue',
                    'Light-curated glue',
                    'Surlyn (Du Pont)',
                    'Epoxy; Polymer',
                    'Polymer',
                    'SLG',
                    'Polyolefin elastomer',
                    'Thermally curable epoxy (Kyoritsu Chemical)',
                    'Surlyn',
                    'UV-glue (ThreeBond)',
                    'UV-curable epoxy (Ossila E131)',
                    'Butyl rubber',
                    'Cover glass-QDs',
                    'Polydimethylsiloxane',
                ]
            ),
        ),
    )

    atmosphere_for_encapsulation = Quantity(
        type=str,
        shape=[],
        description="""
    The surrounding atmosphere during encapsulation.
- If the surrounding atmosphere is a mixture of different gases, e.g. A and B, list the gases in alphabetic order and separate them with semicolons, as in (A; B)
- “Dry air” represent air with low relative humidity but where the relative humidity is not known
- “Ambient” represent air where the relative humidity is not known. For ambient conditions where the relative humidity is known, state this as “Air”
- “Vacuum” (of unspecified pressure) is for this purpose considered as an atmospheric gas
Example
N2
Vacuum
Air
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'Dry air',
                    'Unknown',
                    'Air',
                    'Ambient',
                    'N2',
                    'Vacuum',
                    'Ar',
                ]
            ),
        ),
    )

    water_vapour_transmission_rate = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description="""
    The water vapour transmission rate trough the encapsulation.
- If there are uncertainties, only state the best estimate, e.g. write 35 and not 20-50.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    oxygen_transmission_rate = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description="""
    The oxygen transmission rate trough the encapsulation.
- If there are uncertainties, only state the best estimate, e.g. write 35 and not 20-50.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )
