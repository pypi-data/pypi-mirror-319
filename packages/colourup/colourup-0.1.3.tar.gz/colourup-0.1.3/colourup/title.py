"""This module contains the code for the title function."""

import sys


def title(text: str, borderchar: str = "=", borderlen: int = 10, endln=True) -> None:
    """Create a centered text with decorative borders.

    Args:
        text (str): The text to display.
        borderchar (str): The character used for the border.
        borderlen (int): The length of the border.
        endln (bool): Whether to add a newline before the title.

    Returns:
        None
    """
    border = borderchar * borderlen
    sys.stdout.write(f"{"\n" if endln else ""}{border} {text} {border}\n")
