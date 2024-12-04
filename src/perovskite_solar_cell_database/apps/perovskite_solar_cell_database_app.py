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
    ScaleEnum,
    MenuSizeEnum,
    AxisScale,
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
        Column(
            quantity='results.properties.optoelectronic.solar_cell.efficiency',
            selected=True,
            # format={'decimals': 2, 'mode': 'standard'},
            label='Efficiency (%)',
        ),
        Column(
            quantity='results.properties.optoelectronic.solar_cell.open_circuit_voltage',
            selected=True,
            format={'decimals': 3, 'mode': 'standard'},
            unit='V',
        ),
        Column(
            quantity='results.properties.optoelectronic.solar_cell.short_circuit_current_density',
            selected=True,
            # format={'decimals': 3, 'mode': 'standard'},
            unit='A/m**2',
        ),
        Column(
            quantity='results.properties.optoelectronic.solar_cell.fill_factor',
            selected=True,
            # format={'decimals': 3, 'mode': 'standard'},
        ),
        Column(quantity='references', selected=True),
        Column(quantity='results.material.chemical_formula_hill', label='Formula'),
        Column(quantity='results.material.structural_type'),
        Column(
            quantity='results.properties.optoelectronic.solar_cell.illumination_intensity',
            # format={'decimals': 3, 'mode': 'standard'},
            label='Illum. intensity',
            unit='W/m**2',
        ),
        Column(quantity='results.eln.lab_ids'),
        Column(quantity='results.eln.sections'),
        Column(quantity='results.eln.methods'),
        Column(quantity='results.eln.tags'),
        Column(quantity='results.eln.instruments'),
        Column(quantity='entry_name', label='Name'),
        Column(quantity='entry_type'),
        Column(quantity='mainfile'),
        Column(quantity='upload_create_time', label='Upload time'),
        Column(quantity='authors'),
        Column(quantity='comment'),
        Column(quantity='datasets'),
        Column(quantity='published', label='Access'),
    ],
    menu=Menu(
        items=[
            Menu(
                title='Absorber Material',
                size=MenuSizeEnum.XXL,
                items=[
                    MenuItemPeriodicTable(
                        quantity='results.material.elements',
                        show_input=True,
                    ),
                    MenuItemTerms(
                        search_quantity='results.material.chemical_formula_hill',
                        width=6,
                        options=0,
                    ),
                    MenuItemTerms(
                        search_quantity='results.material.chemical_formula_iupac',
                        width=6,
                        options=0,
                    ),
                    MenuItemTerms(
                        search_quantity='results.material.structural_type',
                        width=6,
                        options=2,
                        scale=ScaleEnum.LOG,
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity='results.properties.electronic.band_structure_electronic.band_gap.value',
                            scale='linear',
                            unit='eV',
                            title='Band gap',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.POW4,
                        ),
                        title='Band gap',
                        width=6,
                        show_input=False,
                        nbins=30,
                    ),
                ],
            ),
            Menu(
                title='Publication',
                size=MenuSizeEnum.XXL,
                items=[
                    MenuItemTerms(
                        search_quantity='data.ref.journal#perovskite_solar_cell_database.schema.PerovskiteSolarCell',
                        show_input=True,
                        width=6,
                        options=10,
                        title='Journal',
                    ),
                    MenuItemTerms(
                        search_quantity='data.ref.DOI_number#perovskite_solar_cell_database.schema.PerovskiteSolarCell',
                        show_input=True,
                        width=6,
                        options=10,
                        title='DOI',
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity='data.ref.publication_date#perovskite_solar_cell_database.schema.PerovskiteSolarCell',
                            title='Publication Date',
                        )
                    ),
                ],
            ),
            Menu(
                title='Transport layers',
                size=MenuSizeEnum.XXL,
                items=[
                    MenuItemTerms(
                        search_quantity='results.properties.optoelectronic.solar_cell.hole_transport_layer',
                        show_input=True,
                        width=6,
                        options=10,
                        title='Hole transport layer',
                    ),
                    MenuItemTerms(
                        search_quantity='results.properties.optoelectronic.solar_cell.electron_transport_layer',
                        show_input=True,
                        width=6,
                        options=10,
                        title='Electron transport layer',
                    ),
                    MenuItemTerms(
                        search_quantity='data.htl.deposition_procedure#perovskite_solar_cell_database.schema.PerovskiteSolarCell',
                        show_input=True,
                        width=6,
                        options=10,
                        title='HTL deposition method',
                    ),
                    MenuItemTerms(
                        search_quantity='data.etl.deposition_procedure#perovskite_solar_cell_database.schema.PerovskiteSolarCell',
                        show_input=True,
                        width=6,
                        options=10,
                        title='ETL deposition method',
                    ),
                ],
            ),
        ]
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
            """
        )
    ),
    filters_locked={
        'section_defs.definition_qualified_name': [
            'perovskite_solar_cell_database.schema.PerovskiteSolarCell'
        ]
    },
)
