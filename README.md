# data-file-merge

Project Synopsis:
    This python module will merge multiple source files into one destination file.

Considerations:
- Currently only JSON files are supported but YAML files could be supported with ease in future.
- Doing the reverse operation will soon be supported (splitting a single sourcefile into multiple destination files).
- You should be aware of:
    - json-lib's dollar-notation syntax
    - path-lib's path syntax

Build Config Syntax:
    Type:
        Dict
    Synopsis:
        The contents of a "build config" file that can be parsed in order to run a "build" operation and merge multiple source files into one destination file. This can be done by running 'pantry.config.load_config_from_file()' in a python shell.
    Details:
        {
            "SourceFiles" : [
                <<SourceFile>> (see below),
                <<SourceFile>>,
                ...
            ],
            "DestinationFile" : <<DestinationFile>> (see below)
        }

Source File:
    Type:
        Dict
    Synopsis:
        The data required to collect data from a set of files when preparing to build a new file.
    Details:
        {
            "SourceFileLocation" : <<FileLocation>> (see below),
            "SourceFileRoot" : <<FileRoot> (see below),
            "DestinationFileContent" : <<DestinationFileContent>> (see below)
        }

Destination File:
    Type:
        Dict
    Synopsis:
        The data required to define a file that will be the destination of a new built file. The file can already exist and all existing data will be preserved. No data can be overwritten as part of a merge however.
    Details:
        {
        "DestinationFileLocation" : <<FileLocation>> (see below)
        }

File Location:
    Type:
        Dict
    Synopsis:
        The data required top point to one or more files on a local file system
    Details:
        {
            "Path" : <<RelativePath> (see below),
            "PathSubs" : {
                "<<SubKey (see RelativePath above for how to sub)>>" : <<Substitution>> (See below),
                ...
        }

Relative Path:
    Type:
        Str
    Synopsis:
        A pointer to one or more local files.
    Details:
        A path relative from "/" on the local file system. (The "/" is currently hardcoded but will be a configurable env var in future). It adheres to path-lib path syntax. The path can either be to a single file or multiple files. Substitution placeholders can be added using the "${SubKey}" syntax. These will be substiutited for corresponding values from the PathSubs keys (see above) of the same name.

Substitution:
    Type:
        Dict
    Synopsis:
        The data required to perform a substitution on a path.
    Details:
        {
            "Type" : <<SubstitutionType>> (See below),
            "Value" : <<SubstitutionValue>> (See below),
            "Regex" : <<SubstitutionRegex>> (See below)
        }

Substitution Type:
    Type:
        Str
    Synopsis:
        Defines the type of substitution to perform.
    Details:
        Can be one of the following:
            - "Literal":
                Will be substituting for the literal value given as <<SubstitutionValue>>.
            - "Parameter":
                Will be substituting for the value of a parameter with the same namesake as the <<SubstitutionValue>>
            - "Content":
                Will be substituting for the value at a particular key within the file. The particular key is determined using <<SubstitutionValue>> assuming it adheres to json-path dollar notation syntax. The value at this particular node must be a string or int. This is only accessable in substitutions for a destination file path (during a build).
            - "Key":
                Will be substituting for a key's name within the file. The particular key is determined using <<SubstitutionValue>> and it adheres to json-path dollar notiation syntax. The specified node must be a single key. This is only accessable in substitutions for a destination file path (during a build).

Substitution Value:
    Type:
        Str
    Synopsis:
        Value to pass into the substitution logic for a given substitution type.
    Details:
        See <<SubstitutionTypes>> for a full explanation as to how the <<SubstitutionValue>> is used.

Regex (Optional):
    Type:
        Dict
    Synopsis:
        A regex operation to perform after the substitution candidate is determined by the corresponding <<SubstitutionType>>. The result of this will be used as the substitution.
    Details:
        {
            "Expression" : <<RegexExpression>>",
            "CaptureGroup" : <<RegexCaptureGroup>>
        }

Regex Expression:
    Type:
        Str
    Synopsis:
        A regex string that will produce a set of named or unnamed capture groups. This uses Python regex syntax.
    Details:
        E.g "(?P<provider>.+)::(?P<service>.+)::(?P<datatype>.+)" will extract the three sections of an AWS cloudformation resource type.

Regex Capture Group:
    Type:
        Str or Int
    Synopsis:
        The identifier for a particular regex capture group. The value of which is used in the substitution.
    Details:
        String names are used for named capture groups and integers are used for zero-indexed unnamed capture groups in an ordered list.

File Root Syntax:
    Type:
        Str
    Synopsis:
        The node in each source file to use as the root node for merging from.
    Details:
        Everything below this node will be copied. It adheres to json-path dollar-notation syntax. It must point to a single key; or "$" which will be the root of the file itself.

Destination File Content:
    Type:
        Str
    Synopsis:
        The node in the destination file to use as the root node for merging to.
    Details:
        It adheres to json-path dollar-notation syntax. It must point to a single key; or "$" which will be the root of the file itself. The key doesn't need to neccessarily exist beforehand. But if it does exist, it's value must be an empty list/dict or null. It will not overwrite existing values.

# Development

- install pre-commit hooks: ``poetry run pre-commit install``
- check and fix linting issues: ``make lint``
