from copy import deepcopy
from dataclasses import dataclass
from typing import Dict


@dataclass
class BaseJsonMerger:
    

    def __post_init__(self):
        self.TYPE_TO_MERGER_MAPPING = (
            (list, self.merge_a_list),
            (int, self.merge_an_int),
            (dict, self.merge_a_dict),
            (str, self.merge_a_str)
        )

    def merge_a_list(self, the_list:list):
        raise NotImplementedError
    
    def merge_an_int(self, the_int:int):
        raise NotImplementedError
    
    def merge_a_dict(self, the_dict:dict):
        raise NotImplementedError

    def merge_a_str(self, the_str:str):
        raise NotImplementedError

    def merge_obj(self, the_obj:list | int | dict | str):
        for mapping in self.TYPE_TO_MERGER_MAPPING:
            if type(the_obj) == mapping[0]:
                return mapping[1](the_obj)
        raise Exception(f"Json object for merging was not one of the 4 expected types (list, int, dict, str). Instead it was {str(type(the_obj))}")

class ListJsonMerger(BaseJsonMerger):
    json_list:list

    def merge_a_list(self, the_list:list) -> list:
        self.json_list += the_list
    
    def merge_an_int(self, the_int:int) -> list:
        self.json_list.append(the_int)
    
    def merge_a_dict(self, the_dict:dict) -> list:
        self.json_list.append(the_dict)

    def merge_a_str(self, the_str:str) -> list:
        self.json_list.append(the_str)

@dataclass
class IntJsonMerger(BaseJsonMerger):
    json_int:int

    def merge_a_list(self, the_list:list):
        raise Exception("Cannot merge a list into an int.")
    
    def merge_an_int(self, the_int:int) -> int:
        self.json_int += the_int
    
    def merge_a_dict(self, the_dict:dict):
        raise Exception("Cannot merge a dict into an int.")

    def merge_a_str(self, the_str:str):
        raise Exception("Cannot merge a str into an int.")

@dataclass
class DictJsonMerger(BaseJsonMerger):
    json_dict:dict

    def merge_a_list(self, the_list:list):
        raise Exception("Cannot merge a list into a dict.")
    
    def merge_an_int(self, the_int:int):
        raise Exception("Cannot merge an int into a dict.")
    
    def merge_a_dict(self, the_dict:dict) -> dict:
        for key in the_dict:
            if key in self.json_dict:
                raise Exception("Attempting to override keys!")
        json_dict_copy = deepcopy(self.json_dict)
        self.json_dict = json_dict_copy | the_dict

    def merge_a_str(self, the_str:str):
        raise Exception("Cannot merge a str into a dict.")

@dataclass
class StrJsonMerger(BaseJsonMerger):
    json_str:str

    def merge_a_list(self, the_list:list):
        raise Exception("Cannot merge a list into a str.")
    
    def merge_an_int(self, the_int:int):
        raise Exception("Cannot merge an int into a str.")
    
    def merge_a_dict(self, the_dict:dict) -> dict:
        raise Exception("Cannot merge a dict into a str.")

    def merge_a_str(self, the_str:str):
        self.json_str += the_str


@dataclass
class JsonMergerFactory:
    json_to_merge_into: list | int | dict | str

    def generate_json_merger(self):
        for obj_type, type_merger in zip(
            [
                list,
                int,
                dict,
                str
            ],
            [
                ListJsonMerger,
                IntJsonMerger,
                DictJsonMerger,
                StrJsonMerger
            ]
        ):
            if type(self.json_to_merge_into) == obj_type:
                return type_merger(self.json_to_merge_into)
        raise Exception(f"Json object for merging was not one of the 4 expected types (list, int, dict, str). Instead it was {str(type(self.json_to_merge_into))}")
