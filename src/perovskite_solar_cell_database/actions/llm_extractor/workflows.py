from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError

with workflow.unsafe.imports_passed_through():
    from perovskite_solar_cell_database.actions.llm_extractor.activities import (
        extract_from_pdf,
        get_list_of_pdfs,
        process_new_files,
        remove_source_pdfs,
    )
    from perovskite_solar_cell_database.actions.llm_extractor.models import (
        CleanupInput,
        ExtractWorkflowInput,
        ProcessNewFilesInput,
        SingleExtractionInput,
    )


@workflow.defn
class ExtractWorkflow:
    @workflow.run
    async def run(self, data: ExtractWorkflowInput) -> dict:
        errors = []
        retry_policy = RetryPolicy(
            maximum_attempts=3,
        )
        list_of_pdfs = await workflow.execute_activity(
            get_list_of_pdfs,
            data,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=retry_policy,
        )
        if not list_of_pdfs['pdfs']:
            error_msg = 'No PDF files found in the upload.'
            workflow.logger.error(error_msg)
            errors.append(error_msg)
            return {'refs': [], 'success': False, 'errors': errors}
        try:
            all_saved_cells = []
            for pdf in list_of_pdfs['pdfs']:
                single_input = SingleExtractionInput(
                    upload_id=data.upload_id,
                    user_id=data.user_id,
                    pdf=pdf,
                    api_token=data.api_token,
                    model=data.model,
                )
                extraction_result = await workflow.execute_activity(
                    extract_from_pdf,
                    single_input,
                    start_to_close_timeout=timedelta(seconds=600),
                    retry_policy=retry_policy,
                )
                saved_cells = extraction_result['saved_cells']
                all_saved_cells.extend(saved_cells)
                if not extraction_result['success']:
                    errors.extend(extraction_result['errors'])

            input_for_processing = ProcessNewFilesInput(
                upload_id=data.upload_id,
                user_id=data.user_id,
                result_path=all_saved_cells,
            )
            processing_result = await workflow.execute_activity(
                process_new_files,
                input_for_processing,
                start_to_close_timeout=timedelta(seconds=60),
                retry_policy=retry_policy,
            )
            result_entry_refs = processing_result['refs']
            if not processing_result['success']:
                errors.extend(processing_result['errors'])
        except ActivityError as e:
            error_msg = f'Extraction activity failed: {e}'
            workflow.logger.error(error_msg)
            if len(error_msg) > 10000:
                error_msg = error_msg[:10000] + '... [truncated]'
            errors.append(error_msg)
            return {'refs': [], 'success': False, 'errors': errors}

        finally:
            await workflow.execute_activity(
                remove_source_pdfs,
                CleanupInput(
                    upload_id=data.upload_id,
                    user_id=data.user_id,
                    pdfs=list_of_pdfs['pdfs'],
                ),
                start_to_close_timeout=timedelta(seconds=60),
                retry_policy=retry_policy,
            )

        return {'refs': result_entry_refs, 'success': errors == [], 'errors': errors}
