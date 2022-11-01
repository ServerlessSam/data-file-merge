from src.naming_conventions import (
    ConversionStringParser,
    PascalCase,
    SnakeCase,
    StringConverter,
)


class TestNamingConventions:
    def test_conversion_string_parser(self):
        conversion = ConversionStringParser(conversion_string="PascalToSnake")
        print(conversion.from_convention)
        assert issubclass(conversion.from_convention, PascalCase)
        assert issubclass(conversion.to_convention, SnakeCase)


class TestStringConverter:
    class TestConversionFromPascalCase:
        def test_pascal_case_conversion(self):
            converter = StringConverter(
                from_convention=PascalCase(), to_convention=SnakeCase()
            )

            assert converter.convert("HelloThere!") == "hello_there!"

    class TestConversionFromSnakeCase:
        def test_pascal_case_conversion(self):
            converter = StringConverter(
                from_convention=SnakeCase(), to_convention=PascalCase()
            )

            assert converter.convert("hello_there!") == "HelloThere!"
