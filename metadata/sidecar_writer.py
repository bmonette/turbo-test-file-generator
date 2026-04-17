"""
Sidecar metadata writer for generated files.
"""

import json
from pathlib import Path


def write_sidecar_metadata(file_path, metadata):
    """
    Write metadata to a sidecar JSON file.

    Args:
        file_path: Path to the original file.
        metadata: Metadata dictionary.

    Returns:
        Path to the created sidecar file.
    """
    if not isinstance(metadata, dict):
        raise ValueError("metadata must be a dictionary.")

    base_path = Path(file_path)
    sidecar_path = base_path.with_suffix(base_path.suffix + ".metadata.json")

    with open(sidecar_path, "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=4)

    return sidecar_path
