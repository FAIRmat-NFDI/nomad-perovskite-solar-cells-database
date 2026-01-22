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
    """
    Test function for extracting perovskite solar cells from a PDF.
    """
    import json
    import time

    m = re.search(r'^(.*)(?=/src/)', os.path.abspath(__file__))
    if m:
        path_to_plugin = m.group(1)
    else:
        return []
    print(f'#### path_to_plugin: {path_to_plugin}')
    try:
        open(pdf, 'rb')
    except FileNotFoundError:
        logger.error(f'PDF file not found: {pdf}')
        return []
    
    with open(
        f'{path_to_plugin}/tests/data/claude-4-sonnet-20250514-10.1002--aenm.201900555-cell-1.archive.json'
    ) as f:
        try:
            cell_1 = json.load(f)
        except Exception as e:
            logger.error('Error loading test extraction result.', exc_info=e)

    with open(
        f'{path_to_plugin}/tests/data/claude-4-sonnet-20250514-10.1002--aenm.201900555-cell-2.archive.json'
    ) as f:
        try:
            cell_2 = json.load(f)
        except Exception as e:
            logger.error('Error loading test extraction result.', exc_info=e)

    time.sleep(5)  # Simulate some processing time
    return [cell_1, cell_2]


def extract_doi(doi: str) -> str|None:
    """
    Extracts the DOI prefix and suffix (10.xxxx/xxxx) from a DOI string.
    Returns None if no valid DOI is found.
    """
    match = re.search(r'10\.\d{4,9}/[-._;()/:\w\[\]]+', doi, re.IGNORECASE)
    if match:
        return match.group(0)
    return None