"""
Base generator class for all file generators.

Each specific generator will inherit from this class so the app
has a consistent structure for generating files.
"""

from abc import ABC, abstractmethod
from pathlib import Path


class BaseGenerator(ABC):
    """
    Abstract base class for all file generators.
    """

    def __init__(
        self,
        output_dir,
        file_type,
        use_sidecar_metadata=True,
        use_embedded_metadata=True,
    ):
        """
        Initialize the generator with shared settings.

        Args:
            output_dir: Folder where files will be created.
            file_type: File extension/type handled by this generator.
            use_sidecar_metadata: Whether to create a sidecar metadata JSON file.
            use_embedded_metadata: Whether to embed metadata in the file when supported.
        """
        self.output_dir = Path(output_dir)
        self.file_type = file_type
        self.use_sidecar_metadata = use_sidecar_metadata
        self.use_embedded_metadata = use_embedded_metadata

    @abstractmethod
    def generate(self, filename, metadata=None, **kwargs):
        """
        Generate a file and return information about it.

        Args:
            filename: Name of the file to generate.
            metadata: Optional metadata dictionary.
            **kwargs: Extra generator-specific options.

        Returns:
            A dictionary describing the generated file.
        """
        raise NotImplementedError("Subclasses must implement the generate() method.")
