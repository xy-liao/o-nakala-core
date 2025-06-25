#!/bin/bash

# Complete NAKALA Data Cleanup Script for unakala1 User
# =====================================================
# 
# This script removes ALL data items and collections belonging to unakala1
# from the NAKALA test environment using the existing cleanup tools.
#
# Usage:
#   ./cleanup_all_unakala1_data.sh <api-key>
#   ./cleanup_all_unakala1_data.sh <api-key> --force
#
# Author: o-nakala-core development team
# Date: 2025-06-23

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check arguments
if [ -z "$1" ]; then
    echo -e "${RED}❌ Error: API key required${NC}"
    echo "Usage: $0 <api-key> [--force]"
    echo "Example: $0 33170cfe-f53c-550b-5fb6-4814ce981293"
    exit 1
fi

API_KEY="$1"
FORCE_MODE="$2"

echo -e "${BLUE}🧹 NAKALA Complete Data Cleanup${NC}"
echo "=================================="
echo -e "🔑 API Key: ${API_KEY:0:10}...${API_KEY: -10}"
echo -e "🌐 Environment: NAKALA Test API"
echo ""

# Get current user info
echo -e "${BLUE}🔍 Checking current user data...${NC}"
USER_INFO=$(o-nakala-user-info --api-key "$API_KEY" --collections-only 2>/dev/null || echo "Failed to get user info")

if [[ "$USER_INFO" == *"Failed"* ]]; then
    echo -e "${RED}❌ Failed to connect to NAKALA API${NC}"
    echo "   Check your API key and network connection"
    exit 1
fi

# Extract counts from user info
COLLECTIONS_COUNT=$(echo "$USER_INFO" | grep -o "Found [0-9]* collections" | grep -o "[0-9]*" || echo "0")

echo -e "${GREEN}📊 Current data summary:${NC}"
echo "   📚 Collections: $COLLECTIONS_COUNT"
echo ""

# Safety check
if [ "$COLLECTIONS_COUNT" -eq 0 ]; then
    echo -e "${GREEN}🎉 No data found to cleanup - account is already clean!${NC}"
    exit 0
fi

# Confirmation unless force mode
if [ "$FORCE_MODE" != "--force" ]; then
    echo -e "${YELLOW}⚠️  WARNING: This will PERMANENTLY DELETE ALL user data${NC}"
    echo "   • All $COLLECTIONS_COUNT collections will be removed"
    echo "   • All associated datasets will be removed"
    echo "   • This action cannot be undone"
    echo ""
    read -p "🔴 Type 'DELETE ALL' to confirm permanent deletion: " CONFIRM
    
    if [ "$CONFIRM" != "DELETE ALL" ]; then
        echo -e "${RED}❌ Cleanup cancelled by user${NC}"
        exit 1
    fi
fi

echo ""
echo -e "${BLUE}🚀 Starting complete cleanup process...${NC}"
echo ""

# Method 1: Try using the existing Python cleanup script
if [ -f "cleanup_test_data.py" ]; then
    echo -e "${BLUE}📋 Using existing cleanup script...${NC}"
    
    # Get list of data to cleanup
    TEMP_UPLOAD_FILE="temp_all_data.csv"
    
    # Create a temporary file with all user data for cleanup
    echo "identifier,files,title,status,response" > "$TEMP_UPLOAD_FILE"
    
    # Use o-nakala-curator to get all user datasets and add to temp file
    echo -e "${BLUE}🔍 Gathering all user datasets...${NC}"
    
    # Export all user data
    if command -v o-nakala-curator &> /dev/null; then
        o-nakala-curator --api-key "$API_KEY" --export-user-data --output "$TEMP_UPLOAD_FILE" 2>/dev/null || true
    fi
    
    # Run cleanup with the temporary file
    if [ -f "$TEMP_UPLOAD_FILE" ] && [ -s "$TEMP_UPLOAD_FILE" ]; then
        echo "yes" | python cleanup_test_data.py "$API_KEY" "$TEMP_UPLOAD_FILE" 2>/dev/null || {
            echo -e "${YELLOW}⚠️  Python cleanup script encountered issues, continuing with API calls...${NC}"
        }
        rm -f "$TEMP_UPLOAD_FILE"
    fi
fi

# Method 2: Direct API cleanup using the Python script we just created
echo -e "${BLUE}🔧 Using comprehensive Python cleanup tool...${NC}"

if [ "$FORCE_MODE" == "--force" ]; then
    python cleanup_all_unakala1_data.py "$API_KEY" --force
else
    echo "DELETE ALL" | python cleanup_all_unakala1_data.py "$API_KEY"
fi

# Verification
echo ""
echo -e "${BLUE}🔍 Verifying cleanup...${NC}"
FINAL_INFO=$(o-nakala-user-info --api-key "$API_KEY" --collections-only 2>/dev/null || echo "Failed")

if [[ "$FINAL_INFO" == *"Found 0 collections"* ]]; then
    echo -e "${GREEN}✅ Complete cleanup verified - no data remaining${NC}"
elif [[ "$FINAL_INFO" == *"Failed"* ]]; then
    echo -e "${YELLOW}⚠️  Could not verify cleanup status${NC}"
else
    REMAINING=$(echo "$FINAL_INFO" | grep -o "Found [0-9]* collections" | grep -o "[0-9]*" || echo "unknown")
    echo -e "${YELLOW}⚠️  $REMAINING collections may still remain${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Cleanup process completed!${NC}"
echo -e "${BLUE}📊 For detailed statistics, run the Python script directly${NC}"