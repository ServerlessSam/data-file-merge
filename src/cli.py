import argparse

from src.config import BuildConfig


def parse_parameter_string(param_str: str) -> dict:
    dict_to_return = {}
    key_value_pairs = param_str.split(",")

    for pair in key_value_pairs:
        if len(pair.split("=")) != 2:
            raise Exception("Incorrect parameter format used!")
        key = pair.split("=")[0]
        value = pair.split("=")[1]
        if key in dict_to_return:
            raise Exception(f"Parameter with key '{key}' already exists!")
        dict_to_return[key] = value

    return dict_to_return


"""
Usage:
------
    $ dfm [options] [local path to config file]
Available options are:
    -h, --help          Show this help
    -p, --parameters    Parameters to feed into your config (key1:value1,key2:value2...)
--------
- data-file-merge v0.1.0
"""


def main():

    parser = argparse.ArgumentParser(
        description="Merge files into a single file based on the rules defined in a config file."
    )
    parser.add_argument("action", choices=["merge", "split"])
    parser.add_argument(
        "config_file_path",
        type=str,
        help="The complete local path to the data-file-merge config file.",
    )
    parser.add_argument(
        "-p",
        "--parameters",
        type=str,
        help='Key value pairs of parameters. E.g "Key1=Value1,Key2=Value2..."',
    )
    args = parser.parse_args()
    print(args)

    # Parse parameters
    if args.parameters:
        parameters = parse_parameter_string(args.parameters)
    else:
        parameters = None

    if args.action == "merge":
        cfg = BuildConfig.load_config_from_file(args.config_file_path, parameters)
        cfg.build()

    elif args.action == "split":
        raise NotImplementedError(
            "Splitting has not been implimented for data-file-merge ... yet."
        )


if __name__ == "__main__":
    main()
