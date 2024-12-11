from nomad.config.models.plugins import ParserEntryPoint


class TandemParserEntryPoint(ParserEntryPoint):
    """
    Tandem Parser plugin entry point.
    """

    def load(self):
        # lazy import to avoid circular dependencies
        from perovskite_tandem_database.parsers.tandemparser import TandemParser

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
