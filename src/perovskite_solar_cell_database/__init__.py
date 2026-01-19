from pydantic import Field
from temporalio import workflow

# currently, imports inside workflow.unsafe.imports_passed_through() to avoid issues with temporalio workflow checks at the start of cpu-worker. TODO: move this init and related files to a dedicated folder, take care of m_def of the old files
with workflow.unsafe.imports_passed_through():
    from nomad.config.models.plugins import (
        ParserEntryPoint,
        SchemaPackageEntryPoint,
    )

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


class PerovskiteCompositionEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from perovskite_solar_cell_database.composition import (
            m_package,
        )

        return m_package


perovskite_composition = PerovskiteCompositionEntryPoint(
    name='PerovskiteComposition',
    description='Schema package defined for the perovskite compositions.',
)


class LLMSchemaExtractionPackageEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from perovskite_solar_cell_database.llm_extraction_schema import (
            m_package,
        )

        return m_package


llm_extraction_schema = LLMSchemaExtractionPackageEntryPoint(
    name='LLMExtractionSchema',
    description='Schema package defined for the perovskite solar cells database LLM extraction.',
)
