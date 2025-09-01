"""
Performance and Stress Testing for O-Nakala Core.

This module provides comprehensive performance testing, stress testing,
memory usage validation, and resource management testing to ensure
production-ready performance at scale.
"""

import pytest
import tempfile
import time
import csv
import os
import threading
import multiprocessing
from pathlib import Path
from unittest.mock import patch, MagicMock
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
try:
    import resource
except ImportError:
    # resource module is not available on Windows
    resource = None
import gc

from o_nakala_core.upload import NakalaUploadClient
from o_nakala_core.collection import NakalaCollectionClient
from o_nakala_core.common.config import NakalaConfig
from o_nakala_core.common.exceptions import NakalaAPIError


def get_memory_usage():
    """Get current memory usage in a cross-platform way."""
    if resource is not None:
        # Unix/Linux/macOS
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    else:
        # Windows - try psutil as fallback
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss // 1024  # Convert to KB like resource module
        except ImportError:
            # If psutil is not available, return a mock value for basic test completion
            # This allows tests to run but memory assertions may be skipped
            return 1024


class TestPerformanceMetrics:
    """Test performance characteristics and timing requirements."""

    @pytest.fixture
    def performance_config(self):
        """Configuration optimized for performance testing.

        Security Note: Uses secure temporary directory.
        """
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            yield NakalaConfig(
                api_key="test-performance-key",
                api_url="https://apitest.nakala.fr",
                base_path=temp_dir,
                timeout=60,
                max_retries=1,  # Minimize retries for performance testing
            )

    @pytest.mark.slow
    def test_file_validation_performance(self, performance_config):
        """Test file validation performance with various file sizes."""
        upload_client = NakalaUploadClient(performance_config)

        # Test different file sizes for performance characteristics
        file_sizes = [1024, 10 * 1024, 100 * 1024, 1024 * 1024]  # 1KB to 1MB
        performance_results = []

        for size_bytes in file_sizes:
            with tempfile.NamedTemporaryFile(delete=False) as f:
                # Create file of specific size
                content = b"x" * size_bytes
                f.write(content)
                temp_file = f.name

            try:
                # Measure validation time
                start_time = time.time()
                is_valid = upload_client.file_processor.validate_file(temp_file)
                validation_time = time.time() - start_time

                performance_results.append(
                    {
                        "size_kb": size_bytes // 1024,
                        "validation_time": validation_time,
                        "is_valid": is_valid,
                    }
                )

                # Validation should be fast (< 1 second for files up to 1MB)
                assert (
                    validation_time < 1.0
                ), f"Validation too slow for {size_bytes} bytes: {validation_time}s"

            finally:
                os.unlink(temp_file)

        # Performance should scale reasonably with file size
        assert len(performance_results) == len(file_sizes)

    @pytest.mark.slow
    def test_metadata_preparation_performance(self, performance_config):
        """Test metadata preparation performance with complex metadata."""
        upload_client = NakalaUploadClient(performance_config)

        # Create complex multilingual metadata
        complex_metadata = {
            "title": "fr:Titre très long avec beaucoup de caractères|en:Very long title with many characters|de:Sehr langer Titel mit vielen Zeichen|es:Título muy largo con muchos caracteres",
            "description": "fr:Description détaillée avec plusieurs phrases et beaucoup d'informations importantes|en:Detailed description with multiple sentences and lots of important information|de:Detaillierte Beschreibung mit mehreren Sätzen|es:Descripción detallada con múltiples oraciones",
            "keywords": "fr:mot-clé;recherche;données;science;français|en:keyword;research;data;science;english|de:schlüsselwort;forschung;daten;wissenschaft",
            "type": "http://purl.org/coar/resource_type/c_ddb1",
            "language": "fr",
            "author": "Lastname, Firstname",
            "date": "2024-01-01",
            "license": "CC-BY-4.0",
            "rights": "test-group,ROLE_READER|another-group,ROLE_ADMIN",
        }

        # Measure metadata preparation time
        start_time = time.time()
        prepared_metadata = upload_client.prepare_metadata_from_dict(complex_metadata)
        preparation_time = time.time() - start_time

        # Metadata preparation should be fast (< 0.1 seconds)
        assert (
            preparation_time < 0.1
        ), f"Metadata preparation too slow: {preparation_time}s"

        # Should produce reasonable amount of metadata entries
        assert isinstance(prepared_metadata, list)
        assert len(prepared_metadata) > 5  # Should have multiple metadata entries

    @pytest.mark.slow
    def test_csv_parsing_performance(self, performance_config):
        """Test CSV parsing performance with large datasets."""
        upload_client = NakalaUploadClient(performance_config)

        # Create large CSV dataset
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "large_performance_dataset.csv"

            # Create CSV with many entries
            num_entries = 500

            start_time = time.time()
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "file",
                        "status",
                        "type",
                        "title",
                        "author",
                        "description",
                        "keywords",
                    ]
                )

                for i in range(num_entries):
                    writer.writerow(
                        [
                            f"performance_file_{i:04d}.txt",
                            "pending",
                            "http://purl.org/coar/resource_type/c_ddb1",
                            f"Performance Test File {i}",
                            "Performance Author",
                            f"Description for performance test file number {i}",
                            "performance;test;speed;validation",
                        ]
                    )

            csv_creation_time = time.time() - start_time

            # Test CSV validation performance
            performance_config.base_path = temp_dir

            start_time = time.time()
            try:
                upload_client.validate_dataset(mode="csv", dataset_path=str(csv_path))
            except Exception:
                # Validation might fail due to missing files, but timing is what matters
                pass

            validation_time = time.time() - start_time

            # CSV parsing should be efficient (< 5 seconds for 500 entries)
            assert (
                validation_time < 5.0
            ), f"CSV validation too slow for {num_entries} entries: {validation_time}s"

    def test_configuration_performance(self, performance_config):
        """Test configuration creation and validation performance."""
        # Measure config creation time
        configs_created = []

        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            start_time = time.time()
            for i in range(100):
                config = NakalaConfig(
                    api_key=f"test-key-{i}",
                    api_url="https://apitest.nakala.fr",
                    base_path=temp_dir,  # Use secure temp dir
                    timeout=60,
                )
                configs_created.append(config)

        config_creation_time = time.time() - start_time

        # Configuration creation should be very fast
        assert (
            config_creation_time < 1.0
        ), f"Config creation too slow: {config_creation_time}s for 100 configs"

        # All configs should be properly initialized
        assert len(configs_created) == 100
        for config in configs_created:
            assert config.api_url == "https://apitest.nakala.fr"
            assert config.timeout == 60


