from typing import Literal

from pydantic import BaseModel, Field, SecretStr, field_serializer

ModelName = Literal[
    'gpt-4o',
    # 'gpt-5',  # Uncomment when temperature support is correct in LiteLLM
    'claude-4-sonnet-20250514',
    #  'meta.llama3-70b-instruct-v1:0',  # Uncomment when someone can test it
]  # Restricted set of LLM model names supported.


class ExtractWorkflowInput(BaseModel):
    """Input model for the simple workflow."""

    upload_id: str = Field(
        ...,
        description='Unique identifier for the upload associated with the workflow.',
    )
    user_id: str = Field(
        ..., description='Unique identifier for the user who initiated the workflow.'
    )
    api_token: SecretStr = Field(..., description='API token for LLM access.')
    model: ModelName = Field(
        'claude-4-sonnet-20250514', description='LLM model to be used for extraction.'
    )

    @field_serializer('api_token', when_used='json')
    def dump_secret(self, v):
        return v.get_secret_value()


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
    api_token: SecretStr = Field(..., description='API token for LLM access.')
    model: ModelName = Field(
        'claude-4-sonnet-20250514', description='LLM model to be used for extraction.'
    )

    @field_serializer('api_token', when_used='json')
    def dump_secret(self, v):
        return v.get_secret_value()


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


class CleanupInput(BaseModel):
    """Data for cleanup activity."""

    upload_id: str = Field(
        ...,
        description='Unique identifier for the upload associated with the workflow.',
    )
    user_id: str = Field(
        ..., description='Unique identifier for the user who initiated the workflow.'
    )
    pdfs: list[str] = Field(..., description='Paths to the PDF files to be removed.')
