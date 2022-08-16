from pantry.regex import RegexExtractor

class TestRegexExtractor:

    '''
    Synopsis: Ensures AWS Cloudformation resource types parse correctly. Main use case at the moment.
    TODO: add more test cases when needed.
    '''
    def test_aws_extraction_by_name(self):
        for capture_group, expected_val in zip(
            ["provider", "service", "datatype"],
            ["AWS", "Ec2", "Instance"]
            ):
            regex = RegexExtractor("(?P<provider>.+)::(?P<service>.+)::(?P<datatype>.+)", capture_group)
            assert regex.resolve("AWS::Ec2::Instance") == expected_val

    def test_aws_extraction_by_value(self):
        for i, expected_val in zip(
            [1, 2, 3], # Might need to be 1,2,3
            ["AWS", "Ec2", "Instance"]
            ):
            regex = RegexExtractor("(.+)::(.+)::(.+)", i)
            assert regex.resolve("AWS::Ec2::Instance") == expected_val