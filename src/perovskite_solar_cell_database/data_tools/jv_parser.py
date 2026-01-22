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

from io import StringIO

import pandas as pd


def jv_dict_generator(filename):
    # Read file content and clean up bad characters (e.g., '²' -> '^2')
    with open(filename, encoding='cp1252') as f:
        filedata = f.read()
    cleaned_data = filedata.replace('²', '^2')

    # Parse different sections from the cleaned data
    df = pd.read_csv(
        StringIO(cleaned_data),
        skiprows=8,
        nrows=9,
        sep='\t',
        index_col=0,
        engine='python',
    )
    df_header = pd.read_csv(
        StringIO(cleaned_data),
        skiprows=0,
        nrows=6,
        sep=':|\t',
        index_col=0,
        engine='python',
    )
    df_curves = pd.read_csv(
        StringIO(cleaned_data),
        header=19,
        skiprows=[20],
        sep='\t',
        engine='python',
    )
    df_curves = df_curves.dropna(how='all', axis=1)

    list_columns = list(df.columns[0:-1])
    jv_dict = {}
    jv_dict['active_area'] = df_header.iloc[0, 1]
    jv_dict['intensity'] = df_header.iloc[1, 1]
    jv_dict['integration_time'] = df_header.iloc[2, 1]
    jv_dict['settling_time'] = df_header.iloc[3, 1]

    jv_dict['reverse_scan_Jsc'] = []
    jv_dict['reverse_scan_Voc'] = []
    jv_dict['reverse_scan_FF'] = []
    jv_dict['reverse_scan_PCE'] = []
    jv_dict['reverse_scan_Vmp'] = []
    jv_dict['reverse_scan_Jmp'] = []
    jv_dict['reverse_scan_series_resistance'] = []
    jv_dict['reverse_scan_shunt_resistance'] = []

    jv_dict['forward_scan_Jsc'] = []
    jv_dict['forward_scan_Voc'] = []
    jv_dict['forward_scan_FF'] = []
    jv_dict['forward_scan_PCE'] = []
    jv_dict['forward_scan_Vmp'] = []
    jv_dict['forward_scan_Jmp'] = []
    jv_dict['forward_scan_series_resistance'] = []
    jv_dict['forward_scan_shunt_resistance'] = []

    for i in list_columns:
        if 'rev' in i:
            jv_dict['reverse_scan_Jsc'].append(float(f'{abs(df[i].iloc[0]):0.3e}'))
            jv_dict['reverse_scan_Voc'].append(float(f'{df[i].iloc[1]:0.3e}'))
            jv_dict['reverse_scan_FF'].append(float(f'{df[i].iloc[2]:0.3e}'))
            jv_dict['reverse_scan_PCE'].append(float(f'{df[i].iloc[3]:0.3e}'))
            jv_dict['reverse_scan_Vmp'].append(float(f'{df[i].iloc[6]:0.3e}'))
            jv_dict['reverse_scan_Jmp'].append(float(f'{abs(df[i].iloc[5]):0.3e}'))
            jv_dict['reverse_scan_series_resistance'].append(
                float(f'{df[i].iloc[7]:0.3e}')
            )
            jv_dict['reverse_scan_shunt_resistance'].append(
                float(f'{df[i].iloc[8]:0.3e}')
            )

        elif 'for' in i:
            jv_dict['forward_scan_Jsc'].append(abs(float(f'{df[i].iloc[0]:0.3e}')))
            jv_dict['forward_scan_Voc'].append(float(f'{df[i].iloc[1]:0.3e}'))
            jv_dict['forward_scan_FF'].append(float(f'{df[i].iloc[2]:0.3e}'))
            jv_dict['forward_scan_PCE'].append(float(f'{df[i].iloc[3]:0.3e}'))
            jv_dict['forward_scan_Vmp'].append(float(f'{df[i].iloc[6]:0.3e}'))
            jv_dict['forward_scan_Jmp'].append(float(f'{abs(df[i].iloc[5]):0.3e}'))
            jv_dict['forward_scan_series_resistance'].append(
                float(f'{df[i].iloc[7]:0.3e}')
            )
            jv_dict['forward_scan_shunt_resistance'].append(
                float(f'{df[i].iloc[8]:0.3e}')
            )

    jv_dict['no_cells'] = len(jv_dict['reverse_scan_Jsc'])
    jv_dict['reverse_scan_Jsc'] = sum(jv_dict['reverse_scan_Jsc']) / len(
        jv_dict['reverse_scan_Jsc']
    )
    jv_dict['reverse_scan_Voc'] = sum(jv_dict['reverse_scan_Voc']) / len(
        jv_dict['reverse_scan_Voc']
    )
    jv_dict['reverse_scan_FF'] = sum(jv_dict['reverse_scan_FF']) / len(
        jv_dict['reverse_scan_FF']
    )
    jv_dict['reverse_scan_PCE'] = sum(jv_dict['reverse_scan_PCE']) / len(
        jv_dict['reverse_scan_PCE']
    )
    jv_dict['reverse_scan_Vmp'] = sum(jv_dict['reverse_scan_Vmp']) / len(
        jv_dict['reverse_scan_Vmp']
    )
    jv_dict['reverse_scan_Jmp'] = sum(jv_dict['reverse_scan_Jmp']) / len(
        jv_dict['reverse_scan_Jmp']
    )
    jv_dict['reverse_scan_series_resistance'] = sum(
        jv_dict['reverse_scan_series_resistance']
    ) / len(jv_dict['reverse_scan_series_resistance'])
    jv_dict['reverse_scan_shunt_resistance'] = sum(
        jv_dict['reverse_scan_shunt_resistance']
    ) / len(jv_dict['reverse_scan_shunt_resistance'])

    jv_dict['forward_scan_Jsc'] = sum(jv_dict['forward_scan_Jsc']) / len(
        jv_dict['forward_scan_Jsc']
    )
    jv_dict['forward_scan_Voc'] = sum(jv_dict['forward_scan_Voc']) / len(
        jv_dict['forward_scan_Voc']
    )
    jv_dict['forward_scan_FF'] = sum(jv_dict['forward_scan_FF']) / len(
        jv_dict['forward_scan_FF']
    )
    jv_dict['forward_scan_PCE'] = sum(jv_dict['forward_scan_PCE']) / len(
        jv_dict['forward_scan_PCE']
    )
    jv_dict['forward_scan_Vmp'] = sum(jv_dict['forward_scan_Vmp']) / len(
        jv_dict['forward_scan_Vmp']
    )
    jv_dict['forward_scan_Jmp'] = sum(jv_dict['forward_scan_Jmp']) / len(
        jv_dict['forward_scan_Jmp']
    )
    jv_dict['forward_scan_series_resistance'] = sum(
        jv_dict['forward_scan_series_resistance']
    ) / len(jv_dict['forward_scan_series_resistance'])
    jv_dict['forward_scan_shunt_resistance'] = sum(
        jv_dict['forward_scan_shunt_resistance']
    ) / len(jv_dict['forward_scan_shunt_resistance'])

    if jv_dict['reverse_scan_PCE'] >= jv_dict['forward_scan_PCE']:
        jv_dict['default_Jsc'] = jv_dict['reverse_scan_Jsc']
        jv_dict['default_Voc'] = jv_dict['reverse_scan_Voc']
        jv_dict['default_FF'] = jv_dict['reverse_scan_FF']
        jv_dict['default_PCE'] = jv_dict['reverse_scan_PCE']
        jv_dict['default_Voc_scan_direction'] = 'Reversed'
        jv_dict['default_Jsc_scan_direction'] = 'Reversed'
        jv_dict['default_FF_scan_direction'] = 'Reversed'
        jv_dict['default_PCE_scan_direction'] = 'Reversed'

    else:
        jv_dict['default_Jsc'] = jv_dict['forward_scan_Jsc']
        jv_dict['default_Voc'] = jv_dict['forward_scan_Voc']
        jv_dict['default_FF'] = jv_dict['forward_scan_FF']
        jv_dict['default_PCE'] = jv_dict['forward_scan_PCE']
        jv_dict['default_Voc_scan_direction'] = 'Forward'
        jv_dict['default_Jsc_scan_direction'] = 'Forward'
        jv_dict['default_FF_scan_direction'] = 'Forward'
        jv_dict['default_PCE_scan_direction'] = 'Forward'

    jv_dict['jv_curve'] = []
    for column in range(1, len(df_curves.columns)):
        jv_dict['jv_curve'].append(
            {
                'name': df_curves.columns[column],
                'voltage': df_curves[df_curves.columns[0]].values,
                'current_density': df_curves[df_curves.columns[column]].values,
            }
        )

    return jv_dict
