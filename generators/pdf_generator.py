"""
PDF file generator for the Turbo Test File Generator project.
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from pypdf import PdfReader, PdfWriter

from generators.base_generator import BaseGenerator
from metadata.builder import build_metadata
from metadata.sidecar_writer import write_sidecar_metadata
from utils.helpers import build_file_path, ensure_directory
from utils.random_data import get_random_paragraph, get_random_title


def apply_pdf_metadata(file_path, metadata):
    """
    Apply metadata to a PDF file using pypdf.
    """
    reader = PdfReader(file_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    pdf_metadata = {
        "/Title": metadata.get("file_name", ""),
        "/Author": metadata.get("author", ""),
        "/Subject": metadata.get("category", ""),
        "/Keywords": ", ".join(metadata.get("tags", [])),
        "/Producer": "Turbo Test File Generator",
    }

    writer.add_metadata(pdf_metadata)

    with open(file_path, "wb") as f:
        writer.write(f)


class PdfGenerator(BaseGenerator):
    """
    Generator for PDF files.
    """

    def __init__(
        self,
        output_dir,
        use_sidecar_metadata=True,
        use_embedded_metadata=True,
    ):
        super().__init__(
            output_dir=output_dir,
            file_type="pdf",
            use_sidecar_metadata=use_sidecar_metadata,
            use_embedded_metadata=use_embedded_metadata,
        )

    def generate(self, filename, metadata=None, **kwargs):
        output_dir = kwargs.get("output_dir", self.output_dir)

        ensure_directory(output_dir)

        file_path = build_file_path(output_dir, filename)
        built_metadata = build_metadata(filename, self.file_type, metadata)

        # Create PDF content
        c = canvas.Canvas(str(file_path), pagesize=letter)
        width, height = letter

        title = get_random_title()
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, title)

        c.setFont("Helvetica", 10)

        y_position = height - 80

        for _ in range(5):
            paragraph = get_random_paragraph()
            for line in paragraph.split(". "):
                if y_position < 50:
                    c.showPage()
                    y_position = height - 50
                c.drawString(50, y_position, line.strip())
                y_position -= 15

        c.save()

        # Apply embedded metadata
        if self.use_embedded_metadata:
            apply_pdf_metadata(file_path, built_metadata)

        # Write sidecar metadata
        sidecar_path = None
        if self.use_sidecar_metadata:
            sidecar_path = write_sidecar_metadata(file_path, built_metadata)

        return {
            "file_name": filename,
            "file_type": self.file_type,
            "file_path": str(file_path),
            "metadata": built_metadata,
            "size_bytes": file_path.stat().st_size,
            "sidecar_metadata_enabled": self.use_sidecar_metadata,
            "sidecar_path": str(sidecar_path) if sidecar_path else None,
            "embedded_metadata_enabled": self.use_embedded_metadata,
        }
