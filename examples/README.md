# Data-file-merge Working Examples
This directory contains a set of working examples for merging JSON files via dfm.

## Usage
For each example, there is a dfm config file with the name `drm-config-example-*.json`. The complete local path to this file should be used for `file_path` in Python or the command argument if using the CLI. The complete local path to the indivual example's directory should be used as `root_path` in Python or the `--root-path` argument if using the CLI.

Remember to delete the generated file after each merge!

### CLI
See [dfm install instructions](https://github.com/ServerlessSam/data-file-merge/wiki/Installation) for getting the CLI installed.

The CLI can be called using `dfm merge <path to config file> --root-path <path to example's directory>`. Note for some examples you may need to pass parameters using `-p key1=value1,key2=value2...`.

### Python
You can checkout the Python project [from GitHub](https://github.com/ServerlessSam/data-file-merge).

In a python shell (project supports Poetry) with the projects root directory in `PYTHONPATH` run the following:
```
from dfm.config import BuildConfig
from pathlib import Path
cfg = BuildConfig.load_config_from_file(file_path=Path("<path to config file>"), root_path=Path("<path to example's directory"))
cfg.build()
```
Note for some examples you may need to pass parameter by adding a second argument to `load_config_from_file` of the form `{"ParameterKey1":"Value1", "ParamterKey2":"Value2"...}`.
