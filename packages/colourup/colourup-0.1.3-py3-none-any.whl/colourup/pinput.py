"""This module contains the pinput function for displaying styled input prompts."""

import sys


def pinput(prompt: str, customprefix=">>") -> str:
    """Display a styled input prompt with a custom prefix.

    Args:
        prompt (str): The input prompt message.
        customprefix (str): A custom prefix for the input prompt.

    Returns:
        str: The user's input.
    """
    sys.stdout.write("\n" + prompt + "\n" + customprefix + " ")
    sys.stdout.flush()
    return sys.stdin.readline().strip()
