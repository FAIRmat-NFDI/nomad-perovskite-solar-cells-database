from typing import (
    TYPE_CHECKING,
    get_args,
)

from nomad.actions.manager import get_action_result, get_action_status, start_action
from nomad.datamodel.data import UseCaseElnCategory
from nomad.datamodel.metainfo.annotations import ELNComponentEnum, SectionProperties
from nomad.datamodel.metainfo.eln import ELNAnnotation
from nomad.metainfo import Quantity, Section, SubSection
from nomad.metainfo.metainfo import MEnum

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

from nomad.datamodel.data import ArchiveSection, Schema
from nomad.metainfo import SchemaPackage

from perovskite_solar_cell_database.actions.llm_extractor.models import (
    ExtractWorkflowInput,
    ModelName,
)
from perovskite_solar_cell_database.llm_extraction_schema import (
    LLMExtractedPerovskiteSolarCell,
)

m_package = SchemaPackage()


class LlmPerovskitePaperExtractor(Schema):
    m_def = Section(
        label='LLM Perovskite Paper Extractor',
        categories=[UseCaseElnCategory],
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                order=[
                    'api_token',
                    'model',
                    'trigger_run_action',
                    'trigger_get_status',
                    'action_id',
                    'action_status',
                    'pdfs',
                    'extracted_solar_cells',
                ]
            )
        ),
    )
    api_token = Quantity(
        type=str,
        description='API token for LLM extraction',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity, props=dict(type='password')
        ),
    )
    extracted_solar_cells = Quantity(
        type=LLMExtractedPerovskiteSolarCell,
        shape=['*'],
        description='List of extracted perovskite solar cells from the paper',
    )
    model = Quantity(
        type=MEnum(
            *get_args(ModelName)
        ),  # an enum of supported model names - better way of defining model and ModelName from one constant does not work in python 3.10
        description='LLM model to use for extraction',
        default='claude-4-sonnet-20250514',
        a_eln=ELNAnnotation(component=ELNComponentEnum.EnumEditQuantity),
    )
    trigger_run_action = Quantity(
        type=bool,
        default=False,
        description="""Starts an asynchronous action for running the LLM Extraction. 
        It will search for all PDF files in the associated upload/project, extract perovskite 
        solar cells information using the specified LLM model, create and process new entries 
        for each detected solar cell, and finally delete the source PDF files.""",
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.ActionEditQuantity,
            label='Run LLM Extraction Action',
        ),
    )
    trigger_get_status = Quantity(
        type=bool,
        default=False,
        description='Retrieve the current status of the LLM Extraction action.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.ActionEditQuantity,
            label='Get Action Status',
        ),
    )
    action_id = Quantity(
        type=str,
        description='ID of the LLM Extraction action.',
    )
    action_status = Quantity(
        type=str,
        description='Status of the LLM Extraction action.',
    )
    pdfs = Quantity(
        type=str,
        shape=['*'],
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.FileEditQuantity,
            label='Upload PDF files here or directly in the associated upload/project',
        ),
        description='Upload PDF files for the extraction here or directly in the associated upload/project.',
    )

    def check_results(self, archive: 'EntryArchive', logger: 'BoundLogger'):
        """
        Checks the status of the triggered action and retrieves results if completed
        """
        if (
            self.trigger_get_status
            and self.action_id is not None
            and self.action_status == 'RUNNING'
        ):
            try:
                status = get_action_status(
                    self.action_id,  # pyright: ignore[reportArgumentType]
                    archive.metadata.authors[0].user_id,  # type: ignore
                )
                if status:
                    self.action_status = status.name
            except Exception as e:
                logger.error(
                    'Error retrieving LLM Extraction action status.', exc_info=e
                )

            if self.action_status == 'COMPLETED':
                result_refs = get_action_result(
                    self.action_id,  # pyright: ignore[reportArgumentType]
                    archive.metadata.authors[0].user_id,  # type: ignore
                )
                if result_refs is not None:
                    if result_refs.get('success'):
                        self.extracted_solar_cells = result_refs['refs']
                    else:
                        self.action_status = 'FAILED'
                        logger.error(
                            f'LLM Extraction action completed with errors: {result_refs.get("errors")}'
                        )
                else:
                    self.extracted_solar_cells = []
                    self.action_status = 'FAILED'
                    logger.error(
                        'LLM Extraction action completed but no results were found.'
                    )

    def delete_token(self, archive: 'EntryArchive', logger: 'BoundLogger'):
        """
        Deletes the token from this archive, and also from the JSON file stored on disk.
        """
        self.api_token = None
        mainfile = archive.metadata.mainfile
        with archive.m_context.update_entry(
            mainfile,  # pyright: ignore[reportArgumentType]
            write=True,
            process=False,
        ) as entry:
            try:
                del entry['data']['api_token']
            except KeyError:
                logger.warning('API token not found in the archive during deletion.')

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger'):
        from nomad.actions.manager import get_upload_files

        # read and delete api token for security reasons
        api_token = self.api_token
        if self.api_token is not None:
            self.delete_token(archive, logger)
        else:
            api_token = ''
        super().normalize(archive, logger)

        # find all pdf files already in the upload
        self.pdfs = []
        upload_files = get_upload_files(
            archive.metadata.upload_id,  # pyright: ignore[reportArgumentType]
            archive.metadata.authors[0].user_id,  # type: ignore
        )
        if upload_files is not None:
            raw_files = upload_files.raw_directory_list(
                path='',
                recursive=True,
                files_only=True,
            )
            for file_info in raw_files:
                if file_info.path.lower().endswith('.pdf'):
                    self.pdfs.append(file_info.path)

        # trigger LLM Extraction action, fill in action_id and action_status
        if self.trigger_run_action and (
            self.action_status is None
            or (self.action_id is not None and self.action_status != 'RUNNING')
        ):
            self.trigger_run_action = False
            self.action_status = 'RUNNING'
            # avoiding multiple triggers due to possible race conditions
            mainfile = archive.metadata.mainfile
            with archive.m_context.update_entry(
                mainfile,  # pyright: ignore[reportArgumentType]
                write=True,
                process=False,
            ) as entry:
                try:
                    entry['data']['trigger_run_action'] = False
                    entry['data']['action_status'] = 'RUNNING'
                except KeyError:
                    logger.warning(
                        'trigger_run_action not found in the archive during reset.'
                    )

            input_data = ExtractWorkflowInput(
                upload_id=archive.metadata.upload_id,  # pyright: ignore[reportArgumentType]
                user_id=archive.metadata.authors[0].user_id,  # type: ignore
                api_token=api_token,  # pyright: ignore[reportArgumentType]
                model=self.model,  # pyright: ignore[reportArgumentType]
            )

            try:
                action_id = start_action(
                    action_id='perovskite_solar_cell_database.actions:llm_extractor_action_entry_point',
                    data=input_data,
                )
                self.action_id = action_id
                logger.info(f'LLM Extraction action started with ID: {action_id}')
            except Exception as e:
                self.action_status = 'FAILED'
                logger.error('Error starting LLM Extraction action.', exc_info=e)

        self.check_results(archive, logger)
        self.trigger_get_status = False
        self.trigger_run_action = False


m_package.__init_metainfo__()
