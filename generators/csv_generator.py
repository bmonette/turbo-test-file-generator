"""
CSV file generator for the Turbo Test File Generator project.
"""

import csv

from generators.base_generator import BaseGenerator
from metadata.builder import build_metadata
from utils.helpers import build_file_path, ensure_directory
from utils.random_data import get_random_row


class CsvGenerator(BaseGenerator):
    """
    Generator for CSV files.
    """

    def __init__(
        self,
        output_dir,
        use_sidecar_metadata=True,
        use_embedded_metadata=True,
    ):
        """
        Initialize the CSV generator with shared settings.
        """
        super().__init__(
            output_dir=output_dir,
            file_type="csv",
            use_sidecar_metadata=use_sidecar_metadata,
            use_embedded_metadata=use_embedded_metadata,
        )

    def generate(self, filename, metadata=None, **kwargs):
        """
        Generate a CSV file and return information about it.

        Args:
            filename: Name of the CSV file to generate.
            metadata: Optional custom metadata dictionary.
            **kwargs: Extra options such as output_dir or row_count.

        Returns:
            A dictionary describing the generated file.
        """
        output_dir = kwargs.get("output_dir", self.output_dir)
        row_count = kwargs.get("row_count", 10)

        if not isinstance(row_count, int) or isinstance(row_count, bool) or row_count < 1:
            raise ValueError("row_count must be a positive integer.")

        ensure_directory(output_dir)

        file_path = build_file_path(output_dir, filename)
        built_metadata = build_metadata(filename, self.file_type, metadata)

        rows = [get_random_row() for _ in range(row_count)]
        fieldnames = list(rows[0].keys())

        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        return {
            "file_name": filename,
            "file_type": self.file_type,
            "file_path": str(file_path),
            "metadata": built_metadata,
            "size_bytes": file_path.stat().st_size,
            "row_count": row_count,
            "sidecar_metadata_enabled": self.use_sidecar_metadata,
            "embedded_metadata_enabled": self.use_embedded_metadata,
        }
