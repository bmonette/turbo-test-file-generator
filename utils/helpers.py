"""
Shared helper functions for the Turbo Test File Generator project.
"""

from pathlib import Path


def ensure_directory(path):
    """
    Create a directory if it does not already exist.

    Args:
        path: Directory path as a string or Path object.

    Returns:
        A Path object pointing to the ensured directory.
    """
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def build_file_path(output_dir, filename):
    """
    Build a full file path from an output directory and filename.

    Args:
        output_dir: Directory where the file should be created.
        filename: Name of the file.

    Returns:
        A Path object for the full file path.
    """
    if not filename or not str(filename).strip():
        raise ValueError("filename must be a non-empty string.")
    return Path(output_dir) / str(filename).strip()


def get_file_extension(filename):
    """
    Extract the file extension from a filename.

    Args:
        filename: File name string.

    Returns:
        The file extension without the dot, in lowercase.
        Returns an empty string if no extension exists.
    """
    if not filename or not str(filename).strip():
        return ""
    return Path(str(filename).strip()).suffix.lower().lstrip(".")
