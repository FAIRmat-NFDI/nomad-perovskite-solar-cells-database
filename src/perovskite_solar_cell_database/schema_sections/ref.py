import numpy as np
from nomad.datamodel.data import ArchiveSection
from nomad.metainfo import Datetime, Quantity, Section


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
                given_name = temp_dict['message']['author'][0]['given']
                familiy_name = temp_dict['message']['author'][0]['family']
                self.journal = temp_dict['message']['container-title'][0]
                self.publication_date = dateutil.parser.parse(
                    temp_dict['message']['created']['date-time']
                )
                self.lead_author = given_name + ' ' + familiy_name
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
