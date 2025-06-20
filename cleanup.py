#!/usr/bin/env python3
"""
O-Nakala Core - Pre-Release Cleanup Script

This script cleans up development artifacts, test outputs, and temporary files
to prepare the repository for release or to reset it to a clean state.

Usage:
    python cleanup.py [--dry-run] [--keep-logs] [--help]

Options:
    --dry-run      Show what would be removed without actually removing files
    --keep-logs    Keep log files (useful for debugging)
    --help         Show this help message
"""

import os
import sys
import shutil
import argparse
import json
from pathlib import Path
from typing import List, Dict


class NakalaCleanup:
    """Handles cleanup operations for the o-nakala-core project."""

    def __init__(self, dry_run: bool = False, keep_logs: bool = False):
        self.dry_run = dry_run
        self.keep_logs = keep_logs
        self.project_root = Path(__file__).parent
        self.removed_files = []
        self.removed_dirs = []
        self.preserved_files = []

    def cleanup_development_files(self):
        """Remove development-only documentation and analysis files."""
        # Development files that may exist in root
        dev_files = [
            "feedback_1.md",
            "api_validation_test.py", 
            "fix_data_curation.py",
        ]

        # Development documentation now in docs/development/
        dev_docs = [
            "docs/development/CSV_TRANSFORMATION_ANALYSIS.md",
            "docs/development/DOCUMENTATION_VALIDATION_STRATEGY.md", 
            "docs/development/ENDPOINT_FIELD_IMPROVEMENT_PLAN.md",
            "docs/development/ENDPOINT_IMPLEMENTATION_STATUS.md",
        ]

        print("🗑️  Removing development files...")
        for file in dev_files:
            self._remove_file(file)
            
        print("📝 Removing development documentation...")
        for file in dev_docs:
            self._remove_file(file)

    def cleanup_directories(self):
        """Remove development directories."""
        dev_dirs = [
            "archive", 
            "dev-docs",
            "docs/development",  # Remove entire development docs directory
            "examples/sample_dataset/workshops",  # Remove workshop exercises
            "venv",  # Remove virtual environment
        ]

        print("📁 Removing development directories...")
        for dir_name in dev_dirs:
            self._remove_directory(dir_name)

    def cleanup_build_artifacts(self):
        """Remove Python build artifacts."""
        build_paths = [
            "src/o_nakala_core.egg-info",
            "src/o_nakala_core.egg-info",  # Updated egg-info directory
            "nakala-python-client/build",
            "nakala-python-client/dist", 
            "nakala-python-client/openapi_client.egg-info",
            "build",
            "dist",
            "*.egg-info",
        ]

        print("🏗️  Removing build artifacts...")
        for path in build_paths:
            self._remove_directory(path)

    def cleanup_output_files(self):
        """Remove test output and log files."""
        print("📄 Removing output files...")

        # Output file patterns to check
        csv_output_patterns = [
            "output.csv",
            "collections_output.csv", 
            "upload_results.csv",
            "final_validation_upload.csv",
            "final_test_upload.csv",
            "single_item_test.csv",
            "collection_curation.csv",
            "modification_template.csv",
            "datasets_template.csv",
            "test_modifications.csv",
            "test_curator_modifications.csv",
            "test_upload_output.csv",
        ]

        json_output_indicators = [
            "test_", "debug_", "validation_", "curation_", "results", "output", "report"
        ]

        # Process files in root directory
        for file_path in self.project_root.iterdir():
            if file_path.is_file():
                filename = file_path.name

                # Check specific CSV output files
                if filename in csv_output_patterns:
                    self._remove_file(filename)
                # Check pattern-based CSV files
                elif filename.endswith(".csv") and not self._is_essential_csv(filename):
                    if any(pattern.replace("*", "") in filename for pattern in ["data_curation_", "test_validation_"]):
                        self._remove_file(filename)

                # Check JSON output files
                elif filename.endswith(".json") and self._is_output_json(filename, json_output_indicators):
                    self._remove_file(filename)

    def cleanup_log_files(self):
        """Remove log files (unless --keep-logs is specified)."""
        if self.keep_logs:
            print("📝 Keeping log files (--keep-logs specified)")
            return

        print("📝 Removing log files...")
        # Remove all .log files recursively
        for file_path in self.project_root.rglob("*.log"):
            self._remove_file(str(file_path.relative_to(self.project_root)))

    def cleanup_workshop_outputs(self):
        """Remove generated workshop outputs."""
        print("🎓 Removing workshop generated files...")
        
        # Remove old workshop directory if it exists
        workshop_dir = self.project_root / "o-nakala-workshop" / "outputs"
        if workshop_dir.exists():
            for file_path in workshop_dir.glob("workshop_report_*.md"):
                self._remove_file(str(file_path.relative_to(self.project_root)))
                
        # Clean up Jupyter notebook checkpoints and temporary files
        notebooks_dir = self.project_root / "examples" / "notebooks"
        if notebooks_dir.exists():
            # Remove Jupyter checkpoints
            for checkpoint_dir in notebooks_dir.rglob(".ipynb_checkpoints"):
                self._remove_directory(str(checkpoint_dir.relative_to(self.project_root)))
                
            # Remove temporary files that might be created by the notebook
            temp_files = [
                "upload_results.csv",
                "quality_report.json", 
                "quality_report_after.json",
                "modification_results.json",
                "workshop_modifications.csv"
            ]
            for temp_file in temp_files:
                temp_path = notebooks_dir / temp_file
                if temp_path.exists():
                    self._remove_file(str(temp_path.relative_to(self.project_root)))

    def cleanup_cache_files(self):
        """Remove Python cache files."""
        print("🧹 Removing Python cache files...")
        for cache_dir in self.project_root.rglob("__pycache__"):
            self._remove_directory(str(cache_dir.relative_to(self.project_root)))

        for pyc_file in self.project_root.rglob("*.pyc"):
            self._remove_file(str(pyc_file.relative_to(self.project_root)))
            
        # Remove mypy cache
        mypy_cache = self.project_root / ".mypy_cache"
        if mypy_cache.exists():
            self._remove_directory(".mypy_cache")

    def cleanup_temp_files(self):
        """Remove temporary files and IDE artifacts."""
        print("🗂️  Removing temporary files...")
        temp_patterns = [
            ".DS_Store",
            "Thumbs.db",
            "*.tmp",
            "*.temp",
            "*.swp",
            "*.swo",
            "*~",
        ]

        for pattern in temp_patterns:
            for temp_file in self.project_root.rglob(pattern):
                self._remove_file(str(temp_file.relative_to(self.project_root)))

    def _is_essential_csv(self, filename: str) -> bool:
        """Check if a CSV file is essential and should be preserved."""
        essential_patterns = [
            "folder_data_items.csv",
            "folder_collections.csv",
            "dataset.csv",
        ]

        # Files in examples directory are essential
        if "examples" in str(filename):
            return True

        # Check if it matches essential patterns
        for pattern in essential_patterns:
            if pattern in filename:
                self.preserved_files.append(filename)
                return True

        return False

    def _is_output_json(self, filename: str, indicators: list) -> bool:
        """Check if a JSON file is a development output file."""
        # Don't remove essential JSON files
        essential_files = ["nakala-apitest.json", "nakala_metadata_vocabulary.json"]

        if filename in essential_files:
            self.preserved_files.append(filename)
            return False

        return any(indicator in filename.lower() for indicator in indicators)

    def _remove_file(self, file_path: str):
        """Remove a single file."""
        full_path = self.project_root / file_path

        if full_path.exists():
            if self.dry_run:
                print(f"  Would remove: {file_path}")
            else:
                try:
                    full_path.unlink()
                    print(f"  ✅ Removed: {file_path}")
                    self.removed_files.append(file_path)
                except Exception as e:
                    print(f"  ❌ Failed to remove {file_path}: {e}")
        else:
            print(f"  ⚠️  Not found: {file_path}")

    def _remove_directory(self, dir_path: str):
        """Remove a directory and all its contents."""
        full_path = self.project_root / dir_path

        if full_path.exists() and full_path.is_dir():
            if self.dry_run:
                print(f"  Would remove directory: {dir_path}")
            else:
                try:
                    shutil.rmtree(full_path)
                    print(f"  ✅ Removed directory: {dir_path}")
                    self.removed_dirs.append(dir_path)
                except Exception as e:
                    print(f"  ❌ Failed to remove directory {dir_path}: {e}")
        else:
            print(f"  ⚠️  Directory not found: {dir_path}")

    def generate_report(self):
        """Generate a cleanup report."""
        print("\n" + "=" * 60)
        print("📋 CLEANUP REPORT")
        print("=" * 60)

        print(f"\n📁 Directories removed: {len(self.removed_dirs)}")
        for dir_name in self.removed_dirs:
            print(f"  - {dir_name}")

        print(f"\n📄 Files removed: {len(self.removed_files)}")
        for file_name in self.removed_files:
            print(f"  - {file_name}")

        if self.preserved_files:
            print(f"\n✅ Essential files preserved: {len(self.preserved_files)}")
            for file_name in self.preserved_files:
                print(f"  - {file_name}")

        if self.dry_run:
            print("\n🔍 DRY RUN MODE - No files were actually removed")
            print("Remove --dry-run flag to perform actual cleanup")

        total_removed = len(self.removed_files) + len(self.removed_dirs)
        print(
            f"\n📊 Total items {'would be ' if self.dry_run else ''}removed: {total_removed}"
        )

        if not self.dry_run and total_removed > 0:
            print("\n✨ Project is now in clean, pre-release state!")

        print("=" * 60)

    def verify_essential_files(self):
        """Verify that essential files are still present."""
        essential_files = [
            "src/o_nakala_core/__init__.py",
            "src/o_nakala_core/upload.py",
            "src/o_nakala_core/collection.py",
            "src/o_nakala_core/curator.py",
            "docs/README.md",
            "examples/sample_dataset/folder_data_items.csv",
            "pyproject.toml",
            "setup.py",
        ]

        print("\n🔍 Verifying essential files...")
        missing_files = []

        for file_path in essential_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                missing_files.append(file_path)
                print(f"  ❌ Missing: {file_path}")
            else:
                print(f"  ✅ Present: {file_path}")

        if missing_files:
            print(f"\n⚠️  WARNING: {len(missing_files)} essential files are missing!")
            return False
        else:
            print("\n✅ All essential files are present")
            return True

    def run_full_cleanup(self):
        """Run complete cleanup process."""
        print("🧹 Starting O-Nakala Core cleanup...")
        print(f"📂 Project root: {self.project_root}")

        if self.dry_run:
            print("🔍 DRY RUN MODE - No files will be removed")

        print("\n" + "-" * 60)

        # Perform cleanup operations
        self.cleanup_development_files()
        self.cleanup_directories()
        self.cleanup_build_artifacts()
        self.cleanup_output_files()
        self.cleanup_log_files()
        self.cleanup_workshop_outputs()
        self.cleanup_cache_files()
        self.cleanup_temp_files()

        # Generate report
        self.generate_report()

        # Verify essential files
        if not self.dry_run:
            self.verify_essential_files()


def main():
    """Main entry point for the cleanup script."""
    parser = argparse.ArgumentParser(
        description="Clean up o-nakala-core project for release",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Preview what would be removed
    python cleanup.py --dry-run
    
    # Clean up everything except logs
    python cleanup.py --keep-logs
    
    # Full cleanup (removes everything)
    python cleanup.py
        """,
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be removed without actually removing files",
    )

    parser.add_argument(
        "--keep-logs", action="store_true", help="Keep log files (useful for debugging)"
    )

    args = parser.parse_args()

    # Create and run cleanup
    cleanup = NakalaCleanup(dry_run=args.dry_run, keep_logs=args.keep_logs)
    cleanup.run_full_cleanup()

    return 0


if __name__ == "__main__":
    sys.exit(main())
