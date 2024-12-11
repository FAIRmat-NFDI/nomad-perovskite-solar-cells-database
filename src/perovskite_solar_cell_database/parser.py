import time

import numpy as np
import pandas as pd
from nomad.datamodel import EntryArchive
from nomad.parsing import MatchingParser

from perovskite_solar_cell_database.composition import (
    PerovskiteAIon,
    PerovskiteBIon,
    PerovskiteXIon,
)
from perovskite_solar_cell_database.utils import create_archive


class IonParser(MatchingParser):
    def parse(
        self,
        mainfile: str,
        archive: EntryArchive,
        logger=None,
        child_archives: dict[str, EntryArchive] = None,
    ) -> None:
        df = pd.read_excel(mainfile).replace(np.nan, None)
        for index, row in df.iterrows():
            if row['perovskite_site'] == 'A':
                ion = PerovskiteAIon()
            elif row['perovskite_site'] == 'B':
                ion = PerovskiteBIon()
            elif row['perovskite_site'] == 'X':
                ion = PerovskiteXIon()
            else:
                raise ValueError(f'Unknown ion type {row["perovskite_site"]}')
            ion.abbreviation = row['abbreviation']
            ion.molecular_formula = row['molecular_formula']
            ion.smiles = row['smiles']
            ion.common_name = row['common_name']
            ion.iupac_name = row['iupac_name']
            ion.cas_number = row['cas_number']
            ion.source_compound_iupac_name = row['source_compound_iupac_name']
            ion.source_compound_smiles = row['source_compound_smiles']
            ion.source_compound_cas_number = row['source_compound_cas_number']
            time.sleep(1)  # Waiting to avoid rate limiting
            create_archive(
                ion, archive, f'{row["abbreviation"]}_perovskite_ion.archive.json'
            )
