import yaml
from nomad.config.models.ui import (
    App,
    Axis,
    Column,
    Dashboard,
    Menu,
    MenuItemHistogram,
    MenuItemPeriodicTable,
    MenuItemTerms,
    SearchQuantities,
)

schemas = [
    '*#perovskite_solar_cell_database.schema.PerovskiteSolarCell',
]
# noqa: E501
perovskite_database_app = App(
    label='The Perovskite Solar Cell Database',
    path='perovskite-solar-cells',
    category='Halide Perovskites',
    description='Search Entries of the Perovskite Solar Cell Database',
    search_quantities=SearchQuantities(include=schemas),
    columns=[
        Column(quantity='entry_create_time', selected=True),
    ],
    # Column(
    #     quantity='results.properties.optoelectronic.solar_cell.efficiency',
    #     selected=True,
    #     format={'decimals': 2, 'mode': 'standard'},
    #     label='Efficiency (%)',
    # ),
    # Column(
    #     quantity='results.properties.optoelectronic.solar_cell.open_circuit_voltage',
    #     selected=True,
    #     format={'decimals': 3, 'mode': 'standard'},
    #     unit='V',
    # ),
    # Column(
    #     quantity='results.properties.optoelectronic.solar_cell.short_circuit_current_density',
    #     selected=True,
    #     format={'decimals': 3, 'mode': 'standard'},
    #     unit='A/m**2',
    # ),
    # Column(
    #     quantity='results.properties.optoelectronic.solar_cell.fill_factor',
    #     selected=True,
    #     format={'decimals': 3, 'mode': 'standard'},
    # ),
    # Column(quantity='references', selected=True),
    # Column(quantity='results.material.chemical_formula_hill', label='Formula'),
    # Column(quantity='results.material.structural_type'),
    # Column(
    #     quantity='results.properties.optoelectronic.solar_cell.illumination_intensity',
    #     format={'decimals': 3, 'mode': 'standard'},
    #     label='Illum. intensity',
    #     unit='W/m**2',
    # ),
    # Column(quantity='results.eln.lab_ids'),
    # Column(quantity='results.eln.sections'),
    # Column(quantity='results.eln.methods'),
    # Column(quantity='results.eln.tags'),
    # Column(quantity='results.eln.instruments'),
    # Column(quantity='entry_name', label='Name'),
    # Column(quantity='entry_type'),
    # Column(quantity='mainfile'),
    # Column(quantity='upload_create_time', label='Upload time'),
    # Column(quantity='authors'),
    # Column(quantity='comment'),
    # Column(quantity='datasets'),
    # Column(quantity='published', label='Access'),
    menu=Menu(
        items=[
            MenuItemTerms(
                quantity='results.material.chemical_formula_hill',
                show_input=False,
            ),
            Menu(
                title='Absorber Material',
                items=[
                    MenuItemTerms(
                        quantity='results.material.chemical_formula_hill',
                        show_input=True,
                    ),
                ],
            ),
        ]
    ),
    # menu=Menu(
    #     items=[
    #         # MenuItemTerms(
    #         #     quantity=f'data.status#{schema_name}',
    #         #     show_input=False,
    #         # ),
    #         Menu(
    #             title='Absorber Material',
    #             items=[
    #                 MenuItemTerms(
    #                     quantity='results.material.chemical_formula_descriptive',
    #                     show_input=True,
    #                 ),
    #                 MenuItemTerms(
    #                     quantity='results.material.chemical_formula_iupac',
    #                     show_input=False,
    #                 ),
    #                 MenuItemHistogram(
    #                     x=Axis(
    #                         search_quantity='results.material.n_atoms',
    #                     )
    #                 ),
    #             ],
    #         ),
    # Menu(
    #     size='xs',
    #     title='',
    #     items=[
    #         MenuItemTerms(
    #             quantity=f'data.parameters.name#{schema_name}',
    #         ),
    #     ],
    # ),
    # Menu(
    #     title='Recommender',
    #     items=[
    #         MenuItemTerms(
    #             search_quantity=f'data.recommender.type#{schema_name}',
    #             show_input=False,
    #         ),
    #         MenuItemTerms(
    #             search_quantity=f'data.recommender.surrogate_model.type#{schema_name}',
    #             show_input=False,
    #         ),
    #         MenuItemTerms(
    #             search_quantity=f'data.recommender.acquisition_function.type#{schema_name}',
    #             show_input=False,
    #             options=1,
    #         ),
    #         MenuItemTerms(
    #             search_quantity=f'data.recommender.hybrid_sampler#{schema_name}',
    #             show_input=False,
    #         ),
    #         MenuItemHistogram(
    #             x=Axis(
    #                 search_quantity=f'data.recommender.sampling_percentage#{schema_name}'
    #             )
    #         ),
    #     ],
    # ),
    #     ]
    # ),
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
            """
        )
    ),
    filters_locked={
        'section_defs.definition_qualified_name': [
            'perovskite_solar_cell_database.schema.PerovskiteSolarCell'
        ]
    },
)
