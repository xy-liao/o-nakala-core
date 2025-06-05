#!/usr/bin/env python3
"""
Nakala User Info Script

Retrieves information about the connected user including personal data,
collections, datasets, and group permissions.

This script provides detailed information about what the current API key
has access to and what permissions the user has.
"""

import sys
import os

# Add src directory to path to import new modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nakala_client.user_info import main

if __name__ == '__main__':
    main()