import pytest

from src.datafilemerge.reference_types import (
    ContentReferenceType,
    KeyReferenceType,
    LiteralReferenceType,
    ParameterReferenceType,
    ReferenceTypeFactory,
)


class TestLiteralReferenceType:
    def test_literal_reference_type_with_string(self):
        assert LiteralReferenceType().evaluate("One") == "One"

    def test_literal_reference_type_with_int(self):
        assert LiteralReferenceType().evaluate(1) == "1"


class TestParameterReferenceType:
    def test_parameter_reference_type(self):
        assert (
            ParameterReferenceType(
                parameters={"Key1": "Value1", "Key2": "Value2"}
            ).evaluate("Key1")
            == "Value1"
        )


class TestReferenceTypeFactory:
    def test_reference_type_factory(self):
        assert ReferenceTypeFactory("Literal").generate() == LiteralReferenceType
        assert ReferenceTypeFactory("Key").generate() == KeyReferenceType
        assert ReferenceTypeFactory("Content").generate() == ContentReferenceType
        assert ReferenceTypeFactory("Parameter").generate() == ParameterReferenceType
        with pytest.raises(Exception):
            assert ReferenceTypeFactory("ItsATrap").generate()
