#!/bin/bash

# 🦫 File created by 𝖇𝖑4𝖘𝖘
# GitHub: https://github.com/IlyVoid

# Prompt the user for the ZIP file
read -p "Enter the path to the ZIP file: " ZIPFILE

# Check if the ZIP file exists
if [ ! -f "$ZIPFILE" ]; then
    echo "ZIP file not found!"
    exit 1
fi

# Prompt the user for the wordlist
read -p "Enter the path to the password wordlist: " WORDLIST

# Check if the wordlist exists
if [ ! -f "$WORDLIST" ]; then
    echo "Password list not found!"
    exit 1
fi

# Function to test passwords
test_password() {
    PASSWORD=$1
    if unzip -P "$PASSWORD" -t "$ZIPFILE" > /dev/null 2>&1; then
        echo "[+] Success! Password found: $PASSWORD"
        exit 0
    fi
}

export -f test_password  # Export the function for xargs

# Run in parallel
cat "$WORDLIST" | xargs -n 1 -P 10 bash -c 'test_password "$@"' _ 

echo "Password not found in the wordlist."
