from nomad.config.models.plugins import AppEntryPoint

from perovskite_solar_cell_database.apps.solar_cell_app import solar_cell_app

solar_cells = AppEntryPoint(
    name='Solar Cells',
    description="""
      This app allows you to search **solar cell data** within NOMAD. The filter
      menu on the left and the shown default columns are specifically designed
      for solar cell exploration. The dashboard directly shows useful
      interactive statistics about the data.
    """,
    app=solar_cell_app,
)
