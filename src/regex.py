import re
from dataclasses import dataclass


@dataclass
class RegexExtractor:
    """
    Synopsis: a helper class for extracting substrings via regex
    Parameters:
        expression =    a regex expression
        capture_group = the intended capture group as an integer or named string to retrieve as the intended substring
    """

    expression: str
    capture_group: str | int

    def resolve(self, string_input: str) -> str:
        """
        Synopsis :  executes a regex query and filters for a particular capture group
        Parameters:
            string_input =  The string to query against via regex
        Returns:    the string found in the desired capture group after running the regex query
        """
        pattern = re.compile(self.expression)
        match = pattern.match(string_input)
        if not match:
            raise Exception("No match was found in regex.")
        else:
            return match.group(self.capture_group)

    @staticmethod
    def parse_from_sub_dict(sub_dict: dict):
        regex = (
            RegexExtractor(
                sub_dict["Regex"]["Expression"], sub_dict["Regex"]["CaptureGroup"]
            )
            if "Regex" in sub_dict
            else None
        )
        return regex
