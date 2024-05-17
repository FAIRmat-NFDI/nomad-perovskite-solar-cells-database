import numpy as np
from nomad.datamodel.data import ArchiveSection
from nomad.metainfo import Quantity


class Module(ArchiveSection):
    """
    Specific section containing information if the reported device is a module.
    """

    Module = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if the cell is a module composed of connected individual sub cells
                    """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    number_of_cells_in_module = Quantity(
        type=np.dtype(np.int64),
        shape=[],
        description="""
    The number of cells in the module
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    area_total = Quantity(
        type=np.dtype(np.float64),
        unit=('cm**2'),
        shape=[],
        description="""
    The total area of the module in cm2. This includes scribes, contacts, boundaries, etc. and represent the module’s geometrical footprint.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    area_effective = Quantity(
        type=np.dtype(np.float64),
        unit=('cm**2'),
        shape=[],
        description="""
    The active area of the module in cm2.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    JV_data_recalculated_per_cell = Quantity(
        type=bool,
        shape=[],
        description="""
    The preferred way to report IV data for modules is to recalculate the IV data to average data per sub-cells in the module. That simplifies downstream comparisons, and it ensures that there is no erroneous transformation that otherwise may occur when error checking the IV data. Mark this as TRUE if the conversation is done.
                    """,
        a_eln=dict(component='BoolEditQuantity'),
    )