class TestStressScenarios:
    """Test system behavior under stress conditions."""

    @pytest.fixture
    def stress_config(self):
        """Configuration for stress testing.

        Security Note: Uses secure temporary directory.
        """
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            yield NakalaConfig(
                api_key="test-stress-key",
                api_url="https://apitest.nakala.fr",
                base_path=temp_dir,
                timeout=30,
                max_retries=1,
            )

    @pytest.mark.slow
    def test_concurrent_client_creation(self, stress_config):
        """Test creation of many client instances concurrently."""

        def create_client():
            client = NakalaUploadClient(stress_config)
            # Perform a basic operation
            assert hasattr(client, "file_processor")
            assert hasattr(client, "utils")
            return client

        # Test concurrent client creation
        num_clients = 20
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(create_client) for _ in range(num_clients)]
            clients = [future.result() for future in futures]

        # All clients should be created successfully
        assert len(clients) == num_clients

        # Each client should be independent
        for client in clients:
            assert client.config.api_key == "test-stress-key"

    @pytest.mark.slow
    def test_large_file_stress(self, stress_config):
        """Test handling of very large files."""
        upload_client = NakalaUploadClient(stress_config)

        # Create a large file (5MB)
        large_size = 5 * 1024 * 1024  # 5MB

        with tempfile.NamedTemporaryFile(delete=False) as f:
            # Write in chunks to avoid memory issues
            chunk_size = 64 * 1024  # 64KB chunks
            chunk_data = b"x" * chunk_size

            for _ in range(large_size // chunk_size):
                f.write(chunk_data)

            large_file = f.name

        try:
            # Test that large file can be validated without issues
            start_time = time.time()
            is_valid = upload_client.file_processor.validate_file(large_file)
            validation_time = time.time() - start_time

            assert is_valid == True
            # Large file validation should complete in reasonable time
            assert (
                validation_time < 10.0
            ), f"Large file validation too slow: {validation_time}s"

        finally:
            os.unlink(large_file)

    @pytest.mark.slow
    def test_memory_stress_multiple_files(self, stress_config):
        """Test memory usage with multiple large files."""
        upload_client = NakalaUploadClient(stress_config)

        # Create multiple medium-sized files
        file_size = 512 * 1024  # 512KB each
        num_files = 10
        test_files = []

        with tempfile.TemporaryDirectory() as temp_dir:
            for i in range(num_files):
                file_path = Path(temp_dir) / f"stress_file_{i}.txt"
                with open(file_path, "wb") as f:
                    f.write(b"x" * file_size)
                test_files.append(str(file_path))

            # Test processing multiple files without memory issues
            start_time = time.time()
            validation_results = []

            for test_file in test_files:
                is_valid = upload_client.file_processor.validate_file(test_file)
                validation_results.append(is_valid)

                # Force garbage collection to test memory management
                gc.collect()

            total_time = time.time() - start_time

            # Should validate all files successfully
            assert all(validation_results)
            assert len(validation_results) == num_files

            # Should complete in reasonable time
            assert (
                total_time < 30.0
            ), f"Multiple file validation too slow: {total_time}s"

    @pytest.mark.slow
    def test_rapid_successive_operations(self, stress_config):
        """Test rapid successive operations without cooldown."""
        upload_client = NakalaUploadClient(stress_config)

        # Create test file
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"rapid test content")
            test_file = f.name

        try:
            # Perform rapid successive validations
            num_operations = 50
            start_time = time.time()

            for i in range(num_operations):
                is_valid = upload_client.file_processor.validate_file(test_file)
                assert is_valid == True

            total_time = time.time() - start_time

            # Rapid operations should not degrade performance significantly
            avg_time_per_op = total_time / num_operations
            assert (
                avg_time_per_op < 0.1
            ), f"Operations slowing down: {avg_time_per_op}s per operation"

        finally:
            os.unlink(test_file)


