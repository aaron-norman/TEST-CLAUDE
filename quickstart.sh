#!/bin/bash
# Quickstart script for Notary Invoice Generator

echo "=== Notary Invoice Generator - Quickstart ==="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.7 or higher and try again."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "Error: pip is not installed."
    echo "Please install pip and try again."
    exit 1
fi

echo "✓ pip found"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt || pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "Error: Failed to install dependencies."
    echo "You may need to install system dependencies first."
    echo ""
    echo "On Ubuntu/Debian:"
    echo "  sudo apt-get install python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0"
    echo ""
    echo "On macOS:"
    echo "  brew install cairo pango gdk-pixbuf libffi"
    exit 1
fi

echo ""
echo "✓ Dependencies installed successfully!"
echo ""
echo "Next steps:"
echo "1. Edit config.yaml with your business information"
echo "2. Run: python3 invoice_generator.py --interactive"
echo "   OR"
echo "   Run: python3 example_usage.py (to see examples)"
echo ""
echo "For detailed usage instructions, see README.md"
