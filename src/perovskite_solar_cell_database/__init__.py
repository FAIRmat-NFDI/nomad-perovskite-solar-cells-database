from nomad.config.models.plugins import (
    ParserEntryPoint,
    SchemaPackageEntryPoint,
)
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


class IonParserEntryPoint(ParserEntryPoint):
    def load(self):
        from perovskite_solar_cell_database.parser import IonParser

        return IonParser(**self.dict())


ion_parser = IonParserEntryPoint(
    name='PerovskiteIonParser',
    description='Parse excel files containing perovskite ions.',
    mainfile_name_re=r'.+\.xlsx',
    mainfile_mime_re='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    mainfile_contents_dict={
        'Sheet1': {
            '__has_all_keys': [
                'perovskite_site',
                'abbreviation',
                'molecular_formula',
                'smiles',
                'common_name',
                'iupac_name',
                'cas_number',
                'source_compound_iupac_name',
                'source_compound_smiles',
                'source_compound_cas_number',
            ]
        },
    },
)
