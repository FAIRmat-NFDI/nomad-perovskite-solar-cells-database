#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import logging
import os

import pytest
import structlog
from nomad.client import parse
from nomad.utils import structlogging
from structlog.testing import LogCapture

from perovskite_solar_cell_database.parsers.tandem_json_parser import (
    get_eln_archive_name,
)

structlogging.ConsoleFormatter.short_format = True
setattr(logging, 'Formatter', structlogging.ConsoleFormatter)


@pytest.fixture(
    name='caplog',
    scope='function',
)
def fixture_caplog(request):
    """
    Extracts log messages from the logger and raises an assertion error if the specified
    log levels in the `request.param` are found.
    """
    caplog = LogCapture()
    processors = structlog.get_config()['processors']
    old_processors = processors.copy()

    try:
        processors.clear()
        processors.append(caplog)
        structlog.configure(processors=processors)
        yield caplog
        for record in caplog.entries:
            if record['log_level'] in request.param:
                assert False, record
    finally:
        processors.clear()
        processors.extend(old_processors)
        structlog.configure(processors=processors)


@pytest.fixture(
    name='parsed_tandem_archive',
    scope='function',
)
def fixture_parsed_tandem_archive(request):
    """
    Sets up data for testing and cleans up after the test. The data file is parsed,
    returning an `EntryArchive` object. It contains a reference to the `.archive.json`
    file created by plugin parsers for the tandem data. Parsing this
    `.archive.json` file returns the `EntryArchive` object for the tandem data,
    which is finally yeilded to the test function.
    """
    rel_file_path = request.param
    file_archive = parse(rel_file_path)[0]
    directory, file_name = os.path.split(rel_file_path)
    rel_tandem_archive_path = os.path.join(directory, get_eln_archive_name(file_name))
    assert file_archive.data.tandem.m_proxy_value == os.path.abspath(
        rel_tandem_archive_path
    )

    yield parse(rel_tandem_archive_path)[0]

    if os.path.exists(rel_tandem_archive_path):
        os.remove(rel_tandem_archive_path)