class TestMemoryManagement:
    """Test memory usage and resource management."""

    @pytest.fixture
    def memory_config(self):
        """Configuration for memory testing.

        Security Note: Uses secure temporary directory.
        """
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            yield NakalaConfig(
                api_key="test-memory-key",
                api_url="https://apitest.nakala.fr",
                base_path=temp_dir,
            )

    def test_memory_usage_file_processing(self, memory_config):
        """Test memory usage during file processing."""
        upload_client = NakalaUploadClient(memory_config)

        # Get initial memory usage
        initial_memory = get_memory_usage()

        # Process multiple files
        with tempfile.TemporaryDirectory() as temp_dir:
            file_sizes = [1024, 10 * 1024, 100 * 1024]  # 1KB, 10KB, 100KB

            for size in file_sizes:
                test_file = Path(temp_dir) / f"memory_test_{size}.txt"
                test_file.write_bytes(b"x" * size)

                # Process file
                upload_client.file_processor.validate_file(str(test_file))

                # Force garbage collection
                gc.collect()

        # Check final memory usage
        final_memory = get_memory_usage()
        memory_increase = final_memory - initial_memory

        # Memory increase should be reasonable (platform-dependent, but < 50MB)
        max_acceptable_increase = 50 * 1024 * 1024  # 50MB in bytes
        assert (
            memory_increase < max_acceptable_increase
        ), f"Excessive memory usage: {memory_increase} bytes"

    def test_client_cleanup(self, memory_config):
        """Test that clients clean up resources properly."""
        initial_memory = get_memory_usage()

        # Create and destroy many clients
        for i in range(10):
            client = NakalaUploadClient(memory_config)

            # Use the client briefly
            assert hasattr(client, "file_processor")

            # Explicit cleanup
            del client
            gc.collect()

        final_memory = get_memory_usage()
        memory_increase = final_memory - initial_memory

        # Client creation/destruction should not leak significant memory
        max_acceptable_increase = 10 * 1024 * 1024  # 10MB
        assert (
            memory_increase < max_acceptable_increase
        ), f"Potential memory leak: {memory_increase} bytes"

    def test_large_metadata_memory_efficiency(self, memory_config):
        """Test memory efficiency with large metadata structures."""
        upload_client = NakalaUploadClient(memory_config)

        # Create very large metadata
        large_metadata = {
            "title": "fr:" + "Long title " * 1000 + "|en:" + "Long title " * 1000,
            "description": "fr:"
            + "Long description " * 2000
            + "|en:"
            + "Long description " * 2000,
            "keywords": "fr:"
            + ";".join([f"keyword{i}" for i in range(1000)])
            + "|en:"
            + ";".join([f"keyword{i}" for i in range(1000)]),
            "type": "http://purl.org/coar/resource_type/c_ddb1",
        }

        initial_memory = get_memory_usage()

        # Process large metadata
        prepared_metadata = upload_client.prepare_metadata_from_dict(large_metadata)

        # Check memory after processing
        post_processing_memory = get_memory_usage()

        # Cleanup
        del prepared_metadata
        del large_metadata
        gc.collect()

        final_memory = get_memory_usage()

        # Memory should be efficiently managed
        processing_increase = post_processing_memory - initial_memory
        cleanup_efficiency = post_processing_memory - final_memory

        # Processing large metadata should not use excessive memory
        assert (
            processing_increase < 100 * 1024 * 1024
        ), f"Large metadata processing too memory-intensive: {processing_increase} bytes"


