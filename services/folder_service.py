"""
Folder service for building output folder paths.
"""

from pathlib import Path
import random

from utils.helpers import ensure_directory
from utils.validators import validate_file_type


DEFAULT_FOLDER_CATEGORIES = {
    "txt": ["notes", "drafts", "text_files"],
    "csv": ["tables", "exports", "datasets"],
    "json": ["data", "api_responses", "records"],
    "log": ["logs", "system_logs", "events"],
    "md": ["markdown", "docs", "notes"],
    "pdf": ["pdfs", "reports", "documents"],
    "docx": ["documents", "letters", "reports"],
    "xlsx": ["spreadsheets", "reports", "financials"],
    "jpg": ["images", "photos", "media"],
    "png": ["images", "graphics", "media"],
    "mp3": ["audio", "music", "recordings"],
    "wav": ["audio", "recordings", "raw_audio"],
}


def get_output_subfolder(base_output_dir, file_type, use_nested_folders=False):
    """
    Return the output folder path for a given file type.

    Args:
        base_output_dir: Base output directory.
        file_type: File type such as 'txt' or 'pdf'.
        use_nested_folders: Whether to place files into a type-related subfolder.

    Returns:
        A Path object for the target output folder.
    """
    validated_file_type = validate_file_type(file_type)
    base_path = ensure_directory(base_output_dir)

    if not isinstance(use_nested_folders, bool):
        raise ValueError("use_nested_folders must be a boolean.")

    if not use_nested_folders:
        return base_path

    folder_options = DEFAULT_FOLDER_CATEGORIES.get(validated_file_type, [validated_file_type])
    chosen_folder = random.choice(folder_options)

    target_path = base_path / chosen_folder
    return ensure_directory(target_path)
