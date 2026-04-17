"""
Global configuration for the Turbo Test File Generator project.

This file stores constants and default settings used across the app.
Keeping them here avoids hardcoding values all over the project.
"""

from pathlib import Path


# Base project folder
BASE_DIR = Path(__file__).resolve().parent

# Default output folder
OUTPUT_DIR = BASE_DIR / "output"

# Presets folder
PRESETS_DIR = BASE_DIR / "presets"


# Supported file types for the generator
SUPPORTED_FILE_TYPES = [
    "txt",
    "csv",
    "json",
    "log",
    "md",
    "pdf",
    "docx",
    "xlsx",
    "jpg",
    "png",
    "mp3",
    "wav",
]


# Default app settings
DEFAULT_FILE_COUNT = 10
DEFAULT_SIDECAR_METADATA = True
DEFAULT_EMBED_METADATA = True
DEFAULT_USE_NESTED_FOLDERS = False
DEFAULT_RANDOM_SEED = None


# Default metadata values
DEFAULT_AUTHOR = "Turbo Test File Generator"
DEFAULT_CATEGORY = "test_data"
DEFAULT_TAGS = ["generated", "testing", "turbo_db"]


# Common filename prefixes by file type
FILE_TYPE_PREFIXES = {
    "txt": "note",
    "csv": "table",
    "json": "data",
    "log": "event_log",
    "md": "readme",
    "pdf": "report",
    "docx": "document",
    "xlsx": "spreadsheet",
    "jpg": "image",
    "png": "graphic",
    "mp3": "audio",
    "wav": "recording",
}
