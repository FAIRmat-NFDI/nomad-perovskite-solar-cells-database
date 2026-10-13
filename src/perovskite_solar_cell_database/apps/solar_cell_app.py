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
    - type: periodictable
      scale: linear
      search_quantity: results.material.elements
      title: null
      layout:
        xxl:
          minH: 8
          minW: 12
          h: 8
          w: 13
          y: 0
          x: 0
        xl:
          minH: 8
          minW: 12
          h: 8
          w: 12
          y: 0
          x: 0
        lg:
          minH: 8
          minW: 12
          h: 8
          w: 12
          y: 0
          x: 0
        md:
          minH: 8
          minW: 12
          h: 8
          w: 12
          y: 0
          x: 0
        sm:
          minH: 8
          minW: 12
          h: 8
          w: 12
          y: 48
          x: 0
    - type: scatterplot
      autorange: true
      size: 1000
      markers:
        color:
          scale: linear
          title: null
          unit: mA/cm^2
          search_quantity: results.properties.optoelectronic.solar_cell.short_circuit_current_density
      y:
        scale: linear
        title: Efficiency (%)
        unit: null
        search_quantity: results.properties.optoelectronic.solar_cell.efficiency
      x:
        scale: linear
        title: null
        unit: null
        search_quantity: results.properties.optoelectronic.solar_cell.open_circuit_voltage
      title: null
      layout:
        xxl:
          minH: 3
          minW: 3
          h: 8
          w: 12
          y: 0
          x: 24
        xl:
          minH: 3
          minW: 3
          h: 8
          w: 9
          y: 0
          x: 12
        lg:
          minH: 3
          minW: 3
          h: 6
          w: 12
          y: 8
          x: 0
        md:
          minH: 3
          minW: 3
          h: 6
          w: 9
          y: 8
          x: 0
        sm:
          minH: 3
          minW: 3
          h: 10
          w: 12
          y: 0
          x: 0
    - type: scatterplot
      autorange: true
      size: 1000
      markers:
        color:
          scale: linear
          title: null
          unit: null
          search_quantity: results.properties.optoelectronic.solar_cell.device_architecture
      y:
        scale: linear
        title: Efficiency (%)
        unit: null
        search_quantity: results.properties.optoelectronic.solar_cell.efficiency
      x:
        scale: linear
        title: null
        unit: null
        search_quantity: results.properties.optoelectronic.solar_cell.open_circuit_voltage
      title: null
      layout:
        xxl:
          minH: 3
          minW: 3
          h: 8
          w: 11
          y: 0
          x: 13
        xl:
          minH: 3
          minW: 3
          h: 8
          w: 9
          y: 0
          x: 21
        lg:
          minH: 3
          minW: 3
          h: 6
          w: 12
          y: 14
          x: 0
        md:
          minH: 3
          minW: 3
          h: 6
          w: 9
          y: 8
          x: 9
        sm:
          minH: 3
          minW: 3
          h: 11
          w: 12
          y: 10
          x: 0
    - type: terms
      query_mode: null
      show_input: true
      scale: linear
      search_quantity: results.properties.optoelectronic.solar_cell.device_stack
      title: null
      layout:
        xxl:
          minH: 3
          minW: 3
          h: 6
          w: 6
          y: 8
          x: 18
        xl:
          minH: 3
          minW: 3
          h: 6
          w: 6
          y: 8
          x: 14
        lg:
          minH: 3
          minW: 3
          h: 6
          w: 6
          y: 0
          x: 12
        md:
          minH: 3
          minW: 3
          h: 4
          w: 6
          y: 4
          x: 12
        sm:
          minH: 3
          minW: 3
          h: 6
          w: 6
          y: 42
          x: 6
    - type: histogram
      show_input: true
      autorange: true
      nbins: 30
      y:
        scale: 1/4
      x:
        scale: linear
        title: null
        unit: null
        search_quantity: results.properties.optoelectronic.solar_cell.illumination_intensity
      title: null
      layout:
        xxl:
          minH: 3
          minW: 3
          h: 3
          w: 12
          y: 8
          x: 0
        xl:
          minH: 3
          minW: 3
          h: 3
          w: 8
          y: 11
          x: 0
        lg:
          minH: 3
          minW: 3
          h: 4
          w: 12
          y: 12
          x: 12
        md:
          minH: 3
          minW: 3
          h: 3
          w: 8
          y: 17
          x: 10
        sm:
          minH: 3
          minW: 3
          h: 7
          w: 12
          y: 21
          x: 0
    - type: terms
      query_mode: null
      show_input: true
      scale: linear
      search_quantity: results.properties.optoelectronic.solar_cell.absorber_fabrication
      title: null
      layout:
        xxl:
          minH: 3
          minW: 3
          h: 6
          w: 6
          y: 8
          x: 12
        xl:
          minH: 3
          minW: 3
          h: 6
          w: 6
          y: 8
          x: 8
        lg:
          minH: 3
          minW: 3
          h: 6
          w: 6
          y: 0
          x: 18
        md:
          minH: 3
          minW: 3
          h: 4
          w: 6
          y: 0
          x: 12
        sm:
          minH: 3
          minW: 3
          h: 8
          w: 6
          y: 34
          x: 6
    - type: histogram
      show_input: false
      autorange: false
      nbins: 30
      y:
        scale: 1/4
      x:
        scale: linear
        title: null
        unit: null
        search_quantity: results.properties.electronic.band_structure_electronic.band_gap.value
      title: Band gap
      layout:
        xxl:
          minH: 3
          minW: 8
          h: 3
          w: 12
          y: 11
          x: 0
        xl:
          minH: 3
          minW: 8
          h: 3
          w: 8
          y: 8
          x: 0
        lg:
          minH: 3
          minW: 8
          h: 4
          w: 12
          y: 16
          x: 12
        md:
          minH: 3
          minW: 8
          h: 3
          w: 8
          y: 14
          x: 10
        sm:
          minH: 3
          minW: 8
          h: 6
          w: 12
          y: 28
          x: 0
    - type: terms
      query_mode: null
      show_input: true
      scale: linear
      search_quantity: results.properties.optoelectronic.solar_cell.electron_transport_layer
      title: null
      layout:
        xxl:
          minH: 3
          minW: 3
          h: 6
          w: 6
          y: 8
          x: 24
        xl:
          minH: 3
          minW: 3
          h: 6
          w: 5
          y: 8
          x: 25
        lg:
          minH: 3
          minW: 3
          h: 6
          w: 6
          y: 6
          x: 18
        md:
          minH: 3
          minW: 3
          h: 6
          w: 5
          y: 14
          x: 0
        sm:
          minH: 3
          minW: 3
          h: 8
          w: 6
          y: 34
          x: 0
    - type: terms
      query_mode: null
      show_input: true
      scale: linear
      search_quantity: results.properties.optoelectronic.solar_cell.hole_transport_layer
      title: null
      layout:
        xxl:
          minH: 3
          minW: 3
          h: 6
          w: 6
          y: 8
          x: 30
        xl:
          minH: 3
          minW: 3
          h: 6
          w: 5
          y: 8
          x: 20
        lg:
          minH: 3
          minW: 3
          h: 6
          w: 6
          y: 6
          x: 12
        md:
          minH: 3
          minW: 3
          h: 6
          w: 5
          y: 14
          x: 5
        sm:
          minH: 3
          minW: 3
          h: 6
          w: 6
          y: 42
          x: 0
"""
)
