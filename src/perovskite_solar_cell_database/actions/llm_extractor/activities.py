from temporalio import activity

from perovskite_solar_cell_database.actions.llm_extractor.models import (
    ExtractWorkflowInput,
)


@activity.defn
async def greet(data: ExtractWorkflowInput) -> str:
    return f'hello {data.name} - created by user {data.user_id} for upload {data.upload_id}'
