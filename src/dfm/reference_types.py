from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from jsonpath_ng import parse

from dfm.exceptions import ReferenceTypeError
from dfm.regex import RegexExtractor


@dataclass
class BaseReferenceType(ABC):
    """
    Synopsis:   A base class for all reference types to inherit
    """

    parameters: dict = field(default_factory=dict)
    file_content: dict | list = None

    @abstractmethod
    def evaluate(self, value: str, **kwargs) -> str:
        raise NotImplementedError()


@dataclass
class ParameterReferenceType(BaseReferenceType):
    """
    Synopsis:   A class for the 'Parameter' reference type.
                This will retrieve a given parameter to use as a value.
    Parameters:
        parameters = a key-value dictionary of the parameters used when triggering the build/split
        #TODO we should get these in a better way I think.
    """

    def evaluate(self, value: str, regex: str = None) -> str:
        if value in self.parameters:
            if regex:
                return regex.resolve(self.parameters[value])
            else:
                return self.parameters[value]
        else:
            raise ValueError(
                f"Expected parameter with name '{value}' not found. Are your parameters correct?"
            )


@dataclass
class ContentReferenceType(BaseReferenceType):
    """
    Synopsis:   A class for the 'Content' reference type.
                This will retrieve a string/int from a dict/list using jsonpath.
    Parameters:
        file_content = dictionary/list form of a json file
    """

    def evaluate(self, value: str, regex: RegexExtractor = None) -> str:
        """
        Synopsis:   Retrieves desired string (or int cast as string) from a dict/list using jsonpath.
                    The result can be filtered using regex.
        Parameters:
            value = The jsonpath string to use for object navigation.
            regex = The regex object to use for further filtering
        Returns:    The aquired (and possibly filtered) string/int from an original dict/list
        """
        jsonpath_expr = parse(value)
        jsonpath_matches = [
            match.value for match in jsonpath_expr.find(self.file_content)
        ]
        if len(jsonpath_matches) != 1:
            raise ReferenceTypeError(
                f"Content reference type returned {len(jsonpath_matches)} matches instead of the required 1."
            )
        value_in_file = jsonpath_matches[0]
        if type(value_in_file) not in [int, str]:
            raise ReferenceTypeError(
                f"Content from file: {str(value_in_file)} is not a string or int."
            )
        if regex:
            return regex.resolve(value_in_file)
        else:
            return value_in_file


@dataclass
class KeyReferenceType(BaseReferenceType):
    """
    Synopsis:   A class for the "Key" reference type.
                This will retrieve a key's name using jsonpath
    Parameters:
        file_content = dictionary/list form of a json file
    """

    def evaluate(self, value: str, regex: RegexExtractor = None) -> str:
        """
        Synopsis:   Retrieves desired key's name from a dict/list using jsonpath.
                    The result can be filtered using regex.
        Parameters:
            value = The jsonpath string to use for object navigation.
                    Once resolved, this must produce a dictionary with one key.
                    That one key's name will be retrieved.
            regex = The regex object to use for further filtering
        Returns:    The aquired (and possibly filtered) key's name from an original dict/list
        """
        jsonpath_expr = parse(value)
        jsonpath_matches = [
            match.value for match in jsonpath_expr.find(self.file_content)
        ]
        if len(jsonpath_matches) != 1:
            raise ReferenceTypeError(
                f"Key reference type returned {len(jsonpath_matches)} matches instead of the required 1."
                f" A key reference type must return a dictionary with a single key."
            )
        key_in_file = list(jsonpath_matches[0].keys())[0]
        if regex:
            return regex.resolve(key_in_file)
        else:
            return key_in_file


@dataclass
class LiteralReferenceType(BaseReferenceType):
    """
    Synopsis:   A class for the "Literal" reference type
                This will blindly use the string given as the value.
    """

    def evaluate(self, value: str, regex: RegexExtractor = None) -> str:
        """
        Synopsis:   Blindly returns a string value
        Parameters:
            value = The string to blindly return
        """
        if regex:
            return regex.resolve(str(value))
        else:
            return str(value)


@dataclass
class ReferenceTypeFactory:
    reference_type_str: str

    REFERENCE_TYPE_MAPPING = tuple(
        zip(
            ["Parameter", "Content", "Key", "Literal"],
            [
                ParameterReferenceType,
                ContentReferenceType,
                KeyReferenceType,
                LiteralReferenceType,
            ],
        )
    )

    def generate(self):
        for type in self.REFERENCE_TYPE_MAPPING:
            if self.reference_type_str == type[0]:
                return type[1]
        raise ReferenceTypeError(
            f"Reference type was not found for string: {self.reference_type_str}"
        )
