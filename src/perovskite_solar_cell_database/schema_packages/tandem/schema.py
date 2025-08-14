import re
from typing import (
    TYPE_CHECKING,
)

from nomad.atomutils import (
    Formula,
)
from nomad.datamodel.metainfo.common import ProvenanceTracker
from nomad.datamodel.results import (
    BandGap,
    ElectronicProperties,
    ElementalComposition,
    Material,
    OptoelectronicProperties,
    Properties,
    Relation,
    Results,
    SolarCell,
    System,
)
from nomad.normalizing.topology import add_system, add_system_info

from perovskite_solar_cell_database.composition import PerovskiteIonComponent

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

from itertools import cycle

from nomad.datamodel.data import Schema, UseCaseElnCategory
from nomad.datamodel.metainfo.plot import PlotlyFigure, PlotSection
from nomad.metainfo import JSON, Quantity, SchemaPackage, Section, SubSection

from perovskite_solar_cell_database.schema_packages.tandem.device_stack import (
    Layer,
    Photoabsorber,
    Photoabsorber_CIGS,
    Photoabsorber_CZTS,
    Photoabsorber_DSSC,
    Photoabsorber_GaAs,
    Photoabsorber_OPV,
    Photoabsorber_Perovskite,
    Photoabsorber_QuantumDot,
    Photoabsorber_Silicon,
    PhotoabsorberOther,
)
from perovskite_solar_cell_database.schema_packages.tandem.encapsulation_data import (
    EncapsulationData,
)
from perovskite_solar_cell_database.schema_packages.tandem.general import General
from perovskite_solar_cell_database.schema_packages.tandem.key_performance_metrics import (
    KeyPerformanceMetrics,
)
from perovskite_solar_cell_database.schema_packages.tandem.measurements import (
    PerformedMeasurements,
)
from perovskite_solar_cell_database.schema_packages.tandem.module_data import ModuleData
from perovskite_solar_cell_database.schema_packages.tandem.reference import Reference
from perovskite_solar_cell_database.utils import create_cell_stack_figure

m_package = SchemaPackage()


