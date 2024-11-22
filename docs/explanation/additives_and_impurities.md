# Additives and Impurites data schema
This gives a description to all the data fields defined for the additives and the impurities. <br>
An additive is defined as anything that deliberately have been added to the perovskite film but with not is a part of the perovskite crystal structure. <br>
An impurity is defined as anything that unintentionally is present in the perovskite film. <br>
The schema structure is teh same for both additives and impurities

## Top level fields
### abbreviation
The standard abbreviation for when referring to the additive or impurity

### concentration
The concentration of the substance in the perovskite film expressed in number per cm<sup>3</sup> <br>
Concentrations are challenging to work with as there are a number of different possible units. per cm<sup>3</sup> is a natural unit ofr dopants and impurities percent in small amount. In other cases, the preferred way to deal with concentrations is in the form of a mass fraction (see below)

### mass_fraction
The mass fraction of the additive or impurity in the film. If you originally have expressed your concentration as a volume fraction or a mole fraction, the recommended way is to convert it to a mass_fraction as that will work better for downstream data processing and analysis. <br>
Note: the concentration and mass fraction reefers to the amount of materials in the perovskite film, and not the concentration of those substances in precursor solutions. Such concentrations would instead be stated in corresponding synthesis protocols.   

## Subsection for the pure substance (pure_substance)
This subsection provides detailed information about the nature of the additive and the impurity. <br>
This section is linked to pubchem (https://pubchem.ncbi.nlm.nih.gov/). This means that it usually is enough to one key data for the compound, like the smiles, inchi, inchi key, cas-number, iupac name, or the Pubchem ID. If one of those are give. Press the save icon and the rest of the data will be populated from Pubchem if it is in their database. But, please, check that the populated data looks right before you proceed.   

### name
The common or trivial name of the substance

### iupac_name
The preferred systematic IUPAC name of the substance.

### molecular_formula
The molecular formula which indicates the numbers of each type of atom in a molecule, with no information about the structure. <br> 

### molar_mass
The molar mass of the substance

### cas_number
The CAS number for the substance.

### smile
The SMILES string of the substance.

### canonical_smile
The canonical SMILES string of the substance.

### inchi
The inchi of the substance

### inchi_key
The inchi key of hte substance

### pub_chem_id
The database ID for substance in hte Pub chem database

### pub_chem_link
A link to the pub chem entry