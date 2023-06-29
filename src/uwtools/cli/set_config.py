# pylint: disable=duplicate-code

"""
This utility creates a command line interface for handling config files.
"""

import sys
from argparse import ArgumentError, ArgumentParser

from uwtools import config, exceptions
from uwtools.utils import cli_helpers


def parse_args(args):
    """
    Function maintains the arguments accepted by this script. Please see
    Python's argparse documentation for more information about settings of each
    argument.
    """

    parser = ArgumentParser(description="Set config with user-defined settings.")

    group = parser.add_mutually_exclusive_group()

    parser.add_argument(
        "-i",
        "--input-base-file",
        help="Path to a config base file. Accepts YAML, bash/ini or namelist",
        required=True,
        type=cli_helpers.path_if_file_exists,
    )
    parser.add_argument(
        "-o",
        "--outfile",
        help=(
            "Full path to output file. If different from input, will will perform conversion."
            'For field table output, specify model such as "field_table.FV3_GFS_v16"'
        ),
    )
    parser.add_argument(
        "-c",
        "--config-file",
        help="Optional path to configuration file. Accepts YAML, bash/ini or namelist",
        type=cli_helpers.path_if_file_exists,
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="If provided, print rendered config file to stdout only",
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="If provided, show diff between -i and -c files.",
    )
    parser.add_argument(
        "--show-format",
        action="store_true",
        help="If provided, print the required formatting to generate the requested output file",
    )
    parser.add_argument(
        "--values-needed",
        action="store_true",
        help="If provided, prints a list of required configuration settings to stdout",
    )
    parser.add_argument(
        "--input-file-type",
        help=(
            "If provided, will convert provided input file to provided file type."
            "Accepts YAML, bash/ini or namelist"
        ),
        choices=["YAML", "INI", "F90"],
    )
    parser.add_argument(
        "--config-file-type",
        help=(
            "If provided, will convert provided config file to provided file type."
            "Accepts YAML, bash/ini or namelist"
        ),
        choices=["YAML", "INI", "F90"],
    )
    parser.add_argument(
        "--output-file-type",
        help=(
            "If provided, will convert provided output file to provided file type."
            "Accepts YAML, bash/ini or namelist"
        ),
        choices=["YAML", "INI", "F90", "FieldTable"],
    )
    group.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="If provided, print all logging messages.",
    )
    group.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="If provided, print no logging messages",
    )
    parser.add_argument(
        "-l",
        "--log-file",
        help="Optional path to a specified log file",
        # #PM# WHAT TO DO ABOUT THIS LOGDFILE PATH?
        default="/dev/null",  # os.path.join(os.path.dirname(__file__), "set_config.log"),
    )

    # Parse arguments.

    parsed = parser.parse_args(args)

    # Validate arguments.

    if parsed.show_format and not parsed.outfile:
        raise ArgumentError(None, "Option --show_format requires --outfile")

    if parsed.quiet and parsed.dry_run:
        raise ArgumentError(None, "Specifying --quiet will suppress --dry-run output")

    # Return validated arguments.

    return parsed


def main():
    """
    Main entry-point function.
    """
    cli_args = parse_args(sys.argv[1:])
    LOG_NAME = "set_config"
    cli_log = cli_helpers.setup_logging(
        log_file=cli_args.log_file,
        log_name=LOG_NAME,
        quiet=cli_args.quiet,
        verbose=cli_args.verbose,
    )
    try:
        config.create_config_obj(user_args=cli_args, log=cli_log)
    except exceptions.UWConfigError as e:
        sys.exit(str(e))
