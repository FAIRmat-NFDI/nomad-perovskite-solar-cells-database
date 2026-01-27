import json
import time

from temporalio import activity

from perovskite_solar_cell_database.actions.llm_extractor.models import (
    CleanupInput,
    ExtractWorkflowInput,
    ProcessNewFilesInput,
    SingleExtractionInput,
)

MAX_ATTEMPT_NUM = 100  # attempts to reprocess upload with new entries


@activity.defn
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

    return {
        'pdfs': pdfs,
    }


@activity.defn
def extract_from_pdf(input_data: SingleExtractionInput) -> list[str] | None:
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
        return

    extracted_cells = []
    if not input_data.api_token:
        activity.logger.warning('API token is required for LLM extraction')
        return
    try:
        extracted_cells = pdf_to_solar_cells(
            pdf=upload_files.raw_file_object(input_data.pdf).os_path,
            api_token=input_data.api_token.get_secret_value(),
            model=input_data.model,
            logger=activity.logger,
        )
    except Exception as e:
        activity.logger.error('Error during LLM extraction from PDF.', exc_info=e)

    saved_cells = []
    for idx, cell in enumerate(extracted_cells):
        doi_name = (extract_doi(cell['data']['DOI_number']) or 'unnamed').replace(
            '/', '--', 1
        )
        fname = f'{input_data.model}-{doi_name}-cell-{idx + 1}.archive.json'
        with upload_files.raw_file(file_path=fname, mode='w', encoding='utf-8') as f:
            json.dump({'data': cell['data']}, f, indent=4)
        saved_cells.append(fname)

    return saved_cells


@activity.defn
async def process_new_files(data: ProcessNewFilesInput) -> list[str]:
    """Process newly created entries in the upload, then return their references."""
    from nomad.actions.manager import get_upload_files
    from nomad.app.v1.routers.uploads import get_upload_with_read_access
    from nomad.datamodel import User
    from nomad.utils import generate_entry_id

    upload_files = get_upload_files(
        data.upload_id,
        data.user_id,
    )
    if upload_files is None:
        activity.logger.error(
            f'Upload files not found or can not be accessed for upload ID: {data.upload_id}'
        )
        return []

    file_operations = []

    for path in data.result_path:
        file_operations.append(
            dict(
                op='ADD',
                path=upload_files.raw_file_object(path).os_path,
                target_dir='',
                temporary=False,
            )
        )

    # Wait until the upload is not busy
    for i in range(MAX_ATTEMPT_NUM):
        upload = get_upload_with_read_access(
            data.upload_id,
            User(user_id=data.user_id),
            include_others=True,
        )

        if not upload.process_running:
            break
        else:
            # reload if upload is busy
            time.sleep(0.5)
            activity.logger.warning('Upload is currently being processed. Waiting...')

    handle = upload.process_upload(
        file_operations=file_operations,
        only_updated_files=True,
    )

    await handle.result()  # type: ignore

    result_entry_refs = []

    for path in data.result_path:
        if upload_files.raw_path_exists(path) and upload_files.raw_path_is_file(path):
            result_entry_refs.append(
                f'../uploads/{upload.upload_id}/archive/{generate_entry_id(str(upload.upload_id), path)}#/data'
            )

    return result_entry_refs


@activity.defn
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
