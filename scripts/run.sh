#!/bin/bash

# Define the path to the src directory
SRC_DIR="src"

ls -a

# Ensure the virtual environment exists
if [ ! -d "$SRC_DIR/venv" ]; then
    echo "Virtual environment not found in $SRC_DIR. Please run 'setup_venv.sh' first."
    exit 1
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source "$SRC_DIR/venv/bin/activate" || { echo "Failed to activate virtual environment!"; exit 1; }

# Run the game
echo "Starting the game..."
python "$SRC_DIR/main.py" || { echo "Game execution failed!"; deactivate; exit 1; }

# Deactivate the virtual environment after the game exits
echo "Deactivating virtual environment..."
deactivate
