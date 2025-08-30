#!/usr/bin/env python3
"""
O-Nakala Core Enhanced Workflow Demo

Demonstrates the streamlined workflow with intelligent metadata enhancement
integrated directly into the preview tool.
"""

import os
import sys
import subprocess
from pathlib import Path

def demo_enhanced_workflow():
    """Demonstrate the enhanced workflow."""
    
    print("🎉 O-Nakala Core Enhanced Workflow")
    print("=" * 50)
    print()
    
    # Paths
    dataset_dir = Path("../sample_dataset")
    csv_file = dataset_dir / "folder_data_items.csv"
    
    print("🎯 Enhanced Workflow Features:")
    print("  ✅ Intelligent metadata enhancement (content-aware)")
    print("  ✅ Integrated enhancement in preview tool")
    print("  ✅ Preview with enhancement suggestions")
    print("  ✅ Interactive or automatic enhancement application")
    print("  ✅ Streamlined workflow")
    print()
    
    print("📋 Streamlined Workflow:")
    print("  1. o-nakala-preview --csv data.csv --enhance --interactive")
    print("  2. o-nakala-upload --csv data_enhanced.csv --api-key KEY")
    print("  ✨ Enhancement built into preview tool!")
    print()
    
    # Demo the enhanced preview (non-interactive for demo)
    print("🔍 DEMO: Enhanced Preview Tool")
    print("-" * 40)
    
    if csv_file.exists():
        print(f"Analyzing: {csv_file}")
        print("Running: o-nakala-preview --csv {csv_file} --enhance")
        print()
        
        # Run enhanced preview in non-interactive mode
        try:
            env = os.environ.copy()
            
            result = subprocess.run([
                'o-nakala-preview',
                '--csv', str(csv_file),
                '--enhance'
            ], 
            capture_output=True, 
            text=True, 
            timeout=10,
            env=env
            )
            
            if result.returncode == 0:
                print("✅ Enhanced preview completed successfully!")
                print()
                print("📊 Preview Output:")
                print(result.stdout)
            else:
                print("⚠️  Preview output (may include enhancements):")
                print(result.stdout)
                if result.stderr:
                    print("Errors:", result.stderr)
                    
        except subprocess.TimeoutExpired:
            print("⏱️  Preview completed (timeout reached)")
        except Exception as e:
            print(f"⚠️  Demo error: {e}")
    else:
        print(f"❌ Sample CSV not found: {csv_file}")
        print("Please ensure you're running from examples/notebooks/")
    
    print()
    print("💡 Key Enhancement Features:")
    print("  🧠 Content-aware enhancement (detects: code, images, documents, data, presentations)")
    print("  🎨 Professional multilingual metadata generation")
    print("  ⚡ Auto-application of high-confidence improvements")
    print("  🤝 Interactive mode for researcher control")
    print("  📁 Original files preserved, enhanced versions created")
    print()
    
    print("🎯 Next Steps:")
    print("  1. Try: o-nakala-preview --csv your_data.csv --enhance --interactive")
    print("  2. Apply enhancements and preview JSON")
    print("  3. Upload with confidence: o-nakala-upload --csv your_data_enhanced.csv")
    print()
    
    print("✨ Enhancement Features Integrated into Preview Tool!")

if __name__ == "__main__":
    demo_enhanced_workflow()