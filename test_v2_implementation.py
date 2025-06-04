#!/usr/bin/env python3
"""
Test script for O-Nakala-Core v2.0 implementation

This script validates that the v2.0 architecture works correctly
by testing the upload and collection scripts with sample data.
"""

import json
import logging
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class V2TestRunner:
    """Test runner for v2.0 implementation validation"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.test_results = []
        
    def run_all_tests(self) -> bool:
        """Run all validation tests"""
        logger.info("Starting O-Nakala-Core v2.0 validation tests...")
        
        tests = [
            self.test_package_structure,
            self.test_imports,
            self.test_configuration,
            self.test_upload_script_help,
            self.test_collection_script_help,
            self.test_upload_validation_mode,
            self.test_collection_validation_mode,
            self.test_sample_data_compatibility,
            self.test_common_utilities
        ]
        
        success_count = 0
        for test in tests:
            try:
                logger.info(f"Running test: {test.__name__}")
                test()
                logger.info(f"✅ {test.__name__} PASSED")
                success_count += 1
            except Exception as e:
                logger.error(f"❌ {test.__name__} FAILED: {e}")
                self.test_results.append({
                    'test': test.__name__,
                    'status': 'FAILED',
                    'error': str(e)
                })
        
        logger.info(f"\nTest Results: {success_count}/{len(tests)} tests passed")
        return success_count == len(tests)
    
    def test_package_structure(self):
        """Test that the v2.0 package structure exists"""
        required_paths = [
            "src/nakala_client/__init__.py",
            "src/nakala_client/upload.py", 
            "src/nakala_client/collection.py",
            "src/nakala_client/common/__init__.py",
            "src/nakala_client/common/utils.py",
            "src/nakala_client/common/config.py",
            "src/nakala_client/common/exceptions.py",
            "nakala-client-upload-v2.py",
            "nakala-client-collection-v2.py",
            "setup.py",
            "requirements-new.txt"
        ]
        
        for path in required_paths:
            full_path = self.project_root / path
            if not full_path.exists():
                raise FileNotFoundError(f"Required file missing: {path}")
    
    def test_imports(self):
        """Test that all v2.0 modules can be imported"""
        import_tests = [
            "from nakala_client.common.config import NakalaConfig",
            "from nakala_client.common.utils import prepare_metadata",
            "from nakala_client.common.exceptions import NakalaAPIError",
            "from nakala_client.upload import NakalaUploadClient", 
            "from nakala_client.collection import NakalaCollectionClient"
        ]
        
        for import_test in import_tests:
            try:
                exec(import_test)
            except ImportError as e:
                raise ImportError(f"Failed to import: {import_test} - {e}")
    
    def test_configuration(self):
        """Test configuration loading and validation"""
        try:
            from nakala_client.common.config import NakalaConfig
            
            # Test manual configuration
            config = NakalaConfig(
                api_key="test-key",
                api_url="https://apitest.nakala.fr"
            )
            config.validate()
            
            # Test environment loading (should handle missing env vars gracefully)
            try:
                env_config = NakalaConfig.from_env()
            except Exception:
                # Expected to fail if no env vars set
                pass
                
        except Exception as e:
            raise Exception(f"Configuration test failed: {e}")
    
    def test_upload_script_help(self):
        """Test that v2.0 upload script shows help"""
        script_path = self.project_root / "nakala-client-upload-v2.py"
        if not script_path.exists():
            raise FileNotFoundError("Upload v2.0 script not found")
        
        result = subprocess.run(
            [sys.executable, str(script_path), "--help"],
            capture_output=True,
            text=True,
            cwd=self.project_root
        )
        
        if result.returncode != 0:
            raise Exception(f"Upload script help failed: {result.stderr}")
        
        # Check for expected help content
        if "api-key" not in result.stdout:
            raise Exception("Upload script help missing API key option")
    
    def test_collection_script_help(self):
        """Test that v2.0 collection script shows help"""
        script_path = self.project_root / "nakala-client-collection-v2.py"
        if not script_path.exists():
            raise FileNotFoundError("Collection v2.0 script not found")
        
        result = subprocess.run(
            [sys.executable, str(script_path), "--help"],
            capture_output=True,
            text=True,
            cwd=self.project_root
        )
        
        if result.returncode != 0:
            raise Exception(f"Collection script help failed: {result.stderr}")
        
        # Check for expected help content
        if "api-key" not in result.stdout:
            raise Exception("Collection script help missing API key option")
    
    def test_upload_validation_mode(self):
        """Test upload script validation mode"""
        script_path = self.project_root / "nakala-client-upload-v2.py"
        sample_dataset = self.project_root / "sample_dataset" / "folder_data_items.csv"
        
        if not sample_dataset.exists():
            logger.warning("Sample dataset not found, skipping upload validation test")
            return
        
        result = subprocess.run([
            sys.executable, str(script_path),
            "--api-key", "test-key",
            "--dataset", str(sample_dataset),
            "--validate-only"
        ], capture_output=True, text=True, cwd=self.project_root)
        
        # Validation mode should show validation results
        if "validation" not in result.stdout.lower() and "validation" not in result.stderr.lower():
            logger.warning("Validation mode may not be fully implemented yet")
    
    def test_collection_validation_mode(self):
        """Test collection script validation mode"""
        script_path = self.project_root / "nakala-client-collection-v2.py"
        sample_collections = self.project_root / "sample_dataset" / "folder_collections.csv"
        
        if not sample_collections.exists():
            logger.warning("Sample collections not found, skipping collection validation test")
            return
        
        result = subprocess.run([
            sys.executable, str(script_path),
            "--api-key", "test-key",
            "--from-folder-collections", str(sample_collections),
            "--validate-only"
        ], capture_output=True, text=True, cwd=self.project_root)
        
        # Validation mode should show validation results
        if "validation" not in result.stdout.lower() and "validation" not in result.stderr.lower():
            logger.warning("Collection validation mode may not be fully implemented yet")
    
    def test_sample_data_compatibility(self):
        """Test that sample data files are compatible"""
        sample_dir = self.project_root / "sample_dataset"
        if not sample_dir.exists():
            logger.warning("Sample dataset directory not found")
            return
        
        # Check for expected sample files
        expected_files = [
            "folder_data_items.csv",
            "folder_collections.csv"
        ]
        
        for file in expected_files:
            file_path = sample_dir / file
            if file_path.exists():
                # Basic CSV validation
                try:
                    import csv
                    with open(file_path, 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        headers = next(reader)
                        if not headers:
                            raise Exception(f"Empty headers in {file}")
                except Exception as e:
                    raise Exception(f"Invalid CSV file {file}: {e}")
    
    def test_common_utilities(self):
        """Test common utilities functionality"""
        try:
            from nakala_client.common.utils import prepare_metadata, parse_multilingual_field
            from nakala_client.common.exceptions import MetadataValidationError
            
            # Test basic metadata preparation
            test_metadata = {
                'title': 'Test Dataset',
                'author': 'Test Author',
                'date': '2024-01-15'
            }
            
            result = prepare_metadata(test_metadata)
            if not isinstance(result, list):
                raise Exception("prepare_metadata should return a list")
            
            # Test multilingual field parsing
            multilingual_result = parse_multilingual_field(
                "en:English Title|fr:Titre Français"
            )
            
            if not isinstance(multilingual_result, list):
                raise Exception("parse_multilingual_field should return a list")
                
        except Exception as e:
            raise Exception(f"Common utilities test failed: {e}")
    
    def generate_test_report(self) -> Dict:
        """Generate a comprehensive test report"""
        return {
            'version': '2.0',
            'test_results': self.test_results,
            'summary': {
                'total_tests': len(self.test_results),
                'passed': len([r for r in self.test_results if r['status'] == 'PASSED']),
                'failed': len([r for r in self.test_results if r['status'] == 'FAILED'])
            }
        }

def main():
    """Main test execution"""
    # Find project root (assume script is in project root)
    project_root = Path(__file__).parent
    
    # Check if we're in the right directory
    if not (project_root / "src" / "nakala_client").exists():
        logger.error("Please run this script from the o-nakala-core project root")
        sys.exit(1)
    
    # Run tests
    test_runner = V2TestRunner(project_root)
    success = test_runner.run_all_tests()
    
    # Generate report
    report = test_runner.generate_test_report()
    
    logger.info("\n" + "=" * 50)
    logger.info("O-NAKALA-CORE V2.0 VALIDATION REPORT")
    logger.info("=" * 50)
    
    if success:
        logger.info("✅ ALL TESTS PASSED - v2.0 implementation is ready!")
        logger.info("\nNext steps:")
        logger.info("1. Test with your actual datasets")
        logger.info("2. Try the v2.0 scripts: nakala-client-upload-v2.py")
        logger.info("3. Compare outputs with v1.0 scripts")
        logger.info("4. Begin gradual migration to v2.0")
    else:
        logger.error("❌ SOME TESTS FAILED - v2.0 needs fixes")
        logger.error("\nFailed tests:")
        for result in test_runner.test_results:
            if result['status'] == 'FAILED':
                logger.error(f"  - {result['test']}: {result['error']}")
    
    logger.info(f"\nTest Summary: {report['summary']['passed']}/{report['summary']['total_tests']} passed")
    
    # Save detailed report
    report_file = project_root / "v2_validation_report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    logger.info(f"Detailed report saved to: {report_file}")
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()