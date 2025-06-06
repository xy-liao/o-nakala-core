#!/usr/bin/env python3
"""
CLI interface for NAKALA curator functionality.
This module provides the command-line interface for the curator functionality,
wrapping the core curator module.
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path to import from the legacy scripts
parent_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(parent_dir))

def main():
    """Main entry point for nakala-curator CLI command."""
    # Import and execute the curator script
    try:
        from nakala_curator import main as curator_main
        curator_main()
    except ImportError:
        # Fallback to direct execution
        import subprocess
        script_path = parent_dir / "nakala-curator.py"
        subprocess.run([sys.executable, str(script_path)] + sys.argv[1:])

if __name__ == "__main__":
    main()