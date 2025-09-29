#!/bin/bash

echo "========================================"
echo "Python App to Binary Converter for Linux"
echo "========================================"

echo
echo "[1/4] Activating Python virtual environment..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment!"
    exit 1
fi

echo
echo "[2/4] Installing required packages (psutil and pyinstaller)..."
pip install psutil pyinstaller

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install packages!"
    exit 1
fi

echo
echo "[3/4] Converting app.py to flowbit binary..."
pyinstaller --onefile --noconsole --name flowbit app.py

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create binary!"
    exit 1
fi

echo
echo "[4/4] Build completed successfully!"
echo
echo "Binary created at: dist/flowbit"
echo
echo "You can find your executable in the 'dist' folder."
echo "To run it: ./dist/flowbit"
echo

echo "Press Enter to continue..."
read