#!/usr/bin/env python3
"""
Nakala Curator Script

Provides data curation and quality management tools including:
- Metadata validation and quality assessment
- Duplicate detection across collections and datasets
- Batch metadata modifications with validation
- Quality reporting and recommendations
- Template generation for bulk operations

This script is designed for digital humanities researchers and data managers
who need to maintain high-quality metadata and organize large collections.
"""

import sys
import os

# Add src directory to path to import new modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nakala_client.curator import main

if __name__ == '__main__':
    main()