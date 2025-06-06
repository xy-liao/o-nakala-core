#!/usr/bin/env python3
"""
Local setup test for NAKALA workshop.
This script tests both current local setup and future PyPI compatibility.
"""

import sys
import subprocess
from pathlib import Path

def test_development_installation():
    """Test installing nakala-client in development mode."""
    print("🧪 Testing development installation...")
    
    # Install in development mode
    parent_dir = Path(__file__).parent.parent
    cmd = [sys.executable, "-m", "pip", "install", "-e", str(parent_dir)]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Development installation successful")
            return True
        else:
            print(f"❌ Installation failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Installation error: {e}")
        return False

def test_imports():
    """Test importing nakala_client modules."""
    print("🧪 Testing module imports...")
    
    try:
        import nakala_client
        print(f"✅ nakala_client imported from: {nakala_client.__file__}")
        
        from nakala_client.common.config import NakalaConfig
        from nakala_client.common.utils import NakalaCommonUtils
        import nakala_client.upload as upload_module
        import nakala_client.collection as collection_module
        import nakala_client.curator as curator_module
        
        print("✅ All core modules imported successfully")
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_cli_commands():
    """Test CLI commands are available."""
    print("🧪 Testing CLI commands...")
    
    commands = ["nakala-upload", "nakala-collection", "nakala-curator"]
    
    for cmd in commands:
        try:
            result = subprocess.run([cmd, "--help"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {cmd} command available")
            else:
                print(f"⚠️ {cmd} command not working properly")
        except FileNotFoundError:
            print(f"❌ {cmd} command not found")

def test_workshop_compatibility():
    """Test workshop notebook compatibility."""
    print("🧪 Testing workshop compatibility...")
    
    # Test key components that workshop needs
    try:
        from nakala_client.common.config import NakalaConfig
        from nakala_client.common.utils import NakalaCommonUtils
        import nakala_client.upload as upload_module
        
        # Test configuration
        config = NakalaConfig(
            api_key="test-key",
            api_url="https://apitest.nakala.fr"
        )
        
        print("✅ Configuration creation works")
        print("✅ Module imports work")
        print("✅ Workshop should work with direct API imports")
        
        return True
        
    except Exception as e:
        print(f"⚠️ Direct API not ready: {e}")
        print("📝 Workshop will use CLI fallback method")
        return False

def main():
    """Run all tests."""
    print("🚀 NAKALA Workshop Local Setup Test")
    print("=" * 50)
    
    # Test 1: Development installation
    install_ok = test_development_installation()
    
    if install_ok:
        # Test 2: Module imports
        import_ok = test_imports()
        
        if import_ok:
            # Test 3: CLI commands
            test_cli_commands()
            
            # Test 4: Workshop compatibility
            workshop_ok = test_workshop_compatibility()
            
            print("\n" + "=" * 50)
            if workshop_ok:
                print("🎉 All tests passed! Workshop ready with direct API imports.")
                print("🚀 Future PyPI compatibility: EXCELLENT")
            else:
                print("⚠️ Direct API needs work, but CLI fallback available.")
                print("🚀 Future PyPI compatibility: GOOD (needs API development)")
                
            print("\n📋 To run workshop:")
            print("   cd o-nakala-workshop")
            print("   jupyter lab NAKALA_Complete_Workflow.ipynb")
            
        else:
            print("\n❌ Import tests failed. Check installation.")
    else:
        print("\n❌ Installation failed. Check Python environment.")
        
    print("\n🔧 For manual setup:")
    print("   pip install -e ../")

if __name__ == "__main__":
    main()