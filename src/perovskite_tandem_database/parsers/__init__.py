from nomad.config.models.plugins import ParserEntryPoint


class TandemParserEntryPoint(ParserEntryPoint):
    """
    XRF Parser plugin entry point.
    """

    def load(self):
        # lazy import to avoid circular dependencies
        from perovskite_tandem_database.parsers.tandemparser import TandemParser

        return TandemParser(**self.dict())


tandem_parser = TandemParserEntryPoint(
    name='TandemParser',
    description='Tandem Parser for .csv files.',
    mainfile_name_re='.*\.csv',
    # mainfile_content_re='',
)
