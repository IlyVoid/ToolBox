#!/bin/bash

# Set up a hidden virtual environment in the home directory
VENV_DIR="$HOME/.Vuln"

# Check for Python3
if ! command -v python3 &>/dev/null; then
    echo "Python3 not found. Install it and try again."
    exit 1
fi

# Create a hidden virtual environment if it doesn’t exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating a hidden virtual environment in $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
else
    echo "Virtual environment already exists at $VENV_DIR. Skipping creation."
fi

# Activate the virtual environment and install dependencies
source "$VENV_DIR/bin/activate"
echo "Installing required libraries in the virtual environment..."
pip install requests regex argparse colorama beautifulsoup4 pyfiglet rich

# Set up a symbolic link to the Vulnity main script in a global directory
VULNITY_PATH="$PWD/main.py"
BIN_DIR="$HOME/.local/bin"

# Ensure the bin directory exists
mkdir -p "$BIN_DIR"
ln -sf "$VULNITY_PATH" "$BIN_DIR/vulnity"

# Add $BIN_DIR to PATH in .zshrc if not already there
ZSHRC="$HOME/.zshrc"
if ! grep -q "$BIN_DIR" "$ZSHRC"; then
    echo "export PATH=\"\$PATH:$BIN_DIR\"" >> "$ZSHRC"
    echo "Added $BIN_DIR to PATH in $ZSHRC"
else
    echo "$BIN_DIR is already in your PATH."
fi

echo "Installation complete. Open a new terminal session or manually run 'source ~/.zshrc' to enable 'vulnity' command globally."
