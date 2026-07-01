#!/usr/bin/env python
"""
Quick verification script to check that the PPE Detection system is properly set up.
Run this before reporting issues.
"""

import sys
from pathlib import Path

def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    print(f"❌ Python {version.major}.{version.minor} - Need 3.10+")
    return False

def check_dependencies():
    """Check required dependencies."""
    deps_map = {
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn',
        'opencv-python': 'cv2',
        'ultralytics': 'ultralytics',
        'numpy': 'numpy',
        'pydantic': 'pydantic',
        'pyyaml': 'yaml',
    }
    
    missing = []
    for name, import_name in deps_map.items():
        try:
            __import__(import_name)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - Missing")
            missing.append(name)
    
    return len(missing) == 0

def check_files():
    """Check project structure."""
    root = Path(__file__).parent
    required_dirs = [
        'app',
        'app/core',
        'app/models',
        'app/services',
        'app/utils',
        'app/api',
        'app/static',
        'tests',
        'weights',
        'output',
        'logs',
    ]
    
    required_files = [
        'config.yaml',
        'run.py',
        'requirements.txt',
        'app/static/index.html',
        'app/static/style.css',
        'app/static/app.js',
    ]
    
    all_ok = True
    
    for dir_path in required_dirs:
        full_path = root / dir_path
        if full_path.exists():
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/ - Missing")
            all_ok = False
    
    for file_path in required_files:
        full_path = root / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Missing")
            all_ok = False
    
    return all_ok

def check_config():
    """Check configuration."""
    try:
        from app.core.settings import load_config
        config = load_config()
        print(f"✅ Configuration loaded")
        print(f"   Model: {config.model.path}")
        print(f"   Device: {config.model.device}")
        print(f"   Confidence: {config.model.confidence_threshold}")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def check_model():
    """Check model file."""
    model_path = Path(__file__).parent / 'weights' / 'best.pt'
    if model_path.exists():
        size_mb = model_path.stat().st_size / (1024 * 1024)
        print(f"✅ Model file ({size_mb:.1f} MB)")
        return True
    else:
        print(f"❌ Model file missing: {model_path}")
        return False

def check_app():
    """Check app initialization."""
    try:
        from run import create_app
        app = create_app()
        print(f"✅ App initialized ({len(app.routes)} routes)")
        return True
    except Exception as e:
        print(f"❌ App initialization failed: {e}")
        return False

def main():
    """Run all checks."""
    print("\n" + "="*50)
    print("PPE Detection System - Health Check")
    print("="*50 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Project Structure", check_files),
        ("Configuration", check_config),
        ("Model File", check_model),
        ("App Initialization", check_app),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append(False)
    
    print("\n" + "="*50)
    passed = sum(results)
    total = len(results)
    
    if all(results):
        print(f"✅ All checks passed! ({passed}/{total})")
        print("\nYou can now run:")
        print("  python run.py")
        print("\nThen open:")
        print("  http://127.0.0.1:8000")
        return 0
    else:
        print(f"⚠️  Some checks failed ({passed}/{total})")
        print("\nSee above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
