import os

from temporalio import activity

from perovskite_solar_cell_database.actions.llm_extractor.models import (
    ExtractWorkflowInput,
    SingleExtractionInput,
)


@activity.defn
def get_list_of_pdfs(input_data: ExtractWorkflowInput):
    # from perovskite_solar_cell_database.actions.llm_extractor.utils import (
    #     extract_doi,
    # )
    from nomad.files import UploadFiles

    pdfs = []
    dois = []
    upload_files = UploadFiles.get(input_data.upload_id)
    if upload_files is not None:
        raw_files = upload_files.raw_directory_list(
            path='',
            recursive=True,
            files_only=True,
        )
        for file_info in raw_files:
            if file_info.path.lower().endswith('.pdf'):
                print('#### found pdf:', file_info.path)
                #TODO: not only staging?
                pdfs.append(f'.volumes/fs/staging/{input_data.upload_id[0:2]}/{input_data.upload_id}'
                    + f'/raw/{file_info.path}')
                # TODO: replace with actual doi extraction
                dois.append('10.0000/placeholder-doi')
    print(f'#### raw_files: {raw_files}')
    print(f'#### pdfs: {pdfs}, dois: {dois}')
    return {
        'pdfs': pdfs,  # List of PDF file paths
        'dois': dois,  # Corresponding list of DOIs
    }


@activity.defn
def extract_from_pdf(input_data: SingleExtractionInput) -> None:
    from perovskite_solar_cell_database.actions.llm_extractor.utils import (
        delete_pdf,
        pdf_to_solar_cells,
        test_pdf_to_solar_cells,
    )
    extracted_cells = []
    try:
        if not input_data.api_token:
            activity.logger.warning('API token is required for LLM extraction')
            return
        if not input_data.doi:
            activity.logger.warning('DOI is required for LLM extraction')
            return
        if not isinstance(input_data.pdf, str) or not input_data.pdf.endswith('.pdf'):
            activity.logger.warning('PDF file is required for LLM extraction')
            return
        extracted_cells = test_pdf_to_solar_cells(
            pdf=input_data.pdf,
            doi=input_data.doi,
            api_token=input_data.api_token,
            model=input_data.model,
            logger=activity.logger,
        )
    finally:
        delete_pdf(pdf=input_data.pdf)  # Delete the PDF after extraction for copyright reasons

    print(f'done extracting from {input_data.pdf}.')
    # cell_references = []
    # for idx, cell in enumerate(extracted_cells):
    #     name = f'{self.model}-{self.doi_to_name()}-cell-{idx + 1}.archive.json'
    #     with archive.m_context.update_entry(
    #         name, write=True, process=True
    #     ) as entry:
    #         entry['data'] = cell['data']
    #     cell_references.append(
    #         get_reference(upload_id=archive.metadata.upload_id, mainfile=name)
    #     )
    # if cell_references:
    #     self.extracted_solar_cells = cell_references