# data-file-merge

This python module allows you to merge multiple JSON files into a single destination JSON file using a set of rules defined in the [dfm config file](https://github.com/ServerlessSam/data-file-merge/wiki/Configuration)

Please refer to the [project wiki](https://github.com/ServerlessSam/data-file-merge/wiki) for complete documentation including how [usage](https://github.com/ServerlessSam/data-file-merge/wiki/Usage) and [configuration file syntax](https://github.com/ServerlessSam/data-file-merge/wiki/Configuration).

## Considerations

* Currently only JSON files are supported but YAML files could be supported with ease in future.
* Doing the reverse operation will soon be supported (splitting a single sourcefile into multiple destination files).
* You should be aware of:
  * [json-path's dollar-notation syntax](https://pypi.org/project/jsonpath-ng/)
  * [path-lib's path syntax](https://docs.python.org/3/library/pathlib.html)
  * [regex syntax](https://www.rexegg.com/regex-quickstart.html)

## Development

* install pre-commit hooks: ``poetry run pre-commit install``
* check and fix linting issues: ``make lint``
