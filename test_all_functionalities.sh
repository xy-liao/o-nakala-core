#!/bin/bash
set -e

echo "=== O-Nakala Core Functionality Test ==="

# 1. Installation check
echo "1. Checking installation..."
pip install -e .[all]

# 2. Run test suite
echo "2. Running test suite..."
pytest tests/ -v --cov=src/o_nakala_core

# 3. Code quality checks
echo "3. Running code quality checks..."
black --check src/ || echo "Code formatting issues found"
flake8 src/ || echo "Linting issues found"

# 4. CLI command availability
echo "4. Testing CLI commands availability..."
o-nakala-upload --help > /dev/null && echo "✓ o-nakala-upload"
o-nakala-collection --help > /dev/null && echo "✓ o-nakala-collection" 
o-nakala-curator --help > /dev/null && echo "✓ o-nakala-curator"
o-nakala-user-info --help > /dev/null && echo "✓ o-nakala-user-info"

# 5. Import tests
echo "5. Testing Python imports..."
python -c "import o_nakala_core; print('✓ Core import successful')"
python -c "from o_nakala_core.upload import *; print('✓ Upload module')"
python -c "from o_nakala_core.collection import *; print('✓ Collection module')"
python -c "from o_nakala_core.curator import *; print('✓ Curator module')"

echo "=== Test Complete ==="