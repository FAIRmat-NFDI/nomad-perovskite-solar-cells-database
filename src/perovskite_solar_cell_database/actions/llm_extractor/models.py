from pydantic import BaseModel, Field


class ExtractWorkflowInput(BaseModel):
    """Input model for the simple workflow"""

    upload_id: str = Field(
        ...,
        description='Unique identifier for the upload associated with the workflow.',
    )
    user_id: str = Field(
        ..., description='Unique identifier for the user who initiated the workflow.'
    )

    name: str = Field(..., description='The name to greet.')
