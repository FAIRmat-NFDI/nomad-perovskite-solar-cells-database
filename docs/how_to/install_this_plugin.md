# Install This Plugin

To add a new plugin to the docker image you should add it to the plugins table in the [`pyproject.toml`](pyproject.toml) file of a [NOMAD distribution repository](https://github.com/FAIRmat-NFDI/nomad-distro-template?tab=readme-ov-file).

Here you can put either plugins distributed to PyPI, e.g.

```toml
[project.optional-dependencies]
plugins = [
  "perovskite-solar-cell-database>=1.0.0",
]
```

or plugins in a git repository with either the commit hash

```toml
[project.optional-dependencies]
plugins = [
  "perovskite-solar-cell-database @ git+https://github.com/FAIRmat-NFDI/nomad-perovskite-solar-cells-database.git@4b10f9927fb51d5779a386727867c7542c54f3f7"]
```

or with a tag

```toml
[project.optional-dependencies]
plugins = [
  "perovskite-solar-cell-database @ git+https://github.com/FAIRmat-NFDI/nomad-perovskite-solar-cells-database.git@v1.0.0"
]
```

For more detailed installation instructions, visit our [docs for NOMAD plugins](https://nomad-lab.eu/prod/v1/develop/docs/howto/oasis/plugins_install.html).
