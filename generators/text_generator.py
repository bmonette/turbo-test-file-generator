"""
Text file generator for the Turbo Test File Generator project.
"""

from generators.base_generator import BaseGenerator
from metadata.builder import build_metadata
from utils.helpers import build_file_path, ensure_directory
from utils.random_data import get_random_text


class TextGenerator(BaseGenerator):
    """
    Generator for TXT files.
    """

    def __init__(
        self,
        output_dir,
        use_sidecar_metadata=True,
        use_embedded_metadata=True,
    ):
        """
        Initialize the text generator with shared settings.
        """
        super().__init__(
            output_dir=output_dir,
            file_type="txt",
            use_sidecar_metadata=use_sidecar_metadata,
            use_embedded_metadata=use_embedded_metadata,
        )

    def generate(self, filename, metadata=None, **kwargs):
        """
        Generate a TXT file and return information about it.

        Args:
            filename: Name of the TXT file to generate.
            metadata: Optional custom metadata dictionary.
            **kwargs: Extra options such as output_dir or paragraph_count.

        Returns:
            A dictionary describing the generated file.
        """
        output_dir = kwargs.get("output_dir", self.output_dir)
        paragraph_count = kwargs.get("paragraph_count", 3)

        ensure_directory(output_dir)

        file_path = build_file_path(output_dir, filename)
        content = get_random_text(paragraph_count=paragraph_count)
        built_metadata = build_metadata(filename, self.file_type, metadata)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

        return {
            "file_name": filename,
            "file_type": self.file_type,
            "file_path": str(file_path),
            "metadata": built_metadata,
            "size_bytes": file_path.stat().st_size,
            "sidecar_metadata_enabled": self.use_sidecar_metadata,
            "embedded_metadata_enabled": self.use_embedded_metadata,
        }
