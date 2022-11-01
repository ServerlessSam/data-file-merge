from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

from jsonpath_ng import parse

from src import ROOT_PATH
from src.file_location import FileLocation, Substitution
from src.file_types import JsonFileType
from src.json_merger import JsonMergerFactory
from src.reference_types import ReferenceTypeFactory
from src.regex import RegexExtractor


@dataclass
class SourceFile:
    """
    Synopsis:   A class for handling a source file definition for a build.
    Parameters:
        source_file_location = a FileLocation object that provides one or more file locations for the build.
        source_file_root = the jsonpath to the root node to copy from in each source file found.
        destination_file_content = the jsonpath to the root node to copy to in the destination file.
    """

    source_file_location: FileLocation
    source_file_root: str
    destination_file_content: str

    @cached_property
    def retrieved_src_content(self) -> list:
        """
        Synopsis:   Retrieves the content (from the specified node downwards)
                    for all files that are found at the specified file location.
        Returns:    A list of objects that will be merged within the destination file at the specified root node.
        """
        retrieved_src_content = []
        for src_file in self.source_file_location.resolved_paths:
            src_content = JsonFileType.load_from_file(src_file)
            jsonpath_expr = parse(self.source_file_root)
            retrieved_src_content.extend(
                [match.value for match in jsonpath_expr.find(src_content)]
            )
        return retrieved_src_content


@dataclass
class DestinationFile:
    """
    Synopsis:   A class for handling the destination file definition for a build.
    Parameters:
        destination_file_location = a FileLocation object that provides one single file location for the build.
    """

    destination_file_location: FileLocation

    def __post_init__(self):
        if len(self.destination_file_location.resolved_paths) > 1:
            raise Exception(
                "Attempting to use multiple destination files. We don't support this (yet)!"
            )

    @cached_property
    def file_content(self) -> dict | list:
        return (
            JsonFileType.load_from_file(
                Path(ROOT_PATH) / self.destination_file_location.substituted_path
            )
            if (
                Path(ROOT_PATH) / self.destination_file_location.substituted_path
            ).exists()
            else {}
        )


@dataclass
class BuildConfig:
    source_files: list[SourceFile]
    destination_file: DestinationFile

    def __eq__(self, other):

        src_files_match = True
        for src, other_src in zip(self.source_files, other.source_files):
            if src.source_file_root != other_src.source_file_root:
                src_files_match = False
                break
            if (
                src.source_file_location.substituted_path
                != other_src.source_file_location.substituted_path
            ):
                src_files_match = False
                break
            if src.destination_file_content != other_src.destination_file_content:
                src_files_match = False
                break

        return (
            self.destination_file.destination_file_location.substituted_path
            == other.destination_file.destination_file_location.substituted_path
            and self.destination_file.file_content
            == other.destination_file.file_content
            and src_files_match
        )

    def generate_new_dest_content(self) -> dict | list:
        """
        Synopsis:   Combines the current state of the desination file with desired source file content
        Parameters:
            src = A SourceFile object to be combined at the destination during a build.
        Returns: The new destination file content. Note the file has not been saved to disk yet.
        """
        dest_content = self.destination_file.file_content
        for src in self.source_files:
            jsonpath_expr = parse(src.destination_file_content)
            dest_content_matches = [
                match.value for match in jsonpath_expr.find(dest_content)
            ]
            if dest_content_matches == []:
                dest_content_matches = [None]
            for destination_match in dest_content_matches:
                for src_content in src.retrieved_src_content:
                    dest_json_merger = JsonMergerFactory(
                        destination_match
                    ).generate_json_merger()
                    dest_json_merger.merge_obj(src_content)
                    destination_match = dest_json_merger.json_obj
                    dest_content = jsonpath_expr.update_or_create(
                        dest_content, dest_json_merger.json_obj
                    )
        return dest_content

    def write_content(self, content: dict):
        # Only current use case is writing a destination file which at the moment uses the substituted path instead of a resolved path.
        # This is because the file to write to can be new so doesn't resolve (hence have empty list for resolved_paths)
        # JsonFileType.save_to_file(content, self.destination_file.destination_file_location.resolved_paths[0])
        JsonFileType.save_to_file(
            content,
            Path(ROOT_PATH)
            / self.destination_file.destination_file_location.substituted_path,
        )

    @staticmethod
    def load_config_from_file(
        file_path: Path,
        parameters=None,
    ):
        if parameters is None:
            parameters = {}
        config_dict = JsonFileType.load_from_file(file_path)
        source_files = []
        for src in config_dict["SourceFiles"]:
            subs = {}
            if "PathSubs" in src["SourceFileLocation"]:
                for sub_key, sub_dict in src["SourceFileLocation"]["PathSubs"].items():
                    reference_type = ReferenceTypeFactory(sub_dict["Type"]).generate()
                    regex = RegexExtractor.parse_from_sub_dict(sub_dict)
                    subs[sub_key] = Substitution(
                        reference_type(
                            parameters, None  # TODO support reading from content
                        ),
                        sub_dict["Value"],
                        regex,
                    )
            source_files.append(
                SourceFile(
                    FileLocation(src["SourceFileLocation"]["Path"], subs),
                    src["SourceFileRoot"],
                    src["DestinationFileContent"],
                )
            )
        dest_subs = {}
        if "PathSubs" in config_dict["DestinationFile"]["DestinationFileLocation"]:
            for sub_key, sub_dict in config_dict["DestinationFile"][
                "DestinationFileLocation"
            ]["PathSubs"].items():
                reference_type = ReferenceTypeFactory(sub_dict["Type"]).generate()
                regex = RegexExtractor.parse_from_sub_dict(sub_dict)
                dest_subs[sub_key] = Substitution(
                    reference_type(
                        parameters, None
                    ),  # TODO support reading from content
                    sub_dict["Value"],
                    regex,
                )
        dest_file = DestinationFile(
            FileLocation(
                config_dict["DestinationFile"]["DestinationFileLocation"]["Path"],
                dest_subs,
            )
        )
        return BuildConfig(source_files=source_files, destination_file=dest_file)

    def build(self):
        content = self.generate_new_dest_content()
        self.write_content(content)
