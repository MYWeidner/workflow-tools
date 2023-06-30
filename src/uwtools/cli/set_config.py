# pylint: disable=duplicate-code

"""
This utility creates a command line interface for handling config files.
"""

import sys
from argparse import ArgumentError, ArgumentParser, HelpFormatter

from uwtools import config, exceptions
from uwtools.utils import cli_helpers


def parse_args(args):
    """
    Function maintains the arguments accepted by this script. Please see
    Python's argparse documentation for more information about settings of each
    argument.
    """
    args = args or ["--help"]
    parser = ArgumentParser(
        description="Set config with user-defined settings.",
        formatter_class=lambda prog: HelpFormatter(prog, max_help_position=8),
    )
    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "-i",
        "--input-base-file",
        help="Path to a YAML, bash/ini, or namelist config base file",
        required=True,
        type=cli_helpers.path_if_file_exists,
    )
    optional = parser.add_argument_group("optional arguments")
    optional.add_argument(
        "-c",
        "--config-file",
        help="Path to YAML, bash/ini, or namelist configuration file.",
        metavar="FILE",
        type=cli_helpers.path_if_file_exists,
    )
    optional.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Print rendered config file to stdout only.",
    )
    optional.add_argument(
        "-l",
        "--log-file",
        # #PM# WHAT TO DO ABOUT THIS LOGDFILE PATH?
        default="/dev/null",  # os.path.join(os.path.dirname(__file__), "set_config.log"),
        help="Optional path to a file to log to",
        metavar="FILE",
    )
    optional.add_argument(
        "-o",
        "--outfile",
        help=(
            "Path to output file. If different from input, will will perform conversion. "
            'For field table output, specify model such as "field_table.FV3_GFS_v16".'
        ),
        metavar="FILE",
    )
    optional.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Print no logging messages.",
    )
    optional.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print all logging messages.",
    )
    optional.add_argument(
        "--compare",
        action="store_true",
        help="Show diff between input base and config files.",
    )
    optional.add_argument(
        "--config-file-type",
        help="Convert provided config file to provided file type.",
        choices=["F90", "INI", "YAML"],
    )
    optional.add_argument(
        "--input-file-type",
        help="Convert provided input file to provided file type.",
        choices=["F90", "INI", "YAML"],
    )
    optional.add_argument(
        "--output-file-type",
        help="Convert provided output file to provided file type.",
        choices=["F90", "FieldTable", "INI", "YAML"],
    )
    optional.add_argument(
        "--show-format",
        action="store_true",
        help="Print the required formatting to generate the requested output file.",
    )
    optional.add_argument(
        "--values-needed",
        action="store_true",
        help="Print a list of required configuration settings.",
    )

    # Parse arguments.

    parsed = parser.parse_args(args)

    # Validate arguments.

    if parsed.show_format and not parsed.outfile:
        raise ArgumentError(None, "Option --show-format requires --outfile")

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
