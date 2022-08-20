from dataclasses import dataclass, field
from pathlib import Path

from pantry.reference_types import BaseReferenceType

"""
Synopsis:   A class for handling the preparation of a string substitution.
            The class will use the specified reference type's logic to determine the value to use in substitution.
Parameters:
    reference_type = The ReferenceType object containing the specific substitution preparation logic
    value = The string to pass into the substitution preparation logic
    regex = The optional regex to filter the result on futher before finalising the substitution value #TODO make this optional
"""


@dataclass
class Substitution:
    reference_type: BaseReferenceType  # TODO is this right? I want it to be any reference type so I've set the type to the base which they all inherit?
    value: str
    regex: str = None

    """
    Synopsis:   Evaluates a substitution request for a given reference type.
    Returns:    The value to use in the subsiquent substitution.
    """

    def evaluate(self) -> str:
        return self.reference_type.evaluate(
            self.value, self.regex  # I want to pass this conditionally
        )


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


@dataclass
class FileLocation:
    path: str
    subs: dict = field(
        default_factory=dict
    )  # TODO I want this to be dict(Substitution) but I was getting an error that the object was not itterable.

    def __post_init__(self):
        self.substituted_path = self.substitute()
        self.resolved_paths = self.resolve()

    """
    Synopsis:   Resolves all substitutions against the path string
                then finds all local files matching this path.
    Returns:    A list of pathlib paths that satisfy the file search
    """

    def resolve(self) -> list[Path]:
        p = Path(
            "/"
        )  # TODO somehow set the root node to search for files from. Either an env var or in the file. Probably the file.
        return list(p.glob(self.substituted_path))

    """
    Synopsis: Performs a substitution on the 'path' attribute using the 'subs' attributes as substitutions.
    Returns: A fully substitutited path.
    """

    def substitute(self) -> str:
        subbed_path = self.path
        for sub_key in self.subs:
            substitutor = self.subs[sub_key]
            evaluated_sub = substitutor.evaluate()
            subbed_path = subbed_path.replace(f"${{{sub_key}}}", evaluated_sub)
        return subbed_path
