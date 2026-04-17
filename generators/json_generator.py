"""
JSON file generator for the Turbo Test File Generator project.
"""

import json

from generators.base_generator import BaseGenerator
from metadata.builder import build_metadata
from metadata.sidecar_writer import write_sidecar_metadata
from utils.helpers import build_file_path, ensure_directory
from utils.random_data import get_random_row, get_random_title, get_random_tags


class JsonGenerator(BaseGenerator):
    """
    Generator for JSON files.
    """

    def __init__(
        self,
        output_dir,
        use_sidecar_metadata=True,
        use_embedded_metadata=True,
    ):
        """
        Initialize the JSON generator with shared settings.
        """
        super().__init__(
            output_dir=output_dir,
            file_type="json",
            use_sidecar_metadata=use_sidecar_metadata,
            use_embedded_metadata=use_embedded_metadata,
        )

    def generate(self, filename, metadata=None, **kwargs):
        """
        Generate a JSON file and return information about it.

        Args:
            filename: Name of the JSON file to generate.
            metadata: Optional custom metadata dictionary.
            **kwargs: Extra options such as output_dir or record_count.

        Returns:
            A dictionary describing the generated file.
        """
        output_dir = kwargs.get("output_dir", self.output_dir)
        record_count = kwargs.get("record_count", 5)

        if not isinstance(record_count, int) or isinstance(record_count, bool) or record_count < 1:
            raise ValueError("record_count must be a positive integer.")

        ensure_directory(output_dir)

        file_path = build_file_path(output_dir, filename)
        built_metadata = build_metadata(filename, self.file_type, metadata)

        content = {
            "title": get_random_title(),
            "description": get_random_title(),
            "tags": get_random_tags(),
            "records": [get_random_row() for _ in range(record_count)],
        }

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(content, file, indent=4)

        sidecar_path = None

        if self.use_sidecar_metadata:
            sidecar_path = write_sidecar_metadata(file_path, built_metadata)

        return {
            "file_name": filename,
            "file_type": self.file_type,
            "file_path": str(file_path),
            "metadata": built_metadata,
            "size_bytes": file_path.stat().st_size,
            "record_count": record_count,
            "sidecar_metadata_enabled": self.use_sidecar_metadata,
            "sidecar_path": str(sidecar_path) if sidecar_path else None,
            "embedded_metadata_enabled": self.use_embedded_metadata,
        }
