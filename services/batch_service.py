"""
Batch service for orchestrating file generation runs.
"""

from utils.validators import validate_file_count, validate_file_type
from services.naming_service import generate_filename
from services.folder_service import get_output_subfolder


def run_batch_generation(
    generators,
    output_dir,
    file_types,
    file_count,
    use_nested_folders=False,
    custom_metadata=None,
):
    """
    Run a batch file generation process.

    Args:
        generators: Dictionary mapping file types to generator instances.
        output_dir: Base output directory.
        file_types: List of file types to generate.
        file_count: Number of files to generate per file type.
        use_nested_folders: Whether to place files into type-related subfolders.
        custom_metadata: Optional metadata dictionary to pass to generators.

    Returns:
        A list of dictionaries describing generated files.
    """
    if not isinstance(generators, dict) or not generators:
        raise ValueError("generators must be a non-empty dictionary.")

    validated_count = validate_file_count(file_count)

    if not isinstance(file_types, list) or not file_types:
        raise ValueError("file_types must be a non-empty list.")

    if not isinstance(use_nested_folders, bool):
        raise ValueError("use_nested_folders must be a boolean.")

    if custom_metadata is not None and not isinstance(custom_metadata, dict):
        raise ValueError("custom_metadata must be a dictionary or None.")

    results = []

    for file_type in file_types:
        validated_file_type = validate_file_type(file_type)

        if validated_file_type not in generators:
            raise ValueError(f"No generator registered for file type: {validated_file_type}")

        generator = generators[validated_file_type]
        target_folder = get_output_subfolder(
            output_dir,
            validated_file_type,
            use_nested_folders=use_nested_folders,
        )

        for index in range(1, validated_count + 1):
            filename = generate_filename(validated_file_type, index)
            result = generator.generate(
                filename=filename,
                metadata=custom_metadata,
                output_dir=target_folder,
            )

            if not isinstance(result, dict):
                raise ValueError(
                    f"Generator for '{validated_file_type}' must return a dictionary."
                )

            results.append(result)

    return results
