#!/bin/bash

# O-Nakala Core Workflow Validation Test Runner
# 
# This script provides a simple interface to run the comprehensive
# workflow validation test that proves 100% compatibility with the
# documented workflow requirements.

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print header
echo -e "${BLUE}================================================================${NC}"
echo -e "${BLUE}   O-Nakala Core Comprehensive Workflow Validation Test${NC}"
echo -e "${BLUE}================================================================${NC}"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not found${NC}"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "test_workflow_validation.py" ]; then
    echo -e "${RED}❌ test_workflow_validation.py not found${NC}"
    echo "Please run this script from the o-nakala-core directory"
    exit 1
fi

# Set default environment variables for test API
export NAKALA_API_KEY="${NAKALA_API_KEY:-33170cfe-f53c-550b-5fb6-4814ce981293}"
export NAKALA_BASE_URL="${NAKALA_BASE_URL:-https://apitest.nakala.fr}"

echo -e "${YELLOW}🔧 Configuration:${NC}"
echo "   API Key: ${NAKALA_API_KEY:0:8}..."
echo "   Base URL: $NAKALA_BASE_URL"
echo ""

# Install package if needed
echo -e "${YELLOW}📦 Installing O-Nakala Core...${NC}"
pip install -e . > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Package installation successful${NC}"
else
    echo -e "${RED}❌ Package installation failed${NC}"
    exit 1
fi
echo ""

# Run the validation test
echo -e "${YELLOW}🚀 Starting Workflow Validation Test...${NC}"
echo ""

python3 test_workflow_validation.py "$@"
test_exit_code=$?

echo ""
echo -e "${BLUE}================================================================${NC}"

if [ $test_exit_code -eq 0 ]; then
    echo -e "${GREEN}🎉 VALIDATION SUCCESSFUL!${NC}"
    echo -e "${GREEN}   O-Nakala Core system is ready for production use${NC}"
    echo -e "${GREEN}   All documented workflow capabilities validated${NC}"
else
    echo -e "${RED}⚠️  VALIDATION ISSUES DETECTED${NC}"
    echo -e "${YELLOW}   Check the validation report for details${NC}"
    echo -e "${YELLOW}   Some capabilities may need attention${NC}"
fi

echo -e "${BLUE}================================================================${NC}"
echo ""

# Show quick help
echo -e "${YELLOW}📋 Available Options:${NC}"
echo "   ./run_validation_test.sh                    # Standard test"
echo "   ./run_validation_test.sh --verbose          # Detailed logging"
echo "   ./run_validation_test.sh --test-dir /path   # Custom test directory"
echo "   ./run_validation_test.sh --production-api   # Use production API"
echo ""

exit $test_exit_code