from typing import (
    TYPE_CHECKING,
    get_args,
)

from nomad.actions.manager import get_action_result, get_action_status, start_action
from nomad.datamodel.data import UseCaseElnCategory
from nomad.datamodel.metainfo.annotations import ELNComponentEnum
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


class ActionStatus(ArchiveSection):
    """Section to fetch the status of an LLM Extraction action."""

    action_id = Quantity(
        type=str,
        description='ID of the LLM Extraction action.',
    )
    status = Quantity(
        type=str,
        description='Status of the LLM Extraction action.',
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger'):
        super().normalize(archive, logger)


class LlmPerovskitePaperExtractor(Schema):
    m_def = Section(
        label='LLM Perovskite Paper Extractor',
        categories=[UseCaseElnCategory],
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
        description='Starts an asynchronous action for running the LLM Extraction.',
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
    triggered_action = SubSection(
        section_def=ActionStatus,
        description='A section for storing the status of the triggered action.',
    )

    def check_results(self, archive: 'EntryArchive', logger: 'BoundLogger'):
        if (
            self.trigger_get_status
            and self.triggered_action
            and self.triggered_action.action_id
            and self.triggered_action.status != 'COMPLETED'
        ):
            self.trigger_get_status = False

            try:
                status = get_action_status(
                    self.triggered_action.action_id,  # pyright: ignore[reportArgumentType]
                    archive.metadata.authors[0].user_id,  # type: ignore
                )
                if status:
                    self.triggered_action.status = status.name
            except Exception as e:
                logger.error(
                    'Error retrieving LLM Extraction action status.', exc_info=e
                )

            if self.triggered_action.status == 'COMPLETED':
                result_refs = get_action_result(
                    self.triggered_action.action_id,  # pyright: ignore[reportArgumentType]
                    archive.metadata.authors[0].user_id,  # type: ignore
                )
                if result_refs is not None:
                    self.extracted_solar_cells = result_refs['refs']
                else:
                    self.extracted_solar_cells = []
                    self.triggered_action.status = (
                        'COMPLETED // FAILED TO RETRIEVE RESULTS'
                    )
                    logger.warning(
                        'LLM Extraction action completed but no results were found.'
                    )

        self.trigger_get_status = False

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
        api_token = self.api_token
        if self.api_token is not None:
            self.delete_token(archive, logger)
        super().normalize(archive, logger)

        if self.trigger_run_action:
            self.trigger_run_action = False

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
                self.triggered_action = ActionStatus(
                    action_id=action_id,
                    status='RUNNING',
                )
            except Exception as e:
                logger.error('Error starting LLM Extraction action.', exc_info=e)

        self.check_results(archive, logger)


m_package.__init_metainfo__()
