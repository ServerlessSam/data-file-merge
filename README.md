# data-file-merge

This python module will merge multiple source files into one destination file.

* [Considerations](#considerations)
* [Syntaxes](#syntaxes)
  * [Build Config](#build-config)
  * [Source File](#source-file)
  * [Destination File](#destination-file)
  * [File Location](#file-location)
  * [Relative Path](#relative-path)
  * [Substitution](#substitution)
  * [Substitution Type](#substitution-type)
  * [Substitution Value](#substitution-value)
  * [Regex (Optional)](#regex-optional)
  * [Regex Expression](#regex-expression)
  * [Regex Capture Group](#regex-capture-group)
  * [File Root Syntax](#file-root-syntax)
  * [Destination File Context](#destination-file-content)
* [Development](#development)

## Considerations

* Currently only JSON files are supported but YAML files could be supported with ease in future.
* Doing the reverse operation will soon be supported (splitting a single sourcefile into multiple destination files).
* You should be aware of:
  * json-lib's dollar-notation syntax
  * path-lib's path syntax

## Syntaxes

The following describes various syntaxes in use by **data-file-merge**.

### Build Config

**Type:** Dict \
**Synopsis:** The contents of a "build config" file that can be parsed in order to run a "build" operation and merge multiple source files into one destination file. This can be done by running `pantry.config.load_config_from_file()` in a python shell.

```json5
{
  "SourceFiles" : [
    <<SourceFile>>, // (see below)
    <<SourceFile>>,
    <<SourceFile>>...
  ],
  "DestinationFile" : <<DestinationFile>> // (see below)
}
```

### Source File

**Type:** Dict \
**Synopsis:** The data required to collect data from a set of files when preparing to build a new file.

```json5
{
  "SourceFileLocation": <<FileLocation>>, // (see below)
  "SourceFileRoot": <<FileRoot>>, // (see below)
  "DestinationFileContent": <<DestinationFileContent>> // (see below)
}
```

### Destination File

**Type:** Dict \
**Synopsis:** The data required to define a file that will be the destination of a new built file. The file can already exist and all existing data will be preserved. No data can be overwritten as part of a merge however.

```json5
{
  "DestinationFileLocation" : <<FileLocation>> // (see below)
}
```

### File Location

**Type:** Dict \
**Synopsis:** The data required top point to one or more files on a local file system.

```json5
{
  "Path" : <<RelativePath>>, // (see below)
  "PathSubs" : {
    <<SubKey>>: <<Substitution>>, // SubKey: see Relative Path, Substitution: (see below)
    <<SubKey>>...: <<Substitution>>...
  }
}
```

### Relative Path

**Type:** Str \
**Synopsis:** A pointer to one or more local files.

A path relative from `/` on the local file system. (The `/` is currently hardcoded but will be a configurable env var in future). It adheres to path-lib path syntax. The path can either be to a single file or multiple files. Substitution placeholders can be added using the `${SubKey}` syntax. These will be substiutited for corresponding values from the PathSubs keys (see above) of the same name.

### Substitution

**Type:** Dict \
**Synopsis:** The data required to perform a substitution on a path.

```json5
{
  "Type": <<SubstitutionType>>, // (see below)
  "Value": <<SubstitutionValue>>, // (see below)
  "Regex": <<SubstitutionRegex>> // (see below)
}
```

### Substitution Type

**Type:** Str \
**Synopsis:** Defines the type of substitution to perform.

Can be one of the following:

* `Literal`: \
  Will be substituting for the literal value given as `<<SubstitutionValue>>`.
* `Parameter`: \
  Will be substituting for the value of a parameter with the same namesake as the `<<SubstitutionValue>>`.
* `Content`: \
  Will be substituting for the value at a particular key within the file. The particular key is determined using `<<SubstitutionValue>>` assuming it adheres to json-path dollar notation syntax. The value at this particular node must be a string or int. This is only accessable in substitutions for a destination file path (during a build).
* `Key`: \
  Will be substituting for a key's name within the file. The particular key is determined using `<<SubstitutionValue>>` and it adheres to json-path dollar notiation syntax. The specified node must be a single key. This is only accessable in substitutions for a destination file path (during a build).

### Substitution Value

**Type:** Str \
**Synopsis:** Value to pass into the substitution logic for a given substitution type.

See `<<SubstitutionTypes>>` for a full explanation as to how the `<<SubstitutionValue>>` is used.

### Regex (Optional)

**Type:** Dict \
**Synopsis:** A regex operation to perform after the substitution candidate is determined by the corresponding `<<SubstitutionType>>`. The result of this will be used as the substitution.

```json5
{
  "Expression" : <<RegexExpression>>, // (see below)
  "CaptureGroup" : <<RegexCaptureGroup>> // (see below)
}
```

### Regex Expression

**Type:** Str \
**Synopsis:** A regex string that will produce a set of named or unnamed capture groups. This uses Python regex syntax.

E.g `(?P<provider>.+)::(?P<service>.+)::(?P<datatype>.+)` will extract the three sections of an AWS cloudformation resource type.

### Regex Capture Group

**Type:** Str or Int \
**Synopsis:** The identifier for a particular regex capture group. The value of which is used in the substitution.

String names are used for named capture groups and integers are used for zero-indexed unnamed capture groups in an ordered list.

### File Root Syntax

**Type:** Str \
**Synopsis:** The node in each source file to use as the root node for merging from.

Everything below this node will be copied. It adheres to json-path dollar-notation syntax. It must point to a single key; or `$` which will be the root of the file itself.

### Destination File Content

**Type:** Str \
**Synopsis:** The node in the destination file to use as the root node for merging to.

It adheres to json-path dollar-notation syntax. It must point to a single key; or `$` which will be the root of the file itself. The key doesn't need to neccessarily exist beforehand. But if it does exist, it's value must be an empty list/dict or null. It will not overwrite existing values.

## Development

* install pre-commit hooks: ``poetry run pre-commit install``
* check and fix linting issues: ``make lint``
