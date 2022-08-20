import json
from pathlib import Path


class BaseFileType:
    def __init__(self):
        pass

    def load_from_file(self, file_path: Path):
        raise NotImplementedError

    def save_to_file(self, object: dict | list, file_path: Path):
        raise NotImplementedError


class JsonFileType(BaseFileType):
    @classmethod
    def load_from_file(self, file_path: Path):
        with open(file_path) as loadedFile:
            obj = json.load(loadedFile)
        return obj

    @classmethod
    def save_to_file(self, object: dict | list, file_path: Path):
        with open(file_path, "w+") as output:
            json.dump(object, output, indent=4)
