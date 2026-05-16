"""
Quick test script to verify all dependencies are installed
Run this after installation completes
"""

def test_imports():
    """Test if all required packages can be imported"""
    packages = {
        'numpy': 'NumPy',
        'cv2': 'OpenCV',
        'scipy': 'SciPy',
        'sklearn': 'Scikit-learn',
        'imutils': 'Imutils'
    }
    
    print("Testing package imports...")
    print("-" * 50)
    
    failed = []
    for module, name in packages.items():
        try:
            __import__(module)
            print(f"✓ {name:20} - OK")
        except ImportError as e:
            print(f"✗ {name:20} - FAILED: {e}")
            failed.append(name)
    
    print("-" * 50)
    
    if failed:
        print(f"\n❌ {len(failed)} package(s) missing:")
        for name in failed:
            print(f"   - {name}")
        return False
    else:
        print("\n✓ All dependencies installed successfully!")
        return True


if __name__ == "__main__":
    success = test_imports()
    exit(0 if success else 1)
