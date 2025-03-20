import yaml
from nomad.config.models.ui import (
    App,
    Axis,
    AxisScale,
    Column,
    Dashboard,
    Menu,
    MenuItemHistogram,
    MenuItemTerms,
    MenuSizeEnum,
    ScaleEnum,
    SearchQuantities,
)

schema = 'perovskite_solar_cell_database.schema_packages.tandem.schema.PerovskiteTandemSolarCell'


perovskite_tandem_solar_cell_app = App(
    label='Perovskite Tandem Solar Cell Database',
    path='tandem-solar-cells',
    category='Solar cells',
    description='Search tandem solar cells',
    search_quantities=SearchQuantities(include=[f'*#{schema}']),
    filters_locked={'entry_type': 'PerovskiteTandemSolarCell'},
    columns=[
        Column(quantity='data.reference.DOI_number', selected=True),
        #Column(quantity='data.general.photoabsorber', selected=True),
        Column(quantity='data.general.architecture', selected=True),
        Column(quantity='data.general.number_of_junctions', selected=True),
        Column(quantity='data.general.number_of_terminals', selected=True),
        Column(quantity='results.material.elements', selected=True),
    ],
    menu=Menu(
        title='Tandem Solar Cells',
        items=[
            Menu(
                title='Publication',
                size=MenuSizeEnum.XXL,
                items=[
                    MenuItemTerms(
                        search_quantity=f'data.reference.journal#{schema}',
                        show_input=True,
                        width=6,
                        options=10,
                        title='Journal',
                    ),
                    MenuItemTerms(
                        search_quantity=f'data.reference.DOI_number#{schema}',
                        show_input=True,
                        width=6,
                        options=10,
                        title='DOI',
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.reference.publication_date#{schema}',
                            title='Publication Date',
                        )
                    ),
                ],
            ),
            Menu(
                title='General Device Information',
                size=MenuSizeEnum.MD,
                items=[
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.general.area#{schema}',
                            scale=ScaleEnum.LOG,
                            title='Total area',
                            unit='cm**2',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.POW4,
                        ),
                        title='Total area',
                        show_input=False,
                        nbins=30,
                    ),
                    MenuItemTerms(
                        search_quantity=f'data.general.architecture#{schema}',
                        options=3,
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.general.number_of_terminals#{schema}',
                            scale=ScaleEnum.LOG,
                            title='Number of terminals',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.POW4,
                        ),
                        title='Number of terminals',
                        show_input=False,
                        nbins=10,
                    ),
                ],
            ),
        ],
    ),
)
