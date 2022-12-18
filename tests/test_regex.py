import pytest

from src.datafilemerge.regex import RegexExtractor


class TestRegexExtractor:

    """
    Synopsis: Ensures AWS Cloudformation resource types parse correctly. Main use case at the moment.
    TODO: add more test cases when needed.
    """

    def test_aws_extraction_by_name(self):
        for capture_group, expected_val in zip(
            ["provider", "service", "datatype"], ["AWS", "Ec2", "Instance"]
        ):
            regex = RegexExtractor(
                "(?P<provider>.+)::(?P<service>.+)::(?P<datatype>.+)", capture_group
            )
            assert regex.resolve("AWS::Ec2::Instance") == expected_val

    def test_aws_extraction_by_value(self):
        for i, expected_val in zip(
            [1, 2, 3], ["AWS", "Ec2", "Instance"]  # Might need to be 1,2,3
        ):
            regex = RegexExtractor("(.+)::(.+)::(.+)", i)
            assert regex.resolve("AWS::Ec2::Instance") == expected_val

    def test_out_of_bounds_extraction(self):
        regex = RegexExtractor(
            "(?P<provider>.+)::(?P<service>.+)::(?P<datatype>.+)", "something_else"
        )
        with pytest.raises(IndexError):
            assert regex.resolve("AWS::Ec2::Instance")
