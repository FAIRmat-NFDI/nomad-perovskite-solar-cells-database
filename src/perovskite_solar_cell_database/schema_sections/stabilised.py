import numpy as np
from nomad.datamodel.data import ArchiveSection
from nomad.metainfo import Quantity


class Stabilised(ArchiveSection):
    """
    A section describing if a stabilised efficiency has been measured in the solar cell.
    """

    performance_measured = Quantity(
        type=bool,
        shape=[],
        description="""
    TRUE if a stabilised cell efficiency has been measured
- A stabilised efficiency requires a continuous measurement. Measuring an IV-curve, storing the cell in the dark for a while, and then measure a new IV-curve does thus not count as a stabilised efficiency measurement.
                    """,
        a_eln=dict(component='BoolEditQuantity'),
    )

    performance_procedure = Quantity(
        type=str,
        shape=[],
        description="""
    The Potentiostatic load condition during the stabilised performance measurement
Examples:
Constant current
Constant potential
MPPT
Passive resistance
Short circuit
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    'MPPT',
                    'Constant potential',
                    'Constant Potential',
                    'Constant current',
                ]
            ),
        ),
    )

    performance_procedure_metrics = Quantity(
        type=str,
        shape=[],
        description="""
    The metrics associated to the load condition in the previous filed
- For measurement under constant current, state the current in mA/cm2
- For measurement under constant potential. State the potential in V
- For a measurement under constant resistive load, state the resistance in ohm
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    '',
                    '0.8',
                    '0.82',
                    '0.885',
                    '0.99',
                    '0.64',
                    '0.91',
                    '0.757',
                    '0.97',
                    '0.76',
                    '0.92',
                    '0.7959999999999999',
                    '0.895',
                    '0.96',
                    '1.19',
                    '0.85',
                    '0.94',
                    '0.61',
                    '0.83',
                    '1.31',
                    '0.87',
                    '0.9',
                    '0.86',
                    '0.78',
                    '0.93',
                    '0.74',
                    '0.79',
                    '0.867',
                    '0.98',
                    '0.73',
                    '1.3',
                    '0.8140000000000001',
                    '0.8740000000000001',
                    '0.8590000000000001',
                    '1.23',
                    '0.81',
                    '0.818',
                    '0.71',
                    '0.75',
                    '1.0',
                    '0.62',
                    '0.66',
                    '0.88',
                    '0.84',
                    '0.95',
                    '0.72',
                    '0.77',
                    '1.35',
                ]
            ),
        ),
    )

    performance_measurement_time = Quantity(
        type=np.dtype(np.float64),
        unit=('minute'),
        shape=[],
        description="""
    The duration of the stabilised performance measurement.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    performance_PCE = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description="""
    The stabilised efficiency, PCE
- Give the efficiency in %
- If there are uncertainties, only state the best estimate, e.g. write 20.5 and not 19-20
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    performance_Vmp = Quantity(
        type=np.dtype(np.float64),
        unit=('V'),
        shape=[],
        description="""
    The stabilised Vmp
- Give Vmp in volts [V]
- If there are uncertainties, only state the best estimate, e.g. write 1.03 and not 1.01-1.05
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    performance_Jmp = Quantity(
        type=np.dtype(np.float64),
        unit=('mA/cm**2'),
        shape=[],
        description="""
    The stabilised Jmp
- Give Jmp in mA/cm2
- If there are uncertainties, only state the best estimate, e.g. write 20.5 and not 19-20
- If unknown or not applicable, leave this field empty.
                    """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    performance_link_raw_data = Quantity(
        type=str,
        shape=[],
        description="""
    A link to where the data file for the stability measurement is stored
- This is a beta feature. The plan is to create a file repository where the raw files for IV data can be stored and disseminated. With the link and associated protocols, it should be possible to programmatically access and analyse the raw IV-data.
                    """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=['', 'false', 'www.testsite…']),
        ),
    )
