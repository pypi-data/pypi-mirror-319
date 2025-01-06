# delete_me_discord/utils.py

import logging
from datetime import timedelta
from typing import List, Dict, Any, Tuple
import argparse

class FetchError(Exception):
    """Custom exception for fetch-related errors."""

def setup_logging(log_level: str = "INFO") -> None:
    """
    Configures the logging settings.

    Args:
        log_level (str): The logging level (e.g., 'DEBUG', 'INFO').
    """
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        numeric_level = logging.INFO
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[logging.StreamHandler()]
    )


def channel_str(channel: Dict[str, Any]) -> str:
    """
    Returns a human-readable string representation of a Discord channel.

    Args:
        channel (Dict[str, Any]): The channel data.

    Returns:
        str: A formatted string representing the channel.
    """
    channel_types: Dict[int, str] = {0: "GuildText", 1: "DM", 3: "GroupDM"}
    channel_type = channel_types.get(channel["type"], "Unknown")
    channel_name = channel.get("name") or ', '.join(
        [recipient.get("username", "Unknown") for recipient in channel.get("recipients", [])]
    )
    return f"{channel_type} {channel_name} (ID: {channel.get('id')})"


def parse_random_range(arg: List[str], parameter_name: str) -> Tuple[float, float]:
    """
    Parses command-line arguments that can accept either one or two float values.
    If two values are provided, ensures the first is less than or equal to the second.

    Args:
        arg (List[str]): List of string arguments.
        parameter_name (str): Name of the parameter (for error messages).

    Returns:
        Tuple[float, float]: A tuple representing the range.
                             If one value is provided, both elements are the same.
                             If two values are provided, they represent the range.

    Raises:
        argparse.ArgumentTypeError: If the input format is incorrect.
    """
    try:
        values = [float(value) for value in arg]
        if len(values) == 1:
            return (values[0], values[0])
        elif len(values) == 2:
            if values[0] > values[1]:
                raise ValueError(f"The first value must be less than or equal to the second value for {parameter_name}.")
            return (values[0], values[1])
        else:
            raise ValueError(f"Expected 1 or 2 values for {parameter_name}, got {len(values)}.")
    except ValueError as e:
        raise argparse.ArgumentTypeError(
            f"Invalid format for {parameter_name}. Provide one value or two values separated by space or comma. Error: {e}"
        ) from e


def parse_preserve_last(time_str: str) -> timedelta:
    """
    Parses a time delta string and returns a timedelta object.

    Supported formats:
    - 'weeks=2'
    - 'days=10'
    - 'hours=5'
    - 'minutes=30'
    - Combinations like 'weeks=1,days=3'

    Args:
        time_str (str): The time delta string.

    Returns:
        timedelta: The corresponding timedelta object.

    Raises:
        argparse.ArgumentTypeError: If the format is incorrect.
    """
    try:
        kwargs = {}
        parts = time_str.split(',')
        for part in parts:
            key, value = part.split('=')
            key = key.strip().lower()
            value = int(value.strip())
            if key not in ['weeks', 'days', 'hours', 'minutes', 'seconds']:
                raise ValueError(f"Unsupported time unit: {key}")
            kwargs[key] = value
        return timedelta(**kwargs)
    except Exception as e:
        raise argparse.ArgumentTypeError(
            f"Invalid time delta format: '{time_str}'. Use format like 'weeks=2,days=3'. Error: {e}"
        ) from e


def confirm_action(prompt: str) -> bool:
    """
    Prompts the user for confirmation.

    Args:
        prompt (str): The confirmation prompt.

    Returns:
        bool: True if the user confirms, False otherwise.
    """
    while True:
        response = input(f"{prompt} (y/n): ").strip().lower()
        if response in {'y', 'yes'}:
            return True
        elif response in {'n', 'no'}:
            return False
        else:
            print("Please respond with 'y' or 'n'.")
