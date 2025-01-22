# Install This Plugin

If you want to run this plugin locally on your Oasis to use the defined schemas, you 
need to add the plugin to your Oasis image.
The recommended way of doing this is to add it to the plugins table in the 
[`pyproject.toml`](pyproject.toml) file of your
 [NOMAD distribution repository](https://github.com/FAIRmat-NFDI/nomad-distro-template?tab=readme-ov-file).

 Currently the plugin is not published to PyPI and you will need to specify a git 
 source. For this you also need to specify a version tag, branch, or commit. 
 For example, to use the v0.1.1 release you should add the following the to the 
 `pyproject.toml`:

```toml
[project.optional-dependencies]
plugins = [
  "perovskite-solar-cell-database @ git+https://github.com/FAIRmat-NFDI/nomad-perovskite-solar-cells-database.git@v0.1.1"
]
```

For more detailed installation instructions, visit our [docs for NOMAD plugins](https://nomad-lab.eu/prod/v1/develop/docs/howto/oasis/plugins_install.html).
