"""
Naming service for generated files.

This module creates consistent and reusable file names based on
file type prefixes, counters, and optional custom prefixes.
"""

from config import FILE_TYPE_PREFIXES


def generate_filename(file_type, index, prefix=None):
    """
    Generate a filename for a given file type.

    Args:
        file_type: File extension/type such as 'txt' or 'pdf'.
        index: Numeric index used to make the filename unique.
        prefix: Optional custom prefix. If not provided, the default
                prefix for the file type will be used.

    Returns:
        A generated filename string.
    """
    if not isinstance(file_type, str) or not file_type.strip():
        raise ValueError("file_type must be a non-empty string.")

    normalized_file_type = file_type.lower().strip()

    if normalized_file_type not in FILE_TYPE_PREFIXES:
        raise ValueError(f"Unsupported file type: {file_type}")

    if not isinstance(index, int) or index < 1:
        raise ValueError("index must be a positive integer.")

    if prefix is not None and (not isinstance(prefix, str) or not prefix.strip()):
        raise ValueError("prefix must be a non-empty string if provided.")

    name_prefix = prefix.strip() if prefix else FILE_TYPE_PREFIXES[normalized_file_type]
    return f"{name_prefix}_{index:03d}.{normalized_file_type}"
