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
        retry_policy = RetryPolicy(
            maximum_attempts=3,
        )
        list_of_pdfs = await workflow.execute_activity(
            get_list_of_pdfs,
            data,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=retry_policy,
        )
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
                saved_cells = await workflow.execute_activity(
                    extract_from_pdf,
                    single_input,
                    start_to_close_timeout=timedelta(seconds=600),
                    retry_policy=retry_policy,
                )
                all_saved_cells.extend(saved_cells or [])

            input_for_processing = ProcessNewFilesInput(
                upload_id=data.upload_id,
                user_id=data.user_id,
                result_path=all_saved_cells,
            )
            result_entry_refs = await workflow.execute_activity(
                process_new_files,
                input_for_processing,
                start_to_close_timeout=timedelta(seconds=60),
                retry_policy=retry_policy,
            )
        except ActivityError as e:
            error_msg = f'Extraction activity failed: {e}'
            workflow.logger.error(error_msg)
            if len(error_msg) > 10000:
                error_msg = error_msg[:10000] + '... [truncated]'
            return {'refs': [], 'extraction_successful': False, 'errors': [error_msg]}

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

        return {'refs': result_entry_refs, 'extraction_successful': True, 'errors': []}
