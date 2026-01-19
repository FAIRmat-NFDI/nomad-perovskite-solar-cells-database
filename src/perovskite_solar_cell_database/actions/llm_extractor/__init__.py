from nomad.actions import TaskQueue
from pydantic import Field
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from nomad.config.models.plugins import ActionEntryPoint


class LLMExtractorActionEntryPoint(ActionEntryPoint):
    task_queue: str = Field(
        default=TaskQueue.CPU, description='Determines the task queue for this action'
    )

    def load(self):
        from nomad.actions import Action

        from perovskite_solar_cell_database.actions.llm_extractor.activities import (
            greet,
        )
        from perovskite_solar_cell_database.actions.llm_extractor.workflows import (
            ExtractWorkflow,
        )

        return Action(
            task_queue=self.task_queue,
            workflow=ExtractWorkflow,
            activities=[greet],
        )


llm_extractor_action_entry_point = LLMExtractorActionEntryPoint(
    name='LLMExtractorAction',
    description='Extract perovskite solar cell data from research papers in the upload.',
)
