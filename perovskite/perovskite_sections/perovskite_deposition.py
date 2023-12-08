import numpy as np
from nomad.metainfo import MSection, Quantity
from .utils import add_solar_cell
class PerovskiteDeposition(MSection):
    """
    This section contains information about the deposition of the perovskite layer.
    """

    number_of_deposition_steps = Quantity(
        type=np.dtype(np.int64),
        shape=[],
        description="""
    The number of production steps involved in making the perovskite-stack
- A spin coating program that are composed of several segments with different spin speed are still counted as one step (1)
- A spin coating program involving an antisolvent step counts as a 1-step method (1).
- Depositing PbI2 first and subsequently converting it to a perovskite count as a 2-step procedure (2)
- Thermal annealing is considered separately. The motivation for this is that every step is considered to have its own thermal history.
                    """,
        a_eln=dict(
            component='NumberEditQuantity'))

    procedure = Quantity(
        type=str,
        shape=[],
        description="""
    The deposition procedures for the perovskite block.
- The perovskite stack is considered as one block/layer when we consider the synthesis. Thus, even if the perovskite is layered, consider it as one block, i.e. no vertical bars in this field
- When more than one reaction step, separate them by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- There should be as many reaction steps described here as indicated in the field “Perovskite. Deposition. Number of deposition steps”
- Thermal annealing is generally not considered as an individual reaction step. The philosophy behind this is that every deposition step has a thermal history, which is specified in a separate filed. In exceptional cases with thermal annealing procedures clearly disconnected from other procedures, state ‘Thermal annealing’ as a separate reaction step.
- Antisolvent treatment is considered in a separate filed. The motivation for that is that it usually is conducted simultaneously as a spin-coating procedure, and thus acts as an additional aspect of reaction step already accounted for. Exception to this is if there is an antisolvent step that is distinctly separated in time, e.g. a film with a spin-coated perovskite solution is immersed in an antisolvent. In that case, this could eb added as a dipp-coating event, while also being reported in the antisolvent field.
- Even if the most common deposition procedures have been used for 95 % of all reported devise, do not be surprised if you do not find your deposition procedure in the list of reported deposition procedure, as the original dataset tended to use a simplified notation.
- A few clarifications
- Air brush spray
- Deposition with something looking like an old perfume bottle. Classified as a solution technique.
- Brush painting
o A precursor ink is applied with a brush
- CBD
- Chemical bath deposition. Refers to procedures where a film has been immersed in a solution where a reaction occurs. The typical example is when a PbI2 film is immerse in an IPA solution with MAI in which the PbI2 is converted to the perovskite.
- Co-evaporation
- Simultaneous evaporation from multiple sources with line of sight deposition.
- CVD
o Chemical vapour deposition. A gas phase process where a chemical reaction is occurring in the gas phase. If a MA-containing compound is evaporated and reacted with PbI2 where another species is released to the gas phase, it is labeled as CVD. A process where MAI in gas phase react with PbI2 in gas phase is labelled as CVD. A process where MAI or MA gas is reacting with solid PbI2 is instead labelled as a gas reaction as no chemical reaction is occurring the gas phase. Note that all reactions labelled as CVD in the literature may not be CVD even if it is conducted in a CVD reactor, and should instead be labelled as a gas reaction.
- Diffusion
o Solid state reaction where two solid components are mixed. E.g. solid MAI is bought in direct contact with solid PbI2
- Diffusion-gas reaction
- A special case. Where one compound, e.g. MAI is placed on top of another e.g. PbI2 where it is evaporated. It is thus a combination of a gas phase reaction and solid-solid diffusion.
- Dipp-coating
o The thing that separates dipp-coating from CBD is the occurrence of a reaction. If you have component A in solution, dip your substrate in the solution, take it up and you have component A on your substrate, then you have done a dipp-coating. If you have substance A in solution, dip your substrate in the solution, take it up and have something else than A on your substrate, you have done a CBD (e.g. PbI2 dipped in MAI/IPA which gives MAPbI3 and not MAI on the substrate)
- Dropcasting
o A drop is applied to a substrate where it is left to dry without any additional procedures.
- Drop-infiltration
- A mesoporous scaffold in which a drop of the precursor solution is infiltrated without the aid of spin-coating.
- Doctor blading
- There is a family of related techniques, but if it could be described as doctor blading, that is the label to use.
- Evaporation
- Refers to thermal evaporation with line-of-sigh deposition. i.e. PVD
- Flash evaporation
- Fast evaporation (in a flash) of a perovskite that sublimes on another substrate. Line of sight deposition.
- Closed space sublimation
- Evaporation of a well controlled amount of substance (usually in the form of a thin film) in a small container containing the final substrate.
- Gas reaction
- A gas phase reaction. Not a line of sight deposition. In the typical case, MAI is evaporated and the MAI gas builds up a pressure in the reaction chamber in which it reacts with a PbI2 film forming the perovskite.
- Ion exchange
- One perovskite is dipped into a solution (or exposed to a gas) which leads to an ion exchange, e.g. I is replaced by Br.
- Lamination
- A readymade film is transferred directly to the device stack. A rather broad concept. An everyday kitchen related example of lamination would eb to place a thin plastic film over a slice of pie.
- Recrystallization
- A perovskite that already have been formed is deformed and then recrystallised. E.g. MAPbI3 is exposed to Methylamine gas for a short while which dissolved the perovskite which then can crystallize again
- Rinsing
- Cleaning step with a solvent
- Sandwiching
- When a readymade top stack simply is placed on top of the device stack. Could be held together with clams.
- Ultrasonic spray
- A bit like air brush spray but with better control of droplet size. Classified as a solution technique.
Example
Spin-coating
Spin-coating >> Spin-coating
Spin-coating >> CBD
Spin-coating >> Gas reaction
Drop-infiltration
Co-evaporation
Doctor blading
Evaporation >> Evaporation
Evaporation >> Spin-coating
Evaporation >> Gas reaction
Slot-die coating
Spray-coating
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['Spin-coating | Spin-coating >> Spin-coating', 'Gas-assisted fast crystallisation', 'Electrospraying >> Dropcasting', 'Slot-die coating >> Doctor blading', 'Spin-coating >> Spin-coating', 'Spin-coating >> Evaporation', 'Roller-coating >> Roller-coating', 'Spin-coating >> Drop-infiltration >> Recrystallization', 'Co-evaporation >> Evaporation >> Spin-coating', 'Evaporation >> Evaporation >> Evaporation', 'Spin-coating >> Vapour annealing >> CBD', 'Spin-coating >> CBD >> Spin-coating >> Spin-coating', 'Evaporation >> Gas reaction >> Washing', 'Spin-coating >> Diffusion-gas reaction', 'Spin-coating | Spin-coating', 'Spin-coating >> Gas reaction >> Ion exchange', 'Spin-coating >> Spin-coating >> Rinsing >> Spin-coating', 'Slot-die coating >> Dipp-coating', 'Spin-coating >> Spin-coating >> Gas reaction', 'Spin-coating >> Dipp-coating >> Rinsing', 'Spin-coating >> Spin-coating | Spin-coating', 'Evaporation >> Evaporation >> Gas reaction >> Dipp-coating', 'Slot-die coating', 'Brush painting', 'Ultrasonic spray >> Gas reaction', 'Spin-coating >> CBD', 'Co-evaporation >> Gas reaction >> Spin-coating', 'Evaporation >> Flash evaporation >> Evaporation >> Flash evaporation', 'Spin-coating >> Spray-coating', 'Ultrasonic spray', 'Spin-coating | Evaporation', 'Spin-coating >> CBD >> Spray-coating', 'Space-limited inverse temperature crystallization', 'Evaporation | Spin-coating', 'Spin-coating | Dripping', 'Meniscus coating', 'Spin-coating | Spin-coating >> IPA washing', 'Evaporation >> Sandwiching >> Rinsing', 'Co-evaporation', 'Evaporation >> CBD >> CBD', 'Co-evaporation >> Diffusion-gas reaction', 'Ultrasonic spray >> Ultrasonic spray', 'Spin-coating >> CBD >> Gas reaction', 'Evaporation >> Diffusion-gas reaction', 'Sputtering >> Gas reaction', 'Spin-coating >> CVD', 'Sputtering >> Sulfurization', 'Spin-coating >> Air brush spray >> Air brush spray', 'Spray-coating >> Gas reaction', 'Spin-coating >> Recrystallization', 'Inkjet printing', 'Spin-coating >> Spin-coating >> Spin-coating', 'Evaporation >> Spin-coating', 'Spin-coating >> Gas reaction >> Solvent annealing >> Recrystallization', 'Pulsed laser deposition >> Gas reaction', 'Dipp-coating >> Dipp-coating', 'Spin-coating >> CBD >> CBD', 'Spin-coating >> Closed space sublimation', 'Evaporation >> Evaporation >> Evaporation >> Evaporation >> Evaporation >> Evaporation', 'Co-evaporation >> Spin-coating', 'Air brush spray', 'Spin-coating | Spray-coating', 'Flash evaporation >> CBD', 'Doctor blading >> Doctor blading', 'Dropcasting >> Spin-coating', 'Spray-coating >> Spin-coating', 'Ultrasonic spray >> CBD', 'Spin-coating >> Dipp-coating', 'Single-source thermal evaporation', 'Inverse temperture crysilization >> Lamination', 'LT-SCD >> LT-SCD', 'Evaporation >> Gas reaction >> Gas reaction', 'Spin-coating >> Dropcasting >> Spin-coating', 'Vacuum flash evaporation', 'Drop-infiltration >> Recrystallization', 'Spray-coating >> Spray-coating', 'Evaporation >> Ultrasonic spray', 'Electrodeposition >> Spin-coating', 'Spin-coating >> Dipp-coating >> Spin-coating', 'Evaporation >> Spin-coating >> Spin-coating', 'Spin-coating >> Dropcasting', 'Dropcasting >> CBD', 'Spin-coating >> Evaporation >> Ultrasonic spray', 'Solvent evaporation crystallization', 'GC-LCG', 'Drop-infiltration >> Drop-infiltration', 'Dropcasting >> Pneumatic pressure', 'spin-coatng', 'Spin-coating >> Spin-coating >> Diffusion', 'Evaporation >> Evaporation >> Gas reaction', 'Evaporation >> Gas reaction', 'Spin-coating >> Spin-coating >> Spin-coating >> Spin-coating >> Dropcasting >> Rinsing', 'Doctor blading >> CBD', 'Spin-coating >> CBD >> Washing', 'PVD', 'Dipp-coating >> CBD', 'Spin-coating >> Inkjet printing', 'Spin-coating >> CBD >> Rinsing', 'Dipp-coating', 'Spin-coating >> Air brush spray', 'Hot-casting', 'Spin-coating >> Spin-coating >> Ion exchange', 'Springkling >> Recrystallization', 'Spin-coating >> Spin-coating >> Spin-coating >> Spin-coating >> Spin-coating >> Dropcasting >> Rinsing', 'Electrodeposition >> Dipp-coating >> CBD', 'Evaporation >> CBD >> CBD >> CBD', 'Drop-infiltration >> CBD', 'Spin-coating | Gas reaction', 'Spin-coating >> Spin-coating >> Air brush spray', 'Electrospraying >> Gas reaction', 'Spin-coating >> Diffusion', 'Evaporation', 'Spin-coating >> Evaporation >> Spray-coating', 'Electrodeposition >> Gas reaction >> CBD', 'Electrospraying', 'Unknown', 'Spray-pyrolys', 'Evaporation >> Inkjet printing', 'CBD', 'Drop-infiltration', 'Spin-coating >> CBD >> Ion exchange', 'Spin-coating >> Evaporation >> CBD', 'CVD', 'Roller-coating', 'Co-evaporation >> Co-evaporation', 'Spin-coating >> Spin-coating >> Spin-coating >> Spin-coating >> Spin-coating >> Spin-coating', 'Unknown >> Unknown', 'Spin-coating >> Sandwiching', 'Spin-coating >> Spin-coating >> CBD', 'Electrodeposition >> CBD', 'Spin-coating >> Co-evaporation', 'Doctor blading', 'Spin-coating >> Printing', 'Magnetron sputtering', 'Evaporation >> Evaporation', 'Spin-coating >> Drop-infiltration', 'Spin-coating >> Ligand exchange >> Dipp-coating', 'Soft-cover deposition', 'Spin-coating >> Spin-coating >> Dipp-coating >> Dipp-coating >> Spin-coating >> Dipp-coating >> Dipp-coating >> Spin-coating >> Dipp-coating >> Dipp-coating', 'Slot-die coating >> Spin-coating', 'Evaporation >> Electrodeposition', 'Spin-coating >> Dipp-coating >> Dipp-coating >> Spin-coating >> Dipp-coating >> Dipp-coating >> Spin-coating >> Dipp-coating >> Dipp-coating', 'Spin-coating >> Evaporation >> Evaporation', 'Spin-coating >> Gas reaction', 'Space-confined single crystal formation', 'Electrospinning', 'Spin-coating >> CBD >> Spin-coating', 'Electrodeposition >> Gas reaction >> Spin-coating', 'Closed space sublimation', 'Spin-coating >> Spin-coating >> Spray-coating', 'Spin-coating >> CBD >> Recrystallization', 'Spin-coating | Spin-coating >> IPA washing | Spin-coating >> IPA washing | Spin-coating >> IPA washing', 'Spin-coating >> Spin-coating >> Evaporation', 'Co-evaporation >> Co-evaporation >> Co-evaporation', 'Spin-coating >> CBD >> Spin-coating >> Gas reaction', 'Spin-coating | Dropcasting', 'CBD >> Spin-coating >> Gas reaction', 'Substrate vibration assisted dropcasting >> Substrate vibration assisted dropcasting', 'Roller-coating >> Spin-coating', 'Spray-coating >> CBD', 'Spin-coating >> Gas reaction >> Gas reaction >> Gas reaction', 'Spin-coating >> Spin-coating >> Dropcasting >> Rinsing', 'Spin-coating | CBD', 'Dropcasting', 'Spin-coating >> Spin-coating >> Spin-coating >> Spin-coating', 'Sputtering >> Spin-coating', 'Pulsed laser deposition', 'Single crystal growth', 'Evaporation >> Diffusion', 'Spin-coating >> Electrospraying', 'Blow-drying', 'Spin-coating >> Spin-coating >> Close space sublimation', 'Dipp-coating >> Spin-coating', 'Spin-coating | Spin-coating >> IPA washing | Spin-coating >> IPA washing', 'Inkjet printing >> Diffusion-gas reaction', 'Spin-coating >> Ion exchange', 'Drop-infiltration >> Spin-coating', 'Spin-coating >> Spin-coating >> Recrystallization', 'Flash evaporation', 'Spin-coating', 'Spin-coating >> Gas reaction >> Spin-coating', 'Electrodeposition >> CBD >> CBD', 'Crystallization >> Recrystallization', 'Slot-die coating >> CBD', 'Hot-pressed', 'Dipp-coating >> Gas reaction', 'Spray-coating', 'Spin-coating >> Spin-coating >> Spin-coating >> Dropcasting >> Rinsing', 'Air brush spray >> Air brush spray', 'Electrodeposition >> Electrodeposition', 'Sputtering >> CBD', 'Spin-coating >> Ultrasonic spray', 'Evaporation >> CBD', 'Spin-coating >> Dipp-coating >> Dipp-coating', 'Evaporation >> Evaporation >> Evaporation >> Evaporation', 'Slot-die coating >> Slot-die coating', 'Spin-coating >> Gas reaction >> Gas reaction', 'Spin-coating >> Condensation >> CBD'])))

    aggregation_state_of_reactants = Quantity(
        type=str,
        shape=[],
        description="""
    The physical state of the reactants
- The three basic categories are Solid/Liquid/Gas
- The perovskite stack is considered as one block/layer when we consider the synthesis. Thus, even if the perovskite is layered, consider it as one block, i.e. no vertical bars in this field
- When more than one reaction step, separate the aggregation state associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- Most cases are clear cut, e.g. spin-coating involves species in solution and evaporation involves species in gas phase. For less clear-cut cases, consider where the reaction really is happening as in:
o For a spray-coating procedure, it is droplets of liquid that enters the substrate (thus a liquid phase reaction)
o For sputtering and thermal evaporation, it is species in gas phase that reaches the substrate (thus a gas phase reaction)
Example
Liquid
Gas >> Liquid
Liquid >> Liquid >> Liquid
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['Liquid >> Unknown', 'Liquid >> Gas >> Gas >> Gas', 'Liquid | Liquid >> Liquid | Liquid >> Liquid', 'Liquid | Liquid', 'Liquid >> Liquid >> Solid', 'Gas', 'Liquid | Liquid >> Liquid', 'Liquid | Liquid >> Liquid | Liquid >> Liquid | Liquid >> Liquid', 'Gas >> Liquid >> Liquid >> Liquid', 'Liquid >> Liquid >> Liquid', 'Liquid >> Liquid >> Liquid >> Gas', 'Gas >> Solid >> Liquid', 'Solid >> Liquid', 'Liquid | Gas', 'Unknown', 'Liquid >> Liquid >> Liquid >> Liquid >> Liquid >> Liquid >> Liquid >> Liquid >> Liquid >> Liquid', 'Liquid >> Liquid >> Liquid >> Liquid', 'Liquid >> Liquid', 'Liquid >> Liquid >> Liquid >> Liquid >> Liquid >> Liquid', 'Gas >> Gas >> Liquid', 'Liquid >> Liquid >> Liquid >> Liquid >> Liquid >> Liquid >> Liquid', 'Liquid >> Gas', 'Liquid >> Gas >> Gas', 'Liquid | Liquid >> Liquid | Liquid', 'Liquid >> Gas >> Liquid', 'Solid', 'Liquid', 'Gas >> Gas >> Gas >> Gas', 'Liquid >> Liquid | Liquid', 'Gas >> Gas >> Gas >> Liquid', 'Liquid >> Liquid >> Gas', 'Unknown >> Liquid', 'Liquid >> Liquid >> Liquid >> Liquid >> Liquid', 'Gas >> Gas >> Gas', 'Gas >> Gas >> Gas >> Gas >> Gas >> Gas', 'Liquid >> Solid', 'Liquid >> Liquid >> Liquid >> Liquid >> Liquid >> Liquid >> Liquid >> Liquid >> Liquid', 'Gas >> Liquid', 'Gas >> Gas', 'Gas >> Liquid >> Liquid', 'Gas | Liquid', 'Gas >> Solid'])))

    synthesis_atmosphere = Quantity(
        type=str,
        shape=[],
        description="""
    The synthesis atmosphere
- When more than one reaction step, separate the atmospheres associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- The number and order and deposition steps must line up with the previous columns.
- If the synthesis atmosphere is a mixture of different gases, e.g. A and B, list the gases in alphabetic order and separate them with semicolons, as in (A; B)
- “Dry air” represent air with low relative humidity but where the relative humidity is not known
- “Ambient” represent air where the relative humidity is not known. For ambient conditions where the relative humidity is known, state this as “Air”
- “Vacuum” (of unspecified pressure) is for this purpose considered as an atmospheric gas
- This category was included after the projects initial phase wherefor the list of reported categories is short. Thus, be prepared to expand the given list of alternatives in the data template.
Example
N2
Air
N2 >> N2
Vacuum
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['N2 | Vacuum', 'Inert', 'DMSO; N2 >> N2', 'Air >> MAI; N2', 'FAI >> Unknown', 'FABr', 'FAI >> FABr @ 75 >> 25', 'Methylamin; N2', 'Vacuum >> MAI; toluene', 'Ar; MAI; Pbl2', 'N2 >> N2; TBP', 'Air >> Ar', 'Ar; MAI; PbI2', 'Methylamin; N2 >> Methylamin; N2', 'Acetone; N2 >> N2', 'FAI; N2; Vacuum', 'N2 >> Vacuum', 'Air >> MAI; NH4Cl; Vacuum', 'Vacuum >> MAI; Vacuum >> Vacuum; BAI', 'Unknown >> Air', 'Air >> Ar; Methylamin', 'Vacuum >> FAI', 'N2 >> Air; Methylamin; HI', 'Vacuum >> Vacuum >> IPA', 'N2 >> MABr >> MAI', 'Air >> MAI; Vacuum', 'Unknown >> Vacuum', 'Unknown >> Br2', 'O2', 'Unknown >> Unknown >> Air', 'Air >> MACl >> MAI', 'N2 >> MAI; N2', 'Unknown >> Methylamin', 'N2 >> N2; IPA >> N2', 'N2 >> Dry air', 'N2 >> N2 >> N2 >> N2 >> N2 >> N2 >> N2 >> N2 >> N2', 'Vacuum >> N2', 'N2 >> Air; Methylamin >> Air; HI', 'N2 >> Chlorobenzene; N2 >> N2', 'Dry air | Dry air', 'N2 >> N2 >> N2 >> N2', 'Vacuum >> FAI; Vacuum', 'N2; Vacuum', 'Vacuum >> Vacuum', 'Dry air >> MAI', 'Vacuum >> Vacuum >> N2', 'Ar', 'Unknown >> MAI; Vacuum', 'Air >> Air; I2 >> N2', 'Air >> N2 >> Air', 'N2', 'Ar; MAI; PbCl2', 'Vacuum >> Air; MAI', 'N2 >> FAI; MAI; Vacuum', 'N2 | N2 | N2 | N2', 'Vacuum >> IPA; MAI', 'Vacuum >> TiBr4', 'Air >> Air >> Air', 'FAI', 'N2 >> FA-Ac', 'Air >> MaBr', 'N2 >> N2 >> FAI; Vacuum', 'Vacuum >> Ar; MAI', 'N2 >> MAI', 'Vacuum >> Vacuum >> Unknown', 'N2 | N2 | N2', 'Liquid Air', 'N2 >> MACl', 'Vacuum >> N2; MAI', 'N2 >> N2; Toluene >> N2', 'Air >> Vacuum >> N2', 'Ambient >> Air; MAI', 'N2 >> FAI; Vacuum >> N2', 'Vacuum >> FAI; N2', 'Ar >> MABr', 'Unknown >> Unknown >> Vacuum', 'Unknown >> Unknown >> Methylamin', 'Air >> Vacuum >> Air', 'Vacuum >> Chlorobenzene; MAI', 'Air >> Air; MABr', 'Ambient >> Ambient', 'Air >> MAI; MACl; MABr; Vacuum', 'N2 >> Air; Methylamin', 'Dry air', 'Vacuum >> Vacuum >> Vacuum >> Vacuum >> Vacuum >> Vacuum', 'Unknown >> N2; MAI', 'Unknown >> MAI', 'Vacuum >> Vacuum >> FAI; N2', 'Unknown >> FAI', 'N2 >> Air; DMSO >> Air; DMSO >> Air; Methylamin', 'Vacuum >> N2 >> N2 >> N2', 'Dry air >> Dry air >> Dry air', 'Chlorobenzene; N2', 'DMF; N2 >> N2', 'N2 >> Vacuum >> N2', 'Unknown >> Unknown >> MAI', 'Inert >> Inert', 'Air >> Air >> Pyridine', 'Unknown >> Vacuum >> Air', 'Unknown >> Air; Methylamin', 'Vacuum >> Ar', 'FAI; FABr >> Unknown', 'Air >> Air | Air', 'Unknown >> MABr', 'Vacuum >> Unknown', 'N2 >> N2 >> N2', 'Unknown', 'Ar >> Ar >> Ar', 'Air >> Br2', 'N2 >> N2', 'N2 >> Methylamin; N2', 'N2 >> N2 >> MAI; N2', 'Unknown >> Unknown >> Unknown', 'Dry air >> Dry air', 'Unknown >> Pyridine', 'N2 >> Air; MAI', 'Air >> Air; MAI', 'N2 >> FA', 'Hydrazine; N2', 'N2 >> Ambient', 'Vacuum >> Vacuum >> Vacuum', 'FAI >> FABr @ 25 >> 75', 'Vacuum >> MAI', 'Ambient', 'Unknown >> Unknown', 'N2 >> Vacuum >> Vacuum', 'Air >> Air; MACl', 'Unknown >> MACl', 'Air >> Air; Methylamin', 'Air >> Methyl amine', 'FAI >> FABr @ 50 >> 50', 'Air >> MAI', 'Vacuum >> MAI; Vacuum; FAI >> N2', 'Ait >> Air; MAI', 'Air', 'N2 >> MAI >> MABr', 'Vacuum', 'Air >> FAI; FABr; MACl; Vacuum', 'Dry air >> Air; MAI', 'Vacuum >> Vacuum >> Vacuum >> Vacuum', 'Unknown >> N2; MAI >> Unknown', 'Air >> Air', 'N2 >> Air; DMSO; HBr >> Air; DMSO >> Air; Methylamin', 'N2 >> Air', 'Air >> Air; HI >> Air; Methylamin >> Air; Hi', 'Vacuum >> MAI; N2', 'Vacuum >> Vacuum >> I2; N2 >> N2', 'Vacuum >> Air', 'N2 >> MAI; N2; O2', 'Vacuum >> Vacuum >> FAI; Vacuum', 'Air >> FAI; Vacuum', 'Glovebox', 'Air >> Air >> N2', 'Air >> Methylamine', 'Air >> N2', 'Vacuum >> FAI; N2; Vacuum', 'Air >> Methylamin; Vacuum', 'Unknown >> Unknown >> Unknown >> MAI', 'N2 >> N2 >> N2 >> N2 >> N2 >> N2 >> N2 >> N2 >> N2 >> N2', 'N2 >> MAI; Vacuum', 'Air | Ari; MAI', 'Air >> MAI; NH4Cl', 'N2 >> FAI; FACl; Vacuum', 'N2 >> N2 >> Vacuum', 'N2 | N2', 'N2 >> FAI; Vacuum', 'Air >> Air >> Air >> Air', 'N2 >> Methylamin', 'N2 >> BEAI2; N2', 'Dry air >> Dry air; Methylamin', 'Air >> Air >> Air >> Air >> Air >> Air', 'N2 >> DMSO; N2 >> N2', 'Air | Air', 'IPA; N2 >> N2', 'Ar >> Ar', 'N2 >> Methylamin; Vacuum', 'Air; O2', 'Air >> Vacuum', 'Vacuum >> N2 >> N2', 'N2 >> Ar; MAI', 'N2 >> FAI; MABr; MACl; N2; Vacuum', 'Ar >> Vacuum', 'Vacuum >> MAI; Vacuum', 'N2 >> MABr', 'Unknown >> Air >> Air', 'N2 >> N2; 1,2-dichlorobenzene >> N2'])))

    synthesis_atmosphere_pressure_total = Quantity(
        type=str,
        shape=[],
        description="""
    The total gas pressure during each reaction step
- When more than one reaction step, separate the pressures associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- The number and order of deposition steps must line up with the previous columns.
- Pressures can be stated in different units suited for different situations. Therefore, specify the unit. The preferred units are:
o atm, bar, mbar, mmHg, Pa, torr, psi
- If a pressure is not known, stat that as ‘nan’
- For values with uncertainties, state the best estimate, e.g. write 100 pa and not 80-120 pa.
Example
1 atm
0.002 torr
1 atm >> 1 atm >> nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', '1 atm >> 1 atm', '0.000001 mbar', '1 atm | 1 atm', '1 atm >> 0.00003 bar', '1 atm >> 1 atm >> 1 atm >> 1 atm >> 1 atm >> 1 atm >> 1 atm >> 1 atm >> 1 atm >> 1 atm', '1 atm >> 60 Pa', '1 atm', '0.000001 mbar >> 1 atm', '1 atm >> 1 atm >> 1 atm >> 1 atm >> 1 atm >> 1 atm >> 1 atm >> 1 atm >> 1 atm', '1 atm >> 1 atm | 1 atm', '0.00001 mbar', 'nan | 700 Pa'])))

    synthesis_atmosphere_pressure_partial = Quantity(
        type=str,
        shape=[],
        description="""
    The partial pressures for the gases present during each reaction step.
- When more than one reaction step, separate the pressures associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- The number and order of deposition steps must line up with the previous columns.
- If the synthesis atmosphere is a mixture of different gases, e.g. A and B, list the partial pressures and separate them with semicolons, as in (A; B). The list of partial pressures must line up with the gases they describe.
- In cases where no gas mixtures are used, this field will be the same as the previous filed.
Example
1 atm
0.002 torr; 0.03 torr
0.8 atm; 0.2 atm >> 1 atm >> nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', '1 atm >> 1 atm', '0.000001 mbar', '1 atm | 1 atm', '1 atm >> 1 atm >> 1 atm >> 1 atm >> 1 atm >> 1 atm >> 1 atm >> 1 atm >> 1 atm >> 1 atm', '1 atm', '0.000001 mbar >> 1 atm', '1 atm >> 1 atm >> 1 atm >> 1 atm >> 1 atm >> 1 atm >> 1 atm >> 1 atm >> 1 atm', '1 atm >> 1 atm | 1 atm', '0.00001 mbar', '1 atm >> 0.00003 bar'])))

    synthesis_atmosphere_relative_humidity = Quantity(
        type=str,
        shape=[],
        description="""
    The relative humidity during each deposition step
- When more than one reaction step, separate the relative humidity associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- The number and order of deposition steps must line up with the previous columns
- If the relative humidity for a step is not known, stat that as ‘nan’
- For values with uncertainties, state the best estimate, e.g. write 35 and not 30-40.
Example
35
0 >> 20
25 >> 25 >> 0
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', '40.0', '25', '30 >> 30', '0 >> 40 >> 0', '15', '0 >> 0', '0.4', '0 >> 1', '0 >> 22 >> 0', '0', '1', '5', '85', '32', '10.0', '70', '28', '2', '15 >> 15', '55 >> 55', '80', '30 | 30', '45', '20 >> 20', '40', '75', '20', '60', '65', '36', '45 >> 45', '0 >> 20', '24', '0 >> 16 >> 0', '30', '55', '8', '0 >> 30', '90', '25 >> 25', '35 >> 35', '0 >> 12 >> 0', '10 >> 0', '40 >> 40', '0.01', '52', '70 >> 70', '0 >> 33 >> 0', '27.5 >> 27.5 >> 27.5', '50 >> 50', '10 >> 10', '42', '0.0', 'nan >> 40', '50', '40 >> 40 >> 40', '0 >> 60', '65 >> 65', '35', '12 >> 12', '0 >> 40', '42 >> 42', '30; 40', '60 >> 60', '10'])))

    solvents = Quantity(
        type=str,
        shape=[],
        description="""
    The solvents used in each deposition procedure for each layer in the stack
- When more than one reaction step, separate the solvents associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If a solvent is a mixture of different solvents, e.g. A and B, list the solvents in alphabetic order and separate them with semicolons, as in (A; B)
- The number and order of deposition steps must line up with the previous columns.
- For non-liquid processes with no solvents, state the solvent as ‘none’
- If the solvent is not known, state this as ‘Unknown’
- Use common abbreviations when appropriate but spell it out when risk for confusion
- This category was included after the projects initial phase wherefor the list of reported categories is short. Thus, be prepared to expand the given list of alternatives in the data template.
Example
DMF; DMSO
GBL
DMF >> IPA
DMF >> none
DMF; DMSO >> IPA
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['DMF; DMSO >> H2O; Methanol', 'DMF >> none >> Unknown', 'Diiodoctane, DMF', 'Unknown >> none', 'n-methyl-2-pyrrolidone', 'acetonitrile; DMF; DMSO >> IPA', 'DMF', 'Octane >> Methyl acetate >> Ethyl acetate', 'DMSO; GBL >> DMF; IPA', 'DMSO | 1-pentanol', 'Ethanol', 'GBL; DMSO; n-butanol', 'DMF; DMSO >> Octane >> IPA', 'DMF; Furfural', 'Octane >> Methyl acetate', 'DMF; DMSO >> H2O; IPA', 'DMF; DMSO >> IPA >> IPA >> IPA', 'Octane >> IPA', 'none; DMF >> IPA', 'DMF >> Methanol', 'acetonitrile', 'acetonitrile; DMF', 'DMSO; N-methyl-2-pyrrolidone', 'DMF; DMSO >> IPA', 'GBL; N-methyl-2-pyrrolidinone', 'DMF; DMSO >> DMF; IPA', 'GBL; Ethanol', 'DMF; DMSO; NMP', 'none >> 2-methoxyethanol; Ethanol', 'DMF >> IPA >> IPA >> IPA', 'DMF >> H2O; IPA >> Unknown', 'DMSO; GBL >> IPA', 'DMF >> Ethyl acetate', 'DMF >> IPA >> Anisole', 'Diethyl ether; DMF; DMSO', 'DMF; Benzaldehyde', 'DMF; g-Valerolacetone', '1-Ethyl-2-pyrrolidone >> none', 'DMF >> DMSO >> IPA', 'Ethanol; Methylamine', 'DMSO; acetonitrile >> IPA', 'BA; Ethanol >> none', 'acetonitrile; NMP', 'Unknown >> Unknown', 'DMF >> n-hexyl alchohol', 'DMSO >> Hexane; Toluene', 'NMP', 'Dimethylacetamide; DMSO', 'Ethanol; H2O', 'DMF; DMSO >> n-butanol', 'DMF >> DMSO; IPA', 'DMSO >> 1-butanol', 'DMF; DMSO >> GBL; IPA', 'DMF >> Cyclohexene; IPA', 'Heptane; Hexane', 'GBL >> DMF', 'GBL', 'DMF; Methylfomramid', 'none >> none >> none >> none >> none >> none', 'DMF; GBL; IPA', '1-Octadecene; n-Heptane >> none', 'Octane >> Octane >> Octane >> Octane', 'Ethyl acetate', 'DMF; DMSO; GBL; NMP', 'DMF >> DMF >> Cyclohexene; IPA', 'Toluene', 'DMSO; NMP', 'DMF; DMSO >> IPA; o-dichlorobenzene', 'Acetic acid; GBL', 'DMF >> IPA; NMP', 'DMF; DMSO >> Methanol', 'DMF >> none >> none', 'N,N-dimethylacetamide', 'DMSO >> Methanol', 'DMF >> IPA; n-hexane', 'Chlorobenzene >> none', 'DMF >> Octane >> Methyl acetate >> Methyl acetate', 'Toluene >> IPA', 'DMAc; NMP', 'DMF >> Octane >> Octane >> Octane >> Octane >> Methyl acetate >> Methyl acetate', 'none', 'DMF >> Toluene', 'DMF; NMP >> IPA', 'acetonitrile; DMF >> IPA', 'DMF; GLB', 'Chlorobenzene', 'methylamine formate; IPA', 'DMF; THF', 'Ethyl amine; HCl', 'DMF; GBL', 'DMF >> H2O', '2-Methoxy-ethanol', '2‐butoxyethano; DMSO', 'DMF; Tetrahydrothiophene-1-oxide', '2-methoxyethanol; DMSO', 'Cyclohexyl-2-pyrrolidone; DMF', 'DMF; Benzylamine', 'DMSO; NMP >> IPA', 'DMF; DMSO >> Hexane', 'DMF >> IPA >> DMF; IPA', 'DMF >> Methanol | Cyclohexane', 'DMF; Tetrahydrothiophene 1-oxid', 'Cl-Cyclohexane; DMF', 'DMSO >> DMSO >> DMSO', 'DMF; NMP', 'DMF; Me-Cyclohexane', 'DMSO >> IPA >> Toluene', 'none >> none', 'DMSO; GBL @ 3; 7 >> IPA', 'DMF; DMSO >> Chloroform', 'DMF | IPA | H2O | Ethanol', 'DMSO; GBL @ 3; 7 >> DMSO; GBL @ 3; 7', 'DMF; DMSO', 'DMF; TBP >> IPA', 'DMSO >> IPA >> Toluene >> none', 'DMF >> IPA >> Chlorobenzene; DMF', 'DMF >> Unknown', 'Ethanol; H2O >> Chlorobenzene; Tert-butanol', 'DMF >> Chex; IPA', 'Unknown >> none >> none', 'acetonitrile; DMF; Methoxyactonitrile', 'none >> Methanol; Ethanol', 'DMSO >> Octane', 'Chlorobenzene >> Methylacetate', 'DMF; GBL; IPA >> IPA', 'Methylammonium acetate', 'DMSO; o-xylene', 'DMSO | Propanetriol', 'Ocatane >> MeOAc', 'DMSO >> IPA', 'DMF; HCl >> IPA', 'DMSO >> Ethanol', '2-methoxyethanol; acetonitrile', 'IPA >> DMF', 'DMF >> Pentan-1-ol >> Unknown', 'none >> IPA', 'DMF; HCl', 'DMF; DMSO >> Cyclohexane; IPA', 'DMF >> Cyclohexane; IPA', 'DMF; DMSO >> Chlorobenzene; IPA', 'DMF; o-DCB', 'DMF >> Methanol >> Methanol', 'Unknown >> IPA >> none', '2-methoxyethanol', 'H2O >> none', 'DMF >> IPA >> DMF >> IPA >> DMF >> IPA', 'n-propylamine', 'DMF >> none >> none >> none', 'THF', 'DMSO >> Toluene', 'DMF >> tert-butanol; Chlorobenzene', 'DMF; Glycerol >> DMF >> IPA', 'Butylamine', 'DMF; o-xylene', 'DMF; DMSO >> none >> none >> none', 'Ethanol; H2O >> IPA', 'IPA', 'DMF; DMSO >> Toluene', 'DMF >> Ethanol; IPA', 'acetonitrile; Ethanol; Methylamine', 'DMSO >> none', 'Hexane; Octane', 'H2O >> IPA', 'NMP >> IPA', 'Octane', 'DMF >> IPA >> Toluene', 'Dimethylacetamide; DMSO; NMP', 'H2O >> none >> IPA', 'DMSO; GBL', 'Dimetyletanamid', 'Dimethylacetamide; DMF', 'DMF; DMSO; HAc >> IPA', 'Diiodomethane; DMF; DMSO', 'DMF; DMSO | IPA', 'DMF; DMSO; HCl >> IPA', 'DMF >> Methanol >> Methanol >> Methanol', 'H2O >> H2O; HI >> IPA', 'DMSO; GBL >> none', 'Methylacetate', 'DMF >> IPA >> DMF >> IPA', 'Methanol; THF', 'IPA >> DMF >> IPA', 'Acetic acid; Ethanol; Water', 'DMF; DMSO; Formamide', 'GBL >> IPA', 'DMF; H2O', 'DMF; DMSO >> Ethanol', '2-methoxyethanol; DMSO; GBL', 'Butylamine; DMF; DMSO >> Butanol', 'Octane >> Pb(OAc)2 satured ethyl acetate solution >> Ethyl acetate >> Octane >> Pb(OAc)2 satured ethyl acetate solution >> Ethyl acetate >> Octane >> Pb(OAc)2 satured ethyl acetate solution >> Ethyl acetate', 'DMF; DMSO >> Methyl acetate', 'DMF; DMSO | IPA >> IPA', 'DMF; THF >> IPA', 'DMF >> Chlorobenzene; IPA', 'DMF; DMSO >> IPA >> DMSO; IPA', 'DMF; NNP', 'DMSO; GBL @ 4; 7 >> IPA', 'GBL; NMP', 'DMF >> IPA >> Methybenene', 'GBL; DMSO', 'Octane >> Ethyl acetate', 'IPA >> IPA', 'Unknown', 'Water >> Ethanol >> IPA', 'H2O; HI; Methylamine', 'DMF; DMA >> IPA', 'Hexane >> Octane', 'DMSO; GBL; IPA', 'IPA >> Ethanol', 'none | IPA', 'Octane >> Octane >> Octane >> Octane >> Octane >> Methyl acetate', 'Terpineol', 'Unknown >> IPA', 'DMF; Acetophenone', 'DMF; N-Methyl-2-pyrrolidone', 'GBL >> GBL', 'none >> IPA >> IPA', 'DMF; DMSO; H2O', 'Hexane', 'DMF | IPA', 'DMF >> DMF; IPA', 'Dimethylacetamide', 'DMF >> IPA; Toluene', 'DMSO; Hac >> IPA', 'DMF >> Ethanol >> Ethanol', 'none >> Ethanol', 'DMSO >> H2O; IPA', 'DMF >> PA', 'Ethyl acetate >> Ethyl acetate', 'DMF >> Ethanol', 'DMF >> DMF', 'DMSO; H2O >> IPA', 'none >> none >> none >> IPA', 'DMF >> n-butyl alchohol', 'DMF; HMPA >> IPA', 'DMF >> IPA; Propanol', 'DMF | DMF; IPA', 'none >> none >> none', 'DMF; DMSO @ 9; 1 >> IPA', 'DMF; IPA', 'Methylamine >> Methylamine', 'Methyl acetate >> Ethyl acetate', 'none >> Hydrophosphorous acid; IPA', 'DMF >> n-amyl alcohol', 'DMF >> IPA; TBP', 'DMSO; GBL; NMP', 'DMSO; BL', 'Aceton; DMF >> IPA', 'DMSO | Butanol; IPA', 'none >> IPA >> IPA >> IPA', 'DMF; DMSO >> Chlorobenzene', 'DMF >> Cyclohexanol; IPA', 'DMF; DMSO >> none', 'DMF >> DMF >> Ethanol', 'Water >> none', 'Octane >> Methyl acetate >> Methyl acetate', 'DMF; DMSO; Pyridin', 'DMF; DMSO; Methanol', 'DMF >> IPA >> none', 'DMF >> Octane >> Pb(OAc)2 satured ethyl acetate solution >> Ethyl acetate >> Octane >> Pb(OAc)2 satured ethyl acetate solution >> Ethyl acetate >> Octane >> Pb(OAc)2 satured ethyl acetate solution >> Ethyl acetate', 'DMF >> Octane >> Octane >> Octane >> Methyl acetate >> Methyl acetate', 'DMF; DMSO >> Chlorobenzene; DMF', 'DMF; DMSO >> DMF; DMSO >> DMSO >> DMSO | IPA', 'none >> Ethanol; Methoxyethanol', 'DMF; Tetraline', 'Dimethylacetamide >> IPA', 'Acetic acid; GBL; Propanol', 'DMF | none', 'DMF; DMSO; N-cyclohexyl-2pyrrolidone', 'DMF; DMSO >> IPA >> IPA', 'DMF; DMSO; Formarmid', 'DMF; NMP >> Ethanol', 'DMF; DMSO >> Ethanol; IPA', 'DMF; DMSO >> IPA >> none', 'DMF >> DMF >> IPA', 'IPA >> DMF >> none', 'Butanol; GBL', 'DMF >> none >> IPA', '1-Octane', 'DMF; DMSO; GBL', 'DMSO >> Octane >> Octane', 'DMF; DMSO >> DMSO; IPA', 'GBL; Polyethylene glycol >> H2O', 'DMF; DMSO; Thiourea', 'DMF >> IPA >> DMF', 'DMF; DMI >> Ethanol', 'Acetic acid; Ethanol; GBL', 'none >> none >> none >> none', 'DMF; n-butanol >> IPA', 'DMF; DMSO; GBL >> IPA', 'Dimethylacetamide; NMP', 'n-butylamine', 'Diiodooctane; DMF', 'acetonitrile; DMF; DMSO', 'DMSO; Formamide', 'DMF | IPA | H2O', 'DMF >> IPA >> IPA', 'DMF; DMSO; n-butyl amine >> n-butanol', 'DMF; HPA', 'GBL >> none', 'acetonitrile; Methylamine', 'acetonitrile; DMSO >> IPA', 'DMF; DMI >> IPA', 'Hexame >> Methyl acetate >> Ethyl acetate', 'DMF >> Octane >> Octane >> Methyl acetate >> Methyl acetate', 'none >> none >> IPA', 'DMF; DMSO >> IPA; H2O', 'DMF >> Acetonitrile, Methylamine', 'IPA >> DMF; DMSO', 'acetonitrile; Methylamine >> IPA', 'DMF; TBP', 'Ethanol; GBL', 'H2O >> none >> none', 'DMF >> TBA', 'DMF >> IPA >> Chlorobenzene; GBL', 'DMSO >> IPA >> IPA', 'DMSO | IPA', 'DMF; Tetramethylene sulfoxide', 'DMSO >> DMF; DMSO', 'DMF >> none', 'DMF >> IPA >> Chlorobenzene', 'DMF; DMSO >> DMF; DMSO >> IPA', 'Methanol; Water', 'DMF >> IPA', 'DMF; DMSO >> none >> IPA', 'DMF; Glycerol >> DMF; DMSO', 'DMF >> Methyl acetate', 'DMSO >> Hexane', 'DMSO', 'DMF >> DMF >> none', 'DMF; HI', 'DMF >> Methanol >> Toluene', 'DMF; DMSO >> IPA | IPA', 'DMF >> IPA >> Chlorobenzene; DMSO', 'DMF >> IPA >> Unknown', 'DMF; DMSO >> DMF; DMSO', 'DMF >> Terpineol', 'DMSO | butanol', 'DMF; DMSO >> DMSO; Methanol', 'DMF; DMSO; Hac >> IPA', 'H2O >> Hexane; IPA', 'acetonitrile; MA(MeOH)'])))

    solvents_mixing_ratios = Quantity(
        type=str,
        shape=[],
        description="""
    The mixing ratios of the solvents used in each deposition procedure for each layer in the stack
- When more than one reaction step, separate the solvent mixing ratios associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- The number and order of deposition steps must line up with the previous columns.
- For pure solvents, state the mixing ratio as 1
- For non-solvent processes, state the mixing ratio as 1
- For unknown mixing ratios, state the mixing ratio as ‘nan’
- For solvent mixtures, i.e. A and B, state the mixing ratios by using semicolons, as in (VA; VB)
- The preferred metrics is the volume ratios. If that is not available, mass or mol ratios can be used instead, but it the analysis the mixing ratios will be assumed to be based on volumes.
Example
1
4; 1 >> 1
1 >> 5; 2; 0.3 >> 2; 1
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=[])))

    solvents_supplier = Quantity(
        type=str,
        shape=[],
        description="""
    The suppliers of all the solvents.
- When more than one reaction step, separate the solvent suppliers associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If a solvent is a mixture of different solvents, e.g. A and B, list the associated suppliers and separate them with semicolons, as in (A; B)
- The number and order of reaction steps and solvents must line up with the previous columns.
- For non-liquid processes with no solvents, mark the supplier as ‘none’
- If the supplier for a solvent is unknown, state this as ‘Unknown’
- This category was included after the projects initial phase wherefor the list of reported categories is short. Thus, be prepared to expand the given list of alternatives in the data template.
Example
Sigma Aldrich
Sigma Aldrich; Fisher >> Acros
none >> Sigma Aldrich; Sigma Aldrich >> Unknown
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['J&K Scientific; J&K Scientific >> Unknown', 'ACORS Organic; ACORS Organic', 'Alfa Aesar; Alfa Aesar', 'Sigma Aldrich; Daejung', 'Acros Organics; Sigma Aldrich', 'Sigma Aldrich', 'Unknown >> Alfa Aesar; Sigma Aldrich', "Xi'an Polymer Light Technology >> Xi'an Polymer Light Technology >> Unknown", 'Alfa Aesar', 'ACORS Organic; ACORS Organic; Unknown', 'Unknown', 'Panreac', 'J&K Scientific >> Unknown', 'Millipore Sigma', 'Aladdin >> Sigma Aldrich', 'NanoPac; NanoPac', 'Aldrich', 'Sigma Aldrich; Alfa Aesar', 'Sigma Aldrich; Sigma Aldrich', "Xi'an Polymer Light Technology; Xi'an Polymer Light Technology", 'Wako Pure Chemical Industries >> Wako Pure Chemical Industries', 'Fisher Scientific; Fisher Scientific', 'sigma aldrich; sigma aldrich', 'Sigma Aldrich; Sigma Aldrich >> Unknown', 'Wako >> Wako; Wako', 'Sigma Aldrich >> Sigma Aldrich >> Sigma Aldrich', 'Alfa Aesar; Sigma Aldrich', 'Tokyo Chemical Industry, Japan', 'J&K', 'Wako; Wako', 'Merck >> Merck >> Merck', 'Wako >> Wako', 'Nacalai Tesque', 'Tokyo Chemical Industry >> Sigma Aldrich', 'Alfa Aesar >> Alfa Aesar', 'Kanto Chemical Tokyo', 'J&K; J&K', 'Aladdin; Aladdin', 'Sigma Aldrich; Unknown', 'Sigma; Aladdin', 'Merck >> Merck', 'Tianjin Guangfu Fine Chemical Research Institute; Unknown'])))

    solvents_purity = Quantity(
        type=str,
        shape=[],
        description="""
    The purity of the solvents used.
- When more than one reaction step, separate the solvent purities associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If a solvent is a mixture of different solvents, e.g. A and B, list the associated purities and separate them with semicolons, as in (A; B)
- The number and order of layers, reaction steps, and solvents must line up with the previous columns.
- Use standard nomenclature for purities, e.g. pro analysis, puris, extra dry, etc.
- For non-liquid processes with no solvents, state the purity as ‘none’
- If the purity for a solvent is not known, state this as ‘Unknown’
- This category was included after the projects initial phase wherefor the list of reported categories is short. Thus, be prepared to expand the given list of alternatives in the data template.
Example
Pro analysis
Puris; Puris>> Tecnical
none >> Pro analysis; Pro analysis >> Unknown
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['Pro analysis', '0.99', 'Unknown >> Puris; Puris', 'AR 99% GC', 'Pro analysis; Pro analysis', '99.9%; 99.8%', 'Unknown', 'Reagent Grade >> 99.5% >> 99.8%', '99%; 99%', '0.998', '99.7%; 99%', 'Puris', 'Puris; Puris', '99.8% >> Unkown', '99.99%; 99.5%', 'Puris; Unknown', '99.9%; 99.8% >> Unkown', '99.8%; 99.9%', '99.8', '99.7%; 99%; Unkown', '99%; 99,9%', '99.9%; 99.5%', 'Puris; Puris >> Unknown', '99.8% Anhydrous; 99.5% anhydrous'])))

    reaction_solutions_compounds = Quantity(
        type=str,
        shape=[],
        description="""
    The non-solvent precursor chemicals used in each deposition procedure
- When more than one reaction step, separate the non-solvent chemicals associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If a solution contains several compounds, e.g. A and B, list the associated compounds in alphabetic order and separate them with semicolons, as in (A; B)
- Note that also dopants/additives should be included
- When several precursor solutions are made and mixed before the reaction step, it is the properties of the final mixture used in the reaction we here describe.
- The number and order of reaction steps must line up with the previous columns.
- For gas phase reactions, state the reaction gases as if they were in solution.
- For solid-state reactions, state the compounds as if they were in solution.
- For reaction steps involving only pure solvents, state this as ‘none’
- If the compounds for a deposition step is not known, state this as ‘Unknown’
- This category was included after the projects initial phase wherefor the list of reported categories is short. Thus, be prepared to expand the given list of alternatives in the data template.
Example
CsI; FAI; MAI; PbBr2; PbI2
PbI2 >> MAI
PbBr2; PbI2 >> FAI; MAI >> none
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', 'nan >> PEAI', 'FAPbI3; MABr >> PEAI; PbI2', 'CsI; FAI; MABr; PbBr2; PbI2 >> Cs-oleate; PbBr2; PbBI2', 'PEAI; PbI2; MABr >> PEAI; PbI2; MABr', 'CsBr; FAI; PbI2 >> PEAI', 'CsI; MABr; PbBr2; FAI; PbI2', 'PbBr2, MgBr2 >> CsBr', 'MAI; PbI2; TPAI', 'MAI; PbI2 >> MAI', 'SnI2; FASnI', 'SnI2; FAI; SnF2; ethylenediamine; PbI2; MAI; MABr', 'SnI2; FAI; SnF2; ethylenediamine; PbI2; MAI', 'nan >> n-butyl amine', '1,8-octanedithiol; CsI; FAI; PbI2', 'MAI; PbI2; NiI2', 'F5PEAI, PEAI; PbI2', 'SnI2; FAI', 'MAI; PbI2; SnI2', 'MAI; BA; PbI2', 'PbCl2; PbI2 >> MAI', 'SnI2; FAI; SnF2; PbI2; MAI', 'MAI; PbSCN2; PbI2; FAI', 'CsI; CsBr; PbI2; PbBr2', 'PbCl2; PbI2 >> MAI; PMMA', 'CsBr; PbI2 >> CsPbI3-QDs >> Pb(OAc)2 >> nan >> CsPbI3-QDs >> Pb(OAc)2 >> nan >> CsPbI3-QDs >> Pb(OAc)2 >> nan', 'MAI; PbI2; FeI2', 'PbI2; PbBr2; FAI; MABr; g-C3N4', 'CsI; PbBr2 >> CsI', 'CsI; FAI; MABr; PbBr2; PbI2', 'nan >> Guanidinium iodide', 'nan >> Cs2CO3', 'CsI; FAI; PbI2; PbBr2', 'FAI; MAI; PbBr2; PbI2', 'PbI2 >> MAI; MAPbI3-QDs', 'PbI2; FAI; MACl; MABr; PbBr2', 'FAI; MABr; MACl; PbI2; PbBr2', 'CsAc; HPbBr3; PEABr', 'nan >> nan >> nan', 'PbI2 >> MAI >> nan', 'MACl; MAI; PbI2', 'NH4I; PbI2 >> MA', 'MAI; PbI2 >> MAI >> 4-DA', 'CsBr; PbBr2', 'MAI; PbCl2; PbI2', 'FAI; MABr; PbI2; PbBr2 >> CsI', 'MACl; SnCl2', 'MAI; PbI2; CoI2', 'MAI; PbI2 >> nan', 'nan >> CsNO3', 'PbI2; PbBr2; CsI', 'MAI; BDAI; PbI2', 'CsI; PbI2', 'MAI; MnI2', 'nan >> FAI', 'FAI; MABr; PbBr2; PbI2', 'CsAc; HPbBr3', 'PEAI, PbI2', 'MAI; PbCl2 >> IPFB', 'CsI; FAI; MABr; PbBr2; PbI2; RbI >> FABr', 'FAI; PbI2; ThMAI', 'PbI2 >> MAI', 'CsBr; FAI; PbI2', 'PbI2 >> MACl; MAI', 'nan >> MABr', 'CsBr >> PbBr | PQD', 'nan >> GuBr', 'HPbI3; CsI', 'PbI2; PbBr2; FAI; MABr; C3N5', 'nan >> nan >> nan >> Pb(NO3)2', 'PbI2 >> MAI; MACl', 'MAI; MTEACl; PbI2', 'CsI; SnI2', '1,8-diiodooctane; MAI; PbCl2', 'MAI; PbI2; PEAI', 'nan >> ETB; NaI', 'nan >> NH3I(CH2)4NH3I', 'AgI; Bi3', 'CsAc; HPbI3', 'MAI; PbI2', 'MAI; PBI2; SbBr3', 'nan >> FaBr', 'PbBr2, SrBr2 >> CsBr', 'F5PEAI; CsI; FAI; MABr; PbI2; PbBr2; Pb(SCN)2; PEAI', 'CsI; CsBr; PbI2', 'MAI; PbI2 >> PbI2', 'F5PEAI; CsI; FAI; MABr; PbI2; PbBr2; Pb(SCN)2', 'nan >> NH3I(CH2)8NH3I', 'PbI2 >> FAI; MACl', 'F5PEAI, PbI2', 'MAI; PbCl2; Pb(OAc)2.3H2O', 'PbI2 >> 5-AVAI; MAI', 'CsBr; FAI; PbI2 >> PMAI', 'PbCl2 >> MAI', 'MABr; PbBr2', 'CsI; PbBr2; PbI2; FAI >> FAI', 'CsI; FAI; HI; PbI2 >> FA(PF6)', 'CsI; FAI; MABr; PbI2; PbBr2', 'CsBr; CsI; PbI2', 'SnI2; FABr', 'nan >> Eu-pyP', 'PbCl2; PbI2 >> FAI; MAI', 'nan >> CsI', 'PbBr2, CaBr2 >> CsBr', 'MAI; PbCl2; PbI2; Phenol', 'MAI; PbCl2; PbI2; FAI', 'MAI; PbI2 >> MAI; PbI2', 'Cs2CO3; oleic acid; 1-octadecene; PbBr2; oleylamine', 'CsI; PbI2 >> FAI; MABr', 'MAI; PbCl2', 'nan >> Octylammonium iodide', 'MAI; NMA; PbI2', 'C3H5CsO2; HPbBr3; HPbI3', 'CsBr; PbI2 >> CsPbI3-QDs >> Pb(OAc)2 >> nan >> CsPbI3-QDs >> Pb(OAc)2 >> nan >> CsPbI3-QDs >> Pb(OAc)2 >> nan >> nan', 'CsBr; FAI; PbI2 >> PAI', 'nan >> Pb(NO3)2', 'nan >> Ethylammonium Iodide', 'nan >> GAI', 'CsI; FAI; MAI; PbBr2; PbI2', 'MAI; PbI2 >> MAPbI3-QDs', 'CsAc; HPbBr3; HPbI3; PEABr; PEAI', 'nan >> CsAc', 'MAI; PbAc', 'CsI; PbBr2; PbI2; FAI >> FABr', 'MAI; PbCl2; PbI2 >> MAPbI3-QDs', 'nan >> NH3I(CH2)2O(CH2)2O(CH2)2NH3I', 'PbI2 >> FAI; MABr; MACl', 'AuBr3; MABr', 'nan >> MAI', 'MAI; PbI2; MnI2', 'nan >> CsBr', 'CsI; FAI; PbBr2; PbI2', 'CsI; FAI; MABr; MACl; PbI2; PbBr2', 'Pb(NO3)2 >> MACl; MAI', 'PbI2 >> FAI; MAI; MACl', 'CsI; FAI; MABr; PbBr2; PbI2 >> PFPAI', 'CsBr; PbI2', 'FAI; MAI; PbI2', '5-AVAI; MAI; PbI2', 'MAI; PBI2', 'PbI2 >> 5-AVAI; MAI; MACl', 'MAI; 5-AVAI; PbI2', 'PbCl2 >> MAI >> nan', 'AgBr; BiBr3; CsBr', 'MABr; PbBr2; PbI2; FAI', 'CsI; FAI; GaAA3; PbI2', 'CsAc; HPbI3; PEAI', 'CsI; FAI; MAI; PbBr2; PbI2 >> 10%mol TBAI-doped PTzDPPBTz', 'CsPbI3-QDs >> Pb(OAc)2 >> nan >> CsPbI3-QDs >> Pb(OAc)2 >> nan >> CsPbI3-QDs >> Pb(OAc)2 >> nan', 'MAI; PbI2; PbCl2', 'CsAc; HPbBr3; HPbI3', 'PbI2 >> nan >> MAI', 'HPbI3 >> MA', 'C2H3CsO2; HPbBr3; HPbI3', 'CsBr >> PbBr', 'CsI; PbBr2; PbI2', '(BDA)I2; CsI; PbI2; PbBr2', 'CsI; FAI; MABr; PbI2', 'MAI; Pb(OAc)2', 'FAI; MAI; PbI2; Pb(SCN)2', 'HCOOCs; HPbBr3; HPbI3', 'FAI; SnI2', 'MAI; Pb (OAc)2.3H2O', 'PbI2; HI; MA; ethanol; diethyl ether', 'Pb(NO3)2 >> MAI', 'CsI; PbBr2', 'PbI2; FAI; MACl', 'FAI; MAI; PbI2; Pb(SCN)2 >> PMMA', 'KI; FAI; MABr; PbBr2; PbI2', 'SnI2; MASnI', 'PbI2; HI; MA; diethyl ether', 'FAPbI2Br >> MAPbI2Br >> CsPbI2Br >> RbI | BABr', 'CsI; FAI; MAI; PbBr2; PbI2 >> PTABr', 'FAI; PbI2', 'CsI; PbBr2; PbI2; FAI >> FAI; FABr', 'CsBr; HI; PbF2; PbI2', 'nan >> Imidazolium iodide', 'nan >> GABr', 'nan >> MACl', 'PbI2; MAI', 'CsI; FAI; HI; PbI2', 'PbBr2; MAI', 'PbBr2 >> CsBr', 'FAI; MAI; PbBr2; PbI2; Pb(SCN)2 >> PMMA', 'CsI; PbI2 >> FAI; MABr; MACl', 'PbCl2; MAI', 'CsI; FAI; MAI; PbI2', 'nan >> FABr', 'DOI; MABr; PbBr2', 'MAI: PbI2', 'MAI; PbI2 >> BEAI2', 'nan >> nan >> FAI', 'CsBr; HI; PbI2', 'MAPbI3-xClx', 'CsI; FAI; MABr; PbI2; PbBr2; Pb(SCN)2; PEAI; nan', 'CsPbI3 >> Pb(NO3)2 >> FAI', 'CsI; FAI; MAI; PbI2; RbI', 'CsI; FAI; PbI2', 'MAI; BAI; PbI2', 'nan >> EDBE', 'DOI; MAI; PbCl2', 'DMAI; PbI2', 'RbI; CsI; FAI; MABr; PbI2; PbBr2', 'FAI, MABr; PbI2; PbBr2', 'FAI; MACl; MABr; PbI2', 'PbI2; PbCl2; MAI', 'MAI; SnF2; SnI2 >> nan', 'nan >> Pb(NO3)2 >> nan', 'CsI; PbI2 >> MACl; MABr; FAI; MAI', 'PbI2 >> MAI >> TSA', 'nan >> ITIC'])))

    reaction_solutions_compounds_supplier = Quantity(
        type=str,
        shape=[],
        description="""
    The suppliers of the non-solvent chemicals.
- When more than one reaction step, separate the non-solvent chemical suppliers associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If a solution contains several dissolved compounds, e.g. A and B, list the associated suppliers and separate them with semicolons, as in (A; B)
- The number and order of reaction steps and solvents must line up with the previous columns.
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
            component='EnumEditQuantity', props=dict(suggestions=['Aldrich; Aldrich; Junsei Chemical; Unknown; Unknown', 'Lab made; synthesiyed; Aladdin; Sigma Aldrich', 'Xian Polymer Light Technology; Alfa Aesar', 'Dyesol; Sigma; Alfa Aesar; Dyesol', 'Lab made; Unknown >> Lab made; Unknown', 'Showa Chemical; Sigma Aldrich', 'Sigma Aldrich; Dyesol; Sigma Aldrich; Sigma Aldrich; Sigma Aldrich; Dyesol; Sigma Aldrich', 'Sigma Aldrich >> Unknown >> Lab made', 'Lab-made; Sigma Aldrich', 'GreatCell Solar; Sigma-Aldrich', 'Greatcell Ltd.; Xi’An Polymer Light Technology Corp.; TCI', 'Youxuan Tech; Youxuan Tech', 'Wako; Tokyo Chemical Industry', 'Dyesol; Sigma; Sigma', 'Sigma Aldrich; Showa Chemical', 'Dyesol; Sigma Aldrich', 'TCI; GreatCell Solar Materials; Dyenamo; GreatCell Solar Materials; TCI', "Xi'an Polymer Light Technology; Alfa Aesar", 'Sigma Aldrich; Alfa-Aesar', 'Sigma Aldrich; Sigma Aldrich; TCI', 'Acros Organics; Acros Organics; Sigma Aldrich; Dyesol', 'Sigma Aldrich; Sigma Aldrich; Sigma Aldrich; Unknown; Unknown', 'Unknown >> Lab-made; Lab-made', 'Dyesol; Sigma; Dyesol; Dyesol', 'Dynamo; Sigma Aldrich', 'Sigma Aldrich; Dyesole; Dyesole; TCI; TCI', 'Alfa Aesar; Lab made', 'Sigma Aldrich >> Sigma Aldrich', 'Xi’an p-OLED >> Lab made', 'Unknown >> Lab made; Unknown', 'Sigma Aldrich; Sigma Aldrich >> Dyesol; Dyesol', 'Synthesiyed; Sigma Aldrich; Sigma Aldrich', 'TCI; Kanto Chemical Tokyo', 'Shanghai Mater. Win. New Materials Corporation; Sigma Aldrich; Sigma Aldrich; Shanghai Mater. Win. New Materials Corporation', 'Sigma Aldrich; Greatcell Solar', 'Sigma Aldrich >> Lab made', 'ACROS Organic; STAREK scientific Co. Ltd.', 'Dyesol; Dyesol; Alfa Aesar', 'Advanced Election Technology Co.. Ltd; GreatCell Solar; Advanced Election Technology Co.. Ltd. TCI.', 'Dyesol; Dyesol; TCI; Alfa Aesar; Sigma Aldrich >> Sigma Aldrich', 'Lab-made; Sigma Aldrich; Sigma Aldrich', 'GreatCell Solar; Sigma Aldrich', 'Sigma Aldrich >> Unknown; Unknown', 'Sigma Aldrich; Lab made; Lab made; Sigma Aldrich; Sigma Aldrich', 'Vizuchem; Vizuchem', 'Sigma Aldrich; Lab made; Sigma Aldrich; Sigma Aldrich >> Greatcell Solar', 'Alfa Aesar; Lumtec; Sigma Aldrich; Luminiscence; Sigma Aldrich', 'Lab made; Sigma Aldrich', 'Dyesol; Dyesol; TCI; Sigma Aldrichch', "Xi'an Polymer Light Technology Corporation.", 'Unknown; Unknown; Unknown', 'Shanghai MaterWin New Materials Co.. Ltd; Sigma Aldrich', 'Alfa Aesar; Greatcell Solar', 'Sigma Aldrich. 1-Material', 'Showa Chemical; Sigma Aldrich; Sigma Aldrich', 'Dynamo; Tokyo Chemical Industry', 'Sigma Aldrich; Daejung', 'Sigma Aldrich; Lab made; Sigma Aldrich; Sigma Aldrich', 'Alfa Aesar; Xi’an Polymer Light Technology; Xi’an Polymer Light Technology', 'Unknown', 'YOUXUAN Technology Co. Ltd.; Sigma Aldrich Co. Ltd.', 'Sigma Aldrich; Lab made; Sigma Aldrich', 'Dynamo; TCI', 'Alfa Aesar; Dyesol', 'Aladdin; Lab made; synthesiyed; Aladdin; Sigma Aldrich', 'Dyesol; Dyesol; TCI', 'Sigma Aldrich; Sigma Aldrich', "Acros Organics; Xi'an Polymer Light Tech. Corp.", 'Lab made; Alfa Aesar', 'Xi’an Polymer Light Technology Corp; Alfa Aesar', 'Alfa Aesar; Alfa Aesar; Alfa Aesar; Alfa Aesar; Alfa Aesar', 'Ossila', 'Sigma Aldrich; Macklin', 'Sigma Aldrich; Dyesol; Sigma Aldrich; Sigma Aldrich; Dyesol', 'Unknown >> PEAI', 'Acros Organics; Acros Organics; Sigma Aldrich; Dyesol; Unknown', 'Unknown >> Lab made', 'Alfa Aesar; Alfa Aesar', 'TCI; Sigma Aldrichch', 'Xian Polymer Light Technology; Xian Polymer Light Technology', 'Dysol; Unknown; Unknown', 'Xi’an p-OLED; Xi’an p-OLED', 'Sigma Aldrich; Dyesol; Sigma Aldrich; Sigma Aldrich; Sigma Aldrich; Dyesol', 'Lab made; Lab made; Sigma Aldrich', 'Dyesol; Alfa Aesar', 'PbI2; MAI', "Xi'an Polymer Light Technology; Xi'an Polymer Light Technology", 'Tokio Chemical Industry; Sigma Aldrich', 'Dyesol; Dyesol; TCI; Sigma Aldrich >> Sigma Aldrich', 'Sigma Aldrich >> Dyesol', 'TCI; TCI', 'Alfa Aesar; Sigma Aldrich', 'Sigma Aldrich; Lab made', "Xi'an Polymer Light Technology Corp.; Xi'an Polymer Light Technology Corp.; Sigma Aldrich; Sigma Aldrich", 'Alfa Aesar; Xian Polymer Light Technology', 'GreatCell Solar; GreatCell Solar; Sigma Aldrich; Sigma Aldrich'])))

    reaction_solutions_compounds_purity = Quantity(
        type=str,
        shape=[],
        description="""
    The purity of the chemicals used.
- When more than one reaction step, separate the compound purities associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If a solution contains several dissolved compounds, i.e. A and B, list the associated purities and separate them with semicolons, as in (A; B)
- The number and order of reaction steps and solvents must line up with the previous columns.
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
            component='EnumEditQuantity', props=dict(suggestions=['99,985 >> Unknown', 'Puris; Pro analysis; Puris; Unknown', 'Unknown; 99,9%', '99.5; 99', 'Unknown; Unknown; Puris; Puris', '99,9%; Unknown; Unknown; 99,9%; 99,999%', 'Unknown; 98%', '99.9%; 99.9%', 'Unknown; 99%', 'Puris; technical; technical; Unknown; Unknown', 'Unknown >> Unknown; Unknown', '99.999% >> Unknown', '99.999%; 99.999%', '99.99%; Unknown; 99.9985%', 'Unknown; Unknown; 99,9%; 99,999%', 'Unknown; 99,999%', 'Unknown', '99.99%; Unknown; 99.99%; 99.9985%; Unknown', 'Unknown; 99.9985%', '98%; Unknown', '99.99%; Unknown; 99.99%; 99.9985%', '99.5; 99.99', 'Puris; Pro analysis; Puris; Unknown; Unknown', 'Puris; Puris; Puris', 'Unknown >> 99,999% >> Unknown', '99%; Unknown >> Unkown', 'Puris; Puris; Unknown; Puris; Unknown', 'Unknown; Unknown', 'Puris; Puris', 'Puris; Unknown', 'Unknown; Puris; Puris; Unkown', 'Unknown >> MACl', 'Puris; technical; technical; puris; technical', 'Unknown; Puris', '99 %; 99.5%', 'Unknown; Unknown; 99,9%', 'Unknown; Unknown; Unknown', 'Puris >> Puris', 'Puris; Unknown; Unknown; Unknown; Unknown', 'Unknown; 99.999%', '99,5%; 99,99%', 'Unknown >> ODAI', 'Puris; Puris; Unknown; Puris; Puris; Unknown', 'Unknown >> CsAc', '99,999%; 99,999% >> 99,8%; 99,8%', '99,999% >> Unknown; Unknown', 'Puris; Puris; Unknown; Puris; Puris; Unknown; Puris', 'Unknown; 99%; 99,99%', '99% >> Unknown', '95%; 99.9%'])))

    reaction_solutions_concentrations = Quantity(
        type=str,
        shape=[],
        description="""
    The concentration of the non-solvent precursor chemicals.
- When more than one reaction step, separate the concentrations associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- The number and order of deposition steps and chemicals must line up with the previous columns.
- If a solution contains several dissolved compounds, e.g. A and B, list the associated concentrations and separate them with semicolons, as in (A; B)
- The order of the chemicals must line up to the chemicals in the previous column.
- The order of the compounds must be the same as in the previous filed.
- For reaction steps involving only pure solvents, state this as ‘none’
- For gas phase reactions, state the concentration as ‘none’
- For solid-state reactions, state the concentration as ‘none’
- When concentrations are unknown, state that as ‘nan’
- Concentrations can be stated in different units suited for different situations. Therefore, specify the unit used. When possible, use one of the preferred units
o M, mM, molal; g/ml, mg/ml, µg/ml, wt%, mol%, vol%, ppt, ppm, ppb
- For values with uncertainties, state the best estimate, e.g write 4 wt% and not 3-5 wt%.
Example
0.063 M; 1.25 M; 1.25 M; 1.14 M; 1.14 M
1.25 M; 1.25 M >> 1.14 M; 1.14 M; 10 mg/ml
1 M; 1 M >> none
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', '1 M >> 40 mg/ml', '0.4 M; 0.6 M; 0.8 M', '0.18 M; 1.02 M; 1.2 M', '0.75; 0.788; 0.713', '600 mg/ml >> 1 mg/ml', '1 M >> 0.07 M | nan', '50 wt%', '0.024 M; 1.176 M >> 8 mg/ml', '461 mg/ml; 57 wt%; 33 wt%; nan; nan', '0.063 M; 1.14 M; 1.14 M; 1.25 M; 1.25 M', '0.2 M; 0.06', '1 vol%; 0.05 M; 0.95 M; 1 M', '46.8 mg/ml; 226.9 mg/ml; 0.05 vol%; 608.5 mg/ml >> 1 mg/ml', '0.5 M; 0.5 M', '1 M; 30 mg/ml', '0.442 molal; 1.07 molal; 0.173 molal; 1.36 molal; 13.6 mg/ml >> 1 mg/ml', '1.125 M; 0.75 M', '548.6 mg/ml >> 50 mg/ml', '462 mg/ml >> 35 mg/ml', 'nan; 1 M; 0.2 M; 0.2 M; 1.1 M >> 1000 mM', '1.26 M; 0.14 M; 1.4 M', 'nan; 1 M; 0.2 M; 0.2 M; 1.1 M >> 200 mM', '600 mg/ml >> 10 mg/ml', '1 M >> 0.0031 M; 0.0598 M', '1 M; 1.05 M', '0.5 M >> 20 mg/ml', '573.3 mg/ml; 197.7 mg/ml', '0.1426 M; 1.56 M; 1.74 M >> 4 mM', '1 M >> 10 mg/ml >> 5 mM', '2 wt%; 163.33 mg/ml; 535.2 mg/ml', '0.75; 0.75; 0.75', '0.1426 M; 1.56 M; 1.74 M >> 10 mM', '1 M >> 7 mg/ml', '0.75 M; 0.50 M; 1 M', '1 M >> 8 mg/ml', '0.5 M >> 38 mg/ml', '553 mg/ml; 190 mg/ml', '0.5 M; 0.5 M; 0.6 M; 0.3 M', '1 M >> 10 mg/ml >> 10 mM', '1 M; 1.06 M', 'nan >> 2 mg/ml', '1.25 M; 1.25 M >> nan', '1.5 M; nan', '462 mg/ml >> nan >> 10 mg/ml', '1.4 M; 1.4 M', '1.08 M; 1.08 M; 0.12 M', '1.2 M >> 1.6 mol%', 'nan >> 5 mg/ml', '500 mg/ml >> 10 mg/ml >> nan', '1 M >> 0.07 M', 'nan >> 3 mg/ml', '46.8 mg/ml; 226.9 mg/ml; 0.05 vol%; 608.5 mg/ml >> 7 mg/ml', '0.3 M; 0.06', '1.5 M >> 62.3 M', '3 vol%; 0.05 M; 0.95 M; 1 M', '1 M; 0.2 M; 1 M; 1.1 M', '1.3 M; 1.3 M; 1.3 M; 1.3 M | 1 mg/ml', '1.5 M; 1.5 M', '1.5 M >> 23.5 mM; 70.8 mM', '0.1426 M; 1.56 M; 1.74 M >> 2 mM', '1.35 M; 1.35 M', '1.25 M; 1.3 M', '440 mg/ml; 180 mg/ml', '1.1 M; 0.2 M; 1.15 M; 0.2 M', '50 mg/ml >> nan >> nan >> 50 mg/ml >> nan >> nan >> 50 mg/ml >> nan >> nan', '1.2 M', '400 mg/ml >> 10 mg/ml', '1.0 M; 1.1 M', '462 mg/ml >> 10 mg/ml >> nan', '52.6 mg/ml; 197.4 mg/ml; 622.4 mg/ml', '1 M >> 10 mg/ml >> 2.5 mM', '0.85 M; 0.15 M; 0.15 M; 0.85 M', '0.8 M; 0.3 vol%; 0.12 M; 0.68 M', '0.05 M; 1.1 M; 0.2 M; 0.2 M; 1.25 M', '0.5 M; 0.5 M >> 20 mg/ml', '0.90 M; 0.90 M; 0.10 M', '1.3 M; 0.14 M; 1.26 M; 50 mg/ml', 'nan; 1 M; 0.2 M; 0.2 M; 1.1 M', '0.5 M; 1 M; 1 M', '1.4 M >> 10 mg/ml; nan', '1.8 M; 1.8 M >> nan', '1 M; 0.07 M', '2; 1', '450 mg/ml >> 5 mg/ml; 50 mg/ml', '1 M >> nan', '1 :3molarratio', '2 wt%; 2.43 M; 0.81 M', '0.8 M; 0.3 vol%; 0.28 M; 0.52 M', '0.11 M; 0.91 M; 0.18 M; 0.186 M; 1.014 M', '2.44 M; 2.44 M; 0.9 M', '1.3 M; 1.3 M', '1 M; 57 wt%; 33 wt%; nan; nan', '13.7 mg/ml; 197.5 mg/ml; 573 mg/ml', '0.98 M; 1 M', '70 mg/ml', '1.02 M; 0.18 M; 0.18 M; 1.02 M', '1 mM; 1 mM >> 30 mg/ml', 'nan; 10 mg/ml', '1 M >> 50 mg/ml', '0.95 M; 0.05 M; 0.05 M; 0.95 M', '461 mg/ml; 159 mg/ml', '691.5 mg/ml >> nan; nan', '0.5 M >> 36 mg/ml', '0.4 M; 0.8 M; 0.8 M', '1 M; 50 mM', '0.75 M; 0.75 M', '367 mg/ml', '1.125; 0.75; 0.75', '0.2 M; 0.22 M; 1.1 M; 1 M', '0.5 M >> 50 mg/ml', '45 wt%', '636.4 mg/ml; 90 mg/ml; 89.79 wt%; 8.97 wt%', '33.8 mg/ml; 599 mg/ml >> 60 mg/ml; 6 mg/ml; 6 mg/ml', '1.2 M; 0.28 M', '0.18 M; 1.02 M; 1.2 M; 0.1 M', '1.2 mM', '0.5 M >> 34 mg/ml', '1 M; 0.2 M; 1.1 M; 0.2 M', '66 mg/ml; 187 mg/ml; 12 mg/ml; 80 mg/ml; 568 mg/ml; nan', '0.3 M; 1.2 M >> 40 mg/ml', '0.5 M >> 32 mg/ml', '1.5; 0.75; 0.75', '1.3 M; 0.14 M; 1.26 M', '2.7 M; 0.9 M', '0 M; 0.8 M; 0.8 M', '0.5 M >> 30 mg/ml', '227.14 mg/ml; 80 mg/ml; 527.14 mg/ml', '510 mg/ml >> 8.5 mg/ml >> nan', '0.15 M; 0.85 M; 1 M', '1 M; 1 M; 1 M', 'nan >> 0.5 mg/ml', '0.5 M; 0.5 M; 1 M; 0.2 M', '1.8 M; 0.45 M; 0.45 M', '1 M >> 10 mg/ml', '2.4 M; 0.8 M', '0.6 M; 0.6 M >> 50 mg/ml >> nan >> nan >> 50 mg/ml >> nan >> nan >> 50 mg/ml >> nan >> nan', '1 mol/L; 1 mol/L', '0.7 M; 0.7 M', '50.87 mg/ml; 147.5 mg/ml', '1.42 M; 1.42 M', '0.18 M; 1.32 M; 1.5 M', '0.4 M', '1.25 M; 1 M', '0.05 M; 1.0 M; 0.2 M; 0.2 M; 1.1 M', '450 mg/ml >> 50 mg/ml', '1 M >> 0.0031 M; 0.0126 M; 0.0472 M', '0.06 M; 0.96 M; 0.18 M; 0.186 M; 1.014 M', '1.02 M; 0.18 M; 0.186 M; 1.014 M', '0.375; 0.75; 0.75', '0.5 M >> 40 mg/ml', '159 mg/ml; 461 mg/ml >> 461 mg/ml', '1.467; 1.6', '0.6 M; 0.6 M', '0.05 M; 1 M; 0.2 M; 0.2 M; 1.1 M', '1.59 mol/kg; 1.59 mol/kg', '0.11 M; 1.07 M; 0.19 M; 0.19 M; 1.23 M', '197.6 mg/ml; 787 mg/ml', '0.15 M; 0.75 M; 0.1 M; 1 M', '1.467; 1.6; 2 mol%', '206.2 mg/ml; 597.8 mg/ml', '1.5 M; 0.75 M', '1.53 M; 1.4 M; 0.5 M; 0.0122 M; 0.0122 M', '5 wt%; 1.4 M >> 60 mg/ml; 6 mg/ml', '2.25 M; 0.75 M', 'nan >> 0.16 ml/ml; 9.04 mg/ml; 23.04 mg/ml', '0.8 M; 0.3 vol%; 0.2 M; 0.6 M', '1 M; 1 M', '1.6 M', '9 wt%; 26 wt%', '1.2 M; 1.2 M', '397 mg/ml >> 9 mg/ml', '1.6 mol%; 1.2 M; 1.2 M >> 1.6 mol%; 1.2 M; 1.2 M', '1 wt%; 2.43 M; 0.81 M', '75 mg/ml >> 1 mg/ml >> 1 mg/ml', '0.9 M; 0.3 M; 1.0 M; 0.3 M', '0.14 M; 1.4 M >> 70 mg/ml', '1.3 M; 0.14 M; 1.26 M; 75 mg/ml', '0.5 M; 0.5 M >> 20 mg/ml; 0.005 mg/ml', '6.4 wt%; 33.6 wt%', '1.05 M; nan', '0.9 M; 0.9 M', '636.4 mg/ml; 90 mg/ml; 89.79 wt%; 8.97 wt%; 4 wt%', '1 M; 0.2 M; 0.22 M; 1.1 M', '1.1 M; 10 mg/ml', '1.4 M; 1.45 M', '0.17 M; 0.83 M; 0.5 M; 0.5 M', '0.172 mg/ml; 0.022 mg/ml; 0.507 mg/ml; 0.08 mg/ml >> 1.5 M', '0.072 M; 1.11 M; 0.21 M; 0.21 M; 1.2 M', '0.5 M; 1.2 M; 1 M; 0.2 M', '330 mg/ml >> 10 mg/ml', '1.4 M', '1.3 M; 1 M', '0.05 M; 0.95 M; 1 M', '3 M; 1 M', '450 mg/ml >> 50 mg/ml; 10 mg/ml', '2.1 M; 0.7 M', '596 mg/ml; 200 mg/ml', 'nan >> nan', '159 mg/ml; 461 mg/ml', '0.4 M; 0.4 M; 0.8 M', '1.3 M; 1.35 M', '0.6 M; 0.6 M >> 50 mg/ml >> nan >> nan >> 50 mg/ml >> nan >> nan >> 50 mg/ml >> nan >> nan >> nan', '0.2 M; 0.8 M >> 15 mg/ml', '2.55 M; 0.85 M', '1.3 M; 0.14 M; 1.26 M; 5 mg/ml', '26 mg/ml; 172 mg/ml; 22.4 mg/ml; 16.7 mg/m; 507 mg/ml; 73.4 mg/ml', '0.1426 M; 1.56 M; 1.74 M >> 6 mM', '0.88 M; 1.1 M; 0.44 M', '460 mg/ml >> 10 mg/ml', '199 mg/ml; 605.5 mg/ml', '1 M; 10 mg/ml', '20 mg/ml; 172 mg/ml; 22.4 mg/ml; 507.2 mg/ml; 73.4 mg/ml', '1.1 M; 1.1 M', '0.1125 M; 1.1375 M; 1.25 M', '46.8 mg/ml; 226.9 mg/ml; 0.05 vol%; 608.5 mg/ml >> 28 mg/ml', '1 M; 0.5 M; 0.5 M', '163.33 mg/ml; 535.2 mg/ml', '190 mg/ml; 0.0176 mg/ml; 530 mg/ml', '1.4 M >> 10 mg/ml', '0.54 M; 0.54 M; 0.06 M', '0.2 M; 0.2 M; 1.1 M; 1 M', '470 mg/ml >> 50 mg/ml; 5 mg/ml', '0.196 mg/mLPbI2; 1.5 M', '28 wt%', '20 mg/ml; 1.6 M; 1.6 M; 20 mg/ml', '1.0 M', '0.5 M; 0.75 M; 1 M', '1.4 M; 0.1 M; 0.01 M; 1.4 M; 0.1 M', '40 wt%', '0.214 mg/mLPbI2; 1.5 M', '1 wt%; 163.33 mg/ml; 535.2 mg/ml', '1.875 M; 0.75 M', '1.3 M | 1.3 M', '4 M; 1 M', '5 vol%; 0.05 M; 0.95 M; 1 M', '1.3 M >> 60 mg/ml; 6 mg/ml; 6 mg/ml', '1.2 M; 1.2 M >> nan', '238.5 mg/ml; 726 mg/ml', '1.8 M >> nan', '0.5 M; 0.5 M; 0.4 M', '0.21 M; 0.81 M; 0.18 M; 0.186 M; 1.014 M', '687 mg/ml; 237 mg/ml', 'nan; nan', '1.2 M >> 8 mg/ml', '691.5 mg/ml >> 70 mg/ml', 'nan >> 7 mg/ml', '1.25 M; 1.25 M', '60 mg/ml >> 1.3 M', '0.348 mg/ml; 0.922 mg/ml', '0.075 M; 1 M; 0.2 M; 1 M; 1.1 M', '254.4 mg/ml; 737.6 mg/ml', '1 :1mol%', '0.1 M; 0.06', '20 wt%', '1.24 M', '1; 0.2; 1; 1.1', '0.1426 M; 1.56 M; 1.74 M', '0.8 M; 0.3 vol%; 0.18 M; 0.62 M', '1 M >> 0.0126 M; 0.0503 M', '1.4 M >> 70 mg/ml', '0.9 M; 0.1 M; 0.1 M; 0.9 M', '1.35 M; 0.14 M; 1.26 M', '0.70 M; 0.17 M; 0.10 M; 1.30 M', '0.18 M; 1.02 M; 1.5 mg/ml; 1.2 M', '1 M; 0.33 M; 0.66 M', '1 M; 1 M >> nan', '46.8 mg/ml; 226.9 mg/ml; 0.05 vol%; 608.5 mg/ml', '21.25 wt%; 21.25 wt%', '3.75 M; 1.25 M', '100 mg/ml; 300 mg/ml', '0.375 M; 0.75 M', '19.4 mg/ml; 172 mg/ml; 22.4 mg/ml; 73.4 mg/ml; 507 mg/ml; nan', '2.2 M; 2 M', '112 mg/ml; 38 mg/ml', 'nan; 1 M; 0.2 M; 0.2 M; 1.1 M >> 100 mM', '0.063 M; 1.25 M; 1.25 M; 1.14 M; 1.14 M', '1.2 M; 0.3 M; 0.3 M', '400 mg/ml >> nan', '7 mg/ml; 1.2 M; 0.2 M', '1.3 M; 0.14 M; 1.26 M; 20 mg/ml', '0.12 M; 1.08 M >> 8 mg/ml', 'nan; 1 M; 0.2 M; 0.2 M; 1.1 M >> 50 mM', '0.24 M; 1.36 M >> 30 mg/ml; 70 mg/ml', '1.467; 1.6; 4 mol%', '0.06 M; 1.14 M >> 8 mg/ml', '1.2 M; 8 mg/ml', '190.8 mg/ml; 553 mg/ml', '197.6 mg/ml; 787 mg/ml; 19.1 mg/ml', '46.8 mg/ml; 226.9 mg/ml; 0.05 vol%; 608.5 mg/ml >> 14 mg/ml', '0.3 M; 0.3 M', '32 wt%', '16.89 mg/ml; 600 mg/ml >> 1 mg/ml; 10.75 mg/ml', '198 mg/ml; 577 mg/ml', '0.3 M; 0.3 M; 0.6 M', '1.10 M; 0.20 M; 0.20 M; 1.15 M', '0.8 M; 0.2 M; 0.2 M; 0.8 M', '1.8 M; 0.45 M; 0.45 M >> nan', '0.72 M; 0.72 M; 0.08 M', '0.06 M; 0.95 M; 0.19 M; 0.2 M; 1 M', '4.07 mg/ml; 9.66 vol%; 48.85 vol%; 6.9 mg/ml; 10 vol%', '0.07 M; 1.4 M >> 70 mg/ml', '1 vol%; 1.1 M; 1.1 M', '0.22 M; 0.66 M', 'nan; 1 M; 0.2 M; 0.22 M; 1.1 M', '462 mg/ml >> 20 mg/ml', '1.2 M >> 45 mg/ml', 'nan; 1 M; 0.2 M; 0.2 M; 1.1 M >> 500 mM', '460 mg/ml >> 0.15 M', '1.38 M; 1.38 M', '0.8 M; 0.3 vol%; 0.8 M', '460 mg/ml >> nan; nan', '0.039 M; 0.091 M; 1.1 M; 0.2 M; 1.2 M; 0.2 M', '39.5 mg/ml; 115.7 mg/ml', '0.442 molal; 1.07 molal; 1.48 molal; 13.6 mg/ml', '6.4 wt%; 33.6 wt% >> nan', '0.1426 M; 1.56 M; 1.74 M >> 8 mM', '0.3 M; 1.2 M >> 40 mg/ml >> 2 mg/ml', '0.442 molal; 1.07 molal; 1.48 molal; 13.6 mg/ml >> 1 mg/ml', '1 M.0.03M; 0.07 M', 'nan >> 1 mg/ml', '2.43 M; 0.81 M', '0.8 M; 10 mg/ml', '1 M; 0.952 M; 0.048 M', '1 M >> 30 mg/ml', '460 mg/ml >> 8.3 mg/ml >> nan', '2 M; 1 M', '0.06 M; 1 M; 0.2 M; 0.2 M; 1.1 M', '0.8 M; 0.8 M'])))

    reaction_solutions_volumes = Quantity(
        type=str,
        shape=[],
        description="""
    The volume of the reaction solutions used. used in each deposition procedure
- When more than one reaction step, separate the volumes associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- The volumes refer the volumes used, not the volume of the stock solutions. Thus if 0.15 ml of a solution is spin-coated, the volume is 0.15 ml
- For reaction steps without solvents, state the volume as ‘nan’
- When volumes are unknown, state that as ‘nan’
Example
0.04
nan >> 0.1
nan >> 10
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['0.02', '0.045', '0.07; Unknown', 'Unknown >> 0.05', 'Unknown >> 0.2', '0.06 >> Unknown', '0.75; 0.15; 0.1; 0.05 | 0.09', '1.25', '5.0', '0.05', 'Unknown >> 0.04', 'Unknown', '0.065', '0.08', '0.04 >> 0.04', '0.075', '0.035', 'Unknown >> 0.0157 >> 0.5', 'Unknown >> Unknown >> Unknown', '0.05 >> 0.1', 'Unknown >> Unknown >> 50.0', '0.25', 'Unknown >> Unknown', '0.0025; 0.0025', '0.06', '0.01', '0.08 >> 0.1', '1.0', '0.003', 'Unknown >> 8.0', '0.1', 'Unknown >> 0.00942 >> 0.5', '0.08 >> Unknown >> Unknown', '0.03 >> 0.2', '0.03'])))

    reaction_solutions_age = Quantity(
        type=str,
        shape=[],
        description="""
    The age of the solutions used in the deposition
- When more than one reaction step, separate the age of the solutions associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- As a general guideline, the age refers to the time from the preparation of the final precursor mixture to the reaction procedure.
- When the age of a solution is not known, state that as ‘nan’
- For reaction steps where no solvents are involved, state this as ‘nan’
- For solutions that is stored a long time, an order of magnitude estimate is adequate.
Example
0.5
nan >> 10
10000 >> nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['0.0 | 0.0', '24.0', '3.0', '1.0 >> 2.0', '60.0; 25.0', '600.0', '12.0', 'Unknown', '0.08', 'Unknown >> 60.0', '2.0 >> Unknown', '8.0', '70.0', '6.0', '0.167', 'Unknown >> Unknown', '2.0', 'Unknown >> 30.0', '12.0 >> Unknown >> Unknown', '0.5', '12.0 >> 0.033', '1.0', '48.0', 'Unknown >> 45.0', '8.0; 12.0'])))

    reaction_solutions_temperature = Quantity(
        type=str,
        shape=[],
        description="""
    The temperature of the reaction solutions.
- If there is more than one reaction step involved, list the solution temperatures and separate the data for each step by a double forward angel bracket (‘ >> ‘)
- If a reaction solution undergoes a temperature program, list the temperatures (e.g. start, end, and other important points) and separate them with a semicolon (e.g. heated to 80°C and cooled to room temperature before used would be80; 25)
- When the temperature of a solution is not known, state that as ‘nan’
- For reaction steps where no solvents are involved, state the temperature of the gas or the solid if that make sense. Otherwise mark this with ‘nan’
- Assume that an undetermined room temperature is 25
Example
25
nan >> 50
80; 25
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['80 | Unknown', '25', '310 >> 150 >> 25', '25 >> 13', '0 | Unknown', 'Unknown; 50', '40 | Unknown', '70 >> 25 >> 25', '70 >> 80', '50.0', 'Unknown >> 150', '70', '125.0', 'Unknown', '60; Unknown', '25; 25', '100', '130', '75.0', '60; 25', '100.0', 'Unknown >> 160', '70 | Unknown', '12', '75', '60', '65', '70 >> 25 >> 70', 'Unknown >> 120', '25 >> 25 >> 25 >> 25 >> 25 >> 25 >> 25 >> 25 >> 25', '90', '25 >> 25', '80 >> 25', 'Unknown >> 140', 'Unknown >> 25', '150.0', '70; 25', '100 >> 25', '25.0', '80; 25', '75 >> 25', '70 >> 25', '50', '70 >> Unknown', '55; 100 >> 25 >> 25 >> 25 >> 25 >> 25 >> 25 >> 25 >> 25 >> 25', '55; 100', 'Unknown; 150', '60 >> 60', '60 >> 70'])))

    substrate_temperature = Quantity(
        type=str,
        shape=[],
        description="""
    The temperature of the substrate on which the perovskite is deposited.
- When more than one reaction step, separate the temperatures of the solutions associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If a reaction solution undergoes a temperature program, list the temperatures (e.g. start, end, and other important points) and separate them with semicolons, e.g. 25; 100
- When the temperature of a solution is unknown, state that as ‘nan’
- For reaction steps where no solvents are involved, state the temperature of the gas or the solid if that make sense. Otherwise state this as ‘nan’
- For values with uncertainties, state the best estimate, e.g. write 120 and not 110-130.
- Assume an undetermined room temperature to be 25
Example
25
70 >> 25
nan >> 40
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['80 | Unknown', '', '25', '0 | Unknown', '25 >> 13', '85 >> 25', '40 | Unknown', '0', '25 >> 50', '85', '70', '25 >> 110', '-10', '21', 'Unknown', '100', '25 >> Unknown', '120', 'Unknown >> 20; 110', '40', '150', '25 >> 130', '140.0', '70 | Unknown', '25 >> 75', '100 >> Unknown', '70.0', '60', 'Unknown >> 70', '190.0', '90', 'Unknown >> Unknown', '25 >> 25', '80 >> 25', '25 >> 25 >> 25 >> 25 >> 25 >> 25 >> 25 >> 25 >> 25', '25 >> 90', 'Unknown; 25 >> 25; 150 >> 25', '175', 'Unknown >> 25', '25 >> 25 >> 25 >> 25 >> 25 >> 25 >> 25 >> 25 >> 25 >> 25', '100 >> 25', '70 >> 25', '90 | 25', '25 >> 150', '50', 'Unknown >> 25 >> 25', '70 >> Unknown', '70 >> 150', '90 >> 25', '10'])))

    quenching_induced_crystallisation = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE is measures were taken to discontinuously accelerate the crystallisation process without significantly changing the temperature. i.e. an antisolvent treatment or an analogue process was used.
