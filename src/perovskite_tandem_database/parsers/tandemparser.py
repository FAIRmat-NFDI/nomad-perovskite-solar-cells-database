from typing import TYPE_CHECKING

from nomad.config import config
from nomad.datamodel.data import EntryData
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.metainfo import Quantity
from nomad.parsing.parser import MatchingParser
from nomad.parsing.tabular import create_archive

from perovskite_tandem_database.schema_packages.schema import PerovskiteTandemSolarCell

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

class TandemParser(MatchingParser):
    """
    Parser for matching tandem db files and creating instances of .
    """

    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
        child_archives: dict[str, 'EntryArchive'] = None,
    ) -> None:
        logger.info('TandemParser.parse')
        # data_file = mainfile.split('/')[-1]
        # entry = PerovskiteTandemSolarCell.m_from_dict(PerovskiteTandemSolarCell.m_def.a_template)
        # entry.data_file = data_file
        # file_name = f'{"".join(data_file.split(".")[:-1])}.archive.json'
        # archive.data = RawFileXRFData(
        #     measurement=create_archive(entry, archive, file_name)
        # )
        # archive.metadata.entry_name = f'{data_file} data file'
