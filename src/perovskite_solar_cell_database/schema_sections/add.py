from nomad.datamodel.data import ArchiveSection
from nomad.metainfo import Quantity


class Add(ArchiveSection):
    """
    A section to describe **additional layers** present in the device besides the
    *Substrate*, *ETL*, *Perovskite*, *HTL* and *back contact*.
    """

    lay_front = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if there is a functional layer below the substrate, i.e. on the opposite side of the substrate from with respect to the perovskite.
                    """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    lay_front_function = Quantity(
        type=str,
        shape=[],
        description="""
    The function of the additional layers on the substrate side
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- If a layer has more than one function, e.g. A and B, list the functions in order and separate them with semicolons, as in (A; B)
Example:
A.R.C.
Back reflection
Down conversion
Encapsulation
Light management
Upconversion
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    'Antireflection',
                    'Unknown',
                    'Down conversion',
                    'A.R.C.',
                    'Light management',
                ]
            ),
        ),
    )

    lay_front_stack_sequence = Quantity(
        type=str,
        shape=[],
        description="""
    The stack sequence describing the additional layers on the substrate side
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- If two materials, e.g. A and B, are mixed in one layer, list the materials in alphabetic order and separate them with semicolons, as in (A; B)
- Use common abbreviations when appropriate but spell it out if risk for confusion.
- There are separate filed for doping. Indicate doping with colons. E.g. wither aluminium doped NiO-np as Al:NiO-np
- This category was included after the projects initial phase wherefor the list of reported categories is short. Thus, be prepared to expand the given list of alternatives in the data template.
Example:
MgF2
Au-np
NaYF4:Eu-np
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'ZnSe-QDs',
                    'N-Graphene-QDs',
                    'Ag-np',
                    'Moth eye PDMS',
                    'Polyimide',
                    'PDMS',
                    'Unknown',
                    'NaYF4:Eu-np',
                    'NaF',
                    'Eu(TTA)2(Phen)MAA',
                    'MgF2',
                    'Y2O3:Eu3',
                    'CdSeS-QDs',
                    'Y2O3:Eu3 | Au-np',
                    'Mica',
                    'Eu-complex LDL',
                    'textured antireflective foil',
                    'Phosphor-in-glass',
                    'INVAR',
                    'Mn:CsPbCl3-QDs',
                    'LiF',
                ]
            ),
        ),
    )

    lay_front_thickness_list = Quantity(
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
            component='EnumEditQuantity',
            props=dict(suggestions=['', '90.0', '100.0', '50.0', '80.0']),
        ),
    )

    lay_front_additives_compounds = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[''])),
    )

    lay_front_additives_concentrations = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[''])),
    )

    lay_front_deposition_procedure = Quantity(
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
            props=dict(suggestions=['Evaporation', 'Unknown']),
        ),
    )

    lay_front_deposition_aggregation_state_of_reactants = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_front_deposition_synthesis_atmosphere = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_front_deposition_synthesis_atmosphere_pressure_total = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[''])),
    )

    lay_front_deposition_synthesis_atmosphere_pressure_partial = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[''])),
    )

    lay_front_deposition_synthesis_atmosphere_relative_humidity = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[''])),
    )

    lay_front_deposition_solvents = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_front_deposition_solvents_mixing_ratios = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[''])),
    )

    lay_front_deposition_solvents_supplier = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_front_deposition_solvents_purity = Quantity(
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

    lay_front_deposition_reaction_solutions_compounds = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[''])),
    )

    lay_front_deposition_reaction_solutions_compounds_supplier = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_front_deposition_reaction_solutions_compounds_purity = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_front_deposition_reaction_solutions_concentrations = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[''])),
    )

    lay_front_deposition_reaction_solutions_volumes = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_front_deposition_reaction_solutions_age = Quantity(
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

    lay_front_deposition_reaction_solutions_temperature = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_front_deposition_substrate_temperature = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_front_deposition_thermal_annealing_temperature = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_front_deposition_thermal_annealing_time = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_front_deposition_thermal_annealing_atmosphere = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_front_storage_time_until_next_deposition_step = Quantity(
        type=str,
        shape=[],
        description="""
    The time between the back contact is finalised and the next layer is deposited
- If there are uncertainties, only state the best estimate, e.g. write 35 and not 20-50.
- If this is the last layer in the stack, state this as ‘nan’
                    """,
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_front_storage_atmosphere = Quantity(
        type=str,
        shape=[],
        description="""
    The atmosphere in which the sample with the finalised back contact is stored until the next deposition step or device performance measurement
Example
Air
N2
Vacuum
                    """,
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_front_storage_relative_humidity = Quantity(
        type=str,
        shape=[],
        description="""
    The relive humidity under which the sample with the finalised back contact is stored until the next deposition step or device performance measurement
- If there are uncertainties, only state the best estimate, e.g write 35 and not 20-50.
                    """,
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[''])),
    )

    lay_front_surface_treatment_before_next_deposition_step = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[''])),
    )

    lay_back = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if there is a functional layer above the back contact, i.e. layers deposited after the back contact has been finalised.
                    """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    lay_back_function = Quantity(
        type=str,
        shape=[],
        description="""
    The function of the additional layers on the backcontact side.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- If a layer has more than one function, e.g. A and B, list the functions in order and separate them with semicolons, as in (A; B)
Example:
A.R.C.
Back reflection
Down conversion
Encapsulation
Light management
Upconversion
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=['', 'Upconversion', 'Dielectric mirror', 'Antireflection']
            ),
        ),
    )

    lay_back_stack_sequence = Quantity(
        type=str,
        shape=[],
        description="""
    The stack sequence describing the additional layers on the backcontact side.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- If two materials, e.g. A and B, are mixed in one layer, list the materials in alphabetic order and separate them with semicolons, as in (A; B)
- Use common abbreviations when appropriate but spell it out if risk for confusion.
- There are now separate filed for doping. Indicate doping with colons. E.g. wither aluminium doped NiO-np as Al:NiO-np
- This category was included after the projects initial phase wherefor the list of reported categories is short. Thus, be prepared to expand the given list of alternatives in the data template.
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['MgF2', 'Unknown'])
        ),
    )

    lay_back_thickness_list = Quantity(
        type=str,
        shape=[],
        description="""
    A list of thicknesses of the individual layers in the stack.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- The layers must line up with the previous filed.
- State thicknesses in nm
- Every layer in the stack have a thickness. If it is unknown, state this as ‘nan’
- If there are uncertainties, state the best estimate, e.g write 100 and not 90-110
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', '105.0', '90.0'])
        ),
    )

    lay_back_additives_compounds = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[''])),
    )

    lay_back_additives_concentrations = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[''])),
    )

    lay_back_deposition_procedure = Quantity(
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
            props=dict(suggestions=['Evaporation', 'Unknown']),
        ),
    )

    lay_back_deposition_aggregation_state_of_reactants = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_back_deposition_synthesis_atmosphere = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_back_deposition_synthesis_atmosphere_pressure_total = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[''])),
    )

    lay_back_deposition_synthesis_atmosphere_pressure_partial = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[''])),
    )

    lay_back_deposition_synthesis_atmosphere_relative_humidity = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[''])),
    )

    lay_back_deposition_solvents = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_back_deposition_solvents_mixing_ratios = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[''])),
    )

    lay_back_deposition_solvents_supplier = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_back_deposition_solvents_purity = Quantity(
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

    lay_back_deposition_reaction_solutions_compounds = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[''])),
    )

    lay_back_deposition_reaction_solutions_compounds_supplier = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_back_deposition_reaction_solutions_compounds_purity = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_back_deposition_reaction_solutions_concentrations = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[''])),
    )

    lay_back_deposition_reaction_solutions_volumes = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_back_deposition_reaction_solutions_age = Quantity(
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

    lay_back_deposition_reaction_solutions_temperature = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_back_deposition_substrate_temperature = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_back_deposition_thermal_annealing_temperature = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_back_deposition_thermal_annealing_time = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_back_deposition_thermal_annealing_atmosphere = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_back_storage_time_until_next_deposition_step = Quantity(
        type=str,
        shape=[],
        description="""
    The time between the back contact is finalised and the next layer is deposited
- If there are uncertainties, only state the best estimate, e.g. write 35 and not 20-50.
- If this is the last layer in the stack, state this as ‘nan’
                    """,
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_back_storage_atmosphere = Quantity(
        type=str,
        shape=[],
        description="""
    The atmosphere in which the sample with the finalised back contact is stored until the next deposition step or device performance measurement
Example
Air
N2
Vacuum
                    """,
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=['Unknown'])),
    )

    lay_back_storage_relative_humidity = Quantity(
        type=str,
        shape=[],
        description="""
    The relive humidity under which the sample with the finalised back contact is stored until the next deposition step or device performance measurement
- If there are uncertainties, only state the best estimate, e.g write 35 and not 20-50.
                    """,
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[''])),
    )

    lay_back_surface_treatment_before_next_deposition_step = Quantity(
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
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[''])),
    )
