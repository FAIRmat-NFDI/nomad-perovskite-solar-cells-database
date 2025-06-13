import logging
import os

import pytest
import structlog
from nomad.client import normalize_all, parse
from nomad.config import config
from nomad.datamodel.metainfo.plot import PlotlyFigure
from nomad.utils import structlogging
from structlog.testing import LogCapture

structlogging.ConsoleFormatter.short_format = True
setattr(logging, 'Formatter', structlogging.ConsoleFormatter)

test_files = [
    'Json_data_tandem_cell_initial_data_0.archive.json',
    'Json_data_tandem_cell_initial_data_522.archive.json',
]
log_levels = ['error', 'critical']
values_for_comparison_dicts = [
    {'number_of_layers': 11, 'fill_factor': 0.1267},
    {'number_of_layers': 18, 'fill_factor': 0.074},
]


@pytest.mark.parametrize(
    'test_file, value_for_comparison_dict',
    [
        (file, values_dict)
        for file, values_dict in zip(test_files, values_for_comparison_dicts)
    ],
    ids=[os.path.basename(file) for file in test_files],
)
def test_normalize_all(test_file, value_for_comparison_dict):
    """
    set up test logging
    """

    caplog = LogCapture()
    processors = structlog.get_config()['processors']
    old_processors = processors.copy()
    processors.clear()
    processors.append(caplog)
    structlog.configure(processors=processors)

    """
    test normalization of the parsed archive
    """

    test_file_path = os.path.join(os.path.dirname(__file__), 'data', test_file)
    parsed_tandem_archive = parse(test_file_path)[0]
    normalize_all(parsed_tandem_archive)

    assert (
        parsed_tandem_archive.data.general.number_of_layers
        == value_for_comparison_dict['number_of_layers']
    )
    assert parsed_tandem_archive.data.general.stack_sequence is not None
    assert (
        parsed_tandem_archive.data.key_performance_metrics.fill_factor
        == pytest.approx(value_for_comparison_dict['fill_factor'], rel=1e-3)
    )
    assert len(parsed_tandem_archive.data.figures) > 0
    assert all(
        isinstance(fig, PlotlyFigure) for fig in parsed_tandem_archive.data.figures
    )

    """
    check the logging for the events of set level and clean up
    """

    for record in caplog.entries:
        if record['log_level'] in log_levels:
            assert False, record
    processors.clear()
    processors.extend(old_processors)
    structlog.configure(processors=processors)
