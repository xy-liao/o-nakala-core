#!/usr/bin/env python3
"""
O-Nakala Core Web Server Launcher

Simple script to start the FastAPI web server for the O-Nakala Core web interface.
Includes dependency checking and helpful error messages.
"""

import sys
import subprocess
import importlib.util
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        ('fastapi', 'pip install fastapi'),
        ('uvicorn', 'pip install uvicorn'),
    ]
    
    missing_packages = []
    
    for package, install_cmd in required_packages:
        spec = importlib.util.find_spec(package)
        if spec is None:
            missing_packages.append((package, install_cmd))
    
    if missing_packages:
        print("❌ Missing required dependencies:")
        for package, install_cmd in missing_packages:
            print(f"   - {package}: {install_cmd}")
        print("\n💡 Install all dependencies with:")
        print("   pip install fastapi uvicorn")
        return False
    
    return True

def start_server(host="0.0.0.0", port=8000, debug=False):
    """Start the O-Nakala Core web server."""
    
    if not check_dependencies():
        return False
    
    print("🚀 Starting O-Nakala Core Web Server...")
    print(f"📍 Server will be available at: http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"🌐 Web Interface: Open web/index.html in your browser")
    print("=" * 60)
    
    try:
        # Import and start the web API
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        from nakala_client.web_api import main
        
        # Set command line arguments for the web API
        sys.argv = ['web_api.py', '--host', host, '--port', str(port)]
        if debug:
            sys.argv.append('--debug')
        
        main()
        
    except ImportError as e:
        print(f"❌ Failed to import O-Nakala Core modules: {e}")
        print("💡 Make sure you're in the correct directory and the package is installed:")
        print("   pip install -e .")
        return False
    except KeyboardInterrupt:
        print("\n👋 Stopping O-Nakala Core Web Server...")
        return True
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="O-Nakala Core Web Server Launcher")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to (default: 8000)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    success = start_server(args.host, args.port, args.debug)
    sys.exit(0 if success else 1)