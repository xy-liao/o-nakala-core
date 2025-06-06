#!/usr/bin/env python3
"""
CLI interface for NAKALA user info functionality.
This module provides the command-line interface for the user info functionality,
wrapping the core user_info module.
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path to import from the legacy scripts
parent_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(parent_dir))

def main():
    """Main entry point for nakala-user-info CLI command."""
    # Import and execute the user info script
    try:
        from nakala_user_info import main as user_info_main
        user_info_main()
    except ImportError:
        # Fallback to direct execution
        import subprocess
        script_path = parent_dir / "nakala-user-info.py"
        subprocess.run([sys.executable, str(script_path)] + sys.argv[1:])

if __name__ == "__main__":
    main()