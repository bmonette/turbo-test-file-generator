"""
Simple test runner for the Turbo Test File Generator project.

This version tests the TXT and CSV generators with the batch service.
"""

from config import OUTPUT_DIR
from generators.text_generator import TextGenerator
from generators.csv_generator import CsvGenerator
from services.batch_service import run_batch_generation


def main():
    """
    Run a small test batch using the TXT and CSV generators.
    """
    try:
        text_generator = TextGenerator(output_dir=OUTPUT_DIR)
        csv_generator = CsvGenerator(output_dir=OUTPUT_DIR)

        generators = {
            "txt": text_generator,
            "csv": csv_generator,
        }

        results = run_batch_generation(
            generators=generators,
            output_dir=OUTPUT_DIR,
            file_types=["txt", "csv"],
            file_count=3,
            use_nested_folders=True,
            custom_metadata={
                "author": "Ben",
                "category": "turbo_db_test",
                "tags": ["batch", "test", "sample"],
            },
        )

        print("\nGeneration complete.\n")

        for result in results:
            print(f"File Name: {result['file_name']}")
            print(f"File Type: {result['file_type']}")
            print(f"File Path: {result['file_path']}")
            if result.get("sidecar_path"):
                print(f"Sidecar Path: {result['sidecar_path']}")
            print(f"Size (bytes): {result['size_bytes']}")

            if "row_count" in result:
                print(f"Row Count: {result['row_count']}")

            print(f"Metadata: {result['metadata']}")
            print("-" * 50)

    except Exception as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
