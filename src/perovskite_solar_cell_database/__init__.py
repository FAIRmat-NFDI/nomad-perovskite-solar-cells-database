from nomad.config.models.plugins import SchemaPackageEntryPoint
from pydantic import Field


class PerovskiteDatabasePackageEntryPoint(SchemaPackageEntryPoint):
    # parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from perovskite_solar_cell_database.schema import (
            m_package,
        )

        return m_package


perovskite_solar_cell = PerovskiteDatabasePackageEntryPoint(
    name='PerovskiteSolarCell',
    description='Schema package defined for the perovskite solar cells database.',
)

# entry point for perovskite_composition


class PerovskiteCompositionDatabasePackageEntryPoint(SchemaPackageEntryPoint):
    # parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from perovskite_solar_cell_database.perovskite_composition import (
            m_package,
        )

        return m_package


perovskite_composition = PerovskiteCompositionDatabasePackageEntryPoint(
    name='PerovskiteComposition',
    description='Schema package to calculate and define perovskite compositions.',
)
