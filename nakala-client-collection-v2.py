#!/usr/bin/env python3
"""
Improved Nakala Collection Script

This is an updated version of the original nakala-client-collection.py script
that uses the new common utilities and improved architecture.

For backward compatibility, this script maintains the same CLI interface
while using the improved internal modules.
"""

import sys
import os

# Add src directory to path to import new modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nakala_client.collection import main

if __name__ == '__main__':
    main()
