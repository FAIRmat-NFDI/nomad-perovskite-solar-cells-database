from nomad.config.models.plugins import AppEntryPoint

from perovskite_solar_cell_database.apps.perovskite_ions_app import perovskite_ions_app
from perovskite_solar_cell_database.apps.perovskite_solar_cell_database_app import (
    perovskite_database_app,
)
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

perovskite_solar_cell_database_app = AppEntryPoint(
    name='The Perovskite Solar Cell Database',
    description="""
      Search Entries of the Perovskite Solar Cell Database
    """,
    app=perovskite_database_app,
)

perovskite_ions = AppEntryPoint(
    name='Halide Perovskite Ions',
    description="""
      This app allows you to search **ions of halide perovskites** within NOMAD. The filter
      menu on the left and the shown default columns are specifically designed
      for perovskite ions exploration. The dashboard directly shows useful
      interactive statistics about the data.
    """,
    app=perovskite_ions_app,
)
