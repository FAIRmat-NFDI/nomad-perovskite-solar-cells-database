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
        'perovskite_solar_cell_database_dashboard.yaml'
    )
    with yaml_path.open('r') as additional_file:
        widgets = yaml.safe_load(additional_file)
except Exception as e:
    raise RuntimeError(f'Failed to load widgets from YAML file: {e}')


schema = 'perovskite_solar_cell_database.schema.PerovskiteSolarCell'

perovskite_database_app = App(
    label='The Perovskite Solar Cell Database',
    path='perovskite-solar-cells-database',
    category='Solar cells',
    description='Search entries of the perovskite solar cell database',
    search_quantities=SearchQuantities(include=[f'*#{schema}']),
    columns=[
        Column(
            quantity='results.material.chemical_formula_descriptive',
            selected=True,
            label='Descriptive formula',
        ),
        Column(
            quantity='results.properties.optoelectronic.solar_cell.efficiency',
            selected=True,
            format={'decimals': 2, 'mode': 'standard'},
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
            format={'decimals': 3, 'mode': 'standard'},
            unit='A/m**2',
        ),
        Column(
            quantity='results.properties.optoelectronic.solar_cell.fill_factor',
            selected=True,
            format={'decimals': 3, 'mode': 'standard'},
        ),
        Column(quantity='references', selected=True),
        Column(quantity='results.material.chemical_formula_hill', label='Formula'),
        Column(quantity='results.material.structural_type'),
        Column(
            quantity='results.properties.optoelectronic.solar_cell.illumination_intensity',
            format={'decimals': 3, 'mode': 'standard'},
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
        Column(
            quantity=f'data.ref.extraction_method#{schema}', label='Extraction method'
        ),
    ],
    menu=Menu(
        items=[
            Menu(
                title='Publication',
                size=MenuSizeEnum.XXL,
                items=[
                    MenuItemTerms(
                        search_quantity=f'data.ref.authors.name#{schema}',
                        show_input=True,
                        width=6,
                        options=10,
                        title='Publication Authors',
                    ),
                    MenuItemTerms(
                        search_quantity=f'data.ref.journal#{schema}',
                        show_input=True,
                        width=6,
                        options=10,
                        title='Journal',
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.ref.publication_date#{schema}',
                            title='Publication Date',
                        )
                    ),
                    MenuItemTerms(
                        search_quantity=f'data.ref.extraction_method#{schema}',
                        title='Solar Cell Data Extraction Method',
                        show_input=False,
                        width=6,
                    ),
                    MenuItemTerms(
                        search_quantity=f'data.ref.DOI_number#{schema}',
                        show_input=True,
                        width=6,
                        options=5,
                        title='DOI',
                    ),
                ],
            ),
            Menu(
                title='Perovskite Material',
                size=MenuSizeEnum.XXL,
                items=[
                    MenuItemPeriodicTable(
                        quantity='results.material.elements',
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
                    MenuItemTerms(
                        search_quantity=f'data.perovskite.composition_a_ions#{schema}',
                        width=4,
                        options=10,
                        title='A cations',
                    ),
                    MenuItemTerms(
                        search_quantity=f'data.perovskite.composition_b_ions#{schema}',
                        width=4,
                        options=10,
                        title='B cations',
                    ),
                    MenuItemTerms(
                        search_quantity=f'data.perovskite.composition_c_ions#{schema}',
                        width=4,
                        options=10,
                        title='X anions',
                    ),
                ],
            ),
            Menu(
                title='Perovskite Fabrication',
                size=MenuSizeEnum.SM,
                items=[
                    MenuItemTerms(
                        search_quantity=f'data.perovskite_deposition.procedure#{schema}',
                        options=10,
                    ),
                    MenuItemTerms(
                        search_quantity=f'data.perovskite_deposition.solvents#{schema}',
                        options=10,
                    ),
                    MenuItemTerms(
                        search_quantity=f'data.perovskite.additives_compounds#{schema}',
                        options=10,
                    ),
                ],
            ),
            Menu(
                title='Device Architecture',
                size=MenuSizeEnum.MD,
                items=[
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.cell.area_total#{schema}',
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
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity='data.cell.area_measured#perovskite_solar_cell_database.schema.PerovskiteSolarCell',
                            scale=ScaleEnum.LOG,
                            title='Measured area',
                            unit='cm**2',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.POW4,
                        ),
                        title='Measured area',
                        show_input=False,
                        nbins=30,
                    ),
                    MenuItemTerms(
                        search_quantity='results.properties.optoelectronic.solar_cell.device_stack',
                        options=10,
                    ),
                    MenuItemTerms(
                        search_quantity=f'data.cell.architecture#{schema}',
                        options=3,
                    ),
                ],
            ),
            Menu(
                title='Transport Layers',
                size=MenuSizeEnum.XXL,
                items=[
                    MenuItemTerms(
                        search_quantity='results.properties.optoelectronic.solar_cell.hole_transport_layer',
                        show_input=True,
                        width=6,
                        options=10,
                        title='Hole transport layer (HTL)',
                    ),
                    MenuItemTerms(
                        search_quantity='results.properties.optoelectronic.solar_cell.electron_transport_layer',
                        show_input=True,
                        width=6,
                        options=10,
                        title='Electron transport layer (ETL)',
                    ),
                    MenuItemTerms(
                        search_quantity=f'data.htl.deposition_procedure#{schema}',
                        show_input=True,
                        width=6,
                        options=10,
                        title='HTL deposition method',
                    ),
                    MenuItemTerms(
                        search_quantity=f'data.etl.deposition_procedure#{schema}',
                        show_input=True,
                        width=6,
                        options=10,
                        title='ETL deposition method',
                    ),
                ],
            ),
            Menu(
                title='Solar Cell Performance',
                size=MenuSizeEnum.XXL,
                items=[
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity='results.properties.optoelectronic.solar_cell.efficiency',
                            title='Efficiency (%)',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.LINEAR,
                        ),
                        title='Efficiency',
                        width=6,
                        show_input=True,
                        nbins=30,
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity='results.properties.optoelectronic.solar_cell.open_circuit_voltage',
                            scale=ScaleEnum.LINEAR,
                            title='Voc',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.LINEAR,
                        ),
                        title='Voc',
                        width=6,
                        show_input=True,
                        nbins=30,
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity='results.properties.optoelectronic.solar_cell.short_circuit_current_density',
                            title='Jsc',
                            unit='mA/cm**2',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.LINEAR,
                        ),
                        title='Jsc',
                        width=6,
                        show_input=True,
                        nbins=30,
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity='results.properties.optoelectronic.solar_cell.fill_factor',
                            scale=ScaleEnum.LINEAR,
                            title='Fill factor',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.LINEAR,
                        ),
                        title='Fill factor',
                        width=6,
                        show_input=True,
                        nbins=30,
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity='results.properties.optoelectronic.solar_cell.illumination_intensity',
                            scale=ScaleEnum.LINEAR,
                            title='Illumination intensity',
                            unit='mW/cm^2',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.LINEAR,
                        ),
                        title='Illumination intensity',
                        width=6,
                        show_input=True,
                        nbins=30,
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.eqe.integrated_Jsc#{schema}',
                            scale=ScaleEnum.LINEAR,
                            title='Integrated Jsc (EQE)',
                            unit='mA/cm**2',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.LINEAR,
                        ),
                        title='Integrated Jsc (EQE)',
                        width=6,
                        show_input=True,
                        nbins=30,
                    ),
                ],
            ),
            Menu(
                title='Stability',
                size=MenuSizeEnum.MD,
                items=[
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.stability.PCE_T80#{schema}',
                            title='PCE T80',
                            unit='hour',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.LINEAR,
                        ),
                        title='PCE T80',
                        show_input=True,
                        nbins=30,
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.stability.PCE_T95#{schema}',
                            title='PCE T95',
                            unit='hour',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.LINEAR,
                        ),
                        title='PCE T95',
                        show_input=True,
                        nbins=30,
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.stability.PCE_initial_value#{schema}',
                            scale=ScaleEnum.LINEAR,
                            title='PCE initial value',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.LINEAR,
                        ),
                        title='PCE initial value',
                        show_input=True,
                        nbins=30,
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.stability.PCE_end_of_experiment#{schema}',
                            title='PCE end of experiment',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.LINEAR,
                        ),
                        title='PCE end of experiment',
                        show_input=True,
                        nbins=30,
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.stabilised.performance_measurement_time#{schema}',
                            scale=ScaleEnum.LOG,
                            title='Stabilized performance measurement time',
                            unit='hour',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.LINEAR,
                        ),
                        title='Stabilized performance measurement time',
                        show_input=True,
                        nbins=30,
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.stability.PCE_after_1000_h#{schema}',
                            scale=ScaleEnum.LINEAR,
                            title='PCE after 1000 h',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.LINEAR,
                        ),
                        title='PCE after 1000 h',
                        show_input=True,
                        nbins=30,
                    ),
                    MenuItemDefinitions(show_header=False),
                ],
            ),
        ]
    ),
    dashboard=Dashboard.parse_obj(widgets),
    filters_locked={'section_defs.definition_qualified_name': [f'{schema}']},
)
