from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

from itertools import cycle

# import numpy as np
from nomad.datamodel.data import Schema, UseCaseElnCategory
from nomad.datamodel.metainfo.plot import PlotlyFigure, PlotSection
from nomad.metainfo import JSON, Quantity, SchemaPackage, Section, SubSection

from perovskite_solar_cell_database.utils import create_cell_stack_figure

# from .layer_stack import Layer
from .device_stack import DeviceStack
from .encapsulation_data import EncapsulationData
from .general import General
from .key_performance_metrics import KeyPerformanceMetrics
from .measurements import PerformedMeasurements
from .module_data import ModuleData
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

    # Key performance metrics
    key_performance_metrics = SubSection(
        section_def=KeyPerformanceMetrics,
        description='Key performance metrics.'
    )

    # The Device stack
    device_stack = SubSection(
        section_def=DeviceStack,
        description='Description of the device stack and all layers in it',             
    )  

    # Measurements
    measurements = SubSection(
        section_def=PerformedMeasurements,
        description='The measurements performed on the device.',
    )

    # Module data
    module_data = SubSection(
        section_def=ModuleData,
        description='Module specific data',
    )

    # Encapsulation data
    encapsulation_data = SubSection(
        section_def=EncapsulationData,
        description='Encapsulation specific data',
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger'):
        """
        Populate the key performance metrics section
        """
        super().normalize(archive, logger)
        
        ######## The device stack
        stack_seq = getattr(getattr(self, "device_stack", None), "stack_sequence", None)
        if stack_seq is not None:
            if self.general is None:
                self.general = General()
            self.general.stack_sequence = stack_seq 
              
        ####### Key performance metrics   
        # Identify the PCE from all IV measurements
        pce = []
        pce_index = []    
            
        # Check if there are JV measurements 
        if hasattr(self, 'measurements') and hasattr(self.measurements, 'jv'):
            # Go through all JV measurements
            for i, measurement in enumerate(self.measurements.jv):
                # Check that the JV measuremtn is done under standard light conditions
                if getattr(measurement, 'device_subset', None) == 0 and \
                getattr(measurement, 'light_regime', None) == 'standard_light':
                    # Extract the PCE if it excist
                    results = getattr(measurement, 'results', None)
                    pce_value = getattr(results, 'power_conversion_efficiency', None)
                    if pce_value is not None:
                        pce.append(pce_value)
                        pce_index.append(i)
        
        # Identify the JV measurement with the highest PCE
        if pce:
            i_best_pce = pce_index[pce.index(max(pce))]

            if self.key_performance_metrics is None:
                self.key_performance_metrics = KeyPerformanceMetrics()

            # Add the identified best PCE measurement to the key performance metrics
            self.key_performance_metrics.power_conversion_efficiency = \
                self.measurements.jv[i_best_pce].results.power_conversion_efficiency    

            # Add additional values from that JV scan if they excisit
            if hasattr(self.measurements.jv[i_best_pce].results, 'short_circuit_current_density'):
                self.key_performance_metrics.short_circuit_current_density = \
                    self.measurements.jv[i_best_pce].results.short_circuit_current_density 

            if hasattr(self.measurements.jv[i_best_pce].results, 'open_circuit_voltage'):
                self.key_performance_metrics.open_circuit_voltage = \
                    self.measurements.jv[i_best_pce].results.open_circuit_voltage
                    
            if hasattr(self.measurements.jv[i_best_pce].results, 'fill_factor'):
                self.key_performance_metrics.fill_factor = \
                    self.measurements.jv[i_best_pce].results.fill_factor
                    
            if hasattr(self.measurements.jv[i_best_pce].results, 'maximum_power_point_voltage'):
                self.key_performance_metrics.maximum_power_point_voltage = \
                    self.measurements.jv[i_best_pce].results.maximum_power_point_voltage
                    
            if hasattr(self.measurements.jv[i_best_pce].results, 'maximum_power_point_current_density'):        
                self.key_performance_metrics.maximum_power_point_current_density = \
                    self.measurements.jv[i_best_pce].results.maximum_power_point_current_density
                      
        # Identify the PCE from all stabilised performance measurements
        pce = []
        pce_index = []    
           
        # Check if there are stabilised performance measurements 
        if hasattr(self, 'measurements') and hasattr(self.measurements, 'stabilized_performance'):
            # Go through all stabilised  measurements
            for i, measurement in enumerate(self.measurements.stabilized_performance):
                # Check that the measurement is done under standard light conditions
                if getattr(measurement, 'device_subset', None) == 0 and \
                getattr(measurement, 'light_regime', None) == 'standard_light':
                    # Extract the PCE if it excist
                    results = getattr(measurement, 'results', None)
                    pce_value = getattr(results, 'power_conversion_efficiency', None)
                    if pce_value is not None:
                        pce.append(pce_value)
                        pce_index.append(i)

        if pce:
            i_best_pce = pce_index[pce.index(max(pce))]

            if self.key_performance_metrics is None:
                self.key_performance_metrics = KeyPerformanceMetrics()

            self.key_performance_metrics.power_conversion_efficiency_stabilized = \
                self.measurements.stabilized_performance[i_best_pce].results.power_conversion_efficiency   
                
        # Stability data
        # Check if stability measurements exist
        if hasattr(self, 'measurements') and hasattr(self.measurements, 'stability'):
            # Go through all JV measurements
            for i, measurement in enumerate(self.measurements.stability):        
                pce_1000h = getattr(getattr(measurement, "results", None), "power_conversion_efficiency_1000h", None)
                T80 = getattr(getattr(measurement, "results", None), "T80", None)

                if pce_1000h is not None or T80 is not None:
                    # Make sure key_performance_metrics exists
                    if self.key_performance_metrics is None:
                        self.key_performance_metrics = KeyPerformanceMetrics()

                # ISOS-L1 conditions
                if getattr(measurement, "stability_protocol", None) == "ISOS-L-1":
                    current_best = getattr(self.key_performance_metrics, "pce_1000h_isos_l1", None)
                    if current_best is None or pce_1000h > current_best:
                        self.key_performance_metrics.pce_1000h_isos_l1 = pce_1000h

                    current_best = getattr(self.key_performance_metrics, "T80_isos_l1", None)
                    if current_best is None or T80 > current_best:
                        self.key_performance_metrics.T80_isos_l1 = T80

                # ISOS-L3 conditions
                if getattr(measurement, "stability_protocol", None) == "ISOS-L-3":
                    current_best = getattr(self.key_performance_metrics, "pce_1000h_isos_l3", None)
                    if current_best is None or pce_1000h > current_best:
                        self.key_performance_metrics.pce_1000h_isos_l3 = pce_1000h

                    current_best = getattr(self.key_performance_metrics, "T80_isos_l3", None)
                    if current_best is None or T80 > current_best:
                        self.key_performance_metrics.T80_isos_l3 = T80

       
        ####### Figure of the device stack
        #  Plot the layer stack of the device and add it to the figures.

        # A few different shades of gray for intermediate layers
        gray_shades = ['#D3D3D3', '#BEBEBE', '#A9A9A9', '#909090']
        gray_cycle = cycle(gray_shades)

        # Initialize thicknesses and colors
        thicknesses = []
        colors = []
        layer_names = []
        opacities = []

        # construct the layer stack
        if getattr(self, 'device_stack', None) and getattr(self.device_stack, "layers", None):        
            for layer in self.device_stack.layers:
                # Check if the layer has a name
                name = getattr(layer, 'name', '-')
                layer_names.append(name)
                
                functionality = getattr(layer, 'functionality', None)
                if functionality == "substrate": 
                    thicknesses.append(1.0)
                    colors.append('lightblue')
                    opacities.append(1)
                elif functionality == 'photoabsorber':
                    thicknesses.append(0.8)
                    opacities.append(1)
                    colors.append('firebrick')
                    if name == 'Perovskite':
                        colors.append('red')
                    elif name == 'CIGS':
                        colors.append('orange')
                    elif name == 'Silicon':
                        colors.append('orangered')
                    else:
                        colors.append('firebrick')
                elif functionality == 'air_gap':
                    thicknesses.append(0.5)
                    colors.append('white')
                    opacities.append(0.05)
                elif functionality == 'optical_spacer':
                    thicknesses.append(0.5)
                    colors.append('white')
                    opacities.append(0.05)    
                else:
                    thicknesses.append(0.1)
                    colors.append(next(gray_cycle))
                    opacities.append(1)

        # Check if the key performance metrics section has values
        values = {
            'efficiency': getattr(self.key_performance_metrics, 'power_conversion_efficiency', None),
            'voc': getattr(self.key_performance_metrics, 'open_circuit_voltage', None),
            'jsc': getattr(self.key_performance_metrics, 'short_circuit_current_density', None),
            'ff': getattr(self.key_performance_metrics, 'fill_factor', None),
        }
        
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
