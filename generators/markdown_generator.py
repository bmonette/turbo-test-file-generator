"""
Markdown file generator for the Turbo Test File Generator project.
"""

from generators.base_generator import BaseGenerator
from metadata.builder import build_metadata
from metadata.sidecar_writer import write_sidecar_metadata
from utils.helpers import build_file_path, ensure_directory
from utils.random_data import (
    get_random_paragraph,
    get_random_tags,
    get_random_text,
    get_random_title,
)


class MarkdownGenerator(BaseGenerator):
    """
    Generator for Markdown files.
    """

    def __init__(
        self,
        output_dir,
        use_sidecar_metadata=True,
        use_embedded_metadata=True,
    ):
        """
        Initialize the Markdown generator with shared settings.
        """
        super().__init__(
            output_dir=output_dir,
            file_type="md",
            use_sidecar_metadata=use_sidecar_metadata,
            use_embedded_metadata=use_embedded_metadata,
        )

    def generate(self, filename, metadata=None, **kwargs):
        """
        Generate a Markdown file and return information about it.

        Args:
            filename: Name of the Markdown file to generate.
            metadata: Optional custom metadata dictionary.
            **kwargs: Extra options such as output_dir or section_count.

        Returns:
            A dictionary describing the generated file.
        """
        output_dir = kwargs.get("output_dir", self.output_dir)
        section_count = kwargs.get("section_count", 3)

        if not isinstance(section_count, int) or isinstance(section_count, bool) or section_count < 1:
            raise ValueError("section_count must be a positive integer.")

        ensure_directory(output_dir)

        file_path = build_file_path(output_dir, filename)
        built_metadata = build_metadata(filename, self.file_type, metadata)

        title = get_random_title()
        tags = ", ".join(get_random_tags())
        sections = [f"# {title}", "", f"**Tags:** {tags}", ""]

        for _ in range(section_count):
            section_title = get_random_title()
            intro = get_random_paragraph()
            bullet_items = get_random_tags(count=3)
            code_example = "print('Hello, Turbo DB')"

            sections.extend([
                f"## {section_title}",
                "",
                intro,
                "",
                "### Key Points",
                "",
                *(f"- {item}" for item in bullet_items),
                "",
                "### Example",
                "",
                "```python",
                code_example,
                "```",
                "",
                get_random_text(paragraph_count=2),
                "",
            ])

        content = "\n".join(sections).strip()

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
            "section_count": section_count,
            "sidecar_metadata_enabled": self.use_sidecar_metadata,
            "sidecar_path": str(sidecar_path) if sidecar_path else None,
            "embedded_metadata_enabled": self.use_embedded_metadata,
        }
