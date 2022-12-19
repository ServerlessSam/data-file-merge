import json
from abc import ABC, abstractmethod
from pathlib import Path


class BaseFileType(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def load_from_file(self, file_path: Path):
        raise NotImplementedError("load_from_file has not been implemented yet")

    @abstractmethod
    def save_to_file(self, json_object: dict | list, file_path: Path):
        raise NotImplementedError("save_to_file has not been implemented yet")


class JsonFileType(BaseFileType):
    @classmethod
    def load_from_file(cls, file_path: Path):
        with open(file_path) as loadedFile:
            obj = json.load(loadedFile)
        return obj

    @classmethod
    def save_to_file(cls, json_object: dict | list, file_path: Path):
        with open(file_path, "w+") as output:
            json.dump(json_object, output, indent=4)
