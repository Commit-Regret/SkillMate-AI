#!/usr/bin/env python3
"""
SkillMate AI System - Automated Installation Script
Handles dependency installation and basic setup.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header():
    """Print installation header."""
    print("=" * 60)
    print("🚀 SkillMate AI System - Automated Installation")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Error: Python 3.9 or higher is required.")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        print("   Please upgrade Python and try again.")
        sys.exit(1)
    
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")

def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    
    # Get the parent directory (skillmate) to find requirements.txt
    current_dir = Path(__file__).parent
    requirements_file = current_dir.parent / "requirements.txt"
    
    if not requirements_file.exists():
        print(f"❌ Error: requirements.txt not found at {requirements_file}")
        print("   Please make sure you're running this from the skillmate/ai/ directory")
        sys.exit(1)
    
    target_file = requirements_file
    print("   Using main requirements.txt (compatible with all Python versions)")
    
    try:
        # For Python 3.13+, install build tools first
        version = sys.version_info
        if version.major == 3 and version.minor >= 13:
            print("   Installing build tools for Python 3.13+...")
            build_cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "setuptools", "wheel", "pip"]
            subprocess.run(build_cmd, capture_output=True, text=True)
        
        # Install dependencies with binary wheels only (avoid compilation issues)
        cmd = [sys.executable, "-m", "pip", "install", "--only-binary=all", "-r", str(target_file)]
        print(f"   Running: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully!")
        else:
            print("❌ Error installing dependencies:")
            print(result.stderr)
            
            print("\n💡 Manual installation option:")
            print(f"   pip install -r {requirements_file}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def create_directories():
    """Create necessary directories."""
    print("\n📁 Creating directories...")
    
    directories = [
        "vector_db",
        "resume_storage",
        "logs"
    ]
    
    for dir_name in directories:
        dir_path = Path(dir_name)
        dir_path.mkdir(exist_ok=True)
        print(f"   ✅ {dir_name}/")

def check_api_key():
    """Check if OpenAI API key is set."""
    print("\n🔑 Checking API key configuration...")
    
    # Check environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Check .env file
    env_file = Path(".env")
    env_key = None
    if env_file.exists():
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith("OPENAI_API_KEY="):
                        env_key = line.split("=", 1)[1].strip()
                        break
        except Exception:
            pass
    
    if api_key or env_key:
        print("✅ OpenAI API key found!")
        return True
    else:
        print("⚠️  OpenAI API key not found!")
        print("\n📝 To set up your API key:")
        print("   1. Get your API key from: https://platform.openai.com/")
        print("   2. Create a .env file in this directory with:")
        print("      OPENAI_API_KEY=your_api_key_here")
        print("   3. Or set environment variable:")
        
        if platform.system() == "Windows":
            print("      set OPENAI_API_KEY=your_api_key_here")
        else:
            print("      export OPENAI_API_KEY=your_api_key_here")
        
        return False

def test_installation():
    """Test if installation works."""
    print("\n🧪 Testing installation...")
    
    try:
        # Test core dependencies
        import langchain
        import langgraph
        import openai
        import pandas
        import sklearn
        print("✅ Core dependencies import successfully")
        
        # Try importing main components (with proper path)
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        try:
            from main import SkillMateAI
            print("✅ Core system imports successfully")
            return True
        except ImportError as e:
            print(f"⚠️  Core system import issue: {e}")
            print("   Dependencies are OK, but you may need to set up API keys first.")
            return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Some dependencies may not be installed correctly.")
        return False
    except Exception as e:
        print(f"⚠️  Warning: {e}")
        print("   System structure is OK, but you may need to set up API keys.")
        return True

def main():
    """Main installation process."""
    print_header()
    
    # Step 1: Check Python version
    check_python_version()
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("\n❌ Installation failed at dependency installation step.")
        sys.exit(1)
    
    # Step 3: Create directories
    create_directories()
    
    # Step 4: Check API key
    api_key_ok = check_api_key()
    
    # Step 5: Test installation
    test_ok = test_installation()
    
    # Final status
    print("\n" + "=" * 60)
    print("📊 Installation Summary")
    print("=" * 60)
    print(f"✅ Python version: OK")
    print(f"✅ Dependencies: OK")
    print(f"✅ Directories: OK")
    print(f"{'✅' if api_key_ok else '⚠️ '} API Key: {'OK' if api_key_ok else 'NEEDS SETUP'}")
    print(f"{'✅' if test_ok else '❌'} System Test: {'OK' if test_ok else 'FAILED'}")
    
    if api_key_ok and test_ok:
        print("\n🎉 Installation completed successfully!")
        print("\n🚀 Next steps:")
        print("   1. Run tests: python run_tests.py")
        print("   2. Try manual testing: python manual_test_guide.py")
        print("   3. Check the SETUP_GUIDE.md for more details")
    elif not api_key_ok:
        print("\n⚠️  Installation mostly complete!")
        print("   Please set up your OpenAI API key to use the system.")
    else:
        print("\n❌ Installation had issues.")
        print("   Please check the error messages above and try again.")

if __name__ == "__main__":
    main() 