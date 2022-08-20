import re
from dataclasses import dataclass

"""
Synopsis: a helper class for extracting substrings via regex
Parameters: 
    expression =    a regex expression
    capture_group = the intended capture group as an integer or named string to retrieve as the intended substring
"""


@dataclass
class RegexExtractor:
    expression: str

    capture_group: str | int

    """
    Synopsis :  executes a regex query and filters for a particular capture group
    Parameters: 
        string_input =  The string to query against via regex
    Returns:    the string found in the desired capture group after running the regex query
    """

    def resolve(self, string_input: str) -> str:
        pattern = re.compile(self.expression)
        match = pattern.match(string_input)
        if not match:
            raise Exception("No match was found in regex.")
        else:
            return match.group(self.capture_group)
