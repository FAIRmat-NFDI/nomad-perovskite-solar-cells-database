from typing import Literal

from pydantic import BaseModel, Field, SecretStr, field_serializer

ModelName = Literal[
    'GPT 4o',
    'Claude Sonnet 4.6',
    'Claude Sonnet 4.v20250514',
    'Claude Sonnet 5',
    'Claude Fable 5',
    'Claude Opus 4.8',
    'GPT 5.6 Sol',
    'GPT 5.6 Terra',
    'GPT 5.6 Luna',
    'Gemini Pro Latest',
    'Gemini 3 Flash',
    'Gemini 3.6 Flash',
    'Gemini 3.5 Flash',
]  # Restricted set of LLM model names supported.

ModelAliases = {
    'GPT 4o': 'gpt-4o',
    'Claude Sonnet 4.6': 'claude-sonnet-4-6',
    'Claude Sonnet 4.v20250514': 'claude-4-sonnet-20250514',
    'Claude Sonnet 5': 'claude-sonnet-5',
    'Claude Fable 5': 'claude-fable-5',
    'Claude Opus 4.8': 'claude-opus-4-8',
    'GPT 5.6 Sol': 'gpt-5.6-sol',
    'GPT 5.6 Terra': 'gpt-5.6-terra',
    'GPT 5.6 Luna': 'gpt-5.6-luna',
    'Gemini Pro Latest': 'gemini-pro-latest',
    'Gemini 3 Flash': 'gemini-3-flash',
    'Gemini 3.6 Flash': 'gemini-3.6-flash',
    'Gemini 3.5 Flash': 'gemini-3.5-flash',
}


class ExtractWorkflowInput(BaseModel):
    """
    Run this action to extract perovskite solar cells information from all PDFs in a
    project/upload.

    First, upload the research papers as PDF files to the project. Then, submit this action
    providing the project ID (upload ID) and api token for the chosen LLM. The action will
    find and process all PDF files in the project using the specified LLM, then create and
    process new entries for each detected solar cell and delete the source PDF files.
    """

    upload_id: str = Field(
        ...,
        description='Unique identifier for the project associated with the action.',
    )
    user_id: str = Field(
        ..., description='Unique identifier for the user who initiated the action.'
    )
    api_token: SecretStr = Field(..., description='API token for LLM access.')
    model: ModelName = Field(
        'Claude Sonnet 4.6', description='LLM model to be used for extraction.'
    )
    api_base_url: str | None = Field(
        None,
        description='Optional: Base URL for the LLM API; can use https://openrouter.ai/',
    )
    model_name: str | None = Field(
        None,
        description='Optional: LLM model to be used for extraction as a free text. If filled, the model from the drop-down menu will be ignored.',
    )

    @field_serializer('api_token', when_used='json')
    def dump_secret(self, v):
        return v.get_secret_value()

    @property
    def model_technical_name(self):
        return ModelAliases[self.model]


class SingleExtractionInput(BaseModel):
    """Data for extraction from a single pdf file."""

    upload_id: str = Field(
        ...,
        description='Unique identifier for the project associated with the action.',
    )
    user_id: str = Field(
        ..., description='Unique identifier for the user who initiated the action.'
    )
    pdf: str = Field(..., description='Path to the PDF file to be processed.')
    api_token: SecretStr = Field(..., description='API token for LLM access.')
    model: ModelName = Field(
        'Claude Sonnet 4.6', description='LLM model to be used for extraction.'
    )
    api_base_url: str | None = Field(
        None,
        description='Optional: Base URL for the LLM API; can use https://openrouter.ai/',
    )
    model_name: str | None = Field(
        None,
        description='Optional: LLM model to be used for extraction as a free text. If filled, the model from the drop-down menu will be ignored.',
    )

    @field_serializer('api_token', when_used='json')
    def dump_secret(self, v):
        return v.get_secret_value()

    @property
    def model_technical_name(self):
        return ModelAliases[self.model]


class ProcessNewFilesInput(BaseModel):
    """Data for processing new files activity."""

    upload_id: str = Field(
        ...,
        description='Unique identifier for the project associated with the action.',
    )
    user_id: str = Field(
        ..., description='Unique identifier for the user who initiated the action.'
    )
    result_path: list[str] = Field(
        ..., description='Paths to the new entries to be processed.'
    )


class CleanupInput(BaseModel):
    """Data for cleanup activity."""

    upload_id: str = Field(
        ...,
        description='Unique identifier for the project associated with the action.',
    )
    user_id: str = Field(
        ..., description='Unique identifier for the user who initiated the action.'
    )
    pdfs: list[str] = Field(..., description='Paths to the PDF files to be removed.')
