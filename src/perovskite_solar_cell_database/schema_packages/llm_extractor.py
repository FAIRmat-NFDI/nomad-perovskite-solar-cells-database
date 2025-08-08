import os
import re
from typing import (
    TYPE_CHECKING,
)

from nomad.datamodel.data import UseCaseElnCategory
from nomad.datamodel.metainfo.annotations import ELNComponentEnum
from nomad.datamodel.metainfo.eln import ELNAnnotation
from nomad.metainfo import Quantity, Section

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive

from nomad.datamodel.data import Schema
from nomad.metainfo import SchemaPackage

from perovskite_solar_cell_database.llm_extraction_schema import (
    LLMExtractedPerovskiteSolarCell,
    get_reference,
)

m_package = SchemaPackage()


class LlmPerovskitePaperExtractor(Schema):
    m_def = Section(
        label='LLM Perovskite Paper Extractor',
        categories=[UseCaseElnCategory],
    )
    pdf = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.FileEditQuantity),
    )
    doi = Quantity(
        type=str,
        description='DOI of the paper',
        a_eln=ELNAnnotation(component=ELNComponentEnum.URLEditQuantity),
    )
    open_ai_token = Quantity(
        type=str,
        description='OpenAI API token for LLM extraction',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity, props=dict(type='password')
        ),
    )
    extracted_solar_cells = Quantity(
        type=LLMExtractedPerovskiteSolarCell,
        shape=['*'],
        description='List of extracted perovskite solar cells from the paper',
    )

    def delete_pdf(self):
        """
        Deletes the PDF file from the upload.
        """
        if self.pdf:
            try:
                os.remove(os.path.join(self.m_context.raw_path(), self.pdf))
                self.pdf = None  # Clear the reference to the deleted file
            except FileNotFoundError:
                pass  # File already deleted or does not exist

    def doi_to_name(self) -> str:
        """
        Converts the DOI to a name suitable for the entry.
        """
        if not self.doi:
            return 'unnamed'
        return extract_doi(self.doi) or 'unnamed'

    def normalize(self, archive: 'EntryArchive', logger):
        super().normalize(archive, logger)
        extracted_cells = []
        try:
            if not self.open_ai_token:
                logger.warn('OpenAI token is required for LLM extraction')
                return
            _open_ai_token = self.open_ai_token
            self.open_ai_token = None  # Hide token in the archive
            if not self.doi:
                logger.warn('DOI is required for LLM extraction')
                return
            if not isinstance(self.pdf, str) or not self.pdf.endswith('.pdf'):
                logger.warn('PDF file is required for LLM extraction')
                return
            extracted_cells = pdf_to_solar_cells(
                pdf=os.path.join(archive.m_context.raw_path(), self.pdf),
                doi=self.doi,
                open_ai_token=_open_ai_token,
                logger=logger,
            )
        finally:
            self.delete_pdf()  # Delete the PDF after extraction for copyright reasons
        cell_references = []
        for idx, cell in enumerate(extracted_cells):
            name = f'{self.doi_to_name()}-cell-{idx + 1}.archive.json'
            with archive.m_context.update_entry(
                name, write=True, process=True
            ) as entry:
                entry['data'] = cell['data']
            cell_references.append(
                get_reference(upload_id=archive.metadata.upload_id, mainfile=name)
            )
        if cell_references:
            self.extracted_solar_cells = cell_references


def pdf_to_solar_cells(pdf: str, doi: str, open_ai_token: str, logger) -> list[dict]:
    """
    Extract perovskite solar cells from a PDF using an LLM.
    """
    try:
        from perovscribe.pipeline import ExtractionPipeline

        return ExtractionPipeline(
            'gpt-4o', 'pymupdf', 'NONE', '', False
        ).extract_from_pdf_nomad(pdf, doi, open_ai_token)
    except ImportError:
        logger.error(
            'The perovskite-solar-cell-database plugin needs to be installed with the "extraction" extra to use LLM extraction.'
        )
        return []


def extract_doi(doi: str) -> str:
    """
    Extracts the DOI prefix and suffix (10.xxxx/xxxx) from a DOI string,
    and replaces the forward slash ("/") between the prefix and suffix with a double hyphen ("--").
    Returns None if no valid DOI is found.
    """
    match = re.search(r'10\.\d{4,9}/[-._;()/:\w\[\]]+', doi, re.IGNORECASE)
    if match:
        return match.group(0).replace('/', '--', 1)
    return None


m_package.__init_metainfo__()