class PerovskiteTandemSolarCell(Schema, PlotSection):
    """
    This is schema for representing Perovskite Tandem Solar Cells.
    The descriptions in the quantities represent the instructions given to the user
    who manually curated the data.
    """

    m_def = Section(
        label='Perovskite Tandem Solar Cell',
        a_eln=dict(lane_width='600px'),
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
        section_def=KeyPerformanceMetrics, description='Key performance metrics.'
    )

    # The Device stack
    device_stack = SubSection(
        section_def=Layer,
        description='The stack of layers in the device starting from the bottom.',
        repeats=True,
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

    def make_plotly_figure(self):
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
        if self.device_stack:
            for layer in self.device_stack:
                # Check if the layer has a name
                name = getattr(layer, 'name', '-')
                layer_names.append(name)

                functionality = layer.functionality
                if functionality == 'substrate':
                    thicknesses.append(1.0)
                    colors.append('lightblue')
                    opacities.append(1)
                elif functionality == 'photoabsorber':
                    thicknesses.append(0.8)
                    opacities.append(1)
                    if name in ['Perovskite', 'perovskite']:
                        colors.append('red')
                    elif name in ['CIGS', 'cigs']:
                        colors.append('orange')
                    elif name in ['Silicon', 'silicon']:
                        colors.append('darkblue')
                    elif name in ['OPV', 'opv']:
                        colors.append('darkgreen')
                    elif name in ['GaAs', 'gaas']:
                        colors.append('lightgreen')
                    else:
                        colors.append('firebrick')
                elif functionality == 'air gap':
                    thicknesses.append(0.5)
                    colors.append('white')
                    opacities.append(0.05)
                elif functionality == 'optical spacer':
                    thicknesses.append(0.5)
                    colors.append('white')
                    opacities.append(0.05)
                else:
                    thicknesses.append(0.1)
                    colors.append(next(gray_cycle))
                    opacities.append(1)

        # Check if the key performance metrics section has values
        values = {
            'efficiency': self.key_performance_metrics.power_conversion_efficiency,
            'voc': self.key_performance_metrics.open_circuit_voltage,
            'jsc': self.key_performance_metrics.short_circuit_current_density,
            'ff': self.key_performance_metrics.fill_factor,
        }

        fig = create_cell_stack_figure(
            layers=layer_names,
            thicknesses=thicknesses,
            colors=colors,
            opacities=opacities,
            **values,
            x_min=0,
            x_max=5,
            y_min=0,
            y_max=5,
        )

        return fig

    def create_system_from_layer(
        self,
        layer: Photoabsorber,
        logger: 'BoundLogger',
        layer_name: str,
        layer_formula='',
    ) -> System:
        system = System(
            label=f'{layer_name} Layer',
            description=f'{layer_name} layer in the tandem solar cell.',
        )
        if layer_formula != '':
            formula = Formula(layer_formula)
            formula.populate(system, overwrite=True)
        elif hasattr(layer, 'molecular_formula') and layer.molecular_formula:
            formula = Formula(layer.molecular_formula)
            formula.populate(system, overwrite=True)
        else:
            logger.warn(
                f'Could not find chemical formula for {layer_name} layer {layer.layer_index}.'
            )
        return system

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger'):
        """
        Populate the key performance metrics section
        """
        super().normalize(archive, logger)

        ######## The device stack
        if self.device_stack:
            # Number of layers
            if self.general is None:
                self.general = General()
            self.general.number_of_layers = len(self.device_stack)

            # The stack sequence
            stack_sequence = []
            for i, layer in enumerate(self.device_stack):
                # Check if the layer has a name
                name = layer.name
                if name is not None:
                    stack_sequence.append(name)
                else:
                    stack_sequence.append('-')

                # Change layer class to PhotoabsorberOther if needed
                if layer.functionality == 'photoabsorber' and type(layer) is Layer:
                    m_dict = layer.m_to_dict()
                    self.device_stack[i] = PhotoabsorberOther(**m_dict)

            if stack_sequence:
                self.general.stack_sequence = ' | '.join(stack_sequence)

            # Layer index
            for i, layer in enumerate(self.device_stack):
                self.device_stack[i].layer_index = i + 1

        ####### Key performance metrics
        # Identify the PCE from all IV measurements.
        pce = []
        pce_index = []

        # Check if there are JV measurements
        if self.measurements and self.measurements.jv:
            # Go through all JV measurements
            for i, measurement in enumerate(self.measurements.jv):
                # Check that the JV measuremtn is done under standard light conditions
                if (
                    measurement.device_subset == 0
                    and measurement.light_regime == 'standard light'
                ):
                    # Extract the PCE if it exists
                    if measurement.results is not None:
                        pce_value = measurement.results.power_conversion_efficiency
                        if pce_value is not None:
                            pce.append(pce_value)
                            pce_index.append(i)

        # Identify the JV measurement with the highest PCE
        if pce:
            i_best_pce = pce_index[pce.index(max(pce))]

            if self.key_performance_metrics is None:
                self.key_performance_metrics = KeyPerformanceMetrics()

            # Add the identified best PCE measurement to the key performance metrics
            self.key_performance_metrics.power_conversion_efficiency = (
                self.measurements.jv[i_best_pce].results.power_conversion_efficiency
            )

            # Add additional values from that JV scan if they excisit
            if self.measurements.jv[i_best_pce].results.short_circuit_current_density:
                self.key_performance_metrics.short_circuit_current_density = (
                    self.measurements.jv[
                        i_best_pce
                    ].results.short_circuit_current_density
                )

            if self.measurements.jv[i_best_pce].results.open_circuit_voltage:
                self.key_performance_metrics.open_circuit_voltage = (
                    self.measurements.jv[i_best_pce].results.open_circuit_voltage
                )

            if self.measurements.jv[i_best_pce].results.fill_factor:
                self.key_performance_metrics.fill_factor = self.measurements.jv[
                    i_best_pce
                ].results.fill_factor

            if self.measurements.jv[i_best_pce].results.maximum_power_point_voltage:
                self.key_performance_metrics.maximum_power_point_voltage = (
                    self.measurements.jv[i_best_pce].results.maximum_power_point_voltage
                )

            if self.measurements.jv[
                i_best_pce
            ].results.maximum_power_point_current_density:
                self.key_performance_metrics.maximum_power_point_current_density = (
                    self.measurements.jv[
                        i_best_pce
                    ].results.maximum_power_point_current_density
                )

        # Identify the PCE from all stabilised performance measurements
        pce = []
        pce_index = []

        # Check if there are stabilised performance measurements
        if self.measurements and self.measurements.stabilized_performance:
            # Go through all stabilised  measurements
            for i, measurement in enumerate(self.measurements.stabilized_performance):
                # Check that the measurement is done under standard light conditions
                if (
                    measurement.device_subset == 0
                    and measurement.light_regime == 'standard light'
                ):
                    # Extract the PCE if it excist
                    if measurement.results is not None:
                        pce_value = measurement.results.power_conversion_efficiency
                        if pce_value is not None:
                            pce.append(pce_value)
                            pce_index.append(i)

        if pce:
            i_best_pce = pce_index[pce.index(max(pce))]

            if self.key_performance_metrics is None:
                self.key_performance_metrics = KeyPerformanceMetrics()

            self.key_performance_metrics.power_conversion_efficiency_stabilized = (
                self.measurements.stabilized_performance[
                    i_best_pce
                ].results.power_conversion_efficiency
            )

        # Stability data
        # Check if stability measurements exist
        if self.measurements and self.measurements.stability:
            # Go through all JV measurements
            for i, measurement in enumerate(self.measurements.stability):
                pce_1000h = measurement.results.power_conversion_efficiency_end
                pce_start = measurement.results.power_conversion_efficiency_start
                T80 = measurement.results.T80

                if pce_1000h is not None or T80 is not None:
                    # Make sure key_performance_metrics exists
                    if self.key_performance_metrics is None:
                        self.key_performance_metrics = KeyPerformanceMetrics()

                # ISOS-L1 conditions
                if measurement.stability_protocol == 'ISOS-L-1':
                    current_best = self.key_performance_metrics.pce_1000h_isos_l1_end
                    if current_best is None or pce_1000h > current_best:
                        self.key_performance_metrics.pce_1000h_isos_l1_end = pce_1000h

                        if pce_start is not None:
                            self.key_performance_metrics.pce_1000h_isos_l1_start = (
                                pce_start
                            )

                    current_best = self.key_performance_metrics.t80_isos_l1
                    if current_best is None or T80 > current_best:
                        self.key_performance_metrics.t80_isos_l1 = T80

                # ISOS-L3 conditions
                if measurement.stability_protocol == 'ISOS-L-3':
                    current_best = self.key_performance_metrics.pce_1000h_isos_l3_end
                    if current_best is None or pce_1000h > current_best:
                        self.key_performance_metrics.pce_1000h_isos_l3_end = pce_1000h

                        if pce_start is not None:
                            self.key_performance_metrics.pce_1000h_isos_l3_start = (
                                pce_start
                            )

                    current_best = self.key_performance_metrics.t80_isos_l3
                    if current_best is None or T80 > current_best:
                        self.key_performance_metrics.t80_isos_l3 = T80

        fig = self.make_plotly_figure()

        self.figures = [PlotlyFigure(figure=fig.to_plotly_json())]

        # creating topology - root level
        topology = {}
        tandem_system = System(
            label='Tandem Solar Cell',
            description='A system describing the tandem solar cell.',
            system_relation=Relation(type='root'),
        )
        add_system(tandem_system, topology)
        add_system_info(tandem_system, topology)

        # adding nested topology systems
        for layer in self.device_stack:
            if (
                isinstance(layer, Photoabsorber_Perovskite)
                and layer.composition is not None
            ):
                system = layer.composition.to_topology_system(logger=logger)
                system.label = 'Perovskite Layer'
                system.description = 'A perovskite layer in the tandem solar cell.'
                system.dimensionality = layer.composition.dimensionality
                add_system(system, topology, parent=tandem_system)
                add_system_info(system, topology)
                ions: list[PerovskiteIonComponent] = (
                    layer.composition.ions_a_site
                    + layer.composition.ions_b_site
                    + layer.composition.ions_x_site
                )
                for ion in ions:
                    child_system = ion.to_topology_system()
                    add_system(child_system, topology, system)
                    add_system_info(child_system, topology)

            elif isinstance(layer, Photoabsorber_Silicon):
                system = self.create_system_from_layer(
                    layer=layer, logger=logger, layer_name='Silicon', layer_formula='Si'
                )
                system.dimensionality = '3D'
                system.structural_type = 'bulk'
                add_system(system, topology, parent=tandem_system)
                add_system_info(system, topology)
            elif isinstance(layer, Photoabsorber_CIGS):
                system = self.create_system_from_layer(
                    layer=layer, logger=logger, layer_name='CIGS'
                )
                system.dimensionality = '3D'
                system.structural_type = 'bulk'
                add_system(system, topology, parent=tandem_system)
                add_system_info(system, topology)
            elif isinstance(layer, Photoabsorber_CZTS):
                system = self.create_system_from_layer(
                    layer=layer, logger=logger, layer_name='CZTS'
                )
                system.dimensionality = '3D'
                system.structural_type = 'bulk'
                add_system(system, topology, parent=tandem_system)
                add_system_info(system, topology)
            elif isinstance(layer, Photoabsorber_GaAs):
                system = self.create_system_from_layer(
                    layer=layer, logger=logger, layer_name='GaAs'
                )
                system.dimensionality = '3D'
                system.structural_type = 'bulk'
                add_system(system, topology, parent=tandem_system)
                add_system_info(system, topology)
            elif isinstance(layer, Photoabsorber_OPV):
                system = System(
                    label='OPV Layer',
                    description='OPV layer in the tandem solar cell.',
                )
                add_system(system, topology, parent=tandem_system)
                add_system_info(system, topology)
            elif isinstance(layer, Photoabsorber_DSSC):
                system = System(
                    label='DSSC Layer',
                    description='DSSC layer in the tandem solar cell.',
                )
                add_system(system, topology, parent=tandem_system)
                add_system_info(system, topology)
            elif isinstance(layer, Photoabsorber_QuantumDot):
                system = System(
                    label='QD Layer',
                    description='QD layer in the tandem solar cell.',
                )
                add_system(system, topology, parent=tandem_system)
                add_system_info(system, topology)
            elif isinstance(layer, PhotoabsorberOther):
                system = System(
                    label='Other Photoabsorber Layer',
                    description='Other photoabsorber layer in the tandem solar cell.',
                )
                add_system(system, topology, parent=tandem_system)
                add_system_info(system, topology)

        if not archive.results:
            archive.results = Results()
        if not archive.results.material:
            archive.results.material = Material()

        # populating the root level of topology
        elements_already_added = []
        descriptive_formula_str = ''
        for system in topology.values():
            if (
                system.parent_system
                and system.parent_system == 'results/material/topology/0'
            ):
                for element in system.elemental_composition:
                    if element.element not in elements_already_added:
                        tandem_system.elemental_composition.append(
                            ElementalComposition(
                                element=element.element,
                                mass=element.mass,
                            )
                        )  # pyright: ignore[reportOptionalCall]
                        elements_already_added.append(element.element)

                if descriptive_formula_str != '':
                    descriptive_formula_str += ' | '
                if system.chemical_formula_descriptive:
                    descriptive_formula_str += system.chemical_formula_descriptive
                else:
                    descriptive_formula_str += re.sub(
                        r' Layer(?!.* Layer)', '', system.label
                    )
        tandem_system.chemical_formula_descriptive = descriptive_formula_str
        tandem_system.elements = sorted(elements_already_added)
        tandem_system.structural_type = 'not processed'

        # populating archive.materials from the root level of topology
        archive.results.material.chemical_formula_descriptive = (
            tandem_system.chemical_formula_descriptive
        )
        archive.results.material.elemental_composition = (
            tandem_system.elemental_composition
        )
        archive.results.material.elements = tandem_system.elements

        for system in topology.values():
            archive.results.material.m_add_sub_section(Material.topology, system)

        if not archive.results.properties:
            archive.results.properties = Properties()

        band_gaps = []
        for layer in self.device_stack:
            if layer.functionality == 'photoabsorber':
                try:
                    band_gap_value = layer.properties.band_gap.value
                    band_gaps.append(
                        BandGap(
                            value=band_gap_value,
                            provenance=ProvenanceTracker(
                                label=f'layer index {layer.layer_index} - {layer.name}'
                            ),
                            label=layer.name,
                        )
                    )
                except Exception as e:
                    logger.warn(
                        f'No band gap value found for layer {layer.layer_index}',
                        exc_info=e,
                    )

        # populate electronic properties
        if band_gaps:
            archive.results.properties.electronic = ElectronicProperties(
                band_gap=band_gaps
            )

        # populate optoelectronic properties
        if not archive.results.properties.optoelectronic:
            archive.results.properties.optoelectronic = OptoelectronicProperties()
        result_device_stack = []
        result_absorber = []
        result_electron_transport_layer = []
        result_hole_transport_layer = []
        result_back_contact = []
        result_substrate = []

        for layer in self.device_stack:
            result_device_stack.append(layer.name)
            if layer.functionality == 'photoabsorber':
                result_absorber.append(layer.name)
            if layer.functionality == 'electron transport layer':
                result_electron_transport_layer.append(layer.name)
            if layer.functionality == 'hole transport layer':
                result_hole_transport_layer.append(layer.name)
            if layer.functionality == 'back contact':
                result_back_contact.append(layer.name)
            if layer.functionality == 'substrate':
                result_substrate.append(layer.name)

        result_solar_cell = SolarCell(
            efficiency=self.key_performance_metrics.power_conversion_efficiency,
            fill_factor=self.key_performance_metrics.fill_factor,
            open_circuit_voltage=self.key_performance_metrics.open_circuit_voltage,
            short_circuit_current_density=self.key_performance_metrics.short_circuit_current_density,
            device_area=self.general.active_area,
            device_stack=result_device_stack,
            absorber=result_absorber,
            electron_transport_layer=result_electron_transport_layer,
            hole_transport_layer=result_hole_transport_layer,
            back_contact=result_back_contact,
            substrate=result_substrate,
        )

        archive.results.properties.optoelectronic.solar_cell = result_solar_cell


class RawFileTandemJson(Schema):
    """
    Section for a tandem json data file.
    """

    tandem = Quantity(type=PerovskiteTandemSolarCell)
    data = Quantity(type=JSON)


m_package.__init_metainfo__()
