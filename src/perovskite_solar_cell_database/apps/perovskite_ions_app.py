import yaml
from nomad.config.models.ui import (
    App,
    Axis,
    Column,
    Dashboard,
    Menu,
    MenuItemHistogram,
    MenuItemTerms,
    SearchQuantities,
)

schemas = [
    '*#perovskite_solar_cell_database.composition.PerovskiteAIon',
    '*#perovskite_solar_cell_database.composition.PerovskiteBIon',
    '*#perovskite_solar_cell_database.composition.PerovskiteXIon',
]
# noqa: E501
perovskite_ions_app = App(
    label='Halide Perovskite Ions Database',
    path='perovskite-ions',
    category='Solar cells',
    description='Search ions used in halide perovskites compunds',
    search_quantities=SearchQuantities(include=schemas),
    columns=[
        Column(quantity='results.material.elements', selected=True),
        Column(
            quantity='results.material.chemical_formula_iupac',
            selected=True,
        ),
        Column(
            quantity='data.iupac_name#perovskite_solar_cell_database.composition.PerovskiteAIon',
            selected=True,
            title='IUPAC Name',
        ),
        Column(
            quantity='data.smiles#perovskite_solar_cell_database.composition.PerovskiteAIon',
            selected=True,
            title='SMILES',
        ),
    ],
    menu=Menu(
        title='Ions Database',
        items=[
            MenuItemTerms(
                quantity='data.abbreviation#perovskite_solar_cell_database.composition.PerovskiteAIon',
                show_input=True,
                title='A cation Abbreviation',
            ),
            MenuItemTerms(
                quantity='data.smiles#perovskite_solar_cell_database.composition.PerovskiteAIon',
                show_input=True,
                title='A cation SMILES',
            ),
            MenuItemTerms(
                quantity='data.iupac_name#perovskite_solar_cell_database.composition.PerovskiteAIon',
                show_input=True,
            ),
            MenuItemHistogram(
                x=Axis(
                    search_quantity='data.pure_substance.molar_mass#perovskite_solar_cell_database.composition.PerovskiteAIon',
                    title='A cation Molar Mass',
                )
            ),
            MenuItemHistogram(x=Axis(search_quantity='results.material.n_elements')),
        ],
    ),
    dashboard=Dashboard.parse_obj(
        yaml.safe_load(
            """
            widgets:
                - type: periodictable
                  scale: linear
                  search_quantity: results.material.elements
                  layout:
                    xxl:
                      minH: 8
                      minW: 12
                      h: 9
                      w: 13
                      y: 0
                      x: 0
                    xl:
                      minH: 8
                      minW: 12
                      h: 9
                      w: 12
                      y: 0
                      x: 0
                    lg:
                      minH: 8
                      minW: 12
                      h: 8
                      w: 12
                      y: 0
                      x: 0
                    md:
                      minH: 8
                      minW: 12
                      h: 8
                      w: 12
                      y: 0
                      x: 0
                    sm:
                      minH: 8
                      minW: 12
                      h: 8
                      w: 12
                      y: 0
                      x: 0
                - type: scatter_plot
                  autorange: true
                  size: 1000
                  markers:
                    color:
                      search_quantity: results.material.topology[0].structural_type
                  y:
                    search_quantity: data.pure_substance.molar_mass#perovskite_solar_cell_database.composition.PerovskiteAIon
                    title: A cation molar mass
                  x:
                    search_quantity: results.material.topology[0].n_atoms
                    title: Number of atoms
                  layout:
                    xxl:
                      minH: 3
                      minW: 3
                      h: 6
                      w: 9
                      y: 0
                      x: 12
                    xl:
                      minH: 3
                      minW: 3
                      h: 9
                      w: 18
                      y: 0
                      x: 12
                    lg:
                      minH: 3
                      minW: 3
                      h: 8
                      w: 12
                      y: 0
                      x: 12
                    md:
                      minH: 3
                      minW: 3
                      h: 8
                      w: 6
                      y: 0
                      x: 12
                    sm:
                      minH: 3
                      minW: 3
                      h: 6
                      w: 9
                      y: 8
                      x: 0
            """
        )
    ),
    filters_locked={
        'results.eln.sections': ['PerovskiteAIon', 'PerovskiteBIon', 'PerovskiteXIon']
    },
)
