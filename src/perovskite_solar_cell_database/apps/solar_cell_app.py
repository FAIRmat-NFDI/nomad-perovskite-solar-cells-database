import yaml

solar_cell_app = yaml.safe_load(
    """
label: Solar Cells
path: solarcells
category: Solar cells
description: Search general solar cells
readme: 'This page allows you to search **solar cell data**
  within NOMAD. The filter menu on the left and the shown
  default columns are specifically designed for solar cell
  exploration. The dashboard directly shows useful
  interactive statistics about the data.'
filters:
  include:
  - '*#perovskite_solar_cell_database.schema.PerovskiteSolarCell'
  exclude:
  - mainfile
  - entry_name
  - combine
filters_locked:
  sections: nomad.datamodel.results.SolarCell
pagination:
  order_by: results.properties.optoelectronic.solar_cell.efficiency
search_syntaxes:
  exclude:
  - free_text
columns:
  selected:
  - results.material.chemical_formula_descriptive
  - results.properties.optoelectronic.solar_cell.efficiency
  - results.properties.optoelectronic.solar_cell.open_circuit_voltage
  - results.properties.optoelectronic.solar_cell.short_circuit_current_density
  - results.properties.optoelectronic.solar_cell.fill_factor
  - references
  options:
    results.material.chemical_formula_descriptive: {label: Descriptive formula}
    results.properties.optoelectronic.solar_cell.efficiency:
      format:
        decimals: 2
        mode: standard
      label: Efficiency (%)
    results.properties.optoelectronic.solar_cell.open_circuit_voltage:
      format:
        decimals: 3
        mode: standard
      unit: V
    results.properties.optoelectronic.solar_cell.short_circuit_current_density:
      format:
        decimals: 3
        mode: standard
      unit: A/m**2
    results.properties.optoelectronic.solar_cell.fill_factor:
      format:
        decimals: 3
        mode: standard
    references: {}
    results.material.chemical_formula_hill:
      label: Formula
    results.material.structural_type: {}
    results.properties.optoelectronic.solar_cell.illumination_intensity:
      format:
        decimals: 3
        mode: standard
      label: Illum. intensity
      unit: W/m**2
    results.eln.lab_ids: {}
    results.eln.sections: {}
    results.eln.methods: {}
    results.eln.tags: {}
    results.eln.instruments: {}
    entry_name: {label: Name}
    entry_type: {}
    mainfile: {}
    upload_create_time: {label: Upload time}
    authors: {}
    comment: {}
    datasets: {}
    published: {label: Access}
filter_menus:
  options:
    material:
      label: Absorber Material
    elements:
      label: Elements / Formula
      level: 1
      size: xl
    structure:
      label: Structure / Symmetry
      level: 1
    electronic:
      label: Electronic Properties
    solarcell:
      label: Solar Cell Properties
    eln:
      label: Electronic Lab Notebook
    custom_quantities:
      label: User Defined Quantities
      size: l
    author:
      label: Author / Origin / Dataset
      size: m
    metadata:
      label: Visibility / IDs / Schema
    optimade:
      label: Optimade
      size: m
dashboard:
  widgets:
  - layout:
      lg: {h: 8, minH: 8, minW: 12, w: 12, x: 0, y: 0}
      md: {h: 8, minH: 8, minW: 12, w: 12, x: 0, y: 0}
      sm: {h: 8, minH: 8, minW: 12, w: 12, x: 0, y: 16}
      xl: {h: 8, minH: 8, minW: 12, w: 12, x: 0, y: 0}
      xxl: {h: 8, minH: 8, minW: 12, w: 13, x: 0, y: 0}
    quantity: results.material.elements
    scale: linear
    type: periodictable
  - autorange: true
    layout:
      lg: {h: 6, minH: 3, minW: 3, w: 12, x: 0, y: 8}
      md: {h: 6, minH: 3, minW: 3, w: 9, x: 0, y: 8}
      sm: {h: 5, minH: 3, minW: 3, w: 6, x: 0, y: 0}
      xl: {h: 8, minH: 3, minW: 3, w: 9, x: 12, y: 0}
      xxl: {h: 8, minH: 3, minW: 3, w: 12, x: 24, y: 0}
    markers:
      color:
        quantity: results.properties.optoelectronic.solar_cell.short_circuit_current_density
        unit: 'mA/cm^2'
    size: 1000
    type: scatterplot
    x:
      quantity: results.properties.optoelectronic.solar_cell.open_circuit_voltage
    y:
      quantity: results.properties.optoelectronic.solar_cell.efficiency
      title: 'Efficiency (%)'
  - autorange: true
    layout:
      lg: {h: 6, minH: 3, minW: 3, w: 12, x: 0, y: 14}
      md: {h: 6, minH: 3, minW: 3, w: 9, x: 9, y: 8}
      sm: {h: 5, minH: 3, minW: 3, w: 6, x: 6, y: 0}
      xl: {h: 8, minH: 3, minW: 3, w: 9, x: 21, y: 0}
      xxl: {h: 8, minH: 3, minW: 3, w: 11, x: 13, y: 0}
    markers:
      color:
        quantity: results.properties.optoelectronic.solar_cell.device_architecture
    size: 1000
    type: scatterplot
    x:
      quantity: results.properties.optoelectronic.solar_cell.open_circuit_voltage
    y:
      quantity: results.properties.optoelectronic.solar_cell.efficiency
      title: 'Efficiency (%)'
  - layout:
      lg: {h: 6, minH: 3, minW: 3, w: 6, x: 12, y: 0}
      md: {h: 4, minH: 3, minW: 3, w: 6, x: 12, y: 4}
      sm: {h: 6, minH: 3, minW: 3, w: 4, x: 0, y: 10}
      xl: {h: 6, minH: 3, minW: 3, w: 6, x: 14, y: 8}
      xxl: {h: 6, minH: 3, minW: 3, w: 6, x: 14, y: 8}
    quantity: results.properties.optoelectronic.solar_cell.device_stack
    scale: linear
    showinput: true
    type: terms
  - autorange: true
    layout:
      lg: {h: 4, minH: 3, minW: 3, w: 12, x: 12, y: 12}
      md: {h: 3, minH: 3, minW: 3, w: 8, x: 10, y: 17}
      sm: {h: 3, minH: 3, minW: 3, w: 8, x: 4, y: 13}
      xl: {h: 3, minH: 3, minW: 3, w: 8, x: 0, y: 11}
      xxl: {h: 3, minH: 3, minW: 3, w: 8, x: 0, y: 8}
    nbins: 30
    quantity: results.properties.optoelectronic.solar_cell.illumination_intensity
    scale: 1/4
    showinput: true
    type: histogram
  - layout:
      lg: {h: 6, minH: 3, minW: 3, w: 6, x: 18, y: 0}
      md: {h: 4, minH: 3, minW: 3, w: 6, x: 12, y: 0}
      sm: {h: 5, minH: 3, minW: 3, w: 4, x: 0, y: 5}
      xl: {h: 6, minH: 3, minW: 3, w: 6, x: 8, y: 8}
      xxl: {h: 6, minH: 3, minW: 3, w: 6, x: 8, y: 8}
    quantity: results.properties.optoelectronic.solar_cell.absorber_fabrication
    scale: linear
    showinput: true
    type: terms
  - autorange: false
    layout:
      lg: {h: 4, minH: 3, minW: 8, w: 12, x: 12, y: 16}
      md: {h: 3, minH: 3, minW: 8, w: 8, x: 10, y: 14}
      sm: {h: 3, minH: 3, minW: 8, w: 8, x: 4, y: 10}
      xl: {h: 3, minH: 3, minW: 8, w: 8, x: 0, y: 8}
      xxl: {h: 3, minH: 3, minW: 8, w: 8, x: 0, y: 11}
    nbins: 30
    quantity: results.properties.electronic.band_structure_electronic.band_gap.value
    title: 'Band gap'
    scale: 1/4
    showinput: false
    type: histogram
  - layout:
      lg: {h: 6, minH: 3, minW: 3, w: 6, x: 18, y: 6}
      md: {h: 6, minH: 3, minW: 3, w: 5, x: 0, y: 14}
      sm: {h: 5, minH: 3, minW: 3, w: 4, x: 4, y: 5}
      xl: {h: 6, minH: 3, minW: 3, w: 5, x: 25, y: 8}
      xxl: {h: 6, minH: 3, minW: 3, w: 6, x: 20, y: 8}
    quantity: results.properties.optoelectronic.solar_cell.electron_transport_layer
    scale: linear
    showinput: true
    type: terms
  - layout:
      lg: {h: 6, minH: 3, minW: 3, w: 6, x: 12, y: 6}
      md: {h: 6, minH: 3, minW: 3, w: 5, x: 5, y: 14}
      sm: {h: 5, minH: 3, minW: 3, w: 4, x: 8, y: 5}
      xl: {h: 6, minH: 3, minW: 3, w: 5, x: 20, y: 8}
      xxl: {h: 6, minH: 3, minW: 3, w: 6, x: 26, y: 8}
    quantity: results.properties.optoelectronic.solar_cell.hole_transport_layer
    scale: linear
    showinput: true
    type: terms
"""
)
