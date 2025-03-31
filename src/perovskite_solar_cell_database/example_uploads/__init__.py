from nomad.config.models.plugins import ExampleUploadEntryPoint
from nomad.utils import strip

getting_started = ExampleUploadEntryPoint(
    title='Using ions database',
    description=strip("""
    Example upload that contains a Jupyter notebooks demonstrating how to use the 
    ions database.
    """),
    path='example_uploads/ions_database/*',
    category='Perovskite database',
)
