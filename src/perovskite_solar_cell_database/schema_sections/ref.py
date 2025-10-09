import numpy as np
from nomad.datamodel.data import ArchiveSection
from nomad.metainfo import Datetime, Quantity, Section
from nomad.metainfo.metainfo import MEnum, SchemaPackage, SubSection

m_package = SchemaPackage()


class Author(ArchiveSection):
    name = Quantity(
        type=str,
        description='The full name of the author, typically a combination of first and last name.',
    )
    first_name = Quantity(
        type=str,
        description='The first name of the author.',
    )
    last_name = Quantity(
        type=str,
        description='The last name of the author.',
    )

    def normalize(self, archive, logger):
        if not self.name and self.first_name and self.last_name:
            self.name = f'{self.first_name} {self.last_name}'
        super().normalize(archive, logger)


class Ref(ArchiveSection):
    """Information about the source of the data. It describes who curated the data,
    the journal in which the data was published,
    the DOI number of the publication, the lead author and the publication date."""

    m_def = Section(a_eln=dict(lane_width='800px'))

    internal_sample_id = Quantity(
        type=str,
        shape=[],
        description="""
    This is your own unique cell identifier. With this text string alone, you should be able to identify this cell in your own internal data management system.
                    """,
        a_eln=dict(component='StringEditQuantity'),
    )

    free_text_comment = Quantity(
        type=str,
        shape=[],
        description="""
    This could be anything given additional description to the cell that is not captured by any other field.
                    """,
        a_eln=dict(component='RichTextEditQuantity'),
    )

    ID = Quantity(
        type=np.dtype(np.int64),
        shape=[],
        description="""
                    """,
    )

    ID_temp = Quantity(
        type=np.dtype(np.int64),
        shape=[],
        description="""
                    """,
    )

    # Add in the future auto filling from metadata.author
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

    DOI_number = Quantity(
        type=str,
        shape=[],
        description="""
    The DOI number referring to the published paper or dataset where the data can be found. If the data is unpublished, enter “Unpublished”
Examples:
10.1021/jp5126624
10.1016/j.electacta.2017.06.032
Unpublished
                    """,
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[])),
    )

    lead_author = Quantity(
        type=str,
        shape=[],
        description="""
    The surname of the first author. If several authors, end with et al. If the DOI number is given correctly, this will be extracted automatically from www.crossref.org
                    """,
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[])),
    )

    authors = SubSection(
        section_def=Author,
        repeats=True,
    )

    publication_date = Quantity(
        type=Datetime,
        shape=[],
        description="""
    Publication date. If the DOI number is given correctly, this will be extracted automatically from www.crossref.org
                    """,
    )

    journal = Quantity(
        type=str,
        shape=[],
        description="""
    nan
                    """,
    )

    part_of_initial_dataset = Quantity(
        type=bool,
        shape=[],
        description="""
    nan
                    """,
    )

    original_filename_data_upload = Quantity(
        type=str,
        shape=[],
        description="""
    nan
                    """,
    )

    extraction_method = Quantity(
        type=MEnum(
            'Author', 'Perovskite Database Project', 'LLM', 'LLM Reviewed by Human'
        ),
        description='How the solar cell data was extracted from the publication.',
    )

    def normalize(self, archive, logger):
        import dateutil.parser
        import requests
        from nomad.datamodel.datamodel import EntryMetadata

        # Parse journal name, lead author and publication date from crossref
        if self.DOI_number:
            if not self.ID_temp:
                r = requests.get(f'https://api.crossref.org/works/{self.DOI_number}')
                temp_dict = r.json()
                # make sure the doi has the prefix https://doi.org/
                if self.DOI_number.startswith('10.'):
                    self.DOI_number = 'https://doi.org/' + self.DOI_number
                message = temp_dict.get('message', {})
                given_name = message.get('author', [{}])[0].get('given', '')
                family_name = message.get('author', [{}])[0].get('family', '')
                self.journal = message.get('container-title', [None])[0]
                self.publication_date = dateutil.parser.parse(
                    message.get('created', {}).get('date-time', None)
                )
                self.lead_author = given_name + ' ' + family_name
                self.authors = [
                    Author(
                        first_name=author.get('given', None),
                        last_name=author.get('family', None),
                        name=author.get('given', '') + ' ' + author.get('family', ''),
                    )
                    for author in message.get('author', [])
                ]
            if not archive.metadata:
                archive.metadata = EntryMetadata()
            if not archive.metadata.references:
                archive.metadata.references = []
                archive.metadata.references.append(self.DOI_number)
                if self.ID_temp is not None:
                    archive.metadata.references.append(
                        'https://doi.org/10.1038/s41560-021-00941-3'
                    )
                    archive.metadata.references.append(
                        'https://www.perovskitedatabase.com/'
                    )
                    archive.metadata.external_db = 'The Perovskite Database Project'
            for i, ref in enumerate(archive.metadata.references):
                if ref.startswith('10.'):
                    archive.metadata.references[i] = 'https://doi.org/' + ref


m_package.__init_metainfo__()
