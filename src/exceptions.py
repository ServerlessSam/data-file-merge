class ConfigSeperationError(Exception):
    ...


class JsonMergerError(ConfigSeperationError):
    ...


class NamingConventionError(ConfigSeperationError):
    ...


class ReferenceTypeError(ConfigSeperationError):
    ...
