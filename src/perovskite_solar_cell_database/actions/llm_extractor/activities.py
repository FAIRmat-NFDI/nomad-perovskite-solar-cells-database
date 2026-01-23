import json
import re
import time

from nomad.app.v1.routers.uploads import get_upload_with_read_access
from nomad.datamodel import User
from temporalio import activity

from perovskite_solar_cell_database.actions.llm_extractor.models import (
    ExtractWorkflowInput,
    ProcessNewFilesInput,
    SingleExtractionInput,
)

MAX_ATTEMPT_NUM = 100  # attempts to reprocess upload with new entries

@activity.defn
def get_list_of_pdfs(input_data: ExtractWorkflowInput):
    from nomad.actions.manager import get_upload_files
    from nomad.files import UploadFiles

    pdfs = []
    upload_files = get_upload_files(        #use this in all activities, then raw_file() instead of open()
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
                print(f'#### found pdf: {file_info.path}')
                pdfs.append(f'.volumes/fs/staging/{input_data.upload_id[0:2]}/{input_data.upload_id}'
                    + f'/raw/{file_info.path}')
    # upload_files = UploadFiles.get(input_data.upload_id)
    # if upload_files is not None:
    #     raw_files = upload_files.raw_directory_list(
    #         path='',
    #         recursive=True,
    #         files_only=True,
    #     )
    #     for file_info in raw_files:
    #         if file_info.path.lower().endswith('.pdf'):
    #             print('#### found pdf:', file_info.path)
    #             #TODO: not only staging?
    #             pdfs.append(f'.volumes/fs/staging/{input_data.upload_id[0:2]}/{input_data.upload_id}'
    #                 + f'/raw/{file_info.path}')
    #             # TODO: replace with actual doi extraction
    #             dois.append('10.0000/placeholder-doi')
    print(f'#### raw_files: {raw_files}')
    print(f'#### pdfs: {pdfs}')
    return {
        'pdfs': pdfs,
    }


@activity.defn
def extract_from_pdf(input_data: SingleExtractionInput) -> list[str]|None:
    from perovskite_solar_cell_database.actions.llm_extractor.utils import (
        delete_pdf,
        extract_doi,
        pdf_to_solar_cells,
        test_pdf_to_solar_cells,
    )
    extracted_cells = []
    try:
        if not input_data.api_token:
            activity.logger.warning('API token is required for LLM extraction')
            return
        if not isinstance(input_data.pdf, str) or not input_data.pdf.endswith('.pdf'):
            activity.logger.warning('PDF file is required for LLM extraction')
            return
        extracted_cells = test_pdf_to_solar_cells(
            pdf=input_data.pdf,
            api_token=input_data.api_token,
            model=input_data.model,
            logger=activity.logger,
        )
    finally:
        delete_pdf(pdf=input_data.pdf)  # Delete the PDF after extraction for copyright reasons

    print(f'#### done extracting from {input_data.pdf}.')
    m = re.search(r'^(.*)(?=/raw/)', input_data.pdf)
    if m:
        upload_path = m.group(1) + '/raw'
    else:
        activity.logger.warning('Invalid pdf path format')
        return

    saved_cells = []
    for idx, cell in enumerate(extracted_cells):
        doi_name = (
            extract_doi(cell['data']['DOI_number'])
            or 'unnamed'
        ).replace('/', '--', 1)
        fname = f'{input_data.model}-{doi_name}-cell-{idx + 1}.archive.json'
        # fname = f'{input_data.model}-{doi_to_name(input_data.doi)}-cell-{idx + 1}.archive.json'
        fpath = upload_path + '/' + fname
        with open(fpath, 'w', encoding='utf-8') as f:
            json.dump({'data': cell['data']}, f, indent=4)
        saved_cells.append(fpath)

    return saved_cells


@activity.defn
async def process_new_files(data: ProcessNewFilesInput) -> None:
    file_operations = []
    mainfile_names = []

    for path in data.result_path:
        target_dir = path.split('/raw/')[-1]
        mainfile_names.append(target_dir)
        target_dir = '/'.join(target_dir.split('/')[:-1])
        file_operations.append(
            dict(op='ADD', path=path, target_dir=target_dir, temporary=False)
        )

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