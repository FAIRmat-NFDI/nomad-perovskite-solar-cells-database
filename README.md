![](https://github.com/FAIRmat-NFDI/nomad-measurements/actions/workflows/publish.yml/badge.svg)
![](https://img.shields.io/pypi/pyversions/nomad-measurements)
![](https://img.shields.io/pypi/l/nomad-measurements)

# NOMAD Perovskite Solar Cells Database
  [<img src="docs/assets/nomad_plugin_logo.png" width="200">](https://nomad-lab.eu/prod/v1/staging/docs/plugins/plugins.html)

  [<img width="280" alt="image" src="docs/assets/perovskite_database_project.png">](https://www.perovskitedatabase.com/)



## Introduction
Welcome to the NOMAD plugin for the Perovskite Solar Cell Database. This project aims to provide an open-access interface for the perovskite solar cells database in NOMAD making the data accessible and interoperable with many other materials science datasets.
The data can be accessed via the NOMAD API and explored in the [NOMAD Solar Cell APP](https://nomad-lab.eu/prod/v1/staging/gui/search/solarcells).

  [<img src="docs/assets/screenshot_nomad_app.png">](https://nomad-lab.eu/prod/v1/staging/gui/search/solarcells)

Information about the original database is available at [perovskitedatabase.com](https://www.perovskitedatabase.com/).


## Key Features
- Detailed schema of perovskite solar cells.
- Integration with NOMAD for data exploration and access via the API.
- Augmented (meta)data including the elements of the perovskite absolbers and several staandarized chemical formulas, enabling and easy featurization of the composition for ML applications.

## Installation
To integrate this plugin with your NOMAD installation:
1. Add the following lines to your `nomad.yaml` file in your NOMAD installation:

    ```yaml
    plugins:
      include:
        - 'schemas/perovskite_solar_cell_database'
      options:
        schemas/perovskite_solar_cell_database:
          python_package: perovskite_solar_cell_database
    ```

2. For more detailed installation instructions, visit our [docs for NOMAD plugins](https://nomad-lab.eu/prod/v1/staging/docs/plugins/plugins.html).

### Acknowledgments
Special thanks to Jinzhao Li and all contributors who have made this project possible.

## Related Resources
- [Original Paper on Nature Energy](https://www.nature.com/articles/s41560-021-00941-3)  
- [NOMAD Documentation](https://nomad-lab.eu/prod/v1/staging/docs/)
