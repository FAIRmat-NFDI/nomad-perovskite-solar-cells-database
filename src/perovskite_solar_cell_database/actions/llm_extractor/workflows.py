from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from perovskite_solar_cell_database.actions.llm_extractor.activities import (
        extract_from_pdf,
        get_list_of_pdfs,
    )
    from perovskite_solar_cell_database.actions.llm_extractor.models import (
        ExtractWorkflowInput,
        SingleExtractionInput,
    )


@workflow.defn
class ExtractWorkflow:
    @workflow.run
    async def run(self, data: ExtractWorkflowInput) -> None:
        retry_policy = RetryPolicy(
            maximum_attempts=3,
        )
        list_of_pdfs = await workflow.execute_activity(
            get_list_of_pdfs,
            data,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=retry_policy,
        )
        for pdf, doi in zip(list_of_pdfs['pdfs'], list_of_pdfs['dois']):
            single_input = SingleExtractionInput(
                upload_id=data.upload_id,
                user_id=data.user_id,
                pdf=pdf,
                doi=doi,
                api_token=data.api_token,
                model=data.model,
            )
            await workflow.execute_activity(
                extract_from_pdf,
                single_input,
                start_to_close_timeout=timedelta(seconds=600),
                retry_policy=retry_policy,
            )
