import math
import os.path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nomad.datamodel.data import (
        ArchiveSection,
    )
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )


def get_reference(upload_id: str, entry_id: str) -> str:
    return f'../uploads/{upload_id}/archive/{entry_id}#data'


def get_entry_id_from_file_name(file_name: str, archive: 'EntryArchive') -> str:
    from nomad.utils import hash

    return hash(archive.metadata.upload_id, file_name)


def create_archive(
    entity: 'ArchiveSection',
    archive: 'EntryArchive',
    file_name: str,
) -> str:
    import json

    from nomad.datamodel.context import ClientContext

    entity_entry = entity.m_to_dict(with_root_def=True)
    if isinstance(archive.m_context, ClientContext):
        with open(file_name, 'w') as outfile:
            json.dump({'data': entity_entry}, outfile, indent=4)
        return os.path.abspath(file_name)
    if not archive.m_context.raw_path_exists(file_name):
        with archive.m_context.raw_file(file_name, 'w') as outfile:
            json.dump({'data': entity_entry}, outfile)
        archive.m_context.process_updated_raw_file(file_name)
    return get_reference(
        archive.metadata.upload_id, get_entry_id_from_file_name(file_name, archive)
    )
