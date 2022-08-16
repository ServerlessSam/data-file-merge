from pathlib import Path
import json

class BaseFileType():
    def __init__(self):
        pass

    def load_from_file(self, file_path:Path):
        raise NotImplementedError

    def save_to_file(self, object:dict | list, file_path:Path):
        raise NotImplementedError
    

class JsonFileType(BaseFileType):

    @classmethod
    def load_from_file(self, file_path:Path):
        with open(file_path, "r") as loadedFile:
            dictionary = json.load(loadedFile)
        return dictionary

    @classmethod
    def save_to_file(self, object:dict | list, file_path:Path):
        with open(file_path, 'w+') as output:
            json.dump(object, output, indent=4)