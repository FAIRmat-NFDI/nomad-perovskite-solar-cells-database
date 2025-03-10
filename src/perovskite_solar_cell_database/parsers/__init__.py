from nomad.config.models.plugins import ParserEntryPoint


class TandemParserEntryPoint(ParserEntryPoint):
    """
    Tandem Parser plugin entry point.
    """

    def load(self):
        # lazy import to avoid circular dependencies
        from perovskite_solar_cell_database.parsers.tandem_parser import TandemParser

        return TandemParser(**self.dict())


tandem_parser = TandemParserEntryPoint(
    name='TandemParser',
    description='Tandem Parser for .xlsx files.',
    mainfile_name_re=r'.*\.xlsx',
    # mainfile_content_re='',
    mainfile_contents_dict={
        'Master vertical': {
            '__has_all_keys': [
                'Ref. ID temp (Integer starting from 1 and counting upwards)',
            ]
        },
    },
)


class IonParserEntryPoint(ParserEntryPoint):
    def load(self):
        from perovskite_solar_cell_database.parsers.ion_parser import IonParser

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
