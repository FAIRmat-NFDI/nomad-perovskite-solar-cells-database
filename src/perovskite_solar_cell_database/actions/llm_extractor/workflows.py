from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from perovskite_solar_cell_database.actions.llm_extractor.activities import greet
    from perovskite_solar_cell_database.actions.llm_extractor.models import (
        ExtractWorkflowInput,
    )


@workflow.defn
class ExtractWorkflow:
    @workflow.run
    async def run(self, data: ExtractWorkflowInput) -> str:
        retry_policy = RetryPolicy(
            maximum_attempts=3,
        )
        result = await workflow.execute_activity(
            greet,
            data,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=retry_policy,
        )
        return result
