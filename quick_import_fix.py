#!/usr/bin/env python3
"""
Quick fix for some common unused imports based on flake8 output
"""

import os
import re
from pathlib import Path

# Common unused imports that we can safely remove
UNUSED_IMPORTS = [
    "from pathlib import Path",
    "import asyncio", 
    "import json",
    "import hashlib",
    "from typing import Optional",
    "from dataclasses import asdict",
    "from typing import Set",
    "from datetime import timedelta"
]

def fix_file(file_path):
    """Fix unused imports in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        modified = False
        new_lines = []
        
        for line in lines:
            should_remove = False
            for unused in UNUSED_IMPORTS:
                if line.strip() == unused:
                    print(f"Removing from {file_path}: {line.strip()}")
                    should_remove = True
                    modified = True
                    break
            
            if not should_remove:
                new_lines.append(line)
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"Fixed {file_path}")
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    """Main function"""
    src_dir = Path('src/nakala_client')
    
    for py_file in src_dir.rglob('*.py'):
        fix_file(py_file)

if __name__ == '__main__':
    main()