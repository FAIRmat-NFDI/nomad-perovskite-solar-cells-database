# nomad-perovskite-solar-cells-database
A NOMAD plugin containing the schema for the Perovskite Solar Cell Database.

This plugin creates a NOMAD schema of the perovskite solar cell. You can find the paper of the original work of the perovskite database in this [link](https://www.nature.com/articles/s41560-021-00941-3).

## Run this plugin in NOMAD

To run this plugin in a NOMAD installation, you need to include in the `nomad.yaml`
file the following lines:

```yaml
plugins:
  include:
    - 'schemas/perovskite_solar_cell_database'
  options:
    schemas/perovskite_solar_cell_database:
      python_package: perovskite_solar_cell_database
```

See more documentation in NOMAD plugins in the [NOMAD documentation](https://nomad-lab.eu/prod/v1/staging/docs/index.html).
