from nomad.config.models.plugins import SchemaPackageEntryPoint
from pydantic import Field


class PerovskiteDatabasePackageEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from perovskite_solar_cell_database.schema_packages.perovskite_solar_cell_database import (
            m_package,
        )

        return m_package


perovskite_solar_cell_database = PerovskiteDatabasePackageEntryPoint(
    name='PerovskiteSolarCell',
    description='Schema package defined for the perovskite solar cells database.',
)