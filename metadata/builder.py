"""
Metadata builder for generated files.

This module creates a consistent metadata dictionary that can be used
for embedded metadata, sidecar JSON files, and reporting.
"""

from datetime import datetime
from uuid import uuid4

from config import DEFAULT_AUTHOR, DEFAULT_CATEGORY, DEFAULT_TAGS


def build_metadata(file_name, file_type, custom_metadata=None):
    """
    Build a metadata dictionary for a generated file.

    Args:
        file_name: Name of the generated file.
        file_type: File extension/type of the generated file.
        custom_metadata: Optional dictionary of user-provided metadata values.

    Returns:
        A dictionary containing metadata for the file.
    """
    metadata = {
        "file_name": file_name,
        "file_type": file_type,
        "generated_at": datetime.now().isoformat(),
        "test_id": str(uuid4()),
        "author": DEFAULT_AUTHOR,
        "category": DEFAULT_CATEGORY,
        "tags": list(DEFAULT_TAGS),
    }

    if custom_metadata is not None:
        if not isinstance(custom_metadata, dict):
            raise TypeError("custom_metadata must be a dictionary or None.")
        metadata.update(custom_metadata)

    return metadata
