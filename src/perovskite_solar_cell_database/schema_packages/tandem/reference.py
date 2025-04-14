import numpy as np
from nomad.datamodel.metainfo.basesections import PublicationReference
from nomad.metainfo import Quantity, Section


class Reference(PublicationReference):
    """Information about the source of the data. It describes who curated the data,
    the journal in which the data was published,
    the DOI number of the publication, the lead author and the publication date."""

    m_def = Section(a_eln=dict(lane_width='800px'))

    # custom fields for the tandem database

    ID_temp = Quantity(
        type=np.dtype(np.int64),
        shape=[],
        description="""
        A temporary reference number to keep track of the devices before they are submitted to the perovskite database.
        Start with 1 and count upwards. Will in the database be replaced with a unique identifier.
                    """,
    )

    ID = Quantity(
        type=np.dtype(np.int64),
        shape=[],
        description="""
                    """,
    )

    free_text_comment = Quantity(
        type=str,
        shape=[],
        description="""
    This could be anything given additional description to the cell that is not captured by any other field.
                    """,
        a_eln=dict(component='RichTextEditQuantity'),
    )

    name_of_person_entering_the_data = Quantity(
        type=str,
        shape=[],
        description="""
    Your name.
                    """,
    )

    data_entered_by_author = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if you how enter the data also was involved in making the device or if you are a co-author of the paper where the data is presented.
                    """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    def normalize(self, archive, logger):
        """Normalize the reference section."""
        super().normalize(archive, logger)
