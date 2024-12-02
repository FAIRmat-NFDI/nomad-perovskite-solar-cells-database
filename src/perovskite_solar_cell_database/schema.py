from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    pass

from nomad.datamodel.data import Schema, UseCaseElnCategory, ArchiveSection
from nomad.metainfo import SchemaPackage, Section, SubSection, Quantity, Datetime
import numpy as np

from .schema_sections import (
    EQE,
    ETL,
    HTL,
    JV,
    Add,
    Backcontact,
    Cell,
    Encapsulation,
    Module,
    Outdoor,
    Perovskite,
    PerovskiteDeposition,
    Ref,
    Stabilised,
    Stability,
    Substrate,
)

m_package = SchemaPackage()


class PerovskiteSolarCell(Schema):
    """
    This schema is adapted to map the data in the [Perovskite Solar Cell Database
    Project](https://www.perovskitedatabase.com/). The descriptions in the quantities
    represent the instructions given to the user who manually curated the data.
    """

    m_def = Section(
        label='Perovskite Solar Cell',
        a_eln=dict(lane_width='400px'),
        categories=[UseCaseElnCategory],
    )

    ref = SubSection(section_def=Ref)
    cell = SubSection(section_def=Cell)
    module = SubSection(section_def=Module)
    substrate = SubSection(section_def=Substrate)
    etl = SubSection(section_def=ETL)
    perovskite = SubSection(section_def=Perovskite)
    perovskite_deposition = SubSection(section_def=PerovskiteDeposition)
    htl = SubSection(section_def=HTL)
    backcontact = SubSection(section_def=Backcontact)
    add = SubSection(section_def=Add)
    encapsulation = SubSection(section_def=Encapsulation)
    jv = SubSection(section_def=JV)
    stabilised = SubSection(section_def=Stabilised)
    eqe = SubSection(section_def=EQE)
    stability = SubSection(section_def=Stability)
    outdoor = SubSection(section_def=Outdoor)


class PipelineMetrics(ArchiveSection):
    precision = Quantity(
        type=np.float32,
        description='The precision of the results calculated during pipeline design.',
    )

    recall = Quantity(
        type=np.float32,
        description='The recall of the results calculated during pipeline design.',
    )


class ModelSettings(ArchiveSection):
    temperature = Quantity(
        type=np.float32, description='The temperature setting of the LLM model.'
    )

    top_p = Quantity(type=np.float32, description='The Top P setting of the LLM model.')

    max_tokens = Quantity(
        type=int, description='The max tokens setting of the LLM model.'
    )


class LLMPipeline(ArchiveSection):
    pipeline_name = Quantity(type=str, description='The name of the LLM pipeline.')

    prompt_template = Quantity(
        type=str,
        description="""The prompt template used by these pipeline. Variables are
                        listed between curly brackets, {{}}. These variables should
                        be listed within the corresponding LLMActivity instance as
                        Quantities of type str.

                        For example:
                        How many r's are there in {{context}}?
                        """,
    )

    # steps = SubSection( # Just for visualization.
    #     section_def=Workflow,
    # )

    model_name = Quantity(
        type=str,
        description='The name and version, if possible, of the model this pipeline was calibrated against.',
    )

    settings = SubSection(
        section_def=ModelSettings,
    )

    metrics = SubSection(
        section_def=PipelineMetrics,
    )

    repository = Quantity(
        type=str,  # this can be a URL or Link check it out.
        description='The repository link pointing to a specific commit, if applicable, where the code for the pipeline exists.',
    )


class LLMExtractedPerovskiteSolarCell(PerovskiteSolarCell):
    # llm_extraction_pipeline = SubSection(section_def=BreathingPerovskiteDBPipeline)
    llm_extraction_pipeline = SubSection(section_def=LLMPipeline)

    timestamp = Quantity(
        type=Datetime,
        a_eln=dict(component='DateTimeEditQuantity'),
        description='The time when this extraction was made.',
    )

    doi = Quantity(
        type=str,
        shape=[],
        description='The DOI of the resource the solar cell was extracted from.',
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[])),
    )


m_package.__init_metainfo__()
