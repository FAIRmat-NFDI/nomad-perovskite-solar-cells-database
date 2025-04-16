from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

from itertools import cycle

from nomad.datamodel.data import Schema, UseCaseElnCategory
from nomad.datamodel.metainfo.plot import PlotlyFigure, PlotSection
from nomad.metainfo import JSON, Quantity, SchemaPackage, Section, SubSection

from perovskite_solar_cell_database.utils import create_cell_stack_figure

from .general import General
from .layer_stack import Layer
from .measurements import PerformedMeasurements
from .reference import Reference

m_package = SchemaPackage()


class PerovskiteTandemSolarCell(Schema, PlotSection):
    """
    This is schema for representing Perovskite Tandem Solar Cells.
    The descriptions in the quantities represent the instructions given to the user
    who manually curated the data.
    """

    m_def = Section(
        label='Perovskite Tandem Solar Cell',
        a_eln=dict(lane_width='400px'),
        categories=[UseCaseElnCategory],
    )

    # General information
    general = SubSection(
        section_def=General, description='General information about the device.'
    )

    # Reference
    reference = SubSection(
        section_def=Reference, description='The reference for the data in the entry.'
    )

    # Layer Stack as from tandem instructions v4.0
    layer_stack = SubSection(
        section_def=Layer,
        description='The stack of layers in the device starting from the bottom.',
        repeats=True,
    )

    # Measurements
    measurements = SubSection(
        section_def=PerformedMeasurements,
        description='The measurements performed on the device.',
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger'):
        """
        Plot the layer stack of the device and add it to the figures.
        """
        super().normalize(archive, logger)
        # A few different shades of gray for intermediate layers
        gray_shades = ['#D3D3D3', '#BEBEBE', '#A9A9A9', '#909090']
        gray_cycle = cycle(gray_shades)

        # Initialize thicknesses and colors
        thicknesses = []
        colors = []
        layer_names = []
        opacities = []

        # construct the layer stack
        for layer in self.layer_stack:
            layer_names.append(layer.name)
            if layer.functionality:
                if 'Substrate' in layer.functionality and (
                    not thicknesses or thicknesses[-1] != 1.0
                ):
                    thicknesses.append(1.0)
                    colors.append('lightblue')
                    opacities.append(1)
                elif 'Photoabsorber' in layer.functionality:
                    thicknesses.append(0.8)
                    opacities.append(1)
                    if layer.name == 'Perovskite':
                        colors.append('red')
                    elif layer.name == 'CIGS':
                        colors.append('orange')
                    elif layer.name == 'Silicon':
                        colors.append('orangered')
                    else:
                        colors.append('firebrick')
                elif 'Subcell spacer' in layer.functionality:
                    thicknesses.append(0.5)
                    colors.append('white')
                    opacities.append(0.05)
                else:
                    thicknesses.append(0.1)
                    colors.append(next(gray_cycle))
                    opacities.append(1)
            else:
                thicknesses.append(0.1)
                colors.append(next(gray_cycle))
                opacities.append(1)

        # Fetch device parameters from measurement results
        parameter_map = {
            'efficiency': 'power_conversion_efficiency',
            'voc': 'open_circuit_voltage',
            'jsc': 'short_circuit_current_density',
            'ff': 'fill_factor',
        }

        values = {key: None for key in parameter_map}
        measurement_types = [
            'jv_measurements',
            'stability_measurements',
            'performance_measurements',
        ]

        for param_key, result_attr in parameter_map.items():
            for measurement_type in measurement_types:
                measurements = getattr(self.measurements, measurement_type, [])
                for measurement in measurements:
                    if getattr(
                        measurement, 'subcell_association', None
                    ) == 0 and hasattr(measurement, 'results'):
                        value = getattr(measurement.results, result_attr, None)
                        if value is not None:
                            values[param_key] = value
                            break
                if values[param_key] is not None:
                    break

        fig = create_cell_stack_figure(
            layers=layer_names,
            thicknesses=thicknesses,
            colors=colors,
            opacities=opacities,
            **values,
            x_min=0,
            x_max=10,
            y_min=0,
            y_max=10,
        )

        self.figures = [PlotlyFigure(figure=fig.to_plotly_json())]


class RawFileTandemJson(Schema):
    """
    Section for a tandem json data file.
    """

    tandem = Quantity(type=PerovskiteTandemSolarCell)
    data = Quantity(type=JSON)


m_package.__init_metainfo__()
