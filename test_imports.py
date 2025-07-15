#!/usr/bin/env python3
"""
Test script to verify all dependencies for MLSPred-Bench are working correctly
"""

print("=" * 60)
print("MLSPred-Bench Dependencies Test")
print("=" * 60)

print("\nTesting core dependencies...")

# Test 1: NumPy
try:
    import numpy as np
    print(f"✅ NumPy {np.__version__} - OK")
except ImportError as e:
    print(f"❌ NumPy - FAILED: {e}")

# Test 2: H5PY
try:
    import h5py
    print(f"✅ H5PY {h5py.__version__} - OK")
except ImportError as e:
    print(f"❌ H5PY - FAILED: {e}")

# Test 3: MNE
try:
    import mne
    print(f"✅ MNE {mne.__version__} - OK")
except ImportError as e:
    print(f"❌ MNE - FAILED: {e}")

# Test 4: Scikit-learn
try:
    import sklearn
    from sklearn.preprocessing import scale, minmax_scale
    from sklearn.utils import shuffle
    print(f"✅ Scikit-learn {sklearn.__version__} - OK")
except ImportError as e:
    print(f"❌ Scikit-learn - FAILED: {e}")

# Test 5: SciPy
try:
    import scipy
    print(f"✅ SciPy {scipy.__version__} - OK")
except ImportError as e:
    print(f"❌ SciPy - FAILED: {e}")

# Test 6: Standard library modules
try:
    import random, csv, os, time
    print("✅ Standard library modules (random, csv, os, time) - OK")
except ImportError as e:
    print(f"❌ Standard library modules - FAILED: {e}")

# Test 7: Optional dependencies
optional_deps = [
    ("matplotlib", "matplotlib"),
    ("joblib", "joblib"),
    ("tqdm", "tqdm"),
    ("requests", "requests")
]

print("\nTesting optional dependencies...")
for name, module in optional_deps:
    try:
        mod = __import__(module)
        version = getattr(mod, '__version__', 'unknown')
        print(f"✅ {name} {version} - OK")
    except ImportError as e:
        print(f"⚠️  {name} - NOT FOUND (optional)")

print("\n" + "=" * 60)
print("Dependency test completed!")
print("=" * 60)
