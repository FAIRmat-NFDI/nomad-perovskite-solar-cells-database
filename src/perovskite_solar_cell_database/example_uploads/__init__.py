from nomad.config.models.plugins import ExampleUploadEntryPoint
from nomad.utils import strip

ions_database = ExampleUploadEntryPoint(
    title='Halide Perovskite Ions Database',
    description=strip("""
    Example upload that contains a Jupyter notebook demonstrating how to use the
    halide perovskite ions database.
    """),
    path='example_uploads/ions_database/*',
    category='PERLA (Perovskite Living Archive)',
)

perla_notebooks = ExampleUploadEntryPoint(
    title='PERLA Notebooks',
    description=strip("""
    Collection of Jupyter notebooks for comprehensive analysis of perovskite solar cell data
    from PERLA (Perovskite Living Archive). Includes workflows for data retrieval,
    performance evolution, diversity analysis, and machine learning applications.
    """),
    path='example_uploads/perla_notebooks/*',
    category='PERLA (Perovskite Living Archive)',
)
