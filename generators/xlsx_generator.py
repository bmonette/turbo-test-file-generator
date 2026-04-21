"""
XLSX file generator for the Turbo Test File Generator project.
"""

from openpyxl import Workbook

from generators.base_generator import BaseGenerator
from metadata.builder import build_metadata
from metadata.sidecar_writer import write_sidecar_metadata
from utils.helpers import build_file_path, ensure_directory
from utils.random_data import get_random_row, get_random_title


def apply_xlsx_properties(workbook, metadata):
    """
    Apply supported metadata fields to XLSX workbook properties.

    Args:
        workbook: openpyxl Workbook instance.
        metadata: Metadata dictionary.
    """
    properties = workbook.properties

    properties.creator = str(metadata.get("author", ""))
    properties.lastModifiedBy = str(metadata.get("author", ""))
    properties.title = str(metadata.get("file_name", ""))
    properties.subject = str(metadata.get("category", ""))
    properties.keywords = ", ".join(metadata.get("tags", []))
    properties.category = str(metadata.get("category", ""))
    properties.identifier = str(metadata.get("test_id", ""))
    properties.description = str(metadata.get("comments", ""))


class XlsxGenerator(BaseGenerator):
    """
    Generator for XLSX files.
    """

    def __init__(
        self,
        output_dir,
        use_sidecar_metadata=True,
        use_embedded_metadata=True,
    ):
        """
        Initialize the XLSX generator with shared settings.
        """
        super().__init__(
            output_dir=output_dir,
            file_type="xlsx",
            use_sidecar_metadata=use_sidecar_metadata,
            use_embedded_metadata=use_embedded_metadata,
        )

    def generate(self, filename, metadata=None, **kwargs):
        """
        Generate an XLSX file and return information about it.

        Args:
            filename: Name of the XLSX file to generate.
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

        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = get_random_title()[:31] or "Sheet1"

        if self.use_embedded_metadata:
            apply_xlsx_properties(workbook, built_metadata)

        rows = [get_random_row() for _ in range(row_count)]
        headers = list(rows[0].keys())

        worksheet.append(headers)

        for row in rows:
            worksheet.append(list(row.values()))

        workbook.save(file_path)

        embedded_metadata_written = self.use_embedded_metadata

        sidecar_path = None
        if self.use_sidecar_metadata:
            sidecar_path = write_sidecar_metadata(file_path, built_metadata)

        return {
            "file_name": filename,
            "file_type": self.file_type,
            "file_path": str(file_path),
            "metadata": built_metadata,
            "size_bytes": file_path.stat().st_size,
            "row_count": row_count,
            "worksheet_name": worksheet.title,
            "sidecar_metadata_enabled": self.use_sidecar_metadata,
            "sidecar_path": str(sidecar_path) if sidecar_path else None,
            "embedded_metadata_enabled": self.use_embedded_metadata,
            "embedded_metadata_written": embedded_metadata_written,
        }
