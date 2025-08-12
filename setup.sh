#!/bin/bash
# Terminal Command Menu - Setup Script
# This script sets up the virtual environment and installs the package

set -e  # Exit on any error

echo "🚀 Setting up Terminal Command Menu..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    echo "Please install Python 3.8 or higher and try again."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python $required_version or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python $python_version detected"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install the package in development mode
echo "📥 Installing Terminal Command Menu..."
pip install -e .

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To use Terminal Command Menu:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the application: history-menu"
echo ""
echo "To deactivate the virtual environment later: deactivate"
echo ""
echo "📚 For more information, see README.md"
