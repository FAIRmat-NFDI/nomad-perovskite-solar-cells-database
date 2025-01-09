from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    pass

import plotly.graph_objects as go
from nomad.datamodel.data import Schema, UseCaseElnCategory
from nomad.datamodel.metainfo.plot import PlotlyFigure, PlotSection
from nomad.metainfo import SchemaPackage, Section, SubSection

from .schema_sections import (
    EQE,
    ETL,
    HTL,
    JV,
    Add,
    Backcontact,
    Cell,
    Encapsulation,
    Module,
    Outdoor,
    Perovskite,
    PerovskiteDeposition,
    Ref,
    Stabilised,
    Stability,
    Substrate,
)

m_package = SchemaPackage()


class PerovskiteSolarCell(Schema, PlotSection):
    """
    This schema is adapted to map the data in the [Perovskite Solar Cell Database
    Project](https://www.perovskitedatabase.com/). The descriptions in the quantities
    represent the instructions given to the user who manually curated the data.
    """

    m_def = Section(
        label='Perovskite Solar Cell',
        a_eln=dict(lane_width='800px'),
        categories=[UseCaseElnCategory],
    )

    ref = SubSection(section_def=Ref)
    cell = SubSection(section_def=Cell)
    module = SubSection(section_def=Module)
    substrate = SubSection(section_def=Substrate)
    etl = SubSection(section_def=ETL)
    perovskite = SubSection(section_def=Perovskite)
    perovskite_deposition = SubSection(section_def=PerovskiteDeposition)
    htl = SubSection(section_def=HTL)
    backcontact = SubSection(section_def=Backcontact)
    add = SubSection(section_def=Add)
    encapsulation = SubSection(section_def=Encapsulation)
    jv = SubSection(section_def=JV)
    stabilised = SubSection(section_def=Stabilised)
    eqe = SubSection(section_def=EQE)
    stability = SubSection(section_def=Stability)
    outdoor = SubSection(section_def=Outdoor)

    def normalize(self, archive, logger):
        super().normalize(archive, logger)

        # Example list of layers (top to bottom)
        layers = self.cell.stack_sequence.split(' | ')

        # A few different shades of gray for intermediate layers
        gray_shades = ['#D3D3D3', '#BEBEBE', '#A9A9A9', '#909090']
        gray_index = 0  # We'll increment this when we use a gray

        # Initialize thicknesses and colors
        thicknesses = []
        colors = []

        for i, layer in enumerate(layers):
            if i == 0:
                thicknesses.append(1.0)
                colors.append('lightblue')
            elif 'Perovskite' in layer:
                thicknesses.append(0.5)
                colors.append('red')
            elif i == len(layers) - 1:
                thicknesses.append(0.1)
                colors.append('orange')
            else:
                thicknesses.append(0.1)
                # Pick a gray from the list, cycle through if needed
                colors.append(gray_shades[gray_index % len(gray_shades)])
                gray_index += 1

        # Device parameters
        efficiency = self.jv.default_PCE
        voc = self.jv.default_Voc
        jsc = self.jv.default_Jsc
        ff = self.jv.default_FF

        # X/Y extents (same for all layers)
        x_min, x_max = 0, 10
        y_min, y_max = 0, 10

        fig = go.Figure()

        # Helper function to add the black "wireframe" around each cuboid
        def add_cuboid_edges(fig, x0, x1, y0, y1, z0, z1):  # noqa: PLR0913
            """
            Creates a Scatter3d trace with lines connecting the cuboid's edges.
            """
            # List of the 8 corners of the cuboid
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
            # Each pair represents an edge between two corners
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

            edge_x = []
            edge_y = []
            edge_z = []

            for start_i, end_i in edges:
                (xs, ys, zs) = corners[start_i]
                (xe, ye, ze) = corners[end_i]
                # Add the start and end of each edge plus None to break the line
                edge_x.extend([xs, xe, None])
                edge_y.extend([ys, ye, None])
                edge_z.extend([zs, ze, None])

            # Add a Scatter3d trace to draw the edges
            fig.add_trace(
                go.Scatter3d(
                    x=edge_x,
                    y=edge_y,
                    z=edge_z,
                    mode='lines',
                    line=dict(color='black', width=3),
                    showlegend=False,  # Don't clutter the legend with edge lines
                    hoverinfo='skip',  # Avoid hover on edges
                )
            )

        z_current = 0
        for layer_name, thickness, color in zip(layers, thicknesses, colors):
            z0 = z_current
            z1 = z_current + thickness

            # 8 corner points of the cuboid for Mesh3d
            x_corners = [x_min, x_min, x_min, x_min, x_max, x_max, x_max, x_max]
            y_corners = [y_min, y_min, y_max, y_max, y_min, y_min, y_max, y_max]
            z_corners = [z0, z1, z0, z1, z0, z1, z0, z1]

            # Create a solid shape (cuboid) using Mesh3d
            fig.add_trace(
                go.Mesh3d(
                    x=x_corners,
                    y=y_corners,
                    z=z_corners,
                    color=color,
                    alphahull=1,
                    name=layer_name,
                    showlegend=True,
                    hoverinfo='name',
                )
            )

            # Now add the "wireframe" edges on top:
            add_cuboid_edges(fig, x_min, x_max, y_min, y_max, z0, z1)

            z_current = z1

        # Use HTML <sub> for subscripts in the device parameters
        annotation_text = (
            f'<b>Device Parameters</b><br>'
            f'Efficiency = {efficiency}%<br>'
            f'V<sub>OC</sub> = {voc} <br>'
            f'J<sub>SC</sub> = {jsc} <br>'
            f'FF = {ff}%'
        )

        # Configure the layout and annotation (no border box)
        fig.update_layout(
            title_text='3D Perovskite Device Stack',
            legend=dict(x=0.0, y=1.0, xanchor='left', yanchor='top'),
            scene=dict(
                xaxis=dict(visible=False, showgrid=False, zeroline=False),
                yaxis=dict(visible=False, showgrid=False, zeroline=False),
                zaxis=dict(visible=False, showgrid=False, zeroline=False),
                camera=dict(eye=dict(x=1.4, y=1.4, z=1.0)),
            ),
            width=800,
            height=600,
            margin=dict(r=20, l=20, b=20, t=60),
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

        self.figures = [PlotlyFigure(figure=fig.to_plotly_json())]


m_package.__init_metainfo__()
