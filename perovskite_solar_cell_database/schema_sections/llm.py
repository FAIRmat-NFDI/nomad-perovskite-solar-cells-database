import numpy as np
from nomad.metainfo import (
    Quantity, Datetime, Section)
from nomad.datamodel.data import ArchiveSection
class LLM(ArchiveSection):
    """Information about the source of the data. It describes who curated the data,
     the journal in which the data was published,
     the DOI number of the publication, the lead author and the publication date."""

    m_def = Section(
        a_eln=dict(lane_width='800px'))

    doi = Quantity(
        type=str,
        shape=[],
        description="""
    The DOI number referring to the published paper or dataset where the data can be found. If the data is unpublished, enter “Unpublished”
Examples:
10.1021/jp5126624
10.1016/j.electacta.2017.06.032
Unpublished
                    """,
        a_eln=dict(
            component='FileEditQuantity'))


    def normalize(self, archive, logger):
        pass

        
