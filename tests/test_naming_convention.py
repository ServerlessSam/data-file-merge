from pantry.naming_conventions import (
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
    def test_string_conversion(self):
        converter = StringConverter(
            from_convention=PascalCase(), to_convention=SnakeCase()
        )

        assert converter.convert("HelloThere!") == "hello_there!"
