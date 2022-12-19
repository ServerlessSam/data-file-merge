from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path

from dfm.reference_types import BaseReferenceType
from dfm.regex import RegexExtractor


@dataclass
class Substitution:
    """
    Synopsis:   A class for handling the preparation of a string substitution.
                The class will use the specified reference type's logic to determine the value to use in substitution.
    Parameters:
        reference_type = The ReferenceType object containing the specific substitution preparation logic
        value = The string to pass into the substitution preparation logic
        regex = The optional regex to filter the result on futher before finalising the substitution value #TODO make this optional
    """

    reference_type: BaseReferenceType  # TODO is this right? I want it to be any reference type so I've set the type to the base which they all inherit?
    value: str
    regex: RegexExtractor = None

    def evaluate(self) -> str:
        """
        Synopsis:   Evaluates a substitution request for a given reference type.
        Returns:    The value to use in the subsiquent substitution.
        """
        return self.reference_type.evaluate(
            self.value, self.regex  # I want to pass this conditionally
        )


@dataclass
class FileLocation:
    """
    Synopsis:   A class for handling the logic for determining a set of file paths.
    Parameters:
        path =  The path string (see pathlib for possible syntax)
        subs =  A dictionary of substitutions to make on the path.
                Each key is the value to sub for in the path
                (so {"key1" : "value1", "key2" : "value2"} will provide substitutions for
                "${key1" and "${key2}" in the path string.)
    Additional:
        resolved_paths = A list of pathlib paths that satisfy the file search
    """

    path: str
    root_path: Path
    subs: dict = field(
        default_factory=dict
    )  # TODO I want this to be dict(Substitution) but I was getting an error that the object was not itterable.

    @cached_property
    def resolved_paths(self) -> list[Path]:
        """
        Synopsis:   Resolves all substitutions against the path string
                    then finds all local files matching this path.
        Returns:    A list of pathlib paths that satisfy the file search
        """
        return list(self.root_path.glob(self.substituted_path))

    @cached_property
    def substituted_path(self) -> str:
        """
        Synopsis: Performs a substitution on the 'path' attribute using the 'subs' attributes as substitutions.
        Returns: A fully substitutited path.
        """
        subbed_path = self.path
        for sub_key in self.subs:
            substitutor = self.subs[sub_key]
            evaluated_sub = substitutor.evaluate()
            subbed_path = subbed_path.replace(f"${{{sub_key}}}", evaluated_sub)
        return subbed_path
