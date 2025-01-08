#!/usr/bin/env python3
"""
diffract: A CLI tool to diff Python objects by dotted path.

Example usage:
    diffract mypkg.mymodule.some_func otherpkg.module.OtherClass.some_method

Colorized Diffs:
    If `rich` is installed, output will be shown in color.
    Another option is to pipe the output into other tools
    such as `colordiff`.
"""

import sys
import argparse
import enum
from .core import diff_objects, print_diff
from .__version__ import __version__


class ExitCode(enum.IntEnum):
    """
    Exit codes mimicking traditional Unix diff behavior:
    - NO_DIFFERENCES (0) = no differences
    - DIFFERENCES (1) = differences found
    - ERROR (2) = error encountered
    """

    NO_DIFFERENCES = 0
    DIFFERENCES = 1
    ERROR = 2


def make_parser() -> argparse.ArgumentParser:
    """
    Create and return the ArgumentParser for diffract.
    """
    parser = argparse.ArgumentParser(
        description="Diff two Python objects via dotted paths."
    )
    parser.add_argument("obj1", help="e.g. mypkg.mymodule.SomeClass.my_method")
    parser.add_argument("obj2", help="e.g. mypkg2.mymodule2.OtherClass.other_method")
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    return parser


def main() -> None:
    """
    Parse arguments, diff objects, and handle CLI output/exit codes.
    """
    parser = make_parser()
    args = parser.parse_args()

    try:
        diff_lines = list(diff_objects(args.obj1, args.obj2))
    except (ImportError, OSError) as e:
        path = getattr(e, "path", None)
        path_str = f"{path}: " if path else ""
        msg = getattr(e, "msg", str(e))
        print(f"{parser.prog}: {path_str}{msg}")
        sys.exit(ExitCode.ERROR)

    if not diff_lines:
        sys.exit(ExitCode.NO_DIFFERENCES)

    print_diff(diff_lines)
    sys.exit(ExitCode.DIFFERENCES)


if __name__ == "__main__":
    main()
