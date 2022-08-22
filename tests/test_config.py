from pathlib import Path

from pantry.config import BuildConfig, DestinationFile, SourceFile
from pantry.file_location import FileLocation, Substitution
from pantry.file_types import JsonFileType
from pantry.reference_types import (
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
            path="Users/samuellock/Documents/GitHub/config-seperation/tests/test_files_directory/${Sub1}/nested_test_file_*.json",
            subs={"Sub1": Substitution(LiteralReferenceType(), "nested_directory")},
        )
        assert file_location.resolved_paths == [
            Path(
                "/Users/samuellock/Documents/GitHub/config-seperation/tests/test_files_directory/nested_directory/nested_test_file_1.json"
            ),
            Path(
                "/Users/samuellock/Documents/GitHub/config-seperation/tests/test_files_directory/nested_directory/nested_test_file_2.json"
            ),
        ]


class TestDestinationFiles:
    def test_destination_files(self):
        dest_file_location = FileLocation(
            path="Users/samuellock/Documents/GitHub/config-seperation/tests/test_files_directory/${Sub1}/nested_test_file_1.json",
            subs={"Sub1": Substitution(LiteralReferenceType(), "nested_directory")},
        )

        dest = DestinationFile(dest_file_location)
        assert dest.file_content == {
            "AKeyInTheFile": "A value in the file",
            "AnotherKeyInTheFile": {"UhOh": "This", "OneIs": "Nested"},
        }

    def test_destination_file_doesnt_exist(self):
        dest_file_location = FileLocation(
            path="Users/samuellock/Documents/GitHub/config-seperation/tests/test_files_directory/${Sub1}/nested_test_file_DOESNT_EXIST.json",
            subs={"Sub1": Substitution(LiteralReferenceType(), "nested_directory")},
        )
        dest = DestinationFile(dest_file_location)
        assert dest.file_content == {}


class TestSourceFiles:
    def test_source_files(self):
        file_location = FileLocation(
            path="Users/samuellock/Documents/GitHub/config-seperation/tests/test_files_directory/${Sub1}/nested_test_file_*.json",
            subs={"Sub1": Substitution(LiteralReferenceType(), "nested_directory")},
        )
        src = SourceFile(file_location, "$.AnotherKeyInTheFile", "$")
        assert src.retreived_src_content == [
            {"UhOh": "This", "OneIs": "Nested"},
            {"UhOh2": "This", "OneIs2": "NestedAlso"},
        ]


class TestConfigs:
    def test_configs(self):
        src_file_location = FileLocation(
            path="Users/samuellock/Documents/GitHub/config-seperation/tests/test_files_directory/${Sub1}/nested_test_file_*.json",
            subs={"Sub1": Substitution(LiteralReferenceType(), "nested_directory")},
        )
        src = SourceFile(src_file_location, "$.AnotherKeyInTheFile", "$")

        dest_file_location = FileLocation(
            path="Users/samuellock/Documents/GitHub/config-seperation/tests/test_files_directory/${Sub1}/build_test_merged_file.json",
            subs={"Sub1": Substitution(LiteralReferenceType(), "nested_directory")},
        )
        src = SourceFile(src_file_location, "$.AnotherKeyInTheFile", "$")
        dest = DestinationFile(dest_file_location)
        config = BuildConfig([src], dest)
        assert config.generate_new_dest_content() == {
            "Hello": "There",
            "UhOh": "This",
            "OneIs": "Nested",
            "UhOh2": "This",
            "OneIs2": "NestedAlso",
        }

    def test_config_build(self):
        src_file_location = FileLocation(
            path="Users/samuellock/Documents/GitHub/config-seperation/tests/test_files_directory/${Sub1}/nested_test_file_*.json",
            subs={"Sub1": Substitution(LiteralReferenceType(), "nested_directory")},
        )
        src = SourceFile(src_file_location, "$.AnotherKeyInTheFile", "$")

        dest_file_location = FileLocation(
            path="Users/samuellock/Documents/GitHub/config-seperation/tests/test_files_directory/${Sub1}/build_test_merged_file.json",
            subs={"Sub1": Substitution(LiteralReferenceType(), "nested_directory")},
        )
        src = SourceFile(src_file_location, "$.AnotherKeyInTheFile", "$")
        dest = DestinationFile(dest_file_location)
        config = BuildConfig([src], dest)
        config.build()

        assert JsonFileType.load_from_file(
            "/Users/samuellock/Documents/GitHub/config-seperation/tests/test_files_directory/nested_directory/build_test_merged_file.json"
        ) == {
            "Hello": "There",
            "UhOh": "This",
            "OneIs": "Nested",
            "UhOh2": "This",
            "OneIs2": "NestedAlso",
        }

    def test_config_load(self):
        parameters = {"TheWordTest": "test"}
        expected_config = BuildConfig(
            source_files=[
                SourceFile(
                    source_file_location=FileLocation(
                        path="../config-seperation/tests/test_files_directory/nested_directory/nested_${Sub1}_file_1.json",
                        subs={
                            "Sub1": Substitution(
                                ParameterReferenceType(parameters), "TheWordTest"
                            )
                        },
                    ),
                    source_file_root="$.AnotherKeyInTheFile",
                    destination_file_content="$",
                ),
                SourceFile(
                    source_file_location=FileLocation(
                        path="../config-seperation/tests/test_files_directory/nested_directory/nested_${Sub1}_file_2.json",
                        subs={"Sub1": Substitution(LiteralReferenceType(), "test")},
                    ),
                    source_file_root="$.AnotherKeyInTheFile",
                    destination_file_content="$",
                ),
            ],
            destination_file=DestinationFile(
                FileLocation(
                    path="Users/samuellock/Documents/GitHub/../config-seperation/tests/test_files_directory/nested_directory/build_test_merged_file.json"
                )
            ),
        )
        generated_config = BuildConfig.load_config_from_file(
            file_path="/Users/samuellock/Documents/GitHub/config-seperation/tests/test_files_directory/nested_directory/build_test_config.json",
            parameters=parameters,
        )
        assert expected_config == generated_config
