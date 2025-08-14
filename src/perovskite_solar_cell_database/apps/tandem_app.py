from importlib.resources import files

import yaml
from nomad.config.models.ui import (
    App,
    Axis,
    AxisScale,
    Column,
    Dashboard,
    Menu,
    MenuItemHistogram,
    MenuItemOption,
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
    raise RuntimeError(f'Failed to load widgets from YAML file: {e}') from e


schema = 'perovskite_solar_cell_database.schema_packages.tandem.schema.PerovskiteTandemSolarCell'

tandem_app = App(
    label='The Tandem Solar Cell Database',
    path='tandem-solar-cells-database',
    category='Solar cells',
    description='Search Entries of the Tandem Solar Cell Database',
    readme='Search Entries of the Tandem Solar Cell Database',
    search_quantities=SearchQuantities(include=[f'*#{schema}']),
    columns=[
        Column(
            title='File Name',
            search_quantity='mainfile',
        ),
        Column(
            search_quantity='results.material.chemical_formula_descriptive',
            selected=True,
            title='Descriptive formula',
        ),
        Column(
            search_quantity=f'data.key_performance_metrics.power_conversion_efficiency#{schema}',
            selected=True,
            format={'decimals': 3, 'mode': 'standard'},
            label='Power conversion efficiency (%)',
        ),
        Column(
            search_quantity=f'data.key_performance_metrics.short_circuit_current_density#{schema}',
            selected=True,
            format={'decimals': 3, 'mode': 'standard'},
            unit='A/m**2',
        ),
        Column(
            search_quantity=f'data.key_performance_metrics.open_circuit_voltage#{schema}',
            selected=True,
            format={'decimals': 3, 'mode': 'standard'},
            unit='V',
        ),
        Column(
            search_quantity=f'data.key_performance_metrics.fill_factor#{schema}',
            selected=True,
            format={'decimals': 3, 'mode': 'standard'},
        ),
        Column(
            search_quantity=f'data.key_performance_metrics.power_conversion_efficiency_stabilized#{schema}',
            selected=True,
            format={'decimals': 3, 'mode': 'standard'},
            label='Power conversion efficiency stabilized (%)',
        ),
        Column(search_quantity='references', selected=True),
        Column(
            search_quantity="results.material.topology[?parent_system=='results/material/topology/0'].chemical_formula_hill",
            title='Formula - photoabsorbers',
        ),
        Column(
            search_quantity=f'data.measurements.jv[*].illumination.intensity#{schema}',
            format={'decimals': 3, 'mode': 'standard'},
            label='Illum. intensity',
            unit='W/m**2',
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
        Column(search_quantity='authors', title='Upload authors'),
        Column(search_quantity='comment'),
        Column(search_quantity='datasets'),
        Column(search_quantity='published', title='Access'),
    ],
    menu=Menu(
        size=MenuSizeEnum.MD,
        title='Menu',
        items=[
            Menu(
                title='Publication',
                size=MenuSizeEnum.XXL,
                items=[
                    MenuItemTerms(
                        search_quantity=f'data.reference.authors.name#{schema}',
                        show_input=True,
                        width=6,
                        options=10,
                        title='Publication Authors',
                    ),
                    MenuItemTerms(
                        search_quantity=f'data.reference.journal#{schema}',
                        show_input=True,
                        width=6,
                        options=10,
                        title='Journal',
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.reference.publication_date#{schema}',
                            title='Publication Date',
                        )
                    ),
                    MenuItemTerms(
                        search_quantity=f'data.reference.DOI_number#{schema}',
                        show_input=True,
                        options=10,
                        title='DOI',
                    ),
                ],
            ),
            Menu(
                title='Material',
                size=MenuSizeEnum.XXL,
                items=[
                    MenuItemPeriodicTable(
                        quantity='results.material.elements',
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity='results.properties.electronic.band_gap.value',
                            scale='linear',
                            unit='eV',
                            title='Band gap',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.POW4,
                        ),
                        title='Band gap',
                        show_input=True,
                        nbins=30,
                        autorange=True,
                    ),
                ],
            ),
            Menu(
                title='Device Architecture',
                size=MenuSizeEnum.LG,
                items=[
                    MenuItemTerms(
                        search_quantity=f'data.general.architecture#{schema}',
                        options=5,
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.general.number_of_terminals#{schema}',
                            scale=ScaleEnum.LINEAR,
                            title='Number of terminals',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.POW4,
                        ),
                        title='Number of terminals',
                        show_input=False,
                        nbins=30,
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.general.number_of_junctions#{schema}',
                            scale=ScaleEnum.LINEAR,
                            title='Number of junctions',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.POW4,
                        ),
                        title='Number of junctions',
                        show_input=False,
                        nbins=30,
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.general.cell_area#{schema}',
                            scale=ScaleEnum.LOG,
                            title='Total cell area',
                            unit='cm**2',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.POW4,
                        ),
                        title='Total cell area',
                        show_input=False,
                        nbins=30,
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.general.active_area#{schema}',
                            scale=ScaleEnum.LOG,
                            title='Active cell area',
                            unit='cm**2',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.POW4,
                        ),
                        title='Active cell area',
                        show_input=False,
                        nbins=30,
                    ),
                ],
            ),
            Menu(
                title='Stack Layers',
                size=MenuSizeEnum.LG,
                items=[
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.general.number_of_layers#{schema}',
                            scale=ScaleEnum.LINEAR,
                            title='Number of layers',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.POW4,
                        ),
                        title='Number of layers',
                        show_input=False,
                        nbins=30,
                    ),
                    MenuItemTerms(
                        search_quantity=f'data.device_stack.name#{schema}',
                        title='Device stack layers',
                        options=10,
                    ),
                    MenuItemTerms(
                        title='Types of photoabsorber',
                        search_quantity='section_defs.definition_qualified_name',
                        options={
                            'perovskite_solar_cell_database.schema_packages.tandem.device_stack.Photoabsorber_Perovskite': MenuItemOption(
                                label='Perovskite',
                            ),
                            'perovskite_solar_cell_database.schema_packages.tandem.device_stack.Photoabsorber_Silicon': MenuItemOption(
                                label='Silicon',
                            ),
                            'perovskite_solar_cell_database.schema_packages.tandem.device_stack.Photoabsorber_CIGS': MenuItemOption(
                                label='CIGS',
                            ),
                            'perovskite_solar_cell_database.schema_packages.tandem.device_stack.Photoabsorber_CZTS': MenuItemOption(
                                label='CZTS',
                            ),
                            'perovskite_solar_cell_database.schema_packages.tandem.device_stack.Photoabsorber_GaAs': MenuItemOption(
                                label='GaAs',
                            ),
                            'perovskite_solar_cell_database.schema_packages.tandem.device_stack.Photoabsorber_OPV': MenuItemOption(
                                label='OPV',
                            ),
                            'perovskite_solar_cell_database.schema_packages.tandem.device_stack.Photoabsorber_DSSC': MenuItemOption(
                                label='DSSC',
                            ),
                            'perovskite_solar_cell_database.schema_packages.tandem.device_stack.Photoabsorber_QuantumDot': MenuItemOption(
                                label='Quantum Dot',
                            ),
                            'perovskite_solar_cell_database.schema_packages.tandem.device_stack.PhotoabsorberOther': MenuItemOption(
                                label='Other',
                            ),
                        },
                        show_input=False,
                    ),
                    MenuItemTerms(
                        search_quantity=f'data.device_stack.functionality#{schema}',
                        title='Layer functionality',
                        options=10,
                    ),
                ],
            ),
            Menu(
                title='Fabrication',
                size=MenuSizeEnum.SM,
                items=[
                    MenuItemTerms(
                        search_quantity=f'data.device_stack.deposition_procedure.steps.method#{schema}',
                        options=10,
                    ),
                    MenuItemTerms(
                        search_quantity=f'data.reference.sample_id#{schema}',
                        title='Sample ID',
                        options=0,
                    ),
                ],
            ),
            Menu(
                title='Measurements',
                size=MenuSizeEnum.LG,
                items=[
                    MenuItemTerms(
                        title='Types of measurements',
                        search_quantity='section_defs.definition_qualified_name',
                        options={
                            'perovskite_solar_cell_database.schema_packages.tandem.measurements.JV': MenuItemOption(
                                label='JV',
                            ),
                            'perovskite_solar_cell_database.schema_packages.tandem.measurements.ExternalQuantumEfficiency': MenuItemOption(
                                label='External Quantum Efficiency',
                            ),
                            'perovskite_solar_cell_database.schema_packages.tandem.measurements.StabilizedPerformance': MenuItemOption(
                                label='Stabilized Performance',
                            ),
                            'perovskite_solar_cell_database.schema_packages.tandem.measurements.Stability': MenuItemOption(
                                label='Stability',
                            ),
                            'perovskite_solar_cell_database.schema_packages.tandem.measurements.Transmission': MenuItemOption(
                                label='Transmission',
                            ),
                            'perovskite_solar_cell_database.schema_packages.tandem.measurements.Flexibility': MenuItemOption(
                                label='Flexibility',
                            ),
                            'perovskite_solar_cell_database.schema_packages.tandem.measurements.OutdoorPerformance': MenuItemOption(
                                label='Outdoor Performance',
                            ),
                        },
                        show_input=False,
                    ),
                ],
            ),
            Menu(
                title='Solar Cell Performance',
                size=MenuSizeEnum.LG,
                items=[
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.key_performance_metrics.power_conversion_efficiency#{schema}',
                            title='Efficiency (%)',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.LINEAR,
                        ),
                        title='Efficiency (%)',
                        show_input=True,
                        nbins=30,
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.key_performance_metrics.open_circuit_voltage#{schema}',
                            scale=ScaleEnum.LINEAR,
                            title='Voc',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.LINEAR,
                        ),
                        title='Voc',
                        show_input=True,
                        nbins=30,
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.key_performance_metrics.short_circuit_current_density#{schema}',
                            title='Jsc',
                            unit='mA/cm**2',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.LINEAR,
                        ),
                        title='Jsc',
                        show_input=True,
                        nbins=30,
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.key_performance_metrics.fill_factor#{schema}',
                            scale=ScaleEnum.LINEAR,
                            title='Fill factor',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.LINEAR,
                        ),
                        title='Fill factor',
                        show_input=True,
                        nbins=30,
                    ),
                ],
            ),
            Menu(
                title='Stability',
                size=MenuSizeEnum.XXL,
                items=[
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.key_performance_metrics.power_conversion_efficiency_stabilized#{schema}',
                            scale=ScaleEnum.LINEAR,
                            title='Efficiency Stabilized (%)',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.LINEAR,
                        ),
                        title='Efficiency Stabilized (%)',
                        show_input=True,
                        nbins=30,
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.key_performance_metrics.pce_1000h_isos_l1_start#{schema}',
                            scale=ScaleEnum.LINEAR,
                            title='PCE at the start / ISOS L1 (%)',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.LINEAR,
                        ),
                        title='PCE at the start / ISOS L1 (%)',
                        width=6,
                        show_input=True,
                        nbins=30,
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.key_performance_metrics.pce_1000h_isos_l1_end#{schema}',
                            scale=ScaleEnum.LINEAR,
                            title='PCE after 1000h / ISOS L1 (%)',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.LINEAR,
                        ),
                        title='PCE after 1000h / ISOS L1 (%)',
                        width=6,
                        show_input=True,
                        nbins=30,
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.key_performance_metrics.pce_1000h_isos_l3_start#{schema}',
                            scale=ScaleEnum.LINEAR,
                            title='PCE at the start / ISOS L3 (%)',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.LINEAR,
                        ),
                        title='PCE at the start / ISOS L3 (%)',
                        width=6,
                        show_input=True,
                        nbins=30,
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.key_performance_metrics.pce_1000h_isos_l3_end#{schema}',
                            scale=ScaleEnum.LINEAR,
                            title='PCE after 1000h / ISOS L3 (%)',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.LINEAR,
                        ),
                        title='PCE after 1000h / ISOS L3 (%)',
                        width=6,
                        show_input=True,
                        nbins=30,
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.key_performance_metrics.t80_isos_l1#{schema}',
                            scale=ScaleEnum.LINEAR,
                            title='T80 / ISOS L1',
                            unit='hour',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.LINEAR,
                        ),
                        title='T80 / ISOS L1',
                        width=6,
                        show_input=True,
                        nbins=30,
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity=f'data.key_performance_metrics.t80_isos_l3#{schema}',
                            scale=ScaleEnum.LINEAR,
                            title='T80 / ISOS L3',
                            unit='hour',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.LINEAR,
                        ),
                        title='T80 / ISOS L3',
                        width=6,
                        show_input=True,
                        nbins=30,
                    ),
                ],
            ),
            Menu(
                title='NOMAD Upload Information',
                size=MenuSizeEnum.MD,
                items=[
                    MenuItemTerms(
                        search_quantity=f'data.reference.name_of_person_entering_the_data#{schema}',
                        title='Data entered by',
                        options=0,
                    ),
                    MenuItemTerms(
                        search_quantity='authors.name',
                        title='Upload author',
                        options=0,
                    ),
                    MenuItemHistogram(
                        x=Axis(
                            search_quantity='upload_create_time',
                            title='Upload Creation Time',
                        ),
                        y=AxisScale(
                            scale=ScaleEnum.LOG,
                        ),
                        title='Upload Creation Time',
                        show_input=True,
                        nbins=30,
                    ),
                ],
            ),
        ],
    ),
    dashboard=Dashboard.model_validate(widgets),
    filters_locked={'entry_type': 'PerovskiteTandemSolarCell'},
)
