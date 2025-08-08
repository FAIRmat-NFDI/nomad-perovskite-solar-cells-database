from nomad.config.models.plugins import SchemaPackageEntryPoint
from pydantic import Field


class TandemDatabasePackageEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from perovskite_solar_cell_database.schema_packages.tandem.schema import (
            m_package,
        )

        return m_package


tandem_solar_cell = TandemDatabasePackageEntryPoint(
    name='TandemSolarCell',
    description='Schema package defined for the tandem solar cells database.',
)


class LlmExtractorPackageEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from perovskite_solar_cell_database.schema_packages.llm_extractor import (
            m_package,
        )

        return m_package


llm_extractor = LlmExtractorPackageEntryPoint(
    name='LlmExtractor',
    description='Schema package defined for the LLM extractor.',
)
