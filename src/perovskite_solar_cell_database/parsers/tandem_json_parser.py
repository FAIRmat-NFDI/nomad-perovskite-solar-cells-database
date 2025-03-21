import os
from typing import TYPE_CHECKING

from nomad.datamodel.datamodel import EntryArchive
from nomad.parsing.parser import MatchingParser

from perovskite_solar_cell_database.parsers.utils import create_archive
from perovskite_solar_cell_database.schema_packages.tandem.schema import (
    PerovskiteTandemSolarCell,
)

if TYPE_CHECKING:
    from structlog.stdlib import BoundLogger


class TandemJSONParser(MatchingParser):
    """
    Parser for tandem JSON files and creating instances of PerovskiteTandemSolarCell.
    """

    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
        child_archives: dict[str, 'EntryArchive'] = None,
    ) -> None:
        filename = os.path.basename(mainfile)
        logger.info(f'Parsing file {filename}')

        tandem = PerovskiteTandemSolarCell()

        entry_archive = EntryArchive()
        entry_archive.data = tandem

        create_archive(
            entry_archive.m_to_dict(),
            archive.m_context,
            'tandem' + '.archive.json',
            # os.path.splitext(filename)[0] + '.archive.json',
            'json',
            logger,
        )
