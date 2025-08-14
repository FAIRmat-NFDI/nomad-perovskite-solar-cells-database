import numpy as np
from nomad.datamodel.data import ArchiveSection
from nomad.datamodel.metainfo.annotations import (
    ELNAnnotation,
    Filter,
    SectionProperties,
)
from nomad.datamodel.metainfo.basesections import PublicationReference
from nomad.metainfo import Quantity, Section, SubSection
from nomad.metainfo.metainfo import SchemaPackage

m_package = SchemaPackage()


class Author(ArchiveSection):
    name = Quantity(
        type=str,
        description='The full name of the author.',
    )


class Reference(PublicationReference):
    """Information about the source of the data. It describes who curated the data,
    the journal in which the data was published,
    the DOI number of the publication, the lead author and the publication date."""

    m_def = Section(a_eln=dict(lane_width='800px'))

    # DOI number and derived quantities are encapsulated in PublicationReference

    # custom fields for the tandem database
    sample_id = Quantity(
        type=str,
        shape=[],
        description="""
           ID of the device in the original data source (for traceability)
                    """,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    data_entered_by_author = Quantity(
        type=bool,
        shape=[],
        default=False,
        description="""
            TRUE if the data is formatted by the one making the device or by one the study's co-authors
            """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    name_of_person_entering_the_data = Quantity(
        type=str,
        shape=[],
        description="""
            Name of the person providing the data. For traceability-
                    """,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    free_text_comment = Quantity(
        type=str,
        shape=[],
        description="""
            Any additional description not captured by any other field.                    
            """,
        a_eln=dict(component='RichTextEditQuantity'),
    )

    part_of_initial_dataset = Quantity(
        type=bool,
        shape=[],
        default=False,
        description="""TRUE if the data is part of the original dataset""",
    )

    # Fields relevant for tracability in the original data hunt
    ID_temp = Quantity(
        type=np.dtype(np.int64),
        shape=[],
        description="""
            A temporary reference number to keep track of the devices before they are submitted to the perovskite database.
            Start with 1 and count upwards. Will in the database be replaced with a unique identifier.
                    """,
    )

    # Fields to be derived automatically
    ID = Quantity(
        type=np.dtype(np.int64),
        shape=[],
        description="""ID in the NOMAD database""",
    )

    # temporary fix for searchability of authors; should be not needed after basesections v2
    authors = SubSection(
        section_def=Author,
        repeats=True,
    )

    def normalize(self, archive, logger):
        """Normalize the reference section."""
        super().normalize(archive, logger)
        if self.publication_authors:
            self.authors = [Author(name=author) for author in self.publication_authors]


m_package.__init_metainfo__()
