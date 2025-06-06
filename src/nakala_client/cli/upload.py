#!/usr/bin/env python3
"""
CLI interface for NAKALA upload functionality.
This module provides the command-line interface for the upload functionality,
wrapping the core upload module.
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path to import from the legacy scripts
parent_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(parent_dir))

def main():
    """Main entry point for nakala-upload CLI command."""
    # Import and execute the v2 upload script
    try:
        from nakala_client_upload_v2 import main as upload_main
        upload_main()
    except ImportError:
        # Fallback to direct execution
        import subprocess
        script_path = parent_dir / "nakala-client-upload-v2.py"
        subprocess.run([sys.executable, str(script_path)] + sys.argv[1:])

if __name__ == "__main__":
    main()