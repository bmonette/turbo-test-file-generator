"""
Validation helpers for the Turbo Test File Generator project.
"""

from pathlib import Path

from config import SUPPORTED_FILE_TYPES


def validate_file_type(file_type):
    """
    Validate a file type against the supported list.

    Args:
        file_type: File extension/type string.

    Returns:
        The normalized file type string.

    Raises:
        ValueError: If the file type is invalid or unsupported.
    """
    if not isinstance(file_type, str) or not file_type.strip():
        raise ValueError("file_type must be a non-empty string.")

    normalized_file_type = file_type.lower().strip()

    if normalized_file_type not in SUPPORTED_FILE_TYPES:
        raise ValueError(f"Unsupported file type: {file_type}")

    return normalized_file_type


def validate_file_count(count):
    """
    Validate the number of files to generate.

    Args:
        count: Number of files.

    Returns:
        The validated count.

    Raises:
        ValueError: If the count is not a positive integer.
    """
    if not isinstance(count, int) or isinstance(count, bool) or count < 1:
        raise ValueError("count must be a positive integer.")

    return count


def validate_output_dir(path):
    """
    Validate an output directory path.

    Args:
        path: Directory path as a string or Path object.

    Returns:
        A Path object for the validated directory path.

    Raises:
        ValueError: If the path is empty.
    """
    if path is None or not str(path).strip():
        raise ValueError("Output directory path must not be empty.")

    return Path(str(path).strip())


def validate_prefix(prefix):
    """
    Validate an optional filename prefix.

    Args:
        prefix: Optional prefix string.

    Returns:
        The stripped prefix string, or None if no prefix was provided.

    Raises:
        ValueError: If prefix is provided but invalid.
    """
    if prefix is None:
        return None

    if not isinstance(prefix, str) or not prefix.strip():
        raise ValueError("prefix must be a non-empty string if provided.")

    return prefix.strip()