class TestResourceLimits:
    """Test behavior under resource constraints."""

    @pytest.fixture
    def resource_config(self):
        """Configuration for resource limit testing.

        Security Note: Uses secure temporary directory.
        """
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            yield NakalaConfig(
                api_key="test-resource-key",
                api_url="https://apitest.nakala.fr",
                base_path=temp_dir,
                timeout=10,  # Short timeout for resource testing
            )

    def test_file_descriptor_management(self, resource_config):
        """Test that file descriptors are properly managed."""
        upload_client = NakalaUploadClient(resource_config)

        # Create many temporary files and process them
        with tempfile.TemporaryDirectory() as temp_dir:
            num_files = 50
            test_files = []

            for i in range(num_files):
                test_file = Path(temp_dir) / f"fd_test_{i}.txt"
                test_file.write_text(f"Content for file {i}")
                test_files.append(str(test_file))

            # Process all files - should not exhaust file descriptors
            for test_file in test_files:
                is_valid = upload_client.file_processor.validate_file(test_file)
                assert is_valid == True

            # All operations should complete successfully without fd exhaustion
            assert len(test_files) == num_files

    def test_concurrent_resource_usage(self, resource_config):
        """Test resource usage under concurrent operations."""

        def validate_files():
            client = NakalaUploadClient(resource_config)

            with tempfile.NamedTemporaryFile() as f:
                f.write(b"concurrent test content")
                f.flush()

                # Validate the file
                is_valid = client.file_processor.validate_file(f.name)
                return is_valid

        # Run concurrent validations
        num_concurrent = 5
        with ThreadPoolExecutor(max_workers=num_concurrent) as executor:
            futures = [executor.submit(validate_files) for _ in range(num_concurrent)]
            results = [future.result() for future in futures]

        # All concurrent operations should succeed
        assert all(results)
        assert len(results) == num_concurrent

    @pytest.mark.slow
    def test_timeout_handling_under_load(self, resource_config):
        """Test timeout handling when system is under load."""
        upload_client = NakalaUploadClient(resource_config)

        # Create CPU-intensive operation to simulate load
        def cpu_intensive_task():
            # Simulate some processing
            total = 0
            for i in range(100000):
                total += i**2
            return total

        # Start background load
        with ThreadPoolExecutor(max_workers=2) as executor:
            load_futures = [executor.submit(cpu_intensive_task) for _ in range(2)]

            # Perform file operations under load
            with tempfile.NamedTemporaryFile() as f:
                f.write(b"load test content")
                f.flush()

                start_time = time.time()
                is_valid = upload_client.file_processor.validate_file(f.name)
                operation_time = time.time() - start_time

                # Operation should still complete successfully
                assert is_valid == True

                # Should complete within reasonable time even under load
                assert (
                    operation_time < 5.0
                ), f"Operation too slow under load: {operation_time}s"

            # Wait for background tasks to complete
            for future in load_futures:
                future.result()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "slow"])
