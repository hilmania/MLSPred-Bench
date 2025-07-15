#!/bin/bash

# MLSPred-Bench Setup Script
# This script helps setup the environment for MLSPred-Bench

echo "================================================"
echo "MLSPred-Bench Environment Setup"
echo "================================================"

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
echo "Detected Python version: $python_version"

# Check if Python version is compatible
if python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "✅ Python version is compatible (>= 3.8)"
else
    echo "❌ Python version is too old. Please use Python 3.8 or higher."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".mlspredbench" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .mlspredbench
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .mlspredbench/bin/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
python -m pip install -r requirements.txt

echo ""
echo "================================================"
echo "Setup completed!"
echo "================================================"
echo ""
echo "To use MLSPred-Bench:"
echo "1. Activate the virtual environment:"
echo "   source .mlspredbench/bin/activate"
echo ""
echo "2. Run the main script:"
echo "   python mlspred_bench_v001.py [TUSZ_DATA_PATH] [OUTPUT_PATH]"
echo ""
echo "3. To test dependencies:"
echo "   python test_imports.py"
echo ""
