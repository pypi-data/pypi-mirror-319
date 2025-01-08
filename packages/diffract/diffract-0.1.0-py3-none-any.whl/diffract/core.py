"""
diffract.core

This module provides the core functionality for diffract, a tool for diffing 
Python objects by dotted path. It includes functions to import a Python object, 
retrieve its source, generate a unified diff, and (optionally) print that diff 
with color highlighting if Rich is installed.
"""

import inspect
from importlib import import_module
from difflib import unified_diff
from typing import Iterable

try:
    from rich.console import Console
    from rich.syntax import Syntax

    _RICH_AVAILABLE = True
except ImportError:
    _RICH_AVAILABLE = False


def import_object(dotted_str: str) -> object:
    """
    Import the longest valid module prefix from a dotted path, then traverse
    remaining attributes to obtain the final object.

    Example:
        dotted_str = "mypkg.mymodule.SomeClass.NestedClass.my_method"

    Returns:
        The final object (function, class, or module attribute).

    Raises:
        ImportError: If no valid module prefix can be imported or if any attribute
                     along the path can't be accessed.
    """
    # TODO(alexbowe): Use importlib.util.resolve_name()?
    parts = dotted_str.split(".")
    for i in reversed(range(1, len(parts) + 1)):
        try:
            obj = import_module(".".join(parts[:i]))
            for attr in parts[i:]:
                obj = getattr(obj, attr)
            return obj
        except ImportError:
            pass
    raise ImportError(f"Cannot import '{dotted_str}'")


def get_source(dotted_str: str) -> str:
    """
    Retrieve source code for a Python object (function, class, method, etc.)
    identified by a dotted path.

    Args:
        dotted_str: A path like "mypkg.mymodule.SomeClass.my_method".

    Returns:
        The source code of the object as a string.

    Raises:
        ImportError: If the module or attribute cannot be imported.
        OSError: If getting the source fails (e.g., built-in or C extension).
    """
    obj = import_object(dotted_str)
    return inspect.getsource(obj)


def diff_objects(obj_path1: str, obj_path2: str) -> Iterable[str]:
    """
    Generate a unified diff between the source code of two objects.

    Args:
        obj_path1: Dotted path to the first object.
        obj_path2: Dotted path to the second object.

    Returns:
        An iterable of unified diff lines (strings).
    """
    try:
        source1 = get_source(obj_path1)
    except (ImportError, OSError) as e:
        e.path = obj_path1
        raise e

    try:
        source2 = get_source(obj_path2)
    except (ImportError, OSError) as e:
        e.path = obj_path2
        raise e

    return unified_diff(
        source1.splitlines(),
        source2.splitlines(),
        fromfile=obj_path1,
        tofile=obj_path2,
    )


def print_diff(diff_lines: Iterable[str]) -> None:
    """
    Print unified diff lines in color if 'rich' is installed,
    otherwise print plain text.

    Args:
        diff_lines: An iterable of strings representing diff lines.
    """
    diff_text = "\n".join(diff_lines)

    if _RICH_AVAILABLE:
        console = Console(force_terminal=True)
        # 'diff' syntax highlights '+' and '-' lines in color
        syntax = Syntax(diff_text, "diff", theme="ansi_dark", line_numbers=False)
        console.print(syntax)
    else:
        print(diff_text)
