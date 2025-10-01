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
import plotly.graph_objects as go
from nomad.units import ureg


def get_reference(upload_id, entry_id):
    return f'../uploads/{upload_id}/archive/{entry_id}#data'


def get_entry_id_from_file_name(file_name, archive):
    from nomad.utils import hash

    return hash(archive.metadata.upload_id, file_name)


def create_archive(entity, archive, file_name) -> str:
    import json

    from nomad.datamodel.context import ClientContext

    if isinstance(archive.m_context, ClientContext):
        return None
    if not archive.m_context.raw_path_exists(file_name):
        entity_entry = entity.m_to_dict(with_root_def=True)
        with archive.m_context.raw_file(file_name, 'w') as outfile:
            json.dump({'data': entity_entry}, outfile)
        archive.m_context.process_updated_raw_file(file_name)
    return get_reference(
        archive.metadata.upload_id, get_entry_id_from_file_name(file_name, archive)
    )


# Helper functions to plot the device stack


def add_cuboid_edges(fig, x0, x1, y0, y1, z0, z1):  # noqa: PLR0913
    """
    Creates a Scatter3d trace with lines connecting the cuboid's edges
    and adds it to 'fig' to provide a wireframe look.
    """
    corners = [
        (x0, y0, z0),  # 0
        (x0, y1, z0),  # 1
        (x1, y1, z0),  # 2
        (x1, y0, z0),  # 3
        (x0, y0, z1),  # 4
        (x0, y1, z1),  # 5
        (x1, y1, z1),  # 6
        (x1, y0, z1),  # 7
    ]
    edges = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),  # bottom face
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),  # top face
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7),  # verticals
    ]

    edge_x, edge_y, edge_z = [], [], []
    for start_i, end_i in edges:
        (xs, ys, zs) = corners[start_i]
        (xe, ye, ze) = corners[end_i]
        # Add the start/end of each edge plus None to break the line
        edge_x.extend([xs, xe, None])
        edge_y.extend([ys, ye, None])
        edge_z.extend([zs, ze, None])

    # Add lines for edges
    fig.add_trace(
        go.Scatter3d(
            x=edge_x,
            y=edge_y,
            z=edge_z,
            mode='lines',
            line=dict(color='black', width=3),
            showlegend=False,
            hoverinfo='skip',
        )
    )


def format_value(label, value, preferred_unit=None, fmt='.1f'):
    """Formats a value for display, handling both floats and pint quantities with compact units."""
    if value is None:
        return f'{label} = N/A<br>'

    elif isinstance(value, ureg.Quantity):
        if preferred_unit:
            value = value.to(preferred_unit)
        return f'{label} = {value:~{fmt}}<br>'  # Uses Pint's '~' for compact units

    else:  # Assume a float
        return f'{label} = {value:{fmt}}{f" {preferred_unit}" if preferred_unit else ""}<br>'


def create_cell_stack_figure(  # noqa: PLR0913
    layers,
    thicknesses,
    colors,
    efficiency,
    voc,
    jsc,
    ff,
    opacities=1,
    x_min=0,
    x_max=10,
    y_min=0,
    y_max=10,
):
    """
    Builds and returns a Plotly 3D figure showing the device stack.

    :param layers: list of layer names (top to bottom or bottom to top)
    :param thicknesses: list of thickness values corresponding to each layer
    :param colors: list of colors (one per layer)
    :param efficiency: device efficiency (%)
    :param voc: open-circuit voltage
    :param jsc: short-circuit current
    :param ff: fill factor
    :param x_min, x_max, y_min, y_max: 2D footprint of each layer
    :return: A Plotly Figure object
    """
    fig = go.Figure()

    # Ensure opacities is a list of the same length as layers
    if isinstance(opacities, int | float):
        opacities = [opacities] * len(layers)

    z_current = 0
    for layer_name, thickness, color, opacity in zip(
        layers, thicknesses, colors, opacities
    ):
        z0 = z_current
        z1 = z_current + thickness

        # 8 corner points for Mesh3d
        x_corners = [x_min, x_min, x_min, x_min, x_max, x_max, x_max, x_max]
        y_corners = [y_min, y_min, y_max, y_max, y_min, y_min, y_max, y_max]
        z_corners = [z0, z1, z0, z1, z0, z1, z0, z1]

        # Add the cuboid block
        fig.add_trace(
            go.Mesh3d(
                x=x_corners,
                y=y_corners,
                z=z_corners,
                color=color,
                opacity=opacity,
                alphahull=1,
                name=layer_name,
                showlegend=True,
                hoverinfo='name',
            )
        )

        # Add black wireframe around this cuboid
        add_cuboid_edges(fig, x_min, x_max, y_min, y_max, z0, z1)

        z_current = z1

    # Create an annotation for device parameters
    annotation_text = (
        '<b>Device Parameters</b><br>'
        + format_value('Efficiency', efficiency, fmt='.3f')
        + format_value('V<sub>OC</sub>', voc, preferred_unit='V', fmt='.1f')
        + format_value('J<sub>SC</sub>', jsc, preferred_unit='mA/cm²', fmt='.1f')
        + format_value('FF', ff, fmt='.3f').replace('<br>', '')
    )

    # Update layout
    fig.update_layout(
        hovermode='closest',
        legend=dict(x=0.0, y=1.0, xanchor='left', yanchor='top', traceorder='reversed'),
        scene=dict(
            xaxis=dict(visible=False, showgrid=False, zeroline=False),
            yaxis=dict(visible=False, showgrid=False, zeroline=False),
            zaxis=dict(visible=False, showgrid=False, zeroline=False),
            camera=dict(eye=dict(x=1.75, y=1.75, z=1.25)),
            dragmode='turntable',
            # aspectmode='data',
        ),
        width=800,
        height=600,
        margin=dict(r=10, l=10, b=10, t=50),
        showlegend=True,
        annotations=[
            go.layout.Annotation(
                text=annotation_text,
                align='left',
                showarrow=False,
                x=1.0,
                y=1.0,
                xref='paper',
                yref='paper',
                xanchor='right',
                yanchor='top',
                borderwidth=0,
            )
        ],
    )

    return fig
