# Perovskite Composition Schema
This gives a description to all the data fields in the perovskite composition schema

## Top level fields
### composition_estimation
A categorical description of how the composition is estimated. Standard options include:
- "Estimated from precursor solutions" 
- "Literature value"
- "Estimated from XRD data"
- "Estimated from spectroscopic data" 
- "Theoretical simulation"
- "Hypothetical compound"
- "Other"

### sample_type
A categorical description of the type of sample the data describes. Standard options include: 
- "Polycrystalline film" 
- "Single crystal" 
- "Quantum dots" 
- "Nano rods"
- "Colloidal solution"
- "Other"

### dimensionality
A categorical description of the dimensionality of the perovskite. Standard options include:  
- "0D", 
- "1D", 
- "2D", 
- "3D", 
- "2D/3D", 
- "Unknown",

A common situation is that  the deposition of a 3D perovskite is followed by a surface treatment that converts the topmost layer of the original perovskite into a caping layer of a 2D perovskite. Our recommendation in thta case is to treating this as two different perovskites and generate two different composition files and to describe the sample as a layered structure. <br>
When a 2D phase is intermixed with a 3D phase, our general recommendation is to generate a separate perovsktie composition file for each, or alternatively stat it as a "2D/3D" perovskite but where the overall composition is given by the value in *long_form*.             

### band_gap
The band gap of the perovskite expressed in electron volt. Details of how the band gap is estimated is suggested to be encapsulated in a separate data schema. A floating-point number

## Derived quantities
### long_form
The perovskite composition according to IUPAC recommendations, where standard abbreviations are used for all ions.  A-ions are listed in alphabetic order, followed by the B-ions in alphabetics order, followed by the X-ions in alphabetic order, all with their stochiometric coefficients. For increased clarity, we recommend enclosing all ions whose abbreviations are 3 letters or longer in parentheses. <br>
Example: "Cs<sub>0.05</sub>FA<sub>0.78</sub>MA<sub>0.17</sub>PbBr<sub>0.5</sub>I<sub>2.5</sub>".

### short_form
The *long_form* stripped of the numeric coefficients. This is a useful key for searching and groping perovskite data. Example. "CsFAMAPbBrI".

## Subsections
### ions_a_site
Data for all the ions on the a-site. A list of dictionaries on the form [{key_1: value_1, key_2: value_2, ...}, {key_1: value_1,  ...}, ...]. Each element in the list represents one A-site ion in the perovskite structure. Descriptions of the data fields are given under "perovskite_ions_schema"   

### ions_b_site
Data for all the ions on the b-site. Same structure as for the *ions_a_site*

### ions_x_site
Data for all the ions on the x-site. Same structure as for the *ions_a_site*

### additives
Data for all the additives in the perovskite film. An additive is defined as anything that deliberately have been added to the perovskite film but with not is a part of the perovskite crystal structure. A list of dictionaries on the form [{key_1: value_1, key_2: value_2, ...}, {key_1: value_1,  ...}, ...]. Each element in the list represents one additive. Descriptions of the data fields are given under "additives_and_impurities_data_schema"  

### impurities
An impurity is defined as anything that unintentionally is present in the perovskite film. Has the same structure as teh additives. 