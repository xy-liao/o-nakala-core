#!/bin/bash
# Setup script for O-Nakala Core Examples

echo "Setting up O-Nakala Core Examples environment..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing required packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete!"
echo ""
echo "To use the examples:"
echo "1. Activate the environment: source venv/bin/activate"
echo "2. Start Jupyter: jupyter lab"
echo "3. Open notebooks/workflow_notebook.ipynb"
echo ""
echo "Ready to run O-Nakala Core workflows!"