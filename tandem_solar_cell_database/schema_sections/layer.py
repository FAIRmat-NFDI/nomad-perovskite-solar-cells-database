import numpy as np
from nomad.metainfo import Quantity, Datetime, Section, MEnum
from nomad.datamodel.data import ArchiveSection


class Layer(ArchiveSection):
    """'
    Information about the layer in the tandem device
    """

    m_def = Section(a_eln=dict(lane_width='800px'))

    functionality = Quantity(
        type=MEnum(
            'Absorber',
            'Anti reflective coating',
            'Back contact',
            'Back reflector',
            'Beam splitter',
            'Buffer layer',
            'Down conversion',
            'Encapsulant',
            'ETL',
            'Front contact',
            'HTL',
            'Self assembled monolayer',
            'Subcell spacer',
            'Substrate',
            'Upconversion',
            'Window layer',
        ),
        shape=[],
        description="""
        The functionality of the layer in the tandem device. Examples: absorber, ETL, HTL, etc.
        Silicon, perovskite, CIGS, etc. are examples of absorbers.
                    """,
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[])),
    )

    thickness = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='nm',
        description="""
        The thickness of the layer in the tandem device. Examples: 100, 200, 300
                    """,
        a_eln=dict(component='FloatEditQuantity'),
    )

    def normalize(self, archive, logger):
        from nomad.datamodel.datamodel import EntryMetadata
        import requests
        import dateutil.parser

        pass
