import numpy as np
from nomad.metainfo import Quantity, Datetime, Section
from nomad.datamodel.data import ArchiveSection


class Tandem(ArchiveSection):
    """Information about the full tandem device"""

    m_def = Section(a_eln=dict(lane_width='800px'))

    architecture = Quantity(
        type=str,
        shape=[],
        description="""
    The architecture of the tandem device. Examples: 2-terminal, 4-terminal, monolithic, mechanically stacked, etc.
                    """,
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[])),
    )

    number_of_terminals = Quantity(
        type=np.dtype(np.int64),
        shape=[],
        description="""
    The number of terminals of the tandem device. Examples: 2, 4
                    """,
        a_eln=dict(component='IntEditQuantity'),
    )

    number_of_junctions = Quantity(
        type=np.dtype(np.int64),
        shape=[],
        description="""
    The number of junctions in the tandem device. Examples: 2, 3, 4
                    """,
        a_eln=dict(component='IntEditQuantity'),
    )

    absorbers_technology = Quantity(
        type=str,
        shape=['*'],
        description="""
    The technology of the absorbers in the tandem device. Examples: perovskite, CIGS, silicon, etc.
                    """,
        a_eln=dict(component='EnumEditQuantity', props=dict(suggestions=[])),
    )

    absorbers_bandgap = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description="""
    The bandgap of the absorbers in the tandem device. Examples: 1.6, 1.8, 2.0
                    """,
        a_eln=dict(component='FloatEditQuantity'),
    )

    flexible = Quantity(
        type=bool,
        shape=[],
        description="""
    Whether the tandem device is flexible or not.
                    """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    semitransparent = Quantity(
        type=bool,
        shape=[],
        description="""
    Whether the tandem device is semitransparent or not.
                    """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    def normalize(self, archive, logger):
        from nomad.datamodel.datamodel import EntryMetadata
        import requests
        import dateutil.parser

        pass
