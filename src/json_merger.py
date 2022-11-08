from abc import ABC
from copy import deepcopy
from dataclasses import dataclass
from types import NoneType


@dataclass
class BaseJsonMerger(ABC):
    """
    Synopsis: A base class to merge values into an object in preparation for producing a new json object.
    """

    def __post_init__(self):
        """
        Synopsis: Prepares a mapping so that a future JSON merger can determine which merge function to use.
        """
        self.TYPE_TO_MERGER_MAPPING = (
            (list, self.merge_a_list),
            (int, self.merge_an_int),
            (dict, self.merge_a_dict),
            (str, self.merge_a_str),
            (NoneType, self.merge_a_none),
        )

    # These merging methods are overridden in specific typed merger JsonMerger classes where appropriate.
    # The default behaviour is to convert the value at the node into a list and append it with the value to merge in.

    def merge_a_list(self, the_list: list):
        self.json_obj = self.json_obj + (the_list)

    def merge_an_int(self, the_int: int):
        self.json_obj = [self.json_obj]
        self.json_obj.append(the_int)

    def merge_a_dict(self, the_dict: dict):
        self.json_obj = [self.json_obj]
        self.json_obj.append(the_dict)

    def merge_a_str(self, the_str: str):
        self.json_obj = [self.json_obj]
        self.json_obj.append(the_str)

    def merge_a_none(self, the_none: NoneType):
        pass

    def merge_obj(self, the_obj: list | int | dict | str):
        """
        Synopsis:   Inspects the object to merge in order to determing what merge function to use. Then use said function.
                    This should be the primary way of using JSON mergers rather than a specific merge_a_*() function itself.
        Parameters:
            the_obj: The object to merge in.
        Returns: The output of the merger function. However the merger function should change attributes of the class without returning anything.
        """
        for object_type, merge_method in self.TYPE_TO_MERGER_MAPPING:
            if type(the_obj) == object_type:
                return merge_method(the_obj)
        raise TypeError(
            f"Json object for merging was not one of the 4 expected types (list, int, dict, str). Instead it was {str(type(the_obj))}"
        )


@dataclass
class ListJsonMerger(BaseJsonMerger):
    """
    Synopsis: A class for merging into a list object
    Parameters:
        json_obj: The original list to merge into.
    """

    json_obj: list

    def merge_a_list(self, the_list: list):
        """
        Synopsis: Merges a list into the list. The two are merged. E.g [A,B]+[C,D]=[A,B,C,D]
        Parameters:
            the_list: The list to merge in.
        """
        self.json_obj += the_list

    def merge_an_int(self, the_int: int):
        """
        Synopsis: Appends the list with the integer.
        Parameters:
            the_int: The int to merge in.
        """
        self.json_obj.append(the_int)

    def merge_a_dict(self, the_dict: dict):
        """
        Synopsis: Appends the list with the dictionary.
        Parameters:
            the_dict: The dict to merge in.
        """
        self.json_obj.append(the_dict)

    def merge_a_str(self, the_str: str):
        """
        Synopsis: Appends the list with the string.
        Parameters:
            the_str: The str to merge in.
        """
        self.json_obj.append(the_str)


@dataclass
class IntJsonMerger(BaseJsonMerger):
    """
    Synopsis: A class for merging into an integer.
    Parameters:
        json_obj: The integer to merge into.
    """

    json_obj: int

    def merge_an_int(self, the_int: int):
        """
        Synopsis: Sums the original integer with the_int.
        Parameters:
            the_int: The integer to merge in.
        """
        self.json_obj += the_int


@dataclass
class DictJsonMerger(BaseJsonMerger):
    """
    Synopsis: A class for merging into a json dictionary
    Parameters:
        json_obj: The original dictionary to merge into.
    """

    json_obj: dict

    def merge_a_dict(self, the_dict: dict):
        """
        Synopsis:   Adds the keys from the_dict to json_obj as part of a merge.
                    Clashing keys will have their values merged recursively as per the documentation
        Parameters:
            the_dict: The dict to merge in.
        """
        for key in the_dict:
            if key in self.json_obj:
                clashing_json_obj_value = deepcopy(self.json_obj[key])
                clashing_json_obj_value_merger = JsonMergerFactory(
                    clashing_json_obj_value
                ).generate_json_merger()
                clashing_json_obj_value_merger.merge_obj(the_dict[key])
                the_dict[key] = clashing_json_obj_value_merger.json_obj
        json_obj_copy = deepcopy(self.json_obj)
        self.json_obj = json_obj_copy | the_dict


@dataclass
class StrJsonMerger(BaseJsonMerger):
    """
    Synopsis: A class for merging into an string.
    Parameters:
        json_obj: The string to merge into.
    """

    json_obj: str


@dataclass
class NoneJsonMerger(BaseJsonMerger):
    """
    Synopsis: A class for merging into None.
    Parameters:
        json_obj: The string to merge into. (Should be 'None')
    """

    json_obj: list | int | dict | str | NoneType

    def merge_a_list(self, the_list: list):
        """
        Synopsis: Replaces the NoneType object with the list.
        Parameters:
            the_list: The list to merge in.
        """
        self.json_obj = the_list

    def merge_an_int(self, the_int: int):
        """
        Synopsis: Replaces the NoneType object with the int.
        Parameters:
            the_int: The int to merge in.
        """
        self.json_obj = the_int

    def merge_a_dict(self, the_dict: dict):
        """
        Synopsis: Replaces the NoneType object with the dict.
        Parameters:
            the_dict: The dict to merge in.
        """
        self.json_obj = the_dict

    def merge_a_str(self, the_str: str):
        """
        Synopsis: Replaces the NoneType object with the string.
        Parameters:
            the_str: The str to merge in.
        """
        self.json_obj = the_str


@dataclass
class JsonMergerFactory:
    """
    Synopsis: A factory for generating the correct JsonMerger class based on the object being merged into.
    Parameters:
        json_to_merge_into: The object to merge into. The type of this object will determine the JsonMerger class initialised.
    Returns: An initialised JsonMerger object of the correct type.
    """

    json_to_merge_into: list | int | dict | str | NoneType

    def generate_json_merger(self):
        for obj_type, type_merger in zip(
            [list, int, dict, str, NoneType],
            [
                ListJsonMerger,
                IntJsonMerger,
                DictJsonMerger,
                StrJsonMerger,
                NoneJsonMerger,
            ],
        ):
            if type(self.json_to_merge_into) == obj_type:
                return type_merger(self.json_to_merge_into)
        raise TypeError(
            f"Json object for merging was not one of the 4 expected types (list, int, dict, str). Instead it was {str(type(self.json_to_merge_into))}"
        )
