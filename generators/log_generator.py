"""
LOG file generator for the Turbo Test File Generator project.
"""

from datetime import datetime, timedelta
import random

from generators.base_generator import BaseGenerator
from metadata.builder import build_metadata
from metadata.sidecar_writer import write_sidecar_metadata
from utils.helpers import build_file_path, ensure_directory


LOG_LEVELS = ["INFO", "WARNING", "ERROR", "DEBUG"]
SERVICE_NAMES = ["auth", "api", "database", "storage", "worker", "scheduler"]
EVENT_MESSAGES = [
    "User login succeeded",
    "User login failed",
    "Database connection established",
    "Database connection lost",
    "File uploaded successfully",
    "File processing started",
    "File processing completed",
    "File processing failed",
    "Background job started",
    "Background job completed",
    "Cache refreshed",
    "Permission denied",
]


class LogGenerator(BaseGenerator):
    """
    Generator for LOG files.
    """

    def __init__(
        self,
        output_dir,
        use_sidecar_metadata=True,
        use_embedded_metadata=True,
    ):
        """
        Initialize the LOG generator with shared settings.
        """
        super().__init__(
            output_dir=output_dir,
            file_type="log",
            use_sidecar_metadata=use_sidecar_metadata,
            use_embedded_metadata=use_embedded_metadata,
        )

    def generate(self, filename, metadata=None, **kwargs):
        """
        Generate a LOG file and return information about it.

        Args:
            filename: Name of the LOG file to generate.
            metadata: Optional custom metadata dictionary.
            **kwargs: Extra options such as output_dir or line_count.

        Returns:
            A dictionary describing the generated file.
        """
        output_dir = kwargs.get("output_dir", self.output_dir)
        line_count = kwargs.get("line_count", 20)

        if not isinstance(line_count, int) or isinstance(line_count, bool) or line_count < 1:
            raise ValueError("line_count must be a positive integer.")

        ensure_directory(output_dir)

        file_path = build_file_path(output_dir, filename)
        built_metadata = build_metadata(filename, self.file_type, metadata)

        start_time = datetime.now() - timedelta(minutes=line_count)
        lines = []

        for index in range(line_count):
            timestamp = (start_time + timedelta(minutes=index)).strftime("%Y-%m-%d %H:%M:%S")
            level = random.choice(LOG_LEVELS)
            service = random.choice(SERVICE_NAMES)
            message = random.choice(EVENT_MESSAGES)
            lines.append(f"{timestamp} [{level}] ({service}) {message}")

        content = "\n".join(lines)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

        sidecar_path = None

        if self.use_sidecar_metadata:
            sidecar_path = write_sidecar_metadata(file_path, built_metadata)

        return {
            "file_name": filename,
            "file_type": self.file_type,
            "file_path": str(file_path),
            "metadata": built_metadata,
            "size_bytes": file_path.stat().st_size,
            "line_count": line_count,
            "sidecar_metadata_enabled": self.use_sidecar_metadata,
            "sidecar_path": str(sidecar_path) if sidecar_path else None,
            "embedded_metadata_enabled": self.use_embedded_metadata,
        }
