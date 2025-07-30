from importlib.resources import files

import yaml
from nomad.config.models.ui import (
    App,
    Axis,
    AxisScale,
    Column,
    Dashboard,
    Menu,
    MenuItemDefinitions,
    MenuItemHistogram,
    MenuItemPeriodicTable,
    MenuItemTerms,
    MenuSizeEnum,
    ScaleEnum,
    SearchQuantities,
)

# Access the YAML file packaged in the module
try:
    yaml_path = files('perovskite_solar_cell_database.apps').joinpath(
        'tandem_dashboard.yaml'
    )
    with yaml_path.open('r') as additional_file:
        widgets = yaml.safe_load(additional_file)
except Exception as e:
    raise RuntimeError(f'Failed to load widgets from YAML file: {e}')


schema = 'perovskite_solar_cell_database.schema_packages.tandem.schema.PerovskiteTandemSolarCell'

tandem_app = App(
    label='The Tandem Solar Cell Database',
    path='tandem-solar-cells-database',
    category='Solar cells',
    description='Search Entries of the Tandem Solar Cell Database',
    readme='Under construction; currently a placeholder for the Tandem Solar Cell Database',
    search_quantities=SearchQuantities(include=[f'*#{schema}']),
    columns=[
        Column(
            title='File Name',
            search_quantity='mainfile',
            selected=True,
        ),
        Column(
            search_quantity='results.material.chemical_formula_descriptive',
            selected=True,
            title='Descriptive formula',
        ),
        Column(
            search_quantity='data.key_performance_metrics.power_conversion_efficiency_stabilized',
            selected=True,
            format={'decimals': 3, 'mode': 'standard'},
        ),
        Column(
            search_quantity='data.key_performance_metrics.power_conversion_efficiency',
            selected=True,
            format={'decimals': 3, 'mode': 'standard'},
        ),
        Column(
            search_quantity='data.key_performance_metrics.short_circuit_current_density',
            selected=True,
            format={'decimals': 3, 'mode': 'standard'},
            # unit='A/m**2',
        ),
        Column(
            search_quantity='data.key_performance_metrics.open_circuit_voltage',
            selected=True,
            format={'decimals': 3, 'mode': 'standard'},
            # unit='V',
        ),
        Column(
            search_quantity='data.key_performance_metrics.fill_factor',
            selected=True,
            format={'decimals': 3, 'mode': 'standard'},
        ),
        Column(search_quantity='references', selected=True),
        Column(
            search_quantity='results.material.chemical_formula_hill', title='Formula'
        ),
        Column(
            search_quantity='data.measurements.jv[*].illumination.intensity',
            format={'decimals': 3, 'mode': 'standard'},
            label='Illum. intensity',
            # unit='W/m**2',
        ),
        Column(search_quantity='results.material.structural_type'),
        Column(search_quantity='results.eln.lab_ids'),
        Column(search_quantity='results.eln.sections'),
        Column(search_quantity='results.eln.methods'),
        Column(search_quantity='results.eln.tags'),
        Column(search_quantity='results.eln.instruments'),
        Column(search_quantity='entry_name', title='Name'),
        Column(search_quantity='entry_type'),
        Column(search_quantity='upload_create_time', title='Upload time'),
        Column(search_quantity='entry_create_time', title='Entry creation time'),
        Column(search_quantity='authors'),
        Column(search_quantity='comment'),
        Column(search_quantity='datasets'),
        Column(search_quantity='published', title='Access'),
    ],
    menu=Menu(
        size=MenuSizeEnum.MD,
        title='Menu',
        items=[
            Menu(
                title='Elements',
                size=MenuSizeEnum.XXL,
                items=[
                    MenuItemPeriodicTable(
                        search_quantity='results.material.elements',
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
                        search_quantity='results.material.chemical_formula_reduced',
                        width=6,
                        options=0,
                    ),
                    MenuItemTerms(
                        search_quantity='results.material.chemical_formula_anonymous',
                        width=6,
                        options=0,
                    ),
                    MenuItemHistogram(
                        x='results.material.n_elements',
                    ),
                ],
            ),
        ],
    ),
    dashboard=Dashboard.model_validate(widgets),
    filters_locked={'entry_type': 'PerovskiteTandemSolarCell'},
)
