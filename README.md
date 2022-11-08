# data-file-merge

This python module/CLI allows you to merge multiple JSON files into a single destination JSON file using a set of rules defined in the [dfm config file](https://github.com/ServerlessSam/data-file-merge/wiki/Configuration)

Please refer to the [project wiki](https://github.com/ServerlessSam/data-file-merge/wiki) for complete documentation including [usage](https://github.com/ServerlessSam/data-file-merge/wiki/Usage) and [configuration file syntax](https://github.com/ServerlessSam/data-file-merge/wiki/Configuration).

# Hello World Example

You can install the CLI for your operating system from [GitHub here](https://github.com/ServerlessSam/data-file-merge/releases).

Using the following config file:
```json
{
    "SourceFiles" : [
        {
            "SourceFileLocation" : {
                "Path" : "foo/bar.json"
            },
            "SourceFileNode" : "$",
            "DestinationFileNode" : "$"
        },
        {
            "SourceFileLocation" : {
                "Path" : "foo/baz.json"
            },
            "SourceFileNode" : "$",
            "DestinationFileNode" : "$"
        },
    ],
    "DestinationFile" : {
        "DestinationFileLocation" : {
            "Path" : "hello/world.json"
        }
    }
}
```
...you are able to merge the content of `foo/bar.json` and `foo/baz.json` into `hello/world.json` (this can either be an existing or new file). The `$`s indicate that we are merging from the root node of both `foo/*.json` files to the root of `hello/world.json`.
This merge can be achieved with the CLI command `dfm merge --root-path <path to 'foo' directory> <path to this config file>`.
The specific rules followed by the merging logic can be found in [the wiki](https://github.com/ServerlessSam/data-file-merge/wiki/Merging-Logic).

More examples can be found in the [dfm example repo](https://github.com/ServerlessSam/dfm-examples).

## Considerations

* Currently only JSON files are supported but YAML files could be supported with ease in future.
* Doing the reverse operation will soon be supported (splitting a single sourcefile into multiple destination files).
* You should be aware of:
  * [json-path's dollar-notation syntax](https://pypi.org/project/jsonpath-ng/)
  * [path-lib's path syntax](https://docs.python.org/3/library/pathlib.html)
  * [regex syntax](https://www.rexegg.com/regex-quickstart.html)

## Development

* install pre-commit hooks: ``poetry run pre-commit install``
* check and fix linting issues: ``make format``

## Contributing to the project

You are welcome to help us rid the world of monolithic data files! Reach out to [ServerlessSam](https://github.com/ServerlessSam) to either find some tickets to complete or bring up any ideas you have.
