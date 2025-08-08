import yaml
from nomad.config.models.ui import (
    App,
    Column,
    Columns,
    FilterMenu,
    FilterMenus,
    Filters,
)

llm_extracted_solar_cells = App(
    # Label of the App
    label='LLM Extracted Solar Cells',
    # Path used in the URL, must be unique
    path='llm-extracted-solar-cells',
    # Used to categorize apps in the explore menu
    category='LLM strcutured data extraction',
    # Brief description used in the app menu
    description="""
    Explore the LLM extracted solar cells.
    """,
    # Longer description that can also use markdown
    readme="""
    Explore LLM extracted solar cells.
    """,
    # Controls the available search filters. If you want to filter by
    # quantities in a schema package, you need to load the schema package
    # explicitly here. Note that you can use a glob syntax to load the
    # entire package, or just a single schema from a package.
    filters=Filters(
        include=[
            '*#perovskite_solar_cell_database.llm_extraction_schema.LLMExtractedPerovskiteSolarCell',
        ]
    ),
    # Controls which columns are shown in the results table
    columns=Columns(
        selected=[
            'authors',
            # 'results.material.elements',
            'entry_type',
            'data.review_completed#perovskite_solar_cell_database.llm_extraction_schema.LLMExtractedPerovskiteSolarCell',
            'references',
            # 'data.lab_id#nomad_material_processing.combinatorial.ThinFilmCombinatorialSample'
        ],
        options={
            'entry_type': Column(label='Entry type', align='left'),
            'entry_name': Column(label='Name', align='left'),
            'entry_create_time': Column(label='Entry time', align='left'),
            'authors': Column(label='Authors', align='left'),
            'upload_name': Column(label='Upload name', align='left'),
            'references': Column(label='References', align='left'),
            'data.review_completed#perovskite_solar_cell_database.llm_extraction_schema.LLMExtractedPerovskiteSolarCell': Column(
                label='Review completed', align='left'
            ),  # noqa: E501
            'data.publication_title#perovskite_solar_cell_database.llm_extraction_schema.LLMExtractedPerovskiteSolarCell': Column(
                label='Publication title', align='left'
            ),  # noqa: E501
            # 'data.lab_id#nomad_htem_database.schema_packages.htem_package.HTEMLibrary': Column(  # noqa: E501
            #     label='Library ID', align='left'
            # ),
            'results.material.elements': Column(label='Elements', align='left'),
        },
    ),
    # Dictionary of search filters that are always enabled for queries made
    # within this app. This is especially important to narrow down the
    # results to the wanted subset. Any available search filter can be
    # targeted here. This example makes sure that only entries that use
    # MySchema are included.
    filters_locked={
        'entry_type': 'LLMExtractedPerovskiteSolarCell',
    },
    # Controls the filter menus shown on the left
    filter_menus=FilterMenus(
        options={
            'material': FilterMenu(label='Material', level=0),
            'elements': FilterMenu(label='Elements / Formula', level=1, size='xl'),
            'eln': FilterMenu(label='Electronic Lab Notebook', level=0),
            'custom_quantities': FilterMenu(
                label='User Defined Quantities', level=0, size='l'
            ),
            'author': FilterMenu(label='Author / Origin / Dataset', level=0, size='m'),
            'metadata': FilterMenu(label='Visibility / IDs / Schema', level=0),
            'optimade': FilterMenu(label='Optimade', level=0, size='m'),
        }
    ),
    # Controls the default dashboard shown in the search interface
    dashboard=yaml.safe_load(
        """
    widgets:
      - type: terms
        scale: linear
        quantity: data.journal#perovskite_solar_cell_database.llm_extraction_schema.LLMExtractedPerovskiteSolarCell
        layout:
          xxl:
            minH: 3
            minW: 3
            h: 9
            w: 6
            y: 0
            x: 6
          xl:
            minH: 3
            minW: 3
            h: 5
            w: 6
            y: 0
            x: 6
          lg:
            minH: 3
            minW: 3
            h: 9
            w: 6
            y: 0
            x: 6
          md:
            minH: 3
            minW: 3
            h: 5
            w: 4
            y: 0
            x: 4
          sm:
            minH: 3
            minW: 3
            h: 5
            w: 3
            y: 0
            x: 4
      - type: terms
        scale: linear
        quantity: authors.name
        title: Reviewer names
        layout:
          xxl:
            minH: 3
            minW: 3
            h: 9
            w: 6
            y: 0
            x: 0
          xl:
            minH: 3
            minW: 3
            h: 5
            w: 6
            y: 0
            x: 0
          lg:
            minH: 3
            minW: 3
            h: 9
            w: 6
            y: 0
            x: 0
          md:
            minH: 3
            minW: 3
            h: 5
            w: 4
            y: 0
            x: 0
          sm:
            minH: 3
            minW: 3
            h: 5
            w: 4
            y: 0
            x: 0
      - type: histogram
        autorange: false
        nbins: 30
        y:
          scale: linear
        x:
          quantity: data.publication_date#perovskite_solar_cell_database.llm_extraction_schema.LLMExtractedPerovskiteSolarCell
        layout:
          xxl:
            minH: 3
            minW: 3
            h: 3
            w: 8
            y: 0
            x: 12
          xl:
            minH: 3
            minW: 3
            h: 3
            w: 7
            y: 0
            x: 12
          lg:
            minH: 3
            minW: 3
            h: 3
            w: 8
            y: 0
            x: 12
          md:
            minH: 3
            minW: 3
            h: 3
            w: 7
            y: 0
            x: 8
          sm:
            minH: 3
            minW: 3
            h: 3
            w: 5
            y: 0
            x: 7

      """
    ),
)