- The most common case is the antisolvent treatment where a volume of a solvent in which the perovskite is not soluble is poured on the substrate during spin coating.
- The same effect can also be achieved by blowing a gas on the sample
- If the sample quickly after spin coating is subjected to a vacuum, this also counts as quenched induced crystallisation
                    """,
        a_eln=dict(
            component='BoolEditQuantity'))

    quenching_media = Quantity(
        type=str,
        shape=[],
        description="""
    The solvents used in the antisolvent treatment
- If the antisolvent is a mixture of different solvents, e.g. A and B, list the solvents in alphabetic order and separate them with semicolonsas in (A; B)
- If gas quenching was used, state the gas used
- If the sample quickly after spin coating was subjected to a vacuum, state this as ‘Vacuum’
- If an antisolvent was used but it is unknown which one, stat this as “Antisolvent”
- If no antisolvent was used, leave this field blank
Example
Chlorobenzene
Toluene
Diethyl ether
Ethyl acetate
N2
Vacuum
Anisole
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['Tetraethyl orthosilicate', '2-butylalcohol', 'Chlorobenzene; TBP', 'Chlorobenzene; DMSO', 'Butyl acetate', 'Air plasma', 'Tetrachloroethane', '2-Butanol; Ethyl ether', 'Ethyl ether; Hexane', 'Ethyl acetate; IPA', 'Bromobenzene', 'Tetrafluorotoluene', 'Thermal radiation', 'p-xylene', 'MeOAc', 'Chlorobenzene; H2O', 'Chlorobenzene', 'Methyl-phenoxide', 'Chlorobenzene; Ethyl acetate', 'Chloroform; Toluene', 'Ethanol', 'Pumping solvent', 'Acetone', 'Ar', 'Ethyl ether', 'Chloroform', 'N2', 'Gas', 'Anisole; Toluene', 'o-xylene', 'Diethyl ether; Chlorobenzene', 'NIR', 'Chlorobenzene; 2-Butanol', 'He', 'Di-n-butyl ehter', 'n-Butyl alcohol', 'Diethyl ether', 'Rotating magnetic field', 'Dry air', 'Diphenyl ether', 'liquid N2; N2', 'Chlorobenzene; Ether', 'Chlorobenzene; N2', 'Chlorobenzene; Toluene', 'Chloroform; Hexane', 'Trifluorotoluene', 'Dichlorobenzene', '2-Butanol; Chlorobenzene; Ethyl ether', 'acetonitrile; Chlorobenzene', 'Unknown', 'Ethyl benzene', 'Trimethylbenzene', 'Diclorobenzene; Toluene', 'Ethyl acetate; Petroleum ether', 'Petroleum ether', 'N2 >> Chlorobenzene', 'TEOS', 'Diethyl ether; Methanol', '2-Butanol', 'Air', 'Diisopropyl ether', 'Vacuum', '2-Butanol; Chlorobenzene', 'Hot air', 'Diethyl ether; Toluene', 'Ether', 'Hexane', 'Ethanol; Toluene', 'Ethyl acetate; Toluene', 'Dichloromethane', 'Di-n-propyl', 'Chlorobenzene; Diethyl ether', 'Anisole', 'Chlorobenzene; Ethanol', 'Anisole; Chlorobenzene', 'Chlorobenzene; Diiodooctane', 'n-BA', 'Flash infrared annealling', 'Antisolvent', 'Methanol', 'Chlorobenzene; IPA', 'IR', 'Ethyl acetate', 'Anisole >> N2', 'Triochloromethane', 'Methyl acetate', 'Chlorobenzene; Chloroform', 'Propyl acetate', 'Toluene', 'Isopropyl acetate; Toluene', 'IPA', 'Hot substrate', 'Iodobenzene', 'Chlorobenzene; Acetic acid'])))

    quenching_media_mixing_ratios = Quantity(
        type=str,
        shape=[],
        description="""
    The mixing ratios of the antisolvent
- The order of the solvent must line up with the previous column
- For solvent mixtures, i.e. A and B, state the mixing ratios by using semicolons, as in (VA; VB)
- The preferred metrics is the volume ratios. If that is not available, mass or mol ratios can be used instead, but it the analysis the mixing ratios will be assumed to be based on volumes.
- For pure solvents, give the mixing ratio as 1
- For non-solvent processes, give the mixing ratio as 1
Example
1
4; 1
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', '1; 0.08', '1; 0.2', '990; 10', '1; 0.02', '3; 7', '90; 10', '9; 1', '1', '1; 1', '10; 90', '98; 2', '75; 25', '49; 1', '4; 1', '1; 0.04', '1; 0.01', '9; 5; 5', '1; 0.5', '6; 94', '96; 4', '30; 70', '47; 3', '1; 0.12', '97; 3', '15; 1', '1; 0.10', '25; 75', '1; 0.3', '1; 0.4', '2; 3', '20; 80', '95; 5', '99; 1', '40; 60', '1; 3', '50; 50', '1; 0.06', '5; 95', '70; 30', '24; 1', '2; 25', '1; 0.7', '92; 8', '1; 4'])))

    quenching_media_volume = Quantity(
        type=str,
        shape=[],
        description="""
    The volume of the antisolvent
- For gas and vacuum assisted quenching, stat the volume as ‘nan’
- If the sample is dipped or soaked in the antisolvent, state the volume of the entire solution
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['40.0', '90.0', '300.0', '350.0', '50.0', '425.0', '125.0', '0.6', '600.0', '120.0', 'Unknown', '450.0', '180.0', '45.0', '100.0', '900.0', '130.0', '400.0', '140.0', '240.0', '30000.0', '70.0', '110.0', '80.0', '250.0', '190.0', '30.0', '500.0', '150.0', '750.0', '700.0', '1.0', '1000.0', '20.0', '160.0', '200.0'])))

    quenching_media_additives_compounds = Quantity(
        type=str,
        shape=[],
        description="""
    List of the dopants and additives in the antisolvent
- If several dopants/additives, e.g. A and B, are present, list the dopants/additives in alphabetic order and separate them with semicolonsas in (A; B)
- If no dopants/additives, leave the field blank
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', 'FABr', 'CsPbBr3-QDs', 'F-PDI', '2,9,16,23-tetra-tert-butyl-29H,31H-phthalocyanine', 'Poly(TA)', 'K2Rrubrene', 'L‐Leucine', 'Undoped', 'Acetylene black', 'ITIC', 'CsI', 'MAI', 'PbS-QDs', 'MABr', '6TIC-4F', 'Poly(9-vinylcarbazole)', 'Hex', 'PDMS', 'AQ310', 'P3HT', 'FAI', 'Cl-functionalized C-np', 'ITIC; PCBM-60', 'ThFAI; MAI, MACl', 'SM', 'Au-np', 'Rubrene', 'PEG', 'PCBM-60', 'Graphdiyne', 'Carbon black', 'MEH-PPV', 'FAI; MABr', 'PAMS', 'Graphydine-QDs', 'SWCNTs', 'bis-PCBM-60', 'La:BaSnO3-np', 'NPB', 'Spiro-MeOTAD', 'FAPbBr3-QDs', 'C60', 'BAI', 'MAPbBr3-QDs', 'PS', 'PBTI', 'BiFeO3-np', 'BHT', 'DF-C60', 'CuPc', 'tFM-PMAI', 'PTB7; ITIC', 'PTAA', 'IDIC-Th', 'CsPbBr3-np', 'PBDB-T', 'Carbon-nt', 'PCBM-60; TIPD', 'PABr', 'ADAHCl', 'MACl', '[M4N]BF4', 'IEICO-4F', 'H2O', 'HI', 'PEAI', 'Au@CdS', 'I2', 'PFA', 'TPFPB', 'IDIC', 'Br passivated C-np', 'DPPS', 'HEA', 'Polyurethane', 'EABr', 'MA', 'F16CuPc', 'C60; PEG', 'PTB7', 'AQ', 'PMMA', 'MAPbI3-QDs', '(PEA)2PbI4'])))

    quenching_media_additives_concentrations = Quantity(
        type=str,
        shape=[],
        description="""
    The concentration of the dopants/additives in the antisolvent
- If more than one dopant/additive in the layer, e.g. A and B, separate the concentration for each dopant/additive with semicolons, as in (A; B)
- For each dopant/additive, state the concentration.
- The order of the dopants/additives must be the same as in the previous filed.
- Concentrations can be stated in different units suited for different situations. Therefore, specify the unit used.
- The preferred way to state the concentration of a dopant/additive is to refer to the amount in the final product, i.e. the material in the layer. When possible, use on the preferred units
o wt%, mol%, vol%, ppt, ppm, ppb
- When the concentration of the dopant/additive in the final product is unknown, but where the concentration of the dopant/additive in the solution is known, state that concentration instead. When possible, use on the preferred units
o M, mM, molal; g/ml, mg/ml, µg/ml
- For values with uncertainties, state the best estimate, e.g write 4 wt% and not 3-5 wt%.
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', '0.1 mg/ml', '9 mg/ml', '0.024 mM', '40 mg/ml', '0.24 mg/ml; 0.24 mg/ml', '25 mg/ml', '20 mg/ml', '0.32 mg/ml; 0.16 mg/ml', '20 vol%', '1 vol%', '0.25 M', '0.00001 M', '0.5 mg/ml', '0.05', '0.005', '0.5 vol%', '8 mg/ml', '0.001 M', '1 mg/ml', '0.25 mg/ml', '4 vol%', '5 mg/ml', '0.36 mg/ml; 0.12 mg/ml', '0.1 M', '0.015', '2 mg/ml', '0.3 mg/ml', '6 mg/ml', '0.03', '0.000001 M', '15 mg/ml', '12 mg/ml', '30 mg/ml', '2 vol%', '10 mg/ml', '10 wt%', '3 mg/ml', '0.0001 M', '5 wt%', '0.7 mg/ml', '4 mg/ml', '0.5 M'])))

    thermal_annealing_temperature = Quantity(
        type=str,
        shape=[],
        description="""
    The temperatures of the thermal annealing program associated with each deposition step
- When more than one reaction step, separate the annealing temperatures associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If the thermal annealing involves a temperature program with multiple temperature stages, list the temperatures (e.g. start, end, and other important points) and separate them with semicolons (e.g. 25; 100)
- For values with uncertainties, state the best estimate, e.g. write 120 and not 110-130.
- If no thermal annealing is occurring after the deposition of a layer, state that by stating the room temperature (assumed to 25°C if not further specified)
- If the thermal annealing program is not known, state that by ‘nan’
Example
100
70; 100 >> 100
25 >> 90; 150
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['70.0 >> 70.0; 90', '70; 100 >> 150', '320; 200', '105.0 >> 105.0 >> Unknown', '90.0', '170.0 >> 100.0', '65 | 130', '45; 105', 'Unknown >> 105', '325.0', 'Unknown >> 25.0', '85', '50.0', 'Unknown >> 280.0', '70.0 >> 165.0', '100.0 >> Unknown', '220.0', '70.0 >> 100.0', '70.0 >> 85.0', '45; 100 >> 100', '100; 125', '150.0 >> 150', 'Unknown >> 100', '180.0', '65.0; 150', '60.0; 80.0', '45.0', '320; 250', '100 >> 165.0', '240; 105', '120.0 | Unknown', '25 >> 130', '70 | Unknown', '90; 25 >> 25 >> 150', '150.0 >> 100', '85.0 >> 105.0', '40 >> 180', 'Unknown | 100.0', 'Unknown >> 90.0', '85; 100', '30; 160', '65; 100 >> Unknown', '95', 'Unknown >> 115', '150; 100', '70.0 >> 110.0', '70.0 | 140.0', 'Unknown >> Unknown >> 100', '135', '105.0 >> 105', '40.0; 100 >> 90.0', '65.0; 135.0', '200; 105', '70.0 >> 70.0; 70.0', '100.0 >> 135.0', '50 >> 260', '45; 65; 100', '75 >> 75; 70', '25.0; 280.0', '100.0 >> 185.0', '400.0 >> 400.0', '70 | 130', '100; 120', '80 >> 110', '70.0 >> 70', '115; 100', '80.0 >> 135.0', 'Unknown >> 350', '100.0 >> 75.0; 100', 'Unknown >> 130', '90.0 >> 250.0 >> 250.0 >> 250.0', 'Unknown >> 50; 100', '95.0', '25; 300', '90.0 >> Unknown', '70.0 >> 80.0', '40; 100 >> 40; 100', '140.0 >> Unknown', '40; 100 >> 100', '40.0 >> 150.0', '70.0', '100 >> 150', '140.0 >> 145.0', '60.0; 80.0; 100.0', '42.0; 160.0', '160; 100', '70; 90 >> 250', '500.0', '70 >> 100.0', '90 >> 250', '60.0 >> 90.0', '90.0 >> 90.0', '0 >> 100', 'Unknown >> 60', '70 >> Unknown', '145 >> 100', '100.0 >> 100.0 >> 100.0', '130.0 >> Unknown >> 100.0', '70.0; 100 >> 100.0', '60; 85', '150.0 >> 100.0', '120; 100', '80 >> 100', '260.0', '75; 105', '80.0 >> 110.0', '85.0 >> 90.0', '175.0', '100.0 >> 100', 'Unknown >> 275.0', '160.0 >> 160.0', 'Unknown >> 150.0', '40 >> 180 >> 130', '20.0; 70.0; 100.0; 120.0', '90 >> 250 | 85', 'Unknown >> 320.0', '20; 70', '45 >> 160', '90; 25 >> 25 >> 90', '65; 135', '240.0', 'Unknown >> 70', '38.0; 160.0', '110.0 >> 250.0', '70 >> 25 >> Unknown', '70.0; 100 >> 90', '25 >> 25 >> 25 >> 25 >> 25 >> 25 >> 25 >> 25 >> 25 >> Unknown', '60.0 >> 60.0 >> Unknown', '90', 'Unknown >> Unknown', '130 >> 70', '120.0 >> 100.0', 'Unknown >> 325.0', '330.0', 'Unknown >> Unknown >> 120', '40; 60; 70; 100', '75.0 >> 250.0', '70.0; 90.0 >> 90.0', '70 >> 100', 'Unknown >> 85', '120 >> 80', '100; 100', '90 >> 95', '25.0 >> 100.0', '55; 240', '85.0', '40 | 100 | 100', '40.0; 95.0', '25; 50; 75; 100', '260.0 >> Unknown >> Unknown', '70.0 >> 90.0', '90.0 >> 250.0', '100 >> 70; 100', '90.0; 125.0', '20; 100', '100.0 >> 55.0', '70; 250', 'Unknown >> 40; 100; 130', '120.0 >> 80.0', 'Unknown >> 70.0; 150', '60 >> 250', '280', '25.0 >> 170.0 >> 170.0 >> 170.0', '80; 120; 180', '60.0 >> 100.0', '27.0 >> 100.0', '52; 105', '150.0; 100.0', '70.0 | 120.0', '80.0 >> 140.0', '100 >> 70', '65; 105', '90.0 >> 60.0', 'Unknown >> Unknown >> 70.0', '25; 90', '25; 95', '180 >> 280', '70 >> 120', '110.0 | 25.0 | 25.0 | 110.0', 'Unknown >> 120.0', 'Unknown | 150', '60; 80; 100 >> Unknown', 'Unknown >> 104.0', '70; 300', '160; 230', '45.0; 160.0', '80.0; 120.0', '20.0', '25; 100', '165.0', '50', '20.0 >> 100.0', '50; 100 >> 100', '125.0 >> 100.0', '70.0 >> 130.0', '110; 70', '60; 140', '100 >> 65', '110.0 >> 70.0', '92.0', '70 >> 60; 100', '25; 60', '150 >> 150 >> 150 >> 150', '105.0 >> 105.0', '80 >> 80', '0.0; 60.0; 70.0; 80.0; 90.0', '60; 80', '180', '70; 110; 150', '100.0 >> 250.0', '40; 90 >> 95', '100; 330', '100.0; 100', '130; 150', '70.0 >> 75.0', '50.0 >> Unknown', '72.0 >> 140.0', '70.0; 100.0 >> 100.0', '25 >> 90.0', '100; 110; 120', '300.0 >> Unknown', '90; 250 >> 250', '20; 90', '65', '250.0', '20; 70; 100; 120', '60 >> 100', '70.0 >> 145.0', '100.0 >> 100.0 >> 175.0', '65.0', '50; 150; 270', '71.0 >> 70.0', '200; 150', '150.0', '35; 120 >> 120', '60.0; 70.0; 80.0; 90.0', '90 >> 25 >> 90', '85.0 >> 85.0', '28.0 >> 100.0', '60; 60; 90', '110.0 >> 150.0', '240 >> 120', '70; 95 >> 100 >> 100', '60; 100 >> 150', '90.0 >> 150.0', 'Unknown >> 70.0', '25 >> 70 | Unknown', '60; 70; 80; 90; 100; 100', '105', '180.0 >> 180.0', '110 >> 70; 100', '60.0; 100', '150.0 >> 150.0', '67.0; 100.0', '25; 50; 60', 'Unknown >> 80.0', 'Unknown >> 210.0', '150; 100 >> 100', '65.0 >> 100 >> Unknown', '110 >> 150', '50.0 >> 50.0 >> Unknown', '120 >> 100', 'Unknown >> Unknown >> Unknown >> 120.0', '90.0; 120.0', '70.0 >> 125.0', '60.0; 85', 'Unknown >> 170', '60.0 >> 60.0', '25; 90; 120', '70.0 >> 100.0 >> 100.0', 'Unknown >> 160', '40; 100 >> 150', '100.0 >> 100.0 >> 1000 >> Unknown', '60; 70; 80; 90; 100', 'Unknown >> 60; 80; 100', '100.0 >> 100.0', '26.0 >> 100.0', '70; 100 >> 70; 100', 'Unknown >> Unknown >> 105.0', '100 >> 120; 100', '50.0; 100.0', '70; 100 >> 145', '125.0; 100.0', 'Unknown >> 50.0', 'Unknown >> 140.0', '110.0 >> 105.0', '20; 80', '175', '90.0 >> 250.0 >> 250.0', '160; 105', '35.0', '75 >> 150', '140; 180', '120 >> 150', '90 >> 85', '135.0', '80.0 >> 110.0 >> 110', '250', '70 | 145', '40; 160', 'Unknown >> Unknown >> Unknown >> 130.0', '90 >> 250.0', '75.0 >> 100.0', '100.0 >> 100.0 >> Unknown', '33.0', '100 >> Unknown >> Unknown >> 100', '320', '140; 100', '75 >> 250', '25.0 >> Unknown', 'Unknown >> 70.0 >> 70.0', '70.0; 110', '60.0; 120', '66.0; 100.0', '100.0 >> 25.0 >> 100.0', '51.0 >> 70.0', '30; 40; 50; 60; 70; 80; 90; 100', '70 >> 108', '60; 100', 'Unknown >> Unknown >> 60.0 >> 60', '100 >> 80; 100', '75.0 >> 135.0', '70.0 >> 120.0', '40', '70 >> 90 >> 90', '70 >> 100 >> 100', '100 >> Unknown', '40; 60; 80; 100', '60; 150', '100 | 100', '70.0 >> 70.0 >> 80.0', '80 >> 40; 140', '90.0 >> 100.0', '50; 160', '70.0 | 135.0', '110; 25 >> 110', '80.0 >> 170.0', '100.0 >> Unknown >> Unknown >> Unknown', '80.0 >> 80.0 >> 80.0 >> Unknown', '90.0 >> 80.0', 'Unknown >> Unknown >> Unknown >> 350.0', '70.0 >> 200.0', '285.0', '70 >> 70', '120.0 >> 85.0', '25.0', '80.0 >> 120.0', '130.0 >> 130.0', 'Unknown >> 175', '115', '60; 70 >> 70; 115', '35; 120', '70 >> 85', '80.0 >> 250.0', '70 >> 150', 'Unknown >> 35.0', '40.0', '25 >> 115', '60.0; 100 >> 100; 140', '300', '70; 130', '80.0 >> 90.0', '70 >> 145', 'Unknown >> Unknown >> 150.0', 'Unknown >> 150', '70.0 >> 50.0', '70; 100; 120', '100; 120; 140', '100 | 65', '75.0', '110', 'Unknown >> 60.0', '60.0; 100 >> Unknown >> 100.0', '70.0 >> 105.0', '25.0 >> 250.0', '50; 100 | 50; 100', '35; 280', '40 | 105', '190 >> 330.0', 'Unknown >> 100.0 >> 70.0', '120; 130', '70; 130 >> 145', '25; 70 >> 85', '25 >> 100 >> 70', '160.0 >> 100.0', '150.0 >> 110.0', '130; 160', '60; 25; 100', '80; 150', '190.0', '25; 60; 65', '70.0 | Unknown | 130.0', '90.0; 100.0', '90 | 150', '100 >> 100', '330', '40; 55; 75; 100', 'Unknown >> 110.0; 120', '70 >> 140', 'Unknown >> 90', 'Unknown >> Unknown >> 130.0', '70 >> 75', '150.0 >> 90.0', '170; 100', '65.0 >> 70.0', '93.0', '60; 80; 100', '155.0', '100.0 >> 130.0', '25.0 >> 25.0', '70.0 | 70.0', '25; 130', '25 >> 150', '145.0', '45; 160', '65.0 >> 125.0', 'Unknown >> 130.0', '120; 40', '90.0 >> 85.0; 160', '180.0 >> 150.0', 'Unknown >> 90.0 >> 90.0', '110.0; 100.0', '70 >> 70.0', '25', '70.0 >> 160.0', '120.0 >> 150.0', '100.0 >> 150.0', '140.0 >> 140.0', '35; 120; 165', '280.0', 'Unknown >> 60; 70; 80; 90; 100', '60.0', '125.0', '100 >> 90', '80.0 >> 60.0', '120.0 >> Unknown', '70.0 >> Unknown', 'Unknown >> 180; 150', '130', '70.0 >> 95.0', 'Unknown >> 250', 'Unknown >> Unknown >> 350.0', '100.0 >> 75.0 >> Unknown', '60.0; 100 >> 100.0', 'Unknown >> 150.0; 100', '400.0', '70 | 150', '75 >> 75', 'Unknown >> 180.0', '80; 25 >> 80', 'Unknown >> 100.0', 'Unknown | 100', '50.0; 100 >> 150.0', '90.0 >> 110.0', '40.0 >> 250.0', '65; 125', '50; 85', 'Unknown >> 75.0', '50; 120', '115.0', '70.0 >> 140.0', 'Unknown >> Unknown >> 160', '50.0; 150.0', '25; 70; 100; 120', 'Unknown >> 140', '90 >> Unknown', '100.0 >> 70.0 >> 130.0', '90 >> 90', '60.0; 85.0', '265.0 >> 100.0', '80.0 | 150.0', '100; 180', '42; 160', '75; 90', 'Unknown >> 100.0; 140.0', '140', '100.0 >> 70', '70.0 >> 170.0', '70; 275', '80 >> 280', '285', '55; 250', '65 >> 100', '110; 115', '130.0 >> 120.0', '150.0 >> 170.0 >> 170.0 >> 170.0', '80.0 >> 350.0', 'Unknown >> 150; 120', 'Unknown >> 170.0 >> 170.0 >> 170.0', '550', '40 >> 180 >> 150', '120; 200', '40; 55; 70; 100', 'Unknown >> 150 >> 100', '25.0; 90.0', 'Unknown >> 160.0 >> 160.0', 'Unknown >> 135.0', '100 >> 280', '60 >> 200', '70 >> 70 >> Unknown', 'Unknown >> 20.0', '100.0 >> 165.0', '100', '75 >> 180', '100.0', '105.0', '40; 70 >> 40; 100', '65; 185', '70 >> 100; 120', '200; 130', '75 >> 200', '300.0 >> 150.0', '50 >> 200; 150', '80.0 >> Unknown', '70; 25 >> 25 >> 70', '60.0; 80', '60.0 >> 110.0', '90 >> 160', '70; 120', '80 >> 250', '25; 280', 'Unknown >> Unknown >> 135', '75; 125', '50; 100 >> 50; 100', 'Unknown >> Unknown >> 100.0', '70 >> 150 >> 100', '70.0 >> 100.0 >> 100', '300.0 >> 150', '80 | 80', '150 >> 25', '60.0 >> 150.0', '90.0 >> 70.0', '70; 100 | 100', '300 >> Unknown', '120.0 >> 90.0', '90.0 >> 250.0 >> Unknown', '100.0 >> 120.0', '200.0', '70.0; 100 >> Unknown', '300 >> 25 >> 25 >> 25 >> 25 >> 25 >> 25 >> 25 >> 25 >> 25 >> Unknown', '70.0; 90.0; 100.0', 'Unknown >> 50.0; 80', '95; 120', '350.0', '40; 120', '72.0 >> Unknown >> 140.0', '90.0; 120', '60; 125', 'Unknown', '70 >> 70; 100; 120', '90.0 >> 90.0 >> 90.0', '60; 90', '90; 100', '150 >> 280', '50; 150', '50; 130', '40.0; 100.0 >> 40.0; 100.0', '50; 100', '110.0; 130.0', '75 >> 130', '70.0 >> 115.0', '100; 140', '75.0 >> 70.0', '100.0 >> Unknown >> Unknown >> Unknown >> Unknown', '100; 85', '130; 170', '105.0 >> 110.0', '25 >> 25', '25 >> 135', '60 >> 100.0', '340.0', 'Unknown >> 170.0', '70.0 >> 25.0', '120.0 >> 120', '101.0 >> 100.0', '70; 175', 'Unknown >> 125.0', 'Unknown >> 160.0', '110.0 >> 100.0', '85.0 >> 150.0', '80 >> 90', '160.0', '40 >> 100', '70 | 100', '25; 80; 85; 90', '60.0 >> 105.0', '110.0 >> 75.0', '100; 130', '50; 140', '90; 150', '270.0', '50; 75; 100', '70; 100', '25 >> 25 >> 100', '170.0', 'Unknown >> 110.0', '75; 100', '120.0 >> 90.0 >> 80.0', '100.0 >> 70.0', '150 >> 150 >> 150', '150.0 >> 70', '80 >> 150', '25; 85', '170', '200', '70 >> 130', '320; 300', '25; 60; 100', 'Unknown >> 115.0; 100', '70; 70 >> 145', '100; 300 >> 100', '55.0', '65.0; 100.0', 'Unknown | 115.0', '90 | Unknown', '77', '60; 105', '105.0 >> Unknown', '130; 130', '50; 250', '100.0 >> 140.0', '25; 75 >> 135', '340', '50; 60; 70; 100', '22.5; 70; 180', '100.0; 120.0', '70.0 >> 70.0', '100 >> 250', '180; 105', '95.0 >> 60.0', '40; 110 >> 110', '60.0 >> 60.0 >> 60.0 >> Unknown', '110.0 >> 145.0', '65.0; 100', '145', '80.0 >> 150.0', 'Unknown >> 280', '100; 500 >> 110', '70 >> Unknown >> 150', '25; 150', '80.0 >> 100.0', '25; 100.0', '25; 120', '44.0', '110.0 >> 120.0', 'Unknown >> 100.0; 150', '90.0 >> 70.0; 100.0', '100.0 >> 280.0', '80; 100', '90; 120', 'Unknown >> 65; 100', '50; 100; 160', '35; 85', 'Unknown >> 170.0 >> Unknown', '550.0', '100 >> 25; 25', '70; 150 >> 100', '300.0', '120.0 >> 135.0', 'Unknown >> 40.0; 100', '185.0', '3; 5 >> 5', '90; 120 >> 100', '120.0', '0.0; 90.0', '110.0 >> 110.0', '450.0', '90.0 >> 120.0', '40.0; 100 >> 90.0 >> Unknown', '25 >> 25 >> 70', '150 >> 150', '70; 150 >> 400', '70 >> 90', 'Unknown >> 90.0; 120.0; 150.0', '130.0', '70.0 >> 150.0', 'Unknown >> 95.0', '40.0 >> 100.0', '100.0; 100.0', '60.0; 100.0', '50.0 >> 50.0 >> 50.0 >> Unknown', '25.0 >> 110.0', '75', '110.0', '70.0; 100.0', '310.0', '25.0; 100.0', '100.0; 150.0', '220', '25 >> 70', '70.0 >> 95.0 >> 95.0', '25.0 >> 150.0', 'Unknown >> 200.0', '100; 25 >> 25 >> 25', '345.0', '50.0; 85.0', 'Unknown >> 105.0', '60.0; 100 >> 60; 100', '110; 130; 150', 'Unknown >> 250.0', '100.0; 280.0', '170; 330', '100.0 >> 150', '225.0', '60.0; 100 >> Unknown', '70; 90 >> 70.0', '160', '80.0; 100.0', 'Unknown >> 120.0 >> 145.0', '60.0 >> 70.0', '25 >> 85', '170; 150', '100.0 | 100.0', '70 >> 125', '40.0; 160.0', '40.0 >> 40.0', '56; 240', '100 >> 110; 100', '100 | 100 >> 100', '70 >> 75; 70', '40 >> 100 >> 100', '100.0 >> 155.0 >> 150.0', '70; 100 >> 100', '310.0 >> 150.0', '100 >> 100; 100', 'Unknown >> 265.0', '100 >> 110', '10.0', '70', '140.0 >> 160.0', '110.0 | 150.0', '220; 105', '70 >> 70.0 >> 70', '42.0', '150; 25 >> 100', '70.0 >> 70.0 >> 70.0', '150 >> 100', '70 | 70', '200.0 >> 80.0 >> 80.0', 'Unknown >> 120', '250 | 100', '60; 120', '210.0', 'Unknown >> 100.0 >> Unknown', '85.0 >> 100.0', '75 >> 135', '130.0 >> Unknown', '43 >> 160', '60; 110', '90.0 >> 115.0', '80.0 >> 80.0', '70; 100 >> 135', '120.0; 150.0', 'Unknown >> 85.0', '50.0 >> 70.0', '70.0 >> 100.0; 150.0', '95.0 >> 100.0', '350', '75.0 >> 75.0', '100.0 >> Unknown >> Unknown', '32.0', '100.0 >> 50.0; 250', '40.0 >> Unknown', '100.0 >> 155.0', '60; 250', '100; 160', '90; 125', '60.0 >> 60.0 >> 60.0 >> 60.0', '25.0 >> 70.0', 'Unknown >> 85.0 >> 85.0', '70.0 >> 135.0', '110; 25', '130; 100', 'Unknown >> 110', '70.0 >> 70.0 >> Unknown', '100.0 >> 140', 'Unknown >> 150.12', 'Unknown >> 380.0', '25; 90; 100; 130', 'Unknown >> 350.0', '45; 55; 75; 100', '60; 130', '60; 80; 140', '25 >> 120', '100.0 >> 25.0 >> 25.0', '5; 95.0', '80; 150; 350', '80; 140; 160', '265.0 >> 200.0', '200; 170', '150', '45.0 >> 100.0; 150', '90 >> 100', 'Unknown | 125', '160.0; 100', '260.0 >> Unknown', '250.0 >> 80.0', '80.0 >> 50.0; 120', '65; 100', '85.0 >> 250.0', '150.0 >> Unknown', '50; 100; 120 >> 25', '30.0', '55', 'Unknown >> 80', '80; 90; 100; 110', '60.0 >> 140.0', 'Unknown >> 175.0', '100 >> Unknown >> Unknown', '100; 150', '70; 150', '50; 60; 70; 80; 90; 100', '25; 70', '70.0 | 150.0', '40; 100', '25 >> 140', '100.0 >> 110', '70.0 >> 110.0 >> 40.0', '25 >> 100', '100 >> 75', '335.0', '95.0 >> Unknown', 'Unknown >> 145.0', '70.0 >> 175.0', '125.0 >> 160.0', '80; 120', 'Unknown >> 115.0', 'Unknown >> 300.0', '65.0 >> 100', '25; 280 >> Unknown', '120.0 >> 250.0', '150 | 100', '70.0; Unknown', '90; 25 >> 25 >> 120', '55.0; 60.0; 100.0', '100 >> 100 >> 100', '158.0', '60 >> 150', '50.0; 100 >> 100.0', '80', '75.0; 150.0', '50 >> 280', '120', '1000.0 >> Unknown', '100.0; 150', '60; 100 >> 100', '140.0', '65; 75; 85; 95', '25; 100; 25 >> 100', '80.0', '60', '320.0', '70 >> 150 >> 70', '150.0 >> 120.0', '120.0 >> 120.0', '80.0 >> 70.0', 'Unknown >> 100.0 >> 100.0', '60 >> 60 >> 60.0', '70.0 >> 70.0 >> 70.0 >> Unknown', '125.0 >> 125.0', '100 >> 25', '100.0 >> 100.0 >> 100', '130; 140', '130; 120', 'Unknown >> 60.0; 100', '70.0 >> 250.0', '100.0; 140.0', '310', '45; 120', '60.0 >> Unknown'])))

    thermal_annealing_time = Quantity(
        type=str,
        shape=[],
        description="""
    The time program associated to the thermal annealing.
- When more than one reaction step, separate the annealing times associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If the thermal annealing involves a temperature program with multiple temperature stages, list the associated times at those temperatures and separate them with semicolons.
- The annealing times must align in terms of layers¸ reaction steps and annealing temperatures in the previous filed.
- If a time is not known, state that by ‘nan’
- If no thermal annealing is occurring after the deposition of a layer, state that by ‘nan’
- For values with uncertainties, state the best estimate, e.g. write 20 and not 10-30.
Example
60
5; 30 >> 60
0 >> 5; 5
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['90.0', 'Unknown >> Unknown >> 60.0', '45.0 >> 5.0', '5.0; 20.0', 'Unknown >> 25.0', '50.0', '3.0 >> 3.0; 35.0', '5.0 >> 5.0 >> 10.0', '600.0 >> 30.0', '1.0; 1.0; 10.0', '180.0', '45.0', '10.0 >> 70.0', '0.083', '0.0; 5.0', '5.0; 5.0; 5.0; 5.0', '0.133', '3.0; 10.0 >> 3.0; 10.0', '1.0; 2.0', 'Unknown >> Unknown >> 20.0', '60.0 >> 60.0; 10.0', '2880.0 >> 1.0 >> 1.0 >> 15.0', 'Unknown >> 90.0', '30.0 >> 60.0 >> 30.0', '2.0; 28.0', '720.0 >> 3.0', '1.0 >> 1.0', '10.0; 10.0 >> 30.0', '4.0; 1.0', 'Unknown >> 720.0', '0.1666', '60.0 >> 2.0 >> Unknown', '3.0 >> 2.0', '5.0; 10.0 >> 10.0', '15.0; 50.0', '20.0 >> 40.0', '30.0; Unknown >> Unknown >> 30.0', '5.0 >> Unknown >> Unknown', '0.0', '0.066', '5760.0', '15.0 >> 15.0 >> 15.0', '60.0 >> 5.0 >> 5.0 >> 5.0', '15.0; 10.0 >> Unknown', '10.0 >> 10.0 >> 30.0', '0.07', 'Unknown >> 15.0; 60.0', '0.0 >> 0.0 >> 0.0 >> 0.0 >> 0.0 >> 0.0 >> 0.0 >> 0.0 >> 0.0', '0.33; 60.0', '120.0 >> 30.0', '3.0; 20.0', '8.0 >> 120.0', '4.0 >> 30.0', '2.0; 30.0', '30.0; 5.0', '60.0; 10.0 >> 10.0', '1.0 >> 25.0', '5.0 >> 40.0', '95.0', '0.05', '3.0; 5.0 >> 3.0; 5.0', 'Unknown >> 600.0; 10.0', 'Unknown >> 3.0; 15.0', 'Unknown >> 3.0; 30.0', '5.0 >> 30.0 >> 30.0', '3.0 >> 5.0', '70.0', '10.0 >> 30.0', '10.0 >> 60.0 >> Unknown', 'Unknown >> 10.0; 20.0', 'Unknown; Unknown; Unknown; 30.0', '2.0; 20.0', '11.0', '45.0 >> 45.0', '1.5; 2.0', '1.3 >> 10.0 >> 8.0', '15.0; 10.0; 60.0', '15.0 >> 5.0', '60.0 >> 90.0 >> 90.0', '3.0; 10.0 >> 3.0; 30.0', '0.0 >> 40.0', '10.0; 5.0; 2.0; 3.0; 50.0', '5.0; 10.0; 5.0', '0.016 >> 5.0', '1.0', '10.0; 20.0; 10.0', '60.0 >> 90.0', '10.0; 50.0', '1.0 >> 10.0', '60.0; 60.0', '15.0; 25.0; 5.0', '600.0 >> Unknown', '60.0; 35.0', '45.0 >> 10.0', '25.0; 60.0', '2.0 >> 2.0 >> 45.0', '1.5 | 20.0', '10.0 >> 0.5', '5.0; 15.0', '10.0 >> 15.0; 30.0', '30.0 >> 60.0', '10.0; 2.0', 'Unknown >> Unknown >> 15.0 >> 15.0', '15.0 >> 60.0', '0.05; 30.0', '10.0 >> Unknown >> Unknown', 'Unknown >> 15.0', '15.0 >> 4.0', '15.0; 15.0; 15.0; 15.0', '5.0; 30.0', 'Unknown >> 150.0', '0.5 >> 40.0', '3.0 >> 120.0', 'Unknown >> 320.0', '240.0', '5.0; 5.0', '10.0; 10.0; 10.0; 10.0; 10.0; 50.0', '5.0 >> 10.0 >> 10.0', 'Unknown >> 10.0; 40.0', '10.0 >> 30.0 >> 30.0', '10.0; 85.0; 10.0 >> Unknown', '15.0; Unknown', 'Unknown >> Unknown', 'Unknown >> 6.0 >> Unknown', '160.0; 17.0', '15.0; 3.0', '0.5; 30.0', '15.0 | Unknown', '2.0; 60.0', '2.0; 3.0', '10.0 >> 5.0', '20.0 >> 15.0 >> 1.0', '5.0 | Unknown | Unknown | 60.0', 'Unknown >> 240.0', '15.0; 30.0', 'Unknown >> 5.0 >> 100.0', '5.0; 5.0; 30.0', 'Unknown >> 30.0 >> 30.0', '1.0 >> 1.0 >> 1.0 >> 2.0', '3.0; 30.0', '60.0 >> 120.0', '1.0; 15.0', '1.0; 10.0 >> Unknown', '15.0 >> Unknown', '30.0 >> 60.0 >> Unknown', '10.0 >> 2.0', 'Unknown >> 6.0', '9.0', '1.0; 4.0', '50.0 >> 5.0', '30.0 >> 2.0', '1.0; 80.0', 'Unknown >> 2.0 >> 2.0', '10.0; 1.0', '0.5; 30.0 >> 0.5', '30.0 >> 30.0; 0.0', '8.0', '10.0; 10.0 >> 90.0', '2.0; 25.0', '40.0; 10.0; 10.0; 20.0', '5.0 >> 150.0', '60.0 >> 16.0 >> Unknown >> 60.0', '13.0', '0.0 >> 30.0', '0.33 >> 20.0', '1.0; 1.0', '30.0 >> 480.0', '3.0 | 5.0 | 5.0', 'Unknown >> 120.0', 'Unknown >> 30.0', '20.0 >> 45.0', '30.0 >> 65.0', '10.0 >> 10.0 >> 60.0', 'Unknown >> 45.0', '20.0', '30.0; 2.0', '15.0; 5.0', '10.0; 10.0 >> 180.0', '60.0 >> 1.0 >> 1.0 >> 15.0', '20.0 >> 120.0', '2.0 >> 540.0', '15.0; 90.0; 15.0', '90.0; 10.0', '15.0 >> 2.0', '30.0; 30.0; 10.0', '40.0 >> 10.0', '0.5 >> 5.0', '25.0 | 30.0', '5.0; 120.0; 100.0; 130.0', '2.0 >> 15.0', '25.0 >> 30.0', '30.0 >> Unknown', '5.0; 2.0', '30.0 >> 5.0', '5.0; 10.0', '20.0 >> 10.0', '4.0; 20.0', '45.0; 50.0', '0.0; 20.0', '3.0; 5.0; 10.0', '60.0 >> 30.0 >> 5.0', 'Unknown; 2.0', '50.0 >> Unknown', '10.0 >> 90.0', '10.0 | 20.0', '14.0', '0.5 >> 30.0', '0.0 >> 30.0 >> 10.0', '10.0 >> 10.0 >> 90.0', '10.0; 10.0 >> 150.0', '50.0 >> 50.0', '90.0 >> 10.0', '30.0 >> 11.5', '20.0; 10.0', '0.5; 0.5', '360.0 >> 30.0', '5.0 >> 25.0', 'Unknown >> 10.0', '3.0; 5.0 >> 10.0', '10.0 | 10.0', '45.0 | 5.0', '30.0; 30.0', '65.0', '20.0 >> 30.0', 'Unknown; 5.0', '20.0 >> Unknown', '150.0', '10.0; 15.0', '1.0; 60.0', '0.0 >> 60.0', '7.0 >> 30.0', 'Unknown >> 420.0', '3.0; 12.0', '45.0 >> 60.0', 'Unknown >> 70.0', 'Unknown >> 5.0', 'Unknown >> 5.0; 60.0', '60.0; 150.0; 15.0', '4.0; 30.0', '30.0; 180.0', 'Unknown >> 80.0', '150.0; 20.0', '0.3; 50.0', '2.0; 5.0', '3.0 >> 40.0', '0.08; 15.0', '30.0 | 30.0', 'Unknown >> Unknown >> Unknown >> 120.0', '10.0; 10.0; 10.0; 30.0', '5.0 >> 65.0', '10.0; 600.0; 90.0', '60.0 >> 60.0', 'Unknown >> 40.0', '10.0; 5.0', '0.0 | 15.0', '150.0; 15.0 >> 30.0', '1.5; 25.0', '0.16; 14.0', '10.0; 10.0 >> Unknown >> 10.0', '5.0; 10.0 >> 5.0; 10.0', '0.3', '10.0; 10.0 >> 60.0', 'Unknown >> 50.0', '0.12', '10.0 >> 60.0', 'Unknown >> 140.0', '5.0; 5.0 >> 5.0; 5.0', '35.0', '20.0; 20.0', '15.0; 60.0', 'Unknown >> Unknown >> 30.0', '120.0 >> 20.0', '5.0 >> 15.0 >> 15.0', '4.0 >> 20.0', '30.0 >> 45.0', '1.0 >> 40.0', '30.0 | 10.0', '30.0 >> 90.0', '10.0 >> 0.17', '30.0; 60.0', '5.0; 15.0 >> 90.0 >> 5.0', '90.0; 5.0', '30.0 >> 30.0 >> 30.0', '0.0 >> 10.0', '30.0 >> 40.0', '2.0; 2.0; 2.0; 60.0', '33.0', '7200.0', '60.0; 10.0', '1.0 >> 7.0', '2.5', '2.0 >> 20.0', '15.0 >> 12.0', 'Unknown >> 1.0; 20.0', 'Unknown >> 10.0 >> 15.0', '15.0; 10.0', '0.25; 5.0', '10.0 >> 1.0 >> 30.0', 'Unknown | 30.0', '2.0 | 20.0', 'Unknown >> Unknown >> 10.0', '20.0 | 20.0', '10.0 >> 150.0', 'Unknown >> 600.0', '5.0; 5.0; 5.0; 30.0', '10.0 >> 50.0', '181.0 >> 30.0', '0.5; 10.0', '60.0 >> 15.0 >> 10.0', '23.0', '30.0 >> Unknown >> Unknown', '15.0; Unknown >> 15.0', '10.0 | 60.0', '5.0; 2.0; 3.0; 50.0', '0.25', '2.0 >> 10.0', '15.0 >> 120.0', '10.0; 10.0 >> 5.0', '1.0 >> 3.0', '10.0 >> 1.0', '5.0; Unknown >> Unknown >> 90.0', '30.0 | Unknown', '25.0', '30.0; 150.0', '1.3 >> 10.0 >> 10.0', '5.0 >> 1.0', '1.0 | 20.0', '15.0 >> 20.0', 'Unknown >> 0.5', '10.0 >> 5.0 >> Unknown', '15.0 >> 6.0', '1.0 >> 120.0', '80.0 >> 250.0', '0.0 >> 20.0', 'Unknown >> 35.0', '1.0 >> 20.0', '40.0', '1.0 >> 70.0', '20.0; 40.0', '30.0 | 20.0', '2.0 >> 25.0', '5.0 >> 0.0', '120.0 >> 60.0', '144.0', 'Unknown >> Unknown >> 120.0', '2.0; 10.0', 'Unknown >> Unknown; Unknown', 'Unknown >> Unknown >> 150.0', 'Unknown | 20.0', '0.08; 30.0', 'Unknown >> Unknown >> 180.0', '10.0 >> 1.7', '0.33 >> 10.0', '10.0 >> 8.0', '10.0; 20.0; 5.0; 30.0', '2.0 >> 5.0', '75.0', 'Unknown >> 60.0', '30.0 >> 50.0; 30.0', '60.0 >> 30.0', '250.0 >> 30.0', '60.0 >> 20.0', '50.0 >> 20.0', '20.0 >> 120.0; 2.0', '480.0', '90.0; 70.0; 45.0', '60.0 >> 15.0', '3.0; 5.0; 10.0 >> Unknown', '30.0 >> 15.0', '2.0 >> 390.0', '60.0; 90.0', '25.0 >> 25.0', '10.0; 30.0', '75.0; 15.0 >> 5.0', '15.0 >> 0.0', '11.0 >> 30.0', '30.0 >> 150.0', '720.0 >> 15.0', 'Unknown; 0.5; 3.0', '30.0; Unknown', '15.0 >> 15.0', '31.0 >> 30.0', '10.0 >> 10.0 >> 5.0', '10.0; 420.0; 90.0', '50.0; 30.0', '20.0 >> 20.0', '60.0; 2880.0', '45.0 >> 10.0; 30.0', '10.0 >> Unknown', '5.0 >> 60.0', '5.0; 5.0 | 5.0; 5.0', '60.0', '5.0', '0.6', '45.0; 70.0', '7.0', '120.0 >> Unknown', '70.0 >> Unknown', '0.07 >> 0.07', '30.0; 30.0; 30.0', '3.0; 60.0', '3.0; 5.0', '122.0', '60.0 >> 10.0 >> 10.0', '5.0 >> 390.0', 'Unknown >> 180.0', 'Unknown >> 100.0', '15.0 >> 600.0', '20.0; 20.0; 20.0; 40.0', '1.5', 'Unknown >> 75.0', '3.0; 2.0', '3.0 >> Unknown', '2.0', 'Unknown >> 10.0; 10.0; 10.0; 10.0; 40.0', '5.0 >> 10.0', '10.0; 10.0; 50.0', '20.0; 5.0', '10.0 >> 10.0 >> 180.0', '1.0; 8.0', '10.0 >> Unknown >> Unknown >> Unknown', '10.0 >> 80.0', '5.0 >> 5.0; 80.0', '10.0 >> 75.0', '5.0 >> 30.0', '0.66', '5.0 >> 20.0', '4.0', '120.0; 20.0', 'Unknown >> 0.333333333', '121.0', '1.0 | Unknown', '12.0 >> 60.0', '5.0 >> 5.0; 10.0; 10.0', '180.0 >> 30.0', '60.0 >> 5.0 >> Unknown', '10.0; 4.0', '30.0; 90.0', '100.0; 20.0', '15.0 >> 30.0', '6.0 >> 30.0', '10.0 | 1.4', '60.0; 25.0', '600.0', '12.0', '5.0 >> 2.0', 'Unknown | 120.0', '5.0; 5.0 | Unknown', 'Unknown >> 20.0', '16.0 >> 30.0', '100.0', 'Unknown >> 5.0 >> 20.0', '105.0', '10.0 >> 10.0 >> 10.0', '2.0 >> Unknown', '15.0 >> 45.0', '13.0 >> 60.0', '720.0', '10.0 >> 10.0', 'Unknown >> 45.0 >> Unknown', '30.0; Unknown >> 30.0', '10.0; 10.0 >> 120.0', '3.0; 10.0', '3.0; 5.0 >> 30.0', 'Unknown >> Unknown >> 90.0', 'Unknown; Unknown', '10.0 >> 15.0', '20.0 >> 30.0 >> Unknown', '100.0 >> 2.0', '5.0 >> 10.0; 10.0', '15.0; 0.17 >> 4.0', '0.5', '0.3; 2.0', '10.0 >> Unknown >> Unknown >> Unknown >> Unknown', '2.0; 5.0 >> Unknown', 'Unknown >> 5.0; 5.0; 5.0', '0.83; 0.83', '2.0 >> 60.0', '3.0 >> 5.0 >> 5.0', '1.0; 2.0 >> Unknown', '60.0 >> 5.0', 'Unknown >> Unknown >> 5.0', '5.0; 2.0; 5.0', '5.0; 5.0 >> 5.0', '10.0 >> 0.0 >> 0.0 >> 0.0 >> 0.0 >> 0.0 >> 0.0 >> 0.0 >> 0.0 >> 0.0', '90.0; 15.0', 'Unknown >> Unknown >> Unknown >> 1.0', '200.0', '5.0 >> 150.0 >> 20.0', '20.0 >> 5.0', 'Unknown; 10.0', '10.0; 20.0; 0.0', '10.0 >> 20.0; 60.0', '15.0; 15.0; 90.0', '1.2', '30.0; 60.0 >> 60.0', '15.0 | 60.0', '3.0; 50.0', '60.0; 1440.0', '3.0', '1.0 >> 2.0', '10.0; 90.0', '5.0; Unknown >> Unknown >> 10.0', 'Unknown', '10.0 | 30.0', '10.0 >> 40.0', 'Unknown >> 260.0', '2.0 >> 100.0', 'Unknown >> 0.0', '0.16 >> 15.0', '60.0; 720.0', '5.0; 60.0', '60.0; 10.0 >> 5.0; 10.0', '2.0; 6.0 >> 8.0', '10.0 >> 4.0', '1.0 | 10.0', '10.0 | 120.0', '1.0; 7.0', '15.0 >> 150.0', 'Unknown >> Unknown >> Unknown >> 20.0', '7.0; 1.0 >> 10.0', '45.0; 45.0', 'Unknown >> 10.0 >> 10.0', 'Unknown >> 40.0; 100.0; 130.0', '5.0; Unknown >> Unknown >> 30.0', '2.0 >> 0.17', '60.0; 15.0', '15.0; 15.0 >> 15.0', '10.0; 10.0; 0.0', '30.0 >> 30.0', '30.0; 150.0; 15.0', '15.0; 15.0', '20.0; 30.0', '2.0; 30.0 >> 2.0; 30.0', '10.0; 45.0', '1.0 >> 30.0', '0.17; 12.0', '4.0 >> 4.0', '15.0 >> 30.0 >> 10.0', '0.17; 75.0', '38.0', '120.0 >> 1.0 >> 1.0 >> 15.0', '10.0 >> 10.0 >> Unknown', '30.0 >> 10.0 >> 10.0 >> 6.0', '270.0', '0.33; 2.0', 'Unknown >> 10.0; 60.0', '15.0; 90.0; 60.0', 'Unknown >> 4.0', '5.0; 30.0; 5.0; 30.0', '3.0 >> 30.0', '4.0; 10.0', '3.0; 5.0 >> 15.0 >> Unknown', '10.0 >> 20.0', '15.0; 15.0; 120.0; 15.0', '10.0 >> 110.0', '4.0 >> 45.0', '55.0', '1.0 | 15.0', '10.0; 60.0; 90.0', '60.0; 30.0', '10.0 >> 3.0', '1.3 >> 10.0', '50.0 | 10.0 >> 10.0', '0.33 >> 15.0', 'Unknown >> 360.0; 10.0', '6.0', '30.0; 20.0', '5.0; 60.0; 10.0', '30.0 >> 18.5', 'Unknown >> 12.0', '30.0; 30.0 >> 30.0', '60.0 >> 10.0', '10.0 >> 10.0 >> 120.0', '30.0 >> 120.0', '3.0 >> 10.0', '15.0 >> 90.0', '30.0 >> 20.0', '3.0 >> 2.0; 20.0', '15.0 >> 10.0', '5.0 | 12.0', '5.0 | 60.0', '30.0 >> 0.0 >> 120.0', '2.0; 2.0', 'Unknown; 20.0 >> 20.0', '3.0; 6.0 >> 10.0', '0.33; 10.0', 'Unknown >> 0.8541666666666666', '2.0; 15.0', '1.0 >> 1.0 >> 2.0', '1.0 >> 15.0', '15.0', '1.0 >> 60.0', '10.0 >> 10.0; 15.0', '45.0 >> 30.0', '30.0 >> 1.0', 'Unknown | 10.0', '0.58 >> 5.0', 'Unknown >> 2.0 >> 3.0', '45.0 >> Unknown', '300.0', '40.0; 100.0 >> 100.0', 'Unknown >> 60.0 >> Unknown', '2.0; 6.0', '120.0 >> 20.0 >> 5.0', '10.0; 20.0; 20.0; 20.0', '20.0 >> 15.0', '15.0; Unknown >> 25.0 >> Unknown', '120.0', '0.5; 60.0', '0.4305555555555556', '20.0; 20.0; 20.0', 'Unknown >> Unknown >> 15.0', 'Unknown >> 10.0; 10.0; 10.0', '5.0; 10.0 >> 30.0', '40.0 >> 120.0', '0.5; 15.0', '1.0; 3.0', '12.0; 10.0', '5.0; Unknown >> Unknown >> 60.0', '2.0; 5.0; 10.0', '2.0 | Unknown', '0.17', '110.0', '5.0 >> 12.0', '20.0 | 15.0', '1.0; 5.0', '120.0 >> Unknown >> Unknown', '1.0; 10.0', '10.0 >> 10.0 >> 240.0', 'Unknown; Unknown >> 30.0', '10.0 >> 10.0; 20.0', '2.0 >> 2.0', '5.0; 0.0', 'Unknown >> 10.0; 120.0', '1.0 >> 16.0', '5.0 >> 95.0', '15.0; 120.0; 15.0', '10.0 >> 0.0', '15.0 >> 10.0 >> 10.0', 'Unknown >> 200.0', '5.0 >> 312.0', 'Unknown >> 105.0', '3.0 | 10.0', '3.0 >> 5.0 >> 90.0', '2.0; 4.0', '50.0; 5.0 >> 5.0', 'Unknown >> 10.0 >> 60.0', '0.1', '10.0; 300.0; 90.0', '15.0; 15.0; 90.0; 10.0', '15.0 | 15.0', '3.0; 5.0; 60.0', '2.0 >> 45.0', '0.13', '2.0 >> 30.0', 'Unknown >> 1.0', '7.0 >> 1.0', '15.0; 45.0', '2.0 >> 120.0', '40.0 >> 40.0', '10.0 >> 10.0 >> 10.0 >> 10.0', '10.0', '10.0; 40.0', '10.0; 10.0; 10.0; 10.0; 40.0', 'Unknown >> 18.0', '5.0 >> 15.0', '5.0 >> 780.0', '30.0; 15.0', 'Unknown >> 2.0', '6.0; 10.0', '3.0; 5.0 >> 15.0', '0.5; 20.0', '0.5; 5.0', '2.0 >> 240.0', '15.0; 0.05 >> 4.0', '210.0', '10.0; 10.0; 10.0', 'Unknown >> 7.0', '0.5 >> 5.0 | 5.0', '15.0; 20.0', '120.0 >> 10.0', '30.0 >> 600.0', '150.0; 15.0', 'Unknown >> 8.0', '10.0; 5.0; Unknown >> 5.0', '40.0; 120.0; 100.0; 130.0', '1.0; 9.0', 'Unknown >> 15.0 >> Unknown', '1.0; 25.0', '10.0 >> 120.0', '1.45; 60.0', '40.0 >> Unknown', '15.0; 60.0 >> 5.0', '10.0; 150.0; 90.0', '5.0 | 10.0', '5.0; 30.0; 2.0', '30.0; 3.0 >> 15.0', 'Unknown | 5.0', '1.0; 20.0', '2.0 >> 4.0', 'Unknown >> 30.0; 30.0', '24.0', '5.0 >> 5.0', '0.5; 2.0', '30.0 >> 30.0; 30.0', '30.0; 80.0', '30.0 >> 30.0; 5.0', '4320.0', '10.0 >> 1.0 >> 10.0', '8.0; 5.0', 'Unknown >> 65.0', '100.0; 10.0', '30.0', '40.0; 10.0', '2.0; 58.0', '2.0 >> 5.0; 60.0', 'Unknown >> 3.0', '1.0 >> 5.0', '16.0 >> 10.0', 'Unknown >> 10.0; 100.0', '1.6', '15.0 >> Unknown >> Unknown', '360.0', '60.0; 20.0', '10.0; 10.0', 'Unknown >> 10.4', '10.0; 10.0; 10.0; 10.0; 10.0; 10.0', 'Unknown >> 1.0 >> 1.0 >> 15.0', '3.0; 10.0 >> 0.25', '10.0; 30.0; 90.0', '600.0 >> 5.0', '30.0 | 5.0', '1.0; 2.0 >> 2.0; 4.0', '20.0 >> 60.0', '0.25; 60.0', '1440.0', '4.0 >> 15.0', '5.0 >> 5.0 | Unknown', '5.0; 5.0; 5.0; 10.0; 10.0; 10.0; 10.0; 90.0', '30.0 | Unknown | 150.0', '5.0 >> Unknown', '4.0; 60.0', '140.0', '120.0; 10.0', '3.0; 7.0', '80.0', '40.0 >> 30.0', '120.0 >> 120.0', 'Unknown >> 15.0 >> 10.0', '5.0 >> 15.0; 75.0', '11.0 >> 60.0', '5.0 >> 45.0', '3.0; 5.0 >> 5.0', '15.0; 0.08 >> 4.0', '60.0 >> 5.0 >> 5.0', '50.0 | 10.0', '10.0 >> 10.0; 60.0', '10.0; 60.0', '1.0; 30.0', '0.08; 20.0', 'Unknown >> Unknown >> 1.0', '60.0; 60.0; 60.0', '30.0 >> 10.0', '180.0; 17.0', '60.0 >> Unknown'])))

    thermal_annealing_atmosphere = Quantity(
        type=str,
        shape=[],
        description="""
    The atmosphere in which the thermal annealing is conducted.
- When more than one reaction step, separate the atmospheres associated to each annealing step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- The number and order of deposition steps must line up with the previous columns.
- If the atmosphere is a mixture of different gases, i.e. A and B, list the gases in alphabetic order and separate them with semicolons, as in (A; B)
- “Dry air” represent air with low relative humidity but where the relative humidity is not known
- “Ambient” represent air where the relative humidity is not known. For ambient conditions where the relative humidity is known, state this as “Air”
- “Vacuum” (of unspecified pressure) is for this purpose considered as an atmospheric gas.
- This is often the same as the atmosphere under which the deposition is occurring, but not always.
- This category was included after the projects initial phase wherefor the list of reported categories is
short. Thus, be prepared to expand the given list of alternatives in the data template.
Example
N2
Air >> N2
Ar
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['N2', 'Unknown >> O2', 'Vacuum; N2', 'Air >> Air | Air', 'Air >> N2', 'N2 >> N2 >> N2 >> N2 >> N2 >> N2 >> N2 >> N2 >> N2 >> N2', 'Dry air >> Air', 'Unknown', 'N2 >> Vacuum', 'Vacuum; Unknown; Unknown', 'N2 >> N2', 'N2 | N2', 'N2; Air', 'Unknown >> Air', 'Dry air >> Dry air', 'Ambient', 'Unknown >> Unknown', 'Ar >> Ar', 'Unknown >> N2', 'Dry air', 'N2 >> N2 >> N2 >> N2 >> N2 >> N2 >> N2 >> N2 >> N2', 'Vacuum >> N2', 'Air', 'Unknown | 70', 'Vacuum', 'Ar >> Vacuum', 'Unknown >> Air >> Air', 'N2; Ambient', 'Air >> Air', 'Ar', 'N2 >> Air'])))

    thermal_annealing_relative_humidity = Quantity(
        type=str,
        shape=[],
        description="""
    The relative humidity during the thermal annealing
- If there is more than one annealing step involved, list the associate relative humidity in the surrounding atmosphere and separate them by a double forward angel bracket (‘ >> ‘)
- The number and order of annealing steps must line up with the previous column
- If there are uncertainties, only state the best estimate, e.g. write 35 and not 20-50.
- If a humidity is not known, stat that as ‘nan’
Example
0
35 >> 0
nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', '0 >> 0', '15', '0; 60', '32', '50.0', '30; 50', '0; 0', '60.0', '43', '0.9', '45', '20 >> 20', '60', '30', '90', '65.0', '0 | 0', '0 >> 25', '50', '10'])))

    thermal_annealing_pressure = Quantity(
        type=str,
        shape=[],
        description="""
    The atmospheric pressure during the thermal annealing
- If there is more than one annealing step involved, list the associate atmospheric pressures and separate them by a double forward angel bracket (‘ >> ‘)
- The number and order of annealing steps must line up with the previous column
- Pressures can be stated in different units suited for different situations. Therefore, specify the unit. The preferred units are:
o atm, bar, mbar, mmHg, Pa, torr, psi
- If a pressure is not known, stat that as ‘nan’
- For values with uncertainties, state the best estimate, e.g. write 100 pa and not 80-120 pa.
Example
1 atm
1 atm >> 0.002 torr
1 atm >> 1 atm >> nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', '0.1 Torr >> 1 Torr', '0.1 Torr', '1 atm >> 1 atm', ' Vacuum >> 1 atm', '1 bar', '1 atm; 0.2 bar', '1 atm | 1 atm', '50 Pa; nan; nan', '1 atm', '0.001 bar', '1 atm >> 1 atm | 1 atm', 'nan >> 700 Pa'])))

    solvent_annealing = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if there has been a separate solvent annealing step, i.e. a step where the perovskite has been annealing in an atmosphere with a significant amount of solvents. This step should also be included deposition procedure sequence but is also stated separately here to simplify downstream filtering.
                    """,
        a_eln=dict(
            component='BoolEditQuantity'))

    solvent_annealing_timing = Quantity(
        type=str,
        shape=[],
        description="""
    The timing of the solvent annealing with respect to the thermal annealing step under which the perovskite is formed. There are three options.
- The solvent annealing is conducted before the perovskite is formed.
- The solvent annealing is conducted under the same annealing step in which the perovskite is formed
- The solvent annealing is conducted after the perovskite has formed.
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', 'Under', 'Before', 'After'])))

    solvent_annealing_solvent_atmosphere = Quantity(
        type=str,
        shape=[],
        description="""
    The solvents used in the solvent annealing step
- If the solvent atmosphere is a mixture of different solvents and gases, e.g. A and B, list them in alphabetic order and separate them with semicolonsas in (A; B)
Example
DMSO
DMF
DMF; DMSO
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['H2O', 'DMSO; H2O', 'TBP', 'Acetic acid; Chlorobenzene', 'Pyridine', '4‐fluoroaniline', 'Chlorobenzene; DMSO', 'GBL', 'DMSO; IPA', 'Aminobutanol', 'Methylamin', 'Methanol; Methylamin', 'Unknown', 'Hac', 'Triethylenetetramine', 'Diethylenetriamine', 'Methanol', 'DMF', 'DMF; H2O', 'DMSO', 'Chlorobenzene', 'Chlorobenzene; DMF', 'HCl', 'Thiophene', 'DMF; DMSO', 'Toluene', 'DMF; IPA', 'Benzyl alcohol', 'NMP', 'Ethanol', 'Air', 'Air; DMSO', 'Vacuum', 'CCl4', 'MACl', 'DMSO; NMP', 'IPA', 'Hexane'])))

    solvent_annealing_time = Quantity(
        type=str,
        shape=[],
        description="""
    The extend of the solvent annealing step in minutes
- If the time is not known, state that by ‘nan’
- If the solvent annealing involves a temperature program with multiple temperature stages, list the associated times at each temperature and separate them with a semicolon (e.g. 5; 10)
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['40.0', '90.0', '2.5', '50.0', '10.0', '60.0', '5.0', '120.0', 'Unknown', '180.0', '0.16666666666666666', '80.0', '480.0', '1.5', '0.25', '30.0', '0.3', '2.0', '1.0', '20.0', '0.08333333333333333', '15.0'])))

    solvent_annealing_temperature = Quantity(
        type=str,
        shape=[],
        description="""
    The temperature during the solvent annealing step
- The temperature refers to the temperature of the sample
- If the solvent annealing involves a temperature program with multiple temperature stages, list the associated temperatures and separate them with a semicolon (e.g. 5; 10) and make sure they align with the times in the previous field.
- If the temperature is not known, state that by ‘nan’
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['200', '120.0', 'Unknown', '90.0', '100', '90', '100.0', '20', '110.0', '150.0'])))

    after_treatment_of_formed_perovskite = Quantity(
        type=str,
        shape=[],
        description="""
    Any after treatment of the formed perovskite. Most possible reaction steps should have been entered before this point. This is an extra category for procedures that just does not fit into any of the other categories.
Examples:
Hot isostatic pressing
Magnetic field
UV radiation
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', 'Washed with Ether', 'Ultrasonic vibration treatment', 'Washed with Toluene', 'DABr', 'Post annealing', 'Dipped in Toluene', 'Washed with DMSO', 'Degradation in air under AM 1.5', 'Magnetic field', 'CF4 plasma treatment', 'Deposition Nanocrystals of CsPbI3', 'Deposition Nanocrystals of CsPbBr3', 'Thermal radiation', 'Washed with Ethyl acetate', 'Washed with chloroform and Ether', 'Spin coating GASCN', 'Annealed under pulsed light', 'Vacuum oven annealing', 'Pressed with flat stamp', 'Pulsed light', 'Fast Cooling', 'Washed with IPA', 'Dipped in octadecene >> Washed with cyclohexane', 'TETA vapour treatment', 'Hot isostatic pressing', 'Drying cabine', 'Washed with IPA >> Thermal Annealing', 'Poling', 'Slow cooling', 'Washed with DMF', 'Photonic curing', 'IPA:ACE @ 1:1 washing', 'UV laser radiation', 'Repeated Spin-coating', 'Hot-pressing', 'Dipped in Chlorobenzene', 'Washed with acetylene black (15 mg/ml) solution in chlorobenzene', 'Micro contact inprinting', 'Spin coating@Guanidinium thiocyanate', 'Gas pump treatment', 'Spin coating GASCN; MACl', 'IR radiation', 'DCM:DEE @ 50:50 washing', 'Vaccum drying', 'fs laser polishing >> Washed with IPA >> Spin-coating solution of CsI, FAI, MABr in IPA >> annealed at 100', 'Washed with ACE', 'Degradation in air under dark', 'H2O2 treatment', 'Gradient thermal annealing', 'Soaking in Isopropyl', 'Washed with Acetone', 'Washed with IPA >>  Spin-coating Dichloromethane', 'Annealed under intense laser pulses', 'Graphdiyne passivation treatment', 'Ethylacetate washing', 'Cold-roll pressing', 'IPFB immersion', 'Washed with GBL', 'Dipped in Ethyl acetate', 'Ultrasonic transducer', 'Atmospheric-pressure dielectric barrier discharge', 'Washed with IPA >> Drying in flow of N2', 'Washed with Anisole', 'Dissolving polystyren template in toluene', 'Spin-coating Ethanol', 'Cold isostatic pressing', 'Pressed with dotted stamp', 'Washed with IPA >> Washed with Dichloromethane', 'Annealed in a perfluorodecalin bath', 'Intense pulsed light annealing', 'Inverted thermal annealing', 'Washed with MABr solution in IPA', 'Exposed to moist air', 'Dried by N2 gas', 'Intense light', 'FABr treatment >> Rinse with 2-propanol >> Thermal annealing >> Slow cooling', 'Washed with MAI solution in IPA', 'Dried under flow of N2', 'Spin coating GABr   >>   annealing', 'Toluene washing', 'Refrigerated', 'Ultrapure water spray', 'Moisture', 'Spin-coating iodopentafluorobenzene', 'Radiative thermal annealing', 'Near Infrared radiation', 'Light soaking', 'Vacuum annealing', 'UV radiation', 'Washed with Chlorobenzene', 'Microwave radiation', 'Dipped in FAI containing ethyl acetate solution', 'Heating >> Light exposure', 'Dipped in Anisole', 'Washed with Methyl acetate', 'Annealed under light', 'Spin-coating Pr-ITC; Ph-DTIC', 'Pressed with hexagonal stamp', 'Washed with IPA and drying with pressurized air', 'IR laser radiation', 'Stored at elavated temperature', 'Laser annealing', 'Dried under flow of clean air'])))

    after_treatment_of_formed_perovskite_met = Quantity(
        type=str,
        shape=[],
        description="""
    Connected to the previous field (After treatment of formed perovskite). The label describing the method should be in the previous filed, and the associated metrics in this one. For exampleThe sample is intense gamma radiation at a flux of X under 45 minutes. The “gamma radiation” is the label, and the time and the flux is the metrics. Give the units when you state the metrics
Examples:
40kHz; 5W; 4 min
45 deg. C
30 min
50 W/cm2; 2.38 s
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', '50 min', '50 W/cm2; 2.42 s', 'Colling rate < GHT-3', '40kHz; 5W; 2 min', '40kHz; 10W; 2 min', '10 pulses per sample', '2.5', '40kHz; 10W; 1 min', 'Colling rate < GHT-2', '1', '40kHz; 10W; 3 min', '2.47 s', '5', '105 deg. C', '70 C >> 254 nm', '30% RH; 8 h', '30 min', '100 deg. C', '40kHz; 5W; 1 min', '7s', '30% RH; 12 h', '50 W/cm2; 2.40 s', '50 W/cm2; 2.38 s', '50 W/cm2; 2.50 s', '40kHz; 10W; 4 min', '40kHz; 5W; 3 min', '30% RH; 4 h', '2 min', '85 deg. C in Air 50 % RH', '9s', 'Colling rate < GHT-4', '40kHz; 5W; 4 min', '20 min', '50 W/cm2; 2.45 s', '10s', '10 s', '13s', '45 deg. C', '105 C', '40 mW/cm2', 'Fast cooling in ice 150 >> 0', '80 deg. C; 15 s', '11s', '50 W/cm2; 2.53 s', '50 W/cm2; 2.55 s', '50 W/cm2; 2.47 s', '200 Mpa; 90 deg.C; 60 min', '0.5', '85 deg. C in O2', 'Several hours', 'Fast cooling in air 150 >> 0', '85 deg. C in N2', 'nan >> 100 deg C 5 min', '80W/cm 20.1mm/s', '500W, 30 sec', '200 Mpa;  60 min', 'Spin-coating>> 2 mg/ml>> 100 deg. C>> 10 min', '70 deg. C; 60 min'])))

    def normalize(self, archive, logger):
        add_solar_cell(archive)
        if self.procedure:
            archive.results.properties.optoelectronic.solar_cell.absorber_fabrication = self.procedure.split(' | ')


