#!/bin/bash
set -e

echo "=== O-Nakala Core Functionality Test ==="

# 1. Installation check
echo "1. Checking installation..."
pip install -e .[all]

# 2. Run test suite
echo "2. Running test suite..."
pytest tests/ -v --cov=src/nakala_client

# 3. Code quality checks
echo "3. Running code quality checks..."
black --check src/ || echo "Code formatting issues found"
flake8 src/ || echo "Linting issues found"

# 4. CLI command availability
echo "4. Testing CLI commands availability..."
nakala-upload --help > /dev/null && echo "✓ nakala-upload"
nakala-collection --help > /dev/null && echo "✓ nakala-collection" 
nakala-curator --help > /dev/null && echo "✓ nakala-curator"
nakala-user-info --help > /dev/null && echo "✓ nakala-user-info"

# 5. Import tests
echo "5. Testing Python imports..."
python -c "import nakala_client; print('✓ Core import successful')"
python -c "from nakala_client.upload import *; print('✓ Upload module')"
python -c "from nakala_client.collection import *; print('✓ Collection module')"
python -c "from nakala_client.curator import *; print('✓ Curator module')"

echo "=== Test Complete ==="