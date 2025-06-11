import os

import pytest
from nomad.client import normalize_all, parse
from nomad.config import config

test_files = [
    'Json_data_tandem_cell_initial_data_0.archive.json',
]
log_levels = ['error', 'critical']


@pytest.mark.parametrize(
    'test_file',
    [(file) for file in test_files],
    ids=[os.path.basename(file) for file in test_files],
)
def test_normalize_all(test_file):
    """
    test normalization of the parsed archive
    """
    test_file_path = os.path.join(os.path.dirname(__file__), 'data', test_file)
    parsed_tandem_archive = parse(test_file_path)[0]
    normalize_all(parsed_tandem_archive)

    assert (
        parsed_tandem_archive.data.key_performance_metrics.fill_factor
        == pytest.approx(0.1267, rel=1e-3)
    )
