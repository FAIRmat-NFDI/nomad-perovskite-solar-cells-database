from pydantic import BaseModel, Field


class ExtractWorkflowInput(BaseModel):
    """Input model for the simple workflow."""

    upload_id: str = Field(
        ...,
        description='Unique identifier for the upload associated with the workflow.',
    )
    user_id: str = Field(
        ..., description='Unique identifier for the user who initiated the workflow.'
    )
    api_token: str = Field(..., description='API token for LLM access.')
    model: str = Field(..., description='LLM model to be used for extraction.')


class SingleExtractionInput(BaseModel):
    """Data for extraction from a single pdf file."""

    upload_id: str = Field(
        ...,
        description='Unique identifier for the upload associated with the workflow.',
    )
    user_id: str = Field(
        ..., description='Unique identifier for the user who initiated the workflow.'
    )
    pdf: str = Field(..., description='Path to the PDF file to be processed.')
    doi: str = Field(..., description='DOI of the document.')
    api_token: str = Field(..., description='API token for LLM access.')
    model: str = Field(..., description='LLM model to be used for extraction.')


class ProcessNewFilesInput(BaseModel):
    """Data for processing new files activity."""

    upload_id: str = Field(
        ...,
        description='Unique identifier for the upload associated with the workflow.',
    )
    user_id: str = Field(
        ..., description='Unique identifier for the user who initiated the workflow.'
    )
    result_path: list[str] = Field(
        ..., description='Paths to the new entries to be processed.'
    )