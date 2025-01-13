#!/bin/bash

# Navigate to the 'src' directory
cd src || { echo "Directory 'src' not found!"; exit 1; }

# Create a virtual environment if it doesn't already exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv || { echo "Failed to create virtual environment!"; exit 1; }
else
    echo "Virtual environment already exists."
fi

echo "Activating virtual environment..."
source venv/bin/activate || { echo "Failed to activate virtual environment!"; exit 1; }

if [ -f "requirements.txt" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt || { echo "Dependency installation failed!"; exit 1; }
else
    echo "'requirements.txt' not found. Skipping dependency installation."
fi

# Verify environment is ready
echo "Verifying environment..."
if [ -f venv/bin/python ] && pip check; then
    echo "Virtual environment is ready and verified!"
else
    echo "Environment verification failed. Please check setup."
    deactivate
    exit 1
fi
