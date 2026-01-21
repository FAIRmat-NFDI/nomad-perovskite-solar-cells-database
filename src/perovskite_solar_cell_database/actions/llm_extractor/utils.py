import os
import re

from nomad.units import ureg


def delete_pdf(pdf: str) -> None:
        """
        Deletes the PDF file from the upload.
        """
        if pdf:
            try:
                # os.remove(os.path.join(self.m_context.raw_path(), pdf))
                os.remove(pdf)
            except FileNotFoundError:
                pass  # File already deleted or does not exist


def doi_to_name(doi: str) -> str:
    """
    Converts the DOI to a name suitable for the entry.
    """
    if not doi:
        return 'unnamed'
    doi_parsed = extract_doi(doi)
    if doi_parsed is None:
        return 'unnamed'
    else:
        return doi_parsed.replace('/', '--', 1) or 'unnamed'


def pdf_to_solar_cells(pdf: str, doi: str, api_token: str, model: str, logger) -> list[dict]:
    """
    Extract perovskite solar cells from a PDF using an LLM.
    """
    try:
        from perovscribe.pipeline import ExtractionPipeline

        return ExtractionPipeline(
            model, 'pymupdf', 'NONE', '', False
        ).extract_from_pdf_nomad(
            pdf, extract_doi(doi), api_token, ureg)
    except ImportError as e:
        logger.error(
            'The perovskite-solar-cell-database plugin needs to be installed with the "extraction" extra to use LLM extraction.',
            exc_info=e
        )
        return []


def test_pdf_to_solar_cells(pdf: str, doi: str, api_token: str, model: str, logger) -> list[dict]:
    return []


def extract_doi(doi: str) -> str|None:
    """
    Extracts the DOI prefix and suffix (10.xxxx/xxxx) from a DOI string.
    Returns None if no valid DOI is found.
    """
    match = re.search(r'10\.\d{4,9}/[-._;()/:\w\[\]]+', doi, re.IGNORECASE)
    if match:
        return match.group(0)
    return None