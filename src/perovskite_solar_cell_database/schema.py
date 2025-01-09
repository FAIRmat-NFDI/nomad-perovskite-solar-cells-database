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
from .utils import create_cell_stack_figure

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

        fig = create_cell_stack_figure(
            layers=layers,
            thicknesses=thicknesses,
            colors=colors,
            efficiency=efficiency,
            voc=voc,
            jsc=jsc,
            ff=ff,
            x_min=0,
            x_max=10,
            y_min=0,
            y_max=10,
        )

        self.figures = [PlotlyFigure(figure=fig.to_plotly_json())]


m_package.__init_metainfo__()
