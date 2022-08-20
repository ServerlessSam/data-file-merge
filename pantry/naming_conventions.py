import re
from dataclasses import dataclass

"""
Synopsis:   The base naming convention class
Parameters:
    regex = the rstring to use as part of a conversion (if applicable)
"""


@dataclass
class BaseNamingConvention:
    regex = None

    """
    Synopsis:   runs a regex against a string and puts all matches in a lowercase list
    Parameters:
        string_to_convert = string to query against
    Returns:    A list of all the regex matches in lowercase form
    """

    def convert_to_list(self, string_to_convert: str) -> list[str]:
        strings_found = re.findall(self.regex, string_to_convert)
        if not strings_found:
            raise Exception(
                f"{string_to_convert} is not of the expected naming convention."
            )
        lowercase_string_list = list(map(str.lower, strings_found))
        return lowercase_string_list

    def convert_from_list(self, list_to_convert: list[str]) -> str:
        raise NotImplementedError()


"""
Synopsis:   The naming convention class for pascal case
Parameters:
    regex = the rstring to use as part of a conversion. #TODO This regex doesn't enforce pascal from the start of the string. If a string is not pascal to start with, the start is simply not matched. SHOULD FIX.
"""


@dataclass
class PascalCase(BaseNamingConvention):
    regex = r"[A-Z][^A-Z\s]*"

    """
    Synopsis:   Converts a lowercase list of strings to a single pascal case string
    Parameters:
        list_to_convert = a lowercased list of strings
    Returns:    A single string of pascal case naming convention
    """

    def convert_from_list(self, list_to_convert: list[str]) -> str:
        to_return = ""
        for word in list_to_convert:
            if not word.islower():
                raise Exception(
                    "String wasn't lowercase for some reason. Something has gone wrong."
                )
            word[0] = word[0].upper()
            to_return += word
        return to_return


"""
Synopsis:   The naming convention class for snake case
Parameters:
    regex = the rstring to use as part of a conversion. #TODO Improve regex
"""


@dataclass
class SnakeCase(BaseNamingConvention):
    regex = r"(?=(?<=^)|(?<=_))[^A-Z\s]*?(?=_|$)"

    """
    Synopsis:   runs a regex against a string and puts all matches in a lowercase list
    Parameters:
        string_to_convert = string to query against
    Returns:    A list of all the regex matches in lowercase form
    """

    def convert_to_list(self, string_to_convert: str) -> list[str]:
        strings_found = re.findall(self.regex, string_to_convert)
        if not strings_found:
            raise Exception(
                f"{string_to_convert} is not of the expected naming convention."
            )
        else:
            for string_found in strings_found:
                string_found = string_found.LowerCase()

        if (
            len("".join(str(found) for found in strings_found))
            != len(string_to_convert) - len(strings_found) + 1
        ):
            raise Exception("String was not split correctly.")
        return strings_found

    """
    Synopsis:   Converts a lowercase list of strings to a single snake case string
    Parameters:
        list_to_convert = a lowercased list of strings
    Returns:    A single string of snake case naming convention
    """

    def convert_from_list(self, list_to_convert: list[str]) -> str:
        for word in list_to_convert:
            if not word.islower():
                raise Exception(
                    "String wasn't lowercase for some reason. Something has gone wrong."
                )
        return "_".join(str(word) for word in list_to_convert)


"""
Synopsis:   The naming convention class for camel case
Parameters:
    regex = the rstring to use as part of a conversion. #TODO Improve regex
"""


@dataclass
class CamelCase(BaseNamingConvention):
    regex = r"[A-Z][^A-Z\s]*|^[^A-Z\s]*"

    """
    Synopsis:   Converts a lowercase list of strings to a single camel case string
    Parameters:
        list_to_convert = a lowercased list of strings
    Returns:    A single string of camel case naming convention
    """

    def convert_from_list(self, list_to_convert: list[str]) -> str:
        to_return = list_to_convert[0]

        for string in list_to_convert[1:]:
            to_return += string[0].upper()
            to_return += string[1:]

        return to_return


"""
Synopsis:   The naming convention class for upper case
"""


@dataclass
class UpperCase(BaseNamingConvention):
    def convert_to_list(self, string_to_convert: str) -> list[str]:
        return [string_to_convert.lower()]

    def convert_from_list(self, list_to_convert: list[str]) -> str:
        to_return = ""
        for string in list_to_convert:
            to_return += string.upper()


"""
Synopsis:   The naming convention class for lower case
"""


@dataclass
class LowerCase(BaseNamingConvention):
    def convert_to_list(self, string_to_convert: str) -> list[str]:
        return [string_to_convert.lower()]

    def convert_from_list(self, list_to_convert: list[str]) -> str:
        to_return = ""
        for string in list_to_convert:
            to_return += string.lower()


"""
Synopsis:   A class that will parse a 'NamingConvention' value from a config
            and return the naming convention converting from and to.
Parameters:
    conversion_string = a string of the form '{convention1}To{convention2}'.
                        This can be found in config files under the key 'NamingConvention'
"""


@dataclass
class ConversionStringParser:
    conversion_string: str

    SUPPORTED_CONVENTIONS = {
        "Pascal": PascalCase,
        "Snake": SnakeCase,
        "Camel": CamelCase,
        "Upper": UpperCase,
        "Lower": LowerCase,
    }

    def __post_init__(self):
        parsed_naming_conventions = self.parse()
        self.from_convention = parsed_naming_conventions["From"]
        self.to_convention = parsed_naming_conventions["To"]

        """
        Synopsis:   Splits a 'NamingConvention' string to determing the naming convention
                    to convert from and to.
        Returns:    a dictionary with 'From' and 'To' keys
                    and their values are the corresponding naming convention classes.
        """

    def parse(self):
        split_string = self.conversion_string.split("To")
        if len(split_string) != 2:
            raise Exception(
                f"Conversion string {self.conversion_string} is not of the expected format."
            )
        for individual_string in split_string:
            if individual_string not in self.SUPPORTED_CONVENTIONS:
                raise Exception(
                    f"Conversion string requires {individual_string}, but that is not a supported/recognised casing."
                )

        return {
            "From": self.SUPPORTED_CONVENTIONS[split_string[0]],
            "To": self.SUPPORTED_CONVENTIONS[split_string[1]],
        }


"""
Synopsis:   Converts a string from one naming convention to another
Parameters:
    from_convention = The NamingConvention object for converting from
    to_convention = The NamingConvention object for converting to
"""


@dataclass
class StringConverter:
    from_convention: BaseNamingConvention  # TODO should I be useing the base here as the type? I want to be able to use one from a whole group?
    to_convention: BaseNamingConvention

    """
    Synopsis:   Converts a string from one naming convention to another
    Parameters:
        string_to_convert = the string to convert
    Returns:    The converted string
    """

    def convert(self, string_to_convert: str) -> str:
        return self.to_convention.convert_from_list(
            self.from_convention.convert_to_list(string_to_convert)
        )
