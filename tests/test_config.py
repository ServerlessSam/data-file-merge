from pathlib import Path

from dfm.config import BuildConfig, DestinationFile, SourceFile
from dfm.file_location import FileLocation, Substitution
from dfm.file_types import JsonFileType
from dfm.reference_types import (
    ContentReferenceType,
    KeyReferenceType,
    LiteralReferenceType,
    ParameterReferenceType,
)


class TestSubstitutions:
    def test_substitutions(self):
        for reference_type, value, expected_resolution in zip(
            [
                LiteralReferenceType(),
                KeyReferenceType(
                    None, {"key1": {"NestedKey1": "NestedValue1"}, "key2": "value2"}
                ),
                ContentReferenceType(
                    None, {"key1": {"NestedKey1": "NestedValue1"}, "key2": "value2"}
                ),
                ParameterReferenceType({"key1": "value1", "key2": "value2"}),
            ],
            ["ThisShouldLitterallyJustBeCopied", "$.key1", "$.key1.NestedKey1", "key2"],
            [
                "ThisShouldLitterallyJustBeCopied",
                "NestedKey1",
                "NestedValue1",
                "value2",
            ],
        ):
            assert Substitution(reference_type, value).evaluate() == expected_resolution


class TestFileLocations:
    def test_file_locations(self):
        file_location = FileLocation(
            path="test_files_directory/${Sub1}/nested_test_file_*.json",
            root_path=Path(__file__).parent.resolve(),
            subs={"Sub1": Substitution(LiteralReferenceType(), "nested_directory")},
        )
        assert file_location.resolved_paths == [
            Path().absolute()
            / Path(
                "tests/test_files_directory/nested_directory/nested_test_file_1.json"
            ),
            Path().absolute()
            / Path(
                "tests/test_files_directory/nested_directory/nested_test_file_2.json"
            ),
        ]


class TestDestinationFiles:
    def test_destination_files(self):
        dest_file_location = FileLocation(
            path="test_files_directory/${Sub1}/nested_test_file_1.json",
            subs={"Sub1": Substitution(LiteralReferenceType(), "nested_directory")},
            root_path=Path(__file__).parent.resolve(),
        )

        dest = DestinationFile(dest_file_location)
        assert dest.content == {
            "AKeyInTheFile": "A value in the file",
            "AnotherKeyInTheFile": {"UhOh": "This", "OneIs": "Nested"},
        }

    def test_destination_file_doesnt_exist(self):
        dest_file_location = FileLocation(
            path="./tests/test_files_directory/${Sub1}/nested_test_file_DOESNT_EXIST.json",
            subs={"Sub1": Substitution(LiteralReferenceType(), "nested_directory")},
            root_path=Path(__file__).parent.resolve(),
        )
        dest = DestinationFile(dest_file_location)
        assert dest.content == {}


class TestSourceFiles:
    def test_source_files(self):
        file_location = FileLocation(
            path="test_files_directory/${Sub1}/nested_test_file_*.json",
            subs={"Sub1": Substitution(LiteralReferenceType(), "nested_directory")},
            root_path=Path(__file__).parent.resolve(),
        )
        src = SourceFile(file_location, "$.AnotherKeyInTheFile", "$")
        assert src.retrieved_src_content == [
            {"UhOh": "This", "OneIs": "Nested"},
            {"UhOh2": "This", "OneIs2": "NestedAlso"},
        ]


class TestConfigs:
    def test_configs(self):
        src_file_location = FileLocation(
            path="test_files_directory/${Sub1}/nested_test_file_*.json",
            subs={"Sub1": Substitution(LiteralReferenceType(), "nested_directory")},
            root_path=Path(__file__).parent.resolve(),
        )

        # TODO: this leave changes in build_test_merged_file after test suite runs. Should be doing this in memory
        dest_file_location = FileLocation(
            path="test_files_directory/${Sub1}/build_test_merged_file.json",
            subs={"Sub1": Substitution(LiteralReferenceType(), "nested_directory")},
            root_path=Path(__file__).parent.resolve(),
        )
        src = SourceFile(src_file_location, "$.AnotherKeyInTheFile", "$")
        dest = DestinationFile(dest_file_location)
        config = BuildConfig([src], dest, Path(__file__).parent.resolve())
        assert config.build(save_to_local_file=False) == {
            "Hello": "There",
            "UhOh": "This",
            "OneIs": "Nested",
            "UhOh2": "This",
            "OneIs2": "NestedAlso",
        }

    def test_config_build(self):
        src_file_location = FileLocation(
            path="test_files_directory/${Sub1}/nested_test_file_*.json",
            subs={"Sub1": Substitution(LiteralReferenceType(), "nested_directory")},
            root_path=Path(__file__).parent.resolve(),
        )
        src = SourceFile(src_file_location, "$.AnotherKeyInTheFile", "$")

        dest_file_location = FileLocation(
            path="test_files_directory/${Sub1}/build_test_merged_file.json",
            subs={"Sub1": Substitution(LiteralReferenceType(), "nested_directory")},
            root_path=Path(__file__).parent.resolve(),
        )
        src = SourceFile(src_file_location, "$.AnotherKeyInTheFile", "$")
        dest = DestinationFile(dest_file_location)
        config = BuildConfig([src], dest, Path(__file__).parent.resolve())
        config.build()

        assert JsonFileType.load_from_file(
            str(
                Path(__file__).parent.resolve()
                / "test_files_directory/nested_directory/build_test_merged_file.json"
            )
        ) == {
            "Hello": "There",
            "UhOh": "This",
            "OneIs": "Nested",
            "UhOh2": "This",
            "OneIs2": "NestedAlso",
        }

    """
    Commenting out the following test because we still need to include full paths in FileLocation in config files (minus the prefix '/').
    This causes a problem because running unit tests locally vs running them in CI/CD will need the paths to be entirely different.
    TODO Re-add this test once we complete https://github.com/ServerlessSam/data-file-merge/issues/10
    """

    def test_config_load(self):
        parameters = {"TheWordTest": "test"}
        expected_config = BuildConfig(
            source_files=[
                SourceFile(
                    location=FileLocation(
                        path="test_files_directory/nested_directory/nested_${Sub1}_file_1.json",
                        subs={
                            "Sub1": Substitution(
                                ParameterReferenceType(parameters), "TheWordTest"
                            )
                        },
                        root_path=Path(__file__).parent.resolve(),
                    ),
                    node="$.AnotherKeyInTheFile",
                    destination_node="$",
                ),
                SourceFile(
                    location=FileLocation(
                        path="test_files_directory/nested_directory/nested_${Sub1}_file_2.json",
                        subs={"Sub1": Substitution(LiteralReferenceType(), "test")},
                        root_path=Path(__file__).parent.resolve(),
                    ),
                    node="$.AnotherKeyInTheFile",
                    destination_node="$",
                ),
            ],
            destination_file=DestinationFile(
                FileLocation(
                    path="test_files_directory/nested_directory/build_test_merged_file.json",
                    root_path=Path(__file__).parent.resolve(),
                )
            ),
            root_path=Path(__file__).parent.resolve(),
        )
        generated_config = BuildConfig.load_config_from_file(
            file_path=str(
                Path(__file__).parent.resolve()
                / "test_files_directory/nested_directory/build_test_config.json"
            ),
            parameters=parameters,
            root_path=Path(__file__).parent.resolve(),
        )
        assert expected_config == generated_config
