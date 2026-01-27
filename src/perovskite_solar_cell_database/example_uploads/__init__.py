import os
import httpx
from nomad.config.models.plugins import ExampleUploadEntryPoint
from nomad.utils import strip


class PerlaNotebooksEntryPoint(ExampleUploadEntryPoint):
    """Custom entry point to handle external file download with redirects."""

    def load(self, upload_path: str):
        """Load resources with custom redirect handling for external file."""
        # First, load local resources (notebooks)
        from nomad.config.models.plugins import UploadResource

        local_resource = UploadResource(path='example_uploads/perla_notebooks/*')
        self.resolve_resource(local_resource, upload_path)

        # Download external parquet file with redirect following
        parquet_url = 'https://box.hu-berlin.de/f/62464f5f1e7b415ea697/?dl=1'
        target_path = os.path.join(
            upload_path, 'perovskite_solar_cell_database.parquet'
        )

        # Download with redirect following
        with httpx.Client(follow_redirects=True) as client:
            response = client.get(parquet_url)
            response.raise_for_status()
            with open(target_path, 'wb') as f:
                f.write(response.content)


ions_database = ExampleUploadEntryPoint(
    title='Halide Perovskite Ions Database',
    description=strip("""
    Example upload that contains a Jupyter notebook demonstrating how to use the
    halide perovskite ions database.
    """),
    path='example_uploads/ions_database/*',
    category='PERLA (Perovskite Living Archive)',
)

perla_notebooks = PerlaNotebooksEntryPoint(
    title='PERLA Notebooks',
    description=strip("""
    Collection of Jupyter notebooks for comprehensive analysis of perovskite solar cell data
    from PERLA (Perovskite Living Archive). Includes workflows for data retrieval,
    performance evolution, diversity analysis, and machine learning applications.
    """),
    category='PERLA (Perovskite Living Archive)',
)
