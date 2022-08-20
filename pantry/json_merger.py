from copy import deepcopy
from dataclasses import dataclass
from typing import Dict

"""
Synopsis: A base class to merge values into an object in preparation for producing a new json object.
"""


@dataclass
class BaseJsonMerger:

    """
    Synopsis: Prepares a mapping so that a future JSON merger can determine which merge function to use.
    """

    def __post_init__(self):
        self.TYPE_TO_MERGER_MAPPING = (
            (list, self.merge_a_list),
            (int, self.merge_an_int),
            (dict, self.merge_a_dict),
            (str, self.merge_a_str),
        )

    def merge_a_list(self, the_list: list):
        raise NotImplementedError

    def merge_an_int(self, the_int: int):
        raise NotImplementedError

    def merge_a_dict(self, the_dict: dict):
        raise NotImplementedError

    def merge_a_str(self, the_str: str):
        raise NotImplementedError

    """
    Synopsis:   Inspects the object to merge in order to determing what merge function to use. Then use said function. 
                This should be the primary way of using JSON mergers rather than a specific merge_a_*() function itself.
    Parameters:
        the_obj: The object to merge in.
    Returns: The output of the merger function. However the merger function should change attributes of the class without returning anything.
    """

    def merge_obj(self, the_obj: list | int | dict | str):
        for mapping in self.TYPE_TO_MERGER_MAPPING:
            if type(the_obj) == mapping[0]:
                return mapping[1](the_obj)
        raise Exception(
            f"Json object for merging was not one of the 4 expected types (list, int, dict, str). Instead it was {str(type(the_obj))}"
        )


"""
Synopsis: A class for merging into a list object
Parameters:
    json_obj: The original list to merge into.
"""


class ListJsonMerger(BaseJsonMerger):
    json_obj: list

    """
    Synopsis: Merges a list into the list. The two are merged. E.g [A,B]+[C,D]=[A,B,C,D]
    Parameters:
        the_list: The list to merge in.
    """

    def merge_a_list(self, the_list: list) -> list:
        self.json_obj += the_list

    """
    Synopsis: Appends the list with a new element, being the integer. E.g [A,B]+1=[A,B,1]
    Parameters:
        the_int: The integer to merge in.
    """

    def merge_an_int(self, the_int: int) -> list:
        self.json_obj.append(the_int)

    """
    Synopsis: Appends the list with a new element, being the dictionary. E.g [A,B]+{foo:bar}=[A,B,{foo:bar}]
    Parameters:
        the_dict The dictionary to merge in.
    """

    def merge_a_dict(self, the_dict: dict) -> list:
        self.json_obj.append(the_dict)

    """
    Synopsis: Appends the list with a new element, being the string. E.g [A,B]+"foo"=[A,B,"foo"]
    Parameters:
        the_str: The string to merge in.
    """

    def merge_a_str(self, the_str: str) -> list:
        self.json_obj.append(the_str)


"""
Synopsis: A class for merging into an integer.
Parameters:
    json_obj: The integer to merge into.
"""


@dataclass
class IntJsonMerger(BaseJsonMerger):
    json_obj: int

    """
    Synopsis: Ensures an exception is throw when trying to merge a list into an int.
    Parameters:
        the_list: The original list to merge into.
    """

    def merge_a_list(self, the_list: list):
        raise Exception("Cannot merge a list into an int.")

    """
    Synopsis: Sums the original integer with the_int.
    Parameters:
        the_int: The integer to merge in.
    """

    def merge_an_int(self, the_int: int) -> int:
        self.json_obj += the_int

    """
    Synopsis: Ensures an exception is throw when trying to merge a dict into an int.
    Parameters:
        the_dict: The dictionary to merge in.
    """

    def merge_a_dict(self, the_dict: dict):
        raise Exception("Cannot merge a dict into an int.")

    """
    Synopsis: Ensures an exception is throw when trying to merge a str into an int.
    Parameters:
        the_str: The string to merge in.
    """

    def merge_a_str(self, the_str: str):
        raise Exception("Cannot merge a str into an int.")


"""
Synopsis: A class for merging into a json dictionary
Parameters:
    json_obj: The original dictionary to merge into.
"""


@dataclass
class DictJsonMerger(BaseJsonMerger):
    json_obj: dict

    """
    Synopsis: Ensures an exception is throw when trying to merge a list into a dict.
    Parameters:
        the_list: The list to merge in.
    """

    def merge_a_list(self, the_list: list):
        raise Exception("Cannot merge a list into a dict.")

    """
    Synopsis: Ensures an exception is throw when trying to merge an int into a dict.
    Parameters:
        the_int: The integer to merge in.
    """

    def merge_an_int(self, the_int: int):
        raise Exception("Cannot merge an int into a dict.")

    """
    Synopsis:   Adds the keys from the_dict to json_obj as part of a merge.
                Keys cannot be overriden #TODO Maybe make this configurable?
    Parameters:
        the_dict: The dict to merge in.
    """

    def merge_a_dict(self, the_dict: dict) -> dict:
        for key in the_dict:
            if key in self.json_obj:
                raise Exception("Attempting to override keys!")
        json_obj_copy = deepcopy(self.json_obj)
        self.json_obj = json_obj_copy | the_dict

    """
    Synopsis: Ensures an exception is throw when trying to merge a str into a dict.
    Parameters:
        the_str: The string to merge in.
    """

    def merge_a_str(self, the_str: str):
        raise Exception("Cannot merge a str into a dict.")


"""
Synopsis: A class for merging into an string.
Parameters:
    json_obj: The string to merge into.
"""


@dataclass
class StrJsonMerger(BaseJsonMerger):
    json_obj: str

    """
    Synopsis: Ensures an exception is throw when trying to merge a list into a string.
    Parameters:
        the_list: The list to merge in.
    """

    def merge_a_list(self, the_list: list):
        raise Exception("Cannot merge a list into a str.")

    """
    Synopsis: Ensures an exception is throw when trying to merge an int into a string.
    Parameters:
        the_int: The int to merge in.
    """

    def merge_an_int(self, the_int: int):
        raise Exception("Cannot merge an int into a str.")

    """
    Synopsis: Ensures an exception is throw when trying to merge a dict into a string.
    Parameters:
        the_dict: The dict to merge in.
    """

    def merge_a_dict(self, the_dict: dict) -> dict:
        raise Exception("Cannot merge a dict into a str.")

    """
    Synopsis: Appends the_str to the end of json_obj, as part of a merge.
    Parameters:
        the_str: The str to merge in.
    """

    def merge_a_str(self, the_str: str):
        self.json_obj += the_str


"""
Synopsis: A factory for generating the correct JsonMerger class based on the object being merged into.
Parameters:
    json_to_merge_into: The object to merge into. The type of this object will determine the JsonMerger class initialised.
Returns: An initialised JsonMerger object of the correct type.
"""


@dataclass
class JsonMergerFactory:
    json_to_merge_into: list | int | dict | str

    def generate_json_merger(self):
        for obj_type, type_merger in zip(
            [list, int, dict, str],
            [ListJsonMerger, IntJsonMerger, DictJsonMerger, StrJsonMerger],
        ):
            if type(self.json_to_merge_into) == obj_type:
                return type_merger(self.json_to_merge_into)
        raise Exception(
            f"Json object for merging was not one of the 4 expected types (list, int, dict, str). Instead it was {str(type(self.json_to_merge_into))}"
        )
