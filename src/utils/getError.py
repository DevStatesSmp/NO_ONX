import sys
import logging
from typing import List, Optional

RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def print_error(args: List[str], get_error: Optional[str] = None, to_stderr: bool = False) -> None:
    """
    Prints a formatted error message for unknown or incomplete commands.

    Args:
        args: List of command arguments.
        get_error: Optional additional error information.
        to_stderr: If True, outputs to stderr instead of stdout.
    """
    error_message = f"{RED}[!] Unknown or incomplete command:{RESET} {' '.join(args)}"
    if get_error:
        error_message += f"\nInformation:\n{get_error}"
    error_message += f"\nRun with {YELLOW}nnx --help{RESET} to see available modules.\n"

    if to_stderr:
        print(error_message, file=sys.stderr)
    else:
        print(error_message)