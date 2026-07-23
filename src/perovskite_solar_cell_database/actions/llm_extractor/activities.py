import json
import time

from nomad.processing.data import Upload
from temporalio import activity

from perovskite_solar_cell_database.actions.llm_extractor.models import (
    CleanupInput,
    ExtractWorkflowInput,
    ProcessNewFilesInput,
    SingleExtractionInput,
)

ACTION_NAME = 'perovskite_solar_cell_database_llm_extractor'
MAX_ATTEMPT_NUM = 100  # attempts to reprocess upload with new entries


@activity.defn(name=ACTION_NAME + '.get_list_of_pdfs')
def get_list_of_pdfs(input_data: ExtractWorkflowInput) -> dict:
    """
    Find all PDF files in the upload if authorized user has access to the upload.
    """
    from nomad.actions.manager import get_upload_files

    pdfs = []
    upload_files = get_upload_files(
        input_data.upload_id,
        input_data.user_id,
    )
    if upload_files is not None:
        raw_files = upload_files.raw_directory_list(
            path='',
            recursive=True,
            files_only=True,
        )
        for file_info in raw_files:
            if file_info.path.lower().endswith('.pdf'):
                pdfs.append(file_info.path)

    if not pdfs:
        activity.logger.error(
            f'No PDF files found in the upload ID: {input_data.upload_id}'
        )

    return {
        'pdfs': pdfs,
    }


@activity.defn(name=ACTION_NAME + '.extract_from_pdf')
def extract_from_pdf(input_data: SingleExtractionInput) -> dict:
    """
    Extract perovskite solar cell data from a single PDF file using LLM,
    save the extracted data as new entries in the upload, and return the
    list of saved entries.
    """
    from nomad.actions.manager import get_upload_files

    from perovskite_solar_cell_database.actions.llm_extractor.utils import (
        extract_doi,
        pdf_to_solar_cells,
        test_pdf_to_solar_cells,
    )
    # For testing without LLM calls, use test_pdf_to_solar_cells instead of pdf_to_solar_cells

    upload_files = get_upload_files(
        input_data.upload_id,
        input_data.user_id,
    )
    if upload_files is None:
        activity.logger.error(
            f'Upload files not found or can not be accessed for upload ID: {input_data.upload_id}'
        )
        return {'saved_cells': []}

    extracted_cells = []
    if not input_data.api_token or input_data.api_token.get_secret_value() == '':
        activity.logger.error('API token is required for LLM extraction')
        return {'saved_cells': []}
    try:
        if input_data.model_name is None or input_data.model_name.strip() == '':
            model_name = input_data.model_technical_name
        else:
            model_name = input_data.model_name.strip()
        if (
            input_data.api_base_url is not None
            and input_data.api_base_url.strip() != ''
        ):
            model_name = 'openai/' + model_name

        print(f'###### {model_name}')
        extracted_cells = pdf_to_solar_cells(
            pdf=upload_files.raw_file_object(input_data.pdf).os_path,
            api_token=input_data.api_token.get_secret_value(),
            model=model_name,
            api_base_url=input_data.api_base_url,
            logger=activity.logger,
        )
    except Exception as e:
        activity.logger.error('Error during LLM extraction from PDF.', exc_info=e)
        return {'saved_cells': []}

    saved_cells = []
    for idx, cell in enumerate(extracted_cells):
        doi_name = (extract_doi(cell['data']['DOI_number']) or 'unnamed').replace(
            '/', '--', 1
        )
        fname = f'results/{model_name}-{doi_name}-cell-{idx + 1}.archive.json'
        if not upload_files.raw_path_exists('results'):
            upload_files.raw_create_directory('results')
        with upload_files.raw_file(file_path=fname, mode='w', encoding='utf-8') as f:
            json.dump({'data': cell['data']}, f, indent=4)
        saved_cells.append(fname)

    return {'saved_cells': saved_cells}


@activity.defn(name=ACTION_NAME + '.process_new_files')
async def process_new_files(data: ProcessNewFilesInput) -> dict:
    """Process newly created entries in the upload, then return their references."""
    from nomad.actions.manager import get_upload_files
    from nomad.utils import generate_entry_id

    upload_files = get_upload_files(
        data.upload_id,
        data.user_id,
    )
    if upload_files is None:
        activity.logger.error(
            f'Upload files not found or can not be accessed for upload ID: {data.upload_id}'
        )
        return {'refs': []}

    # Wait until the upload is not busy
    for i in range(MAX_ATTEMPT_NUM):
        # authorization already checked with get_upload_files, so we can directly access the upload
        upload = Upload.get(data.upload_id)

        if not upload.process_running:
            break
        else:
            # reload if upload is busy
            time.sleep(0.5)
            activity.logger.warning('Upload is currently being processed. Waiting...')
    else:
        activity.logger.error(
            f'Upload {data.upload_id} is busy for too long. Cannot process new files.'
        )
        return {'refs': []}

    handle = upload.process_upload(
        path_filter='results',
        only_updated_files=True,
    )

    await handle.result()  # type: ignore

    result_entry_refs = []

    for path in data.result_path:
        if upload_files.raw_path_exists(path) and upload_files.raw_path_is_file(path):
            result_entry_refs.append(
                f'../uploads/{upload.upload_id}/archive/{generate_entry_id(str(upload.upload_id), path)}#/data'
            )

    return {'refs': result_entry_refs}


@activity.defn(name=ACTION_NAME + '.remove_source_pdfs')
def remove_source_pdfs(input_data: CleanupInput) -> None:
    """
    Remove source PDF files from the upload after extraction.
    """
    from nomad.actions.manager import get_upload_files

    upload_files = get_upload_files(
        input_data.upload_id,
        input_data.user_id,
    )
    if upload_files is None:
        activity.logger.error(
            f'Upload files not found or can not be accessed for upload ID: {input_data.upload_id}'
        )
        return

    for pdf in input_data.pdfs:
        upload_files.delete_rawfiles(
            path=pdf
        )  # Delete the PDF after extraction for copyright reasons
